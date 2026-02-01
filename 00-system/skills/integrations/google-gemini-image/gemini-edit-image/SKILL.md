---
name: gemini-edit-image
description: "edit image, modify image, change image, gemini edit."
---

# Edit Image with Gemini

Modify existing images using text instructions.

## Usage

```bash
cd 03-skills/google-gemini-image

# Edit an image
uv run python gemini-edit-image/scripts/edit_image.py input.png "make the sky purple"

# Save to specific file
uv run python gemini-edit-image/scripts/edit_image.py photo.jpg "add sunglasses" --output cool_photo.png
```

## Options

| Option | Description |
|--------|-------------|
| `image_path` | Path to the image to edit |
| `prompt` | Text instructions for how to modify the image |
| `--output` | Output filename (default: auto-generated) |

## Examples

```bash
# Color adjustment
uv run python gemini-edit-image/scripts/edit_image.py photo.png "make it warmer, more orange tones"

# Add elements
uv run python gemini-edit-image/scripts/edit_image.py scene.png "add a rainbow in the sky"

# Style transfer
uv run python gemini-edit-image/scripts/edit_image.py portrait.jpg "convert to oil painting style"

# Remove elements
uv run python gemini-edit-image/scripts/edit_image.py photo.png "remove the person in the background"
```

## Supported Formats

- Input: PNG, JPEG, WebP
- Output: PNG

---

*Part of google-gemini-image integration*
