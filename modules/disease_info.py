"""
Disease Information Module
Provides descriptions, precautions, remedies, and severity data for diseases.
"""

# Severity classification for diseases
SEVERITY_MAP = {
    # Critical
    "Heart Attack": "critical", "Stroke": "critical", "Sepsis": "critical",
    "Pulmonary Embolism": "critical", "Meningitis": "critical", "Rabies": "critical",
    "Brain Tumor": "critical", "Subarachnoid Hemorrhage": "critical",
    "Peritonitis": "critical", "Aortic Aneurysm": "critical",
    "ALS": "critical", "Lung Cancer": "critical", "Liver Cancer": "critical",
    "Pancreatic Cancer": "critical", "Leukemia": "critical",
    "Hepatitis E": "critical", "AIDS": "critical",
    
    # High
    "Pneumonia": "high", "Tuberculosis": "high", "Dengue": "high", "Malaria": "high",
    "Typhoid": "high", "COVID-19": "high", "Heart Failure": "high", "COPD": "high",
    "Epilepsy": "high", "Cirrhosis": "high", "Kidney Cancer": "high",
    "Breast Cancer": "high", "Colorectal Cancer": "high", "Prostate Cancer": "high",
    "Lymphoma": "high", "Multiple Sclerosis": "high", "Lupus (SLE)": "high",
    "Chronic Kidney Disease": "high", "Appendicitis": "high",
    "Pyelonephritis": "high", "Endocarditis": "high", "Deep Vein Thrombosis": "high",
    "Pancreatitis": "high", "Hepatitis B": "high", "Hepatitis C": "high",
    "Parkinson Disease": "high", "Alzheimer Disease": "high",
    "Diabetes Type 1": "high", "Tetanus": "high", "Diphtheria": "high",
    "Sickle Cell Disease": "high", "Ovarian Cancer": "high",
    "Stomach Cancer": "high", "Esophageal Cancer": "high", "Bladder Cancer": "high",
    "Myeloma": "high", "Testicular Cancer": "high", "Cervical Cancer": "high",
    "Melanoma": "high", "Thyroid Cancer": "high", "Cystic Fibrosis": "high",
    
    # Moderate
    "Diabetes Type 2": "moderate", "Hypertension": "moderate",
    "Bronchial Asthma": "moderate", "Hepatitis A": "moderate",
    "Hepatitis D": "moderate", "Alcoholic Hepatitis": "moderate",
    "Jaundice": "moderate", "Chicken Pox": "moderate", "Measles": "moderate",
    "Influenza": "moderate", "Anemia": "moderate", "Hypothyroidism": "moderate",
    "Hyperthyroidism": "moderate", "Gout": "moderate",
    "Rheumatoid Arthritis": "moderate", "Crohn Disease": "moderate",
    "Ulcerative Colitis": "moderate", "Gallstones": "moderate",
    "Kidney Stones": "moderate", "Glaucoma": "moderate", "Sleep Apnea": "moderate",
    "Atrial Fibrillation": "moderate", "Angina": "moderate",
    "Peripheral Artery Disease": "moderate", "Celiac Disease": "moderate",
    "Cushing Syndrome": "moderate", "Addison Disease": "moderate",
    "Fibromyalgia": "moderate", "Osteoporosis": "moderate",
    "Scleroderma": "moderate", "Polycystic Ovary Syndrome": "moderate",
    "Endometriosis": "moderate", "Preeclampsia": "moderate",
    "Ankylosing Spondylitis": "moderate", "Psoriatic Arthritis": "moderate",
    "Temporal Arteritis": "moderate", "Pulmonary Hypertension": "moderate",
    
    # Low
    "Common Cold": "low", "Acne": "low", "Allergy": "low", "GERD": "low",
    "Migraine": "low", "Vertigo": "low", "Urinary Tract Infection": "low",
    "Gastroenteritis": "low", "Psoriasis": "low", "Impetigo": "low",
    "Fungal infection": "low", "Dimorphic Hemorrhoids": "low",
    "Drug Reaction": "low", "Varicose Veins": "low", "Cervical Spondylosis": "low",
    "Osteoarthritis": "low", "Arthritis": "low", "Hypoglycemia": "low",
    "Conjunctivitis": "low", "Tonsillitis": "low", "Bronchitis": "low",
    "Sinusitis": "low", "Eczema": "low", "Contact Dermatitis": "low",
    "Hives (Urticaria)": "low", "Warts": "low", "Ringworm": "low",
    "Irritable Bowel Syndrome": "low", "Lactose Intolerance": "low",
    "Hemorrhoids": "low", "Anal Fissure": "low", "Plantar Fasciitis": "low",
    "Carpal Tunnel Syndrome": "low", "Sciatica": "low", "BPH": "low",
    "Insomnia": "low", "Tinnitus": "low",
}

# Disease information database
DISEASE_INFO = {
    "Fungal infection": {
        "description": "A skin infection caused by fungi, leading to itching, rashes, and skin discoloration.",
        "causes": ["Poor hygiene", "Warm/moist environments", "Weakened immune system", "Shared clothing"],
        "precautions": ["Keep skin clean and dry", "Avoid sharing personal items", "Wear breathable fabrics", "Use antifungal powder in prone areas"],
        "home_remedies": ["Apply tea tree oil", "Use coconut oil on affected areas", "Turmeric paste application", "Apple cider vinegar rinse"]
    },
    "Common Cold": {
        "description": "A viral infection of the upper respiratory tract causing sneezing, congestion, and sore throat.",
        "causes": ["Rhinoviruses", "Close contact with infected persons", "Weakened immunity", "Cold weather exposure"],
        "precautions": ["Wash hands frequently", "Avoid close contact with sick people", "Don't touch face", "Boost immunity with proper nutrition"],
        "home_remedies": ["Warm salt water gargle", "Honey and ginger tea", "Steam inhalation", "Rest and hydration"]
    },
    "Diabetes Type 2": {
        "description": "A chronic metabolic disease where the body doesn't use insulin effectively, leading to high blood sugar levels.",
        "causes": ["Obesity", "Sedentary lifestyle", "Genetic factors", "Poor diet", "Insulin resistance"],
        "precautions": ["Monitor blood sugar regularly", "Follow prescribed medication", "Maintain healthy weight", "Regular exercise"],
        "home_remedies": ["Bitter gourd juice", "Fenugreek seeds soaked in water", "Cinnamon tea", "Regular walking after meals"]
    },
    "Hypertension": {
        "description": "Persistently elevated blood pressure that can damage blood vessels and organs over time.",
        "causes": ["High salt intake", "Obesity", "Stress", "Sedentary lifestyle", "Genetics", "Smoking"],
        "precautions": ["Reduce salt intake", "Exercise regularly", "Manage stress", "Limit alcohol", "Monitor BP regularly"],
        "home_remedies": ["Garlic consumption", "Hibiscus tea", "Deep breathing exercises", "Potassium-rich foods (bananas, spinach)"]
    },
    "Migraine": {
        "description": "A neurological condition causing intense, debilitating headaches often with nausea and light sensitivity.",
        "causes": ["Hormonal changes", "Stress", "Certain foods", "Sleep irregularities", "Sensory stimuli"],
        "precautions": ["Identify and avoid triggers", "Maintain regular sleep schedule", "Stay hydrated", "Manage stress levels"],
        "home_remedies": ["Peppermint oil on temples", "Cold compress", "Ginger tea", "Rest in dark quiet room"]
    },
    "Pneumonia": {
        "description": "An infection that inflames the air sacs in one or both lungs, which may fill with fluid.",
        "causes": ["Bacteria", "Viruses", "Fungi", "Weakened immune system", "Hospital-acquired infections"],
        "precautions": ["Get vaccinated", "Practice good hygiene", "Don't smoke", "Keep immune system strong"],
        "home_remedies": ["Warm liquids", "Rest", "Steam inhalation with eucalyptus", "Honey and turmeric milk"]
    },
    "Heart Attack": {
        "description": "A medical emergency where blood flow to the heart is suddenly blocked, causing tissue damage.",
        "causes": ["Coronary artery disease", "Blood clots", "High cholesterol", "Smoking", "Diabetes", "Obesity"],
        "precautions": ["Call emergency services immediately", "Take aspirin if advised", "Regular cardiac checkups", "Healthy lifestyle"],
        "home_remedies": ["THIS IS A MEDICAL EMERGENCY - Call 911/112 immediately", "Chew aspirin while waiting", "Stay calm and rest"]
    },
    "Malaria": {
        "description": "A mosquito-borne infectious disease causing fever, chills, and flu-like symptoms.",
        "causes": ["Plasmodium parasites", "Mosquito bites", "Contaminated blood transfusion"],
        "precautions": ["Use mosquito nets", "Apply insect repellent", "Wear long sleeves", "Take antimalarial drugs when traveling"],
        "home_remedies": ["Ginger and raisin tea", "Cinnamon water", "Citrus fruits for vitamin C", "Rest and hydration"]
    },
    "Dengue": {
        "description": "A viral infection spread by Aedes mosquitoes causing high fever, severe joint pain, and rash.",
        "causes": ["Dengue virus", "Aedes mosquito bites", "Travel to endemic areas"],
        "precautions": ["Prevent mosquito breeding", "Use repellents", "Wear protective clothing", "Keep surroundings clean"],
        "home_remedies": ["Papaya leaf juice", "Giloy juice", "Coconut water for hydration", "Rest and monitoring"]
    },
    "COVID-19": {
        "description": "A respiratory illness caused by SARS-CoV-2 virus with symptoms ranging from mild to severe.",
        "causes": ["SARS-CoV-2 virus", "Airborne transmission", "Close contact", "Surface contamination"],
        "precautions": ["Get vaccinated", "Wear masks", "Maintain social distance", "Wash hands frequently", "Ventilate indoor spaces"],
        "home_remedies": ["Steam inhalation", "Warm fluids", "Vitamin C and Zinc", "Rest and isolation", "Monitor oxygen levels"]
    },
}

# Disease to Specialty Mapping
SPECIALIST_MAP = {
    # Cardiology
    "Heart Attack": "Cardiologist", "Heart Failure": "Cardiologist", "Atrial Fibrillation": "Cardiologist",
    "Angina": "Cardiologist", "Peripheral Artery Disease": "Cardiologist", "Endocarditis": "Cardiologist",
    "Aortic Aneurysm": "Cardiologist",
    # Neurology
    "Stroke": "Neurologist", "Brain Tumor": "Neurologist", "Subarachnoid Hemorrhage": "Neurologist",
    "ALS": "Neurologist", "Epilepsy": "Neurologist", "Multiple Sclerosis": "Neurologist",
    "Parkinson Disease": "Neurologist", "Alzheimer Disease": "Neurologist", "Migraine": "Neurologist",
    "Vertigo": "Neurologist", "Sciatica": "Neurologist", "Tinnitus": "ENT Specialist",
    # Respiratory / Pulmonology
    "Pulmonary Embolism": "Pulmonologist", "Lung Cancer": "Pulmonologist", "Pneumonia": "Pulmonologist",
    "Tuberculosis": "Pulmonologist", "COPD": "Pulmonologist", "Bronchial Asthma": "Pulmonologist",
    "Pulmonary Hypertension": "Pulmonologist", "Bronchitis": "Pulmonologist",
    # Gastroenterology
    "Liver Cancer": "Gastroenterologist", "Pancreatic Cancer": "Gastroenterologist", "Cirrhosis": "Gastroenterologist",
    "Colorectal Cancer": "Gastroenterologist", "Appendicitis": "Gastroenterologist", "Pancreatitis": "Gastroenterologist",
    "Hepatitis A": "Gastroenterologist", "Hepatitis B": "Gastroenterologist", "Hepatitis C": "Gastroenterologist",
    "Hepatitis D": "Gastroenterologist", "Hepatitis E": "Gastroenterologist", "Alcoholic Hepatitis": "Gastroenterologist",
    "Jaundice": "Gastroenterologist", "Crohn Disease": "Gastroenterologist", "Ulcerative Colitis": "Gastroenterologist",
    "Gallstones": "Gastroenterologist", "Celiac Disease": "Gastroenterologist", "GERD": "Gastroenterologist",
    "Gastroenteritis": "Gastroenterologist", "Irritable Bowel Syndrome": "Gastroenterologist",
    "Lactose Intolerance": "Gastroenterologist", "Hemorrhoids": "Proctologist", "Anal Fissure": "Proctologist",
    "Dimorphic Hemorrhoids": "Proctologist", "Stomach Cancer": "Gastroenterologist", "Esophageal Cancer": "Gastroenterologist",
    "Peritonitis": "Gastroenterologist",
    # Nephrology / Urology
    "Kidney Cancer": "Nephrologist", "Chronic Kidney Disease": "Nephrologist", "Pyelonephritis": "Nephrologist",
    "Kidney Stones": "Urologist", "Prostate Cancer": "Urologist", "Bladder Cancer": "Urologist",
    "Testicular Cancer": "Urologist", "Urinary Tract Infection": "Urologist", "BPH": "Urologist",
    # Oncology (General)
    "Leukemia": "Oncologist", "Breast Cancer": "Oncologist", "Lymphoma": "Oncologist",
    "Ovarian Cancer": "Oncologist", "Cervical Cancer": "Oncologist", "Melanoma": "Dermatologist",
    "Thyroid Cancer": "Endocrinologist", "Myeloma": "Oncologist",
    # Rheumatology / Immunology
    "Lupus (SLE)": "Rheumatologist", "Gout": "Rheumatologist", "Rheumatoid Arthritis": "Rheumatologist",
    "Fibromyalgia": "Rheumatologist", "Scleroderma": "Rheumatologist", "Ankylosing Spondylitis": "Rheumatologist",
    "Psoriatic Arthritis": "Rheumatologist", "Temporal Arteritis": "Rheumatologist", "Osteoarthritis": "Rheumatologist",
    "Arthritis": "Rheumatologist", "Allergy": "Allergist",
    # Endocrinology
    "Diabetes Type 1": "Endocrinologist", "Diabetes Type 2": "Endocrinologist", "Hypothyroidism": "Endocrinologist",
    "Hyperthyroidism": "Endocrinologist", "Cushing Syndrome": "Endocrinologist", "Addison Disease": "Endocrinologist",
    "Polycystic Ovary Syndrome": "Gynecologist", "Hypoglycemia": "Endocrinologist",
    # Dermatology
    "Acne": "Dermatologist", "Psoriasis": "Dermatologist", "Impetigo": "Dermatologist",
    "Fungal infection": "Dermatologist", "Eczema": "Dermatologist", "Contact Dermatitis": "Dermatologist",
    "Hives (Urticaria)": "Dermatologist", "Warts": "Dermatologist", "Ringworm": "Dermatologist",
    # Infectious Disease
    "Sepsis": "Infectious Disease Specialist", "Meningitis": "Infectious Disease Specialist", "Rabies": "Infectious Disease Specialist",
    "Dengue": "Infectious Disease Specialist", "Malaria": "Infectious Disease Specialist", "Typhoid": "General Physician",
    "COVID-19": "General Physician", "Tetanus": "Infectious Disease Specialist", "Diphtheria": "Infectious Disease Specialist",
    "Chicken Pox": "General Physician", "Measles": "Pediatrician", "Influenza": "General Physician",
    "Common Cold": "General Physician", "Drug Reaction": "Allergist",
    # Orthopedics / Musculoskeletal
    "Osteoporosis": "Orthopedist", "Cervical Spondylosis": "Orthopedist", "Plantar Fasciitis": "Podiatrist",
    "Carpal Tunnel Syndrome": "Orthopedist",
    # Gynecology / Obstetrics
    "Endometriosis": "Gynecologist", "Preeclampsia": "Obstetrician",
    # Hematology
    "Sickle Cell Disease": "Hematologist", "Anemia": "Hematologist",
    # Ophthalmology
    "Glaucoma": "Ophthalmologist", "Conjunctivitis": "Ophthalmologist",
    # ENT (Otolaryngology)
    "Sleep Apnea": "ENT / Pulmonologist", "Tonsillitis": "ENT Specialist", "Sinusitis": "ENT Specialist",
    # Vascular Surgery
    "Deep Vein Thrombosis": "Vascular Surgeon", "Varicose Veins": "Vascular Surgeon",
    # General
    "Cystic Fibrosis": "Pulmonologist", "Insomnia": "Psychiatrist"
}

def get_disease_info(disease_name: str) -> dict:
    """Get information for a specific disease."""
    info = DISEASE_INFO.get(disease_name, {})
    severity = SEVERITY_MAP.get(disease_name, "moderate")
    
    if not info:
        # Generate generic info for diseases not in the detailed database
        info = {
            "description": f"{disease_name} is a medical condition that requires proper diagnosis and treatment.",
            "causes": ["Multiple factors may contribute", "Consult a healthcare provider for specific causes"],
            "precautions": ["Consult a healthcare professional", "Follow prescribed treatment", "Maintain healthy lifestyle", "Get regular checkups"],
            "home_remedies": ["Stay hydrated", "Get adequate rest", "Eat nutritious food", "Follow medical advice"]
        }
    
    info["severity"] = severity
    info["consult_doctor"] = severity in ("high", "critical")
    info["specialist"] = SPECIALIST_MAP.get(disease_name, "General Physician")
    return info

def get_severity_display(severity: str) -> dict:
    """Get display properties for a severity level."""
    display_map = {
        "low": {"label": "Low Risk", "color": "#4CAF50", "icon": "🟢", "bg": "rgba(76,175,80,0.1)"},
        "moderate": {"label": "Moderate Risk", "color": "#FF9800", "icon": "🟡", "bg": "rgba(255,152,0,0.1)"},
        "high": {"label": "High Risk", "color": "#F44336", "icon": "🔴", "bg": "rgba(244,67,54,0.1)"},
        "critical": {"label": "Critical", "color": "#B71C1C", "icon": "🚨", "bg": "rgba(183,28,28,0.15)"},
    }
    return display_map.get(severity, display_map["moderate"])
