#!/usr/bin/env python3
"""
Refine images iteratively using Gemini.

Usage:
    uv run python refine_image.py "add more stars"
    uv run python refine_image.py "make it darker" --image specific.png
"""

import argparse
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


def get_last_image() -> Path:
    """Get the most recently generated/refined image."""
    output_dir = get_output_dir()

    # Find all generated/refined images
    images = list(output_dir.glob("*.png"))
    if not images:
        return None

    # Sort by modification time, newest first
    images.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    return images[0]


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


def refine_image(prompt: str, image_path: str = None, output_path: str = None) -> Path:
    """Refine an image using text instructions."""

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY not set")
        print("Get your key from: https://aistudio.google.com/app/apikey")
        sys.exit(1)

    # Determine which image to refine
    if image_path:
        input_path = Path(image_path)
        if not input_path.exists():
            print(f"ERROR: Image not found: {image_path}")
            sys.exit(1)
    else:
        input_path = get_last_image()
        if not input_path:
            print("ERROR: No previous image found to refine")
            print("Generate an image first with gemini-generate-image")
            print("Or specify an image with --image path/to/image.png")
            sys.exit(1)

    # Read and encode image
    with open(input_path, "rb") as f:
        image_data = f.read()

    mime_type = get_mime_type(input_path)

    client = genai.Client(api_key=api_key)

    print(f"Refining image: {input_path.name}")
    print(f"Instruction: \"{prompt}\"")

    try:
        # Create content with image and refinement instruction
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
                        types.Part(text=f"Refine this image: {prompt}")
                    ]
                )
            ],
            config=types.GenerateContentConfig(
                response_modalities=["TEXT", "IMAGE"],
            ),
        )

        # Extract refined image from response
        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:
                # Decode and save image
                refined_data = part.inline_data.data
                image = Image.open(BytesIO(refined_data))

                # Determine output path
                if output_path:
                    save_path = Path(output_path)
                    if not save_path.is_absolute():
                        save_path = get_output_dir() / save_path
                else:
                    save_path = get_output_dir() / generate_filename("refined")

                # Ensure parent directory exists
                save_path.parent.mkdir(parents=True, exist_ok=True)

                # Save image
                image.save(save_path, "PNG")
                print(f"\nRefined image saved to: {save_path}")
                return save_path

        # No image in response
        print("ERROR: No refined image returned")
        if response.candidates[0].content.parts:
            for part in response.candidates[0].content.parts:
                if hasattr(part, 'text') and part.text:
                    print(f"Response: {part.text}")
        sys.exit(1)

    except Exception as e:
        error_msg = str(e)
        if "SAFETY" in error_msg.upper():
            print("ERROR: Content blocked by safety filter")
            print("The refinement request may have triggered content policies.")
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
        description="Refine images iteratively using Gemini",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "add more detail"
  %(prog)s "make it brighter" --image previous.png
  %(prog)s "add a rainbow" --output final.png
        """
    )
    parser.add_argument("prompt", help="Refinement instructions")
    parser.add_argument("--image", "-i", help="Image to refine (default: last generated)")
    parser.add_argument("--output", "-o", help="Output filename (saved to generated-images/)")

    args = parser.parse_args()

    refine_image(args.prompt, args.image, args.output)


if __name__ == "__main__":
    main()
