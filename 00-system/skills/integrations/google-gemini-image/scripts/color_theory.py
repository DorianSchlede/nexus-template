#!/usr/bin/env python3
"""
Color Theory Engine for Brand-Aware Image Generation.

See references/ folder for documentation:
  - color-theory.md: Color psychology, specification rules
  - color-harmonies.md: Harmony types and usage
  - mutagent-brand.md: Mutagent-specific colors
"""

import colorsys
import re
from dataclasses import dataclass
from typing import List, Tuple, Optional


@dataclass
class Color:
    """Represents a color with multiple format support."""
    hex: str
    name: Optional[str] = None

    def __post_init__(self):
        # Normalize hex
        self.hex = self.hex.upper().lstrip('#')
        if len(self.hex) == 3:
            self.hex = ''.join(c*2 for c in self.hex)

    @property
    def rgb(self) -> Tuple[int, int, int]:
        """Return RGB tuple (0-255)."""
        return tuple(int(self.hex[i:i+2], 16) for i in (0, 2, 4))

    @property
    def rgb_normalized(self) -> Tuple[float, float, float]:
        """Return RGB tuple (0.0-1.0)."""
        return tuple(c / 255.0 for c in self.rgb)

    @property
    def hsl(self) -> Tuple[float, float, float]:
        """Return HSL tuple (H: 0-360, S: 0-100, L: 0-100)."""
        r, g, b = self.rgb_normalized
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        return (h * 360, s * 100, l * 100)

    @property
    def hsv(self) -> Tuple[float, float, float]:
        """Return HSV tuple (H: 0-360, S: 0-100, V: 0-100)."""
        r, g, b = self.rgb_normalized
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        return (h * 360, s * 100, v * 100)

    @property
    def luminance(self) -> float:
        """Calculate relative luminance (WCAG formula)."""
        def adjust(c):
            c = c / 255.0
            return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
        r, g, b = self.rgb
        return 0.2126 * adjust(r) + 0.7152 * adjust(g) + 0.0722 * adjust(b)

    @property
    def is_dark(self) -> bool:
        """Check if color is dark (for text contrast decisions)."""
        return self.luminance < 0.179

    @property
    def css(self) -> str:
        """Return CSS hex format."""
        return f"#{self.hex}"

    @property
    def prompt_description(self) -> str:
        """Return description for AI prompts."""
        h, s, l = self.hsl

        # Determine hue name
        hue_names = [
            (15, "red"), (45, "orange"), (75, "yellow"), (105, "yellow-green"),
            (135, "green"), (165, "teal"), (195, "cyan"), (225, "blue"),
            (255, "indigo"), (285, "purple"), (315, "magenta"), (345, "pink"), (360, "red")
        ]
        hue_name = "gray"
        if s > 10:  # Not grayscale
            for threshold, name in hue_names:
                if h <= threshold:
                    hue_name = name
                    break

        # Determine lightness descriptor
        if l < 20:
            lightness = "very dark"
        elif l < 40:
            lightness = "dark"
        elif l < 60:
            lightness = "medium"
        elif l < 80:
            lightness = "light"
        else:
            lightness = "very light"

        # Determine saturation descriptor
        if s < 20:
            saturation = "muted"
        elif s < 50:
            saturation = "soft"
        elif s < 80:
            saturation = "vibrant"
        else:
            saturation = "highly saturated"

        if self.name:
            return f"{self.name} ({lightness} {saturation} {hue_name}, {self.css})"
        return f"{lightness} {saturation} {hue_name} ({self.css})"

    def __str__(self):
        return self.css


def hex_to_color(hex_code: str, name: str = None) -> Color:
    """Create Color from hex code."""
    return Color(hex=hex_code, name=name)


def hsl_to_hex(h: float, s: float, l: float) -> str:
    """Convert HSL to hex. H: 0-360, S: 0-100, L: 0-100."""
    h = h / 360.0
    s = s / 100.0
    l = l / 100.0
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return f"#{int(r*255):02X}{int(g*255):02X}{int(b*255):02X}"


# ============================================================================
# COLOR HARMONY FUNCTIONS
# ============================================================================

def complementary(color: Color) -> Color:
    """Return complementary color (opposite on color wheel)."""
    h, s, l = color.hsl
    new_h = (h + 180) % 360
    return Color(hex=hsl_to_hex(new_h, s, l))


def analogous(color: Color, angle: float = 30) -> List[Color]:
    """Return analogous colors (adjacent on color wheel)."""
    h, s, l = color.hsl
    return [
        Color(hex=hsl_to_hex((h - angle) % 360, s, l)),
        color,
        Color(hex=hsl_to_hex((h + angle) % 360, s, l))
    ]


def triadic(color: Color) -> List[Color]:
    """Return triadic colors (equidistant on color wheel)."""
    h, s, l = color.hsl
    return [
        color,
        Color(hex=hsl_to_hex((h + 120) % 360, s, l)),
        Color(hex=hsl_to_hex((h + 240) % 360, s, l))
    ]


def split_complementary(color: Color, angle: float = 30) -> List[Color]:
    """Return split-complementary colors."""
    h, s, l = color.hsl
    comp_h = (h + 180) % 360
    return [
        color,
        Color(hex=hsl_to_hex((comp_h - angle) % 360, s, l)),
        Color(hex=hsl_to_hex((comp_h + angle) % 360, s, l))
    ]


def tetradic(color: Color) -> List[Color]:
    """Return tetradic/rectangular colors."""
    h, s, l = color.hsl
    return [
        color,
        Color(hex=hsl_to_hex((h + 90) % 360, s, l)),
        Color(hex=hsl_to_hex((h + 180) % 360, s, l)),
        Color(hex=hsl_to_hex((h + 270) % 360, s, l))
    ]


def monochromatic(color: Color, steps: int = 5) -> List[Color]:
    """Return monochromatic variations (same hue, different lightness)."""
    h, s, _ = color.hsl
    step = 80 / (steps - 1) if steps > 1 else 0
    return [
        Color(hex=hsl_to_hex(h, s, 10 + i * step))
        for i in range(steps)
    ]


def shade(color: Color, amount: float = 20) -> Color:
    """Darken color by mixing with black."""
    h, s, l = color.hsl
    return Color(hex=hsl_to_hex(h, s, max(0, l - amount)))


def tint(color: Color, amount: float = 20) -> Color:
    """Lighten color by mixing with white."""
    h, s, l = color.hsl
    return Color(hex=hsl_to_hex(h, s, min(100, l + amount)))


def desaturate(color: Color, amount: float = 20) -> Color:
    """Reduce saturation."""
    h, s, l = color.hsl
    return Color(hex=hsl_to_hex(h, max(0, s - amount), l))


def saturate(color: Color, amount: float = 20) -> Color:
    """Increase saturation."""
    h, s, l = color.hsl
    return Color(hex=hsl_to_hex(h, min(100, s + amount), l))


# ============================================================================
# CONTRAST & ACCESSIBILITY
# ============================================================================

def contrast_ratio(color1: Color, color2: Color) -> float:
    """Calculate WCAG contrast ratio between two colors."""
    l1 = color1.luminance
    l2 = color2.luminance
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


def meets_wcag_aa(foreground: Color, background: Color, large_text: bool = False) -> bool:
    """Check if color combination meets WCAG AA standards."""
    ratio = contrast_ratio(foreground, background)
    return ratio >= 3.0 if large_text else ratio >= 4.5


def meets_wcag_aaa(foreground: Color, background: Color, large_text: bool = False) -> bool:
    """Check if color combination meets WCAG AAA standards."""
    ratio = contrast_ratio(foreground, background)
    return ratio >= 4.5 if large_text else ratio >= 7.0


def best_text_color(background: Color) -> Color:
    """Return white or black based on background luminance."""
    return Color(hex="FFFFFF" if background.is_dark else "000000")


# ============================================================================
# BRAND PALETTE GENERATION
# ============================================================================

@dataclass
class BrandPalette:
    """Complete brand color palette with all necessary colors."""
    primary: Color
    secondary: Color
    accent: Color
    background_dark: Color
    background_light: Color
    text_on_dark: Color
    text_on_light: Color
    success: Color
    warning: Color
    error: Color

    def for_prompt(self, mode: str = "dark") -> str:
        """Generate color description for AI prompts."""
        if mode == "dark":
            return (
                f"Color palette: {self.primary.prompt_description} as primary, "
                f"{self.secondary.prompt_description} as secondary, "
                f"{self.accent.prompt_description} as accent, "
                f"on {self.background_dark.prompt_description} background"
            )
        else:
            return (
                f"Color palette: {self.primary.prompt_description} as primary, "
                f"{self.secondary.prompt_description} as secondary, "
                f"{self.accent.prompt_description} as accent, "
                f"on {self.background_light.prompt_description} background"
            )

    def hex_list(self) -> List[str]:
        """Return list of hex codes for easy reference."""
        return [
            self.primary.css, self.secondary.css, self.accent.css,
            self.background_dark.css, self.background_light.css
        ]


def create_tech_palette(primary_hex: str) -> BrandPalette:
    """Create a tech startup palette from a primary color."""
    primary = Color(hex=primary_hex)

    # Generate harmonious secondary (split-complementary)
    split = split_complementary(primary, 150)
    secondary = shade(split[1], 30)  # Darker, muted

    # Accent is analogous but more saturated
    accent_base = analogous(primary, 45)[2]
    accent = saturate(accent_base, 20)

    return BrandPalette(
        primary=primary,
        secondary=secondary,
        accent=accent,
        background_dark=Color(hex="0F172A", name="Slate 900"),  # Near black
        background_light=Color(hex="F8FAFC", name="Slate 50"),  # Near white
        text_on_dark=Color(hex="F1F5F9", name="Slate 100"),
        text_on_light=Color(hex="1E293B", name="Slate 800"),
        success=Color(hex="10B981", name="Emerald"),
        warning=Color(hex="F59E0B", name="Amber"),
        error=Color(hex="EF4444", name="Red")
    )


# ============================================================================
# MUTAGENT SPECIFIC PALETTE
# ============================================================================

MUTAGENT_PALETTE = BrandPalette(
    primary=Color(hex="7C3AED", name="Electric Purple"),
    secondary=Color(hex="1E293B", name="Deep Navy"),
    accent=Color(hex="06B6D4", name="Cyan"),
    background_dark=Color(hex="0F172A", name="Slate 900"),
    background_light=Color(hex="F1F5F9", name="Slate 100"),
    text_on_dark=Color(hex="F1F5F9", name="Slate 100"),
    text_on_light=Color(hex="0F172A", name="Slate 900"),
    success=Color(hex="10B981", name="Emerald"),
    warning=Color(hex="F59E0B", name="Amber"),
    error=Color(hex="F43F5E", name="Rose")
)


if __name__ == "__main__":
    # Demo
    print("=== MUTAGENT PALETTE ===")
    print(f"Primary: {MUTAGENT_PALETTE.primary.prompt_description}")
    print(f"Secondary: {MUTAGENT_PALETTE.secondary.prompt_description}")
    print(f"Accent: {MUTAGENT_PALETTE.accent.prompt_description}")
    print()
    print("For dark mode prompt:")
    print(MUTAGENT_PALETTE.for_prompt("dark"))
    print()
    print("Complementary to primary:", complementary(MUTAGENT_PALETTE.primary).css)
    print("Triadic colors:", [c.css for c in triadic(MUTAGENT_PALETTE.primary)])
