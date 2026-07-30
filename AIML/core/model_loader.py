"""
core/model_loader.py — Model & Scaler Loader (Singleton)
========================================================
Loads the pre-trained GradientBoostingClassifier and StandardScaler
from disk exactly once, then caches them for the lifetime of the app.

Also loads test data artifacts for the Performance page.

Usage:
    loader = ModelLoader()
    model = loader.model
    scaler = loader.scaler
"""

import os
import logging
from typing import Optional

import joblib
import numpy as np

from core.utils import MODELS_DIR

logger = logging.getLogger("HealthcareAI.model_loader")


class ModelLoader:
    """
    Singleton loader for ML model artifacts.

    Loads from the models/ directory:
        - model.joblib       → trained classifier
        - scaler.joblib      → fitted StandardScaler
        - X_test.joblib      → test features
        - y_test.joblib      → test labels
        - X_train.joblib     → training features (SHAP background)
        - feature_names.joblib → ordered feature column names

    Attributes:
        model:         The trained sklearn classifier.
        scaler:        The fitted StandardScaler.
        X_test:        Test feature matrix (scaled).
        y_test:        Test label vector.
        X_train:       Training feature matrix (scaled, for SHAP).
        feature_names: List of feature column names.
        is_loaded:     True if all artifacts loaded successfully.
        error_message: Error description if loading failed.
    """

    _instance: Optional["ModelLoader"] = None

    def __new__(cls) -> "ModelLoader":
        """Ensure only one instance exists (singleton pattern)."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        """Load model artifacts on first instantiation."""
        if self._initialized:
            return

        self.model = None
        self.scaler = None
        self.X_test: Optional[np.ndarray] = None
        self.y_test: Optional[np.ndarray] = None
        self.X_train: Optional[np.ndarray] = None
        self.feature_names: list[str] = []
        self.is_loaded: bool = False
        self.error_message: str = ""

        self._load_artifacts()
        self._initialized = True

    def _load_artifacts(self) -> None:
        """
        Attempt to load all required model artifacts from disk.
        Sets is_loaded=True on success, populates error_message on failure.
        """
        required_files = {
            "model":         "model.joblib",
            "scaler":        "scaler.joblib",
            "X_test":        "X_test.joblib",
            "y_test":        "y_test.joblib",
            "X_train":       "X_train.joblib",
            "feature_names": "feature_names.joblib",
        }

        logger.info("Loading model artifacts from: %s", MODELS_DIR)

        # Check that models directory exists
        if not os.path.isdir(MODELS_DIR):
            self.error_message = (
                f"Models directory not found: {MODELS_DIR}\n"
                "Please run 'python train_model.py' first."
            )
            logger.error(self.error_message)
            return

        # Check all files exist before loading any
        missing = []
        for attr_name, filename in required_files.items():
            path = os.path.join(MODELS_DIR, filename)
            if not os.path.isfile(path):
                missing.append(filename)

        if missing:
            self.error_message = (
                f"Missing model files: {', '.join(missing)}\n"
                "Please run 'python train_model.py' to generate them."
            )
            logger.error(self.error_message)
            return

        # Load each artifact
        try:
            for attr_name, filename in required_files.items():
                path = os.path.join(MODELS_DIR, filename)
                obj = joblib.load(path)
                setattr(self, attr_name, obj)
                logger.info("  Loaded %s (%s)", filename, type(obj).__name__)

            self.is_loaded = True
            logger.info("All model artifacts loaded successfully.")

        except Exception as e:
            self.error_message = f"Error loading model artifacts: {str(e)}"
            logger.exception(self.error_message)

    def reload(self) -> None:
        """Force reload of all artifacts (useful after retraining)."""
        self._initialized = False
        self.is_loaded = False
        self.error_message = ""
        self._load_artifacts()
        self._initialized = True
        logger.info("Model artifacts reloaded.")
