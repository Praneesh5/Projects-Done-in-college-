"""
gui/app.py — Main Application Window
=====================================
The root window of the Healthcare AI application. Manages:
    - Window configuration and centering
    - Top navigation bar (logo, title, clock, status)
    - Left sidebar navigation with icons and active states
    - Content area with page routing via frame stacking
    - Footer with university/project/developer info
    - Live clock update
    - Page transitions

This is the only module that directly creates a CTk() window.
All pages are instantiated here and stacked in the content area.
"""

import logging
from datetime import datetime
from typing import Optional

import customtkinter as ctk

from gui.theme import Colors, Fonts, Spacing, Icons, SIDEBAR_ITEMS
from gui.components import SidebarButton

# Import all page classes
from gui.pages.dashboard import DashboardPage
from gui.pages.prediction import PredictionPage
from gui.pages.performance import PerformancePage
from gui.pages.shap_page import SHAPPage
from gui.pages.lime_page import LIMEPage
from gui.pages.reports import ReportsPage
from gui.pages.about import AboutPage
from gui.pages.settings import SettingsPage

logger = logging.getLogger("HealthcareAI.app")


class HealthcareApp(ctk.CTk):
    """
    Main application window.

    Orchestrates the entire UI: sidebar navigation, page routing,
    top bar with live clock, and footer. All pages are created once
    at startup and shown/hidden via frame stacking.
    """

    APP_TITLE = "Healthcare AI — Explainable Clinical Prediction"
    APP_VERSION = "1.0.0"
    WINDOW_WIDTH = 1400
    WINDOW_HEIGHT = 850
    MIN_WIDTH = 1100
    MIN_HEIGHT = 700

    def __init__(self) -> None:
        super().__init__()

        # ── Window Configuration ──────────────────────────────────────
        self.title(self.APP_TITLE)
        self.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}")
        self.minsize(self.MIN_WIDTH, self.MIN_HEIGHT)
        self._center_window()

        # Use light mode by default for the clinical/professional look
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.configure(fg_color=Colors.BACKGROUND)

        # ── Internal State ────────────────────────────────────────────
        self._pages: dict[str, ctk.CTkFrame] = {}
        self._sidebar_buttons: dict[str, SidebarButton] = {}
        self._current_page: str = ""

        # ── Build Layout ──────────────────────────────────────────────
        self._build_topbar()
        self._build_sidebar()
        self._build_content_area()
        self._build_footer()

        # ── Initialize Pages ──────────────────────────────────────────
        self._create_pages()

        # ── Show Default Page ─────────────────────────────────────────
        self.navigate("dashboard")

        # ── Start Clock ───────────────────────────────────────────────
        self._update_clock()

        # ── Load Dashboard Metrics (deferred) ─────────────────────────
        self.after(500, self._load_initial_data)

        logger.info("Application window initialized: %dx%d",
                     self.WINDOW_WIDTH, self.WINDOW_HEIGHT)

    def _center_window(self) -> None:
        """Center the window on the screen."""
        self.update_idletasks()
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        x = (screen_w - self.WINDOW_WIDTH) // 2
        y = (screen_h - self.WINDOW_HEIGHT) // 2
        self.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}+{x}+{y}")

    # ─────────────────────────────────────────────────────────────────
    # TOP BAR
    # ─────────────────────────────────────────────────────────────────

    def _build_topbar(self) -> None:
        """Build the top navigation bar."""
        self._topbar = ctk.CTkFrame(
            self, fg_color=Colors.TOPBAR_BG,
            height=Spacing.TOPBAR_HEIGHT,
            corner_radius=0,
        )
        self._topbar.pack(fill="x", side="top")
        self._topbar.pack_propagate(False)

        # Left section: Logo + Title
        left = ctk.CTkFrame(self._topbar, fg_color="transparent")
        left.pack(side="left", fill="y", padx=16)

        ctk.CTkLabel(
            left, text=f"{Icons.HEART}",
            font=("Segoe UI Emoji", 22),
        ).pack(side="left", padx=(0, 8))

        title_frame = ctk.CTkFrame(left, fg_color="transparent")
        title_frame.pack(side="left")

        ctk.CTkLabel(
            title_frame,
            text="Healthcare AI",
            font=Fonts.HEADING_3,
            text_color=Colors.PRIMARY,
        ).pack(anchor="w")

        ctk.CTkLabel(
            title_frame,
            text="Explainable Clinical Prediction",
            font=Fonts.CAPTION,
            text_color=Colors.TEXT_MUTED,
        ).pack(anchor="w")

        # Right section: Date + Time + Status
        right = ctk.CTkFrame(self._topbar, fg_color="transparent")
        right.pack(side="right", fill="y", padx=16)

        # Status indicator
        self._status_dot = ctk.CTkLabel(
            right, text="●",
            font=("Segoe UI", 14),
            text_color=Colors.SUCCESS,
        )
        self._status_dot.pack(side="right", padx=(8, 0))

        ctk.CTkLabel(
            right, text="Model Ready",
            font=Fonts.CAPTION,
            text_color=Colors.TEXT_MUTED,
        ).pack(side="right")

        # Time
        self._time_label = ctk.CTkLabel(
            right,
            text="",
            font=Fonts.BODY_BOLD,
            text_color=Colors.TEXT_PRIMARY,
        )
        self._time_label.pack(side="right", padx=(16, 16))

        # Date
        self._date_label = ctk.CTkLabel(
            right,
            text="",
            font=Fonts.SMALL,
            text_color=Colors.TEXT_SECONDARY,
        )
        self._date_label.pack(side="right", padx=(0, 8))

        # Separator line
        sep = ctk.CTkFrame(self, fg_color=Colors.TOPBAR_BORDER, height=1, corner_radius=0)
        sep.pack(fill="x", side="top")

    # ─────────────────────────────────────────────────────────────────
    # SIDEBAR
    # ─────────────────────────────────────────────────────────────────

    def _build_sidebar(self) -> None:
        """Build the left sidebar navigation."""
        self._sidebar = ctk.CTkFrame(
            self, fg_color=Colors.SIDEBAR_BG,
            width=Spacing.SIDEBAR_WIDTH,
            corner_radius=0,
        )
        self._sidebar.pack(fill="y", side="left")
        self._sidebar.pack_propagate(False)

        # App brand in sidebar
        brand = ctk.CTkFrame(self._sidebar, fg_color="transparent")
        brand.pack(fill="x", padx=12, pady=(16, 8))

        ctk.CTkLabel(
            brand, text="NAVIGATION",
            font=Fonts.CAPTION_BOLD,
            text_color=Colors.TEXT_MUTED,
        ).pack(anchor="w", padx=4)

        # Separator
        ctk.CTkFrame(
            self._sidebar, fg_color=Colors.SIDEBAR_HOVER,
            height=1, corner_radius=0,
        ).pack(fill="x", padx=12, pady=(0, 8))

        # Navigation buttons
        for item in SIDEBAR_ITEMS:
            btn = SidebarButton(
                self._sidebar,
                text=item["label"],
                icon=item["icon"],
                command=lambda k=item["key"]: self.navigate(k),
            )
            btn.pack(fill="x", padx=8, pady=2)
            self._sidebar_buttons[item["key"]] = btn

        # Bottom spacer + version
        spacer = ctk.CTkFrame(self._sidebar, fg_color="transparent")
        spacer.pack(fill="both", expand=True)

        ctk.CTkFrame(
            self._sidebar, fg_color=Colors.SIDEBAR_HOVER,
            height=1, corner_radius=0,
        ).pack(fill="x", padx=12, pady=(0, 4))

        ctk.CTkLabel(
            self._sidebar,
            text=f"v{self.APP_VERSION}",
            font=Fonts.CAPTION,
            text_color=Colors.TEXT_MUTED,
        ).pack(pady=(0, 12))

    # ─────────────────────────────────────────────────────────────────
    # CONTENT AREA
    # ─────────────────────────────────────────────────────────────────

    def _build_content_area(self) -> None:
        """Build the main content area where pages are stacked."""
        self._content = ctk.CTkFrame(
            self, fg_color=Colors.BACKGROUND, corner_radius=0,
        )
        self._content.pack(fill="both", expand=True, side="top")

    # ─────────────────────────────────────────────────────────────────
    # FOOTER
    # ─────────────────────────────────────────────────────────────────

    def _build_footer(self) -> None:
        """Build the footer bar."""
        footer = ctk.CTkFrame(
            self, fg_color=Colors.TOPBAR_BG,
            height=32, corner_radius=0,
        )
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)

        # Separator
        sep = ctk.CTkFrame(self, fg_color=Colors.TOPBAR_BORDER, height=1, corner_radius=0)
        sep.pack(fill="x", side="bottom")

        # Left: University
        ctk.CTkLabel(
            footer, text="Your University Name",
            font=Fonts.CAPTION,
            text_color=Colors.TEXT_MUTED,
        ).pack(side="left", padx=16)

        # Right: Developer
        ctk.CTkLabel(
            footer, text="Developed by: Your Name",
            font=Fonts.CAPTION,
            text_color=Colors.TEXT_MUTED,
        ).pack(side="right", padx=16)

        # Center: Version
        ctk.CTkLabel(
            footer,
            text=f"Model Interpretability in Clinical ML v{self.APP_VERSION}",
            font=Fonts.CAPTION,
            text_color=Colors.TEXT_MUTED,
        ).pack(side="right", padx=16)

    # ─────────────────────────────────────────────────────────────────
    # PAGE CREATION & ROUTING
    # ─────────────────────────────────────────────────────────────────

    def _create_pages(self) -> None:
        """Instantiate all page frames and stack them in the content area."""
        page_classes = {
            "dashboard":   lambda p: DashboardPage(p, navigate_callback=self.navigate),
            "prediction":  lambda p: PredictionPage(p, app_ref=self),
            "performance": lambda p: PerformancePage(p),
            "shap":        lambda p: SHAPPage(p, app_ref=self),
            "lime":        lambda p: LIMEPage(p, app_ref=self),
            "reports":     lambda p: ReportsPage(p, app_ref=self),
            "about":       lambda p: AboutPage(p),
            "settings":    lambda p: SettingsPage(p),
        }

        for key, factory in page_classes.items():
            page = factory(self._content)
            page.place(relx=0, rely=0, relwidth=1, relheight=1)
            self._pages[key] = page

        logger.info("Created %d pages.", len(self._pages))

    def navigate(self, page_key: str) -> None:
        """
        Switch to the specified page.

        Args:
            page_key: Key of the page to show (e.g., 'dashboard', 'prediction').
        """
        if page_key not in self._pages:
            logger.warning("Unknown page: %s", page_key)
            return

        if page_key == self._current_page:
            return  # Already on this page

        # Update sidebar buttons
        for key, btn in self._sidebar_buttons.items():
            btn.set_active(key == page_key)

        # Raise the target page to the top of the stack
        self._pages[page_key].lift()
        self._current_page = page_key

        # Trigger page-specific loading
        self._on_page_shown(page_key)

        logger.info("Navigated to: %s", page_key)

    def _on_page_shown(self, page_key: str) -> None:
        """Trigger any loading logic when a page is first shown."""
        if page_key == "performance":
            perf = self._pages.get("performance")
            if perf and hasattr(perf, "load_metrics"):
                perf.load_metrics()

    def get_page(self, page_key: str) -> Optional[ctk.CTkFrame]:
        """
        Get a reference to a page by key.

        Used by pages that need to access other pages' data
        (e.g., Reports page reading from Prediction page).
        """
        return self._pages.get(page_key)

    # ─────────────────────────────────────────────────────────────────
    # CLOCK
    # ─────────────────────────────────────────────────────────────────

    def _update_clock(self) -> None:
        """Update the top bar date and time every second."""
        now = datetime.now()
        self._time_label.configure(text=now.strftime("%I:%M:%S %p"))
        self._date_label.configure(text=now.strftime("%B %d, %Y"))
        self.after(1000, self._update_clock)

    # ─────────────────────────────────────────────────────────────────
    # INITIAL DATA LOADING
    # ─────────────────────────────────────────────────────────────────

    def _load_initial_data(self) -> None:
        """Load initial data for the dashboard (deferred start)."""
        dashboard = self._pages.get("dashboard")
        if dashboard and hasattr(dashboard, "load_metrics"):
            dashboard.load_metrics()

        # Update status indicator based on model loading
        from core.model_loader import ModelLoader
        loader = ModelLoader()
        if loader.is_loaded:
            self._status_dot.configure(text_color=Colors.SUCCESS)
        else:
            self._status_dot.configure(text_color=Colors.DANGER)
