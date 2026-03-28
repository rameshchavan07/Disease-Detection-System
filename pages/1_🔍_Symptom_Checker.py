"""
🔍 Symptom Checker Page
Select symptoms and get AI-powered disease predictions with premium UI.
"""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.ml_engine import get_all_symptoms, predict_disease, format_symptom_name
from modules.disease_info import get_disease_info, get_severity_display
from modules.pdf_generator import generate_report
from modules.nlp_extractor import extract_symptoms, translate_to_english
from modules.database import save_prediction
from modules.shared_ui import inject_premium_css, render_sidebar
from modules.email_service import send_report_email
from audio_recorder_streamlit import audio_recorder
import groq
from groq import Groq
import uuid
from modules.logger import get_logger

logger = get_logger("symptom_checker")

st.set_page_config(page_title="Symptom Checker - MedDetect AI", page_icon="🔍", layout="wide")

# Auth Check
if "user_id" not in st.session_state or not st.session_state.user_id:
    st.error("🔒 Please sign in from the **🔑 Sign In** page to access the Symptom Checker.")
    st.info("Creating a free account allows you to securely save your prediction history.")
    st.stop()

# Inject shared premium CSS & sidebar
inject_premium_css()
render_sidebar()

# Page-specific CSS
st.markdown("""
<style>
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1117 0%, #161b26 100%);
    border-right: 1px solid rgba(108,99,255,0.08);
}

.checker-header {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 1.5rem 2rem;
    background: linear-gradient(135deg, rgba(108,99,255,0.1), rgba(99,179,255,0.05));
    border: 1px solid rgba(108,99,255,0.12);
    border-radius: 20px;
    margin-bottom: 2rem;
    backdrop-filter: blur(10px);
}

.checker-header h1 {
    margin: 0;
    font-size: 1.8rem;
    font-weight: 800;
    background: linear-gradient(135deg, #6C63FF, #8B83FF);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.checker-header p {
    margin: 0.3rem 0 0;
    font-size: 0.88rem;
    color: rgba(250,250,250,0.5);
}

.result-card {
    background: linear-gradient(145deg, rgba(26,29,41,0.9), rgba(26,29,41,0.5));
    border: 1px solid rgba(108,99,255,0.12);
    border-radius: 20px;
    padding: 1.5rem 1.8rem;
    margin-bottom: 1rem;
    backdrop-filter: blur(10px);
    transition: all 0.3s ease;
}

.result-card:hover {
    border-color: rgba(108,99,255,0.25);
    box-shadow: 0 8px 24px rgba(108,99,255,0.08);
}

.disease-name {
    font-size: 1.3rem;
    font-weight: 700;
    color: #FAFAFA;
    margin-bottom: 0.3rem;
}

.disease-rank {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 28px;
    height: 28px;
    border-radius: 8px;
    background: linear-gradient(135deg, #6C63FF, #8B83FF);
    color: white;
    font-weight: 700;
    font-size: 0.85rem;
    margin-right: 0.6rem;
}

.confidence-bar-bg {
    background: rgba(255,255,255,0.06);
    border-radius: 10px;
    height: 10px;
    overflow: hidden;
    margin: 0.5rem 0;
}

.confidence-bar-fill {
    height: 100%;
    border-radius: 10px;
    background: linear-gradient(90deg, #6C63FF, #8B83FF, #63B3FF);
    transition: width 1.5s cubic-bezier(0.4, 0, 0.2, 1);
}

.severity-badge {
    display: inline-block;
    padding: 0.3rem 0.9rem;
    border-radius: 100px;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.3px;
}

.emergency-alert {
    background: rgba(183,28,28,0.12);
    border: 1px solid rgba(244,67,54,0.3);
    border-radius: 16px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 1.5rem;
    animation: alertPulse 2s ease-in-out infinite;
}

@keyframes alertPulse {
    0%, 100% { box-shadow: 0 0 0 0 rgba(244,67,54,0.2); }
    50% { box-shadow: 0 0 25px 5px rgba(244,67,54,0.1); }
}

.input-section {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(108,99,255,0.08);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="checker-header">
    <span style="font-size: 2.5rem;">🔍</span>
    <div>
        <h1>Symptom Checker</h1>
        <p>Select your symptoms and let our AI analyze them to predict possible diseases.</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Get all symptoms
all_symptoms = get_all_symptoms()
symptom_display_map = {format_symptom_name(s): s for s in all_symptoms}

# ── Symptom Input Section ──
st.markdown("### 📋 Describe Your Symptoms")

st.markdown('<div class="input-section">', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["✍️ Type Symptoms", "🎙️ Dr. Docyote Voice (FAST)"])

nlp_input = ""

with tab1:
    text_input = st.text_area(
        "Describe how you're feeling in plain language:",
        value=st.session_state.get("nlp_voice_text", ""),
        height=80,
        placeholder="e.g., I have a terrible headache and my throat hurts...",
        help="Our AI will extract symptoms automatically."
    )
    if text_input:
        nlp_input = text_input

with tab2:
    st.markdown("**Speak directly to Dr. Docyote!** Click the microphone below, describe your symptoms, and click to stop.")
    
    col_mic, col_info = st.columns([1, 4])
    with col_mic:
        audio_bytes = audio_recorder(text="", recording_color="#FF3D71", neutral_color="#6C63FF", icon_name="microphone", icon_size="3x")
    
    with col_info:
        if audio_bytes:
            st.audio(audio_bytes, format="audio/wav")
            
            # Prevent re-transcribing the same audio byte repeatedly
            if "last_audio" not in st.session_state or st.session_state["last_audio"] != audio_bytes:
                st.session_state["last_audio"] = audio_bytes
                
                # Check for minimum audio length (avoid 400 errors from Groq)
                if len(audio_bytes) < 3000: # ~0.15s to 0.2s
                    st.toast("🎤 Recording too short. Please speak clearly for at least a second!")
                else:
                    with st.spinner("Dr. Docyote is transcribing your voice instantly..."):
                        try:
                            client = Groq(api_key=os.environ.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY")))
                            # Groq Whisper API call
                            transcription = client.audio.transcriptions.create(
                                file=("audio.wav", audio_bytes),
                                model="whisper-large-v3", # Lightning-fast Groq transcription
                                response_format="json"
                            )
                            # 2. Translate to English if non-English
                            translated_text = translate_to_english(transcription.text)
                            
                            st.session_state["nlp_voice_text"] = translated_text
                            
                            if translated_text.lower() != transcription.text.lower():
                                st.success(f"✅ Translated to English: \"{translated_text}\"")
                            else:
                                st.success("✅ Transcription complete!")
                                
                            st.rerun() # Refresh to populate the text box
                        except groq.APIConnectionError as e:
                            logger.error(f"Groq Connection Error: {e}")
                            st.error("Could not connect to the voice service due to a network issue.")
                        except groq.AuthenticationError as e:
                            logger.error(f"Groq Auth Error: {e}")
                            st.error("Voice service authentication failed. Please check the API key.")
                        except groq.APIError as e:
                            logger.error(f"Groq API Error: {e}")
                            st.error("The voice transcription service returned an error. Please try again later.")
                        except Exception as e:
                            logger.exception(f"Unexpected transcription error: {e}")
                            st.error(f"Could not complete transcription: {e}")

# Apply transcription if it exists
if "nlp_voice_text" in st.session_state and st.session_state["nlp_voice_text"]:
    nlp_input = st.session_state["nlp_voice_text"]

extracted_symptoms = []
if nlp_input:
    # 3. Check if the input itself is a quota error from tab1 (rare but possible if typed)
    if nlp_input == "[[QUOTA_EXCEEDED]]":
        st.warning("⚠️ AI Rate Limit Reached: Please wait 60 seconds before trying again.")
    else:
        extracted_symptoms = extract_symptoms(nlp_input, all_symptoms)
        if extracted_symptoms:
            st.success(f"🤖 **Dr. Docyote extracted**: {', '.join([format_symptom_name(s) for s in extracted_symptoms])}")
        elif any(ord(c) > 127 for c in nlp_input):
            # If no symptoms found and text is Hindi/Marathi, it might be a quota fail in extract_symptoms
            st.info("💡 **Tip**: If your regional symptoms weren't found, the AI might be on a 60-second break. Please try again in a minute!")

default_selections = [format_symptom_name(s) for s in extracted_symptoms] if extracted_symptoms else []

selected_display = st.multiselect(
    "Or manually search and select symptoms:",
    options=sorted(symptom_display_map.keys()),
    default=default_selections,
    placeholder="Start typing a symptom name...",
    help="More symptoms = better accuracy."
)

st.markdown('</div>', unsafe_allow_html=True)

# Convert display names back
selected_symptoms = [symptom_display_map[s] for s in selected_display]

col1, col2 = st.columns([1, 3])
with col1:
    analyze_btn = st.button("🔬 Analyze Symptoms", type="primary", use_container_width=True, disabled=len(selected_symptoms) < 1)
with col2:
    if len(selected_symptoms) > 0:
        st.success(f"✅ **{len(selected_symptoms)}** symptom(s) selected — ready to analyze")
    else:
        st.warning("⚠️ Please select at least 1 symptom")

# ── Prediction Results ──
if analyze_btn and selected_symptoms:
    st.markdown("---")
    
    progress_bar = st.progress(0, text="🧠 Initializing AI model...")
    import time
    progress_bar.progress(30, text="🔄 Processing symptoms...")
    predictions = predict_disease(selected_symptoms, top_k=5)
    progress_bar.progress(70, text="📊 Generating predictions...")
    time.sleep(0.3)
    progress_bar.progress(100, text="✅ Analysis complete!")
    time.sleep(0.5)
    progress_bar.empty()
    
    # Store in session state so they persist when typing name
    st.session_state['last_predictions'] = predictions
    st.session_state['last_symptoms'] = selected_display
    st.session_state['last_symptoms_raw'] = selected_symptoms
    
    # Save to DB
    if predictions:
        user_id = st.session_state.user_id
        save_prediction(user_id, selected_display, predictions)

# Show results from session state (persists across name input reruns)
predictions = st.session_state.get('last_predictions', None)
last_symptoms_display = st.session_state.get('last_symptoms', [])
last_symptoms_raw = st.session_state.get('last_symptoms_raw', [])

if predictions:
    st.markdown("---")
    st.markdown("### 🏥 Prediction Results")
    
    # Emergency check (Show at most one alert)
    for pred in predictions:
        info = get_disease_info(pred["disease"])
        if info.get("severity") == "critical" and pred["confidence"] > 10:
            room_id = f"MedDetect_Emergency_{uuid.uuid4().hex[:8]}"
            jitsi_url = f"https://meet.jit.si/{room_id}"
            
            st.markdown(f"""
            <div class="emergency-alert">
                🚨 <strong>EMERGENCY ALERT:</strong> High probability of <strong>{pred['disease']}</strong> detected.
                Please <strong>seek immediate medical attention</strong> or call emergency services (911/112).
            </div>
            """, unsafe_allow_html=True)
            
            st.link_button("📞 Emergency Video Call with Doctor", jitsi_url, use_container_width=True, type="primary")
            break  # Only show one emergency alert
    
    # Display predictions
    for pred in predictions:
        info = get_disease_info(pred["disease"])
        sev = get_severity_display(info["severity"])
        
        st.markdown(f"""
        <div class="result-card">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.5rem;">
                <div style="display: flex; align-items: center;">
                    <span class="disease-rank">{pred['rank']}</span>
                    <span class="disease-name">{pred['disease']}</span>
                </div>
                <span class="severity-badge" style="background: {sev['bg']}; color: {sev['color']}; border: 1px solid {sev['color']};">
                    {sev['icon']} {sev['label']}
                </span>
            </div>
            <div style="color: rgba(250,250,250,0.6); font-size: 0.9rem; margin-top: 0.5rem;">
                Confidence: <strong style="color: #6C63FF;">{pred['confidence']}%</strong>
            </div>
            <div class="confidence-bar-bg">
                <div class="confidence-bar-fill" style="width: {min(pred['confidence'], 100)}%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander(f"📖 Details for {pred['disease']}", expanded=(pred['rank'] == 1)):
            st.markdown(f"**📝 Description:** {info['description']}")
            
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown("**🔬 Possible Causes:**")
                for c in info.get("causes", []):
                    st.markdown(f"• {c}")
                
                st.markdown("**🛡️ Precautions:**")
                for p in info.get("precautions", []):
                    st.markdown(f"• {p}")
            
            with col_b:
                st.markdown("**🌿 Home Remedies:**")
                for r in info.get("home_remedies", []):
                    st.markdown(f"• {r}")
                
                st.markdown(f"<p style='margin-top: 1rem;'><strong>👨‍⚕️ Recommended Specialist:</strong> <span style='color: #6C63FF; font-weight: 700;'>{info.get('specialist', 'General Physician')}</span></p>", unsafe_allow_html=True)
                
                specialist = info.get('specialist', 'General Physician')
                search_query = f"{specialist} near me".replace(" ", "+")
                maps_url = f"https://www.google.com/maps/search/{search_query}"
                st.link_button(f"🏥 Find a {specialist} Near Me", maps_url, use_container_width=True)
                
                if info.get("consult_doctor"):
                    st.error("🚨 **Consult a doctor immediately** for this condition.")
                else:
                    st.info("💡 Monitor symptoms. Consult a doctor if they persist.")
    
    # PDF Report - outside analyze_btn so name typing doesn't lose results
    st.markdown("---")
    st.markdown("### 📄 Download Report")
    
    st.info("💡 **Tip:** Add your details to customize the PDF, then press **Enter** to save.")
    
    col1_pdf, col2_pdf = st.columns(2)
    with col1_pdf:
        user_name = st.text_input("Patient Name:", placeholder="Type name...", key="report_name")
    with col2_pdf:
        user_age = st.text_input("Patient Age:", placeholder="e.g., 34", key="report_age")
    
    # Use entered name or fallback
    pdf_name = user_name.strip() if user_name.strip() else st.session_state.get("user_email", "Patient").split("@")[0].title()
    pdf_email = st.session_state.get("user_email", "Not provided")
    pdf_age = user_age.strip() if user_age.strip() else "Unspecified"
    
    disease_info_map = {}
    for p in predictions:
        disease_info_map[p["disease"]] = get_disease_info(p["disease"])
    
    try:
        pdf_bytes = generate_report(pdf_name, pdf_email, last_symptoms_raw, predictions, disease_info_map, pdf_age)
        st.download_button(
            label="📥 Download PDF Report",
            data=pdf_bytes,
            file_name=f"MedDetect_Report_{predictions[0]['disease'].replace(' ', '_')}.pdf",
            mime="application/pdf",
            type="primary",
            use_container_width=True
        )
        
        # Button to send email if user is logged in
        if st.session_state.get("user_email"):
            if st.button("✉️ Send Report to My Email", type="secondary", use_container_width=True):
                with st.spinner("📧 Sending copy to your email..."):
                    success, msg = send_report_email(
                        st.session_state.user_email, 
                        pdf_bytes, 
                        predictions[0]['disease']
                    )
                    if success:
                        st.success(f"✅ A copy of this report has been emailed to **{st.session_state.user_email}**.")
                    else:
                        st.warning(f"⚠️ Could not send email: {msg}")
                    
    except Exception as e:
        st.error(f"Error generating report: {e}")

# Disclaimer
st.markdown("---")
st.caption("⚠️ **Disclaimer:** This tool is for informational purposes only. Consult a healthcare professional for medical advice.")

# Disclaimer
st.markdown("---")
st.caption("⚠️ **Disclaimer:** This tool is for informational purposes only. Consult a healthcare professional for medical advice.")
