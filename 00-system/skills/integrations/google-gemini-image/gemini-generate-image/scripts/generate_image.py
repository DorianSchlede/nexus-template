#!/usr/bin/env python3
"""
Generate images from text prompts using Gemini.

Usage:
    uv run python generate_image.py "your prompt here"
    uv run python generate_image.py "prompt" --aspect 16:9
    uv run python generate_image.py "prompt" --output myimage.png
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


def generate_image(prompt: str, aspect_ratio: str = "1:1", output_path: str = None) -> Path:
    """Generate an image from a text prompt."""

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY not set")
        print("Get your key from: https://aistudio.google.com/app/apikey")
        sys.exit(1)

    client = genai.Client(api_key=api_key)

    print(f"Generating image: \"{prompt}\"")
    print(f"Aspect ratio: {aspect_ratio}")

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp-image-generation",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=["TEXT", "IMAGE"],
            ),
        )

        # Extract image from response
        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:
                # Decode and save image
                image_data = part.inline_data.data
                image = Image.open(BytesIO(image_data))

                # Determine output path
                if output_path:
                    save_path = Path(output_path)
                    if not save_path.is_absolute():
                        save_path = get_output_dir() / save_path
                else:
                    save_path = get_output_dir() / generate_filename("generated")

                # Ensure parent directory exists
                save_path.parent.mkdir(parents=True, exist_ok=True)

                # Save image
                image.save(save_path, "PNG")
                print(f"\nImage saved to: {save_path}")
                return save_path

        # No image in response
        print("ERROR: No image generated")
        if response.candidates[0].content.parts:
            for part in response.candidates[0].content.parts:
                if hasattr(part, 'text') and part.text:
                    print(f"Response: {part.text}")
        sys.exit(1)

    except Exception as e:
        error_msg = str(e)
        if "SAFETY" in error_msg.upper():
            print("ERROR: Content blocked by safety filter")
            print("Try a different prompt that doesn't trigger content policies.")
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
        description="Generate images from text prompts using Gemini",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "a cat in space"
  %(prog)s "sunset over mountains" --aspect 16:9
  %(prog)s "abstract art" --output my_art.png
        """
    )
    parser.add_argument("prompt", help="Text description of the image to generate")
    parser.add_argument("--aspect", default="1:1",
                        choices=["1:1", "4:3", "16:9", "9:16"],
                        help="Aspect ratio (default: 1:1)")
    parser.add_argument("--output", "-o", help="Output filename (saved to generated-images/)")

    args = parser.parse_args()

    generate_image(args.prompt, args.aspect, args.output)


if __name__ == "__main__":
    main()
