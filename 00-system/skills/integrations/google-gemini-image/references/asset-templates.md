# Asset-Specific Templates

Templates optimized for each asset type with aspect ratios, tips, and example prompts.

---

## LOGO (1:1)

**Template**:
```
Professional logo mark, [CONCEPT DESCRIPTION],
single iconic symbol, vector style flat design,
[PRIMARY COLOR with hex] on [BACKGROUND COLOR with hex],
perfectly centered, scalable at any size,
clean geometric edges, minimal design,
inspired by Linear and Vercel logo aesthetics.
IMPORTANT: Do NOT include any text, letters, words, or typography.
```

**Tips**:
- Describe the CONCEPT, not "a logo of X"
- Use geometric terms: hexagon, circle, abstract mark
- Specify SINGLE mark, not multiple elements
- Always include "vector style" for clean edges

**Example**:
```
Professional logo mark, abstract transformation symbol showing
two geometric shapes morphing and merging into one unified form,
single iconic symbol, vector style flat design,
electric purple (#7C3AED) on pure black (#000000),
perfectly centered, scalable at any size,
clean geometric edges, minimal sophisticated design.
IMPORTANT: Do NOT include any text, letters, words, or typography.
```

---

## ICON (1:1)

**Template**:
```
App icon design, [SUBJECT],
single symbol, flat design with subtle depth,
[COLOR] on [BACKGROUND],
rounded square format, iOS/macOS style,
simple recognizable shape.
IMPORTANT: No text, no complex details.
```

**Tips**:
- Keep it SIMPLE - one main element
- Think about recognition at 16x16px
- Subtle gradients OK, but not complex

---

## HERO (16:9)

**Template**:
```
Website hero section background, [CONCEPT],
ultra-wide cinematic composition,
[STYLE AESTHETIC description],
color palette: [PRIMARY] as primary, [SECONDARY] as secondary, [ACCENT] as accent,
on [BACKGROUND] background,
professional marketing visual with space for text overlay,
clear area on left/top for headline placement.
IMPORTANT: Do NOT include any text, words, UI elements, or buttons.
```

**Tips**:
- Leave clear space for headline text
- Gradients work well for text readability
- Abstract > literal for flexibility
- Consider dark mode as primary

---

## SOCIAL PROFILE (1:1)

**Template**:
```
Social media profile picture,
[SYMBOL/LOGO DESCRIPTION],
perfectly centered composition for circular crop,
[COLOR] dominant color on [BACKGROUND],
bold simple shape recognizable at 32x32 pixels,
clean edges, no fine details.
IMPORTANT: No text, keep subject centered away from edges.
```

**Tips**:
- Will be cropped to circle - keep subject centered
- Must be recognizable at 32x32px
- Bold colors, simple shapes

---

## SOCIAL COVER (3:1)

**Template**:
```
Social media cover banner,
[ABSTRACT PATTERN/VISUAL],
ultra-wide horizontal composition,
keep left third empty for profile picture overlay,
[COLOR PALETTE description],
subtle gradient or pattern, not busy.
IMPORTANT: No text, no detailed imagery on left side.
```

**Tips**:
- Left side will have profile picture overlay
- Keep important elements on right 2/3
- Subtle patterns > busy imagery

---

## PATTERN (1:1)

**Template**:
```
Seamless tileable pattern,
[PATTERN DESCRIPTION],
[COLOR PALETTE],
subtle density suitable for background use,
repeating design that tiles perfectly.
IMPORTANT: No obvious seams, no centered focal points.
```

**Tips**:
- Think about seamless repetition
- Geometric patterns tile better
- Subtle > bold for backgrounds

---

## MERCH T-SHIRT (1:1)

**Template**:
```
T-shirt print design ready for screen printing,
[GRAPHIC CONCEPT],
[COLOR] artwork designed for [FABRIC COLOR] fabric,
bold graphic with clean edges,
limited color palette (2-3 colors max),
centered chest placement composition.
IMPORTANT: No mockup, no t-shirt template, just the graphic design.
```

**Tips**:
- Limited colors work better for printing
- Bold shapes, no tiny details
- Consider single-color versions

---

## ABSTRACT (1:1)

**Template**:
```
Abstract digital art, [CONCEPT],
[COLOR PALETTE],
[STYLE AESTHETIC],
high resolution, professional quality.
IMPORTANT: No text, no recognizable objects unless specified.
```

**Tips**:
- Abstract works best with strong color direction
- Describe feeling/energy, not literal objects
- Reference other abstract artists for style

---

## Python Module

See `scripts/prompt_engineering.py` for:
- `AssetType` enum
- `PromptTemplate` dataclass
- `ASSET_TEMPLATES` dictionary
- `PromptBuilder` class for automated prompt assembly
