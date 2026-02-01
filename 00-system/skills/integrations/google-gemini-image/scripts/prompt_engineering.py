#!/usr/bin/env python3
"""
Professional Prompt Engineering for AI Image Generation.

See references/ folder for documentation:
  - prompt-structure.md: The 7-part prompt structure
  - style-presets.md: Linear, Vercel, Stripe aesthetics
  - asset-templates.md: Logo, hero, social templates
  - negative-prompts.md: What to avoid per asset type
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum


class AssetType(Enum):
    """Types of brand assets with different prompt requirements."""
    LOGO = "logo"
    ICON = "icon"
    HERO = "hero"
    SOCIAL_PROFILE = "social_profile"
    SOCIAL_COVER = "social_cover"
    SOCIAL_POST = "social_post"
    PITCH_COVER = "pitch_cover"
    PITCH_DIVIDER = "pitch_divider"
    PATTERN = "pattern"
    MERCH_TSHIRT = "merch_tshirt"
    MERCH_STICKER = "merch_sticker"
    ABSTRACT = "abstract"


class StylePreset(Enum):
    """Visual style presets based on admired brands."""
    LINEAR = "linear"           # Clean, dark, minimal, dev-focused
    VERCEL = "vercel"           # Modern, geometric, high-contrast
    STRIPE = "stripe"           # Sophisticated, gradient, premium
    RAYCAST = "raycast"         # Dark, sleek, productivity
    NOTION = "notion"           # Clean, approachable, balanced
    FIGMA = "figma"             # Colorful, playful, creative
    SUPERHUMAN = "superhuman"   # Minimal, fast, premium
    ARC = "arc"                 # Bold, colorful, modern


# ============================================================================
# STYLE PRESET DEFINITIONS
# ============================================================================

STYLE_MODIFIERS: Dict[StylePreset, Dict] = {
    StylePreset.LINEAR: {
        "aesthetic": "minimal dark mode interface aesthetic, clean lines, subtle gradients",
        "composition": "centered composition, generous negative space, balanced layout",
        "lighting": "soft ambient lighting, subtle glow effects, no harsh shadows",
        "texture": "smooth matte surfaces, subtle noise texture, anti-aliased edges",
        "avoid": "clutter, bright colors, playful elements, rounded shapes",
        "reference": "inspired by Linear app design, Vercel dashboard aesthetic"
    },
    StylePreset.VERCEL: {
        "aesthetic": "modern geometric design, high contrast, bold shapes",
        "composition": "asymmetric dynamic composition, edge-to-edge elements",
        "lighting": "dramatic directional lighting, sharp highlights",
        "texture": "smooth gradients, glass morphism, subtle reflections",
        "avoid": "organic shapes, muted colors, vintage elements",
        "reference": "Vercel brand style, Next.js conference visuals"
    },
    StylePreset.STRIPE: {
        "aesthetic": "sophisticated premium design, flowing gradients, depth layers",
        "composition": "layered depth, floating elements, perspective shifts",
        "lighting": "soft diffused lighting, gradient backgrounds, ambient glow",
        "texture": "smooth blended gradients, subtle 3D depth, soft shadows",
        "avoid": "flat design, harsh edges, neon colors",
        "reference": "Stripe visual identity, fintech premium aesthetic"
    },
    StylePreset.RAYCAST: {
        "aesthetic": "dark sleek interface, productivity focused, command palette style",
        "composition": "centered focal point, clean hierarchy, minimal chrome",
        "lighting": "dark background with focused highlights, spotlight effect",
        "texture": "frosted glass, subtle blur, crisp typography areas",
        "avoid": "colorful backgrounds, decorative elements, rounded corners",
        "reference": "Raycast app design, macOS command palette aesthetic"
    }
}


# ============================================================================
# ASSET-SPECIFIC TEMPLATES
# ============================================================================

@dataclass
class PromptTemplate:
    """Template for generating specific asset types."""
    base: str
    required_modifiers: List[str]
    optional_modifiers: List[str]
    negative_prompt: str
    aspect_ratio: str
    tips: List[str]


ASSET_TEMPLATES: Dict[AssetType, PromptTemplate] = {
    AssetType.LOGO: PromptTemplate(
        base=(
            "Professional logo design, {subject}, "
            "single iconic mark, vector style, "
            "{color_primary} color on {background} background, "
            "perfectly centered, scalable at any size, "
            "clean edges, geometric precision"
        ),
        required_modifiers=["subject", "color_primary", "background"],
        optional_modifiers=["style_modifier", "brand_personality"],
        negative_prompt=(
            "text, letters, words, typography, watermark, signature, "
            "gradients, photorealistic, 3D render, multiple elements, "
            "complex details, thin lines, busy background, clipart style"
        ),
        aspect_ratio="1:1",
        tips=[
            "Describe the CONCEPT, not 'a logo of X'",
            "Use geometric terms: hexagon, circle, abstract mark",
            "Specify SINGLE mark, not multiple elements",
            "Always include 'vector style' for clean edges"
        ]
    ),

    AssetType.ICON: PromptTemplate(
        base=(
            "App icon design, {subject}, "
            "single symbol, flat design with subtle depth, "
            "{color_primary} on {background}, "
            "rounded square format, iOS/macOS style, "
            "simple recognizable shape"
        ),
        required_modifiers=["subject", "color_primary", "background"],
        optional_modifiers=["glow_effect", "gradient"],
        negative_prompt=(
            "text, letters, realistic, photograph, multiple icons, "
            "complex details, thin strokes, busy patterns"
        ),
        aspect_ratio="1:1",
        tips=[
            "Keep it SIMPLE - one main element",
            "Think about recognition at 16x16px",
            "Subtle gradients OK, but not complex"
        ]
    ),

    AssetType.HERO: PromptTemplate(
        base=(
            "Website hero section background, {subject}, "
            "wide cinematic composition, {style_aesthetic}, "
            "{color_palette}, "
            "professional marketing visual, "
            "space for text overlay on {text_area}"
        ),
        required_modifiers=["subject", "color_palette", "style_aesthetic"],
        optional_modifiers=["lighting", "depth", "particles"],
        negative_prompt=(
            "text, words, typography, UI elements, buttons, "
            "people faces, stock photo style, watermark, "
            "cluttered composition, centered focal point blocking text area"
        ),
        aspect_ratio="16:9",
        tips=[
            "Leave clear space for headline text",
            "Gradients work well for text readability",
            "Abstract > literal for flexibility",
            "Consider dark mode as primary"
        ]
    ),

    AssetType.SOCIAL_PROFILE: PromptTemplate(
        base=(
            "Social media profile picture, {subject}, "
            "circular crop friendly, centered composition, "
            "{color_primary} dominant color, {background} background, "
            "recognizable at small sizes, bold simple shapes"
        ),
        required_modifiers=["subject", "color_primary", "background"],
        optional_modifiers=["glow", "border"],
        negative_prompt=(
            "text, complex details, thin lines, "
            "elements near edges, asymmetric layout"
        ),
        aspect_ratio="1:1",
        tips=[
            "Will be cropped to circle - keep subject centered",
            "Must be recognizable at 32x32px",
            "Bold colors, simple shapes"
        ]
    ),

    AssetType.SOCIAL_COVER: PromptTemplate(
        base=(
            "Social media cover image, {subject}, "
            "ultra-wide banner composition, {style_aesthetic}, "
            "{color_palette}, "
            "abstract background pattern, "
            "clear left third for profile overlay"
        ),
        required_modifiers=["subject", "color_palette", "style_aesthetic"],
        optional_modifiers=["pattern", "gradient_direction"],
        negative_prompt=(
            "text, typography, faces, detailed imagery on left side, "
            "busy patterns, centered composition"
        ),
        aspect_ratio="3:1",  # Approximate Twitter/LinkedIn ratio
        tips=[
            "Left side will have profile picture overlay",
            "Keep important elements on right 2/3",
            "Subtle patterns > busy imagery"
        ]
    ),

    AssetType.PATTERN: PromptTemplate(
        base=(
            "Seamless tileable pattern, {subject}, "
            "{color_palette}, "
            "repeating geometric design, "
            "subtle texture, professional brand pattern"
        ),
        required_modifiers=["subject", "color_palette"],
        optional_modifiers=["density", "complexity"],
        negative_prompt=(
            "text, obvious seams, non-repeating elements, "
            "centered focal point, gradients that don't tile"
        ),
        aspect_ratio="1:1",
        tips=[
            "Think about seamless repetition",
            "Geometric patterns tile better",
            "Subtle > bold for backgrounds"
        ]
    ),

    AssetType.MERCH_TSHIRT: PromptTemplate(
        base=(
            "T-shirt print design, {subject}, "
            "{color_primary} artwork on {background} fabric, "
            "screen print style, bold graphic, "
            "centered chest placement composition"
        ),
        required_modifiers=["subject", "color_primary", "background"],
        optional_modifiers=["style", "size"],
        negative_prompt=(
            "photorealistic, complex gradients, "
            "too many colors, small details that won't print, "
            "mockup, t-shirt template, model"
        ),
        aspect_ratio="1:1",
        tips=[
            "Limited colors work better for printing",
            "Bold shapes, no tiny details",
            "Consider single-color versions"
        ]
    ),

    AssetType.ABSTRACT: PromptTemplate(
        base=(
            "Abstract digital art, {subject}, "
            "{color_palette}, "
            "{style_aesthetic}, "
            "high resolution, professional quality"
        ),
        required_modifiers=["subject", "color_palette", "style_aesthetic"],
        optional_modifiers=["lighting", "texture", "depth"],
        negative_prompt=(
            "text, words, letters, watermark, "
            "human faces, recognizable objects unless specified"
        ),
        aspect_ratio="1:1",
        tips=[
            "Abstract works best with strong color direction",
            "Describe feeling/energy, not literal objects",
            "Reference other abstract artists for style"
        ]
    )
}


# ============================================================================
# QUALITY & TECHNICAL MODIFIERS
# ============================================================================

QUALITY_MODIFIERS = {
    "ultra": "ultra high quality, 8K resolution, extreme detail, professional photography",
    "high": "high quality, detailed, sharp focus, professional",
    "standard": "good quality, clear, well-composed",
    "stylized": "artistic interpretation, stylized, creative liberty"
}

LIGHTING_MODIFIERS = {
    "studio": "professional studio lighting, soft shadows, even illumination",
    "dramatic": "dramatic lighting, strong shadows, high contrast, chiaroscuro",
    "ambient": "soft ambient lighting, natural feel, gentle shadows",
    "neon": "neon lighting, glowing edges, cyberpunk atmosphere",
    "golden": "golden hour lighting, warm tones, soft directional light",
    "dark": "low-key lighting, dark atmosphere, selective highlights"
}

COMPOSITION_MODIFIERS = {
    "centered": "centered composition, symmetrical balance, focal point in middle",
    "rule_of_thirds": "rule of thirds composition, off-center focal point",
    "dynamic": "dynamic diagonal composition, sense of movement",
    "minimal": "minimal composition, lots of negative space, breathing room",
    "full_bleed": "edge-to-edge design, no margins, immersive"
}


# ============================================================================
# NEGATIVE PROMPT LIBRARY
# ============================================================================

NEGATIVE_PROMPTS = {
    "no_text": "text, words, letters, typography, numbers, writing, captions, labels, watermark, signature, logo text",
    "no_people": "people, humans, faces, hands, figures, portraits, crowd",
    "no_stock": "stock photo, generic, cliche, overused, boring, typical",
    "no_artifacts": "artifacts, noise, grain, blur, distortion, compression, pixelation, low quality",
    "no_busy": "busy, cluttered, chaotic, messy, overcrowded, too many elements",
    "clean_logo": "text, gradients, 3D, shadows, multiple colors, complex shapes, thin lines, decorative elements"
}


# ============================================================================
# PROMPT BUILDER
# ============================================================================

@dataclass
class PromptBuilder:
    """Builds optimized prompts from components."""
    subject: str
    asset_type: AssetType
    style_preset: Optional[StylePreset] = None
    color_primary: Optional[str] = None
    color_secondary: Optional[str] = None
    color_accent: Optional[str] = None
    background: str = "dark"
    quality: str = "high"
    lighting: Optional[str] = None
    composition: Optional[str] = None
    custom_modifiers: List[str] = field(default_factory=list)
    custom_negative: List[str] = field(default_factory=list)

    def build(self) -> Dict[str, str]:
        """Build the complete prompt with positive and negative components."""
        template = ASSET_TEMPLATES.get(self.asset_type, ASSET_TEMPLATES[AssetType.ABSTRACT])

        # Build color palette description
        colors = []
        if self.color_primary:
            colors.append(f"{self.color_primary} as primary")
        if self.color_secondary:
            colors.append(f"{self.color_secondary} as secondary")
        if self.color_accent:
            colors.append(f"{self.color_accent} as accent")
        color_palette = ", ".join(colors) if colors else "harmonious color palette"

        # Get style modifiers
        style_mod = STYLE_MODIFIERS.get(self.style_preset, {})
        style_aesthetic = style_mod.get("aesthetic", "professional modern design")

        # Build the prompt
        prompt_parts = []

        # 1. Base template with substitutions
        base = template.base.format(
            subject=self.subject,
            color_primary=self.color_primary or "brand color",
            color_palette=color_palette,
            background=self.background,
            style_aesthetic=style_aesthetic,
            text_area="left or top area"
        )
        prompt_parts.append(base)

        # 2. Style modifiers
        if self.style_preset and style_mod:
            prompt_parts.append(style_mod.get("composition", ""))
            prompt_parts.append(style_mod.get("lighting", ""))
            prompt_parts.append(style_mod.get("texture", ""))

        # 3. Quality
        prompt_parts.append(QUALITY_MODIFIERS.get(self.quality, ""))

        # 4. Lighting
        if self.lighting:
            prompt_parts.append(LIGHTING_MODIFIERS.get(self.lighting, self.lighting))

        # 5. Composition
        if self.composition:
            prompt_parts.append(COMPOSITION_MODIFIERS.get(self.composition, self.composition))

        # 6. Custom modifiers
        prompt_parts.extend(self.custom_modifiers)

        # Build negative prompt
        negative_parts = [template.negative_prompt]
        if self.style_preset and style_mod:
            negative_parts.append(style_mod.get("avoid", ""))
        negative_parts.extend(self.custom_negative)

        # Clean and join
        positive = ", ".join(filter(None, prompt_parts))
        negative = ", ".join(filter(None, negative_parts))

        return {
            "prompt": positive,
            "negative": negative,
            "aspect_ratio": template.aspect_ratio,
            "tips": template.tips
        }

    def build_with_negative(self) -> str:
        """Build prompt with negative instructions embedded (for models without negative prompt support)."""
        result = self.build()
        # Embed negative as instruction
        return f"{result['prompt']}. IMPORTANT: Do NOT include: {result['negative']}"


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def logo_prompt(
    concept: str,
    primary_color: str,
    background: str = "#0F172A",
    style: StylePreset = StylePreset.LINEAR
) -> str:
    """Quick logo prompt generator."""
    builder = PromptBuilder(
        subject=concept,
        asset_type=AssetType.LOGO,
        style_preset=style,
        color_primary=primary_color,
        background=background,
        quality="ultra"
    )
    return builder.build_with_negative()


def hero_prompt(
    concept: str,
    primary_color: str,
    secondary_color: str,
    accent_color: str,
    style: StylePreset = StylePreset.LINEAR
) -> str:
    """Quick hero image prompt generator."""
    builder = PromptBuilder(
        subject=concept,
        asset_type=AssetType.HERO,
        style_preset=style,
        color_primary=primary_color,
        color_secondary=secondary_color,
        color_accent=accent_color,
        background="dark",
        quality="ultra",
        lighting="ambient"
    )
    return builder.build_with_negative()


if __name__ == "__main__":
    # Demo
    print("=== LOGO PROMPT ===")
    prompt = logo_prompt(
        concept="abstract transformation symbol, two geometric shapes merging into unified form",
        primary_color="electric purple #7C3AED",
        background="pure black #000000",
        style=StylePreset.LINEAR
    )
    print(prompt)
    print()

    print("=== HERO PROMPT ===")
    prompt = hero_prompt(
        concept="abstract visualization of chaos transforming into order, data streams",
        primary_color="electric purple #7C3AED",
        secondary_color="deep navy #1E293B",
        accent_color="cyan #06B6D4",
        style=StylePreset.LINEAR
    )
    print(prompt)
