"""
gui/pages/reports.py — Report Generation & Export Page
======================================================
Provides tools to generate and export:
    - Patient PDF reports
    - SHAP plot images
    - LIME plot images
    - Prediction CSV exports

Lists previously generated reports with file browser.
"""

import os
import logging
import threading
import csv
from datetime import datetime
from typing import Optional

import customtkinter as ctk
from tkinter import filedialog, messagebox

from gui.theme import Colors, Fonts, Spacing, Icons
from gui.components import SectionHeader, AnimatedButton, LoadingOverlay

logger = logging.getLogger("HealthcareAI.pages.reports")


class ReportsPage(ctk.CTkFrame):
    """Report generation and export page."""

    def __init__(self, parent, app_ref=None, **kwargs):
        super().__init__(parent, fg_color=Colors.BACKGROUND, **kwargs)

        self._app_ref = app_ref
        self._build_ui()

    def _build_ui(self) -> None:
        """Build the reports page layout."""
        pad = Spacing.CONTENT_PAD

        self._scroll = ctk.CTkScrollableFrame(
            self, fg_color=Colors.BACKGROUND,
            scrollbar_button_color=Colors.BORDER,
        )
        self._scroll.pack(fill="both", expand=True)

        SectionHeader(
            self._scroll,
            title=f"{Icons.REPORTS}  Report Generation & Export",
            subtitle="Generate PDF reports and export charts and data",
        ).pack(fill="x", padx=pad, pady=(pad, 16))

        # ── PDF Report Section ────────────────────────────────────────
        self._build_section(
            self._scroll,
            title="📄  Generate Patient PDF Report",
            description=(
                "Creates a comprehensive PDF with patient inputs, prediction, "
                "risk assessment, SHAP & LIME interpretations, and model metrics."
            ),
            buttons=[
                ("Generate PDF Report", Icons.SAVE, Colors.PRIMARY, self._generate_pdf),
            ],
        )

        # ── Image Export Section ──────────────────────────────────────
        self._build_section(
            self._scroll,
            title="🖼️  Export Charts & Images",
            description="Save SHAP and LIME plots as high-resolution PNG images.",
            buttons=[
                ("Save SHAP Plot", Icons.SHAP, "#7C3AED", self._save_shap_image),
                ("Save LIME Plot", Icons.LIME, Colors.WARNING, self._save_lime_image),
            ],
        )

        # ── CSV Export Section ────────────────────────────────────────
        self._build_section(
            self._scroll,
            title="📊  Export Prediction Data",
            description="Export prediction results and patient inputs as CSV.",
            buttons=[
                ("Export CSV", Icons.EXPORT, Colors.SUCCESS, self._export_csv),
            ],
        )

        # ── Generated Reports List ────────────────────────────────────
        SectionHeader(
            self._scroll,
            title="📁  Generated Reports",
            subtitle="Previously generated report files",
            accent_color=Colors.TEXT_SECONDARY,
        ).pack(fill="x", padx=pad, pady=(16, 8))

        self._reports_list_frame = ctk.CTkFrame(
            self._scroll, fg_color=Colors.CARD,
            corner_radius=12, border_width=1,
            border_color=Colors.BORDER_LIGHT,
        )
        self._reports_list_frame.pack(fill="x", padx=pad, pady=(0, pad))

        # Refresh button
        AnimatedButton(
            self._reports_list_frame,
            text="Refresh List",
            icon=Icons.REFRESH,
            color=Colors.TEXT_MUTED,
            hover_color=Colors.TEXT_SECONDARY,
            width=140, height=34,
            command=self._refresh_reports_list,
        ).pack(anchor="e", padx=12, pady=8)

        self._reports_list = ctk.CTkFrame(self._reports_list_frame, fg_color="transparent")
        self._reports_list.pack(fill="x", padx=12, pady=(0, 12))

        # Loading
        self._loading = LoadingOverlay(self, message="Generating report...")

        # Initial load
        self._refresh_reports_list()

    def _build_section(self, parent, title: str, description: str,
                        buttons: list) -> None:
        """Build a styled action section card."""
        pad = Spacing.CONTENT_PAD

        card = ctk.CTkFrame(
            parent, fg_color=Colors.CARD,
            corner_radius=12, border_width=1,
            border_color=Colors.BORDER_LIGHT,
        )
        card.pack(fill="x", padx=pad, pady=(0, 12))

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="x", padx=20, pady=16)

        ctk.CTkLabel(
            inner, text=title,
            font=Fonts.HEADING_3,
            text_color=Colors.TEXT_PRIMARY,
            anchor="w",
        ).pack(anchor="w")

        ctk.CTkLabel(
            inner, text=description,
            font=Fonts.SMALL,
            text_color=Colors.TEXT_MUTED,
            anchor="w",
        ).pack(anchor="w", pady=(4, 12))

        btn_frame = ctk.CTkFrame(inner, fg_color="transparent")
        btn_frame.pack(anchor="w")

        for text, icon, color, cmd in buttons:
            AnimatedButton(
                btn_frame, text=text, icon=icon,
                color=color, hover_color=Colors.PRIMARY_DARK,
                width=200, height=40,
                command=cmd,
            ).pack(side="left", padx=(0, 8))

    def _generate_pdf(self) -> None:
        """Generate a PDF report for the current prediction."""
        if self._app_ref is None:
            messagebox.showwarning("Warning", "Application reference not available.")
            return

        pred_page = self._app_ref.get_page("prediction")
        result = pred_page.get_last_result() if pred_page else None

        if result is None or not result.success:
            messagebox.showinfo(
                "No Prediction",
                "Please run a patient prediction first before generating a report."
            )
            return

        self._loading.show()

        def generate():
            try:
                from core.report_generator import generate_report

                # Gather explanations
                shap_page = self._app_ref.get_page("shap")
                lime_page = self._app_ref.get_page("lime")
                perf_page = self._app_ref.get_page("performance")

                shap_text = shap_page.get_explanation_text() if shap_page else ""
                lime_text = lime_page.get_explanation_text() if lime_page else ""
                metrics = perf_page.get_metrics() if perf_page else None

                filepath = generate_report(
                    result=result,
                    shap_explanation=shap_text,
                    lime_explanation=lime_text,
                    metrics=metrics,
                )

                if filepath:
                    self.after(0, lambda: self._on_pdf_success(filepath))
                else:
                    self.after(0, lambda: messagebox.showerror(
                        "Error", "Failed to generate PDF report."
                    ))
            except Exception as e:
                logger.exception("PDF generation failed: %s", e)
                self.after(0, lambda: messagebox.showerror(
                    "Error", f"Report generation failed:\n{str(e)}"
                ))
            finally:
                self.after(0, self._loading.hide)

        threading.Thread(target=generate, daemon=True).start()

    def _on_pdf_success(self, filepath: str) -> None:
        """Handle successful PDF generation."""
        self._refresh_reports_list()
        messagebox.showinfo(
            "Report Generated",
            f"PDF report saved successfully!\n\n{filepath}"
        )

    def _save_shap_image(self) -> None:
        """Save the current SHAP plot as a PNG image."""
        if self._app_ref is None:
            return

        shap_page = self._app_ref.get_page("shap")
        fig = shap_page.get_current_figure() if shap_page else None

        if fig is None:
            messagebox.showinfo(
                "No Plot",
                "Please generate a SHAP plot first."
            )
            return

        self._save_figure(fig, "shap_plot")

    def _save_lime_image(self) -> None:
        """Save the current LIME plot as a PNG image."""
        if self._app_ref is None:
            return

        lime_page = self._app_ref.get_page("lime")
        fig = lime_page.get_current_figure() if lime_page else None

        if fig is None:
            messagebox.showinfo(
                "No Plot",
                "Please generate a LIME explanation first."
            )
            return

        self._save_figure(fig, "lime_plot")

    def _save_figure(self, fig, default_name: str) -> None:
        """Save a matplotlib figure to a user-chosen location."""
        filepath = filedialog.asksaveasfilename(
            title="Save Image",
            defaultextension=".png",
            initialfile=f"{default_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
            filetypes=[("PNG Image", "*.png"), ("JPEG Image", "*.jpg"), ("All Files", "*.*")],
        )

        if filepath:
            try:
                fig.savefig(filepath, dpi=150, bbox_inches="tight",
                             facecolor="white", edgecolor="none")
                messagebox.showinfo("Saved", f"Image saved to:\n{filepath}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image:\n{str(e)}")

    def _export_csv(self) -> None:
        """Export prediction results to CSV."""
        if self._app_ref is None:
            return

        pred_page = self._app_ref.get_page("prediction")
        result = pred_page.get_last_result() if pred_page else None

        if result is None or not result.success:
            messagebox.showinfo(
                "No Prediction",
                "Please run a patient prediction first."
            )
            return

        filepath = filedialog.asksaveasfilename(
            title="Export CSV",
            defaultextension=".csv",
            initialfile=f"prediction_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            filetypes=[("CSV File", "*.csv"), ("All Files", "*.*")],
        )

        if filepath:
            try:
                from core.predict import get_formatted_inputs

                with open(filepath, "w", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow(["Parameter", "Value"])
                    writer.writerow(["Timestamp", datetime.now().isoformat()])
                    writer.writerow([])

                    # Patient inputs
                    writer.writerow(["--- Patient Inputs ---"])
                    for _, display, val in get_formatted_inputs(result.feature_values):
                        writer.writerow([display, val])

                    writer.writerow([])
                    writer.writerow(["--- Prediction Result ---"])
                    writer.writerow(["Prediction", result.prediction_label])
                    writer.writerow(["Probability", result.probability_pct])
                    writer.writerow(["Confidence", result.confidence_pct])
                    writer.writerow(["Risk Category", result.risk_category])

                messagebox.showinfo("Exported", f"CSV exported to:\n{filepath}")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to export CSV:\n{str(e)}")

    def _refresh_reports_list(self) -> None:
        """Refresh the list of generated reports."""
        for w in self._reports_list.winfo_children():
            w.destroy()

        from core.utils import REPORTS_DIR

        if not os.path.isdir(REPORTS_DIR):
            ctk.CTkLabel(
                self._reports_list,
                text="No reports generated yet.",
                font=Fonts.SMALL,
                text_color=Colors.TEXT_MUTED,
            ).pack(pady=8)
            return

        files = sorted(
            [f for f in os.listdir(REPORTS_DIR) if f.endswith(".pdf")],
            reverse=True,
        )

        if not files:
            ctk.CTkLabel(
                self._reports_list,
                text="No reports generated yet.",
                font=Fonts.SMALL,
                text_color=Colors.TEXT_MUTED,
            ).pack(pady=8)
            return

        for filename in files[:10]:  # Show latest 10
            filepath = os.path.join(REPORTS_DIR, filename)
            size_kb = os.path.getsize(filepath) / 1024

            row = ctk.CTkFrame(self._reports_list, fg_color="transparent")
            row.pack(fill="x", pady=2)

            ctk.CTkLabel(
                row, text=f"📄  {filename}",
                font=Fonts.SMALL,
                text_color=Colors.TEXT_PRIMARY,
                anchor="w",
            ).pack(side="left")

            ctk.CTkLabel(
                row, text=f"{size_kb:.1f} KB",
                font=Fonts.CAPTION,
                text_color=Colors.TEXT_MUTED,
            ).pack(side="right", padx=(8, 0))

            ctk.CTkButton(
                row, text="Open",
                font=Fonts.CAPTION,
                fg_color=Colors.PRIMARY,
                hover_color=Colors.PRIMARY_HOVER,
                width=60, height=24,
                corner_radius=4,
                command=lambda p=filepath: os.startfile(p),
            ).pack(side="right", padx=4)
