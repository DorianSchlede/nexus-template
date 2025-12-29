#!/usr/bin/env python3
"""
Create an audio overview (podcast) for a NotebookLM notebook.

Usage:
    python create_audio.py --notebook-id "abc123"
    python create_audio.py --notebook-id "abc123" --focus "Key findings and methodology"
    python create_audio.py --notebook-id "abc123" --source-ids "s1,s2" --language "en" --json
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


def create_audio_overview(
    notebook_id: str,
    source_ids: list = None,
    focus: str = None,
    language: str = "en"
) -> dict:
    """
    Create an audio overview for a notebook.

    Args:
        notebook_id: The notebook ID
        source_ids: Optional list of source IDs to include (default: all sources)
        focus: Optional topic focus for the audio
        language: Language code (default: "en")

    Returns:
        dict with audio overview details and status
    """
    client = get_client()

    data = {}

    if source_ids:
        data["sourceIds"] = [{"id": sid} for sid in source_ids]

    if focus:
        data["episodeFocus"] = focus

    if language:
        data["languageCode"] = language

    return client.post(f"/notebooks/{notebook_id}/audioOverviews", data)


def main():
    parser = argparse.ArgumentParser(description="Create audio overview for NotebookLM notebook")
    parser.add_argument("--notebook-id", required=True, help="Notebook ID")
    parser.add_argument("--source-ids", help="Comma-separated source IDs (default: all sources)")
    parser.add_argument("--focus", help="Topic focus for the audio overview")
    parser.add_argument("--language", default="en", help="Language code (default: en)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    source_ids = None
    if args.source_ids:
        source_ids = [sid.strip() for sid in args.source_ids.split(",")]

    try:
        result = create_audio_overview(
            args.notebook_id,
            source_ids=source_ids,
            focus=args.focus,
            language=args.language
        )

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            audio = result.get("audioOverview", {})
            status = audio.get("status", "UNKNOWN")

            print(f"Audio Overview Request Submitted!")
            print(f"  Notebook ID: {args.notebook_id}")
            print(f"  Audio ID: {audio.get('audioOverviewId', 'N/A')}")
            print(f"  Status: {status}")

            if status == "AUDIO_OVERVIEW_STATUS_IN_PROGRESS":
                print()
                print("  Note: Audio generation takes 5-15 minutes.")
                print("  The audio will be available in the NotebookLM web interface when ready.")

    except Exception as e:
        if args.json:
            print(json.dumps({"error": str(e)}, indent=2))
        else:
            print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
