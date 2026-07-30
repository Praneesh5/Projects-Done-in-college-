"""
gui/pages/about.py — About Page
================================
Displays project information, tech stack, academic context,
and developer credits.
"""

import customtkinter as ctk

from gui.theme import Colors, Fonts, Spacing, Icons
from gui.components import SectionHeader


class AboutPage(ctk.CTkFrame):
    """About / information page."""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color=Colors.BACKGROUND, **kwargs)
        self._build_ui()

    def _build_ui(self) -> None:
        """Build the about page layout."""
        pad = Spacing.CONTENT_PAD

        scroll = ctk.CTkScrollableFrame(
            self, fg_color=Colors.BACKGROUND,
            scrollbar_button_color=Colors.BORDER,
        )
        scroll.pack(fill="both", expand=True)

        # ── Header ────────────────────────────────────────────────────
        header = ctk.CTkFrame(scroll, fg_color=Colors.PRIMARY, corner_radius=12)
        header.pack(fill="x", padx=pad, pady=(pad, 16))

        header_inner = ctk.CTkFrame(header, fg_color="transparent")
        header_inner.pack(fill="x", padx=24, pady=20)

        ctk.CTkLabel(
            header_inner,
            text=f"{Icons.BRAIN}  Model Interpretability in Clinical ML",
            font=Fonts.HEADING_1,
            text_color=Colors.TEXT_WHITE,
        ).pack(anchor="w")

        ctk.CTkLabel(
            header_inner,
            text="Using SHAP & LIME to Ensure Explainable AI in Healthcare",
            font=Fonts.BODY,
            text_color="#BFDBFE",
        ).pack(anchor="w", pady=(4, 0))

        # ── Project Overview ──────────────────────────────────────────
        self._info_card(scroll, "📋  Project Overview", [
            "This application demonstrates how machine learning models can be made",
            "transparent and interpretable in clinical healthcare settings.",
            "",
            "It uses SHAP (SHapley Additive exPlanations) and LIME (Local Interpretable",
            "Model-agnostic Explanations) to provide clear, understandable explanations",
            "for heart disease predictions, supporting the growing need for trustworthy",
            "AI in medical decision-making.",
            "",
            "The system is designed for academic demonstration, research, and portfolio use."
        ])

        # ── Technology Stack ──────────────────────────────────────────
        self._info_card(scroll, "🛠️  Technology Stack", [
            "Language:          Python 3.12",
            "UI Framework:      CustomTkinter + ttkbootstrap",
            "ML Framework:      Scikit-learn (GradientBoostingClassifier)",
            "Interpretability:  SHAP 0.52 (TreeExplainer) + LIME 0.2",
            "Visualization:     Matplotlib",
            "PDF Reports:       ReportLab",
            "Data Handling:     Pandas, NumPy",
            "Model Persistence: Joblib",
            "Packaging:         PyInstaller",
        ])

        # ── Dataset ───────────────────────────────────────────────────
        self._info_card(scroll, "📊  Dataset Information", [
            "Source:     UCI Heart Disease Dataset (Cleveland)",
            "Records:    302 patients (after deduplication)",
            "Features:   13 clinical indicators",
            "Target:     Binary (Heart Disease / No Disease)",
            "Balance:    164 positive / 138 negative",
            "",
            "Clinical features include: age, sex, chest pain type, resting blood",
            "pressure, serum cholesterol, fasting blood sugar, resting ECG,",
            "maximum heart rate, exercise-induced angina, ST depression, ST slope,",
            "number of major vessels, and thalassemia status.",
        ])

        # ── Model Details ─────────────────────────────────────────────
        self._info_card(scroll, "🧠  Model Architecture", [
            "Algorithm:         Gradient Boosting Classifier",
            "Estimators:        200 (with early stopping)",
            "Learning Rate:     0.1",
            "Max Depth:         4",
            "Feature Scaling:   StandardScaler",
            "",
            "Gradient Boosting was chosen for its strong performance on small",
            "tabular datasets and its compatibility with SHAP's TreeExplainer,",
            "which provides exact (not approximate) Shapley values for tree-based",
            "ensemble models.",
        ])

        # ── Explainability ────────────────────────────────────────────
        self._info_card(scroll, "🔬  Explainability Methods", [
            "SHAP (SHapley Additive exPlanations):",
            "  • Based on cooperative game theory (Shapley values)",
            "  • Provides both global and local feature importance",
            "  • TreeExplainer computes exact values for tree ensembles",
            "  • Plots: Summary, Bar, Waterfall, Force, Dependence",
            "",
            "LIME (Local Interpretable Model-agnostic Explanations):",
            "  • Creates local linear approximations around predictions",
            "  • Model-agnostic — works with any classifier",
            "  • Provides intuitive feature weight contributions",
            "  • Shows which features support or contradict the prediction",
        ])

        # ── Credits ───────────────────────────────────────────────────
        self._info_card(scroll, "👤  Credits", [
            "Developer:    Your Name",
            "University:   Your University Name",
            "Department:   Department of Computer Science",
            "Guide:        Your Guide/Professor Name",
            "Version:      1.0.0",
            "",
            "This project was developed as part of an academic research",
            "project on Explainable AI in Healthcare.",
        ])

    def _info_card(self, parent, title: str, lines: list[str]) -> None:
        """Create a styled information card."""
        pad = Spacing.CONTENT_PAD

        card = ctk.CTkFrame(
            parent, fg_color=Colors.CARD,
            corner_radius=12, border_width=1,
            border_color=Colors.BORDER_LIGHT,
        )
        card.pack(fill="x", padx=pad, pady=(0, 12))

        ctk.CTkLabel(
            card, text=title,
            font=Fonts.HEADING_3,
            text_color=Colors.TEXT_PRIMARY,
            anchor="w",
        ).pack(fill="x", padx=20, pady=(16, 8))

        text = "\n".join(lines)
        ctk.CTkLabel(
            card, text=text,
            font=("Consolas", 10) if ":" in lines[0] else Fonts.BODY,
            text_color=Colors.TEXT_SECONDARY,
            wraplength=850, justify="left", anchor="nw",
        ).pack(fill="x", padx=20, pady=(0, 16))
