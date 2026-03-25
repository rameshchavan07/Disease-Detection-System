"""
Authentication Page
Supabase Login/Signup + Google Sign-In via raw OAuth 2.0
Premium glassmorphism UI.
"""
import streamlit as st
import sys, os, json, requests, time
from urllib.parse import urlencode

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)
from modules.database import supabase
from modules.shared_ui import inject_premium_css, render_sidebar

GOOGLE_CRED_PATH = os.path.join(PROJECT_ROOT, 'google_credentials.json')
# Use Google's redirect URI from secrets if it exists, otherwise use localhost
REDIRECT_URI = st.secrets.get("google", {}).get("redirect_uri", 'https://disease-detection-system-rutu.streamlit.app/Sign_in')

st.set_page_config(page_title="Sign In - MedDetect AI", page_icon="🔑", layout="centered")

# Inject shared premium CSS & sidebar
inject_premium_css()
render_sidebar()

# ── Page-specific CSS ──
st.markdown("""
<style>

.stApp::before {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: radial-gradient(circle at 50% 0%, rgba(108,99,255,0.08) 0%, transparent 50%);
    pointer-events: none;
}

/* Google button */
.google-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    background: linear-gradient(135deg, #ffffff 0%, #f5f5f5 100%);
    color: #444 !important;
    padding: 12px 24px;
    text-decoration: none !important;
    border-radius: 12px;
    font-weight: 700;
    font-size: 0.95rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.15);
    transition: all 0.3s ease;
    cursor: pointer;
    border: 1px solid rgba(0,0,0,0.08);
}

.google-btn:hover {
    box-shadow: 0 6px 20px rgba(0,0,0,0.2);
    transform: translateY(-2px);
    color: #222 !important;
}

/* Divider */
.auth-divider {
    display: flex;
    align-items: center;
    text-align: center;
    margin: 1.5rem 0;
    color: rgba(250,250,250,0.25);
    font-size: 0.85rem;
}

.auth-divider::before, .auth-divider::after {
    content: '';
    flex: 1;
    border-bottom: 1px solid rgba(250,250,250,0.08);
}

.auth-divider::before { margin-right: 1rem; }
.auth-divider::after { margin-left: 1rem; }

/* Welcome header */
.auth-header {
    text-align: center;
    margin-bottom: 2rem;
}

.auth-header h1 {
    font-size: 2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #6C63FF, #8B83FF);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.3rem;
}

.auth-header p {
    color: rgba(250,250,250,0.5);
    font-size: 0.9rem;
}

.welcome-card {
    text-align: center;
    padding: 3rem 2rem;
    background: linear-gradient(145deg, rgba(0,214,143,0.06), rgba(0,214,143,0.02));
    border: 1px solid rgba(0,214,143,0.15);
    border-radius: 20px;
    margin-top: 1rem;
}
</style>
""", unsafe_allow_html=True)

if not supabase:
    st.error("Database connection not configured.")
    st.stop()

# Init session
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "user_email" not in st.session_state:
    st.session_state.user_email = None

# ── Google OAuth Credentials ──
google_creds = None

# 1. Check Streamlit Secrets first (for Cloud deployment)
if "google" in st.secrets:
    google_creds = st.secrets["google"]
# 2. Fall back to local JSON file
elif os.path.exists(GOOGLE_CRED_PATH):
    try:
        with open(GOOGLE_CRED_PATH, 'r') as f:
            raw = json.load(f)
            google_creds = raw.get('web', raw.get('installed', raw))
    except Exception as e:
        st.error(f"Error loading local credentials: {e}")

query_params = st.query_params
if "code" in query_params and not st.session_state.user_id and google_creds:
    try:
        token_response = requests.post(
            'https://oauth2.googleapis.com/token',
            data={
                'code': query_params['code'],
                'client_id': google_creds['client_id'],
                'client_secret': google_creds['client_secret'],
                'redirect_uri': REDIRECT_URI,
                'grant_type': 'authorization_code',
            }
        )
        token_data = token_response.json()
        
        if 'error' in token_data:
            st.error(f"Google Sign-In error: {token_data.get('error_description', token_data['error'])}")
        else:
            import base64
            id_token_jwt = token_data.get('id_token', '')
            payload = id_token_jwt.split('.')[1]
            payload += '=' * (4 - len(payload) % 4)
            user_info = json.loads(base64.urlsafe_b64decode(payload))
            
            # Use Google's unique 'sub' claim for user_id (consistent unique ID)
            st.session_state.user_id = user_info.get('sub', user_info.get('email'))
            st.session_state.user_email = user_info.get('email')
            st.session_state.google_name = user_info.get('name', '')
            st.session_state.google_picture = user_info.get('picture', '')
            st.session_state.login_time = time.time()
            
            st.query_params.clear()
            st.rerun()
    except Exception as e:
        st.error(f"Google Sign-In failed: {e}")

# ── Already Logged In ──
if st.session_state.user_id:
    st.markdown(f"""
    <div class="welcome-card">
        <div style="font-size: 3rem; margin-bottom: 1rem;">👋</div>
        <h2 style="margin: 0; color: #FAFAFA;">Welcome back!</h2>
        <p style="color: rgba(250,250,250,0.6); margin-top: 0.5rem;">
            Signed in as <strong style="color: #00D68F;">{st.session_state.user_email}</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🚪 Sign Out", use_container_width=True):
            try:
                supabase.auth.sign_out()
            except Exception:
                pass
            st.session_state.user_id = None
            st.session_state.user_email = None
            st.session_state.pop('google_name', None)
            st.session_state.pop('google_picture', None)
            st.rerun()
    st.stop()

# ── Auth UI ──
st.markdown("""
<div class="auth-header">
    <h1>🔑 MedDetect AI</h1>
    <p>Sign in to save and access your prediction history securely.</p>
</div>
""", unsafe_allow_html=True)

# ── Google Sign-In ──
if google_creds:
    auth_params = urlencode({
        'client_id': google_creds['client_id'],
        'redirect_uri': REDIRECT_URI,
        'response_type': 'code',
        'scope': 'openid email profile',
        'access_type': 'offline',
        'prompt': 'consent',
    })
    authorization_url = f"https://accounts.google.com/o/oauth2/v2/auth?{auth_params}"
    
    st.markdown(f'''
    <div style="margin-bottom: 0.5rem;">
        <a href="{authorization_url}" target="_self" class="google-btn">
            <span style="font-size: 1.3em; margin-right: 10px;">🌐</span> Continue with Google
        </a>
    </div>
    ''', unsafe_allow_html=True)
else:
    st.info("💡 Place `google_credentials.json` in the project root to enable Google Sign-In.")

# Divider
st.markdown('<div class="auth-divider">or use email</div>', unsafe_allow_html=True)

# ── Email Auth Tabs ──
tab1, tab2 = st.tabs(["🔒 Sign In", "📝 Create Account"])

with tab1:
    st.subheader("Welcome Back")
    login_email = st.text_input("Email", key="login_email", placeholder="you@example.com")
    login_password = st.text_input("Password", type="password", key="login_password")
    
    if st.button("Sign In", type="primary", use_container_width=True):
        if not login_email or not login_password:
            st.warning("Please enter both email and password.")
        else:
            with st.spinner("Signing in..."):
                try:
                    response = supabase.auth.sign_in_with_password({"email": login_email, "password": login_password})
                    st.session_state.user_id = response.user.id
                    st.session_state.user_email = response.user.email
                    st.balloons()
                    st.success("✅ Successfully signed in!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Login failed: {str(e)}")
                    
with tab2:
    st.subheader("Join MedDetect AI")
    st.caption("Create a free account to track your health predictions.")
    signup_email = st.text_input("Email", key="signup_email", placeholder="you@example.com")
    signup_password = st.text_input("Password", type="password", help="Must be at least 6 characters.", key="signup_password")
    
    if st.button("Create Account", type="primary", use_container_width=True):
        if not signup_email or not signup_password:
            st.warning("Please enter both email and password.")
        elif len(signup_password) < 6:
            st.warning("Password must be at least 6 characters.")
        else:
            with st.spinner("Creating account..."):
                try:
                    response = supabase.auth.sign_up({"email": signup_email, "password": signup_password})
                    if response.user:
                        st.balloons()
                        st.success("🎉 Account created successfully! You can now sign in.")
                    else:
                        st.warning("Check your email for a confirmation link.")
                except Exception as e:
                    if "User already registered" in str(e):
                        st.error("This email is already registered. Please sign in instead.")
                    else:
                        st.error(f"Signup failed: {str(e)}")

from modules.floating_chat import render_floating_chatbot
render_floating_chatbot()
