import os
import json
import requests
import streamlit as st
from groq import Groq

@st.cache_data(ttl=3600*24)
def get_nearest_doctors(specialist: str, override_city: str = None):
    """
    Uses given city or IP geolocation to find user's city, 
    then uses Llama 3 to find top real doctors in that city.
    """
    # Step 1: Geolocation
    if override_city:
        city = override_city
    else:
        city = "New York"
        try:
            loc = requests.get('http://ip-api.com/json/', timeout=3).json()
            if "city" in loc and loc["city"]:
                city = loc["city"]
        except Exception:
            pass

    # Step 2: Query Groq Llama 3
    try:
        from config.settings import GROQ_API_KEY
    except ImportError:
        GROQ_API_KEY = None
        
    api_key = GROQ_API_KEY or os.environ.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY"))
    if not api_key:
        return None
        
    try:
        client = Groq(api_key=api_key)
        
        prompt = (
            f"You are a medical directory assistant. Return a JSON formatted list containing exactly 2 highly-rated, REAL {specialist} clinics or hospitals located in the city of {city}. "
            f"If you do not know real doctors in {city}, make an educated guess using real prominent main hospitals in {city}. "
            f"Format must be exactly a JSON object with one key 'doctors', which holds a list. Each object must have exactly three string keys: 'name', 'phone', and 'address'. "
            f"Just give pure JSON, no code fences. Output valid JSON only."
        )

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a specialized medical directory robot. Output JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            response_format={"type": "json_object"}
        )
        
        json_data = json.loads(response.choices[0].message.content)
        doctors = json_data.get("doctors", [])
        if doctors and len(doctors) > 0:
            return {"city": city, "doctors": doctors[:2]}
            
    except Exception as e:
        print(f"Doctor Locator JSON Error: {e}")
        
    return None
