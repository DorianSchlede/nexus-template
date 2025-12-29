#!/usr/bin/env python3
"""
List recently viewed NotebookLM notebooks.

Usage:
    python list_notebooks.py
    python list_notebooks.py --json
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


def list_notebooks() -> dict:
    """
    List recently viewed notebooks.

    Returns:
        dict with list of notebooks
    """
    client = get_client()
    return client.get("/notebooks:listRecentlyViewed")


def main():
    parser = argparse.ArgumentParser(description="List NotebookLM notebooks")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    try:
        result = list_notebooks()
        notebooks = result.get("notebooks", [])

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            if not notebooks:
                print("No notebooks found.")
            else:
                print(f"Found {len(notebooks)} notebook(s):\n")
                for nb in notebooks:
                    print(f"  [{nb.get('notebookId')}] {nb.get('title')}")
                    if nb.get('metadata'):
                        meta = nb['metadata']
                        print(f"      Role: {meta.get('userRole', 'N/A')}")
                        print(f"      Sharing: {meta.get('sharingStatus', 'N/A')}")
                    print()

    except Exception as e:
        if args.json:
            print(json.dumps({"error": str(e)}, indent=2))
        else:
            print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
