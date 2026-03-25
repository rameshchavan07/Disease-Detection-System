"""
ML Engine - Disease Prediction Module
Loads trained model and provides prediction functions.
"""
import os, re, sys
import joblib
import numpy as np
import pandas as pd
import streamlit as st

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "trained_model.pkl")

@st.cache_resource(show_spinner="🧠 Loading AI model (first time only)...")
def _load_model():
    """Load and cache the trained model using Streamlit's resource cache."""
    if not os.path.exists(MODEL_PATH):
        import subprocess
        st.toast("First Server Boot: Synthesizing random forest model... This takes ~5 seconds.", icon="⚙️")
        train_script = os.path.join(BASE_DIR, "models", "train_model.py")
        subprocess.run([sys.executable, train_script], check=True)
    return joblib.load(MODEL_PATH)

def get_all_symptoms():
    """Return list of all valid symptom names."""
    data = _load_model()
    return data["feature_names"]

def get_all_diseases():
    """Return list of all disease names."""
    data = _load_model()
    return data["disease_names"]

def _sanitize_symptom(symptom: str) -> str:
    """Sanitize a symptom string — only allow alphanumeric and underscores."""
    s = symptom.strip().lower().replace(" ", "_")
    s = re.sub(r'[^a-z0-9_]', '', s)
    return s

def predict_disease(symptoms: list, top_k: int = 3):
    """
    Predict diseases based on input symptoms.
    Args:
        symptoms: List of symptom name strings
        top_k: Number of top predictions to return
    Returns:
        List of dicts with 'disease', 'confidence', 'rank'
    """
    data = _load_model()
    model = data["model"]
    le = data["label_encoder"]
    features = data["feature_names"]
    
    # Build feature vector with input validation
    X = np.zeros((1, len(features)))
    matched = []
    for s in symptoms:
        s_clean = _sanitize_symptom(s)
        if s_clean in features:
            X[0, features.index(s_clean)] = 1
            matched.append(s_clean)
    
    if not matched:
        return []
    
    # Get probability predictions (use DataFrame to avoid feature name warnings)
    probas = model.predict_proba(pd.DataFrame(X, columns=features))[0]
    top_indices = np.argsort(probas)[::-1][:top_k]
    
    results = []
    for rank, idx in enumerate(top_indices, 1):
        disease_name = le.inverse_transform([idx])[0]
        confidence = float(probas[idx])
        if confidence > 0.001:  # Filter very low probabilities
            results.append({
                "disease": disease_name,
                "confidence": round(confidence * 100, 2),
                "rank": rank
            })
    
    return results

def get_model_accuracy():
    """Return model accuracy metrics."""
    data = _load_model()
    return {
        "accuracy": round(data.get("accuracy", 0) * 100, 2),
        "cv_accuracy": round(data.get("cv_accuracy", 0) * 100, 2)
    }

def format_symptom_name(symptom: str) -> str:
    """Convert symptom_name to Symptom Name for display."""
    return symptom.replace("_", " ").title()
