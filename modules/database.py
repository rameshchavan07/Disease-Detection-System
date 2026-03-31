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

# ──────────────────────────────────────────
# Doctor Functions
# ──────────────────────────────────────────

@with_retry()
def register_doctor(user_id: str, name: str, email: str, specialty: str, phone: str = "", city: str = "", hospital_name: str = "", hospital_address: str = ""):
    """Register a new doctor profile."""
    if not supabase:
        return False
    data = {
        "user_id": user_id,
        "name": name,
        "email": email,
        "specialty": specialty,
        "phone": phone,
        "city": city,
        "hospital_name": hospital_name,
        "hospital_address": hospital_address,
        "created_at": datetime.now().isoformat()
    }
    result = supabase.table("doctors").insert(data).execute()
    logger.info(f"Registered doctor: {name} ({specialty})")
    return len(result.data) > 0

def get_doctor_by_user_id(user_id: str):
    """Check if a user is a registered doctor. Returns doctor record or None."""
    if not supabase:
        return None
    try:
        result = supabase.table("doctors").select("*").eq("user_id", user_id).execute()
        return result.data[0] if result.data else None
    except Exception as e:
        logger.error(f"Error fetching doctor: {e}")
        return None

def get_registered_doctors(specialty: str = None):
    """Get all registered doctors, optionally filtered by specialty."""
    if not supabase:
        return []
    try:
        query = supabase.table("doctors").select("*")
        if specialty:
            query = query.eq("specialty", specialty)
        result = query.order("name").execute()
        return result.data
    except Exception as e:
        logger.error(f"Error fetching doctors: {e}")
        return []

# ──────────────────────────────────────────
# Appointment Functions
# ──────────────────────────────────────────

@with_retry()
def save_appointment(patient_id: str, patient_email: str, doctor_id: str, 
                     doctor_name: str, specialty: str, appointment_date: str, 
                     appointment_time: str, meeting_url: str):
    """Save a new appointment to the database."""
    if not supabase:
        return False
    data = {
        "patient_id": patient_id,
        "patient_email": patient_email,
        "doctor_id": doctor_id,
        "doctor_name": doctor_name,
        "specialty": specialty,
        "appointment_date": appointment_date,
        "appointment_time": appointment_time,
        "meeting_url": meeting_url,
        "status": "upcoming",
        "created_at": datetime.now().isoformat()
    }
    result = supabase.table("appointments").insert(data).execute()
    logger.info(f"Saved appointment: {patient_email} with Dr. {doctor_name}")
    return len(result.data) > 0

def get_doctor_appointments(doctor_id: str):
    """Get all appointments for a specific doctor."""
    if not supabase:
        return []
    try:
        result = (supabase.table("appointments")
                  .select("*")
                  .eq("doctor_id", doctor_id)
                  .order("appointment_date", desc=False)
                  .execute())
        return result.data
    except Exception as e:
        logger.error(f"Error fetching doctor appointments: {e}")
        return []

def get_patient_appointments(patient_id: str):
    """Get all appointments for a specific patient."""
    if not supabase:
        return []
    try:
        result = (supabase.table("appointments")
                  .select("*")
                  .eq("patient_id", patient_id)
                  .order("appointment_date", desc=False)
                  .execute())
        return result.data
    except Exception as e:
        logger.error(f"Error fetching patient appointments: {e}")
        return []

def update_appointment_status(appointment_id: str, status: str):
    """Update the status of an appointment (upcoming/completed/cancelled)."""
    if not supabase:
        return False
    try:
        supabase.table("appointments").update({"status": status}).eq("id", appointment_id).execute()
        logger.info(f"Updated appointment {appointment_id} to {status}")
        return True
    except Exception as e:
        logger.error(f"Error updating appointment: {e}")
        return False

# ──────────────────────────────────────────
# Prescription Functions
# ──────────────────────────────────────────

@with_retry()
def save_prescription(appointment_id: str, doctor_id: str, patient_id: str, patient_email: str, diagnosis: str, medicines: list, notes: str):
    """Save a prescription for an appointment."""
    if not supabase:
        return False
    data = {
        "appointment_id": appointment_id,
        "doctor_id": doctor_id,
        "patient_id": patient_id,
        "patient_email": patient_email,
        "diagnosis": diagnosis,
        "medicines": medicines,
        "notes": notes,
        "created_at": datetime.now().isoformat()
    }
    result = supabase.table("prescriptions").insert(data).execute()
    logger.info(f"Saved prescription for appointment {appointment_id}")
    return len(result.data) > 0

def get_patient_prescriptions(patient_id: str):
    """Get all prescriptions for a specific patient."""
    if not supabase:
        return []
    try:
        result = (supabase.table("prescriptions")
                  .select("*, appointments(*), doctors(*)")
                  .eq("patient_id", patient_id)
                  .order("created_at", desc=True)
                  .execute())
        return result.data
    except Exception as e:
        logger.error(f"Error fetching patient prescriptions: {e}")
        return []
