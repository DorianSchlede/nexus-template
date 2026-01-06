#!/usr/bin/env python3
"""
Delete NotebookLM notebooks.

Usage:
    python delete_notebooks.py --notebook-ids "abc123"
    python delete_notebooks.py --notebook-ids "abc123,def456"
    python delete_notebooks.py --notebook-ids "abc123" --json
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


def delete_notebooks(notebook_ids: list) -> dict:
    """
    Delete multiple notebooks.

    Args:
        notebook_ids: List of notebook IDs to delete

    Returns:
        dict with result
    """
    client = get_client()

    # Build full resource names
    base_url = client.get_base_url()
    names = [f"{base_url}/notebooks/{nid}" for nid in notebook_ids]

    return client.post("/notebooks:batchDelete", {"names": names})


def main():
    parser = argparse.ArgumentParser(description="Delete NotebookLM notebooks")
    parser.add_argument("--notebook-ids", required=True, help="Comma-separated notebook IDs")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--confirm", action="store_true", help="Skip confirmation")
    args = parser.parse_args()

    notebook_ids = [nid.strip() for nid in args.notebook_ids.split(",")]

    if not args.confirm:
        print(f"About to delete {len(notebook_ids)} notebook(s):")
        for nid in notebook_ids:
            print(f"  - {nid}")
        confirm = input("\nAre you sure? (yes/no): ")
        if confirm.lower() != "yes":
            print("Cancelled.")
            sys.exit(0)

    try:
        result = delete_notebooks(notebook_ids)

        if args.json:
            print(json.dumps({"status": "deleted", "count": len(notebook_ids)}, indent=2))
        else:
            print(f"Successfully deleted {len(notebook_ids)} notebook(s).")

    except Exception as e:
        if args.json:
            print(json.dumps({"error": str(e)}, indent=2))
        else:
            print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
