"""
Application Settings & Constants
Multi-Disease Detection System
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ──────────────────────────────────────────
# App Configuration
# ──────────────────────────────────────────
APP_NAME = "MedDetect AI"
APP_VERSION = "2.0.0"
APP_VERSION_DISPLAY = f"v{APP_VERSION}"
APP_DESCRIPTION = "AI-Powered Multi-Disease Detection System"
APP_ICON = "🧠"

# Stats displayed on the home page (update when retraining model)
TOTAL_DISEASES = "221+"
TOTAL_SYMPTOMS = "382+"
MODEL_ACCURACY_DISPLAY = "94.6%"
TRAINING_SAMPLES = "9,400+"

# ──────────────────────────────────────────
# Paths
# ──────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
MODELS_DIR = os.path.join(BASE_DIR, "models")
MODEL_PATH = os.path.join(MODELS_DIR, "trained_model.pkl")
DATASET_PATH = os.path.join(DATA_DIR, "dataset.csv")
DISEASE_INFO_PATH = os.path.join(DATA_DIR, "disease_info.json")
SYMPTOM_SEVERITY_PATH = os.path.join(DATA_DIR, "symptom_severity.json")

# ──────────────────────────────────────────
# Supabase Configuration (loaded from .env)
# ──────────────────────────────────────────
SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "")

# ──────────────────────────────────────────
# ML Model Settings
# ──────────────────────────────────────────
MODEL_TYPE = "RandomForest"
N_ESTIMATORS = 200
RANDOM_STATE = 42
TEST_SIZE = 0.2
TOP_K_PREDICTIONS = 3

# ──────────────────────────────────────────
# Severity Levels
# ──────────────────────────────────────────
SEVERITY_LEVELS = {
    "low": {"label": "Low", "color": "#4CAF50", "icon": "🟢"},
    "moderate": {"label": "Moderate", "color": "#FF9800", "icon": "🟡"},
    "high": {"label": "High", "color": "#F44336", "icon": "🔴"},
    "critical": {"label": "Critical", "color": "#B71C1C", "icon": "🚨"},
}

# ──────────────────────────────────────────
# Medical Disclaimer
# ──────────────────────────────────────────
DISCLAIMER = (
    "⚠️ **Medical Disclaimer**: This system is for informational and educational "
    "purposes only. It does NOT replace professional medical advice, diagnosis, or "
    "treatment. Always seek the advice of a qualified healthcare provider with any "
    "questions regarding a medical condition."
)

def get_secret(name: str, default: str = "") -> str:
    """Safe retrieval of secrets from st.secrets or env vars."""
    try:
        import streamlit as st
        # This only works when running via streamlit
        if name in st.secrets:
            return st.secrets[name]
    except Exception:
        pass
    return os.environ.get(name, default)

# ── API Keys ──
GEMINI_API_KEY = get_secret("GEMINI_API_KEY")
# Support for Multi-Key Rotation
GEMINI_API_KEYS = get_secret("GEMINI_API_KEYS")
if not GEMINI_API_KEYS:
    GEMINI_API_KEYS = [GEMINI_API_KEY] if GEMINI_API_KEY else []
elif isinstance(GEMINI_API_KEYS, str):
    # If passed as a comma-separated string in .env
    GEMINI_API_KEYS = [k.strip() for k in GEMINI_API_KEYS.split(",") if k.strip()]

GROQ_API_KEY = get_secret("GROQ_API_KEY")

# ──────────────────────────────────────────
# Session & Rate Limiting
# ──────────────────────────────────────────
SESSION_TIMEOUT_MINUTES = 60
CHAT_RATE_LIMIT_PER_MINUTE = 10
