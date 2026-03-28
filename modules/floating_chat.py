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


def render_floating_chatbot(context: dict = None):
    """Floating doctor chatbot widget injected into parent Streamlit page via iframe JS."""
    b64 = _get_avatar_b64()
    api_key = GEMINI_API_KEY or ""
    groq_key = GROQ_API_KEY or ""
    
    # Format context for JS injection
    context_str = "None"
    if context:
        symptoms_list = context.get('symptoms', [])
        symptoms = ", ".join(symptoms_list) if isinstance(symptoms_list, list) else str(symptoms_list)
        preds_list = context.get('predictions', [])
        predictions = ", ".join([f"{p['disease']} ({p.get('confidence',0)}%)" for p in (preds_list[:3] if isinstance(preds_list, list) else [])])
        context_str = f"Symptoms: {symptoms} | Top Predictions: {predictions}"

    if b64:
        av_img = 'data:image/png;base64,' + b64
        av_fab = '<img src="' + av_img + '" style="width:100%;height:100%;object-fit:cover;border-radius:50%;" alt="Dr.">'
        av_small = '<img src="' + av_img + '" style="width:100%;height:100%;object-fit:cover;border-radius:9px;" alt="Dr.">'
    else:
        av_fab = '<span style="font-size:1.6rem;">&#128104;&#8205;&#9877;&#65039;</span>'
        av_small = '<span style="font-size:0.85rem;">&#128104;&#8205;&#9877;&#65039;</span>'

    # Base system prompt
    sys_prompt = "You are Dr. Docyote, a friendly AI medical assistant. Give concise helpful answers with emojis. Always advise seeing a real doctor for serious concerns. For emergencies, advise calling emergency services immediately. Respond in the user's language."
    if context_str != "None":
        sys_prompt += " The user just ran a symptom check. " + context_str + ". Use this context to answer follow-up questions."
    
    welcome_msg = "Hi! 👋 I’m Dr. Docyote, your AI health assistant!\n\nAsk me about symptoms, diseases, home remedies, or any health question. I’m here to help! 🪴"
    
    # Use json.dumps to safely inject into JS
    api_key_js = json.dumps(api_key or "")
    groq_key_js = json.dumps(groq_key or "")
    context_str_js = json.dumps(context_str)
    sys_prompt_js = json.dumps(sys_prompt)
    welcome_msg_js = json.dumps(welcome_msg)
    av_small_js = json.dumps(av_small) # Safe for use in JS strings

    # The entire widget is injected into the PARENT document from within the iframe
    # This is the only way to get both JS execution AND fixed positioning in Streamlit
    widget_html = f"""
<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body>
<script>
(function() {{
  // Target the parent Streamlit document
  var doc = window.parent.document;

  // --- Update-if-exists Logic ---
  var existing = doc.getElementById('drd-fab');
  if (existing) {{
    var newContext = {context_str_js};
    var newSys = {sys_prompt_js};
    
    // Update the parent-level state
    doc.body.__drd_context = newContext;
    doc.body.__drd_sys = newSys;
    
    console.log('Dr. Docyote: Context updated to', newContext);
    
    // If a new symptom check was performed, notify the bot
    if (newContext !== "None" && doc.body.__drd_last_notified !== newContext) {{
      doc.body.__drd_last_notified = newContext;
      if (typeof doc.body.__drd_addMsg === 'function') {{
         var msg = 'I see you just updated your symptoms: ' + newContext.split('|')[0].replace('Symptoms:', '') + '. How can I help?';
         doc.body.__drd_addMsg('bot', msg);
      }}
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
      transition: transform 0.25s cubic-bezier(0.34,1.6,0.64,1), box-shadow 0.25s;
    }}
    #drd-fab:hover {{ box-shadow: 0 12px 40px rgba(108,99,255,0.6); transform: scale(1.08); }}

    #drd-dot {{
      position: fixed; bottom: 80px; right: 30px; width: 14px; height: 14px; border-radius: 50%;
      background: #00D68F; border: 2.5px solid #111827; box-shadow: 0 0 10px rgba(0,214,143,0.5);
      z-index: 1000000; animation: drdPulse 2s ease-in-out infinite;
    }}

    #drd-tip {{
      position: fixed; bottom: 105px; right: 28px; background: white; color: #1a1d29;
      font-size: 0.82rem; font-weight: 600; padding: 9px 14px; border-radius: 16px 16px 4px 16px;
      box-shadow: 0 8px 28px rgba(0,0,0,0.18); white-space: nowrap; z-index: 999999;
      font-family: 'Plus Jakarta Sans', sans-serif;
      transition: opacity 0.5s; pointer-events: none;
    }}
    #drd-tip::after {{
      content: ''; position: absolute; bottom: -8px; right: 20px;
      border: 8px solid transparent; border-top-color: white; border-bottom: 0;
    }}

    #drd-panel {{
      position: fixed; bottom: 105px; right: 28px; width: 370px; height: 520px;
      background: linear-gradient(160deg, #111827, #0d1117); border-radius: 24px;
      box-shadow: 0 30px 80px rgba(0,0,0,0.7), 0 0 0 1px rgba(108,99,255,0.2);
      display: flex; flex-direction: column; overflow: hidden; z-index: 999998;
      transform: scale(0.85) translateY(20px); transform-origin: bottom right;
      opacity: 0; pointer-events: none;
      transition: all 0.3s cubic-bezier(0.34,1.2,0.64,1);
      font-family: 'Plus Jakarta Sans', sans-serif;
    }}
    #drd-panel.drd-open {{ opacity: 1; pointer-events: all; transform: scale(1) translateY(0); }}

    .drd-hdr {{
      background: linear-gradient(135deg, #1e2235, #252a3d); padding: 16px 18px;
      display: flex; align-items: center; gap: 12px;
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

  // --- Wire up event handlers ---
  // Store state on doc.body to survive sidebar re-renders
  doc.body.__drd_api = {api_key_js};
  doc.body.__drd_groq = {groq_key_js};
  doc.body.__drd_context = {context_str_js};
  doc.body.__drd_sys = {sys_prompt_js};
  doc.body.__drd_last_notified = doc.body.__drd_context;

  var hist = [];

  var fab = doc.getElementById('drd-fab');
  var panel = doc.getElementById('drd-panel');
  var closeBtn = doc.getElementById('drd-close-btn');
  var sendBtn = doc.getElementById('drd-send');
  var inp = doc.getElementById('drd-inp');
  var msgs = doc.getElementById('drd-msgs');
  var tip = doc.getElementById('drd-tip');

  function togglePanel() {{
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

  fab.addEventListener('click', togglePanel);
  closeBtn.addEventListener('click', togglePanel);

  function addMsg(role, text) {{
    var div = doc.createElement('div');
    div.className = 'drd-msg' + (role === 'user' ? ' drd-u' : '');
    var avHtml = role === 'user' ? '<span style="font-size:0.75rem;">&#128100;</span>' : {av_small_js};
    div.innerHTML = '<div class="drd-av">' + avHtml + '</div><div class="drd-bubble">' + text.replace(/\\n/g, '<br>') + '</div>';
    msgs.appendChild(div);
    msgs.scrollTop = msgs.scrollHeight;
    
    // Expose to parent body for hot-reloading context messages
    doc.body.__drd_addMsg = addMsg;
    return div;
  }}

  function showTyping() {{
    var div = doc.createElement('div');
    div.className = 'drd-msg';
    div.id = 'drd-typing';
    div.innerHTML = '<div class="drd-av">{av_small}</div><div class="drd-bubble"><div class="drd-typing"><span></span><span></span><span></span></div></div>';
    msgs.appendChild(div);
    msgs.scrollTop = msgs.scrollHeight;
    return div;
  }}

  function removeTyping() {{
    var t = doc.getElementById('drd-typing');
    if (t) t.remove();
  }}

  async function sendMessage() {{
    var val = inp.value.trim();
    if (!val) return;
    inp.value = '';
    addMsg('user', val);
    hist.push({{ role: 'user', content: val }});
    sendBtn.disabled = true;
    var typ = showTyping();

    // Prioritize Groq, Fallback to Gemini 2.0-Flash
    var url = doc.body.__drd_groq ? 'https://api.groq.com/openai/v1/chat/completions' : 
              'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=' + doc.body.__drd_api;
    var usingGroq = !!doc.body.__drd_groq;
    
    var bodyMsgs = [{{ role: 'system', content: doc.body.__drd_sys }}].concat(hist.slice(-6));
    var body = usingGroq ? JSON.stringify({{ model: "llama-3.3-70b-versatile", messages: bodyMsgs, temperature: 0.7 }}) 
                        : JSON.stringify({{ contents: [{{ parts: [{{ text: bodyMsgs.map(m=>m.role+": "+m.content).join("\\n") }}] }}], generationConfig: {{ temperature: 0.7 }} }});
    
    try {{
      var res = await fetch(url, {{
        method: 'POST',
        headers: {{ 'Content-Type': 'application/json', ...(usingGroq ? {{'Authorization': 'Bearer ' + doc.body.__drd_groq}} : {{}}) }},
        body: body
      }});
      
      // Handle Rate Limits (429)
      if (res.status === 429) {{
          msgs.removeChild(typ);
          addMsg('bot', 'I’m taking a quick 60-second break to rest my brain! Please ask me again in a minute. ☕');
          sendBtn.disabled = false;
          return;
      }}

      var data = await res.json();
      var botTxt = "";
      
      if (usingGroq) {{
          if (data.choices && data.choices[0]) botTxt = data.choices[0].message.content;
          else throw new Error('Groq format mismatch');
      }} else {{
          if (data.candidates && data.candidates[0]) botTxt = data.candidates[0].content.parts[0].text;
          else if (data.error) {{
              if (data.error.status === 'RESOURCE_EXHAUSTED') {{
                  msgs.removeChild(typ);
                  addMsg('bot', 'My AI batteries are recharging! Please try again in 60 seconds. 🔋');
                  sendBtn.disabled = false;
                  return;
              }}
              throw new Error(data.error.message);
          }}
          else throw new Error('Gemini format mismatch');
      }}
      
      msgs.removeChild(typ);
      addMsg('bot', botTxt);
      hist.push({{ role: 'assistant', content: botTxt }});
    }} catch (err) {{
      console.error('Dr. Docyote Error:', err);
      msgs.removeChild(typ);
      addMsg('bot', 'I encountered a brief connection issue. Please try again in a moment! ⚠️');
    }}
    sendBtn.disabled = false;
    inp.focus();
  }}

  sendBtn.addEventListener('click', sendMessage);

  // Keyboard: Enter to send
  inp.addEventListener('keydown', function(e) {{
    if (e.key === 'Enter' && !e.shiftKey) {{
      e.preventDefault();
      sendMessage();
    }}
  }});

  // --- Initial State ---
  addMsg('bot', {welcome_msg_js});

  if (doc.body.__drd_context !== "None") {{
     var contextMsg = 'I see you just finished a symptom check for: ' + doc.body.__drd_context.split('|')[0].replace('Symptoms:', '') + '. How can I help you with these results?';
     addMsg('bot', contextMsg);
  }}

  // Fade tooltip after 5s
  setTimeout(function() {{
    if (tip) tip.style.opacity = '0';
    setTimeout(function() {{ if (tip) tip.style.display = 'none'; }}, 600);
  }}, 5000);

  console.log('Dr. Docyote: Injection complete!');
}})();
</script>
</body>
</html>
"""

    # Use components.html which executes JS inside an iframe
    # height=0 makes the iframe invisible - the widget is injected into the parent doc
    components.html(widget_html, height=0, width=0)
