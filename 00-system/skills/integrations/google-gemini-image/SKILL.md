---
name: google-gemini-image
description: "gemini image, generate image, create image, text to image, brand assets, logo generation, hero image."
priority: MUST_LOAD_BEFORE_GENERATION
---

# Google Gemini Image Generation

Generate brand-consistent images using AI with color theory and prompt engineering.

## Quick Start

```bash
cd 03-skills/google-gemini-image
uv run python gemini-generate-image/scripts/generate_image.py "PROMPT" --output "path.png"
uv run python gemini-generate-image/scripts/generate_image.py "PROMPT" --aspect 16:9 --output "path.png"
```

---

## Reference Documentation

| Topic | File | Description |
|-------|------|-------------|
| Color Theory | [color-theory.md](references/color-theory.md) | Color psychology, specification rules, contrast |
| Color Harmonies | [color-harmonies.md](references/color-harmonies.md) | Complementary, triadic, analogous, etc. |
| Prompt Structure | [prompt-structure.md](references/prompt-structure.md) | The 7-part prompt structure, golden rules |
| Style Presets | [style-presets.md](references/style-presets.md) | Linear, Vercel, Stripe, Raycast aesthetics |
| Asset Templates | [asset-templates.md](references/asset-templates.md) | Logo, hero, social, pattern, merch templates |
| Negative Prompts | [negative-prompts.md](references/negative-prompts.md) | What to avoid per asset type |
| Mutagent Brand | [mutagent-brand.md](references/mutagent-brand.md) | Mutagent-specific colors and guidelines |

---

## Mutagent Colors (Quick Reference)

| Role | Color | Hex |
|------|-------|-----|
| Primary | Electric Purple | #7C3AED |
| Secondary | Deep Navy | #1E293B |
| Accent | Cyan | #06B6D4 |
| BG Dark | Slate 900 | #0F172A |
| BG Light | Slate 100 | #F1F5F9 |
| Success | Emerald | #10B981 |
| Warning | Amber | #F59E0B |
| Error | Rose | #F43F5E |

---

## Asset Types & Ratios

| Type | Ratio | Use Case |
|------|-------|----------|
| Logo | 1:1 | Brand mark, favicon |
| Icon | 1:1 | App icons |
| Hero | 16:9 | Website headers |
| Social Profile | 1:1 | Avatar (circular crop) |
| Social Cover | 3:1 | Banner/header |
| Pattern | 1:1 | Tileable backgrounds |
| T-Shirt | 1:1 | Screen print graphic |

---

## Style Presets (Quick Reference)

| Style | Aesthetic |
|-------|-----------|
| **LINEAR** | Minimal dark mode, clean lines, subtle gradients |
| **VERCEL** | Modern geometric, high contrast, bold shapes |
| **STRIPE** | Sophisticated premium, flowing gradients, depth |
| **RAYCAST** | Dark sleek, productivity focused, command palette |

---

## Negative Prompts (Essential)

**Always include for logos/icons:**
```
text, letters, words, typography, watermark, gradients, 3D, complex details
```

**Always include for hero/marketing:**
```
text, words, UI elements, buttons, faces, stock photo style
```

---

## Pre-Generation Checklist

- [ ] Identified asset type and aspect ratio
- [ ] Have specific hex codes ready
- [ ] Know target style (Linear, Vercel, etc.)
- [ ] Prepared appropriate negative prompt
- [ ] Read relevant reference file for template

---

## Python Modules

### Color Theory
```python
from scripts.color_theory import Color, MUTAGENT_PALETTE, complementary

# Access Mutagent colors
MUTAGENT_PALETTE.primary.css  # "#7C3AED"

# Generate harmonies
complement = complementary(MUTAGENT_PALETTE.primary)
```

### Prompt Builder
```python
from scripts.prompt_engineering import PromptBuilder, AssetType, StylePreset

builder = PromptBuilder(
    subject="abstract transformation symbol",
    asset_type=AssetType.LOGO,
    style_preset=StylePreset.LINEAR,
    color_primary="electric purple #7C3AED",
    background="pure black #000000"
)
result = builder.build()  # Returns dict with prompt, negative, aspect_ratio
```

---

## Convenience Functions

```python
from scripts.prompt_engineering import logo_prompt, hero_prompt

# Quick logo generation
prompt = logo_prompt(
    concept="geometric transformation mark",
    primary_color="electric purple #7C3AED",
    background="#000000",
    style=StylePreset.LINEAR
)

# Quick hero generation
prompt = hero_prompt(
    concept="abstract data streams transforming",
    primary_color="#7C3AED",
    secondary_color="#1E293B",
    accent_color="#06B6D4",
    style=StylePreset.LINEAR
)
```

---

## Output Organization

```
04-workspace/09-brand/[brand]/assets/concepts/
├── logos/     L1-concept-name.png
├── hero/      H1-concept-name.png
├── social/    S1-profile.png
├── patterns/  Pattern1-name.png
└── merch/     M1-tshirt.png
```

---

## Sub-Skills

| Skill | Purpose |
|-------|---------|
| gemini-generate-image | Create new images from prompts |
| gemini-edit-image | Modify existing images |
| gemini-refine-image | Iteratively improve images |

---

*For detailed documentation, see the [references/](references/) folder.*
