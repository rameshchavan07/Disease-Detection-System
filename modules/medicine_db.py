"""
Medicine Database Module for MedDetect AI
Curated database of common medicines with dosage, side effects,
contraindications, and fuzzy search for real-time suggestions.
"""

# ─────────────────────────────────────────────────────────────
# Master Medicine Database
# ─────────────────────────────────────────────────────────────

MEDICINES = [
    # ── Analgesics / Antipyretics ──
    {
        "name": "Paracetamol",
        "generic_name": "Acetaminophen",
        "category": "Analgesic / Antipyretic",
        "form": "Tablet 500mg",
        "common_dosage": "1-2 tablets every 4-6 hours",
        "max_daily": "4g (8 tablets of 500mg)",
        "side_effects": ["Nausea", "Allergic rash", "Liver damage (overdose)", "Low blood platelets"],
        "contraindications": ["Severe liver disease", "Chronic alcohol use"],
        "interactions": ["Warfarin", "Isoniazid", "Carbamazepine"],
    },
    {
        "name": "Ibuprofen",
        "generic_name": "Ibuprofen",
        "category": "NSAID / Anti-inflammatory",
        "form": "Tablet 400mg",
        "common_dosage": "1 tablet every 6-8 hours with food",
        "max_daily": "1200mg (3 tablets)",
        "side_effects": ["Stomach pain", "Heartburn", "Dizziness", "GI bleeding (prolonged use)"],
        "contraindications": ["Peptic ulcer", "Renal impairment", "Third trimester pregnancy"],
        "interactions": ["Aspirin", "Warfarin", "ACE inhibitors", "Lithium"],
    },
    {
        "name": "Aspirin",
        "generic_name": "Acetylsalicylic Acid",
        "category": "NSAID / Antiplatelet",
        "form": "Tablet 75mg / 325mg",
        "common_dosage": "75-325mg once daily",
        "max_daily": "4g (anti-inflammatory); 325mg (cardioprotective)",
        "side_effects": ["GI irritation", "Tinnitus", "Bruising", "Reye's syndrome (children)"],
        "contraindications": ["Peptic ulcer", "Bleeding disorders", "Children under 16"],
        "interactions": ["Warfarin", "Methotrexate", "Ibuprofen"],
    },
    {
        "name": "Diclofenac",
        "generic_name": "Diclofenac Sodium",
        "category": "NSAID / Anti-inflammatory",
        "form": "Tablet 50mg",
        "common_dosage": "1 tablet 2-3 times daily with food",
        "max_daily": "150mg",
        "side_effects": ["Stomach upset", "Headache", "Dizziness", "Elevated liver enzymes"],
        "contraindications": ["Heart failure", "Peptic ulcer", "Severe hepatic impairment"],
        "interactions": ["Lithium", "Digoxin", "Methotrexate", "Cyclosporine"],
    },
    {
        "name": "Naproxen",
        "generic_name": "Naproxen Sodium",
        "category": "NSAID / Anti-inflammatory",
        "form": "Tablet 250mg / 500mg",
        "common_dosage": "250-500mg twice daily",
        "max_daily": "1250mg (first day), then 1000mg",
        "side_effects": ["Stomach upset", "Drowsiness", "Headache", "Edema"],
        "contraindications": ["Peptic ulcer", "Severe renal impairment", "Late pregnancy"],
        "interactions": ["Warfarin", "ACE inhibitors", "Lithium"],
    },

    # ── Antibiotics ──
    {
        "name": "Amoxicillin",
        "generic_name": "Amoxicillin Trihydrate",
        "category": "Antibiotic (Penicillin)",
        "form": "Capsule 500mg",
        "common_dosage": "1 capsule every 8 hours",
        "max_daily": "3g (severe infections)",
        "side_effects": ["Diarrhea", "Nausea", "Skin rash", "Allergic reaction"],
        "contraindications": ["Penicillin allergy", "Infectious mononucleosis"],
        "interactions": ["Methotrexate", "Warfarin", "Oral contraceptives"],
    },
    {
        "name": "Azithromycin",
        "generic_name": "Azithromycin Dihydrate",
        "category": "Antibiotic (Macrolide)",
        "form": "Tablet 250mg / 500mg",
        "common_dosage": "500mg on day 1, then 250mg daily for 4 days",
        "max_daily": "500mg",
        "side_effects": ["Nausea", "Diarrhea", "Abdominal pain", "QT prolongation (rare)"],
        "contraindications": ["Macrolide allergy", "Severe hepatic impairment"],
        "interactions": ["Warfarin", "Antacids", "Ergotamine"],
    },
    {
        "name": "Ciprofloxacin",
        "generic_name": "Ciprofloxacin Hydrochloride",
        "category": "Antibiotic (Fluoroquinolone)",
        "form": "Tablet 500mg",
        "common_dosage": "250-500mg twice daily",
        "max_daily": "1500mg",
        "side_effects": ["Nausea", "Diarrhea", "Tendon rupture (rare)", "Photosensitivity"],
        "contraindications": ["Pregnancy", "Children under 18", "Tendon disorders"],
        "interactions": ["Theophylline", "Warfarin", "Antacids", "NSAIDs"],
    },
    {
        "name": "Metronidazole",
        "generic_name": "Metronidazole",
        "category": "Antibiotic / Antiprotozoal",
        "form": "Tablet 400mg",
        "common_dosage": "400mg three times daily",
        "max_daily": "2400mg",
        "side_effects": ["Metallic taste", "Nausea", "Headache", "Dark urine"],
        "contraindications": ["First trimester pregnancy", "Alcohol use"],
        "interactions": ["Alcohol (disulfiram reaction)", "Warfarin", "Lithium"],
    },
    {
        "name": "Doxycycline",
        "generic_name": "Doxycycline Hyclate",
        "category": "Antibiotic (Tetracycline)",
        "form": "Capsule 100mg",
        "common_dosage": "100mg twice daily on day 1, then 100mg daily",
        "max_daily": "200mg",
        "side_effects": ["Photosensitivity", "Nausea", "Esophageal irritation", "Tooth discoloration (children)"],
        "contraindications": ["Pregnancy", "Children under 8", "Severe hepatic disease"],
        "interactions": ["Antacids", "Iron supplements", "Warfarin", "Oral contraceptives"],
    },
    {
        "name": "Cephalexin",
        "generic_name": "Cephalexin Monohydrate",
        "category": "Antibiotic (Cephalosporin)",
        "form": "Capsule 500mg",
        "common_dosage": "250-500mg every 6 hours",
        "max_daily": "4g",
        "side_effects": ["Diarrhea", "Nausea", "Rash", "Vaginal candidiasis"],
        "contraindications": ["Cephalosporin allergy", "Severe penicillin allergy (cross-reactivity)"],
        "interactions": ["Metformin", "Probenecid"],
    },

    # ── Gastrointestinal ──
    {
        "name": "Omeprazole",
        "generic_name": "Omeprazole",
        "category": "Proton Pump Inhibitor (PPI)",
        "form": "Capsule 20mg",
        "common_dosage": "20mg once daily before breakfast",
        "max_daily": "40mg",
        "side_effects": ["Headache", "Nausea", "Diarrhea", "Vitamin B12 deficiency (long-term)"],
        "contraindications": ["Hypersensitivity to PPIs"],
        "interactions": ["Clopidogrel", "Methotrexate", "Ketoconazole"],
    },
    {
        "name": "Pantoprazole",
        "generic_name": "Pantoprazole Sodium",
        "category": "Proton Pump Inhibitor (PPI)",
        "form": "Tablet 40mg",
        "common_dosage": "40mg once daily before breakfast",
        "max_daily": "80mg",
        "side_effects": ["Headache", "Diarrhea", "Flatulence", "Joint pain"],
        "contraindications": ["PPI hypersensitivity"],
        "interactions": ["Methotrexate", "Warfarin"],
    },
    {
        "name": "Ranitidine",
        "generic_name": "Ranitidine Hydrochloride",
        "category": "H2 Receptor Antagonist",
        "form": "Tablet 150mg",
        "common_dosage": "150mg twice daily or 300mg at bedtime",
        "max_daily": "300mg",
        "side_effects": ["Headache", "Dizziness", "Constipation", "Diarrhea"],
        "contraindications": ["Porphyria"],
        "interactions": ["Ketoconazole", "Atazanavir", "Gefitinib"],
    },
    {
        "name": "Domperidone",
        "generic_name": "Domperidone Maleate",
        "category": "Antiemetic / Prokinetic",
        "form": "Tablet 10mg",
        "common_dosage": "10mg three times daily before meals",
        "max_daily": "30mg",
        "side_effects": ["Dry mouth", "Headache", "QT prolongation (rare)", "Galactorrhea"],
        "contraindications": ["Prolactinoma", "GI hemorrhage", "Cardiac conditions"],
        "interactions": ["Ketoconazole", "Erythromycin", "Fluconazole"],
    },
    {
        "name": "Ondansetron",
        "generic_name": "Ondansetron Hydrochloride",
        "category": "Antiemetic (5-HT3 Antagonist)",
        "form": "Tablet 4mg / 8mg",
        "common_dosage": "4-8mg every 8 hours as needed",
        "max_daily": "24mg",
        "side_effects": ["Headache", "Constipation", "Dizziness", "QT prolongation"],
        "contraindications": ["Congenital long QT syndrome"],
        "interactions": ["Apomorphine", "Tramadol", "SSRIs"],
    },
    {
        "name": "Loperamide",
        "generic_name": "Loperamide Hydrochloride",
        "category": "Antidiarrheal",
        "form": "Capsule 2mg",
        "common_dosage": "4mg initially, then 2mg after each loose stool",
        "max_daily": "16mg",
        "side_effects": ["Constipation", "Abdominal cramps", "Dizziness", "Nausea"],
        "contraindications": ["Bloody diarrhea", "Bacterial enterocolitis", "Children under 2"],
        "interactions": ["Ritonavir", "Itraconazole"],
    },

    # ── Cardiovascular ──
    {
        "name": "Amlodipine",
        "generic_name": "Amlodipine Besylate",
        "category": "Calcium Channel Blocker",
        "form": "Tablet 5mg / 10mg",
        "common_dosage": "5mg once daily",
        "max_daily": "10mg",
        "side_effects": ["Ankle edema", "Flushing", "Headache", "Dizziness"],
        "contraindications": ["Severe aortic stenosis", "Cardiogenic shock"],
        "interactions": ["Simvastatin", "Cyclosporine", "CYP3A4 inhibitors"],
    },
    {
        "name": "Atenolol",
        "generic_name": "Atenolol",
        "category": "Beta-Blocker",
        "form": "Tablet 50mg",
        "common_dosage": "25-50mg once daily",
        "max_daily": "100mg",
        "side_effects": ["Fatigue", "Cold extremities", "Bradycardia", "Dizziness"],
        "contraindications": ["Severe bradycardia", "Heart block", "Uncontrolled heart failure"],
        "interactions": ["Verapamil", "Clonidine", "NSAIDs"],
    },
    {
        "name": "Losartan",
        "generic_name": "Losartan Potassium",
        "category": "ARB (Angiotensin Receptor Blocker)",
        "form": "Tablet 50mg",
        "common_dosage": "50mg once daily",
        "max_daily": "100mg",
        "side_effects": ["Dizziness", "Hyperkalemia", "Fatigue", "Hypotension"],
        "contraindications": ["Pregnancy", "Bilateral renal artery stenosis"],
        "interactions": ["Potassium supplements", "NSAIDs", "Lithium"],
    },
    {
        "name": "Enalapril",
        "generic_name": "Enalapril Maleate",
        "category": "ACE Inhibitor",
        "form": "Tablet 5mg / 10mg",
        "common_dosage": "5-10mg once daily",
        "max_daily": "40mg",
        "side_effects": ["Dry cough", "Dizziness", "Hyperkalemia", "Angioedema (rare)"],
        "contraindications": ["Pregnancy", "Angioedema history", "Bilateral renal artery stenosis"],
        "interactions": ["Potassium-sparing diuretics", "NSAIDs", "Lithium"],
    },
    {
        "name": "Hydrochlorothiazide",
        "generic_name": "Hydrochlorothiazide",
        "category": "Thiazide Diuretic",
        "form": "Tablet 12.5mg / 25mg",
        "common_dosage": "12.5-25mg once daily",
        "max_daily": "50mg",
        "side_effects": ["Hypokalemia", "Dizziness", "Hyperuricemia", "Photosensitivity"],
        "contraindications": ["Anuria", "Severe renal impairment", "Hypokalemia"],
        "interactions": ["Lithium", "Digoxin", "NSAIDs", "Corticosteroids"],
    },
    {
        "name": "Atorvastatin",
        "generic_name": "Atorvastatin Calcium",
        "category": "Statin (HMG-CoA Reductase Inhibitor)",
        "form": "Tablet 10mg / 20mg",
        "common_dosage": "10-20mg once daily at bedtime",
        "max_daily": "80mg",
        "side_effects": ["Muscle pain", "Headache", "Nausea", "Elevated liver enzymes"],
        "contraindications": ["Active liver disease", "Pregnancy", "Breastfeeding"],
        "interactions": ["Cyclosporine", "Gemfibrozil", "Grapefruit juice", "Erythromycin"],
    },
    {
        "name": "Clopidogrel",
        "generic_name": "Clopidogrel Bisulfate",
        "category": "Antiplatelet Agent",
        "form": "Tablet 75mg",
        "common_dosage": "75mg once daily",
        "max_daily": "75mg (maintenance)",
        "side_effects": ["Bleeding", "Bruising", "Diarrhea", "Rash"],
        "contraindications": ["Active bleeding", "Severe hepatic impairment"],
        "interactions": ["Omeprazole", "Aspirin", "Warfarin", "NSAIDs"],
    },

    # ── Antidiabetic ──
    {
        "name": "Metformin",
        "generic_name": "Metformin Hydrochloride",
        "category": "Antidiabetic (Biguanide)",
        "form": "Tablet 500mg / 850mg",
        "common_dosage": "500mg twice daily with meals",
        "max_daily": "2550mg",
        "side_effects": ["Nausea", "Diarrhea", "Metallic taste", "Lactic acidosis (rare)"],
        "contraindications": ["Renal impairment (eGFR <30)", "Metabolic acidosis", "Severe infection"],
        "interactions": ["Alcohol", "Contrast dyes", "Cimetidine"],
    },
    {
        "name": "Glimepiride",
        "generic_name": "Glimepiride",
        "category": "Antidiabetic (Sulfonylurea)",
        "form": "Tablet 1mg / 2mg",
        "common_dosage": "1-2mg once daily with breakfast",
        "max_daily": "8mg",
        "side_effects": ["Hypoglycemia", "Weight gain", "Nausea", "Dizziness"],
        "contraindications": ["Type 1 diabetes", "Diabetic ketoacidosis", "Severe hepatic impairment"],
        "interactions": ["Fluconazole", "Beta-blockers", "ACE inhibitors"],
    },

    # ── Respiratory ──
    {
        "name": "Salbutamol",
        "generic_name": "Salbutamol Sulfate",
        "category": "Bronchodilator (Beta-2 Agonist)",
        "form": "Inhaler 100mcg/puff",
        "common_dosage": "1-2 puffs every 4-6 hours as needed",
        "max_daily": "8 puffs",
        "side_effects": ["Tremor", "Palpitations", "Headache", "Muscle cramps"],
        "contraindications": ["Hypersensitivity to salbutamol"],
        "interactions": ["Beta-blockers", "Digoxin", "MAO inhibitors"],
    },
    {
        "name": "Montelukast",
        "generic_name": "Montelukast Sodium",
        "category": "Leukotriene Receptor Antagonist",
        "form": "Tablet 10mg",
        "common_dosage": "10mg once daily in the evening",
        "max_daily": "10mg",
        "side_effects": ["Headache", "Abdominal pain", "Mood changes", "Dizziness"],
        "contraindications": ["Hypersensitivity", "Phenylketonuria (chewable form)"],
        "interactions": ["Phenobarbital", "Rifampicin"],
    },
    {
        "name": "Cetirizine",
        "generic_name": "Cetirizine Hydrochloride",
        "category": "Antihistamine (2nd Generation)",
        "form": "Tablet 10mg",
        "common_dosage": "10mg once daily",
        "max_daily": "10mg",
        "side_effects": ["Drowsiness", "Dry mouth", "Headache", "Fatigue"],
        "contraindications": ["Severe renal impairment", "Hypersensitivity"],
        "interactions": ["CNS depressants", "Alcohol", "Theophylline"],
    },
    {
        "name": "Levocetirizine",
        "generic_name": "Levocetirizine Dihydrochloride",
        "category": "Antihistamine (3rd Generation)",
        "form": "Tablet 5mg",
        "common_dosage": "5mg once daily in the evening",
        "max_daily": "5mg",
        "side_effects": ["Drowsiness", "Dry mouth", "Fatigue", "Headache"],
        "contraindications": ["End-stage renal disease", "Hypersensitivity"],
        "interactions": ["CNS depressants", "Alcohol"],
    },
    {
        "name": "Fexofenadine",
        "generic_name": "Fexofenadine Hydrochloride",
        "category": "Antihistamine (Non-Sedating)",
        "form": "Tablet 120mg / 180mg",
        "common_dosage": "120-180mg once daily",
        "max_daily": "180mg",
        "side_effects": ["Headache", "Nausea", "Dizziness", "Drowsiness (rare)"],
        "contraindications": ["Hypersensitivity"],
        "interactions": ["Antacids (aluminium/magnesium)", "Ketoconazole", "Erythromycin"],
    },

    # ── Corticosteroids ──
    {
        "name": "Prednisolone",
        "generic_name": "Prednisolone",
        "category": "Corticosteroid",
        "form": "Tablet 5mg / 10mg",
        "common_dosage": "5-60mg daily (condition-dependent)",
        "max_daily": "60mg (acute); taper required",
        "side_effects": ["Weight gain", "Insomnia", "Mood changes", "Elevated blood sugar", "Osteoporosis (long-term)"],
        "contraindications": ["Systemic fungal infections", "Live vaccines during high-dose therapy"],
        "interactions": ["NSAIDs", "Warfarin", "Antidiabetic drugs", "CYP3A4 inducers"],
    },
    {
        "name": "Dexamethasone",
        "generic_name": "Dexamethasone",
        "category": "Corticosteroid",
        "form": "Tablet 0.5mg / 4mg",
        "common_dosage": "0.5-10mg daily (condition-dependent)",
        "max_daily": "Varies by indication",
        "side_effects": ["Insomnia", "Increased appetite", "Mood swings", "Hyperglycemia"],
        "contraindications": ["Systemic fungal infections", "Cerebral malaria"],
        "interactions": ["Phenytoin", "Rifampicin", "NSAIDs", "Warfarin"],
    },

    # ── CNS / Neurological ──
    {
        "name": "Tramadol",
        "generic_name": "Tramadol Hydrochloride",
        "category": "Opioid Analgesic",
        "form": "Capsule 50mg",
        "common_dosage": "50-100mg every 4-6 hours",
        "max_daily": "400mg",
        "side_effects": ["Nausea", "Dizziness", "Constipation", "Seizures (high dose)"],
        "contraindications": ["Uncontrolled epilepsy", "MAO inhibitor use", "Severe respiratory depression"],
        "interactions": ["SSRIs", "MAO inhibitors", "Carbamazepine", "Warfarin"],
    },
    {
        "name": "Gabapentin",
        "generic_name": "Gabapentin",
        "category": "Anticonvulsant / Neuropathic Pain",
        "form": "Capsule 300mg",
        "common_dosage": "300mg three times daily",
        "max_daily": "3600mg",
        "side_effects": ["Drowsiness", "Dizziness", "Ataxia", "Peripheral edema"],
        "contraindications": ["Hypersensitivity"],
        "interactions": ["Opioids", "Antacids", "CNS depressants"],
    },
    {
        "name": "Amitriptyline",
        "generic_name": "Amitriptyline Hydrochloride",
        "category": "Tricyclic Antidepressant",
        "form": "Tablet 10mg / 25mg",
        "common_dosage": "10-25mg at bedtime",
        "max_daily": "150mg",
        "side_effects": ["Drowsiness", "Dry mouth", "Constipation", "Weight gain", "Blurred vision"],
        "contraindications": ["Recent MI", "MAO inhibitor use", "Heart block"],
        "interactions": ["MAO inhibitors", "SSRIs", "Alcohol", "Anticholinergics"],
    },

    # ── Antifungal ──
    {
        "name": "Fluconazole",
        "generic_name": "Fluconazole",
        "category": "Antifungal (Azole)",
        "form": "Capsule 150mg",
        "common_dosage": "150mg single dose (vaginal candidiasis); 50-200mg daily (systemic)",
        "max_daily": "400mg",
        "side_effects": ["Nausea", "Headache", "Abdominal pain", "Elevated liver enzymes"],
        "contraindications": ["Co-administration with terfenadine/cisapride", "Severe hepatic impairment"],
        "interactions": ["Warfarin", "Phenytoin", "Cyclosporine", "Statins"],
    },

    # ── Vitamins / Supplements ──
    {
        "name": "Vitamin D3",
        "generic_name": "Cholecalciferol",
        "category": "Vitamin Supplement",
        "form": "Tablet 1000 IU / 60000 IU",
        "common_dosage": "1000 IU daily or 60000 IU weekly",
        "max_daily": "4000 IU (maintenance); higher under supervision",
        "side_effects": ["Hypercalcemia (overdose)", "Nausea", "Constipation"],
        "contraindications": ["Hypercalcemia", "Vitamin D toxicity"],
        "interactions": ["Thiazide diuretics", "Corticosteroids", "Orlistat"],
    },
    {
        "name": "Vitamin B12",
        "generic_name": "Methylcobalamin",
        "category": "Vitamin Supplement",
        "form": "Tablet 1500mcg",
        "common_dosage": "1500mcg once daily",
        "max_daily": "1500mcg (oral)",
        "side_effects": ["Mild diarrhea", "Itching", "Headache (rare)"],
        "contraindications": ["Hypersensitivity to cobalt or cobalamin"],
        "interactions": ["Metformin", "PPIs", "Colchicine"],
    },
    {
        "name": "Iron (Ferrous Sulfate)",
        "generic_name": "Ferrous Sulfate",
        "category": "Iron Supplement",
        "form": "Tablet 325mg (65mg elemental iron)",
        "common_dosage": "325mg 1-3 times daily on empty stomach",
        "max_daily": "975mg",
        "side_effects": ["Constipation", "Nausea", "Dark stools", "Stomach cramps"],
        "contraindications": ["Hemochromatosis", "Hemolytic anemia", "Peptic ulcer"],
        "interactions": ["Antacids", "Tetracyclines", "Fluoroquinolones", "Levodopa"],
    },
    {
        "name": "Calcium + Vitamin D",
        "generic_name": "Calcium Carbonate + Cholecalciferol",
        "category": "Bone Health Supplement",
        "form": "Tablet 500mg/250 IU",
        "common_dosage": "1 tablet twice daily with meals",
        "max_daily": "2 tablets",
        "side_effects": ["Constipation", "Bloating", "Hypercalcemia (overdose)"],
        "contraindications": ["Hypercalcemia", "Severe renal impairment", "Kidney stones"],
        "interactions": ["Tetracyclines", "Bisphosphonates", "Thyroid hormones"],
    },

    # ── Muscle Relaxants ──
    {
        "name": "Cyclobenzaprine",
        "generic_name": "Cyclobenzaprine Hydrochloride",
        "category": "Muscle Relaxant",
        "form": "Tablet 5mg / 10mg",
        "common_dosage": "5-10mg three times daily",
        "max_daily": "30mg",
        "side_effects": ["Drowsiness", "Dry mouth", "Dizziness", "Fatigue"],
        "contraindications": ["Hyperthyroidism", "Heart failure", "MAO inhibitor use"],
        "interactions": ["MAO inhibitors", "CNS depressants", "Tramadol"],
    },
    {
        "name": "Tizanidine",
        "generic_name": "Tizanidine Hydrochloride",
        "category": "Muscle Relaxant (Central-acting)",
        "form": "Tablet 2mg / 4mg",
        "common_dosage": "2-4mg every 6-8 hours",
        "max_daily": "36mg",
        "side_effects": ["Drowsiness", "Dry mouth", "Dizziness", "Hypotension"],
        "contraindications": ["Co-administration with ciprofloxacin or fluvoxamine"],
        "interactions": ["CYP1A2 inhibitors", "Antihypertensives", "CNS depressants"],
    },

    # ── Antianxiety ──
    {
        "name": "Alprazolam",
        "generic_name": "Alprazolam",
        "category": "Benzodiazepine (Anxiolytic)",
        "form": "Tablet 0.25mg / 0.5mg",
        "common_dosage": "0.25-0.5mg three times daily",
        "max_daily": "4mg",
        "side_effects": ["Drowsiness", "Memory impairment", "Dependence", "Ataxia"],
        "contraindications": ["Severe respiratory insufficiency", "Sleep apnea", "Myasthenia gravis"],
        "interactions": ["Ketoconazole", "Opioids", "Alcohol", "CYP3A4 inhibitors"],
    },

    # ── Antispasmodic ──
    {
        "name": "Hyoscine Butylbromide",
        "generic_name": "Scopolamine Butylbromide",
        "category": "Antispasmodic",
        "form": "Tablet 10mg",
        "common_dosage": "10-20mg three times daily",
        "max_daily": "60mg",
        "side_effects": ["Dry mouth", "Tachycardia", "Blurred vision", "Constipation"],
        "contraindications": ["Glaucoma", "Myasthenia gravis", "Megacolon"],
        "interactions": ["Other anticholinergics", "Metoclopramide", "Dopamine antagonists"],
    },
    {
        "name": "Mefenamic Acid",
        "generic_name": "Mefenamic Acid",
        "category": "NSAID / Analgesic",
        "form": "Capsule 250mg / 500mg",
        "common_dosage": "500mg three times daily after meals",
        "max_daily": "1500mg",
        "side_effects": ["Stomach pain", "Diarrhea", "Nausea", "Dizziness"],
        "contraindications": ["Peptic ulcer", "Inflammatory bowel disease", "Renal impairment"],
        "interactions": ["Warfarin", "Lithium", "ACE inhibitors", "Methotrexate"],
    },

    # ── Dermatology ──
    {
        "name": "Clotrimazole",
        "generic_name": "Clotrimazole",
        "category": "Antifungal (Topical)",
        "form": "Cream 1%",
        "common_dosage": "Apply thin layer 2-3 times daily",
        "max_daily": "N/A (topical)",
        "side_effects": ["Local irritation", "Burning sensation", "Erythema"],
        "contraindications": ["Hypersensitivity to imidazoles"],
        "interactions": ["Topical corticosteroids (may mask infection)"],
    },
    {
        "name": "Betamethasone Cream",
        "generic_name": "Betamethasone Valerate",
        "category": "Topical Corticosteroid",
        "form": "Cream 0.1%",
        "common_dosage": "Apply thin layer 1-2 times daily",
        "max_daily": "N/A (topical, limit to 2 weeks)",
        "side_effects": ["Skin thinning", "Stretch marks", "Burning", "Acne"],
        "contraindications": ["Viral skin infections", "Rosacea", "Perioral dermatitis"],
        "interactions": ["Other topical preparations (apply separately)"],
    },

    # ── Thyroid ──
    {
        "name": "Levothyroxine",
        "generic_name": "Levothyroxine Sodium",
        "category": "Thyroid Hormone",
        "form": "Tablet 25mcg / 50mcg / 100mcg",
        "common_dosage": "25-100mcg once daily on empty stomach",
        "max_daily": "200mcg (individualized)",
        "side_effects": ["Palpitations", "Weight loss", "Tremor", "Insomnia"],
        "contraindications": ["Untreated adrenal insufficiency", "Thyrotoxicosis"],
        "interactions": ["Calcium supplements", "Iron supplements", "Antacids", "Cholestyramine"],
    },

    # ── Antacid ──
    {
        "name": "Sucralfate",
        "generic_name": "Sucralfate",
        "category": "Mucosal Protectant",
        "form": "Tablet 1g",
        "common_dosage": "1g four times daily before meals and at bedtime",
        "max_daily": "4g",
        "side_effects": ["Constipation", "Nausea", "Dry mouth"],
        "contraindications": ["Renal impairment (aluminium absorption)"],
        "interactions": ["Fluoroquinolones", "Phenytoin", "Tetracyclines", "Warfarin"],
    },

    # ── Anti-gout ──
    {
        "name": "Allopurinol",
        "generic_name": "Allopurinol",
        "category": "Xanthine Oxidase Inhibitor (Anti-gout)",
        "form": "Tablet 100mg / 300mg",
        "common_dosage": "100-300mg once daily after food",
        "max_daily": "800mg",
        "side_effects": ["Rash", "GI upset", "Liver enzyme elevation", "Hypersensitivity syndrome (rare)"],
        "contraindications": ["Acute gout attack (do not initiate)", "Hypersensitivity"],
        "interactions": ["Azathioprine", "Mercaptopurine", "Warfarin", "ACE inhibitors"],
    },
    {
        "name": "Colchicine",
        "generic_name": "Colchicine",
        "category": "Anti-gout",
        "form": "Tablet 0.5mg",
        "common_dosage": "0.5mg 2-3 times daily",
        "max_daily": "1.5mg",
        "side_effects": ["Diarrhea", "Nausea", "Vomiting", "Abdominal cramps"],
        "contraindications": ["Severe renal impairment", "Severe hepatic impairment", "Blood dyscrasias"],
        "interactions": ["CYP3A4 inhibitors", "P-gp inhibitors", "Statins"],
    },
]


# ─────────────────────────────────────────────────────────────
# Search & Lookup Functions
# ─────────────────────────────────────────────────────────────

def search_medicines(query: str, limit: int = 10) -> list:
    """
    Fuzzy prefix search across medicine name and generic name.
    Returns a list of matching medicine dicts, sorted by relevance.
    """
    if not query or len(query.strip()) < 1:
        return []

    query_lower = query.strip().lower()
    results = []

    for med in MEDICINES:
        name_lower = med["name"].lower()
        generic_lower = med["generic_name"].lower()
        category_lower = med["category"].lower()

        # Exact prefix match on name — highest priority
        if name_lower.startswith(query_lower):
            results.append((0, med))
        # Exact prefix match on generic name
        elif generic_lower.startswith(query_lower):
            results.append((1, med))
        # Substring match in name
        elif query_lower in name_lower:
            results.append((2, med))
        # Substring match in generic name
        elif query_lower in generic_lower:
            results.append((3, med))
        # Category match
        elif query_lower in category_lower:
            results.append((4, med))

    results.sort(key=lambda x: (x[0], x[1]["name"]))
    return [r[1] for r in results[:limit]]


def get_medicine_info(name: str) -> dict | None:
    """Get full details for a specific medicine by exact name."""
    for med in MEDICINES:
        if med["name"].lower() == name.lower():
            return med
    return None


def get_all_medicine_names() -> list:
    """Return a sorted list of all medicine names for selectbox."""
    return sorted([m["name"] for m in MEDICINES])


def get_all_categories() -> list:
    """Return unique sorted list of all therapeutic categories."""
    return sorted(set(m["category"] for m in MEDICINES))


def get_medicines_by_category(category: str) -> list:
    """Return all medicines in a specific category."""
    return [m for m in MEDICINES if m["category"] == category]
