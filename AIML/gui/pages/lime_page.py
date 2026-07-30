"""
gui/pages/lime_page.py — LIME Explainability Page
=================================================
Provides LIME (Local Interpretable Model-agnostic Explanations)
for individual patient predictions:
    - Feature contribution bar chart
    - Feature weight table (positive/negative contributions)
    - Plain-English explanation panel
    - Local model fidelity score

Requires a prediction to be run first via the Prediction page.
"""

import logging
import threading
from typing import Optional

import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from gui.theme import Colors, Fonts, Spacing, Icons
from gui.components import SectionHeader, AnimatedButton, LoadingOverlay

logger = logging.getLogger("HealthcareAI.pages.lime_page")


class LIMEPage(ctk.CTkFrame):
    """LIME interpretability analysis page."""

    def __init__(self, parent, app_ref=None, **kwargs):
        super().__init__(parent, fg_color=Colors.BACKGROUND, **kwargs)

        self._app_ref = app_ref
        self._explainer = None
        self._current_result = None
        self._current_figure = None
        self._build_ui()

    def _build_ui(self) -> None:
        """Build the LIME page layout."""
        pad = Spacing.CONTENT_PAD

        self._scroll = ctk.CTkScrollableFrame(
            self, fg_color=Colors.BACKGROUND,
            scrollbar_button_color=Colors.BORDER,
        )
        self._scroll.pack(fill="both", expand=True)

        SectionHeader(
            self._scroll,
            title=f"{Icons.LIME}  LIME Explainability Analysis",
            subtitle="Local Interpretable Model-agnostic Explanations",
        ).pack(fill="x", padx=pad, pady=(pad, 12))

        # ── Action Bar ────────────────────────────────────────────────
        action_frame = ctk.CTkFrame(self._scroll, fg_color="transparent")
        action_frame.pack(fill="x", padx=pad, pady=(0, 12))

        AnimatedButton(
            action_frame,
            text="Generate LIME Explanation",
            icon=Icons.LIME,
            color=Colors.PRIMARY,
            hover_color=Colors.PRIMARY_HOVER,
            width=250, height=42,
            command=self._generate_explanation,
        ).pack(side="left", padx=(0, 8))

        ctk.CTkLabel(
            action_frame,
            text="Requires a patient prediction to be run first.",
            font=Fonts.CAPTION,
            text_color=Colors.TEXT_MUTED,
        ).pack(side="left", padx=8)

        # ── Content: Chart + Table + Explanation ──────────────────────
        self._content_frame = ctk.CTkFrame(self._scroll, fg_color="transparent")
        self._content_frame.pack(fill="both", expand=True, padx=pad, pady=(0, pad))

        # Initial placeholder
        self._show_placeholder()

        # Loading overlay
        self._loading = LoadingOverlay(self, message="Generating LIME explanation...")

    def _show_placeholder(self) -> None:
        """Show placeholder when no explanation is available."""
        for w in self._content_frame.winfo_children():
            w.destroy()

        card = ctk.CTkFrame(
            self._content_frame, fg_color=Colors.CARD,
            corner_radius=12, border_width=1,
            border_color=Colors.BORDER_LIGHT,
        )
        card.pack(fill="both", expand=True, pady=8)

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(
            inner, text="🧪", font=("Segoe UI Emoji", 48),
        ).pack(pady=(0, 8))

        ctk.CTkLabel(
            inner, text="LIME Explanation",
            font=Fonts.HEADING_2,
            text_color=Colors.TEXT_PRIMARY,
        ).pack()

        ctk.CTkLabel(
            inner,
            text="Run a patient prediction first, then click\n"
                 "'Generate LIME Explanation' to see local interpretability.",
            font=Fonts.BODY,
            text_color=Colors.TEXT_MUTED,
            justify="center",
        ).pack(pady=(4, 0))

    def _generate_explanation(self) -> None:
        """Generate LIME explanation for the most recent prediction."""
        if self._app_ref is None:
            return

        pred_page = self._app_ref.get_page("prediction")
        if pred_page is None:
            return

        result = pred_page.get_last_result()
        if result is None or not result.success:
            self._show_error(
                "No prediction available. Please run a patient prediction first."
            )
            return

        self._loading.show()

        def compute():
            try:
                from core.lime_explainer import LIMEExplainer
                if self._explainer is None:
                    self._explainer = LIMEExplainer()

                lime_result = self._explainer.explain(result.scaled_values)
                if lime_result:
                    self._current_result = lime_result
                    self.after(0, lambda: self._display_result(lime_result, result))
                else:
                    self.after(0, lambda: self._show_error(
                        "LIME explanation generation failed."
                    ))
            except Exception as e:
                logger.exception("LIME generation failed: %s", e)
                self.after(0, lambda: self._show_error(str(e)))
            finally:
                self.after(0, self._loading.hide)

        threading.Thread(target=compute, daemon=True).start()

    def _display_result(self, lime_result: dict, pred_result) -> None:
        """Display LIME chart, table, and explanation."""
        for w in self._content_frame.winfo_children():
            w.destroy()

        # ── Chart ─────────────────────────────────────────────────────
        chart_card = ctk.CTkFrame(
            self._content_frame, fg_color=Colors.CARD,
            corner_radius=12, border_width=1,
            border_color=Colors.BORDER_LIGHT,
        )
        chart_card.pack(fill="x", pady=(0, 12))

        fig = lime_result["figure"]
        fig.set_size_inches(10, 6)
        fig.set_facecolor(Colors.CARD)
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=chart_card)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=8, pady=8)
        self._current_figure = fig

        # ── Feature Weight Table ──────────────────────────────────────
        table_card = ctk.CTkFrame(
            self._content_frame, fg_color=Colors.CARD,
            corner_radius=12, border_width=1,
            border_color=Colors.BORDER_LIGHT,
        )
        table_card.pack(fill="x", pady=(0, 12))

        ctk.CTkLabel(
            table_card,
            text="📋  Feature Contribution Table",
            font=Fonts.HEADING_3,
            text_color=Colors.TEXT_PRIMARY,
            anchor="w",
        ).pack(fill="x", padx=16, pady=(12, 8))

        # Table header
        header_frame = ctk.CTkFrame(table_card, fg_color=Colors.PRIMARY, corner_radius=4)
        header_frame.pack(fill="x", padx=16, pady=(0, 2))
        header_frame.columnconfigure(0, weight=3)
        header_frame.columnconfigure(1, weight=1)
        header_frame.columnconfigure(2, weight=1)

        for col, text in enumerate(["Feature", "Weight", "Direction"]):
            ctk.CTkLabel(
                header_frame, text=text, font=Fonts.SMALL_BOLD,
                text_color=Colors.TEXT_WHITE,
            ).grid(row=0, column=col, padx=8, pady=6, sticky="w")

        # Table rows
        table_data = lime_result["table"]
        sorted_data = sorted(table_data, key=lambda x: -abs(x[1]))

        for i, (feat, weight, direction) in enumerate(sorted_data):
            row_bg = Colors.BACKGROUND if i % 2 == 0 else Colors.CARD
            dir_color = Colors.DANGER if direction == "Positive" else Colors.PRIMARY
            dir_icon = "▲" if direction == "Positive" else "▼"

            row_frame = ctk.CTkFrame(table_card, fg_color=row_bg, corner_radius=0, height=32)
            row_frame.pack(fill="x", padx=16, pady=0)
            row_frame.columnconfigure(0, weight=3)
            row_frame.columnconfigure(1, weight=1)
            row_frame.columnconfigure(2, weight=1)
            row_frame.pack_propagate(False)

            ctk.CTkLabel(
                row_frame, text=feat[:50], font=Fonts.SMALL,
                text_color=Colors.TEXT_PRIMARY, anchor="w",
            ).grid(row=0, column=0, padx=8, pady=4, sticky="w")

            ctk.CTkLabel(
                row_frame, text=f"{weight:+.4f}", font=Fonts.MONO if hasattr(Fonts, 'MONO') else Fonts.SMALL,
                text_color=Colors.TEXT_PRIMARY, anchor="w",
            ).grid(row=0, column=1, padx=8, pady=4, sticky="w")

            ctk.CTkLabel(
                row_frame, text=f"{dir_icon} {direction}", font=Fonts.SMALL_BOLD,
                text_color=dir_color, anchor="w",
            ).grid(row=0, column=2, padx=8, pady=4, sticky="w")

        # Fidelity score
        score = lime_result.get("score", 0)
        ctk.CTkLabel(
            table_card,
            text=f"Local Model Fidelity (R²): {score:.4f}",
            font=Fonts.CAPTION,
            text_color=Colors.TEXT_MUTED,
        ).pack(padx=16, pady=(4, 12))

        # ── Explanation Panel ─────────────────────────────────────────
        exp_card = ctk.CTkFrame(
            self._content_frame, fg_color=Colors.CARD,
            corner_radius=12, border_width=1,
            border_color=Colors.BORDER_LIGHT,
        )
        exp_card.pack(fill="x", pady=(0, 12))

        ctk.CTkLabel(
            exp_card,
            text="📝  Plain-English Explanation",
            font=Fonts.HEADING_3,
            text_color=Colors.TEXT_PRIMARY,
            anchor="w",
        ).pack(fill="x", padx=16, pady=(12, 4))

        ctk.CTkLabel(
            exp_card,
            text=lime_result["explanation"],
            font=Fonts.SMALL,
            text_color=Colors.TEXT_SECONDARY,
            wraplength=900, justify="left", anchor="nw",
        ).pack(fill="x", padx=16, pady=(0, 12))

    def _show_error(self, message: str) -> None:
        """Display error message."""
        for w in self._content_frame.winfo_children():
            w.destroy()

        card = ctk.CTkFrame(
            self._content_frame, fg_color=Colors.CARD,
            corner_radius=12, border_width=1,
            border_color=Colors.DANGER,
        )
        card.pack(fill="both", expand=True, pady=8)

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(inner, text="⚠️", font=("Segoe UI Emoji", 36)).pack()
        ctk.CTkLabel(
            inner, text=message, font=Fonts.BODY,
            text_color=Colors.TEXT_SECONDARY,
            wraplength=400, justify="center",
        ).pack(pady=(8, 0))

    def get_current_figure(self):
        """Return the current LIME figure for export."""
        return self._current_figure

    def get_explanation_text(self) -> str:
        """Return current explanation text for reports."""
        if self._current_result:
            return self._current_result.get("explanation", "")
        return ""
