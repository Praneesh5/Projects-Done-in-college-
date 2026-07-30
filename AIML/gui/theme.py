"""
gui/theme.py — Design System & Theme Constants
===============================================
Centralized design tokens for the entire application UI.
Inspired by Microsoft Fluent Design, Windows 11, and modern
medical dashboard aesthetics.

All colors, fonts, spacing, and styling dictionaries live here
so that the entire UI stays visually consistent.

Usage:
    from gui.theme import Colors, Fonts, Spacing
    label.configure(text_color=Colors.PRIMARY)
"""


class Colors:
    """Application color palette — modern healthcare aesthetic."""

    # Brand / Primary
    PRIMARY = "#2563EB"
    PRIMARY_HOVER = "#1D4ED8"
    PRIMARY_LIGHT = "#DBEAFE"
    PRIMARY_DARK = "#1E40AF"

    # Semantic
    SUCCESS = "#16A34A"
    SUCCESS_LIGHT = "#DCFCE7"
    DANGER = "#DC2626"
    DANGER_LIGHT = "#FEE2E2"
    WARNING = "#F59E0B"
    WARNING_LIGHT = "#FEF3C7"
    INFO = "#0EA5E9"
    INFO_LIGHT = "#E0F2FE"

    # Neutral
    BACKGROUND = "#F5F7FA"
    SURFACE = "#FFFFFF"
    CARD = "#FFFFFF"
    BORDER = "#E5E7EB"
    BORDER_LIGHT = "#F3F4F6"

    # Text
    TEXT_PRIMARY = "#1F2937"
    TEXT_SECONDARY = "#6B7280"
    TEXT_MUTED = "#9CA3AF"
    TEXT_WHITE = "#FFFFFF"

    # Sidebar
    SIDEBAR_BG = "#1E293B"
    SIDEBAR_HOVER = "#334155"
    SIDEBAR_ACTIVE = "#2563EB"
    SIDEBAR_TEXT = "#CBD5E1"
    SIDEBAR_TEXT_ACTIVE = "#FFFFFF"

    # Top bar
    TOPBAR_BG = "#FFFFFF"
    TOPBAR_BORDER = "#E5E7EB"

    # Risk gauge
    RISK_LOW = "#16A34A"
    RISK_MEDIUM = "#F59E0B"
    RISK_HIGH = "#DC2626"
    RISK_BG = "#F1F5F9"

    # Charts
    CHART_BG = "#FFFFFF"
    CHART_GRID = "#F3F4F6"


class Fonts:
    """Typography definitions — uses Segoe UI (Windows native)."""

    # Font family — Segoe UI is crisp and professional on Windows
    FAMILY = "Segoe UI"
    FAMILY_MONO = "Consolas"

    # Sizes
    TITLE = (FAMILY, 22, "bold")
    HEADING_1 = (FAMILY, 18, "bold")
    HEADING_2 = (FAMILY, 15, "bold")
    HEADING_3 = (FAMILY, 13, "bold")
    BODY = (FAMILY, 11)
    BODY_BOLD = (FAMILY, 11, "bold")
    SMALL = (FAMILY, 10)
    SMALL_BOLD = (FAMILY, 10, "bold")
    CAPTION = (FAMILY, 9)
    CAPTION_BOLD = (FAMILY, 9, "bold")
    BUTTON = (FAMILY, 11, "bold")
    METRIC_VALUE = (FAMILY, 28, "bold")
    METRIC_LABEL = (FAMILY, 10)
    SIDEBAR_ITEM = (FAMILY, 12)
    SIDEBAR_ITEM_ACTIVE = (FAMILY, 12, "bold")
    MONO = (FAMILY_MONO, 10)


class Spacing:
    """Consistent spacing and sizing tokens."""

    # Padding
    PAD_XS = 4
    PAD_SM = 8
    PAD_MD = 12
    PAD_LG = 16
    PAD_XL = 24
    PAD_XXL = 32

    # Margins
    MARGIN_SM = 8
    MARGIN_MD = 16
    MARGIN_LG = 24

    # Card
    CARD_PAD = 20
    CARD_RADIUS = 12

    # Sidebar
    SIDEBAR_WIDTH = 220
    SIDEBAR_ITEM_HEIGHT = 44
    SIDEBAR_PAD_X = 16

    # Top bar
    TOPBAR_HEIGHT = 60

    # Content area
    CONTENT_PAD = 24

    # Input fields
    INPUT_HEIGHT = 36
    INPUT_RADIUS = 8

    # Buttons
    BUTTON_HEIGHT = 40
    BUTTON_RADIUS = 8
    BUTTON_PAD_X = 20


class Icons:
    """
    Unicode icons for sidebar navigation and UI elements.
    Using Unicode symbols instead of external icon files for
    simplicity and PyInstaller compatibility.
    """
    DASHBOARD = "📊"
    PREDICTION = "🩺"
    PERFORMANCE = "📈"
    SHAP = "🔬"
    LIME = "🧪"
    REPORTS = "📄"
    ABOUT = "ℹ️"
    SETTINGS = "⚙️"
    HEART = "❤️"
    CHECK = "✓"
    CROSS = "✗"
    WARNING = "⚠️"
    CLOCK = "🕐"
    CALENDAR = "📅"
    SAVE = "💾"
    EXPORT = "📤"
    REFRESH = "🔄"
    SEARCH = "🔍"
    USER = "👤"
    HOSPITAL = "🏥"
    CHART = "📉"
    BRAIN = "🧠"
    SHIELD = "🛡️"
    SPARKLE = "✨"


# ─────────────────────────────────────────────────────────────────────
# SIDEBAR NAVIGATION DEFINITION
# ─────────────────────────────────────────────────────────────────────

SIDEBAR_ITEMS = [
    {"key": "dashboard",   "label": "Dashboard",          "icon": Icons.DASHBOARD},
    {"key": "prediction",  "label": "Patient Prediction",  "icon": Icons.PREDICTION},
    {"key": "performance", "label": "Model Performance",   "icon": Icons.PERFORMANCE},
    {"key": "shap",        "label": "SHAP Analysis",       "icon": Icons.SHAP},
    {"key": "lime",        "label": "LIME Analysis",       "icon": Icons.LIME},
    {"key": "reports",     "label": "Reports",             "icon": Icons.REPORTS},
    {"key": "about",       "label": "About",               "icon": Icons.ABOUT},
    {"key": "settings",    "label": "Settings",            "icon": Icons.SETTINGS},
]
