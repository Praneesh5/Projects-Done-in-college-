"""
core/lime_explainer.py — LIME Interpretability Engine
=====================================================
Generates LIME (Local Interpretable Model-agnostic Explanations)
for individual patient predictions.

LIME works by:
    1. Perturbing the input sample to create synthetic neighbors
    2. Training a simple linear model on those neighbors
    3. Using the linear model weights to explain the prediction

Usage:
    explainer = LIMEExplainer()
    result = explainer.explain(scaled_values, raw_values)
    fig = result["figure"]
    table = result["table"]
    text = result["explanation"]
"""

import logging
from typing import Any, Optional

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.figure
from lime.lime_tabular import LimeTabularExplainer

from core.model_loader import ModelLoader
from core.utils import FEATURE_DISPLAY_NAMES, FEATURE_COLUMNS

logger = logging.getLogger("HealthcareAI.lime_explainer")


class LIMEExplainer:
    """
    LIME explanation generator for single-patient predictions.

    Uses LimeTabularExplainer trained on the same training data
    used for the model, ensuring consistent perturbation statistics.

    Attributes:
        explainer: lime.lime_tabular.LimeTabularExplainer instance.
        is_ready:  True if the explainer has been initialized.
    """

    def __init__(self) -> None:
        """Initialize the LIME explainer (deferred setup)."""
        self.explainer: Optional[LimeTabularExplainer] = None
        self.is_ready: bool = False
        self.error_message: str = ""
        self._loader = ModelLoader()

    def setup(self) -> bool:
        """
        Initialize the LIME explainer with training data statistics.

        Returns:
            True if setup succeeded.
        """
        if self.is_ready:
            return True

        if not self._loader.is_loaded:
            self.error_message = self._loader.error_message
            return False

        try:
            feature_labels = [
                FEATURE_DISPLAY_NAMES.get(f, f) for f in FEATURE_COLUMNS
            ]

            # Create the LIME explainer using training data for
            # computing feature statistics (mean, std, bins)
            self.explainer = LimeTabularExplainer(
                training_data=self._loader.X_train,
                feature_names=feature_labels,
                class_names=["No Disease", "Heart Disease"],
                mode="classification",
                discretize_continuous=True,
                random_state=42,
            )

            self.is_ready = True
            logger.info("LIME explainer initialized with %d training samples.",
                         len(self._loader.X_train))
            return True

        except Exception as e:
            self.error_message = f"LIME setup failed: {str(e)}"
            logger.exception(self.error_message)
            return False

    def explain(
        self,
        scaled_values: np.ndarray,
        num_features: int = 13,
    ) -> Optional[dict[str, Any]]:
        """
        Generate a LIME explanation for a single patient prediction.

        Args:
            scaled_values: 1D or 2D numpy array of scaled feature values.
            num_features:  Number of features to include (default: all 13).

        Returns:
            Dictionary with keys:
                - "figure":      Matplotlib Figure with the LIME bar chart.
                - "table":       List of (feature, weight, direction) tuples.
                - "explanation": Plain-English explanation string.
                - "intercept":   The local model intercept.
                - "score":       The local model R² score.
            Returns None on failure.
        """
        if not self.setup():
            return None

        try:
            # Flatten to 1D for LIME
            sample = scaled_values.flatten()

            logger.info("Generating LIME explanation for sample...")

            # Generate explanation
            exp = self.explainer.explain_instance(
                sample,
                self._loader.model.predict_proba,
                num_features=num_features,
                top_labels=1,
            )

            # Get the explained class (the predicted class)
            predicted_class = self._loader.model.predict(sample.reshape(1, -1))[0]
            label = int(predicted_class)

            # Extract feature contributions
            feature_weights = exp.as_list(label=label)

            # Build table data: (feature_description, weight, direction)
            table_data = []
            for feat_desc, weight in feature_weights:
                direction = "Positive" if weight > 0 else "Negative"
                table_data.append((feat_desc, weight, direction))

            # Create matplotlib figure
            fig = self._create_figure(table_data, label)

            # Generate explanation text
            explanation = self._generate_explanation(table_data, label)

            # Get local model metrics
            intercept = exp.intercept.get(label, 0.0)
            score = exp.score

            logger.info("LIME explanation generated: %d features, R²=%.3f",
                         len(table_data), score)

            return {
                "figure": fig,
                "table": table_data,
                "explanation": explanation,
                "intercept": intercept,
                "score": score,
            }

        except Exception as e:
            logger.exception("LIME explanation failed: %s", e)
            return None

    def _create_figure(
        self,
        table_data: list[tuple[str, float, str]],
        predicted_class: int,
    ) -> matplotlib.figure.Figure:
        """
        Create a professional horizontal bar chart of LIME feature weights.

        Positive contributions → blue bars (push toward Disease)
        Negative contributions → green bars (push toward No Disease)

        Args:
            table_data: List of (feature, weight, direction) tuples.
            predicted_class: The predicted class label.

        Returns:
            Matplotlib Figure.
        """
        fig, ax = plt.subplots(figsize=(10, 7))

        # Sort by absolute weight for display
        sorted_data = sorted(table_data, key=lambda x: abs(x[1]))

        features = [d[0] for d in sorted_data]
        weights = [d[1] for d in sorted_data]
        colors = ["#DC2626" if w > 0 else "#2563EB" for w in weights]

        # Truncate long feature names
        features = [f[:40] + "..." if len(f) > 40 else f for f in features]

        bars = ax.barh(features, weights, color=colors, edgecolor="white",
                        height=0.6, alpha=0.85)

        # Styling
        ax.set_xlabel("Feature Weight (Contribution)", fontsize=11, labelpad=10)
        ax.axvline(x=0, color="#1F2937", linewidth=0.8, linestyle="-")

        class_name = "Heart Disease" if predicted_class == 1 else "No Disease"
        ax.set_title(
            f"LIME Explanation — Local Feature Contributions\n"
            f"(Explaining: {class_name})",
            fontsize=13, fontweight="bold", pad=15,
        )

        # Add legend
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor="#DC2626", alpha=0.85, label="Pushes toward Disease"),
            Patch(facecolor="#2563EB", alpha=0.85, label="Pushes toward No Disease"),
        ]
        ax.legend(handles=legend_elements, loc="lower right", fontsize=9)

        ax.tick_params(axis="y", labelsize=9)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        plt.tight_layout()

        return fig

    def _generate_explanation(
        self,
        table_data: list[tuple[str, float, str]],
        predicted_class: int,
    ) -> str:
        """
        Generate a plain-English explanation from LIME feature weights.

        Args:
            table_data: List of (feature, weight, direction) tuples.
            predicted_class: The predicted class.

        Returns:
            Multi-line explanation string.
        """
        class_name = "Heart Disease" if predicted_class == 1 else "No Disease"

        lines = [
            f"LIME Explanation for Predicted Class: {class_name}",
            "=" * 55,
            "",
            "The model made this prediction based on the following",
            "local feature contributions:",
            "",
        ]

        # Sort by absolute weight (strongest first)
        sorted_data = sorted(table_data, key=lambda x: -abs(x[1]))

        for feat_desc, weight, direction in sorted_data[:6]:
            if direction == "Positive":
                verb = "supports" if predicted_class == 1 else "contradicts"
                lines.append(
                    f"  ✦ {feat_desc}: weight = {weight:+.4f} "
                    f"({verb} the prediction)"
                )
            else:
                verb = "contradicts" if predicted_class == 1 else "supports"
                lines.append(
                    f"  ✧ {feat_desc}: weight = {weight:+.4f} "
                    f"({verb} the prediction)"
                )

        lines.extend([
            "",
            "Positive weights push the prediction toward Heart Disease.",
            "Negative weights push the prediction toward No Disease.",
            "",
            "LIME fits a local linear model around this patient's features",
            "to approximate the complex model's behavior in this region.",
        ])

        return "\n".join(lines)
