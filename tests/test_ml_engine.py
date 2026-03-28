import pytest
from modules.ml_engine import predict_disease

def test_ml_prediction_basic():
    # Fever and cough are common for many diseases (e.g., Common Cold, Typhoid)
    symptoms = ["high_fever", "cough"]
    predictions = predict_disease(symptoms, top_k=3)
    
    assert len(predictions) > 0
    assert "disease" in predictions[0]
    assert "confidence" in predictions[0]
    # Check that rank starts at 1
    assert predictions[0]["rank"] == 1

def test_ml_prediction_specific():
    # Itching and skin rash are specific to Fungal infection
    symptoms = ["itching", "skin_rash", "dischromic_patches"]
    predictions = predict_disease(symptoms, top_k=1)
    
    assert predictions[0]["disease"] == "Fungal infection"
    assert predictions[0]["confidence"] > 50

def test_empty_symptoms():
    # Empty symptoms should return empty list
    assert predict_disease([], top_k=5) == []

def test_invalid_symptom_handling():
    # Handling of unknown symptoms (should just ignore them or return general results)
    symptoms = ["unknown_crazy_symptom", "high_fever"]
    predictions = predict_disease(symptoms, top_k=5)
    
    assert len(predictions) > 0
    # Should still find something based on 'high_fever'
    assert any(p["confidence"] > 0 for p in predictions)
