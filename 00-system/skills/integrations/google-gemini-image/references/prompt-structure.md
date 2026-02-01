# Prompt Structure for AI Image Generation

## The 7-Part Structure

AI models weight earlier words more heavily. Structure prompts in this priority order:

```
1. SUBJECT     - What is the main focus (be specific)
2. STYLE       - Artistic style, medium, technique
3. COMPOSITION - Layout, framing, perspective
4. LIGHTING    - Light source, quality, atmosphere
5. COLOR       - Specific colors with hex codes
6. QUALITY     - Resolution, detail level
7. NEGATIVE    - What NOT to include (CRITICAL)
```

---

## Golden Rules

1. **Front-load important details** - Put the most critical elements first
2. **Be specific, not vague** - "electric purple #7C3AED" not "purple"
3. **Use concrete nouns** - "hexagonal node" not "tech shape"
4. **Reference known styles** - "Linear app aesthetic" not "modern"
5. **ALWAYS include negative prompt** - Especially "no text, no letters"
6. **Describe the CONCEPT** - Not "a logo of X" but the actual shape

---

## Quality Modifiers

| Level | Description |
|-------|-------------|
| ultra | "ultra high quality, 8K resolution, extreme detail, professional photography" |
| high | "high quality, detailed, sharp focus, professional" |
| standard | "good quality, clear, well-composed" |
| stylized | "artistic interpretation, stylized, creative liberty" |

---

## Lighting Modifiers

| Style | Description |
|-------|-------------|
| studio | "professional studio lighting, soft shadows, even illumination" |
| dramatic | "dramatic lighting, strong shadows, high contrast, chiaroscuro" |
| ambient | "soft ambient lighting, natural feel, gentle shadows" |
| neon | "neon lighting, glowing edges, cyberpunk atmosphere" |
| golden | "golden hour lighting, warm tones, soft directional light" |
| dark | "low-key lighting, dark atmosphere, selective highlights" |

---

## Composition Modifiers

| Style | Description |
|-------|-------------|
| centered | "centered composition, symmetrical balance, focal point in middle" |
| rule_of_thirds | "rule of thirds composition, off-center focal point" |
| dynamic | "dynamic diagonal composition, sense of movement" |
| minimal | "minimal composition, lots of negative space, breathing room" |
| full_bleed | "edge-to-edge design, no margins, immersive" |

---

## Example Prompt Assembly

```
[SUBJECT] Professional logo mark, abstract transformation symbol showing
two geometric shapes merging into one unified form

[STYLE] vector style flat design, minimal sophisticated design,
inspired by Linear and Vercel logo aesthetics

[COMPOSITION] perfectly centered, scalable at any size

[LIGHTING] (implied by style - no harsh shadows)

[COLOR] electric purple (#7C3AED) on pure black (#000000) background

[QUALITY] clean geometric edges, sharp vectors

[NEGATIVE] IMPORTANT: Do NOT include any text, letters, words,
typography, or watermarks.
```

---

## Python Module

See `scripts/prompt_engineering.py` for the `PromptBuilder` class and template system.
