"""
core/report_generator.py — PDF Report Generator
================================================
Generates professional PDF reports using ReportLab containing:
    - Hospital header (placeholder)
    - Patient inputs with clinical labels
    - Prediction result with probability and risk
    - SHAP interpretation summary
    - LIME interpretation summary
    - Model performance summary
    - Date, time, and footer

Usage:
    from core.report_generator import generate_report
    path = generate_report(prediction_result, shap_text, lime_text, metrics)
"""

import os
import logging
from datetime import datetime
from typing import Optional

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch, mm
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
    PageBreak,
)

from core.predict import PredictionResult, get_formatted_inputs
from core.utils import REPORTS_DIR, get_timestamp

logger = logging.getLogger("HealthcareAI.report_generator")

# ─────────────────────────────────────────────────────────────────────
# COLOR CONSTANTS
# ─────────────────────────────────────────────────────────────────────

PRIMARY = HexColor("#2563EB")
SUCCESS = HexColor("#16A34A")
DANGER = HexColor("#DC2626")
WARNING = HexColor("#F59E0B")
DARK = HexColor("#1F2937")
LIGHT = HexColor("#F5F7FA")
MEDIUM_GRAY = HexColor("#6B7280")


# ─────────────────────────────────────────────────────────────────────
# STYLES
# ─────────────────────────────────────────────────────────────────────

def _get_styles() -> dict:
    """Create custom paragraph styles for the PDF."""
    base = getSampleStyleSheet()

    styles = {
        "title": ParagraphStyle(
            "CustomTitle",
            parent=base["Title"],
            fontSize=20,
            textColor=PRIMARY,
            spaceAfter=6,
            fontName="Helvetica-Bold",
        ),
        "subtitle": ParagraphStyle(
            "CustomSubtitle",
            parent=base["Normal"],
            fontSize=11,
            textColor=MEDIUM_GRAY,
            spaceAfter=12,
            alignment=TA_CENTER,
        ),
        "section": ParagraphStyle(
            "SectionHeader",
            parent=base["Heading2"],
            fontSize=14,
            textColor=PRIMARY,
            spaceBefore=16,
            spaceAfter=8,
            fontName="Helvetica-Bold",
        ),
        "body": ParagraphStyle(
            "BodyText",
            parent=base["Normal"],
            fontSize=10,
            textColor=DARK,
            spaceAfter=4,
            leading=14,
        ),
        "body_bold": ParagraphStyle(
            "BodyBold",
            parent=base["Normal"],
            fontSize=10,
            textColor=DARK,
            fontName="Helvetica-Bold",
            spaceAfter=4,
        ),
        "footer": ParagraphStyle(
            "Footer",
            parent=base["Normal"],
            fontSize=8,
            textColor=MEDIUM_GRAY,
            alignment=TA_CENTER,
        ),
        "risk_high": ParagraphStyle(
            "RiskHigh",
            parent=base["Normal"],
            fontSize=13,
            textColor=DANGER,
            fontName="Helvetica-Bold",
            alignment=TA_CENTER,
        ),
        "risk_medium": ParagraphStyle(
            "RiskMedium",
            parent=base["Normal"],
            fontSize=13,
            textColor=WARNING,
            fontName="Helvetica-Bold",
            alignment=TA_CENTER,
        ),
        "risk_low": ParagraphStyle(
            "RiskLow",
            parent=base["Normal"],
            fontSize=13,
            textColor=SUCCESS,
            fontName="Helvetica-Bold",
            alignment=TA_CENTER,
        ),
    }
    return styles


# ─────────────────────────────────────────────────────────────────────
# REPORT GENERATION
# ─────────────────────────────────────────────────────────────────────

def generate_report(
    result: PredictionResult,
    shap_explanation: str = "",
    lime_explanation: str = "",
    metrics: Optional[dict] = None,
    filename: Optional[str] = None,
) -> Optional[str]:
    """
    Generate a professional PDF report for a patient prediction.

    Args:
        result:           PredictionResult from the prediction engine.
        shap_explanation: Plain-English SHAP interpretation text.
        lime_explanation: Plain-English LIME interpretation text.
        metrics:          Dict of model performance metrics (optional).
        filename:         Custom filename (auto-generated if None).

    Returns:
        Absolute path to the generated PDF, or None on failure.
    """
    if not result.success:
        logger.error("Cannot generate report: prediction was unsuccessful.")
        return None

    # Generate filename with timestamp
    if filename is None:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"patient_report_{ts}.pdf"

    filepath = os.path.join(REPORTS_DIR, filename)
    os.makedirs(REPORTS_DIR, exist_ok=True)

    styles = _get_styles()

    try:
        doc = SimpleDocTemplate(
            filepath,
            pagesize=A4,
            leftMargin=20 * mm,
            rightMargin=20 * mm,
            topMargin=20 * mm,
            bottomMargin=20 * mm,
        )

        elements = []

        # ── Hospital Header ──────────────────────────────────────────
        elements.append(Paragraph(
            "🏥  Your Hospital / Institution Name",
            styles["title"],
        ))
        elements.append(Paragraph(
            "Department of Cardiology — AI-Assisted Diagnostic Report",
            styles["subtitle"],
        ))
        elements.append(HRFlowable(
            width="100%", thickness=2, color=PRIMARY, spaceAfter=12,
        ))

        # ── Report Metadata ──────────────────────────────────────────
        meta_data = [
            ["Report Date:", datetime.now().strftime("%B %d, %Y")],
            ["Report Time:", datetime.now().strftime("%I:%M %p")],
            ["Report ID:", datetime.now().strftime("RPT-%Y%m%d-%H%M%S")],
        ]
        meta_table = Table(meta_data, colWidths=[120, 350])
        meta_table.setStyle(TableStyle([
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("TEXTCOLOR", (0, 0), (0, -1), DARK),
            ("TEXTCOLOR", (1, 0), (1, -1), MEDIUM_GRAY),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]))
        elements.append(meta_table)
        elements.append(Spacer(1, 12))

        # ── Patient Inputs ───────────────────────────────────────────
        elements.append(Paragraph("Patient Clinical Parameters", styles["section"]))

        formatted = get_formatted_inputs(result.feature_values)
        input_data = [["Parameter", "Value"]]
        for _, display_name, value in formatted:
            input_data.append([display_name, str(value)])

        input_table = Table(input_data, colWidths=[240, 230])
        input_table.setStyle(TableStyle([
            # Header row
            ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
            ("TEXTCOLOR", (0, 0), (-1, 0), white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 10),
            ("ALIGN", (0, 0), (-1, 0), "CENTER"),
            # Body
            ("FONTSIZE", (0, 1), (-1, -1), 9),
            ("TEXTCOLOR", (0, 1), (-1, -1), DARK),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, LIGHT]),
            ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#E5E7EB")),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ]))
        elements.append(input_table)
        elements.append(Spacer(1, 16))

        # ── Prediction Result ────────────────────────────────────────
        elements.append(Paragraph("Prediction Result", styles["section"]))

        risk_style_key = f"risk_{result.risk_category.lower()}"
        risk_style = styles.get(risk_style_key, styles["body_bold"])

        elements.append(Paragraph(
            f"<b>Prediction:</b> {result.prediction_label}",
            styles["body"],
        ))
        elements.append(Paragraph(
            f"<b>Disease Probability:</b> {result.probability_pct}",
            styles["body"],
        ))
        elements.append(Paragraph(
            f"<b>Model Confidence:</b> {result.confidence_pct}",
            styles["body"],
        ))
        elements.append(Spacer(1, 6))
        elements.append(Paragraph(
            f"Risk Level: {result.risk_category.upper()} RISK",
            risk_style,
        ))
        elements.append(Spacer(1, 10))

        # Recommendation
        elements.append(Paragraph("Clinical Recommendation", styles["section"]))
        for line in result.recommendation.split("\n"):
            if line.strip():
                elements.append(Paragraph(line.strip(), styles["body"]))
        elements.append(Spacer(1, 12))

        # ── SHAP Interpretation ──────────────────────────────────────
        if shap_explanation:
            elements.append(Paragraph("SHAP Interpretation", styles["section"]))
            for line in shap_explanation.split("\n"):
                if line.strip():
                    elements.append(Paragraph(line.strip(), styles["body"]))
            elements.append(Spacer(1, 12))

        # ── LIME Interpretation ──────────────────────────────────────
        if lime_explanation:
            elements.append(Paragraph("LIME Interpretation", styles["section"]))
            for line in lime_explanation.split("\n"):
                if line.strip():
                    elements.append(Paragraph(line.strip(), styles["body"]))
            elements.append(Spacer(1, 12))

        # ── Model Performance Summary ────────────────────────────────
        if metrics:
            elements.append(Paragraph("Model Performance Summary", styles["section"]))

            perf_data = [
                ["Metric", "Value"],
                ["Accuracy", f"{metrics.get('accuracy', 0):.4f}"],
                ["Precision", f"{metrics.get('precision', 0):.4f}"],
                ["Recall", f"{metrics.get('recall', 0):.4f}"],
                ["F1 Score", f"{metrics.get('f1_score', 0):.4f}"],
                ["ROC AUC", f"{metrics.get('roc_auc', 0):.4f}"],
                ["CV Accuracy", f"{metrics.get('cv_mean', 0):.4f} ± {metrics.get('cv_std', 0):.4f}"],
            ]

            perf_table = Table(perf_data, colWidths=[240, 230])
            perf_table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
                ("TEXTCOLOR", (0, 0), (-1, 0), white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 10),
                ("ALIGN", (0, 0), (-1, 0), "CENTER"),
                ("FONTSIZE", (0, 1), (-1, -1), 9),
                ("TEXTCOLOR", (0, 1), (-1, -1), DARK),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, LIGHT]),
                ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#E5E7EB")),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ]))
            elements.append(perf_table)
            elements.append(Spacer(1, 16))

        # ── Disclaimer ───────────────────────────────────────────────
        elements.append(HRFlowable(
            width="100%", thickness=1, color=MEDIUM_GRAY, spaceAfter=8,
        ))
        elements.append(Paragraph(
            "<b>Disclaimer:</b> This report is generated by an AI-assisted "
            "clinical decision support system for academic and research purposes. "
            "It is NOT a substitute for professional medical diagnosis. "
            "Always consult a qualified healthcare provider for medical decisions.",
            styles["body"],
        ))
        elements.append(Spacer(1, 12))

        # ── Footer ───────────────────────────────────────────────────
        elements.append(HRFlowable(
            width="100%", thickness=1, color=PRIMARY, spaceAfter=6,
        ))
        elements.append(Paragraph(
            "Your University Name — Department of Computer Science",
            styles["footer"],
        ))
        elements.append(Paragraph(
            "Model Interpretability in Clinical ML using SHAP & LIME | v1.0.0",
            styles["footer"],
        ))
        elements.append(Paragraph(
            f"Generated: {get_timestamp()} | Developed by: Your Name",
            styles["footer"],
        ))

        # Build PDF
        doc.build(elements)
        logger.info("PDF report saved: %s", filepath)
        return filepath

    except Exception as e:
        logger.exception("Failed to generate PDF report: %s", e)
        return None
