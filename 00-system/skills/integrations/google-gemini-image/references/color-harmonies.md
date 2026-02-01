# Color Harmonies

Color harmonies are combinations that work well together based on their positions on the color wheel.

---

## Harmony Types

### Complementary
**Definition**: Colors opposite on the wheel (180 degrees apart)

**Example**: Purple and Yellow

**Use When**:
- Need high contrast
- Want to draw attention
- Creating visual tension or energy

**Tip**: Use one color as dominant (70%), the other as accent (30%)

---

### Analogous
**Definition**: Colors adjacent on the wheel (typically 30 degrees apart)

**Example**: Purple, Blue, Indigo

**Use When**:
- Creating harmonious, cohesive designs
- Subtle, unified appearance desired
- Background gradients

**Tip**: Works best with 3 colors, one dominant

---

### Triadic
**Definition**: Three colors equally spaced (120 degrees apart)

**Example**: Purple, Orange, Green

**Use When**:
- Need vibrant, balanced design
- Creating playful, energetic visuals
- Equal emphasis on multiple elements

**Tip**: Let one dominate, use others as accents

---

### Split-Complementary
**Definition**: Base color + two colors adjacent to its complement

**Example**: Purple + Yellow-Green + Yellow-Orange

**Use When**:
- Want contrast without tension
- More sophisticated than complementary
- Dynamic but balanced compositions

**Tip**: The base color typically dominates

---

### Tetradic (Rectangular)
**Definition**: Four colors in two complementary pairs (90 degrees apart)

**Example**: Purple, Cyan, Yellow, Orange

**Use When**:
- Complex, rich color schemes needed
- Multiple distinct elements to highlight
- Bold, varied compositions

**Tip**: Works best with one dominant color, others as accents

---

### Monochromatic
**Definition**: One hue with varying lightness and saturation

**Example**: Dark Purple, Purple, Light Purple, Lavender

**Use When**:
- Elegant, sophisticated design
- Unified, focused appearance
- Minimalist aesthetics

**Tip**: Add depth with 5+ lightness variations

---

## Modification Functions

| Function | Effect | Use Case |
|----------|--------|----------|
| `shade()` | Darken (mix with black) | Shadows, depth |
| `tint()` | Lighten (mix with white) | Highlights, hover states |
| `desaturate()` | Reduce saturation | Muted versions, disabled states |
| `saturate()` | Increase saturation | Emphasis, vibrant accents |

---

## Python Module

See `scripts/color_theory.py` for harmony functions:
- `complementary(color)` - Returns opposite color
- `analogous(color, angle=30)` - Returns 3 adjacent colors
- `triadic(color)` - Returns 3 equidistant colors
- `split_complementary(color, angle=30)` - Returns split-comp trio
- `tetradic(color)` - Returns 4 rectangular colors
- `monochromatic(color, steps=5)` - Returns lightness variations
