#!/usr/bin/env python3
"""
Shared Gemini client wrapper for image generation operations.
"""

import os
import sys
from pathlib import Path
from datetime import datetime

# Check for required dependencies
try:
    from google import genai
    from google.genai import types
except ImportError:
    print("ERROR: google-genai package not installed")
    print("Install with: pip install google-genai")
    sys.exit(1)

try:
    from PIL import Image
except ImportError:
    print("ERROR: Pillow package not installed")
    print("Install with: pip install Pillow")
    sys.exit(1)


def get_client():
    """Get configured Gemini client."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY environment variable not set")
        print("\nSetup instructions:")
        print("1. Get your API key from https://aistudio.google.com/app/apikey")
        print("2. Add to .env: GEMINI_API_KEY=your-key")
        print("3. Or export: export GEMINI_API_KEY=your-key")
        sys.exit(1)

    return genai.Client(api_key=api_key)


def get_output_dir():
    """Get or create output directory for generated images."""
    # Find workspace root (where .env is)
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / ".env").exists():
            output_dir = parent / "04-workspace" / "generated-images"
            output_dir.mkdir(parents=True, exist_ok=True)
            return output_dir

    # Fallback to current directory
    output_dir = Path.cwd() / "generated-images"
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def generate_filename(prefix="gemini"):
    """Generate timestamped filename."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{timestamp}.png"


def save_image(image_data, filename=None, prefix="gemini"):
    """Save image data to file, return path."""
    from io import BytesIO

    output_dir = get_output_dir()
    if filename is None:
        filename = generate_filename(prefix)

    output_path = output_dir / filename

    # Handle different image data formats
    if hasattr(image_data, 'data'):
        # Gemini inline_data response
        image = Image.open(BytesIO(image_data.data))
    elif isinstance(image_data, bytes):
        image = Image.open(BytesIO(image_data))
    elif isinstance(image_data, Image.Image):
        image = image_data
    else:
        raise ValueError(f"Unknown image data type: {type(image_data)}")

    image.save(output_path, "PNG")
    return output_path


# Models available for image generation
MODELS = {
    "flash": "gemini-2.0-flash-exp-image-generation",
    "edit": "gemini-2.0-flash-exp",
}


def get_model(model_type="flash"):
    """Get model ID for given type."""
    return MODELS.get(model_type, MODELS["flash"])
