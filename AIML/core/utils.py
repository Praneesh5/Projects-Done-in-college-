"""
core/utils.py — Utility Functions and Constants
================================================
Provides logging setup, input validation, feature name mappings,
clinical value labels, and shared helper functions used across
the entire application.

This module is imported by nearly every other module — it must
remain dependency-free (no imports from other core/ modules).
"""

import os
import sys
import logging
from datetime import datetime
from typing import Any, Optional

# ─────────────────────────────────────────────────────────────────────
# PATH RESOLUTION — Works both in dev and when packaged with PyInstaller
# ─────────────────────────────────────────────────────────────────────

def get_base_path() -> str:
    """
    Return the application base directory.
    When frozen by PyInstaller, sys._MEIPASS points to the temp bundle.
    Otherwise, use the project root (parent of core/).
    """
    if getattr(sys, "frozen", False):
        return sys._MEIPASS  # type: ignore[attr-defined]
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


BASE_DIR = get_base_path()
MODELS_DIR = os.path.join(BASE_DIR, "models")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
DATA_PATH = os.path.join(BASE_DIR, "heart_cleaned.csv")

# Ensure output directories exist
os.makedirs(REPORTS_DIR, exist_ok=True)


# ─────────────────────────────────────────────────────────────────────
# LOGGING
# ─────────────────────────────────────────────────────────────────────

def setup_logging(level: int = logging.INFO) -> logging.Logger:
    """
    Configure application-wide logging to both console and file.

    Args:
        level: Logging level (default INFO).

    Returns:
        Configured root logger for the application.
    """
    logger = logging.getLogger("HealthcareAI")

    # Avoid adding duplicate handlers on repeated calls
    if logger.handlers:
        return logger

    logger.setLevel(level)
    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)-8s %(name)s — %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console handler
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(level)
    console.setFormatter(formatter)
    logger.addHandler(console)

    # File handler (rotating would be better for production, but keep simple)
    log_path = os.path.join(BASE_DIR, "app.log")
    try:
        file_handler = logging.FileHandler(log_path, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except (PermissionError, OSError):
        logger.warning("Could not create log file at %s", log_path)

    return logger


# Initialize logger for this module
logger = setup_logging()


# ─────────────────────────────────────────────────────────────────────
# FEATURE NAME MAPPINGS
# ─────────────────────────────────────────────────────────────────────

# Maps raw column names → human-readable clinical labels
FEATURE_DISPLAY_NAMES: dict[str, str] = {
    "age":      "Age",
    "sex":      "Sex",
    "cp":       "Chest Pain Type",
    "trestbps": "Resting Blood Pressure",
    "chol":     "Serum Cholesterol",
    "fbs":      "Fasting Blood Sugar",
    "restecg":  "Resting ECG",
    "thalach":  "Maximum Heart Rate",
    "exang":    "Exercise Induced Angina",
    "oldpeak":  "ST Depression (Oldpeak)",
    "slope":    "ST Slope",
    "ca":       "Major Vessels (ca)",
    "thal":     "Thalassemia",
}

# Ordered list of feature column names (must match training order)
FEATURE_COLUMNS: list[str] = [
    "age", "sex", "cp", "trestbps", "chol", "fbs",
    "restecg", "thalach", "exang", "oldpeak", "slope", "ca", "thal",
]


# ─────────────────────────────────────────────────────────────────────
# CATEGORICAL VALUE LABELS
# ─────────────────────────────────────────────────────────────────────

# For each categorical feature, map numeric values → clinical labels
CATEGORICAL_LABELS: dict[str, dict[int, str]] = {
    "sex": {
        0: "Female",
        1: "Male",
    },
    "cp": {
        0: "Typical Angina",
        1: "Atypical Angina",
        2: "Non-anginal Pain",
        3: "Asymptomatic",
    },
    "fbs": {
        0: "≤ 120 mg/dl (Normal)",
        1: "> 120 mg/dl (High)",
    },
    "restecg": {
        0: "Normal",
        1: "ST-T Wave Abnormality",
        2: "Left Ventricular Hypertrophy",
    },
    "exang": {
        0: "No",
        1: "Yes",
    },
    "slope": {
        0: "Upsloping",
        1: "Flat",
        2: "Downsloping",
    },
    "ca": {
        0: "0 vessels",
        1: "1 vessel",
        2: "2 vessels",
        3: "3 vessels",
        4: "4 vessels",
    },
    "thal": {
        0: "Normal",
        1: "Fixed Defect",
        2: "Reversible Defect",
        3: "Thalassemia",
    },
}


# ─────────────────────────────────────────────────────────────────────
# INPUT VALIDATION
# ─────────────────────────────────────────────────────────────────────

# Min/max ranges for numeric input fields
FEATURE_RANGES: dict[str, tuple[float, float]] = {
    "age":      (1, 120),
    "trestbps": (50, 250),
    "chol":     (50, 700),
    "thalach":  (50, 250),
    "oldpeak":  (0.0, 10.0),
}

# Allowed discrete values for categorical fields
FEATURE_ALLOWED_VALUES: dict[str, list[int]] = {
    "sex":     [0, 1],
    "cp":      [0, 1, 2, 3],
    "fbs":     [0, 1],
    "restecg": [0, 1, 2],
    "exang":   [0, 1],
    "slope":   [0, 1, 2],
    "ca":      [0, 1, 2, 3, 4],
    "thal":    [0, 1, 2, 3],
}


def validate_input(feature: str, value: Any) -> tuple[bool, str]:
    """
    Validate a single feature input value.

    Args:
        feature: The feature column name (e.g., 'age', 'cp').
        value:   The user-entered value.

    Returns:
        (is_valid, error_message) tuple.
        error_message is empty string when valid.
    """
    display = FEATURE_DISPLAY_NAMES.get(feature, feature)

    # Check for empty/None
    if value is None or (isinstance(value, str) and value.strip() == ""):
        return False, f"{display} is required."

    # Try numeric conversion
    try:
        num = float(value)
    except (ValueError, TypeError):
        return False, f"{display}: Please enter a valid number."

    # Range check for continuous features
    if feature in FEATURE_RANGES:
        lo, hi = FEATURE_RANGES[feature]
        if not (lo <= num <= hi):
            return False, f"{display}: Value must be between {lo} and {hi}."

    # Discrete value check for categorical features
    if feature in FEATURE_ALLOWED_VALUES:
        if int(num) not in FEATURE_ALLOWED_VALUES[feature]:
            allowed = ", ".join(str(v) for v in FEATURE_ALLOWED_VALUES[feature])
            return False, f"{display}: Allowed values are {allowed}."

    return True, ""


def validate_all_inputs(inputs: dict[str, Any]) -> tuple[bool, list[str]]:
    """
    Validate all 13 feature inputs at once.

    Args:
        inputs: Dict mapping feature names to values.

    Returns:
        (all_valid, list_of_error_messages)
    """
    errors: list[str] = []
    for feat in FEATURE_COLUMNS:
        val = inputs.get(feat)
        ok, msg = validate_input(feat, val)
        if not ok:
            errors.append(msg)
    return len(errors) == 0, errors


# ─────────────────────────────────────────────────────────────────────
# CLINICAL HELPERS
# ─────────────────────────────────────────────────────────────────────

def get_risk_category(probability: float) -> str:
    """
    Categorize disease probability into clinical risk levels.

    Thresholds:
        < 30%  → Low Risk
        30–70% → Medium Risk
        > 70%  → High Risk

    Args:
        probability: Disease probability as a float in [0, 1].

    Returns:
        Risk category string.
    """
    if probability < 0.30:
        return "Low"
    elif probability <= 0.70:
        return "Medium"
    else:
        return "High"


def get_risk_color(category: str) -> str:
    """Return hex color for a risk category."""
    return {
        "Low":    "#16A34A",  # Green
        "Medium": "#F59E0B",  # Amber
        "High":   "#DC2626",  # Red
    }.get(category, "#6B7280")


def get_recommendation(risk_category: str, probability: float) -> str:
    """
    Generate a clinical recommendation based on risk level.

    Args:
        risk_category: "Low", "Medium", or "High".
        probability: Disease probability as a float in [0, 1].

    Returns:
        A multi-line recommendation string.
    """
    pct = f"{probability * 100:.1f}%"

    if risk_category == "Low":
        return (
            f"The predicted probability of heart disease is {pct}, indicating LOW RISK.\n\n"
            "• Continue maintaining a healthy lifestyle with regular exercise.\n"
            "• Monitor blood pressure and cholesterol annually.\n"
            "• No immediate cardiac intervention is indicated based on this screening.\n"
            "• Consult a physician for routine preventive care."
        )
    elif risk_category == "Medium":
        return (
            f"The predicted probability of heart disease is {pct}, indicating MODERATE RISK.\n\n"
            "• Schedule a follow-up consultation with a cardiologist.\n"
            "• Consider additional diagnostic tests (stress test, echocardiogram).\n"
            "• Adopt lifestyle modifications: diet, exercise, stress management.\n"
            "• Monitor blood pressure, cholesterol, and blood sugar closely.\n"
            "• Review family history with your healthcare provider."
        )
    else:
        return (
            f"The predicted probability of heart disease is {pct}, indicating HIGH RISK.\n\n"
            "• Urgent cardiology referral is strongly recommended.\n"
            "• Comprehensive cardiac evaluation should be performed promptly.\n"
            "• Consider coronary angiography or advanced imaging.\n"
            "• Aggressive management of risk factors is essential.\n"
            "• Begin pharmacological intervention as clinically indicated.\n"
            "• This is a screening result — clinical judgment must guide final decisions."
        )


def format_feature_value(feature: str, value: Any) -> str:
    """
    Format a feature value for display, using clinical labels
    for categorical features.

    Args:
        feature: Feature column name.
        value: Numeric value.

    Returns:
        Formatted string (e.g., "Male" instead of "1" for sex).
    """
    if feature in CATEGORICAL_LABELS:
        int_val = int(float(value))
        return CATEGORICAL_LABELS[feature].get(int_val, str(value))
    return str(value)


def get_timestamp() -> str:
    """Return current timestamp in a readable format."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_date_string() -> str:
    """Return current date in a readable format."""
    return datetime.now().strftime("%B %d, %Y")
