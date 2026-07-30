"""
gui/pages/performance.py — Model Performance Page
==================================================
Displays comprehensive model evaluation metrics:
    - Accuracy, Precision, Recall, F1, ROC AUC cards
    - Cross-validation score
    - Confusion Matrix heatmap
    - ROC Curve
    - Feature Importance chart

Metrics are computed once from the saved test set and cached.
"""

import logging
import threading
from typing import Optional

import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

from gui.theme import Colors, Fonts, Spacing, Icons
from gui.components import MetricCard, SectionHeader, LoadingOverlay

logger = logging.getLogger("HealthcareAI.pages.performance")


class PerformancePage(ctk.CTkFrame):
    """Model performance evaluation page."""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color=Colors.BACKGROUND, **kwargs)

        self._metrics: Optional[dict] = None
        self._loaded = False
        self._build_ui()

    def _build_ui(self) -> None:
        """Build the performance page layout."""
        pad = Spacing.CONTENT_PAD

        self._scroll = ctk.CTkScrollableFrame(
            self, fg_color=Colors.BACKGROUND,
            scrollbar_button_color=Colors.BORDER,
        )
        self._scroll.pack(fill="both", expand=True)

        SectionHeader(
            self._scroll,
            title=f"{Icons.PERFORMANCE}  Model Performance Evaluation",
            subtitle="Comprehensive metrics from the trained GradientBoosting model",
        ).pack(fill="x", padx=pad, pady=(pad, 12))

        # Placeholder for content
        self._content_frame = ctk.CTkFrame(self._scroll, fg_color="transparent")
        self._content_frame.pack(fill="both", expand=True, padx=pad, pady=(0, pad))

        # Loading overlay
        self._loading = LoadingOverlay(self, message="Computing metrics...")

        # Initial message
        self._initial_label = ctk.CTkLabel(
            self._content_frame,
            text="Click 'Load Metrics' or navigate here to compute model performance.",
            font=Fonts.BODY,
            text_color=Colors.TEXT_MUTED,
        )
        self._initial_label.pack(pady=40)

    def load_metrics(self) -> None:
        """Compute and display all performance metrics."""
        if self._loaded:
            return

        self._loading.show()

        def compute():
            try:
                from core.charts import compute_all_metrics
                metrics = compute_all_metrics()
                self.after(0, lambda: self._display_metrics(metrics))
            except Exception as e:
                logger.exception("Failed to compute metrics: %s", e)
                self.after(0, lambda: self._show_error(str(e)))
            finally:
                self.after(0, self._loading.hide)

        threading.Thread(target=compute, daemon=True).start()

    def _display_metrics(self, metrics: Optional[dict]) -> None:
        """Render all metrics and charts."""
        if metrics is None:
            self._show_error("Could not compute metrics. Is the model trained?")
            return

        self._metrics = metrics
        self._loaded = True

        # Clear placeholder
        for w in self._content_frame.winfo_children():
            w.destroy()

        pad = Spacing.CONTENT_PAD

        # ── Metric Cards Row ─────────────────────────────────────────
        cards_frame = ctk.CTkFrame(self._content_frame, fg_color="transparent")
        cards_frame.pack(fill="x", pady=(0, 16))
        cards_frame.columnconfigure((0, 1, 2, 3, 4), weight=1, uniform="mcard")

        card_defs = [
            ("Accuracy", f"{metrics['accuracy']:.4f}", Icons.CHECK, Colors.SUCCESS),
            ("Precision", f"{metrics['precision']:.4f}", "🎯", Colors.PRIMARY),
            ("Recall", f"{metrics['recall']:.4f}", "📋", Colors.WARNING),
            ("F1 Score", f"{metrics['f1_score']:.4f}", "⚖️", Colors.INFO),
            ("ROC AUC", f"{metrics['roc_auc']:.4f}", "📐", "#7C3AED"),
        ]

        for col, (title, value, icon, color) in enumerate(card_defs):
            card = MetricCard(
                cards_frame, title=title, value=value,
                icon=icon, accent_color=color,
            )
            card.grid(row=0, column=col, padx=4, pady=4, sticky="nsew")

        # Cross-validation score
        cv_frame = ctk.CTkFrame(
            self._content_frame, fg_color=Colors.CARD,
            corner_radius=12, border_width=1,
            border_color=Colors.BORDER_LIGHT,
        )
        cv_frame.pack(fill="x", pady=(0, 16))

        ctk.CTkLabel(
            cv_frame,
            text=f"📊  Cross-Validation Accuracy: "
                 f"{metrics['cv_mean']:.4f} ± {metrics['cv_std']:.4f} (5-Fold CV)",
            font=Fonts.BODY_BOLD,
            text_color=Colors.TEXT_PRIMARY,
        ).pack(padx=20, pady=12)

        # ── Charts Grid ──────────────────────────────────────────────
        charts_frame = ctk.CTkFrame(self._content_frame, fg_color="transparent")
        charts_frame.pack(fill="both", expand=True)
        charts_frame.columnconfigure((0, 1), weight=1, uniform="chart")

        # Confusion Matrix
        self._embed_chart(
            charts_frame, metrics["confusion_fig"],
            "Confusion Matrix", row=0, col=0,
        )

        # ROC Curve
        self._embed_chart(
            charts_frame, metrics["roc_fig"],
            "ROC Curve", row=0, col=1,
        )

        # Feature Importance (full width)
        self._embed_chart(
            charts_frame, metrics["importance_fig"],
            "Feature Importance", row=1, col=0, colspan=2,
        )

    def _embed_chart(
        self, parent, fig, title: str,
        row: int, col: int, colspan: int = 1,
    ) -> None:
        """Embed a matplotlib figure in a card frame."""
        card = ctk.CTkFrame(
            parent, fg_color=Colors.CARD,
            corner_radius=12, border_width=1,
            border_color=Colors.BORDER_LIGHT,
        )
        card.grid(
            row=row, column=col, columnspan=colspan,
            padx=4, pady=4, sticky="nsew",
        )

        # Resize figure to fit
        fig.set_size_inches(6, 4.5)
        fig.set_facecolor(Colors.CARD)
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=card)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=8, pady=8)

    def _show_error(self, message: str) -> None:
        """Display error message."""
        for w in self._content_frame.winfo_children():
            w.destroy()

        ctk.CTkLabel(
            self._content_frame, text=f"❌  {message}",
            font=Fonts.BODY, text_color=Colors.DANGER,
        ).pack(pady=40)

    def get_metrics(self) -> Optional[dict]:
        """Return cached metrics dict for report generation."""
        return self._metrics
