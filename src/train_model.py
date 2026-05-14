# ============================================
# CROP RECOMMENDATION SYSTEM
# src/train_model.py
# Run this script to retrain and save the model
# Usage: python src/train_model.py
# ============================================

import pandas as pd
import numpy as np
import joblib
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def train_and_save_model():
    """Train the crop recommendation model and save it to disk."""

    print("=" * 50)
    print("  CROP RECOMMENDATION MODEL TRAINING")
    print("=" * 50)

    # --- Step 1: Load Data ---
    print("\n[1/5] Loading dataset...")
    df = pd.read_csv("data/crop_data.csv")
    print(f"      Dataset shape: {df.shape}")

    # --- Step 2: Prepare Features ---
    print("\n[2/5] Preparing features...")
    X = df.drop("label", axis=1)
    y = df["label"]
    print(f"      Features : {X.columns.tolist()}")
    print(f"      Crops    : {y.nunique()} unique crops")

    # --- Step 3: Split Data ---
    print("\n[3/5] Splitting data (80% train / 20% test)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )
    print(f"      Training : {X_train.shape[0]} samples")
    print(f"      Testing  : {X_test.shape[0]} samples")

    # --- Step 4: Train Model ---
    print("\n[4/5] Training Random Forest model...")
    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train, y_train)

    accuracy = accuracy_score(y_test, model.predict(X_test))
    print(f"      Testing Accuracy: {accuracy * 100:.2f}%")

    # --- Step 5: Save Model ---
    print("\n[5/5] Saving model to disk...")
    os.makedirs("models", exist_ok=True)
    model_path = os.path.join("models", "crop_model.pkl")
    joblib.dump(model, model_path, compress=3)

    size_kb = os.path.getsize(model_path) / 1024
    print(f"      Saved to : {model_path}")
    print(f"      Size     : {size_kb:.1f} KB")

    print("\n" + "=" * 50)
    print("  MODEL TRAINING COMPLETE!")
    print(f"  Accuracy : {accuracy * 100:.2f}%")
    print("=" * 50)

    return model, accuracy


if __name__ == "__main__":
    train_and_save_model()
