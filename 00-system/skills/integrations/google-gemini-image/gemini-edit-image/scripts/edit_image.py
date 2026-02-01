#!/usr/bin/env python3
"""
Edit images using Gemini with text instructions.

Usage:
    uv run python edit_image.py input.png "make the sky blue"
    uv run python edit_image.py input.png "add a hat" --output output.png
"""

import argparse
import base64
import os
import sys
from pathlib import Path
from io import BytesIO

# Add parent scripts directory to path for shared modules
scripts_dir = Path(__file__).resolve().parent.parent.parent / "scripts"
sys.path.insert(0, str(scripts_dir))

# Load .env
env_path = Path(__file__).resolve()
for parent in env_path.parents:
    env_file = parent / ".env"
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    os.environ.setdefault(key.strip(), value.strip())
        break

from google import genai
from google.genai import types
from PIL import Image

from gemini_client import get_output_dir, generate_filename


def get_mime_type(path: Path) -> str:
    """Get MIME type from file extension."""
    ext = path.suffix.lower()
    mime_types = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
    }
    return mime_types.get(ext, "image/png")


def edit_image(image_path: str, prompt: str, output_path: str = None) -> Path:
    """Edit an image using text instructions."""

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY not set")
        print("Get your key from: https://aistudio.google.com/app/apikey")
        sys.exit(1)

    # Validate input image
    input_path = Path(image_path)
    if not input_path.exists():
        print(f"ERROR: Image not found: {image_path}")
        sys.exit(1)

    # Read and encode image
    with open(input_path, "rb") as f:
        image_data = f.read()

    mime_type = get_mime_type(input_path)

    client = genai.Client(api_key=api_key)

    print(f"Editing image: {input_path.name}")
    print(f"Instruction: \"{prompt}\"")

    try:
        # Create content with image and edit instruction
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=[
                types.Content(
                    parts=[
                        types.Part(
                            inline_data=types.Blob(
                                mime_type=mime_type,
                                data=image_data
                            )
                        ),
                        types.Part(text=f"Edit this image: {prompt}")
                    ]
                )
            ],
            config=types.GenerateContentConfig(
                response_modalities=["TEXT", "IMAGE"],
            ),
        )

        # Extract edited image from response
        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:
                # Decode and save image
                edited_data = part.inline_data.data
                image = Image.open(BytesIO(edited_data))

                # Determine output path
                if output_path:
                    save_path = Path(output_path)
                    if not save_path.is_absolute():
                        save_path = get_output_dir() / save_path
                else:
                    save_path = get_output_dir() / generate_filename("edited")

                # Ensure parent directory exists
                save_path.parent.mkdir(parents=True, exist_ok=True)

                # Save image
                image.save(save_path, "PNG")
                print(f"\nEdited image saved to: {save_path}")
                return save_path

        # No image in response
        print("ERROR: No edited image returned")
        if response.candidates[0].content.parts:
            for part in response.candidates[0].content.parts:
                if hasattr(part, 'text') and part.text:
                    print(f"Response: {part.text}")
        sys.exit(1)

    except Exception as e:
        error_msg = str(e)
        if "SAFETY" in error_msg.upper():
            print("ERROR: Content blocked by safety filter")
            print("The edit request may have triggered content policies.")
        elif "RATE" in error_msg.upper() or "QUOTA" in error_msg.upper():
            print("ERROR: Rate limit exceeded")
            print("Wait a moment and try again.")
        elif "API_KEY" in error_msg.upper() or "AUTHENTICATION" in error_msg.upper():
            print("ERROR: Invalid API key")
            print("Check your GEMINI_API_KEY in .env")
        else:
            print(f"ERROR: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Edit images using Gemini with text instructions",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s photo.png "make it brighter"
  %(prog)s scene.jpg "add clouds to the sky"
  %(prog)s portrait.png "convert to sketch style" --output sketch.png
        """
    )
    parser.add_argument("image_path", help="Path to the image to edit")
    parser.add_argument("prompt", help="Text instructions for how to edit the image")
    parser.add_argument("--output", "-o", help="Output filename (saved to generated-images/)")

    args = parser.parse_args()

    edit_image(args.image_path, args.prompt, args.output)


if __name__ == "__main__":
    main()
