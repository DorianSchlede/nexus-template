# Mutagent Brand Guidelines

Brand-specific colors, identity, and visual direction for Mutagent assets.

---

## Brand Colors

| Role | Name | Hex | Usage |
|------|------|-----|-------|
| Primary | Electric Purple | #7C3AED | Main brand color, logos, CTAs |
| Secondary | Deep Navy | #1E293B | Supporting elements, backgrounds |
| Accent | Cyan | #06B6D4 | Data highlights, energy, links |
| Success | Emerald | #10B981 | Positive states, confirmations |
| Warning | Amber | #F59E0B | Caution, attention needed |
| Error | Rose | #F43F5E | Error states, critical |
| BG Dark | Slate 900 | #0F172A | Primary dark mode background |
| BG Light | Slate 100 | #F1F5F9 | Light mode background |
| Text Dark | Slate 100 | #F1F5F9 | Text on dark backgrounds |
| Text Light | Slate 900 | #0F172A | Text on light backgrounds |

---

## Brand Identity

| Element | Value |
|---------|-------|
| **Archetypes** | Magician (primary) + Sage (secondary) |
| **Personality** | "The Transformative Expert" |
| **Vision** | "A world where every AI agent maintains itself" |
| **Battle Cry** | "Build the future. We'll maintain the present." |
| **Villain** | Uncertainty |

---

## Color Psychology Alignment

| Color | Meaning | Brand Alignment |
|-------|---------|-----------------|
| Purple #7C3AED | Transformation, magic, wisdom | Magician archetype - core identity |
| Navy #1E293B | Trust, expertise, depth | Sage archetype - authority |
| Cyan #06B6D4 | Technology, clarity, insights | Anti-uncertainty, data |

---

## Visual Direction

- **Mode**: Dark mode primary (Slate 900 background)
- **Aesthetic**: Linear/Vercel inspired - minimal, clean, sophisticated
- **Typography**: Inter (for actual designs)
- **Feel**: Magical expertise - transformation through intelligence

---

## Visual Themes

Use these concepts in Mutagent imagery:

| Theme | Description |
|-------|-------------|
| Transformation | Chaos to Order, Broken to Fixed |
| Continuous improvement | Loops, cycles, upward spirals |
| Data/Insights | Flowing streams, connected nodes, light emerging |
| AI Agents | Network nodes, processing cores, neural connections |
| Clarity from uncertainty | Fog clearing, focus sharpening |

---

## Logo Concepts

1. **Transformation Mark**: Two shapes morphing into one (mutation)
2. **Agent Core**: Hexagonal neural node with connecting points
3. **Insight Spark**: Energy burst representing the "aha" moment
4. **Mutation Helix**: Stylized DNA strand evolving
5. **Infinite Loop**: Mobius strip representing continuous improvement

---

## What to AVOID

- Generic "AI brain" imagery
- Stock photo style
- Overly literal robot imagery
- Bright/neon cyberpunk aesthetic (dated)
- 80s synthwave grids (dated)
- Cluttered compositions
- Text baked into images (use overlays instead)

---

## File Organization

```
04-workspace/09-brand/mutagent/assets/concepts/
├── logos/       # L1-concept-name.png
├── hero/        # H1-concept-name.png
├── social/      # S1-profile.png, C1-cover.png
├── pitch/       # P1-cover.png, D1-divider.png
├── merch/       # M1-tshirt.png
├── patterns/    # Pattern1-name.png
└── icons/       # I1-name.png
```

---

## Python Reference

The Mutagent palette is defined in `scripts/color_theory.py`:

```python
from scripts.color_theory import MUTAGENT_PALETTE

# Access colors
MUTAGENT_PALETTE.primary.css      # "#7C3AED"
MUTAGENT_PALETTE.accent.css       # "#06B6D4"
MUTAGENT_PALETTE.for_prompt("dark")  # Full prompt description
```
