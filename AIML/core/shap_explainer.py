"""
core/shap_explainer.py — SHAP Interpretability Engine
=====================================================
Generates SHAP (SHapley Additive exPlanations) values and plots
for both global model understanding and local (per-patient) explanations.

Uses TreeExplainer for exact Shapley values on the GradientBoosting model.

Supported plots:
    - Summary plot (beeswarm)
    - Bar plot (mean absolute SHAP)
    - Waterfall plot (single prediction breakdown)
    - Force plot (single prediction push/pull)
    - Dependence plot (feature interaction)

Each plot also generates a plain-English explanation.

Usage:
    explainer = SHAPExplainer()
    fig = explainer.summary_plot()
    text = explainer.get_summary_explanation()
"""

import io
import logging
from typing import Optional

import numpy as np
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend for embedding in Tkinter
import matplotlib.pyplot as plt
import matplotlib.figure
import shap

from core.model_loader import ModelLoader
from core.utils import FEATURE_DISPLAY_NAMES, FEATURE_COLUMNS

logger = logging.getLogger("HealthcareAI.shap_explainer")


class SHAPExplainer:
    """
    SHAP explanation generator.

    Computes SHAP values using TreeExplainer and provides methods
    to create publication-quality plots with clinical explanations.

    Attributes:
        explainer:   shap.TreeExplainer instance.
        shap_values: SHAP values for the test set.
        is_ready:    True if SHAP values have been computed.
    """

    def __init__(self) -> None:
        """Initialize the SHAP explainer but defer computation."""
        self.explainer: Optional[shap.TreeExplainer] = None
        self.shap_values: Optional[np.ndarray] = None
        self.expected_value: Optional[float] = None
        self.is_ready: bool = False
        self.error_message: str = ""
        self._loader = ModelLoader()

    def compute(self) -> bool:
        """
        Compute SHAP values for the test dataset.

        Returns:
            True if computation succeeded.
        """
        if self.is_ready:
            return True

        if not self._loader.is_loaded:
            self.error_message = self._loader.error_message
            return False

        try:
            logger.info("Computing SHAP values (TreeExplainer)...")

            # TreeExplainer gives exact Shapley values for tree-based models
            self.explainer = shap.TreeExplainer(self._loader.model)

            # Compute SHAP values for the test set
            shap_result = self.explainer.shap_values(self._loader.X_test)

            # For GradientBoosting, shap_values returns a single array
            # (the log-odds contribution for the positive class)
            if isinstance(shap_result, list):
                self.shap_values = shap_result[1]
            else:
                self.shap_values = shap_result

            # Expected value (base rate before any features)
            ev = self.explainer.expected_value
            if isinstance(ev, (list, np.ndarray)):
                self.expected_value = float(ev[1]) if len(ev) > 1 else float(ev[0])
            else:
                self.expected_value = float(ev)

            self.is_ready = True
            logger.info("SHAP values computed: shape %s", self.shap_values.shape)
            return True

        except Exception as e:
            self.error_message = f"SHAP computation failed: {str(e)}"
            logger.exception(self.error_message)
            return False

    def _get_feature_labels(self) -> list[str]:
        """Return display-friendly feature names."""
        return [FEATURE_DISPLAY_NAMES.get(f, f) for f in FEATURE_COLUMNS]

    # ─────────────────────────────────────────────────────────────────
    # GLOBAL PLOTS (computed on full test set)
    # ─────────────────────────────────────────────────────────────────

    def summary_plot(self) -> Optional[matplotlib.figure.Figure]:
        """
        SHAP summary (beeswarm) plot showing feature impact distribution.
        Each dot represents a sample; color = feature value; x = SHAP value.
        """
        if not self.compute():
            return None

        try:
            fig, ax = plt.subplots(figsize=(10, 7))
            shap.summary_plot(
                self.shap_values,
                self._loader.X_test,
                feature_names=self._get_feature_labels(),
                show=False,
                plot_size=None,
            )
            plt.title("SHAP Summary Plot — Feature Impact Distribution",
                       fontsize=13, fontweight="bold", pad=15)
            plt.tight_layout()
            return plt.gcf()
        except Exception as e:
            logger.exception("Failed to create SHAP summary plot: %s", e)
            return None

    def bar_plot(self) -> Optional[matplotlib.figure.Figure]:
        """
        SHAP bar plot showing mean absolute SHAP values per feature.
        Indicates overall feature importance for the model.
        """
        if not self.compute():
            return None

        try:
            fig, ax = plt.subplots(figsize=(10, 7))
            shap.summary_plot(
                self.shap_values,
                self._loader.X_test,
                feature_names=self._get_feature_labels(),
                plot_type="bar",
                show=False,
                plot_size=None,
            )
            plt.title("SHAP Feature Importance — Mean |SHAP Value|",
                       fontsize=13, fontweight="bold", pad=15)
            plt.tight_layout()
            return plt.gcf()
        except Exception as e:
            logger.exception("Failed to create SHAP bar plot: %s", e)
            return None

    # ─────────────────────────────────────────────────────────────────
    # LOCAL PLOTS (for a specific patient / sample index)
    # ─────────────────────────────────────────────────────────────────

    def waterfall_plot(self, sample_idx: int = 0) -> Optional[matplotlib.figure.Figure]:
        """
        SHAP waterfall plot for a single prediction.
        Shows how each feature pushed the prediction from the base value.

        Args:
            sample_idx: Index into the test set (default: first sample).
        """
        if not self.compute():
            return None

        try:
            fig, ax = plt.subplots(figsize=(10, 7))

            explanation = shap.Explanation(
                values=self.shap_values[sample_idx],
                base_values=self.expected_value,
                data=self._loader.X_test[sample_idx],
                feature_names=self._get_feature_labels(),
            )
            shap.plots.waterfall(explanation, show=False)
            plt.title("SHAP Waterfall — Single Prediction Breakdown",
                       fontsize=13, fontweight="bold", pad=15)
            plt.tight_layout()
            return plt.gcf()
        except Exception as e:
            logger.exception("Failed to create SHAP waterfall plot: %s", e)
            return None

    def force_plot_image(self, sample_idx: int = 0) -> Optional[matplotlib.figure.Figure]:
        """
        SHAP force plot for a single prediction, rendered as a matplotlib figure.

        Args:
            sample_idx: Index into the test set.
        """
        if not self.compute():
            return None

        try:
            # Generate force plot as matplotlib figure
            fig = shap.plots.force(
                self.expected_value,
                self.shap_values[sample_idx],
                feature_names=self._get_feature_labels(),
                matplotlib=True,
                show=False,
            )
            plt.title("SHAP Force Plot — Prediction Drivers",
                       fontsize=13, fontweight="bold", pad=20)
            plt.tight_layout()
            return plt.gcf()
        except Exception as e:
            logger.exception("Failed to create SHAP force plot: %s", e)
            return None

    def dependence_plot(self, feature_idx: int = 0) -> Optional[matplotlib.figure.Figure]:
        """
        SHAP dependence plot showing how a single feature's value
        affects predictions, colored by the strongest interaction.

        Args:
            feature_idx: Index of the feature to plot.
        """
        if not self.compute():
            return None

        try:
            labels = self._get_feature_labels()
            fig, ax = plt.subplots(figsize=(10, 7))
            shap.dependence_plot(
                feature_idx,
                self.shap_values,
                self._loader.X_test,
                feature_names=labels,
                ax=ax,
                show=False,
            )
            plt.title(f"SHAP Dependence — {labels[feature_idx]}",
                       fontsize=13, fontweight="bold", pad=15)
            plt.tight_layout()
            return fig
        except Exception as e:
            logger.exception("Failed to create SHAP dependence plot: %s", e)
            return None

    # ─────────────────────────────────────────────────────────────────
    # PATIENT-SPECIFIC SHAP (for a new prediction, not test set)
    # ─────────────────────────────────────────────────────────────────

    def explain_patient(self, scaled_values: np.ndarray) -> Optional[np.ndarray]:
        """
        Compute SHAP values for a single patient (new input, not from test set).

        Args:
            scaled_values: 1D or 2D numpy array of scaled features.

        Returns:
            1D array of SHAP values, or None on failure.
        """
        if not self.compute():
            return None

        try:
            sv = self.explainer.shap_values(scaled_values)
            if isinstance(sv, list):
                return sv[1].flatten()
            return sv.flatten()
        except Exception as e:
            logger.exception("Failed to compute patient SHAP values: %s", e)
            return None

    # ─────────────────────────────────────────────────────────────────
    # PLAIN-ENGLISH EXPLANATIONS
    # ─────────────────────────────────────────────────────────────────

    def get_summary_explanation(self) -> str:
        """
        Generate a plain-English explanation of the overall SHAP summary.
        Identifies the top contributing features across the test set.
        """
        if not self.is_ready:
            return "SHAP values have not been computed yet."

        labels = self._get_feature_labels()
        mean_abs = np.mean(np.abs(self.shap_values), axis=0)
        ranked = sorted(zip(labels, mean_abs), key=lambda x: -x[1])

        lines = [
            "Overall Feature Importance (SHAP):",
            "=" * 45,
            "",
        ]

        for i, (name, val) in enumerate(ranked[:5], 1):
            pct = val / mean_abs.sum() * 100
            lines.append(
                f"  {i}. {name}: Mean |SHAP| = {val:.4f} "
                f"({pct:.1f}% of total impact)"
            )

        lines.extend([
            "",
            f"The top feature, {ranked[0][0]}, has the strongest",
            "influence on the model's heart disease predictions.",
            f"{ranked[1][0]} and {ranked[2][0]} are also major contributors.",
        ])

        return "\n".join(lines)

    def get_patient_explanation(self, shap_values: np.ndarray) -> str:
        """
        Generate a plain-English explanation for a single patient's
        SHAP values.

        Args:
            shap_values: 1D array of SHAP values for one prediction.

        Returns:
            Multi-line explanation string.
        """
        labels = self._get_feature_labels()
        pairs = list(zip(labels, shap_values))

        # Sort by absolute magnitude
        pairs_sorted = sorted(pairs, key=lambda x: -abs(x[1]))

        lines = [
            "Patient-Specific Feature Contributions (SHAP):",
            "=" * 50,
            "",
        ]

        for name, val in pairs_sorted[:6]:
            direction = "increased" if val > 0 else "decreased"
            strength = "strongly" if abs(val) > 0.5 else "moderately" if abs(val) > 0.2 else "slightly"
            lines.append(
                f"  • {name} {strength} {direction} the predicted risk "
                f"(SHAP = {val:+.4f})"
            )

        lines.extend([
            "",
            "Positive SHAP values push the prediction toward Heart Disease.",
            "Negative SHAP values push it toward No Heart Disease.",
        ])

        return "\n".join(lines)
