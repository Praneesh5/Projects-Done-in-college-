"""
gui/components.py — Reusable Custom UI Widgets
===============================================
Premium custom widgets built on CustomTkinter for a healthcare
dashboard look-and-feel.

Components:
    - MetricCard:       Stat card with icon, value, and label
    - RiskGauge:        Semi-circular gauge (Low/Medium/High)
    - AnimatedButton:   Button with hover color transition
    - SidebarButton:    Nav button with icon and active state
    - LoadingOverlay:   Animated spinner overlay
    - SectionHeader:    Section title with accent underline
    - TooltipManager:   Hover tooltip for any widget
    - ScrollableFrame:  Scrollable content area

Usage:
    card = MetricCard(parent, title="Accuracy", value="95.2%",
                      icon="📊", color=Colors.PRIMARY)
"""

import math
import logging
from typing import Optional, Callable

import customtkinter as ctk

from gui.theme import Colors, Fonts, Spacing

logger = logging.getLogger("HealthcareAI.components")


# ─────────────────────────────────────────────────────────────────────
# METRIC CARD
# ─────────────────────────────────────────────────────────────────────

class MetricCard(ctk.CTkFrame):
    """
    A premium statistics card showing an icon, a large value,
    a title label, and an optional subtitle.

    ┌────────────────────────┐
    │  📊                    │
    │  95.2%                 │
    │  Model Accuracy        │
    │  Test set evaluation   │
    └────────────────────────┘
    """

    def __init__(
        self,
        parent,
        title: str = "",
        value: str = "",
        icon: str = "",
        subtitle: str = "",
        accent_color: str = Colors.PRIMARY,
        width: int = 220,
        **kwargs,
    ):
        super().__init__(
            parent,
            fg_color=Colors.CARD,
            corner_radius=Spacing.CARD_RADIUS,
            border_width=1,
            border_color=Colors.BORDER_LIGHT,
            **kwargs,
        )

        pad = Spacing.CARD_PAD

        # Top accent stripe
        accent = ctk.CTkFrame(
            self, fg_color=accent_color, height=4,
            corner_radius=0,
        )
        accent.pack(fill="x", padx=0, pady=0)

        # Content
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=pad, pady=(pad - 4, pad))

        # Icon
        if icon:
            ctk.CTkLabel(
                content, text=icon, font=("Segoe UI Emoji", 24),
                text_color=accent_color,
            ).pack(anchor="w")

        # Value
        ctk.CTkLabel(
            content, text=value, font=Fonts.METRIC_VALUE,
            text_color=Colors.TEXT_PRIMARY, anchor="w",
        ).pack(anchor="w", pady=(4, 0))

        # Title
        ctk.CTkLabel(
            content, text=title, font=Fonts.SMALL_BOLD,
            text_color=Colors.TEXT_SECONDARY, anchor="w",
        ).pack(anchor="w", pady=(2, 0))

        # Subtitle
        if subtitle:
            ctk.CTkLabel(
                content, text=subtitle, font=Fonts.CAPTION,
                text_color=Colors.TEXT_MUTED, anchor="w",
            ).pack(anchor="w", pady=(2, 0))

    def update_value(self, value: str) -> None:
        """Update the displayed metric value."""
        # Walk the widget tree to find the value label
        for child in self.winfo_children():
            if isinstance(child, ctk.CTkFrame):
                for sub in child.winfo_children():
                    if isinstance(sub, ctk.CTkLabel):
                        try:
                            font = sub.cget("font")
                            if font == Fonts.METRIC_VALUE:
                                sub.configure(text=value)
                                return
                        except Exception:
                            pass


# ─────────────────────────────────────────────────────────────────────
# RISK GAUGE
# ─────────────────────────────────────────────────────────────────────

class RiskGauge(ctk.CTkCanvas):
    """
    Semi-circular risk gauge that visually shows Low / Medium / High risk.

    The gauge is divided into three colored arcs:
        Green (Low) → Amber (Medium) → Red (High)

    A needle points to the current probability value.
    """

    def __init__(
        self,
        parent,
        size: int = 240,
        **kwargs,
    ):
        super().__init__(
            parent,
            width=size,
            height=size // 2 + 40,
            bg=Colors.CARD,
            highlightthickness=0,
            **kwargs,
        )
        self.size = size
        self.cx = size // 2
        self.cy = size // 2 + 10
        self.radius = size // 2 - 20
        self._draw_base()

    def _draw_base(self) -> None:
        """Draw the static gauge background arcs."""
        r = self.radius
        cx, cy = self.cx, self.cy

        # Three arcs: Low (green), Medium (amber), High (red)
        # Angles: 180° to 0° (left to right)
        arc_specs = [
            (180, 60, Colors.RISK_LOW),     # Low:    180° → 120°
            (120, 60, Colors.RISK_MEDIUM),   # Medium: 120° → 60°
            (60, 60, Colors.RISK_HIGH),      # High:   60°  → 0°
        ]

        for start, extent, color in arc_specs:
            self.create_arc(
                cx - r, cy - r, cx + r, cy + r,
                start=start, extent=extent,
                style="arc", outline=color, width=18,
            )

        # Labels
        label_font = ("Segoe UI", 9, "bold")
        self.create_text(cx - r + 10, cy + 15, text="LOW",
                          font=label_font, fill=Colors.RISK_LOW, anchor="w")
        self.create_text(cx, cy - r + 5, text="MED",
                          font=label_font, fill=Colors.RISK_MEDIUM, anchor="s")
        self.create_text(cx + r - 10, cy + 15, text="HIGH",
                          font=label_font, fill=Colors.RISK_HIGH, anchor="e")

    def set_value(self, probability: float, animated: bool = True) -> None:
        """
        Point the needle to the given probability value.

        Args:
            probability: Float 0.0 to 1.0.
            animated:    Whether to animate the needle movement.
        """
        probability = max(0.0, min(1.0, probability))

        if animated:
            self._animate_needle(0.0, probability, steps=30)
        else:
            self._draw_needle(probability)

    def _animate_needle(self, current: float, target: float, steps: int) -> None:
        """Animate the needle from current to target in N steps."""
        if steps <= 0:
            self._draw_needle(target)
            return

        step_size = (target - current) / steps
        new_val = current + step_size

        self._draw_needle(new_val)
        self.after(20, self._animate_needle, new_val, target, steps - 1)

    def _draw_needle(self, probability: float) -> None:
        """Draw the needle at the given probability position."""
        self.delete("needle")
        self.delete("center_dot")
        self.delete("value_text")

        # Convert probability (0–1) to angle (180°–0°)
        angle_deg = 180 - (probability * 180)
        angle_rad = math.radians(angle_deg)

        cx, cy = self.cx, self.cy
        needle_len = self.radius - 30

        # Needle tip
        nx = cx + needle_len * math.cos(angle_rad)
        ny = cy - needle_len * math.sin(angle_rad)

        # Draw needle line
        self.create_line(
            cx, cy, nx, ny,
            fill=Colors.TEXT_PRIMARY, width=3,
            tags="needle",
        )

        # Center dot
        dot_r = 8
        self.create_oval(
            cx - dot_r, cy - dot_r, cx + dot_r, cy + dot_r,
            fill=Colors.TEXT_PRIMARY, outline=Colors.CARD,
            width=2, tags="center_dot",
        )

        # Value text
        pct = f"{probability * 100:.1f}%"
        self.create_text(
            cx, cy + 30, text=pct,
            font=("Segoe UI", 16, "bold"),
            fill=Colors.TEXT_PRIMARY,
            tags="value_text",
        )


# ─────────────────────────────────────────────────────────────────────
# ANIMATED BUTTON
# ─────────────────────────────────────────────────────────────────────

class AnimatedButton(ctk.CTkButton):
    """
    Premium button with hover color transition.
    Changes color smoothly on hover for a polished feel.
    """

    def __init__(
        self,
        parent,
        text: str = "",
        command: Optional[Callable] = None,
        color: str = Colors.PRIMARY,
        hover_color: str = Colors.PRIMARY_HOVER,
        text_color: str = Colors.TEXT_WHITE,
        icon: str = "",
        width: int = 160,
        height: int = Spacing.BUTTON_HEIGHT,
        **kwargs,
    ):
        display_text = f"{icon}  {text}" if icon else text

        super().__init__(
            parent,
            text=display_text,
            command=command,
            fg_color=color,
            hover_color=hover_color,
            text_color=text_color,
            font=Fonts.BUTTON,
            corner_radius=Spacing.BUTTON_RADIUS,
            width=width,
            height=height,
            **kwargs,
        )


# ─────────────────────────────────────────────────────────────────────
# SIDEBAR BUTTON
# ─────────────────────────────────────────────────────────────────────

class SidebarButton(ctk.CTkButton):
    """
    Sidebar navigation button with icon, label, and active state.
    Shows a left accent bar when active.
    """

    def __init__(
        self,
        parent,
        text: str = "",
        icon: str = "",
        command: Optional[Callable] = None,
        **kwargs,
    ):
        display_text = f"  {icon}   {text}"

        super().__init__(
            parent,
            text=display_text,
            command=command,
            fg_color="transparent",
            hover_color=Colors.SIDEBAR_HOVER,
            text_color=Colors.SIDEBAR_TEXT,
            font=Fonts.SIDEBAR_ITEM,
            anchor="w",
            corner_radius=8,
            height=Spacing.SIDEBAR_ITEM_HEIGHT,
            **kwargs,
        )

        self._is_active = False

    def set_active(self, active: bool) -> None:
        """Toggle active/inactive visual state."""
        self._is_active = active
        if active:
            self.configure(
                fg_color=Colors.SIDEBAR_ACTIVE,
                text_color=Colors.SIDEBAR_TEXT_ACTIVE,
                font=Fonts.SIDEBAR_ITEM_ACTIVE,
            )
        else:
            self.configure(
                fg_color="transparent",
                text_color=Colors.SIDEBAR_TEXT,
                font=Fonts.SIDEBAR_ITEM,
            )


# ─────────────────────────────────────────────────────────────────────
# LOADING OVERLAY
# ─────────────────────────────────────────────────────────────────────

class LoadingOverlay(ctk.CTkFrame):
    """
    Semi-transparent overlay with an animated loading spinner.
    Place on top of content during long-running operations.
    """

    def __init__(self, parent, message: str = "Processing...", **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)

        # Semi-transparent background
        self._bg = ctk.CTkFrame(self, fg_color=Colors.BACKGROUND, corner_radius=0)
        self._bg.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Center container
        center = ctk.CTkFrame(self._bg, fg_color=Colors.CARD, corner_radius=16)
        center.place(relx=0.5, rely=0.5, anchor="center")

        # Spinner (simple rotating text)
        self._spinner_label = ctk.CTkLabel(
            center, text="⏳", font=("Segoe UI Emoji", 32),
        )
        self._spinner_label.pack(padx=40, pady=(24, 8))

        ctk.CTkLabel(
            center, text=message, font=Fonts.BODY_BOLD,
            text_color=Colors.TEXT_SECONDARY,
        ).pack(padx=40, pady=(0, 24))

        self._running = False
        self._frames = ["⏳", "⌛"]
        self._frame_idx = 0

    def show(self) -> None:
        """Show the overlay and start the spinner animation."""
        self.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.lift()
        self._running = True
        self._animate()

    def hide(self) -> None:
        """Hide the overlay and stop the animation."""
        self._running = False
        self.place_forget()

    def _animate(self) -> None:
        """Cycle through spinner frames."""
        if not self._running:
            return
        self._frame_idx = (self._frame_idx + 1) % len(self._frames)
        self._spinner_label.configure(text=self._frames[self._frame_idx])
        self.after(500, self._animate)


# ─────────────────────────────────────────────────────────────────────
# SECTION HEADER
# ─────────────────────────────────────────────────────────────────────

class SectionHeader(ctk.CTkFrame):
    """
    Page section title with a colored accent underline.

    ┌──────────────────────────┐
    │  Section Title           │
    │  ▬▬▬▬▬▬ (accent line)   │
    └──────────────────────────┘
    """

    def __init__(
        self,
        parent,
        title: str = "",
        subtitle: str = "",
        accent_color: str = Colors.PRIMARY,
        **kwargs,
    ):
        super().__init__(parent, fg_color="transparent", **kwargs)

        ctk.CTkLabel(
            self, text=title, font=Fonts.HEADING_2,
            text_color=Colors.TEXT_PRIMARY, anchor="w",
        ).pack(anchor="w")

        # Accent line
        ctk.CTkFrame(
            self, fg_color=accent_color, height=3,
            width=50, corner_radius=2,
        ).pack(anchor="w", pady=(4, 0))

        if subtitle:
            ctk.CTkLabel(
                self, text=subtitle, font=Fonts.SMALL,
                text_color=Colors.TEXT_MUTED, anchor="w",
            ).pack(anchor="w", pady=(6, 0))


# ─────────────────────────────────────────────────────────────────────
# TOOLTIP
# ─────────────────────────────────────────────────────────────────────

class ToolTip:
    """
    Hover tooltip for any widget.

    Usage:
        ToolTip(my_label, "This is a helpful tooltip")
    """

    def __init__(self, widget, text: str, delay: int = 400):
        self.widget = widget
        self.text = text
        self.delay = delay
        self._tip_window = None
        self._after_id = None

        widget.bind("<Enter>", self._schedule_show)
        widget.bind("<Leave>", self._hide)

    def _schedule_show(self, event=None) -> None:
        """Schedule tooltip display after delay."""
        self._after_id = self.widget.after(self.delay, self._show)

    def _show(self) -> None:
        """Display the tooltip window."""
        if self._tip_window:
            return

        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5

        self._tip_window = tw = ctk.CTkToplevel(self.widget)
        tw.withdraw()
        tw.overrideredirect(True)

        label = ctk.CTkLabel(
            tw, text=self.text, font=Fonts.CAPTION,
            fg_color=Colors.SIDEBAR_BG,
            text_color=Colors.TEXT_WHITE,
            corner_radius=6,
            padx=10, pady=6,
        )
        label.pack()

        tw.geometry(f"+{x}+{y}")
        tw.deiconify()

    def _hide(self, event=None) -> None:
        """Hide the tooltip window."""
        if self._after_id:
            self.widget.after_cancel(self._after_id)
            self._after_id = None
        if self._tip_window:
            self._tip_window.destroy()
            self._tip_window = None


# ─────────────────────────────────────────────────────────────────────
# SCROLLABLE CONTENT FRAME
# ─────────────────────────────────────────────────────────────────────

class ScrollableContent(ctk.CTkScrollableFrame):
    """
    Pre-configured scrollable frame for page content.
    Provides consistent padding and background.
    """

    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            fg_color=Colors.BACKGROUND,
            scrollbar_button_color=Colors.BORDER,
            scrollbar_button_hover_color=Colors.TEXT_MUTED,
            **kwargs,
        )
