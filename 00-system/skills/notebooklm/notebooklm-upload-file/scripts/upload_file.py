#!/usr/bin/env python3
"""
Upload a file to a NotebookLM notebook as a source.

Supports: PDF, TXT, MD, DOCX, PPTX, XLSX, MP3, WAV, AAC, OGG, PNG, JPG, JPEG

Usage:
    python upload_file.py --notebook-id "abc123" --file "/path/to/document.pdf"
    python upload_file.py --notebook-id "abc123" --file "paper.pdf" --json
"""

import argparse
import json
import mimetypes
import sys
from pathlib import Path

# Add parent paths for imports
SCRIPT_DIR = Path(__file__).parent
MASTER_SCRIPTS = SCRIPT_DIR.parent.parent / "notebooklm-master" / "scripts"
sys.path.insert(0, str(MASTER_SCRIPTS))

from notebooklm_client import get_client

# Supported file types and their MIME types
SUPPORTED_TYPES = {
    # Documents
    ".pdf": "application/pdf",
    ".txt": "text/plain",
    ".md": "text/markdown",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    # Audio
    ".mp3": "audio/mpeg",
    ".wav": "audio/wav",
    ".aac": "audio/aac",
    ".ogg": "audio/ogg",
    ".flac": "audio/flac",
    ".m4a": "audio/mp4",
    # Images
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
}


def get_content_type(file_path: Path) -> str:
    """Get the MIME type for a file."""
    suffix = file_path.suffix.lower()
    if suffix in SUPPORTED_TYPES:
        return SUPPORTED_TYPES[suffix]

    # Fallback to mimetypes
    content_type, _ = mimetypes.guess_type(str(file_path))
    if content_type:
        return content_type

    return "application/octet-stream"


def upload_file(notebook_id: str, file_path: str) -> dict:
    """
    Upload a file as a source.

    Args:
        notebook_id: The notebook ID
        file_path: Path to the file

    Returns:
        dict with source details
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    suffix = path.suffix.lower()
    if suffix not in SUPPORTED_TYPES:
        raise ValueError(f"Unsupported file type: {suffix}. Supported: {', '.join(SUPPORTED_TYPES.keys())}")

    content_type = get_content_type(path)
    client = get_client()

    return client.post_file(f"/notebooks/{notebook_id}/sources:uploadFile", str(path), content_type)


def main():
    parser = argparse.ArgumentParser(description="Upload file to NotebookLM notebook")
    parser.add_argument("--notebook-id", required=True, help="Notebook ID")
    parser.add_argument("--file", required=True, help="Path to file")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    file_path = Path(args.file)

    try:
        result = upload_file(args.notebook_id, args.file)

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"File uploaded successfully!")
            print(f"  File: {file_path.name}")
            if "sourceId" in result:
                print(f"  Source ID: {result.get('sourceId')}")

    except FileNotFoundError as e:
        if args.json:
            print(json.dumps({"error": str(e)}, indent=2))
        else:
            print(f"Error: {e}")
        sys.exit(1)
    except ValueError as e:
        if args.json:
            print(json.dumps({"error": str(e)}, indent=2))
        else:
            print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        if args.json:
            print(json.dumps({"error": str(e)}, indent=2))
        else:
            print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
