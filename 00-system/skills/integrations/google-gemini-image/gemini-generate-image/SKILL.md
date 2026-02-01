---
name: gemini-generate-image
description: "generate image, create image, text to image, gemini generate."
---

# Generate Image with Gemini

Create images from text prompts using Google's Gemini AI.

## Usage

```bash
# Basic generation
uv run python scripts/generate_image.py "a cat astronaut floating in space"

# With options
uv run python scripts/generate_image.py "sunset over mountains" --aspect 16:9

# Save to specific file
uv run python scripts/generate_image.py "abstract art" --output my_image.png
```

## Options

| Option | Values | Default | Description |
|--------|--------|---------|-------------|
| `--aspect` | 1:1, 4:3, 16:9, 9:16 | 1:1 | Aspect ratio |
| `--output` | filename | auto-generated | Output filename |

## Output

Images are saved to `04-workspace/generated-images/` with timestamp filenames unless `--output` is specified.

## Examples

```bash
# Logo concept
uv run python scripts/generate_image.py "minimalist tech logo, blue gradient"

# Marketing asset
uv run python scripts/generate_image.py "happy team working together, modern office" --aspect 16:9

# Social media
uv run python scripts/generate_image.py "motivational quote background, abstract" --aspect 9:16
```

---

*Part of google-gemini-image integration*
