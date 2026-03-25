"""
Supabase Database Client Module for MedDetect AI
"""
from supabase import create_client, Client
import streamlit as st
import sys, os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import SUPABASE_URL, SUPABASE_KEY

# Initialize Supabase client
@st.cache_resource
def init_supabase() -> Client | None:
    if SUPABASE_URL and SUPABASE_KEY:
        try:
            return create_client(SUPABASE_URL, SUPABASE_KEY)
        except Exception as e:
            st.error(f"Failed to initialize Supabase: {e}")
            return None
    return None

supabase = init_supabase()

def save_prediction(user_id: str, symptoms: list, predictions: list):
    """Save a prediction to Supabase"""
    if not supabase:
        return False
        
    try:
        top_disease = predictions[0]['disease'] if predictions else "Unknown"
        confidence = float(predictions[0]['confidence']) if predictions else 0.0
        
        data = {
            "user_id": user_id,
            "symptoms": symptoms,
            "predicted_disease": top_disease,
            "confidence": confidence,
            "created_at": datetime.now().isoformat()
        }
        
        result = supabase.table("predictions").insert(data).execute()
        return len(result.data) > 0
    except Exception as e:
        print(f"Error saving prediction to Supabase: {e}")
        return False

def get_user_predictions(user_id: str):
    """Get all past predictions for a user"""
    if not supabase:
        return []
        
    try:
        result = supabase.table("predictions").select("*").eq("user_id", user_id).order("created_at", desc=True).execute()
        return result.data
    except Exception as e:
        print(f"Error fetching predictions from Supabase: {e}")
        return []

def delete_user_history(user_id: str):
    """Delete all prediction history for a specific user"""
    if not supabase:
        return False
        
    try:
        supabase.table("predictions").delete().eq("user_id", user_id).execute()
        return True
    except Exception as e:
        print(f"Error deleting predictions from Supabase: {e}")
        return False
