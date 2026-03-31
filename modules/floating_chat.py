import streamlit as st
import streamlit.components.v1 as components
import base64
import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import GEMINI_API_KEY, GROQ_API_KEY


def _get_avatar_b64():
    path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'assets', 'doctor_avatar.png'
    )
    if os.path.exists(path):
        with open(path, 'rb') as f:
            return base64.b64encode(f.read()).decode('ascii')
    return None


def _call_ai_server(message: str, history: list, sys_prompt: str) -> str:
    """
    Server-side AI call. API keys NEVER leave the server.
    Tries Groq first, then Gemini with key rotation.
    """
    from config.settings import GEMINI_API_KEYS

    messages = [{"role": "system", "content": sys_prompt}] + history[-6:] + [{"role": "user", "content": message}]

    # Try Groq first
    if GROQ_API_KEY:
        try:
            from groq import Groq
            client = Groq(api_key=GROQ_API_KEY)
            response = client.chat.completions.create(
                messages=messages,
                model="llama-3.3-70b-versatile",
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            pass  # Fall through to Gemini

    # Try Gemini key pool
    keys = GEMINI_API_KEYS if GEMINI_API_KEYS else ([GEMINI_API_KEY] if GEMINI_API_KEY else [])
    if not keys:
        return "I'm currently unavailable — no AI API keys are configured. Please try again later. ⚠️"

    for api_key in keys:
        try:
            from google import genai
            client = genai.Client(api_key=api_key)
            prompt = "\n".join([f"{m['role']}: {m['content']}" for m in messages])
            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=prompt
            )
            return response.text.strip()
        except Exception as e:
            error_msg = str(e).lower()
            if "429" in error_msg or "resource_exhausted" in error_msg:
                continue
            return f"I encountered an issue. Please try again in a moment! ⚠️"

    return "I'm taking a quick break to recharge! Please try again in 60 seconds. ☕"


def render_floating_chatbot(context: dict = None):
    """Floating doctor chatbot widget. API calls are proxied server-side for security."""
    b64 = _get_avatar_b64()

    # Format context
    context_str = "None"
    if context:
        symptoms_list = context.get('symptoms', [])
        symptoms = ", ".join(symptoms_list) if isinstance(symptoms_list, list) else str(symptoms_list)
        preds_list = context.get('predictions', [])
        predictions = ", ".join([f"{p['disease']} ({p.get('confidence',0)}%)" for p in (preds_list[:3] if isinstance(preds_list, list) else [])])
        context_str = f"Symptoms: {symptoms} | Top Predictions: {predictions}"

    # System prompt
    sys_prompt = "You are Dr. Docyote, a friendly AI medical assistant. Give concise helpful answers with emojis. Always advise seeing a real doctor for serious concerns. For emergencies, advise calling emergency services immediately. Respond in the user's language."
    if context_str != "None":
        sys_prompt += " The user just ran a symptom check. " + context_str + ". Use this context to answer follow-up questions."

    welcome_msg = "Hi! 👋 I'm Dr. Docyote, your AI health assistant!\n\nAsk me about symptoms, diseases, home remedies, or any health question. I'm here to help! 🪴"

    # ── Server-side chat handler (Streamlit session state) ──
    if "drd_history" not in st.session_state:
        st.session_state.drd_history = []
    if "drd_sys_prompt" not in st.session_state:
        st.session_state.drd_sys_prompt = sys_prompt
    else:
        st.session_state.drd_sys_prompt = sys_prompt  # Update context each render

    # ── Client-to-Server Bridge ──
    # We use a hidden form to allow JS to submit messages to Python
    st.markdown("""
        <style>
        div[data-testid="stForm"]:has(.drd-bridge-marker) {
            display: none !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    with st.form("drd_hidden_form", clear_on_submit=True):
        st.markdown("<div class='drd-bridge-marker'></div>", unsafe_allow_html=True)
        bridge_input = st.text_input("msg", key="drd_bridge_input")
        submitted = st.form_submit_button("Send", key="drd_bridge_submit")
        
    if submitted and bridge_input:
        st.session_state.drd_history.append({"role": "user", "content": bridge_input})
        bot_response = _call_ai_server(bridge_input, st.session_state.drd_history, st.session_state.drd_sys_prompt)
        st.session_state.drd_history.append({"role": "assistant", "content": bot_response})
        st.rerun()

    # ── Build avatar HTML ──
    if b64:
        av_img = 'data:image/png;base64,' + b64
        av_fab = '<img src="' + av_img + '" style="width:100%;height:100%;object-fit:cover;border-radius:50%;" alt="Dr.">'
        av_small = '<img src="' + av_img + '" style="width:100%;height:100%;object-fit:cover;border-radius:9px;" alt="Dr.">'
    else:
        av_fab = '<span style="font-size:1.6rem;">&#128104;&#8205;&#9877;&#65039;</span>'
        av_small = '<span style="font-size:0.85rem;">&#128104;&#8205;&#9877;&#65039;</span>'

    # Build chat history as JSON for JS (no API keys!)
    history_json = json.dumps(st.session_state.drd_history)
    context_str_js = json.dumps(context_str)
    welcome_msg_js = json.dumps(welcome_msg)
    av_small_js = json.dumps(av_small)

    widget_html = f"""
<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body>
<script>
(function() {{
  var doc = window.parent.document;

  function togglePanel() {{
    var fab = doc.getElementById('drd-fab');
    var panel = doc.getElementById('drd-panel');
    var tip = doc.getElementById('drd-tip');
    var inp = doc.getElementById('drd-inp');

    var isOpen = panel.classList.toggle('drd-open');
    if (isOpen) {{
      fab.style.animation = 'none';
      fab.style.transform = 'rotate(15deg) scale(0.9)';
      if (tip) tip.style.display = 'none';
      setTimeout(function() {{ inp.focus(); }}, 350);
    }} else {{
      fab.style.animation = 'drdFloat 3.5s ease-in-out infinite';
      fab.style.transform = '';
    }}
  }}

  function addMsg(role, text) {{
    var msgs = doc.getElementById('drd-msgs');
    var div = doc.createElement('div');
    div.className = 'drd-msg' + (role === 'user' ? ' drd-u' : '');
    var avHtml = role === 'user' ? '<span style="font-size:0.75rem;">&#128100;</span>' : {av_small_js};
    div.innerHTML = '<div class="drd-av">' + avHtml + '</div><div class="drd-bubble">' + text.replace(/\\n/g, '<br>') + '</div>';
    msgs.appendChild(div);
    msgs.scrollTop = msgs.scrollHeight;
  }}

  // Server-side chat: uses Streamlit's session state via hidden text input + button
  function sendMessage() {{
    var inp = doc.getElementById('drd-inp');
    var msgs = doc.getElementById('drd-msgs');
    var sendBtn = doc.getElementById('drd-send');

    var val = inp.value.trim();
    if (!val) return;
    inp.value = '';
    addMsg('user', val);
    sendBtn.disabled = true;

    // Typing indicator
    var typ = doc.createElement('div');
    typ.className = 'drd-msg';
    typ.id = 'drd-typing';
    typ.innerHTML = '<div class="drd-av">{av_small}</div><div class="drd-bubble"><div class="drd-typing"><span></span><span></span><span></span></div></div>';
    msgs.appendChild(typ);
    msgs.scrollTop = msgs.scrollHeight;

    // Find the hidden Streamlit input and button
    var pyInput = null;
    var pySubmit = null;
    
    // Find the marker and walk up
    var marker = doc.querySelector('.drd-bridge-marker');
    if (marker) {{
      var formContainer = marker.closest('[data-testid="stForm"]') || 
                          marker.closest('form') || 
                          marker.parentElement.parentElement.parentElement.parentElement;
                          
      if (formContainer) {{
         pyInput = formContainer.querySelector('input');
         var buttons = formContainer.querySelectorAll('button');
         pySubmit = buttons.length > 0 ? buttons[buttons.length - 1] : null;
      }}
    }}

    if (pyInput && pySubmit) {{
      // React needs native setter called to register the value change
      var nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, "value").set;
      nativeInputValueSetter.call(pyInput, val);
      pyInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
      // Click the submit button to tell python
      pySubmit.click();
    }} else {{
       // fallback error message
       setTimeout(function() {{
         var typEl = doc.getElementById('drd-typing');
         if (typEl) typEl.remove();
         addMsg('bot', 'Bridge offline. Please try the native expander. ⚠️');
         sendBtn.disabled = false;
       }}, 1500);
    }}
  }}

  // --- Update-if-exists Logic ---
  var existing = doc.getElementById('drd-fab');
  if (existing) {{
    existing.onclick = togglePanel;
    doc.getElementById('drd-close-btn').onclick = togglePanel;

    var sendBtn = doc.getElementById('drd-send');
    if (sendBtn) sendBtn.onclick = sendMessage;

    var inp = doc.getElementById('drd-inp');
    if (inp) {{
      inp.onkeydown = function(e) {{
        if (e.key === 'Enter' && !e.shiftKey) {{
          e.preventDefault();
          sendMessage();
        }}
      }};
    }}

    // Completely rebuild chat to avoid duplicates when JS runs ahead of Python
    var serverHistory = {history_json};
    var existingMsgCount = parseInt(doc.body.__drd_msg_count || '0');
    
    if (serverHistory.length > existingMsgCount || serverHistory.length < existingMsgCount) {{
      var msgs = doc.getElementById('drd-msgs');
      msgs.innerHTML = '';
      for (var i = 0; i < serverHistory.length; i++) {{
        addMsg(serverHistory[i].role === 'assistant' ? 'bot' : 'user', serverHistory[i].content);
      }}
      doc.body.__drd_msg_count = serverHistory.length.toString();
    }}
    
    // Remove typing indicator if present
    var typEl = doc.getElementById('drd-typing');
    if (typEl) typEl.remove();
    
    // Re-enable send button
    var sendBtn = doc.getElementById('drd-send');
    if (sendBtn) sendBtn.disabled = false;

    var newContext = {context_str_js};
    if (newContext !== "None" && doc.body.__drd_last_notified !== newContext) {{
      doc.body.__drd_last_notified = newContext;
      var msg = 'I see you just updated your symptoms: ' + newContext.split('|')[0].replace('Symptoms:', '') + '. How can I help?';
      addMsg('bot', msg);
    }}
    return;
  }}

  console.log('Dr. Docyote: Injecting into parent...');

  // --- Inject CSS into parent ---
  var style = doc.createElement('style');
  style.id = 'drd-styles';
  style.textContent = `
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700&display=swap');

    #drd-fab {{
      position: fixed; bottom: 28px; right: 28px; width: 64px; height: 64px; border-radius: 50%;
      background: linear-gradient(145deg, #6C63FF, #4B45B2);
      box-shadow: 0 8px 32px rgba(108,99,255,0.45); cursor: pointer; z-index: 999999;
      display: flex; align-items: center; justify-content: center;
      border: 3px solid rgba(255,255,255,0.2); overflow: hidden;
      animation: drdFloat 3.5s ease-in-out infinite;
      transition: transform 0.3s, background 0.3s;
    }}
    #drd-fab:hover {{ transform: scale(1.05); background: linear-gradient(145deg, #7B73FF, #5A51C3); }}
    #drd-dot {{
      position: fixed; bottom: 74px; right: 28px; width: 14px; height: 14px; background: #00D68F;
      border-radius: 50%; border: 2px solid #0d1117; z-index: 1000000; box-shadow: 0 0 10px #00D68F;
    }}
    #drd-tip {{
      position: fixed; bottom: 42px; right: 108px; background: #1A1D29; color: #FAFAFA;
      padding: 10px 18px; border-radius: 12px; font-size: 0.82rem; font-weight: 600;
      box-shadow: 0 4px 20px rgba(0,0,0,0.3); border: 1px solid rgba(108,99,255,0.2);
      z-index: 999998; pointer-events: none; transition: opacity 0.6s, transform 0.6s;
      animation: drdIn 0.5s ease; font-family: 'Plus Jakarta Sans', sans-serif;
    }}
    #drd-tip::after {{
      content: ''; position: absolute; right: -14px; top: 12px;
      border-left: 14px solid #1A1D29; border-top: 8px solid transparent; border-bottom: 8px solid transparent;
    }}
    #drd-panel {{
      position: fixed; bottom: 105px; right: 28px; width: 380px; height: 520px;
      background: #0d1117; border-radius: 24px; box-shadow: 0 12px 60px rgba(0,0,0,0.6);
      z-index: 1000001; display: flex; flex-direction: column; overflow: hidden;
      transform: translateY(20px) scale(0.95); opacity: 0; pointer-events: none;
      transition: all 0.35s cubic-bezier(0.18, 0.89, 0.32, 1.28);
      border: 1px solid rgba(108,99,255,0.15); font-family: 'Plus Jakarta Sans', sans-serif;
    }}
    #drd-panel.drd-open {{ transform: translateY(0) scale(1); opacity: 1; pointer-events: all; }}

    .drd-hdr {{
      padding: 18px 20px; background: rgba(26,29,41,0.7); backdrop-filter: blur(12px);
      display: flex; align-items: center; gap: 14px;
      border-bottom: 1px solid rgba(108,99,255,0.12); flex-shrink: 0;
    }}
    .drd-hav {{
      width: 44px; height: 44px; border-radius: 14px;
      background: linear-gradient(135deg, #6C63FF, #4B45B2);
      display: flex; align-items: center; justify-content: center; font-size: 1.4rem;
      overflow: hidden; box-shadow: 0 4px 16px rgba(108,99,255,0.3); flex-shrink: 0;
    }}
    .drd-hdr h3 {{ color: #FAFAFA; font-size: 1rem; font-weight: 700; margin: 0 0 2px; }}
    .drd-status {{ display: flex; align-items: center; gap: 5px; font-size: 0.75rem; color: #00D68F; font-weight: 500; }}
    .drd-sdot {{ width: 7px; height: 7px; border-radius: 50%; background: #00D68F; box-shadow: 0 0 8px #00D68F; animation: drdPulse 2s ease-in-out infinite; }}
    .drd-close {{
      margin-left: auto; background: rgba(255,255,255,0.07); border: none;
      color: rgba(250,250,250,0.6); width: 32px; height: 32px; border-radius: 10px;
      cursor: pointer; font-size: 1.1rem; display: flex; align-items: center;
      justify-content: center; transition: all 0.2s; flex-shrink: 0;
    }}
    .drd-close:hover {{ background: rgba(255,59,48,0.15); color: #FF3D71; }}

    #drd-msgs {{
      flex: 1; overflow-y: auto; padding: 14px; display: flex;
      flex-direction: column; gap: 10px; scroll-behavior: smooth;
    }}
    #drd-msgs::-webkit-scrollbar {{ width: 4px; }}
    #drd-msgs::-webkit-scrollbar-track {{ background: transparent; }}
    #drd-msgs::-webkit-scrollbar-thumb {{ background: rgba(108,99,255,0.3); border-radius: 4px; }}

    .drd-msg {{ display: flex; gap: 8px; align-items: flex-end; animation: drdIn 0.3s ease; }}
    .drd-msg.drd-u {{ flex-direction: row-reverse; }}
    .drd-av {{
      width: 28px; height: 28px; border-radius: 9px;
      background: linear-gradient(135deg, #6C63FF, #4B45B2);
      display: flex; align-items: center; justify-content: center;
      font-size: 0.85rem; flex-shrink: 0; overflow: hidden;
    }}
    .drd-bubble {{
      max-width: 80%; padding: 10px 13px; border-radius: 18px;
      font-size: 0.84rem; line-height: 1.55; white-space: pre-wrap; word-break: break-word;
    }}
    .drd-msg:not(.drd-u) .drd-bubble {{
      background: rgba(108,99,255,0.1); border: 1px solid rgba(108,99,255,0.18);
      color: #E8E9F0; border-bottom-left-radius: 4px;
    }}
    .drd-msg.drd-u .drd-bubble {{
      background: linear-gradient(135deg, #6C63FF, #4B45B2);
      color: #fff; border-bottom-right-radius: 4px;
    }}
    .drd-foot {{
      padding: 12px 14px; border-top: 1px solid rgba(108,99,255,0.1);
      display: flex; gap: 10px; align-items: flex-end;
      background: rgba(26,29,41,0.6); flex-shrink: 0;
    }}
    #drd-inp {{
      flex: 1; background: rgba(255,255,255,0.07); border: 1px solid rgba(108,99,255,0.2);
      border-radius: 14px; padding: 10px 13px; color: #FAFAFA; font-size: 0.84rem;
      outline: none; resize: none; transition: border-color 0.2s; max-height: 80px;
      font-family: 'Plus Jakarta Sans', sans-serif;
    }}
    #drd-inp:focus {{ border-color: rgba(108,99,255,0.5); }}
    #drd-send {{
      width: 40px; height: 40px; border-radius: 12px;
      background: linear-gradient(135deg, #6C63FF, #4B45B2); border: none;
      color: white; cursor: pointer; display: flex; align-items: center;
      justify-content: center; transition: transform 0.2s;
      box-shadow: 0 4px 14px rgba(108,99,255,0.3); font-size: 1.1rem;
    }}
    #drd-send:hover {{ transform: scale(1.08); }}
    #drd-send:disabled {{ opacity: 0.5; cursor: not-allowed; }}
    .drd-disc {{
      font-size: 0.65rem; color: rgba(250,250,250,0.22); text-align: center; padding: 0 14px 8px;
    }}
    .drd-typing {{ display: flex; gap: 4px; padding: 6px 0; }}
    .drd-typing span {{
      width: 6px; height: 6px; border-radius: 50%; background: rgba(108,99,255,0.5);
      animation: drdBounce 1.4s infinite both;
    }}
    .drd-typing span:nth-child(2) {{ animation-delay: 0.2s; }}
    .drd-typing span:nth-child(3) {{ animation-delay: 0.4s; }}

    @keyframes drdFloat {{ 0%,100%{{ transform: translateY(0); }} 50%{{ transform: translateY(-8px); }} }}
    @keyframes drdPulse {{ 0%,100%{{ opacity: 1; transform: scale(1); }} 50%{{ opacity: 0.5; transform: scale(0.8); }} }}
    @keyframes drdIn {{ from{{ opacity: 0; transform: translateY(8px); }} to{{ opacity: 1; transform: translateY(0); }} }}
    @keyframes drdBounce {{ 0%,80%,100%{{ transform: scale(0); }} 40%{{ transform: scale(1); }} }}
  `;
  doc.head.appendChild(style);

  // --- Inject HTML into parent body ---
  var container = doc.createElement('div');
  container.id = 'drd-container';
  container.innerHTML = `
    <div id="drd-dot"></div>
    <div id="drd-tip">&#128075; Ask Dr. Docyote!</div>
    <div id="drd-fab">{av_fab}</div>
    <div id="drd-panel">
      <div class="drd-hdr">
        <div class="drd-hav">{av_small}</div>
        <div>
          <h3>Dr. Docyote</h3>
          <div class="drd-status"><div class="drd-sdot"></div>Online<span style="color:rgba(250,250,250,0.35); font-size:0.7rem;">&nbsp;&middot; AI Medical Assistant</span></div>
        </div>
        <button class="drd-close" id="drd-close-btn">&#x2715;</button>
      </div>
      <div id="drd-msgs"></div>
      <div class="drd-disc">&#129690; For informational use only &middot; Always consult a real doctor</div>
      <div class="drd-foot">
        <textarea id="drd-inp" rows="1" placeholder="Ask a health question..."></textarea>
        <button id="drd-send">&#10148;</button>
      </div>
    </div>
  `;
  doc.body.appendChild(container);

  doc.body.__drd_msg_count = '0';
  doc.body.__drd_last_notified = {context_str_js};

  // --- Wire Listeners ---
  doc.getElementById('drd-fab').onclick = togglePanel;
  doc.getElementById('drd-close-btn').onclick = togglePanel;
  doc.getElementById('drd-send').onclick = sendMessage;
  doc.getElementById('drd-inp').onkeydown = function(e) {{
    if (e.key === 'Enter' && !e.shiftKey) {{
      e.preventDefault();
      sendMessage();
    }}
  }};

  // --- Initial Messages ---
  addMsg('bot', {welcome_msg_js});
  if ({context_str_js} !== "None") {{
     var contextMsg = 'I see you just finished a symptom check for: ' + {context_str_js}.split('|')[0].replace('Symptoms:', '') + '. How can I help you with these results?';
     addMsg('bot', contextMsg);
     doc.body.__drd_msg_count = '0'; // Will sync on next render
  }}

  // Fade tooltip
  setTimeout(function() {{
    var tip = doc.getElementById('drd-tip');
    if (tip) tip.style.opacity = '0';
    setTimeout(function() {{ if (tip) tip.style.display = 'none'; }}, 600);
  }}, 5000);

  console.log('Dr. Docyote: Injection complete! (Secure mode - no API keys in browser)');
}})();
</script>
</body>
</html>
"""

    components.html(widget_html, height=0, width=0)

