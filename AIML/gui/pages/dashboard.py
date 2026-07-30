"""
gui/pages/dashboard.py — Dashboard Overview Page
=================================================
The landing page of the application showing:
    - Welcome header with project title
    - 4 metric summary cards (accuracy, features, model type, dataset)
    - Quick action buttons for navigation
    - System status indicators

This page loads metrics on first display and caches them.
"""

import logging
from typing import Optional

import customtkinter as ctk

from gui.theme import Colors, Fonts, Spacing, Icons
from gui.components import MetricCard, SectionHeader, AnimatedButton

logger = logging.getLogger("HealthcareAI.pages.dashboard")


class DashboardPage(ctk.CTkFrame):
    """Main dashboard overview page."""

    def __init__(self, parent, navigate_callback=None, **kwargs):
        super().__init__(parent, fg_color=Colors.BACKGROUND, **kwargs)

        self._navigate = navigate_callback
        self._build_ui()

    def _build_ui(self) -> None:
        """Construct the dashboard layout."""
        pad = Spacing.CONTENT_PAD

        # Scrollable container
        scroll = ctk.CTkScrollableFrame(
            self, fg_color=Colors.BACKGROUND,
            scrollbar_button_color=Colors.BORDER,
        )
        scroll.pack(fill="both", expand=True, padx=0, pady=0)

        # ── Welcome Header ───────────────────────────────────────────
        header_frame = ctk.CTkFrame(scroll, fg_color=Colors.PRIMARY, corner_radius=12)
        header_frame.pack(fill="x", padx=pad, pady=(pad, 12))

        header_inner = ctk.CTkFrame(header_frame, fg_color="transparent")
        header_inner.pack(fill="x", padx=24, pady=20)

        ctk.CTkLabel(
            header_inner,
            text=f"{Icons.BRAIN}  Welcome to the Healthcare AI Dashboard",
            font=Fonts.HEADING_1,
            text_color=Colors.TEXT_WHITE,
            anchor="w",
        ).pack(anchor="w")

        ctk.CTkLabel(
            header_inner,
            text="Model Interpretability in Clinical ML using SHAP & LIME",
            font=Fonts.BODY,
            text_color="#BFDBFE",
            anchor="w",
        ).pack(anchor="w", pady=(4, 0))

        ctk.CTkLabel(
            header_inner,
            text="Explainable AI for Heart Disease Prediction",
            font=Fonts.CAPTION,
            text_color="#93C5FD",
            anchor="w",
        ).pack(anchor="w", pady=(2, 0))

        # ── Metric Cards Row ─────────────────────────────────────────
        SectionHeader(
            scroll, title="Model Overview",
            subtitle="Key statistics from the trained model",
        ).pack(fill="x", padx=pad, pady=(16, 8))

        cards_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        cards_frame.pack(fill="x", padx=pad, pady=(0, 12))
        cards_frame.columnconfigure((0, 1, 2, 3), weight=1, uniform="card")

        self._cards = {}

        card_configs = [
            {
                "key": "accuracy", "title": "Model Accuracy",
                "value": "—", "icon": Icons.CHART,
                "subtitle": "Test set evaluation",
                "accent": Colors.SUCCESS, "col": 0,
            },
            {
                "key": "features", "title": "Clinical Features",
                "value": "13", "icon": Icons.SEARCH,
                "subtitle": "Heart disease indicators",
                "accent": Colors.PRIMARY, "col": 1,
            },
            {
                "key": "model", "title": "Model Type",
                "value": "GBM", "icon": Icons.BRAIN,
                "subtitle": "Gradient Boosting Machine",
                "accent": Colors.INFO, "col": 2,
            },
            {
                "key": "dataset", "title": "Dataset Size",
                "value": "302", "icon": Icons.USER,
                "subtitle": "Cleaned patient records",
                "accent": Colors.WARNING, "col": 3,
            },
        ]

        for cfg in card_configs:
            card = MetricCard(
                cards_frame,
                title=cfg["title"],
                value=cfg["value"],
                icon=cfg["icon"],
                subtitle=cfg["subtitle"],
                accent_color=cfg["accent"],
            )
            card.grid(
                row=0, column=cfg["col"],
                padx=6, pady=6, sticky="nsew",
            )
            self._cards[cfg["key"]] = card

        # ── Quick Actions ─────────────────────────────────────────────
        SectionHeader(
            scroll, title="Quick Actions",
            subtitle="Navigate to key features",
        ).pack(fill="x", padx=pad, pady=(16, 8))

        actions_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        actions_frame.pack(fill="x", padx=pad, pady=(0, 12))

        actions = [
            ("🩺  Run Prediction", "prediction", Colors.PRIMARY),
            ("📈  View Performance", "performance", Colors.SUCCESS),
            ("🔬  SHAP Analysis", "shap", "#7C3AED"),
            ("🧪  LIME Analysis", "lime", Colors.WARNING),
            ("📄  Generate Report", "reports", Colors.DANGER),
        ]

        for i, (text, key, color) in enumerate(actions):
            btn = AnimatedButton(
                actions_frame,
                text=text,
                color=color,
                hover_color=Colors.PRIMARY_DARK,
                width=200,
                height=44,
                command=lambda k=key: self._navigate(k) if self._navigate else None,
            )
            btn.grid(row=0, column=i, padx=6, pady=6)

        # ── About Section ────────────────────────────────────────────
        SectionHeader(
            scroll, title="About This System",
            subtitle="Academic research project",
        ).pack(fill="x", padx=pad, pady=(16, 8))

        about_card = ctk.CTkFrame(
            scroll, fg_color=Colors.CARD,
            corner_radius=12, border_width=1,
            border_color=Colors.BORDER_LIGHT,
        )
        about_card.pack(fill="x", padx=pad, pady=(0, pad))

        about_text = (
            "This application demonstrates Model Interpretability in Clinical Machine Learning "
            "using SHAP (SHapley Additive exPlanations) and LIME (Local Interpretable Model-agnostic "
            "Explanations) to provide transparent, explainable predictions for heart disease risk.\n\n"
            "The system uses a Gradient Boosting Classifier trained on the UCI Heart Disease dataset "
            "with 13 clinical features. SHAP provides global and local feature importance through "
            "exact Shapley values, while LIME offers intuitive local explanations by fitting "
            "interpretable surrogate models around individual predictions.\n\n"
            "Designed to support academic research, clinical decision support demonstration, "
            "and portfolio presentation for Explainable AI in Healthcare."
        )

        ctk.CTkLabel(
            about_card, text=about_text, font=Fonts.BODY,
            text_color=Colors.TEXT_SECONDARY,
            wraplength=800, justify="left", anchor="nw",
        ).pack(fill="x", padx=20, pady=16)

    def load_metrics(self) -> None:
        """Load and display model accuracy from saved artifacts."""
        try:
            from core.charts import compute_all_metrics
            metrics = compute_all_metrics()
            if metrics:
                acc = f"{metrics['accuracy'] * 100:.1f}%"
                # Update the accuracy card value
                for child in self._cards["accuracy"].winfo_children():
                    if isinstance(child, ctk.CTkFrame):
                        for sub in child.winfo_children():
                            if isinstance(sub, ctk.CTkLabel):
                                try:
                                    f = sub.cget("font")
                                    if f == Fonts.METRIC_VALUE:
                                        sub.configure(text=acc)
                                        return
                                except Exception:
                                    pass
        except Exception as e:
            logger.warning("Could not load dashboard metrics: %s", e)
