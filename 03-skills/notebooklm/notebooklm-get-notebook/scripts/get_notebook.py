#!/usr/bin/env python3
"""
Get details of a specific NotebookLM notebook.

Usage:
    python get_notebook.py --notebook-id "abc123"
    python get_notebook.py --notebook-id "abc123" --json
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


def get_notebook(notebook_id: str) -> dict:
    """
    Get notebook details.

    Args:
        notebook_id: The notebook ID

    Returns:
        dict with notebook details
    """
    client = get_client()
    return client.get(f"/notebooks/{notebook_id}")


def main():
    parser = argparse.ArgumentParser(description="Get NotebookLM notebook details")
    parser.add_argument("--notebook-id", required=True, help="Notebook ID")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    try:
        result = get_notebook(args.notebook_id)

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"Notebook Details:")
            print(f"  Title: {result.get('title')}")
            print(f"  ID: {result.get('notebookId')}")
            print(f"  Name: {result.get('name')}")
            if result.get('metadata'):
                meta = result['metadata']
                print(f"  Role: {meta.get('userRole', 'N/A')}")
                print(f"  Sharing: {meta.get('sharingStatus', 'N/A')}")
            if result.get('emoji'):
                print(f"  Emoji: {result.get('emoji')}")

    except Exception as e:
        if args.json:
            print(json.dumps({"error": str(e)}, indent=2))
        else:
            print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
