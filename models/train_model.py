"""
Model Training Script
Trains Random Forest classifier on symptom-disease dataset.
"""
import os, sys, json, joblib
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "dataset.csv")
MODEL_PATH = os.path.join(BASE_DIR, "models", "trained_model.pkl")

def train():
    print("Loading dataset...")
    df = pd.read_csv(DATA_PATH)
    print(f"Dataset: {df.shape[0]} samples, {df.shape[1]-1} features, {df['prognosis'].nunique()} diseases")
    
    X = df.drop("prognosis", axis=1)
    y = df["prognosis"]
    
    # Encode labels
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
    )
    
    print(f"Train: {X_train.shape[0]} | Test: {X_test.shape[0]}")
    
    # Train Random Forest
    print("Training Random Forest...")
    model = RandomForestClassifier(
        n_estimators=200, max_depth=None, min_samples_split=2,
        min_samples_leaf=1, random_state=42, n_jobs=-1
    )
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\nAccuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
    
    # Cross-validation
    cv_scores = cross_val_score(model, X, y_encoded, cv=5, n_jobs=-1)
    print(f"Cross-Val Accuracy: {cv_scores.mean():.4f} (+/- {cv_scores.std()*2:.4f})")
    
    # Save model, encoder, and feature names
    model_data = {
        "model": model,
        "label_encoder": le,
        "feature_names": list(X.columns),
        "disease_names": list(le.classes_),
        "accuracy": accuracy,
        "cv_accuracy": cv_scores.mean()
    }
    
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(model_data, MODEL_PATH)
    print(f"\nModel saved to: {MODEL_PATH}")
    
    return model_data

if __name__ == "__main__":
    train()
