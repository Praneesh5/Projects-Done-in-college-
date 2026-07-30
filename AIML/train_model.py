"""
train_model.py — One-Time Model Training Script
================================================
Trains a GradientBoostingClassifier on the UCI Heart Disease dataset,
applies StandardScaler, and saves all artifacts needed by the desktop app.

Run this script ONCE before launching the application:
    python train_model.py

Artifacts saved to models/:
    - model.joblib     : Trained GradientBoostingClassifier
    - scaler.joblib    : Fitted StandardScaler
    - X_test.joblib    : Test features (for Performance page metrics)
    - y_test.joblib    : Test labels  (for Performance page metrics)
    - X_train.joblib   : Training features (for SHAP background data)
    - feature_names.joblib : List of feature column names

Author: Your Name
Project: Model Interpretability in Clinical ML using SHAP & LIME
"""

import os
import sys
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    classification_report,
    confusion_matrix,
)
import joblib


def train_and_save_model(data_path: str = "heart_cleaned.csv",
                         output_dir: str = "models") -> None:
    """
    End-to-end training pipeline.

    Steps:
        1. Load and validate the dataset
        2. Split into train/test (80/20, stratified)
        3. Scale features with StandardScaler
        4. Train GradientBoostingClassifier with tuned hyperparameters
        5. Evaluate on test set
        6. Save all artifacts to output_dir/

    Args:
        data_path: Path to the cleaned CSV file.
        output_dir: Directory to save model artifacts.
    """
    # ── 1. Load Dataset ──────────────────────────────────────────────
    print("=" * 60)
    print("  Heart Disease Model Training Pipeline")
    print("=" * 60)

    if not os.path.exists(data_path):
        print(f"\n[ERROR] Dataset not found: {data_path}")
        print("Please ensure 'heart_cleaned.csv' is in the project root.")
        sys.exit(1)

    df = pd.read_csv(data_path)
    print(f"\n[1/6] Dataset loaded: {df.shape[0]} rows × {df.shape[1]} columns")

    # Validate expected columns
    expected_cols = [
        "age", "sex", "cp", "trestbps", "chol", "fbs",
        "restecg", "thalach", "exang", "oldpeak", "slope",
        "ca", "thal", "target",
    ]
    missing = set(expected_cols) - set(df.columns)
    if missing:
        print(f"[ERROR] Missing columns: {missing}")
        sys.exit(1)

    # Separate features and target
    feature_names = [c for c in expected_cols if c != "target"]
    X = df[feature_names].values
    y = df["target"].values
    print(f"       Features: {len(feature_names)}")
    print(f"       Target distribution: {dict(zip(*np.unique(y, return_counts=True)))}")

    # ── 2. Train/Test Split ──────────────────────────────────────────
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )
    print(f"\n[2/6] Train/test split: {len(X_train)} train / {len(X_test)} test")

    # ── 3. Feature Scaling ───────────────────────────────────────────
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    print("[3/6] StandardScaler fitted on training data")

    # ── 4. Train Model ───────────────────────────────────────────────
    # GradientBoosting chosen for:
    #   - Excellent performance on small tabular datasets
    #   - Native predict_proba for calibrated probabilities
    #   - Exact SHAP values via TreeExplainer (no approximation)
    #   - Interpretable feature importances
    model = GradientBoostingClassifier(
        n_estimators=200,
        learning_rate=0.1,
        max_depth=4,
        min_samples_split=5,
        min_samples_leaf=3,
        subsample=0.85,
        random_state=42,
        validation_fraction=0.15,
        n_iter_no_change=15,       # Early stopping to prevent overfitting
        tol=1e-4,
    )
    print("[4/6] Training GradientBoostingClassifier...")
    model.fit(X_train_scaled, y_train)
    print(f"       Stopped at {model.n_estimators_} estimators (early stopping)")

    # ── 5. Evaluate ──────────────────────────────────────────────────
    y_pred = model.predict(X_test_scaled)
    y_proba = model.predict_proba(X_test_scaled)[:, 1]

    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_proba)

    # Cross-validation on full training set
    cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=5, scoring="accuracy")

    print(f"\n[5/6] Evaluation Results:")
    print(f"       Accuracy:    {accuracy:.4f}")
    print(f"       Precision:   {precision:.4f}")
    print(f"       Recall:      {recall:.4f}")
    print(f"       F1 Score:    {f1:.4f}")
    print(f"       ROC AUC:     {roc_auc:.4f}")
    print(f"       CV Accuracy: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")
    print(f"\nConfusion Matrix:\n{confusion_matrix(y_test, y_pred)}")
    print(f"\nClassification Report:\n{classification_report(y_test, y_pred, target_names=['No Disease', 'Disease'])}")

    # ── 6. Save Artifacts ────────────────────────────────────────────
    os.makedirs(output_dir, exist_ok=True)

    artifacts = {
        "model.joblib": model,
        "scaler.joblib": scaler,
        "X_test.joblib": X_test_scaled,
        "y_test.joblib": y_test,
        "X_train.joblib": X_train_scaled,
        "feature_names.joblib": feature_names,
    }

    for filename, obj in artifacts.items():
        path = os.path.join(output_dir, filename)
        joblib.dump(obj, path)
        print(f"       Saved: {path}")

    print(f"\n[6/6] All artifacts saved to '{output_dir}/'")
    print("=" * 60)
    print("  Training complete. You can now launch the application.")
    print("=" * 60)


if __name__ == "__main__":
    train_and_save_model()
