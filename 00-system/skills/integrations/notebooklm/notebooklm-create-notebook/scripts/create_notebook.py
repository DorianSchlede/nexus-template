#!/usr/bin/env python3
"""
Create a new NotebookLM notebook.

Usage:
    python create_notebook.py --title "My Notebook"
    python create_notebook.py --title "Research" --json
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


def create_notebook(title: str) -> dict:
    """
    Create a new notebook.

    Args:
        title: The notebook title

    Returns:
        dict with notebook details including notebookId
    """
    client = get_client()
    return client.post("/notebooks", {"title": title})


def main():
    parser = argparse.ArgumentParser(description="Create a NotebookLM notebook")
    parser.add_argument("--title", required=True, help="Notebook title")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    try:
        result = create_notebook(args.title)

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"Notebook created successfully!")
            print(f"  Title: {result.get('title')}")
            print(f"  ID: {result.get('notebookId')}")
            print(f"  Name: {result.get('name')}")

    except Exception as e:
        if args.json:
            print(json.dumps({"error": str(e)}, indent=2))
        else:
            print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
