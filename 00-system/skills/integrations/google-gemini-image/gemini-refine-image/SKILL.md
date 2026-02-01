---
name: gemini-refine-image
description: "refine image, improve image, iterate image, tweak image."
---

# Refine Image with Gemini

Iteratively refine previously generated images.

## Usage

```bash
cd 03-skills/google-gemini-image

# First, generate an image
uv run python gemini-generate-image/scripts/generate_image.py "a castle on a hill"

# Then refine it (uses last generated image)
uv run python gemini-refine-image/scripts/refine_image.py "add a dragon flying above"

# Or refine a specific image
uv run python gemini-refine-image/scripts/refine_image.py "make it sunset" --image castle.png
```

## Options

| Option | Description |
|--------|-------------|
| `prompt` | Refinement instructions |
| `--image` | Specific image to refine (default: last generated) |
| `--output` | Output filename (default: auto-generated) |

## Examples

```bash
# Iterative refinement workflow
uv run python gemini-generate-image/scripts/generate_image.py "a cozy cabin"
# -> generated_20260131_123456.png

uv run python gemini-refine-image/scripts/refine_image.py "add snow on the roof"
# -> refined_20260131_123500.png

uv run python gemini-refine-image/scripts/refine_image.py "add smoke from chimney"
# -> refined_20260131_123530.png

uv run python gemini-refine-image/scripts/refine_image.py "add northern lights in sky"
# -> refined_20260131_123600.png
```

## How It Works

1. Takes the last generated/refined image (or specified image)
2. Sends it to Gemini with your refinement prompt
3. Returns the refined version
4. The refined image becomes the new "last image" for further iteration

---

*Part of google-gemini-image integration*
