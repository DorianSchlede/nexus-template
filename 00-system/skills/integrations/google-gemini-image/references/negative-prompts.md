# Negative Prompt Library

Negative prompts tell the AI what NOT to include. Critical for clean, professional output.

---

## By Category

### No Text
```
text, words, letters, typography, numbers, writing, captions, labels, watermark, signature, logo text
```

### No People
```
people, humans, faces, hands, figures, portraits, crowd
```

### No Stock Photo Style
```
stock photo, generic, cliche, overused, boring, typical
```

### No Artifacts
```
artifacts, noise, grain, blur, distortion, compression, pixelation, low quality
```

### No Clutter
```
busy, cluttered, chaotic, messy, overcrowded, too many elements
```

### Clean Logo Specific
```
text, gradients, 3D, shadows, multiple colors, complex shapes, thin lines, decorative elements
```

---

## By Asset Type

### LOGO / ICON
```
text, letters, words, typography, watermark, signature, gradients,
photorealistic, 3D render, multiple elements, complex details,
thin lines, busy background, clipart style
```

### HERO / MARKETING
```
text, words, typography, UI elements, buttons, people faces,
stock photo style, watermark, cluttered composition,
centered focal point blocking text area
```

### SOCIAL MEDIA
```
text, complex details, thin lines, elements near edges,
asymmetric layout (for profile), detailed imagery on left side (for cover)
```

### PATTERN
```
text, obvious seams, non-repeating elements,
centered focal point, gradients that don't tile
```

### MERCH / PRINT
```
photorealistic, complex gradients, too many colors,
small details that won't print, mockup template, model
```

### ABSTRACT
```
text, words, letters, watermark, human faces,
recognizable objects unless specified
```

---

## Universal Negative (Add to Everything)
```
blurry, low quality, distorted, artifacts, noise, watermark
```

---

## Iteration Fixes

| Problem | Add to Negative |
|---------|-----------------|
| Unwanted text appearing | "no text, no letters, no words, no typography, no writing, no captions" |
| Stock photo look | "not stock photo, not generic, not cliche, unique" |
| Too busy/cluttered | "not cluttered, minimal, clean composition" |
| Poor quality | "not blurry, not low quality, sharp, clear" |
| Wrong style | Add specific style elements to avoid |
| Weird artifacts | "no artifacts, no distortion, no noise, no compression" |

---

## Python Module

See `scripts/prompt_engineering.py` for:
- `NEGATIVE_PROMPTS` dictionary
- Template-specific negative prompts in `ASSET_TEMPLATES`
