"""
Supabase Database Client Module for MedDetect AI
"""
from supabase import create_client, Client
import streamlit as st
import sys, os
import time
from datetime import datetime
from functools import wraps

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import SUPABASE_URL, SUPABASE_KEY
from modules.logger import get_logger

logger = get_logger("database")

def with_retry(max_retries=3, base_delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            delay = base_delay
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logger.warning(f"Attempt {attempt + 1}/{max_retries} failed for {func.__name__}: {str(e)}")
                    if attempt == max_retries - 1:
                        logger.error(f"All {max_retries} attempts failed for {func.__name__}")
                        return False if func.__name__ != "get_user_predictions" else []
                    time.sleep(delay)
                    delay *= 2
            return False if func.__name__ != "get_user_predictions" else []
        return wrapper
    return decorator

# Initialize Supabase client
@st.cache_resource
def init_supabase() -> Client | None:
    if SUPABASE_URL and SUPABASE_KEY:
        try:
            client = create_client(SUPABASE_URL, SUPABASE_KEY)
            logger.info("Supabase client initialized successfully.")
            return client
        except Exception as e:
            logger.error(f"Failed to initialize Supabase: {e}")
            st.error(f"Failed to initialize database connection.")
            return None
    logger.warning("Supabase credentials not found.")
    return None

supabase = init_supabase()

@with_retry()
def save_prediction(user_id: str, symptoms: list, predictions: list):
    """Save a prediction to Supabase"""
    if not supabase:
        return False
        
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
    logger.info(f"Saved prediction for user {user_id}")
    return len(result.data) > 0

@with_retry()
def get_user_predictions(user_id: str):
    """Get all past predictions for a user"""
    if not supabase:
        return []
        
    result = supabase.table("predictions").select("*").eq("user_id", user_id).order("created_at", desc=True).execute()
    logger.info(f"Fetched {len(result.data)} predictions for user {user_id}")
    return result.data

@with_retry()
def delete_user_history(user_id: str):
    """Delete all prediction history for a specific user"""
    if not supabase:
        return False
        
    supabase.table("predictions").delete().eq("user_id", user_id).execute()
    logger.info(f"Deleted prediction history for user {user_id}")
    return True
