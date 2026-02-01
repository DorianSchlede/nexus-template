# Color Theory for AI Image Generation

## Color Specification Rules

**ALWAYS specify colors with:**
1. **Name** + **Hex code** (e.g., "electric purple #7C3AED")
2. **Role** in composition (primary, secondary, accent, background)
3. **Relationship** to other colors (complementary, analogous, etc.)

**BAD**: "purple and blue colors"
**GOOD**: "electric purple (#7C3AED) as primary, deep navy (#1E293B) as secondary, cyan (#06B6D4) as accent"

---

## Color Psychology

| Color | Psychological Meaning | Use Cases |
|-------|----------------------|-----------|
| Purple | Transformation, magic, wisdom, creativity | Brand identity, premium products |
| Navy/Dark Blue | Trust, expertise, depth, stability | Corporate, authority, tech |
| Cyan | Technology, clarity, insights, energy | Data visualization, action items |
| Green | Growth, success, positive outcomes | Success states, confirmations |
| Amber/Orange | Attention, warmth, caution | Warnings, calls to action |
| Red/Rose | Urgency, importance, error | Error states, critical actions |

---

## Luminance and Contrast

### WCAG Contrast Requirements

| Standard | Ratio Required | For |
|----------|---------------|-----|
| AA Normal Text | 4.5:1 | Body text |
| AA Large Text | 3.0:1 | Headings 18pt+ |
| AAA Normal Text | 7.0:1 | High accessibility |
| AAA Large Text | 4.5:1 | Accessible headings |

### Dark vs Light Detection

A color is considered "dark" when its relative luminance (WCAG formula) is below 0.179. Use this to determine:
- Text color over backgrounds (white on dark, black on light)
- Icon color variations
- Overlay opacity

---

## Color Space Reference

| Format | Range | Use Case |
|--------|-------|----------|
| Hex | #000000-#FFFFFF | Web, CSS, design tools |
| RGB | 0-255 per channel | Digital displays |
| HSL | H: 0-360, S: 0-100%, L: 0-100% | Color manipulation |
| HSV | H: 0-360, S: 0-100%, V: 0-100% | Design tools |

### Hue Names by Degree

| Degrees | Hue Name |
|---------|----------|
| 0-15 | Red |
| 15-45 | Orange |
| 45-75 | Yellow |
| 75-105 | Yellow-Green |
| 105-135 | Green |
| 135-165 | Teal |
| 165-195 | Cyan |
| 195-225 | Blue |
| 225-255 | Indigo |
| 255-285 | Purple |
| 285-315 | Magenta |
| 315-345 | Pink |
| 345-360 | Red |

---

## Python Module

See `scripts/color_theory.py` for the `Color` class and palette generation functions.
