#!/usr/bin/env python3
"""
Delete the audio overview from a NotebookLM notebook.

Usage:
    python delete_audio.py --notebook-id "abc123"
    python delete_audio.py --notebook-id "abc123" --confirm --json
"""

import argparse
import json
import sys
from pathlib import Path

# Add parent paths for imports
SCRIPT_DIR = Path(__file__).parent
MASTER_SCRIPTS = SCRIPT_DIR.parent.parent / "notebooklm-master" / "scripts"
sys.path.insert(0, str(MASTER_SCRIPTS))

from notebooklm_client import get_client


def delete_audio_overview(notebook_id: str) -> dict:
    """
    Delete the audio overview from a notebook.

    Args:
        notebook_id: The notebook ID

    Returns:
        dict with result (empty on success)
    """
    client = get_client()
    return client.delete(f"/notebooks/{notebook_id}/audioOverviews/default")


def main():
    parser = argparse.ArgumentParser(description="Delete audio overview from NotebookLM notebook")
    parser.add_argument("--notebook-id", required=True, help="Notebook ID")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--confirm", action="store_true", help="Skip confirmation")
    args = parser.parse_args()

    if not args.confirm:
        print(f"About to delete audio overview from notebook {args.notebook_id}")
        confirm = input("Are you sure? (yes/no): ")
        if confirm.lower() != "yes":
            print("Cancelled.")
            sys.exit(0)

    try:
        result = delete_audio_overview(args.notebook_id)

        if args.json:
            print(json.dumps({"status": "deleted"}, indent=2))
        else:
            print("Audio overview deleted successfully.")

    except Exception as e:
        if args.json:
            print(json.dumps({"error": str(e)}, indent=2))
        else:
            print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
