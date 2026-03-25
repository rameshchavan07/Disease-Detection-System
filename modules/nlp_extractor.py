"""
NLP Symptom Extractor
Maps free-form text input to the dataset's 382 structured symptoms.
Uses basic string matching, lemmatization simulation, and synonym mapping.
"""
import re

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
    "moody": ["mood_swings"]
}

def clean_text(text: str) -> str:
    """Lowercase and remove punctuation except spaces/hyphens."""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    return text

def extract_symptoms(text: str, all_symptoms: list) -> list:
    """
    Extract structured symptoms from free-form text.
    Returns a list of symptom names that match the dataset.
    """
    if not text.strip():
        return []
    
    cleaned_input = clean_text(text)
    words = cleaned_input.split()
    
    matched_symptoms = set()
    
    # 1. Exact matches (multi-word like "chest pain")
    for symptom in all_symptoms:
        # e.g. "chest_pain" -> "chest pain"
        symptom_spaced = symptom.replace("_", " ")
        if symptom_spaced in cleaned_input:
            matched_symptoms.add(symptom)
            
    # 2. Synonym mapping
    for phrase, mapped_symptoms in SYNONYMS.items():
        if phrase in cleaned_input:
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
    
    for word in words:
        for kw, symp in strong_keywords.items():
            # If the user typed "headachey" we might catch it with startswith
            if word.startswith(kw) and symp in all_symptoms:
                matched_symptoms.add(symp)
                
    return list(matched_symptoms)
