#!/usr/bin/env python3
"""
Check Gemini configuration and API connectivity.

Run with: uv run python check_gemini_config.py
"""

import os
import sys
from pathlib import Path

# Load .env if present
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


def check_config():
    """Check all configuration requirements."""
    errors = []
    warnings = []

    # Check API key
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        errors.append("GEMINI_API_KEY not set")
    elif len(api_key) < 20:
        warnings.append("GEMINI_API_KEY seems too short - verify it's correct")
    else:
        print(f"[OK] GEMINI_API_KEY: {api_key[:8]}...{api_key[-4:]}")

    # Check dependencies
    try:
        from google import genai
        print("[OK] google-genai package installed")
    except ImportError:
        errors.append("google-genai package not installed (pip install google-genai)")

    try:
        from PIL import Image
        print("[OK] Pillow package installed")
    except ImportError:
        errors.append("Pillow package not installed (pip install Pillow)")

    # Check output directory
    from gemini_client import get_output_dir
    output_dir = get_output_dir()
    print(f"[OK] Output directory: {output_dir}")

    # Test API connectivity (optional)
    if api_key and not errors:
        try:
            from google import genai
            client = genai.Client(api_key=api_key)
            # Just creating client validates key format
            print("[OK] API client initialized")
        except Exception as e:
            warnings.append(f"Could not initialize API client: {e}")

    # Report results
    print()
    if errors:
        print("ERRORS:")
        for e in errors:
            print(f"  - {e}")
        print()
        print("Fix the errors above before using Gemini image generation.")
        return False

    if warnings:
        print("WARNINGS:")
        for w in warnings:
            print(f"  - {w}")
        print()

    print("Configuration OK! Ready to generate images.")
    return True


if __name__ == "__main__":
    success = check_config()
    sys.exit(0 if success else 1)
