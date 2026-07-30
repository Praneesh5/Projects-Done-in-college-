"""
core/charts.py — Chart Factory for Model Performance Visuals
============================================================
Creates publication-quality matplotlib figures for the Performance page:
    - Confusion Matrix heatmap
    - ROC Curve with AUC shading
    - Feature Importance bar chart
    - Metrics summary bar chart

All charts use the application color palette and are designed to be
embedded directly into Tkinter canvas widgets.

Usage:
    from core.charts import create_confusion_matrix, create_roc_curve
    fig = create_confusion_matrix(y_test, y_pred)
"""

import logging
from typing import Optional

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.figure
from matplotlib.colors import LinearSegmentedColormap
from sklearn.metrics import (
    confusion_matrix,
    roc_curve,
    auc,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
)

from core.model_loader import ModelLoader

logger = logging.getLogger("HealthcareAI.charts")

# ─────────────────────────────────────────────────────────────────────
# COLOR PALETTE (matches the app theme)
# ─────────────────────────────────────────────────────────────────────

PRIMARY = "#2563EB"
SUCCESS = "#16A34A"
DANGER = "#DC2626"
WARNING = "#F59E0B"
DARK_TEXT = "#1F2937"
LIGHT_BG = "#F5F7FA"


def _style_axes(ax: plt.Axes) -> None:
    """Apply consistent professional styling to chart axes."""
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#D1D5DB")
    ax.spines["bottom"].set_color("#D1D5DB")
    ax.tick_params(colors=DARK_TEXT, labelsize=10)


# ─────────────────────────────────────────────────────────────────────
# CONFUSION MATRIX
# ─────────────────────────────────────────────────────────────────────

def create_confusion_matrix(
    y_true: np.ndarray,
    y_pred: np.ndarray,
) -> matplotlib.figure.Figure:
    """
    Create an annotated confusion matrix heatmap.

    Args:
        y_true: True labels.
        y_pred: Predicted labels.

    Returns:
        Matplotlib Figure.
    """
    cm = confusion_matrix(y_true, y_pred)
    fig, ax = plt.subplots(figsize=(7, 6))

    # Custom blue colormap
    cmap = LinearSegmentedColormap.from_list("blue_custom", ["#EFF6FF", PRIMARY])
    im = ax.imshow(cm, interpolation="nearest", cmap=cmap)

    # Add text annotations
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            color = "white" if cm[i, j] > cm.max() / 2 else DARK_TEXT
            ax.text(j, i, str(cm[i, j]),
                     ha="center", va="center",
                     fontsize=22, fontweight="bold", color=color)

    ax.set_xticks([0, 1])
    ax.set_yticks([0, 1])
    ax.set_xticklabels(["No Disease", "Disease"], fontsize=11)
    ax.set_yticklabels(["No Disease", "Disease"], fontsize=11)
    ax.set_xlabel("Predicted Label", fontsize=12, labelpad=10)
    ax.set_ylabel("True Label", fontsize=12, labelpad=10)
    ax.set_title("Confusion Matrix", fontsize=14, fontweight="bold", pad=15)

    fig.colorbar(im, ax=ax, shrink=0.8)
    plt.tight_layout()
    return fig


# ─────────────────────────────────────────────────────────────────────
# ROC CURVE
# ─────────────────────────────────────────────────────────────────────

def create_roc_curve(
    y_true: np.ndarray,
    y_proba: np.ndarray,
) -> matplotlib.figure.Figure:
    """
    Create an ROC curve with AUC area filled.

    Args:
        y_true:  True labels.
        y_proba: Predicted probabilities for the positive class.

    Returns:
        Matplotlib Figure.
    """
    fpr, tpr, _ = roc_curve(y_true, y_proba)
    roc_auc = auc(fpr, tpr)

    fig, ax = plt.subplots(figsize=(8, 7))

    # Fill area under curve
    ax.fill_between(fpr, tpr, alpha=0.15, color=PRIMARY)

    # ROC curve
    ax.plot(fpr, tpr, color=PRIMARY, linewidth=2.5,
             label=f"ROC Curve (AUC = {roc_auc:.3f})")

    # Diagonal reference line
    ax.plot([0, 1], [0, 1], color="#9CA3AF", linewidth=1.5,
             linestyle="--", label="Random Classifier")

    ax.set_xlabel("False Positive Rate", fontsize=12, labelpad=10)
    ax.set_ylabel("True Positive Rate", fontsize=12, labelpad=10)
    ax.set_title("ROC Curve — Receiver Operating Characteristic",
                  fontsize=14, fontweight="bold", pad=15)
    ax.legend(loc="lower right", fontsize=11, framealpha=0.9)
    ax.set_xlim([-0.02, 1.02])
    ax.set_ylim([-0.02, 1.02])

    _style_axes(ax)
    plt.tight_layout()
    return fig


# ─────────────────────────────────────────────────────────────────────
# FEATURE IMPORTANCE
# ─────────────────────────────────────────────────────────────────────

def create_feature_importance(
    model,
    feature_names: list[str],
) -> matplotlib.figure.Figure:
    """
    Create a horizontal bar chart of model feature importances.

    Args:
        model:         Trained sklearn model with feature_importances_.
        feature_names: List of feature display names.

    Returns:
        Matplotlib Figure.
    """
    importances = model.feature_importances_
    indices = np.argsort(importances)

    fig, ax = plt.subplots(figsize=(9, 7))

    # Gradient colors from light to dark blue
    colors = [plt.cm.Blues(0.3 + 0.7 * i / len(indices)) for i in range(len(indices))]

    ax.barh(
        range(len(indices)),
        importances[indices],
        color=colors,
        edgecolor="white",
        height=0.65,
    )
    ax.set_yticks(range(len(indices)))
    ax.set_yticklabels([feature_names[i] for i in indices], fontsize=10)
    ax.set_xlabel("Feature Importance", fontsize=12, labelpad=10)
    ax.set_title("Feature Importance — Gradient Boosting Model",
                  fontsize=14, fontweight="bold", pad=15)

    _style_axes(ax)
    plt.tight_layout()
    return fig


# ─────────────────────────────────────────────────────────────────────
# METRICS COMPUTATION
# ─────────────────────────────────────────────────────────────────────

def compute_all_metrics() -> Optional[dict]:
    """
    Compute all model performance metrics using the saved test set.

    Returns:
        Dictionary with metrics and figures, or None on failure.
    """
    loader = ModelLoader()
    if not loader.is_loaded:
        logger.error("Cannot compute metrics: model not loaded.")
        return None

    try:
        y_true = loader.y_test
        y_pred = loader.model.predict(loader.X_test)
        y_proba = loader.model.predict_proba(loader.X_test)[:, 1]

        from sklearn.model_selection import cross_val_score
        cv_scores = cross_val_score(
            loader.model, loader.X_train, 
            # We need y_train for CV — approximate from model
            loader.model.predict(loader.X_train),
            cv=5, scoring="accuracy"
        )

        from core.utils import FEATURE_DISPLAY_NAMES, FEATURE_COLUMNS
        feature_labels = [FEATURE_DISPLAY_NAMES.get(f, f) for f in FEATURE_COLUMNS]

        metrics = {
            "accuracy":     accuracy_score(y_true, y_pred),
            "precision":    precision_score(y_true, y_pred),
            "recall":       recall_score(y_true, y_pred),
            "f1_score":     f1_score(y_true, y_pred),
            "roc_auc":      roc_auc_score(y_true, y_proba),
            "cv_mean":      cv_scores.mean(),
            "cv_std":       cv_scores.std(),
            "confusion_fig": create_confusion_matrix(y_true, y_pred),
            "roc_fig":       create_roc_curve(y_true, y_proba),
            "importance_fig": create_feature_importance(loader.model, feature_labels),
            "y_true":        y_true,
            "y_pred":        y_pred,
            "y_proba":       y_proba,
        }

        logger.info(
            "Metrics computed — Accuracy: %.3f, AUC: %.3f",
            metrics["accuracy"], metrics["roc_auc"],
        )
        return metrics

    except Exception as e:
        logger.exception("Failed to compute metrics: %s", e)
        return None
