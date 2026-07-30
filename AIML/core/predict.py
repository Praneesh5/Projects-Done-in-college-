"""
core/predict.py — Prediction Engine
====================================
Takes a dictionary of 13 patient features, scales them, runs them
through the trained model, and returns a structured PredictionResult.

The result includes: binary prediction, probability, confidence,
risk category, and a clinical recommendation string.

Usage:
    from core.predict import predict_heart_disease
    result = predict_heart_disease({"age": 55, "sex": 1, ...})
    print(result.prediction_label)  # "Heart Disease Detected"
"""

import logging
from dataclasses import dataclass, field
from typing import Optional

import numpy as np

from core.model_loader import ModelLoader
from core.utils import (
    FEATURE_COLUMNS,
    get_risk_category,
    get_risk_color,
    get_recommendation,
    format_feature_value,
    FEATURE_DISPLAY_NAMES,
)

logger = logging.getLogger("HealthcareAI.predict")


@dataclass
class PredictionResult:
    """
    Structured result from the prediction engine.

    Attributes:
        prediction:        Binary prediction (0 = No Disease, 1 = Disease).
        prediction_label:  Human-readable prediction string.
        probability:       Probability of heart disease (0.0 to 1.0).
        probability_pct:   Probability as a formatted percentage string.
        confidence:        Confidence in the prediction (0.0 to 1.0).
        confidence_pct:    Confidence as a formatted percentage string.
        risk_category:     "Low", "Medium", or "High".
        risk_color:        Hex color for the risk category.
        recommendation:    Multi-line clinical recommendation.
        feature_values:    Dict of raw input values.
        scaled_values:     Numpy array of scaled feature values.
        success:           True if prediction succeeded.
        error_message:     Error description if prediction failed.
    """
    prediction: int = 0
    prediction_label: str = ""
    probability: float = 0.0
    probability_pct: str = "0.0%"
    confidence: float = 0.0
    confidence_pct: str = "0.0%"
    risk_category: str = "Low"
    risk_color: str = "#16A34A"
    recommendation: str = ""
    feature_values: dict = field(default_factory=dict)
    scaled_values: Optional[np.ndarray] = None
    success: bool = False
    error_message: str = ""


def predict_heart_disease(inputs: dict[str, float]) -> PredictionResult:
    """
    Run a heart disease prediction for a single patient.

    Steps:
        1. Load model and scaler (cached singleton)
        2. Arrange features in the correct column order
        3. Scale the features
        4. Predict class and probability
        5. Compute confidence, risk category, and recommendation

    Args:
        inputs: Dictionary mapping feature names to numeric values.
                Example: {"age": 55, "sex": 1, "cp": 0, ...}

    Returns:
        PredictionResult dataclass with all prediction details.
    """
    result = PredictionResult()
    result.feature_values = dict(inputs)

    # ── 1. Load model ────────────────────────────────────────────────
    loader = ModelLoader()
    if not loader.is_loaded:
        result.error_message = loader.error_message
        logger.error("Prediction failed: model not loaded.")
        return result

    # ── 2. Prepare feature vector ────────────────────────────────────
    try:
        feature_vector = np.array(
            [float(inputs[col]) for col in FEATURE_COLUMNS]
        ).reshape(1, -1)
    except (KeyError, ValueError, TypeError) as e:
        result.error_message = f"Invalid input data: {str(e)}"
        logger.error(result.error_message)
        return result

    # ── 3. Scale features ────────────────────────────────────────────
    try:
        scaled = loader.scaler.transform(feature_vector)
        result.scaled_values = scaled
    except Exception as e:
        result.error_message = f"Scaling error: {str(e)}"
        logger.error(result.error_message)
        return result

    # ── 4. Predict ───────────────────────────────────────────────────
    try:
        prediction = int(loader.model.predict(scaled)[0])
        probabilities = loader.model.predict_proba(scaled)[0]

        # probabilities[0] = P(no disease), probabilities[1] = P(disease)
        disease_prob = float(probabilities[1])

        # Confidence = how far the model is from the 50% decision boundary
        # A 95% prediction is more confident than a 55% prediction
        confidence = abs(disease_prob - 0.5) * 2  # Maps [0.5, 1.0] → [0, 1.0]

        result.prediction = prediction
        result.prediction_label = (
            "Heart Disease Detected" if prediction == 1
            else "No Heart Disease Detected"
        )
        result.probability = disease_prob
        result.probability_pct = f"{disease_prob * 100:.1f}%"
        result.confidence = confidence
        result.confidence_pct = f"{confidence * 100:.1f}%"
        result.risk_category = get_risk_category(disease_prob)
        result.risk_color = get_risk_color(result.risk_category)
        result.recommendation = get_recommendation(result.risk_category, disease_prob)
        result.success = True

        logger.info(
            "Prediction: %s | Prob: %s | Risk: %s | Confidence: %s",
            result.prediction_label,
            result.probability_pct,
            result.risk_category,
            result.confidence_pct,
        )

    except Exception as e:
        result.error_message = f"Prediction error: {str(e)}"
        logger.exception(result.error_message)

    return result


def get_formatted_inputs(inputs: dict[str, float]) -> list[tuple[str, str, str]]:
    """
    Format raw input values for display in reports and result cards.

    Args:
        inputs: Dict mapping feature names to raw numeric values.

    Returns:
        List of (feature_name, display_name, formatted_value) tuples.
    """
    formatted = []
    for col in FEATURE_COLUMNS:
        val = inputs.get(col, "—")
        display_name = FEATURE_DISPLAY_NAMES.get(col, col)
        formatted_val = format_feature_value(col, val)
        formatted.append((col, display_name, formatted_val))
    return formatted
