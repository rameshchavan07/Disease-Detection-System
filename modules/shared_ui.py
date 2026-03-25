"""
Shared Premium CSS & Sidebar Component
Provides consistent styling and user profile across all pages.
"""
import streamlit as st


def inject_premium_css():
    """Inject the global premium design system CSS into any page."""
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

*, *::before, *::after { font-family: 'Plus Jakarta Sans', sans-serif !important; }
html, body, [class*="st-"] { font-family: 'Plus Jakarta Sans', sans-serif !important; }

/* Preserve Streamlit's icon fonts */
[data-testid="stSidebarCollapseButton"] span,
[data-testid="stIconMaterial"],
.material-symbols-rounded,
.material-symbols-outlined,
[class*="material-symbols"],
[class*="stIcon"],
[data-testid="stSidebarCollapseButton"] *,
[data-testid="baseButton-headerNoPadding"] span {
    font-family: 'Material Symbols Rounded', sans-serif !important;
}

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

html { scroll-behavior: smooth; }

.stApp {
    background: linear-gradient(135deg, #0a0e1a 0%, #111827 40%, #0f172a 70%, #0a0e1a 100%);
}

.main .block-container { max-width: 1200px; padding-top: 1.5rem; position: relative; z-index: 1; }

/* Animated gradient orbs */
.stApp::before {
    content: '';
    position: fixed; top: -50%; left: -50%; width: 200%; height: 200%;
    background: radial-gradient(circle at 20% 50%, rgba(108,99,255,0.06) 0%, transparent 50%),
                radial-gradient(circle at 80% 20%, rgba(99,179,255,0.04) 0%, transparent 50%),
                radial-gradient(circle at 50% 80%, rgba(255,99,195,0.03) 0%, transparent 50%);
    animation: orbFloat 20s ease-in-out infinite;
    pointer-events: none; z-index: 0;
}

@keyframes orbFloat {
    0%, 100% { transform: translate(0, 0) rotate(0deg); }
    33% { transform: translate(30px, -20px) rotate(3deg); }
    66% { transform: translate(-20px, 15px) rotate(-2deg); }
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
    box-shadow: 0 0 20px rgba(108,99,255,0.55), 0 8px 25px rgba(108,99,255,0.35) !important;
}

/* Styled Input Fields */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div,
.stMultiSelect > div > div {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(108,99,255,0.15) !important;
    border-radius: 12px !important;
    color: #FAFAFA !important;
    transition: border-color 0.3s ease, box-shadow 0.3s ease !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: rgba(108,99,255,0.5) !important;
    box-shadow: 0 0 12px rgba(108,99,255,0.15) !important;
    outline: none !important;
}

.stMultiSelect [data-baseweb="tag"] {
    background: rgba(108,99,255,0.2) !important;
    border: 1px solid rgba(108,99,255,0.4) !important;
    border-radius: 8px !important;
}

/* Dropdown menus */
[data-baseweb="popover"] > div {
    background: #161b26 !important;
    border: 1px solid rgba(108,99,255,0.15) !important;
    border-radius: 12px !important;
}

[data-baseweb="menu"] [role="option"] { color: #FAFAFA !important; }
[data-baseweb="menu"] [role="option"]:hover { background: rgba(108,99,255,0.12) !important; }

/* Download button */
.stDownloadButton > button {
    background: linear-gradient(135deg, #00D68F, #00B377) !important;
}
.stDownloadButton > button:hover {
    box-shadow: 0 0 20px rgba(0,214,143,0.4), 0 8px 25px rgba(0,214,143,0.25) !important;
}

/* Expander */
.streamlit-expanderHeader {
    background: rgba(255,255,255,0.03) !important;
    border-radius: 12px !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] { gap: 8px; }
.stTabs [data-baseweb="tab"] {
    background: rgba(255,255,255,0.04) !important;
    border-radius: 10px !important;
    border: 1px solid rgba(108,99,255,0.1) !important;
    color: rgba(250,250,250,0.6) !important;
}
.stTabs [aria-selected="true"] {
    background: rgba(108,99,255,0.15) !important;
    border-color: rgba(108,99,255,0.3) !important;
    color: #FAFAFA !important;
}

/* Metric cards */
[data-testid="stMetricValue"] { color: #FAFAFA !important; }
[data-testid="stMetricLabel"] { color: rgba(250,250,250,0.5) !important; }
</style>
""", unsafe_allow_html=True)


def render_sidebar():
    """Render the consistent premium sidebar with user profile and navigation."""
    with st.sidebar:
        st.markdown("### 🧠 MedDetect AI")

        # User profile card
        if st.session_state.get("user_id"):
            user_email = st.session_state.get("user_email", "User")
            user_name = st.session_state.get("google_name", "")
            display_name = user_name if user_name else user_email.split("@")[0].title()
            initial = display_name[0].upper() if display_name else "U"

            st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(108,99,255,0.08), rgba(99,179,255,0.05)); border: 1px solid rgba(108,99,255,0.15); border-radius: 16px; padding: 1rem; margin-bottom: 1rem;">
                <div style="display: flex; align-items: center; gap: 0.8rem;">
                    <div style="width: 44px; height: 44px; border-radius: 14px; background: linear-gradient(135deg, #6C63FF, #4B45B2); display: flex; align-items: center; justify-content: center; font-size: 1.2rem; font-weight: 700; color: white; flex-shrink: 0; box-shadow: 0 4px 12px rgba(108,99,255,0.3);">
                        {initial}
                    </div>
                    <div style="overflow: hidden; flex: 1; min-width: 0;">
                        <div style="font-weight: 700; font-size: 0.92rem; color: #FAFAFA; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                            {display_name}
                        </div>
                        <div style="display: flex; align-items: center; gap: 0.3rem; margin-top: 0.2rem;">
                            <div style="width: 6px; height: 6px; border-radius: 50%; background: #00D68F; box-shadow: 0 0 6px #00D68F;"></div>
                            <span style="font-size: 0.72rem; color: #00D68F;">Online</span>
                        </div>
                    </div>
                </div>
                <div style="font-size: 0.75rem; color: rgba(250,250,250,0.4); margin-top: 0.8rem; word-break: break-all; padding-left: 0.2rem; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 0.8rem;">
                    &#9993; {user_email}
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button("🚪 Sign Out", use_container_width=True, key="sidebar_signout_shared"):
                try:
                    from modules.database import supabase
                    supabase.auth.sign_out()
                except Exception:
                    pass
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
                        &#128100;
                    </div>
                    <div>
                        <div style="font-weight: 600; font-size: 0.9rem; color: rgba(250,250,250,0.7);">Guest</div>
                        <div style="font-size: 0.75rem; color: rgba(250,250,250,0.4); margin-top: 0.15rem;">Sign in to save predictions</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # Quick Navigation
        st.markdown("""
        <div style="margin-bottom: 1rem;">
            <div style="font-size: 0.7rem; text-transform: uppercase; letter-spacing: 1.5px; color: rgba(250,250,250,0.3); margin-bottom: 0.6rem; padding-left: 0.3rem;">Navigation</div>
            <a href="/" target="_self" style="display: flex; align-items: center; gap: 0.6rem; padding: 0.6rem 0.8rem; border-radius: 10px; color: rgba(250,250,250,0.7); text-decoration: none; font-size: 0.85rem; transition: all 0.2s; margin-bottom: 0.2rem;">
                <span>🏠</span> Home
            </a>
            <a href="/Sign_In" target="_self" style="display: flex; align-items: center; gap: 0.6rem; padding: 0.6rem 0.8rem; border-radius: 10px; color: rgba(250,250,250,0.7); text-decoration: none; font-size: 0.85rem; transition: all 0.2s; margin-bottom: 0.2rem;">
                <span>🔑</span> Sign In
            </a>
            <a href="/Symptom_Checker" target="_self" style="display: flex; align-items: center; gap: 0.6rem; padding: 0.6rem 0.8rem; border-radius: 10px; color: rgba(250,250,250,0.7); text-decoration: none; font-size: 0.85rem; transition: all 0.2s; margin-bottom: 0.2rem;">
                <span>🔍</span> Symptom Checker
            </a>
            <a href="/Report_History" target="_self" style="display: flex; align-items: center; gap: 0.6rem; padding: 0.6rem 0.8rem; border-radius: 10px; color: rgba(250,250,250,0.7); text-decoration: none; font-size: 0.85rem; transition: all 0.2s;">
                <span>📊</span> Report History
            </a>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("""
        <div style="font-size: 0.7rem; color: rgba(250,250,250,0.2); padding: 0.5rem 0.3rem;">
            MedDetect AI v2.0<br>Powered by ML & Groq AI
        </div>
        """, unsafe_allow_html=True)
