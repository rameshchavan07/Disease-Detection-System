import re
import os
from functools import lru_cache
from google import genai
from config.settings import GEMINI_API_KEYS, GROQ_API_KEY
from groq import Groq
from modules.logger import get_logger
import streamlit as st

logger = get_logger("nlp_extractor")

def groq_translate(text: str) -> str:
    """Fallback translation using Groq (Llama-3)."""
    if not GROQ_API_KEY:
        return text
    try:
        client = Groq(api_key=GROQ_API_KEY)
        prompt = f"Translate the following medical symptoms/description to concise clinical English. If it is already in English, return it exactly as it is. Output only the English translation: \"{text}\""
        
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"Groq Translation Fallback Error: {e}")
        return text

@lru_cache(maxsize=128)
def translate_to_english(text: str) -> str:
    """Uses a Pool of Gemini keys to translate symptoms. Rotates keys on 429 errors."""
    if not GEMINI_API_KEYS:
        logger.warning("No Gemini keys found in pool. Using Groq fallback.")
        return groq_translate(text)
    
    # Track the current key index in streamlit session state
    if "gemini_key_index" not in st.session_state:
        st.session_state.gemini_key_index = 0
    
    original_idx = st.session_state.gemini_key_index
    num_keys = len(GEMINI_API_KEYS)
    
    # Try all keys in the pool starting from current index
    for attempt in range(num_keys):
        current_idx = (original_idx + attempt) % num_keys
        api_key = GEMINI_API_KEYS[current_idx]
        
        try:
            client = genai.Client(api_key=api_key)
            prompt = f"Translate the following medical symptoms/description to concise clinical English. If it is already in English, return it exactly as it is. Output only the English translation: \"{text}\""
            
            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=prompt
            )
            
            # If successful, update the session index to keep using this key
            st.session_state.gemini_key_index = current_idx
            translated_text = response.text.strip()
            return translated_text if translated_text else text
            
        except Exception as e:
            error_msg = str(e).lower()
            if "429" in error_msg or "resource_exhausted" in error_msg:
                logger.warning(f"Key {current_idx} Quota Exceeded. Rotating to next key...")
                continue # Try next key
            
            logger.error(f"Gemini (Key {current_idx}) Error: {e}")
            break # Non-quota error, don't keep rotating for this request
    
    # If all Gemini keys fail, use Groq as final reserve
    logger.info("All Gemini keys exhausted. Falling back to Groq Reserve Engine.")
    st.toast("Gemini is busy; using Groq Reserve Engine... 🚀")
    return groq_translate(text)

# Synonym dictionary for better matching
SYNONYMS = {
    "fever": ["high_fever", "mild_fever"],
    "headache": ["headache"],
    "cough": ["cough", "persistent_cough", "chronic_cough"],
    "sneeze": ["continuous_sneezing"],
    "sneezing": ["continuous_sneezing"],
    "cold": ["chills", "shivering"],
    "chill": ["chills"],
    "stomach ache": ["stomach_pain", "abdominal_pain", "belly_pain"],
    "stomach pain": ["stomach_pain", "abdominal_pain", "belly_pain"],
    "stomach hurts": ["stomach_pain", "abdominal_pain", "belly_pain"],
    "tummy ache": ["stomach_pain", "abdominal_pain", "belly_pain"],
    "belly ache": ["stomach_pain", "abdominal_pain", "belly_pain"],
    "throw up": ["vomiting"],
    "throwing up": ["vomiting"],
    "vomit": ["vomiting"],
    "nauseous": ["nausea"],
    "dizzy": ["dizziness", "unsteadiness"],
    "dizziness": ["dizziness"],
    "tired": ["fatigue", "lethargy", "weakness_in_limbs"],
    "exhausted": ["fatigue"],
    "runny nose": ["runny_nose"],
    "stuffy nose": ["congestion", "sinus_pressure"],
    "sore throat": ["throat_irritation", "patches_in_throat"],
    "throat hurts": ["throat_irritation"],
    "chest hurts": ["chest_pain"],
    "chest pain": ["chest_pain"],
    "can't breathe": ["breathlessness", "difficulty_breathing"],
    "hard to breathe": ["breathlessness", "difficulty_breathing"],
    "short of breath": ["breathlessness"],
    "rash": ["skin_rash", "nodal_skin_eruptions"],
    "itch": ["itching"],
    "itchy": ["itching"],
    "joint pain": ["joint_pain", "knee_pain", "hip_joint_pain"],
    "muscle pain": ["muscle_pain", "muscle_weakness"],
    "body ache": ["muscle_pain", "fatigue"],
    "back pain": ["back_pain", "lower_back_pain"],
    "sweating": ["sweating"],
    "sweat": ["sweating"],
    "weight loss": ["weight_loss", "unexplained_weight_loss"],
    "losing weight": ["weight_loss"],
    "gaining weight": ["weight_gain"],
    "weight gain": ["weight_gain"],
    "blurry vision": ["blurred_vision", "blurred_and_distorted_vision"],
    "can't see": ["blurred_vision", "vision_loss_temporal"],
    "diarrhea": ["diarrhoea"],
    "constipated": ["constipation"],
    "heart beating fast": ["palpitations", "fast_heart_rate"],
    "palpitations": ["palpitations"],
    "blood in pee": ["blood_in_urine"],
    "blood in stool": ["bloody_stool", "rectal_bleeding"],
    "swollen legs": ["swollen_legs", "peripheral_edema"],
    "yellow skin": ["yellowish_skin", "jaundice"],
    "yellow eyes": ["yellowing_of_eyes", "jaundice"],
    "anxious": ["anxiety"],
    "depressed": ["depression"],
    "sad": ["depression"],
    "moody": ["mood_swings"],
    # Hindi / Hinglish Support
    "bukhaar": ["high_fever", "mild_fever"],
    "bukhar": ["high_fever", "mild_fever"],
    "बुखार": ["high_fever", "mild_fever"],
    "khansi": ["cough"],
    "खांसी": ["cough"],
    "dard": ["muscle_pain", "joint_pain"],
    "दर्द": ["muscle_pain", "joint_pain"],
    "sir dard": ["headache"],
    "सिर दर्द": ["headache"],
    "pet dard": ["stomach_pain", "abdominal_pain"],
    "पेट दर्द": ["stomach_pain", "abdominal_pain"],
    "thakan": ["fatigue"],
    "थकान": ["fatigue"],
    "khujli": ["itching"],
    "खुजली": ["itching"]
}

NEGATION_WORDS = {"no", "not", "don't", "dont", "never", "without", "hardly", "lack"}

import unicodedata

def clean_text(text: str) -> str:
    """Lowercase and remove punctuation except spaces/hyphens/apostrophes/Unicode letters & marks."""
    text = text.lower()
    
    # Use Unicode categories to keep letters (L), marks (M), and numbers (N)
    # This preserves Hindi matras (M) which isalnum() might skip
    chars = []
    for char in text:
        cat = unicodedata.category(char)
        if cat[0] in ('L', 'M', 'N') or char in (" ", "'", "-", "\n"):
            chars.append(char)
        else:
            chars.append(" ")
            
    text = "".join(chars)
    # Remove underscores specifically as they are used in internal keys
    text = text.replace('_', ' ')
    # Normalize multiple spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def is_negated(text: str, match_phrase: str, window: int = 4) -> bool:
    """Check if a matched phrase is negated by preceding words."""
    match_idx = text.find(match_phrase)
    if match_idx == -1: 
        return False
    
    # Extract the substring before the match
    prefix = text[:match_idx].strip()
    if not prefix: 
        return False
    
    # Look at the last 'window' words before the match
    preceding_words = prefix.split()[-window:]
    for word in preceding_words:
        if word in NEGATION_WORDS:
            return True
            
    return False

def extract_symptoms(text: str, all_symptoms: list) -> list:
    """
    Extract structured symptoms from free-form text.
    Returns a list of symptom names that match the dataset, ignoring negated symptoms.
    """
    if not text.strip():
        return []
    
    # 0. Translate if non-English
    text = translate_to_english(text)
    
    # If quota was exceeded, we can't extract symptoms reliably from non-English
    if text == "[[QUOTA_EXCEEDED]]":
        return []
    
    cleaned_input = clean_text(text)
    words = cleaned_input.split()
    
    matched_symptoms = set()
    
    # 1. Exact matches (multi-word like "chest pain")
    for symptom in all_symptoms:
        # e.g. "chest_pain" -> "chest pain"
        symptom_spaced = symptom.replace("_", " ")
        if symptom_spaced in cleaned_input:
            if not is_negated(cleaned_input, symptom_spaced):
                matched_symptoms.add(symptom)
            
    # 2. Synonym mapping
    for phrase, mapped_symptoms in SYNONYMS.items():
        if phrase in cleaned_input:
            if not is_negated(cleaned_input, phrase):
                for s in mapped_symptoms:
                    if s in all_symptoms:
                        matched_symptoms.add(s)
                    
    # 3. Single word aggressive matching (careful with false positives)
    # Only map specific strong single words if not already caught
    strong_keywords = {
        "fever": "high_fever",
        "headache": "headache",
        "cough": "cough",
        "nausea": "nausea",
        "vomit": "vomiting",
        "fatigue": "fatigue",
        "dizzy": "dizziness",
        "itch": "itching",
        "rash": "skin_rash",
        "sweat": "sweating",
        "diarrhea": "diarrhoea",
        "constipation": "constipation"
    }
    
    for i, word in enumerate(words):
        for kw, symp in strong_keywords.items():
            # If the user typed "headachey" we might catch it with startswith
            if word.startswith(kw) and symp in all_symptoms:
                start_window = max(0, i - 4)
                preceding = words[start_window:i]
                if not any(w in NEGATION_WORDS for w in preceding):
                    matched_symptoms.add(symp)
                
    return list(matched_symptoms)
