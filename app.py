"""
MedDetect AI - Multi-Disease Detection System
Main Streamlit Application Entry Point
"""
#streamlit run app.py
import streamlit as st
from modules.logger import get_logger

logger = get_logger("app")
# Page config MUST be first Streamlit command
st.set_page_config(
    page_title="MedDetect AI - Disease Detection",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for auth (shared across all pages)
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "user_email" not in st.session_state:
    st.session_state.user_email = None

# ── Premium Global CSS ──
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

:root {
    --accent: #6C63FF;
    --accent-light: #8B83FF;
    --accent-glow: rgba(108,99,255,0.3);
    --bg-card: rgba(26,29,41,0.7);
    --bg-glass: rgba(255,255,255,0.04);
    --success: #00D68F;
    --warning: #FFAA00;
    --danger: #FF3D71;
    --text-primary: #FAFAFA;
    --text-secondary: rgba(250,250,250,0.6);
    --border-subtle: rgba(108,99,255,0.15);
}

*, *::before, *::after { font-family: 'Plus Jakarta Sans', sans-serif !important; }
html, body, [class*="st-"] { font-family: 'Plus Jakarta Sans', sans-serif !important; }

/* Preserve Streamlit icon fonts */
[data-testid="stSidebarCollapseButton"] span,
[data-testid="stSidebarCollapseButton"] *,
[data-testid="baseButton-headerNoPadding"] span,
[data-testid="stIconMaterial"],
.material-symbols-rounded,
.material-symbols-outlined,
[class*="material-symbols"],
[class*="stIcon"] {
    font-family: 'Material Symbols Rounded', sans-serif !important;
}
html { scroll-behavior: smooth; }

/* Animated background */
.stApp {
    background: linear-gradient(135deg, #0a0e1a 0%, #111827 40%, #0f172a 70%, #0a0e1a 100%);
}

.main .block-container { max-width: 1200px; padding-top: 1.5rem; position: relative; z-index: 1; }

/* Animated gradient orbs behind content */
.stApp::before {
    content: '';
    position: fixed;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle at 20% 50%, rgba(108,99,255,0.06) 0%, transparent 50%),
                radial-gradient(circle at 80% 20%, rgba(99,179,255,0.04) 0%, transparent 50%),
                radial-gradient(circle at 50% 80%, rgba(255,99,195,0.03) 0%, transparent 50%);
    animation: orbFloat 20s ease-in-out infinite;
    pointer-events: none;
    z-index: 0;
}

@keyframes orbFloat {
    0%, 100% { transform: translate(0, 0) rotate(0deg); }
    33% { transform: translate(30px, -20px) rotate(3deg); }
    66% { transform: translate(-20px, 15px) rotate(-2deg); }
}

/* Hero Section */
.hero-container {
    text-align: center;
    padding: 4rem 2rem 3rem;
    background: linear-gradient(135deg, rgba(108,99,255,0.12) 0%, rgba(99,179,255,0.06) 50%, rgba(255,99,195,0.06) 100%);
    border-radius: 28px;
    border: 1px solid rgba(108,99,255,0.15);
    margin-bottom: 2.5rem;
    position: relative;
    overflow: hidden;
    backdrop-filter: blur(20px);
}

.hero-container::before {
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(ellipse at center top, rgba(108,99,255,0.08) 0%, transparent 70%);
    animation: heroPulse 6s ease-in-out infinite;
}

@keyframes heroPulse {
    0%, 100% { opacity: 0.4; }
    50% { opacity: 1; }
}

.hero-badge {
    display: inline-block;
    background: rgba(108,99,255,0.15);
    border: 1px solid rgba(108,99,255,0.3);
    border-radius: 100px;
    padding: 0.4rem 1.2rem;
    font-size: 0.8rem;
    font-weight: 600;
    color: #8B83FF;
    letter-spacing: 0.5px;
    margin-bottom: 1.5rem;
    position: relative;
}

.hero-title {
    font-size: 3.5rem;
    font-weight: 800;
    background: linear-gradient(135deg, #6C63FF 0%, #63B3FF 40%, #FF63C3 80%, #6C63FF 100%);
    background-size: 200% 200%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: gradientShift 8s ease-in-out infinite;
    margin-bottom: 0.5rem;
    position: relative;
    line-height: 1.2;
}

@keyframes gradientShift {
    0%, 100% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
}

.hero-subtitle {
    font-size: 1.15rem;
    color: rgba(250,250,250,0.6);
    font-weight: 300;
    margin-bottom: 2rem;
    position: relative;
    max-width: 600px;
    margin-left: auto;
    margin-right: auto;
    line-height: 1.7;
}

/* Animated Stats */
.hero-stats {
    display: flex;
    justify-content: center;
    gap: 2.5rem;
    margin-top: 1.5rem;
    position: relative;
    flex-wrap: wrap;
}

.stat-item {
    text-align: center;
    padding: 1rem 1.5rem;
    background: rgba(255,255,255,0.03);
    border-radius: 16px;
    border: 1px solid rgba(108,99,255,0.1);
    min-width: 120px;
    transition: all 0.3s ease;
}

.stat-item:hover {
    border-color: rgba(108,99,255,0.3);
    transform: translateY(-3px);
    box-shadow: 0 8px 24px rgba(108,99,255,0.1);
}

.stat-number {
    font-size: 2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #6C63FF, #8B83FF);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.stat-label {
    font-size: 0.75rem;
    color: rgba(250,250,250,0.4);
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-top: 0.25rem;
}

/* Feature Cards */
.feature-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 1.5rem;
    margin: 2rem 0;
}

.feature-card {
    background: linear-gradient(145deg, rgba(26,29,41,0.8), rgba(26,29,41,0.4));
    border: 1px solid rgba(108,99,255,0.1);
    border-radius: 20px;
    padding: 2rem;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    backdrop-filter: blur(10px);
    position: relative;
    overflow: hidden;
}

.feature-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 3px;
    background: linear-gradient(90deg, transparent, var(--accent), transparent);
    opacity: 0;
    transition: opacity 0.4s ease;
}

.feature-card:hover {
    border-color: rgba(108,99,255,0.3);
    transform: translateY(-6px);
    box-shadow: 0 20px 40px rgba(108,99,255,0.12);
}

.feature-card:hover::before { opacity: 1; }

.feature-icon {
    font-size: 2.5rem;
    margin-bottom: 1rem;
    display: inline-block;
    transition: transform 0.3s ease;
}

.feature-card:hover .feature-icon { transform: scale(1.15) rotate(-5deg); }

.feature-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: #FAFAFA;
    margin-bottom: 0.6rem;
}

.feature-desc {
    font-size: 0.88rem;
    color: rgba(250,250,250,0.5);
    line-height: 1.7;
}

/* How To Use Steps */
.step-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(108,99,255,0.08);
    border-radius: 16px;
    padding: 1.5rem;
    text-align: center;
    transition: all 0.3s ease;
}

.step-card:hover {
    border-color: rgba(108,99,255,0.2);
    background: rgba(108,99,255,0.04);
}

.step-number {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 40px;
    border-radius: 12px;
    background: linear-gradient(135deg, #6C63FF, #8B83FF);
    color: white;
    font-weight: 700;
    font-size: 1.1rem;
    margin-bottom: 1rem;
}

.step-title {
    font-weight: 700;
    color: #FAFAFA;
    margin-bottom: 0.4rem;
}

.step-desc {
    font-size: 0.88rem;
    color: rgba(250,250,250,0.5);
    line-height: 1.6;
}

/* CTA Button */
.cta-section {
    text-align: center;
    margin: 3rem 0 1rem;
}

.cta-btn {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: linear-gradient(135deg, #6C63FF, #8B83FF);
    color: white !important;
    padding: 0.9rem 2.5rem;
    border-radius: 14px;
    font-weight: 700;
    font-size: 1.05rem;
    text-decoration: none;
    transition: all 0.3s ease;
    box-shadow: 0 4px 20px rgba(108,99,255,0.3);
}

.cta-btn:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 30px rgba(108,99,255,0.5);
    color: white !important;
}

/* Disclaimer */
.disclaimer-box {
    background: rgba(255,59,48,0.06);
    border: 1px solid rgba(255,59,48,0.15);
    border-radius: 16px;
    padding: 1.2rem 1.5rem;
    margin-top: 2rem;
    font-size: 0.88rem;
    color: rgba(250,250,250,0.7);
    line-height: 1.7;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1117 0%, #161b26 100%);
    border-right: 1px solid rgba(108,99,255,0.08);
}

section[data-testid="stSidebar"] .stMarkdown h3 {
    background: linear-gradient(135deg, #6C63FF, #8B83FF);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #6C63FF, #8B83FF) !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.6rem 1.5rem !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(108,99,255,0.2) !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(108,99,255,0.4) !important;
}

/* Multiselect */
.stMultiSelect [data-baseweb="tag"] {
    background: rgba(108,99,255,0.2) !important;
    border: 1px solid rgba(108,99,255,0.4) !important;
    border-radius: 8px !important;
}

/* Footer */
.footer {
    text-align: center;
    padding: 2rem 0 1rem;
    color: rgba(250,250,250,0.25);
    font-size: 0.8rem;
    border-top: 1px solid rgba(255,255,255,0.05);
    margin-top: 3rem;
}

.footer a {
    color: #6C63FF;
    text-decoration: none;
}
</style>
""", unsafe_allow_html=True)

# ── Sidebar ──
with st.sidebar:
    st.markdown("### 🧠 MedDetect AI")
    
    # User profile card
    if st.session_state.user_id:
        user_email = st.session_state.user_email or "User"
        user_name = st.session_state.get("google_name", "")
        display_name = user_name if user_name else user_email.split("@")[0].title()
        initial = display_name[0].upper() if display_name else "U"
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(108,99,255,0.08), rgba(99,179,255,0.05)); border: 1px solid rgba(108,99,255,0.15); border-radius: 16px; padding: 1rem; margin-bottom: 1rem;">
            <div style="display: flex; align-items: center; gap: 0.8rem;">
                <div style="width: 44px; height: 44px; border-radius: 14px; background: linear-gradient(135deg, #6C63FF, #4B45B2); display: flex; align-items: center; justify-content: center; font-size: 1.2rem; font-weight: 700; color: white; flex-shrink: 0; box-shadow: 0 4px 12px rgba(108,99,255,0.3);">
                    {initial}
                </div>
                <div style="overflow: hidden;">
                    <div style="font-weight: 700; font-size: 0.92rem; color: #FAFAFA; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                        {display_name}
                    </div>
                    <div style="display: flex; align-items: center; gap: 0.3rem; margin-top: 0.2rem;">
                        <div style="width: 6px; height: 6px; border-radius: 50%; background: #00D68F; box-shadow: 0 0 6px #00D68F;"></div>
                        <span style="font-size: 0.72rem; color: #00D68F;">Online</span>
                    </div>
                </div>
            </div>
            <div style="font-size: 0.75rem; color: rgba(250,250,250,0.4); margin-top: 0.6rem; word-break: break-all; padding-left: 0.2rem;">
                ✉️ {user_email}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚪 Sign Out", use_container_width=True, key="sidebar_signout"):
            try:
                from modules.database import supabase
                supabase.auth.sign_out()
                logger.info(f"User signed out: {st.session_state.user_email}")
            except Exception as e:
                logger.warning(f"Error during sign out: {e}")
            st.session_state.user_id = None
            st.session_state.user_email = None
            st.session_state.pop('google_name', None)
            st.session_state.pop('google_picture', None)
            st.rerun()
    else:
        st.markdown("""
        <div style="background: rgba(255,170,0,0.06); border: 1px solid rgba(255,170,0,0.15); border-radius: 16px; padding: 1rem; margin-bottom: 1rem;">
            <div style="display: flex; align-items: center; gap: 0.8rem;">
                <div style="width: 44px; height: 44px; border-radius: 14px; background: rgba(255,170,0,0.15); display: flex; align-items: center; justify-content: center; font-size: 1.2rem; flex-shrink: 0;">
                    👤
                </div>
                <div>
                    <div style="font-weight: 600; font-size: 0.9rem; color: rgba(250,250,250,0.7);">Guest</div>
                    <div style="font-size: 0.75rem; color: rgba(250,250,250,0.4); margin-top: 0.15rem;">Sign in to save predictions</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("##### 🗂️ Navigation")
    st.markdown("""
    <div style="display: flex; flex-direction: column; gap: 0.3rem;">
        <div style="padding: 0.5rem 0.8rem; border-radius: 10px; background: rgba(108,99,255,0.08); font-size: 0.88rem;">🏠 <strong>Home</strong> <span style="color: rgba(250,250,250,0.3);">— Dashboard</span></div>
        <div style="padding: 0.5rem 0.8rem; border-radius: 10px; font-size: 0.88rem; color: rgba(250,250,250,0.6);">🔍 <strong>Symptom Checker</strong></div>
        <div style="padding: 0.5rem 0.8rem; border-radius: 10px; font-size: 0.88rem; color: rgba(250,250,250,0.6);">📊 <strong>Report History</strong></div>
        <div style="padding: 0.5rem 0.8rem; border-radius: 10px; font-size: 0.88rem; color: rgba(250,250,250,0.6);">💬 <strong>AI Chatbot</strong></div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("")
    st.markdown("---")
    st.markdown("##### ℹ️ About")
    st.markdown("""<p style="font-size: 0.8rem; color: rgba(250,250,250,0.4); line-height: 1.6;">
    AI-powered disease detection using ML. Analyzes symptoms to predict diseases with confidence scores.
    </p>""", unsafe_allow_html=True)
    st.markdown("---")
    st.caption("v2.0.0 • Built with ❤️ & AI")

# ── Main Content: Home Page ──

# Hero Section
st.markdown("""
<div class="hero-container">
    <div class="hero-badge">✨ AI-POWERED MEDICAL ASSISTANT</div>
    <div class="hero-title">🧠 MedDetect AI</div>
    <div class="hero-subtitle">
        Input your symptoms and let our machine learning model analyze them to predict 
        possible diseases with confidence scores, severity levels, and actionable health advice.
    </div>
    <div class="hero-stats">
        <div class="stat-item">
            <div class="stat-number">221+</div>
            <div class="stat-label">Diseases</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">382+</div>
            <div class="stat-label">Symptoms</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">94.6%</div>
            <div class="stat-label">Accuracy</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">9400+</div>
            <div class="stat-label">Training Samples</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# CTA
st.markdown("""
<div class="cta-section">
    <a href="/Symptom_Checker" target="_self" class="cta-btn">
        🔬 Start Symptom Analysis →
    </a>
</div>
""", unsafe_allow_html=True)

# Feature Cards
st.markdown("""
<div class="feature-grid">
    <div class="feature-card">
        <div class="feature-icon">🔍</div>
        <div class="feature-title">Smart Symptom Analysis</div>
        <div class="feature-desc">Select from 382+ symptoms with auto-suggestions. Our NLP engine also extracts symptoms from plain text descriptions.</div>
    </div>
    <div class="feature-card">
        <div class="feature-icon">🤖</div>
        <div class="feature-title">ML-Powered Predictions</div>
        <div class="feature-desc">Random Forest classifier trained on 9,400+ samples delivers predictions with confidence scores for 221+ diseases.</div>
    </div>
    <div class="feature-card">
        <div class="feature-icon">🏥</div>
        <div class="feature-title">Disease Information</div>
        <div class="feature-desc">Get detailed descriptions, causes, precautions, home remedies, and severity levels for each predicted condition.</div>
    </div>
    <div class="feature-card">
        <div class="feature-icon">📄</div>
        <div class="feature-title">PDF Health Reports</div>
        <div class="feature-desc">Download comprehensive PDF reports with predictions, precautions, and treatment suggestions to share with your doctor.</div>
    </div>
    <div class="feature-card">
        <div class="feature-icon">💬</div>
        <div class="feature-title">Gemini AI Chatbot</div>
        <div class="feature-desc">Ask health questions and get empathetic, informative responses powered by Google's Gemini AI with medical context.</div>
    </div>
    <div class="feature-card">
        <div class="feature-icon">⚡</div>
        <div class="feature-title">Instant Risk Assessment</div>
        <div class="feature-desc">Real-time severity analysis with color-coded risk levels and emergency alerts for critical conditions.</div>
    </div>
</div>
""", unsafe_allow_html=True)

# How to use
st.markdown("### 🚀 How to Use")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <div class="step-card">
        <div class="step-number">1</div>
        <div class="step-title">Describe Symptoms</div>
        <div class="step-desc">Navigate to Symptom Checker and describe how you're feeling or select from the list.</div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="step-card">
        <div class="step-number">2</div>
        <div class="step-title">Get AI Analysis</div>
        <div class="step-desc">Our ML model processes your input and predicts diseases with confidence scores.</div>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div class="step-card">
        <div class="step-number">3</div>
        <div class="step-title">Review & Download</div>
        <div class="step-desc">See results with severity levels, remedies, and download a comprehensive PDF report.</div>
    </div>
    """, unsafe_allow_html=True)

# Disclaimer
st.markdown("""
<div class="disclaimer-box">
    ⚠️ <strong>Medical Disclaimer:</strong> This system is for <strong>informational and educational purposes only</strong>. 
    It does NOT replace professional medical advice, diagnosis, or treatment. Always seek the advice of a qualified 
    healthcare provider with any questions regarding a medical condition.
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    MedDetect AI v2.0 • Powered by Machine Learning & Google Gemini<br>
    Made with ❤️ for better health awareness
</div>
""", unsafe_allow_html=True)
