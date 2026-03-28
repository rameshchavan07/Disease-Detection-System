import re
import os
from functools import lru_cache
from google import genai
from config.settings import GEMINI_API_KEY
from modules.logger import get_logger

logger = get_logger("nlp_extractor")

@lru_cache(maxsize=128)
def translate_to_english(text: str) -> str:
    """Uses Gemini to translate medical symptoms into clinical English."""
    if not GEMINI_API_KEY:
        logger.warning("GEMINI_API_KEY is missing. Skipping translation.")
        return text
    
    try:
        # 1. Initialize modern client
        client = genai.Client(api_key=GEMINI_API_KEY)
        
        prompt = f"Translate the following medical symptoms/description to concise clinical English. If it is already in English, return it exactly as it is. Output only the English translation: \"{text}\""
        
        # 2. Modern generation call
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt
        )
        
        translated_text = response.text.strip()
        return translated_text if translated_text else text
        
    except Exception as e:
        # Check for Quota Exceeded (429) in the error string or status
        error_msg = str(e).lower()
        if "429" in error_msg or "quota" in error_msg or "resource_exhausted" in error_msg:
            logger.warning(f"Gemini Quota Exceeded (429): {e}")
            return "[[QUOTA_EXCEEDED]]"
        
        logger.error(f"Gemini Translation Error: {e}")
        # Fallback to original text if API fails
        return text

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
