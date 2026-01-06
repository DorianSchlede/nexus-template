#!/usr/bin/env python3
"""
Get details of a source in a NotebookLM notebook.

Usage:
    python get_source.py --notebook-id "abc123" --source-id "source456"
    python get_source.py --notebook-id "abc123" --source-id "source456" --json
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


def get_source(notebook_id: str, source_id: str) -> dict:
    """
    Get source details.

    Args:
        notebook_id: The notebook ID
        source_id: The source ID

    Returns:
        dict with source details
    """
    client = get_client()
    return client.get(f"/notebooks/{notebook_id}/sources/{source_id}")


def main():
    parser = argparse.ArgumentParser(description="Get NotebookLM source details")
    parser.add_argument("--notebook-id", required=True, help="Notebook ID")
    parser.add_argument("--source-id", required=True, help="Source ID")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    try:
        result = get_source(args.notebook_id, args.source_id)

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"Source Details:")
            print(f"  Title: {result.get('title', 'Untitled')}")
            print(f"  Source ID: {result.get('sourceId')}")
            print(f"  Status: {result.get('status', 'N/A')}")
            if result.get('metadata'):
                meta = result['metadata']
                print(f"  Word Count: {meta.get('wordCount', 'N/A')}")
                print(f"  Token Count: {meta.get('tokenCount', 'N/A')}")

    except Exception as e:
        if args.json:
            print(json.dumps({"error": str(e)}, indent=2))
        else:
            print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
