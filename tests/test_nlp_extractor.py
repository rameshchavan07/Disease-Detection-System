import pytest
from modules.nlp_extractor import extract_symptoms

@pytest.fixture
def symptom_list():
    return ["fever", "high_fever", "cough", "headache", "vomiting", "itching", "stomach_pain", "abdominal_pain"]

def test_extract_simple_english(symptom_list):
    text = "I have a fever and a cough"
    results = extract_symptoms(text, symptom_list)
    assert "high_fever" in results or "fever" in results
    assert "cough" in results

def test_extract_negation(symptom_list):
    text = "I have a headache but no fever"
    results = extract_symptoms(text, symptom_list)
    assert "headache" in results
    assert "high_fever" not in results
    assert "fever" not in results

def test_extract_hinglish_bukhar(symptom_list):
    # This should match via the SYNONYMS map
    text = "Mujhe bukhar hai"
    results = extract_symptoms(text, symptom_list)
    assert any(s in results for s in ["high_fever", "fever"])

def test_extract_hindi_script(symptom_list):
    # This should match via the SYNONYMS map for Devanagari
    text = "मुझे बुखार और खांसी है"
    results = extract_symptoms(text, symptom_list)
    # Helpful for debugging
    assert any(s in results for s in ["high_fever", "fever"]), f"Fever not found in {results} for input {text}"
    assert "cough" in results, f"Cough not found in {results} for input {text}"

def test_extract_multi_word_synonym(symptom_list):
    text = "My stomach hurts a lot"
    results = extract_symptoms(text, symptom_list)
    assert any(s in results for s in ["stomach_pain", "abdominal_pain"])

def test_clean_text_logic():
    from modules.nlp_extractor import clean_text
    assert clean_text("Hello, World!") == "hello world"
    assert clean_text("Don't Panic!") == "don't panic"
