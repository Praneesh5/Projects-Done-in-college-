"""
gui/pages/shap_page.py — SHAP Explainability Page
==================================================
Provides interactive SHAP analysis with 5 plot types:
    1. Summary (beeswarm) plot
    2. Bar plot (mean |SHAP|)
    3. Waterfall plot (single sample breakdown)
    4. Force plot (push/pull visualization)
    5. Dependence plot (feature interaction)

Each plot includes a plain-English explanation panel.
Supports both global analysis (test set) and patient-specific
analysis (if a prediction has been run).
"""

import logging
import threading
from typing import Optional

import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

from gui.theme import Colors, Fonts, Spacing, Icons
from gui.components import SectionHeader, AnimatedButton, LoadingOverlay

logger = logging.getLogger("HealthcareAI.pages.shap_page")


class SHAPPage(ctk.CTkFrame):
    """SHAP interpretability analysis page."""

    def __init__(self, parent, app_ref=None, **kwargs):
        super().__init__(parent, fg_color=Colors.BACKGROUND, **kwargs)

        self._app_ref = app_ref
        self._explainer = None
        self._current_plot = None
        self._build_ui()

    def _build_ui(self) -> None:
        """Build the SHAP page layout."""
        pad = Spacing.CONTENT_PAD

        self._scroll = ctk.CTkScrollableFrame(
            self, fg_color=Colors.BACKGROUND,
            scrollbar_button_color=Colors.BORDER,
        )
        self._scroll.pack(fill="both", expand=True)

        SectionHeader(
            self._scroll,
            title=f"{Icons.SHAP}  SHAP Explainability Analysis",
            subtitle="SHapley Additive exPlanations — Global & local feature importance",
        ).pack(fill="x", padx=pad, pady=(pad, 12))

        # ── Plot Selection Buttons ────────────────────────────────────
        btn_frame = ctk.CTkFrame(self._scroll, fg_color="transparent")
        btn_frame.pack(fill="x", padx=pad, pady=(0, 12))

        plots = [
            ("Summary Plot", self._show_summary),
            ("Bar Plot", self._show_bar),
            ("Waterfall Plot", self._show_waterfall),
            ("Force Plot", self._show_force),
            ("Dependence Plot", self._show_dependence),
        ]

        for i, (label, cmd) in enumerate(plots):
            AnimatedButton(
                btn_frame, text=label, command=cmd,
                color=Colors.PRIMARY if i == 0 else Colors.SIDEBAR_BG,
                hover_color=Colors.PRIMARY_HOVER,
                width=150, height=38,
            ).pack(side="left", padx=4)

        # Patient-specific button
        AnimatedButton(
            btn_frame, text="Patient SHAP",
            icon=Icons.USER,
            command=self._show_patient_shap,
            color="#7C3AED",
            hover_color="#6D28D9",
            width=160, height=38,
        ).pack(side="right", padx=4)

        # ── Chart Display Area ────────────────────────────────────────
        self._chart_card = ctk.CTkFrame(
            self._scroll, fg_color=Colors.CARD,
            corner_radius=12, border_width=1,
            border_color=Colors.BORDER_LIGHT,
        )
        self._chart_card.pack(fill="both", expand=True, padx=pad, pady=(0, 12))

        self._chart_container = ctk.CTkFrame(self._chart_card, fg_color="transparent")
        self._chart_container.pack(fill="both", expand=True, padx=8, pady=8)

        # ── Explanation Panel ─────────────────────────────────────────
        self._explanation_card = ctk.CTkFrame(
            self._scroll, fg_color=Colors.CARD,
            corner_radius=12, border_width=1,
            border_color=Colors.BORDER_LIGHT,
        )
        self._explanation_card.pack(fill="x", padx=pad, pady=(0, pad))

        self._explanation_header = ctk.CTkLabel(
            self._explanation_card,
            text="📝  Explanation",
            font=Fonts.HEADING_3,
            text_color=Colors.TEXT_PRIMARY,
            anchor="w",
        )
        self._explanation_header.pack(fill="x", padx=16, pady=(12, 4))

        self._explanation_text = ctk.CTkLabel(
            self._explanation_card,
            text="Select a plot type above to generate SHAP explanations.\n"
                 "SHAP values are computed using TreeExplainer for exact Shapley values.",
            font=Fonts.SMALL,
            text_color=Colors.TEXT_SECONDARY,
            wraplength=900, justify="left", anchor="nw",
        )
        self._explanation_text.pack(fill="x", padx=16, pady=(0, 12))

        # Loading overlay
        self._loading = LoadingOverlay(self, message="Computing SHAP values...")

    def _get_explainer(self):
        """Lazily initialize the SHAP explainer."""
        if self._explainer is None:
            from core.shap_explainer import SHAPExplainer
            self._explainer = SHAPExplainer()
        return self._explainer

    def _show_plot(self, plot_func, explanation_func, title: str) -> None:
        """Generic handler to compute and display a SHAP plot."""
        self._loading.show()

        def compute():
            try:
                explainer = self._get_explainer()
                fig = plot_func(explainer)
                text = explanation_func(explainer)
                self.after(0, lambda: self._render_plot(fig, text, title))
            except Exception as e:
                logger.exception("SHAP plot failed: %s", e)
                self.after(0, lambda: self._render_error(str(e)))
            finally:
                self.after(0, self._loading.hide)

        threading.Thread(target=compute, daemon=True).start()

    def _render_plot(self, fig, explanation: str, title: str) -> None:
        """Render a matplotlib figure and its explanation."""
        # Clear previous chart
        for w in self._chart_container.winfo_children():
            w.destroy()

        if fig is None:
            self._render_error("Failed to generate plot.")
            return

        fig.set_size_inches(10, 6)
        fig.set_facecolor(Colors.CARD)
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self._chart_container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        self._current_plot = fig

        # Update explanation
        self._explanation_header.configure(text=f"📝  {title} — Explanation")
        self._explanation_text.configure(text=explanation)

    def _render_error(self, message: str) -> None:
        """Show error in the chart area."""
        for w in self._chart_container.winfo_children():
            w.destroy()

        ctk.CTkLabel(
            self._chart_container,
            text=f"❌  {message}",
            font=Fonts.BODY,
            text_color=Colors.DANGER,
        ).pack(pady=40)

    # ── Plot Handlers ─────────────────────────────────────────────────

    def _show_summary(self) -> None:
        self._show_plot(
            lambda e: e.summary_plot(),
            lambda e: e.get_summary_explanation(),
            "SHAP Summary Plot",
        )

    def _show_bar(self) -> None:
        self._show_plot(
            lambda e: e.bar_plot(),
            lambda e: (
                "The bar plot shows the mean absolute SHAP value for each feature.\n"
                "Features with higher bars have more influence on the model's predictions overall.\n"
                "This is a global view — it represents average importance across all test samples.\n\n"
                + e.get_summary_explanation()
            ),
            "SHAP Bar Plot",
        )

    def _show_waterfall(self) -> None:
        self._show_plot(
            lambda e: e.waterfall_plot(sample_idx=0),
            lambda e: (
                "The waterfall plot shows how each feature contributes to a single prediction.\n"
                "Starting from the base value (average model output), each feature pushes the\n"
                "prediction higher (red) or lower (blue). The final value is the model output.\n\n"
                "This shows the first test sample. Run a patient prediction and use\n"
                "'Patient SHAP' to see explanations for your own input."
            ),
            "SHAP Waterfall Plot",
        )

    def _show_force(self) -> None:
        self._show_plot(
            lambda e: e.force_plot_image(sample_idx=0),
            lambda e: (
                "The force plot visualizes how features push the prediction away from\n"
                "the base value. Red features push toward higher risk (Heart Disease),\n"
                "while blue features push toward lower risk (No Disease).\n\n"
                "Feature width indicates the magnitude of the contribution.\n"
                "This plot provides an intuitive 'tug-of-war' view of the prediction."
            ),
            "SHAP Force Plot",
        )

    def _show_dependence(self) -> None:
        self._show_plot(
            lambda e: e.dependence_plot(feature_idx=0),
            lambda e: (
                "The dependence plot shows how a single feature's value relates to its\n"
                "SHAP value (impact on prediction). Each dot is a patient.\n\n"
                "The color shows the strongest interacting feature — revealing how\n"
                "feature combinations affect predictions.\n\n"
                "A positive SHAP value means the feature value increases predicted risk\n"
                "for that patient; negative means it decreases risk."
            ),
            "SHAP Dependence Plot",
        )

    def _show_patient_shap(self) -> None:
        """Show SHAP explanation for the most recent patient prediction."""
        # Get the prediction result from the prediction page
        if self._app_ref is None:
            self._render_error("App reference not available.")
            return

        pred_page = self._app_ref.get_page("prediction")
        if pred_page is None:
            self._render_error("Prediction page not found.")
            return

        result = pred_page.get_last_result()
        if result is None or not result.success:
            self._render_error(
                "No prediction available.\n"
                "Please run a patient prediction first, then return here."
            )
            return

        self._loading.show()

        def compute():
            try:
                explainer = self._get_explainer()
                shap_values = explainer.explain_patient(result.scaled_values)
                if shap_values is not None:
                    explanation = explainer.get_patient_explanation(shap_values)
                    # Create a waterfall-like figure for this patient
                    import matplotlib.pyplot as plt
                    import shap
                    import numpy as np
                    from core.utils import FEATURE_DISPLAY_NAMES, FEATURE_COLUMNS

                    labels = [FEATURE_DISPLAY_NAMES.get(f, f) for f in FEATURE_COLUMNS]

                    fig, ax = plt.subplots(figsize=(10, 7))
                    sorted_idx = np.argsort(np.abs(shap_values))
                    colors = ["#DC2626" if v > 0 else "#2563EB" for v in shap_values[sorted_idx]]

                    ax.barh(
                        [labels[i] for i in sorted_idx],
                        shap_values[sorted_idx],
                        color=colors, edgecolor="white",
                        height=0.6, alpha=0.85,
                    )
                    ax.set_xlabel("SHAP Value (Impact on Prediction)", fontsize=11)
                    ax.set_title(
                        f"Patient-Specific SHAP Values — {result.prediction_label}",
                        fontsize=13, fontweight="bold", pad=15,
                    )
                    ax.axvline(x=0, color="#1F2937", linewidth=0.8)
                    ax.spines["top"].set_visible(False)
                    ax.spines["right"].set_visible(False)
                    plt.tight_layout()

                    self.after(0, lambda: self._render_plot(
                        fig, explanation, "Patient-Specific SHAP"
                    ))
                else:
                    self.after(0, lambda: self._render_error("Failed to compute patient SHAP values."))
            except Exception as e:
                logger.exception("Patient SHAP failed: %s", e)
                self.after(0, lambda: self._render_error(str(e)))
            finally:
                self.after(0, self._loading.hide)

        threading.Thread(target=compute, daemon=True).start()

    def get_current_figure(self):
        """Return the currently displayed matplotlib figure (for export)."""
        return self._current_plot

    def get_explanation_text(self) -> str:
        """Return the current explanation text (for reports)."""
        return self._explanation_text.cget("text")
