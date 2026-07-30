"""
gui/pages/settings.py — Settings Page
======================================
Provides application configuration options:
    - Appearance mode (Light/Dark/System)
    - Model path configuration
    - Export path configuration
    - About system info
"""

import os
import customtkinter as ctk

from gui.theme import Colors, Fonts, Spacing, Icons
from gui.components import SectionHeader
from core.utils import MODELS_DIR, REPORTS_DIR, BASE_DIR


class SettingsPage(ctk.CTkFrame):
    """Application settings page."""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color=Colors.BACKGROUND, **kwargs)
        self._build_ui()

    def _build_ui(self) -> None:
        """Build the settings page layout."""
        pad = Spacing.CONTENT_PAD

        scroll = ctk.CTkScrollableFrame(
            self, fg_color=Colors.BACKGROUND,
            scrollbar_button_color=Colors.BORDER,
        )
        scroll.pack(fill="both", expand=True)

        SectionHeader(
            scroll,
            title=f"{Icons.SETTINGS}  Application Settings",
            subtitle="Configure appearance and application paths",
        ).pack(fill="x", padx=pad, pady=(pad, 16))

        # ── Appearance ────────────────────────────────────────────────
        app_card = ctk.CTkFrame(
            scroll, fg_color=Colors.CARD,
            corner_radius=12, border_width=1,
            border_color=Colors.BORDER_LIGHT,
        )
        app_card.pack(fill="x", padx=pad, pady=(0, 12))

        inner = ctk.CTkFrame(app_card, fg_color="transparent")
        inner.pack(fill="x", padx=20, pady=16)

        ctk.CTkLabel(
            inner, text="🎨  Appearance Mode",
            font=Fonts.HEADING_3,
            text_color=Colors.TEXT_PRIMARY,
        ).pack(anchor="w")

        ctk.CTkLabel(
            inner, text="Choose the application color theme",
            font=Fonts.CAPTION,
            text_color=Colors.TEXT_MUTED,
        ).pack(anchor="w", pady=(2, 8))

        mode_frame = ctk.CTkFrame(inner, fg_color="transparent")
        mode_frame.pack(anchor="w")

        self._mode_var = ctk.StringVar(value="Light")
        for mode in ["Light", "Dark", "System"]:
            ctk.CTkRadioButton(
                mode_frame,
                text=mode,
                variable=self._mode_var,
                value=mode,
                font=Fonts.BODY,
                text_color=Colors.TEXT_PRIMARY,
                command=self._on_mode_change,
            ).pack(side="left", padx=(0, 16))

        # ── Paths ─────────────────────────────────────────────────────
        paths_card = ctk.CTkFrame(
            scroll, fg_color=Colors.CARD,
            corner_radius=12, border_width=1,
            border_color=Colors.BORDER_LIGHT,
        )
        paths_card.pack(fill="x", padx=pad, pady=(0, 12))

        paths_inner = ctk.CTkFrame(paths_card, fg_color="transparent")
        paths_inner.pack(fill="x", padx=20, pady=16)

        ctk.CTkLabel(
            paths_inner, text="📁  Application Paths",
            font=Fonts.HEADING_3,
            text_color=Colors.TEXT_PRIMARY,
        ).pack(anchor="w", pady=(0, 8))

        paths = [
            ("Application Root", BASE_DIR),
            ("Model Artifacts", MODELS_DIR),
            ("Reports Output", REPORTS_DIR),
        ]

        for label, path in paths:
            row = ctk.CTkFrame(paths_inner, fg_color="transparent")
            row.pack(fill="x", pady=4)

            ctk.CTkLabel(
                row, text=f"{label}:",
                font=Fonts.SMALL_BOLD,
                text_color=Colors.TEXT_PRIMARY,
                width=160, anchor="w",
            ).pack(side="left")

            ctk.CTkLabel(
                row, text=path,
                font=("Consolas", 10),
                text_color=Colors.TEXT_SECONDARY,
                anchor="w",
            ).pack(side="left", fill="x", expand=True)

        # ── System Info ───────────────────────────────────────────────
        sys_card = ctk.CTkFrame(
            scroll, fg_color=Colors.CARD,
            corner_radius=12, border_width=1,
            border_color=Colors.BORDER_LIGHT,
        )
        sys_card.pack(fill="x", padx=pad, pady=(0, pad))

        sys_inner = ctk.CTkFrame(sys_card, fg_color="transparent")
        sys_inner.pack(fill="x", padx=20, pady=16)

        ctk.CTkLabel(
            sys_inner, text="💻  System Information",
            font=Fonts.HEADING_3,
            text_color=Colors.TEXT_PRIMARY,
        ).pack(anchor="w", pady=(0, 8))

        import sys
        import platform

        info = [
            ("Python Version", f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"),
            ("Platform", platform.platform()),
            ("Architecture", platform.machine()),
            ("Application Version", "1.0.0"),
        ]

        for label, value in info:
            row = ctk.CTkFrame(sys_inner, fg_color="transparent")
            row.pack(fill="x", pady=2)

            ctk.CTkLabel(
                row, text=f"{label}:",
                font=Fonts.SMALL_BOLD,
                text_color=Colors.TEXT_PRIMARY,
                width=160, anchor="w",
            ).pack(side="left")

            ctk.CTkLabel(
                row, text=value,
                font=Fonts.SMALL,
                text_color=Colors.TEXT_SECONDARY,
                anchor="w",
            ).pack(side="left")

    def _on_mode_change(self) -> None:
        """Handle appearance mode change."""
        mode = self._mode_var.get().lower()
        ctk.set_appearance_mode(mode)
