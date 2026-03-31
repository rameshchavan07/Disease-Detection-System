"""
Test Suite for MedDetect AI
Run with: pytest tests/ -v
"""
import sys
import os

# Ensure project root is in path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# ════════════════════════════════════════════
# 1. ML Engine Tests
# ════════════════════════════════════════════

class TestMLEngine:
    """Tests for the ML prediction engine."""

    def test_model_loads(self):
        """Model should load without errors."""
        from modules.ml_engine import get_all_symptoms, get_all_diseases
        symptoms = get_all_symptoms()
        diseases = get_all_diseases()
        assert len(symptoms) > 100, f"Expected 100+ symptoms, got {len(symptoms)}"
        assert len(diseases) > 50, f"Expected 50+ diseases, got {len(diseases)}"

    def test_predict_returns_valid_format(self):
        """Prediction should return list of dicts with expected keys."""
        from modules.ml_engine import predict_disease
        results = predict_disease(["headache", "fever"], top_k=3)
        assert isinstance(results, list)
        if results:
            assert "disease" in results[0]
            assert "confidence" in results[0]
            assert "rank" in results[0]
            assert results[0]["rank"] == 1

    def test_predict_empty_symptoms(self):
        """Empty symptom list should return empty results."""
        from modules.ml_engine import predict_disease
        results = predict_disease([], top_k=3)
        assert results == []

    def test_predict_invalid_symptoms(self):
        """Invalid symptom names should return empty results (no match)."""
        from modules.ml_engine import predict_disease
        results = predict_disease(["xyz_nonexistent_symptom"], top_k=3)
        assert results == []

    def test_sanitize_symptom(self):
        """Symptom sanitization should handle special chars."""
        from modules.ml_engine import _sanitize_symptom
        assert _sanitize_symptom("  Headache  ") == "headache"
        assert _sanitize_symptom("chest pain") == "chest_pain"
        assert _sanitize_symptom("HIGH_FEVER!") == "high_fever"

    def test_format_symptom_name(self):
        """Format should convert snake_case to Title Case."""
        from modules.ml_engine import format_symptom_name
        assert format_symptom_name("chest_pain") == "Chest Pain"
        assert format_symptom_name("high_fever") == "High Fever"

    def test_model_accuracy_returns_dict(self):
        """Model accuracy should return dict with expected keys."""
        from modules.ml_engine import get_model_accuracy
        acc = get_model_accuracy()
        assert "accuracy" in acc
        assert "cv_accuracy" in acc
        assert "version" in acc
        assert acc["accuracy"] > 0


# ════════════════════════════════════════════
# 2. NLP Extractor Tests
# ════════════════════════════════════════════

class TestNLPExtractor:
    """Tests for symptom extraction from text."""

    def test_clean_text(self):
        """Text cleaning should lowercase and remove punctuation."""
        from modules.nlp_extractor import clean_text
        assert clean_text("I have a HEADACHE!!!") == "i have a headache"
        assert clean_text("chest_pain") == "chest pain"

    def test_negation_detection(self):
        """Negated symptoms should be detected."""
        from modules.nlp_extractor import is_negated
        assert is_negated("i don't have fever", "fever") is True
        assert is_negated("i have fever", "fever") is False
        assert is_negated("no headache today", "headache") is True

    def test_extract_exact_match(self):
        """Direct symptom names should be extracted."""
        from modules.nlp_extractor import extract_symptoms
        from modules.ml_engine import get_all_symptoms
        symptoms = get_all_symptoms()
        result = extract_symptoms("i have headache and cough", symptoms)
        assert "headache" in result or "cough" in result

    def test_extract_empty_text(self):
        """Empty text should return empty list."""
        from modules.nlp_extractor import extract_symptoms
        assert extract_symptoms("", []) == []
        assert extract_symptoms("   ", []) == []

    def test_synonym_mapping(self):
        """Synonyms should map to valid symptom names."""
        from modules.nlp_extractor import SYNONYMS
        assert "fever" in SYNONYMS
        assert "headache" in SYNONYMS
        assert isinstance(SYNONYMS["fever"], list)


# ════════════════════════════════════════════
# 3. Medicine Database Tests
# ════════════════════════════════════════════

class TestMedicineDB:
    """Tests for the medicine database."""

    def test_all_medicines_loaded(self):
        """Should have 50+ medicines."""
        from modules.medicine_db import get_all_medicine_names
        names = get_all_medicine_names()
        assert len(names) >= 50, f"Expected 50+ medicines, got {len(names)}"

    def test_search_by_prefix(self):
        """Search should find medicines by prefix."""
        from modules.medicine_db import search_medicines
        results = search_medicines("para")
        assert len(results) >= 1
        assert any("Paracetamol" in r["name"] for r in results)

    def test_search_case_insensitive(self):
        """Search should be case-insensitive."""
        from modules.medicine_db import search_medicines
        r1 = search_medicines("AMOX")
        r2 = search_medicines("amox")
        assert len(r1) == len(r2)

    def test_search_empty_query(self):
        """Empty query should return empty list."""
        from modules.medicine_db import search_medicines
        assert search_medicines("") == []

    def test_get_medicine_info(self):
        """Should return full info for existing medicine."""
        from modules.medicine_db import get_medicine_info
        info = get_medicine_info("Paracetamol")
        assert info is not None
        assert info["name"] == "Paracetamol"
        assert "side_effects" in info
        assert "contraindications" in info
        assert "interactions" in info
        assert isinstance(info["side_effects"], list)

    def test_get_medicine_info_nonexistent(self):
        """Should return None for non-existent medicine."""
        from modules.medicine_db import get_medicine_info
        assert get_medicine_info("NonexistentDrug123") is None

    def test_medicine_data_completeness(self):
        """Every medicine should have all required fields."""
        from modules.medicine_db import get_all_medicine_names, get_medicine_info
        required_keys = {"name", "generic_name", "category", "form", "common_dosage", "max_daily", "side_effects", "contraindications", "interactions"}
        for name in get_all_medicine_names():
            info = get_medicine_info(name)
            assert info is not None, f"Missing info for {name}"
            missing = required_keys - set(info.keys())
            assert not missing, f"Medicine '{name}' missing keys: {missing}"


# ════════════════════════════════════════════
# 4. Prescription PDF Tests
# ════════════════════════════════════════════

class TestPrescriptionPDF:
    """Tests for PDF prescription generation."""

    def test_generates_bytes(self):
        """PDF generator should return bytes."""
        from modules.prescription_pdf import generate_prescription_pdf
        pdf = generate_prescription_pdf(
            hospital_name="Test Hospital",
            hospital_address="123 Test St",
            doctor_name="Test Doctor",
            doctor_specialty="General Physician",
            doctor_email="dr@test.com",
            patient_email="patient@test.com",
            appointment_date="2026-04-01",
            diagnosis="Common Cold",
            medicines=[{"name": "Paracetamol", "dosage": "500mg", "frequency": "3x daily", "duration": "5 days"}],
            medicine_details=[],
            notes="Rest well"
        )
        assert isinstance(pdf, bytes), f"Expected bytes, got {type(pdf)}"
        assert len(pdf) > 500, "PDF too small, likely empty"

    def test_pdf_starts_with_header(self):
        """Valid PDF should start with %PDF header."""
        from modules.prescription_pdf import generate_prescription_pdf
        pdf = generate_prescription_pdf(
            hospital_name="Test", hospital_address="",
            doctor_name="Doc", doctor_specialty="GP",
            doctor_email="", patient_email="p@test.com",
            appointment_date="2026-01-01", diagnosis="Test",
            medicines=[{"name": "Test", "dosage": "1mg", "frequency": "daily", "duration": "1 day"}],
            medicine_details=[], notes=""
        )
        assert pdf[:5] == b"%PDF-", "PDF should start with %PDF- header"

    def test_empty_medicines(self):
        """Should handle empty medicines list gracefully."""
        from modules.prescription_pdf import generate_prescription_pdf
        pdf = generate_prescription_pdf(
            hospital_name="H", hospital_address="A",
            doctor_name="D", doctor_specialty="S",
            doctor_email="e", patient_email="p",
            appointment_date="2026-01-01", diagnosis="D",
            medicines=[], medicine_details=[], notes=""
        )
        assert isinstance(pdf, bytes)


# ════════════════════════════════════════════
# 5. Config / Settings Tests
# ════════════════════════════════════════════

class TestConfig:
    """Tests for application configuration."""

    def test_app_constants_exist(self):
        """All centralized app constants should be defined."""
        from config.settings import (
            APP_NAME, APP_VERSION, APP_VERSION_DISPLAY,
            TOTAL_DISEASES, TOTAL_SYMPTOMS, MODEL_ACCURACY_DISPLAY,
            TRAINING_SAMPLES, SESSION_TIMEOUT_MINUTES
        )
        assert APP_NAME == "MedDetect AI"
        assert "." in APP_VERSION  # e.g., "2.0.0"
        assert APP_VERSION_DISPLAY.startswith("v")
        assert SESSION_TIMEOUT_MINUTES > 0

    def test_paths_exist(self):
        """Critical file paths should resolve."""
        from config.settings import BASE_DIR, DATA_DIR, MODELS_DIR
        assert os.path.isdir(BASE_DIR)
        assert os.path.isdir(DATA_DIR)
        assert os.path.isdir(MODELS_DIR)

    def test_severity_levels(self):
        """Severity config should have all levels."""
        from config.settings import SEVERITY_LEVELS
        for level in ["low", "moderate", "high", "critical"]:
            assert level in SEVERITY_LEVELS
            assert "label" in SEVERITY_LEVELS[level]
            assert "color" in SEVERITY_LEVELS[level]
            assert "icon" in SEVERITY_LEVELS[level]
