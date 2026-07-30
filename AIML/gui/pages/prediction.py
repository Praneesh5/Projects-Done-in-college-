"""
gui/pages/prediction.py — Patient Prediction Page
==================================================
Professional input form for 13 clinical features with:
    - Dropdowns for categorical features
    - Spinboxes for numeric features
    - Input validation with error highlighting
    - Tooltips explaining each field
    - Animated result card with risk gauge
    - Clinical recommendation panel

This is the primary user-facing page of the application.
"""

import logging
import threading
from typing import Optional

import customtkinter as ctk
import numpy as np

from gui.theme import Colors, Fonts, Spacing, Icons
from gui.components import (
    SectionHeader, AnimatedButton, RiskGauge,
    LoadingOverlay, ToolTip,
)
from core.utils import (
    FEATURE_COLUMNS, FEATURE_DISPLAY_NAMES,
    CATEGORICAL_LABELS, FEATURE_RANGES,
    validate_all_inputs,
)

logger = logging.getLogger("HealthcareAI.pages.prediction")


# ─────────────────────────────────────────────────────────────────────
# TOOLTIPS for each feature field
# ─────────────────────────────────────────────────────────────────────

FIELD_TOOLTIPS = {
    "age":      "Patient's age in years (29–77 typical range)",
    "sex":      "0 = Female, 1 = Male",
    "cp":       "0 = Typical Angina, 1 = Atypical, 2 = Non-anginal, 3 = Asymptomatic",
    "trestbps": "Resting blood pressure in mm Hg (94–200 typical)",
    "chol":     "Serum cholesterol in mg/dl (126–564 typical)",
    "fbs":      "Fasting blood sugar > 120 mg/dl: 0 = No, 1 = Yes",
    "restecg":  "0 = Normal, 1 = ST-T abnormality, 2 = LV hypertrophy",
    "thalach":  "Maximum heart rate achieved (71–202 typical)",
    "exang":    "Exercise induced angina: 0 = No, 1 = Yes",
    "oldpeak":  "ST depression induced by exercise (0.0–6.2 typical)",
    "slope":    "Slope of peak exercise ST: 0 = Up, 1 = Flat, 2 = Down",
    "ca":       "Number of major vessels colored by fluoroscopy (0–4)",
    "thal":     "0 = Normal, 1 = Fixed defect, 2 = Reversible, 3 = Thalassemia",
}


class PredictionPage(ctk.CTkFrame):
    """Patient prediction page with input form and result display."""

    def __init__(self, parent, app_ref=None, **kwargs):
        super().__init__(parent, fg_color=Colors.BACKGROUND, **kwargs)

        self._app_ref = app_ref
        self._inputs: dict[str, ctk.CTkWidget] = {}
        self._error_labels: dict[str, ctk.CTkLabel] = {}
        self._result_frame: Optional[ctk.CTkFrame] = None
        self._last_result = None
        self._gauge: Optional[RiskGauge] = None

        self._build_ui()

    def _build_ui(self) -> None:
        """Build the prediction page layout."""
        pad = Spacing.CONTENT_PAD

        # Main scrollable area
        self._scroll = ctk.CTkScrollableFrame(
            self, fg_color=Colors.BACKGROUND,
            scrollbar_button_color=Colors.BORDER,
        )
        self._scroll.pack(fill="both", expand=True)

        # Page header
        SectionHeader(
            self._scroll,
            title=f"{Icons.PREDICTION}  Patient Heart Disease Prediction",
            subtitle="Enter clinical parameters to predict heart disease risk",
        ).pack(fill="x", padx=pad, pady=(pad, 12))

        # Two-column layout: form left, result right
        self._content = ctk.CTkFrame(self._scroll, fg_color="transparent")
        self._content.pack(fill="both", expand=True, padx=pad, pady=(0, pad))
        self._content.columnconfigure(0, weight=3)
        self._content.columnconfigure(1, weight=2)

        # ── Left: Input Form ─────────────────────────────────────────
        self._build_form()

        # ── Right: Result Panel (initially empty) ─────────────────────
        self._result_container = ctk.CTkFrame(
            self._content, fg_color="transparent",
        )
        self._result_container.grid(row=0, column=1, sticky="nsew", padx=(12, 0))

        self._build_empty_result()

        # Loading overlay
        self._loading = LoadingOverlay(self, message="Running prediction...")

    def _build_form(self) -> None:
        """Build the input form with all 13 fields."""
        form_card = ctk.CTkFrame(
            self._content, fg_color=Colors.CARD,
            corner_radius=12, border_width=1,
            border_color=Colors.BORDER_LIGHT,
        )
        form_card.grid(row=0, column=0, sticky="nsew")

        form_inner = ctk.CTkFrame(form_card, fg_color="transparent")
        form_inner.pack(fill="both", expand=True, padx=20, pady=16)

        ctk.CTkLabel(
            form_inner,
            text="Clinical Parameters",
            font=Fonts.HEADING_3,
            text_color=Colors.TEXT_PRIMARY,
        ).pack(anchor="w", pady=(0, 4))

        ctk.CTkLabel(
            form_inner,
            text="All fields are required. Hover over labels for guidance.",
            font=Fonts.CAPTION,
            text_color=Colors.TEXT_MUTED,
        ).pack(anchor="w", pady=(0, 12))

        # Build fields in a 2-column grid
        fields_frame = ctk.CTkFrame(form_inner, fg_color="transparent")
        fields_frame.pack(fill="x")
        fields_frame.columnconfigure((0, 1), weight=1, uniform="field")

        # Field definitions: (key, type, options/range)
        field_defs = [
            ("age",      "spinbox",  (29, 120)),
            ("sex",      "dropdown", {0: "Female", 1: "Male"}),
            ("cp",       "dropdown", {0: "Typical Angina", 1: "Atypical Angina",
                                      2: "Non-anginal Pain", 3: "Asymptomatic"}),
            ("trestbps", "spinbox",  (50, 250)),
            ("chol",     "spinbox",  (50, 700)),
            ("fbs",      "dropdown", {0: "≤ 120 mg/dl (Normal)", 1: "> 120 mg/dl (High)"}),
            ("restecg",  "dropdown", {0: "Normal", 1: "ST-T Abnormality",
                                      2: "LV Hypertrophy"}),
            ("thalach",  "spinbox",  (50, 250)),
            ("exang",    "dropdown", {0: "No", 1: "Yes"}),
            ("oldpeak",  "entry",    (0.0, 10.0)),
            ("slope",    "dropdown", {0: "Upsloping", 1: "Flat", 2: "Downsloping"}),
            ("ca",       "dropdown", {0: "0", 1: "1", 2: "2", 3: "3", 4: "4"}),
            ("thal",     "dropdown", {0: "Normal", 1: "Fixed Defect",
                                      2: "Reversible Defect", 3: "Thalassemia"}),
        ]

        for idx, (key, ftype, options) in enumerate(field_defs):
            row = idx // 2
            col = idx % 2

            field_frame = ctk.CTkFrame(fields_frame, fg_color="transparent")
            field_frame.grid(row=row, column=col, padx=6, pady=4, sticky="ew")

            # Label with required indicator
            display_name = FEATURE_DISPLAY_NAMES.get(key, key)
            label = ctk.CTkLabel(
                field_frame,
                text=f"{display_name} *",
                font=Fonts.SMALL_BOLD,
                text_color=Colors.TEXT_PRIMARY,
            )
            label.pack(anchor="w")
            ToolTip(label, FIELD_TOOLTIPS.get(key, ""))

            # Input widget
            if ftype == "dropdown":
                # Build values list preserving order
                values_map = options
                display_values = [f"{v}" for v in values_map.values()]
                widget = ctk.CTkComboBox(
                    field_frame,
                    values=display_values,
                    font=Fonts.BODY,
                    dropdown_font=Fonts.BODY,
                    height=Spacing.INPUT_HEIGHT,
                    corner_radius=Spacing.INPUT_RADIUS,
                    border_color=Colors.BORDER,
                    button_color=Colors.PRIMARY,
                    state="readonly",
                )
                widget.set(display_values[0])
                widget._values_map = values_map  # Store mapping
                widget._field_type = "dropdown"
                self._inputs[key] = widget

            elif ftype == "spinbox":
                lo, hi = options
                var = ctk.StringVar(value=str(lo))
                widget = ctk.CTkEntry(
                    field_frame,
                    textvariable=var,
                    font=Fonts.BODY,
                    height=Spacing.INPUT_HEIGHT,
                    corner_radius=Spacing.INPUT_RADIUS,
                    border_color=Colors.BORDER,
                    placeholder_text=f"{lo}–{hi}",
                )
                widget._var = var
                widget._field_type = "spinbox"
                widget._range = (lo, hi)
                self._inputs[key] = widget

            elif ftype == "entry":
                lo, hi = options
                var = ctk.StringVar(value=str(lo))
                widget = ctk.CTkEntry(
                    field_frame,
                    textvariable=var,
                    font=Fonts.BODY,
                    height=Spacing.INPUT_HEIGHT,
                    corner_radius=Spacing.INPUT_RADIUS,
                    border_color=Colors.BORDER,
                    placeholder_text=f"{lo}–{hi}",
                )
                widget._var = var
                widget._field_type = "entry"
                self._inputs[key] = widget

            widget.pack(fill="x", pady=(2, 0))

            # Error label (hidden by default)
            err_label = ctk.CTkLabel(
                field_frame, text="",
                font=Fonts.CAPTION,
                text_color=Colors.DANGER,
                anchor="w",
            )
            err_label.pack(anchor="w")
            self._error_labels[key] = err_label

        # ── Action Buttons ────────────────────────────────────────────
        btn_frame = ctk.CTkFrame(form_inner, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(16, 0))

        AnimatedButton(
            btn_frame,
            text="Predict",
            icon=Icons.HEART,
            color=Colors.PRIMARY,
            hover_color=Colors.PRIMARY_HOVER,
            width=180, height=44,
            command=self._on_predict,
        ).pack(side="left", padx=(0, 8))

        AnimatedButton(
            btn_frame,
            text="Clear",
            icon=Icons.REFRESH,
            color=Colors.TEXT_MUTED,
            hover_color=Colors.TEXT_SECONDARY,
            width=120, height=44,
            command=self._on_clear,
        ).pack(side="left", padx=(0, 8))

        AnimatedButton(
            btn_frame,
            text="Sample Data",
            icon=Icons.SPARKLE,
            color=Colors.INFO,
            hover_color=Colors.PRIMARY_DARK,
            width=160, height=44,
            command=self._fill_sample,
        ).pack(side="left")

    def _build_empty_result(self) -> None:
        """Show a placeholder in the result area."""
        for w in self._result_container.winfo_children():
            w.destroy()

        card = ctk.CTkFrame(
            self._result_container, fg_color=Colors.CARD,
            corner_radius=12, border_width=1,
            border_color=Colors.BORDER_LIGHT,
        )
        card.pack(fill="both", expand=True)

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(
            inner, text="🩺", font=("Segoe UI Emoji", 48),
        ).pack(pady=(0, 8))

        ctk.CTkLabel(
            inner, text="Prediction Result",
            font=Fonts.HEADING_2,
            text_color=Colors.TEXT_PRIMARY,
        ).pack()

        ctk.CTkLabel(
            inner, text="Enter patient data and click 'Predict'\nto see the results here.",
            font=Fonts.BODY,
            text_color=Colors.TEXT_MUTED,
            justify="center",
        ).pack(pady=(4, 0))

    def _get_input_values(self) -> dict[str, float]:
        """Extract numeric values from all input widgets."""
        values = {}
        for key, widget in self._inputs.items():
            if hasattr(widget, "_field_type") and widget._field_type == "dropdown":
                # Reverse-lookup the numeric key from display value
                current = widget.get()
                found = False
                for num_val, label in widget._values_map.items():
                    if label == current:
                        values[key] = float(num_val)
                        found = True
                        break
                if not found:
                    values[key] = None
            else:
                try:
                    raw = widget.get() if hasattr(widget, 'get') else widget._var.get()
                    values[key] = float(raw) if raw.strip() else None
                except (ValueError, AttributeError):
                    values[key] = None
        return values

    def _clear_errors(self) -> None:
        """Clear all error messages and reset field borders."""
        for key, label in self._error_labels.items():
            label.configure(text="")
        for key, widget in self._inputs.items():
            try:
                widget.configure(border_color=Colors.BORDER)
            except Exception:
                pass

    def _show_errors(self, errors: list[str]) -> None:
        """Highlight invalid fields and show error messages."""
        for err in errors:
            # Find the matching field by display name
            for key in FEATURE_COLUMNS:
                display = FEATURE_DISPLAY_NAMES.get(key, key)
                if display in err:
                    self._error_labels[key].configure(text=err)
                    try:
                        self._inputs[key].configure(border_color=Colors.DANGER)
                    except Exception:
                        pass
                    break

    def _on_predict(self) -> None:
        """Handle the Predict button click."""
        self._clear_errors()

        values = self._get_input_values()

        # Validate
        valid, errors = validate_all_inputs(values)
        if not valid:
            self._show_errors(errors)
            return

        # Show loading overlay and run prediction in background
        self._loading.show()

        def do_prediction():
            try:
                from core.predict import predict_heart_disease
                result = predict_heart_disease(values)
                self.after(0, lambda: self._show_result(result))
            except Exception as e:
                logger.exception("Prediction failed: %s", e)
                self.after(0, lambda: self._show_error(str(e)))
            finally:
                self.after(0, self._loading.hide)

        threading.Thread(target=do_prediction, daemon=True).start()

    def _show_result(self, result) -> None:
        """Display the prediction result in the right panel."""
        self._last_result = result

        if not result.success:
            self._show_error(result.error_message)
            return

        # Clear result container
        for w in self._result_container.winfo_children():
            w.destroy()

        # Result card
        card = ctk.CTkFrame(
            self._result_container, fg_color=Colors.CARD,
            corner_radius=12, border_width=1,
            border_color=Colors.BORDER_LIGHT,
        )
        card.pack(fill="both", expand=True)

        scroll = ctk.CTkScrollableFrame(card, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=4, pady=4)

        inner = ctk.CTkFrame(scroll, fg_color="transparent")
        inner.pack(fill="x", padx=16, pady=12)

        # Prediction label
        pred_color = Colors.DANGER if result.prediction == 1 else Colors.SUCCESS
        pred_icon = "⚠️" if result.prediction == 1 else "✅"

        ctk.CTkLabel(
            inner, text=f"{pred_icon}  {result.prediction_label}",
            font=Fonts.HEADING_2,
            text_color=pred_color,
        ).pack(anchor="w", pady=(0, 8))

        # Probability and confidence
        stats_frame = ctk.CTkFrame(inner, fg_color="transparent")
        stats_frame.pack(fill="x", pady=(0, 8))
        stats_frame.columnconfigure((0, 1), weight=1)

        for col, (label, val) in enumerate([
            ("Disease Probability", result.probability_pct),
            ("Model Confidence", result.confidence_pct),
        ]):
            box = ctk.CTkFrame(
                stats_frame, fg_color=Colors.BACKGROUND,
                corner_radius=8,
            )
            box.grid(row=0, column=col, padx=4, pady=4, sticky="ew")

            ctk.CTkLabel(
                box, text=val, font=Fonts.HEADING_1,
                text_color=Colors.TEXT_PRIMARY,
            ).pack(padx=12, pady=(8, 2))

            ctk.CTkLabel(
                box, text=label, font=Fonts.CAPTION,
                text_color=Colors.TEXT_MUTED,
            ).pack(padx=12, pady=(0, 8))

        # Risk category badge
        risk_frame = ctk.CTkFrame(
            inner, fg_color=result.risk_color,
            corner_radius=8,
        )
        risk_frame.pack(fill="x", pady=8)
        ctk.CTkLabel(
            risk_frame,
            text=f"  {Icons.SHIELD}  Risk Level: {result.risk_category.upper()}  ",
            font=Fonts.HEADING_3,
            text_color=Colors.TEXT_WHITE,
        ).pack(padx=16, pady=10)

        # Risk gauge
        gauge_frame = ctk.CTkFrame(inner, fg_color="transparent")
        gauge_frame.pack(pady=8)
        self._gauge = RiskGauge(gauge_frame, size=220)
        self._gauge.pack()
        self._gauge.set_value(result.probability, animated=True)

        # Clinical recommendation
        ctk.CTkLabel(
            inner, text="Clinical Recommendation",
            font=Fonts.HEADING_3,
            text_color=Colors.TEXT_PRIMARY,
        ).pack(anchor="w", pady=(12, 4))

        rec_frame = ctk.CTkFrame(
            inner, fg_color=Colors.BACKGROUND, corner_radius=8,
        )
        rec_frame.pack(fill="x", pady=(0, 8))

        ctk.CTkLabel(
            rec_frame, text=result.recommendation,
            font=Fonts.SMALL,
            text_color=Colors.TEXT_SECONDARY,
            wraplength=320, justify="left", anchor="nw",
        ).pack(fill="x", padx=12, pady=10)

        logger.info("Result displayed: %s", result.prediction_label)

    def _show_error(self, message: str) -> None:
        """Display an error message in the result panel."""
        for w in self._result_container.winfo_children():
            w.destroy()

        card = ctk.CTkFrame(
            self._result_container, fg_color=Colors.CARD,
            corner_radius=12, border_width=1,
            border_color=Colors.DANGER,
        )
        card.pack(fill="both", expand=True)

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(inner, text="❌", font=("Segoe UI Emoji", 36)).pack()
        ctk.CTkLabel(
            inner, text="Prediction Error",
            font=Fonts.HEADING_2, text_color=Colors.DANGER,
        ).pack(pady=(4, 8))
        ctk.CTkLabel(
            inner, text=message, font=Fonts.BODY,
            text_color=Colors.TEXT_SECONDARY,
            wraplength=300, justify="center",
        ).pack()

    def _on_clear(self) -> None:
        """Reset all input fields and clear results."""
        self._clear_errors()
        for key, widget in self._inputs.items():
            if hasattr(widget, "_field_type") and widget._field_type == "dropdown":
                first_val = list(widget._values_map.values())[0]
                widget.set(first_val)
            elif hasattr(widget, "_var"):
                if hasattr(widget, "_range"):
                    widget._var.set(str(widget._range[0]))
                else:
                    widget._var.set("0.0")
        self._build_empty_result()
        self._last_result = None

    def _fill_sample(self) -> None:
        """Fill the form with sample patient data for demonstration."""
        sample = {
            "age": 55, "sex": 1, "cp": 0, "trestbps": 140,
            "chol": 260, "fbs": 0, "restecg": 1, "thalach": 145,
            "exang": 1, "oldpeak": 2.0, "slope": 1, "ca": 1, "thal": 2,
        }
        for key, val in sample.items():
            widget = self._inputs.get(key)
            if widget is None:
                continue
            if hasattr(widget, "_field_type") and widget._field_type == "dropdown":
                label = widget._values_map.get(int(val), "")
                if label:
                    widget.set(label)
            elif hasattr(widget, "_var"):
                widget._var.set(str(val))

    def get_last_result(self):
        """Return the most recent PredictionResult (for reports/SHAP/LIME)."""
        return self._last_result

    def get_last_inputs(self) -> Optional[dict]:
        """Return the most recent input values."""
        if self._last_result and self._last_result.success:
            return self._last_result.feature_values
        return None
