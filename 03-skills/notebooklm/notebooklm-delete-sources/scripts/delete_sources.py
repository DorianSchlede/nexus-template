#!/usr/bin/env python3
"""
Delete sources from a NotebookLM notebook.

Usage:
    python delete_sources.py --notebook-id "abc123" --source-ids "source1"
    python delete_sources.py --notebook-id "abc123" --source-ids "source1,source2,source3"
    python delete_sources.py --notebook-id "abc123" --source-ids "source1" --confirm --json
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


def delete_sources(notebook_id: str, source_ids: list) -> dict:
    """
    Delete sources from a notebook.

    Args:
        notebook_id: The notebook ID
        source_ids: List of source IDs to delete

    Returns:
        dict with result
    """
    client = get_client()

    # Build full resource names
    base_url = client.get_base_url()
    names = [f"{base_url}/notebooks/{notebook_id}/sources/{sid}" for sid in source_ids]

    return client.post(f"/notebooks/{notebook_id}/sources:batchDelete", {"names": names})


def main():
    parser = argparse.ArgumentParser(description="Delete sources from NotebookLM notebook")
    parser.add_argument("--notebook-id", required=True, help="Notebook ID")
    parser.add_argument("--source-ids", required=True, help="Comma-separated source IDs")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--confirm", action="store_true", help="Skip confirmation")
    args = parser.parse_args()

    source_ids = [sid.strip() for sid in args.source_ids.split(",")]

    if not args.confirm:
        print(f"About to delete {len(source_ids)} source(s) from notebook {args.notebook_id}:")
        for sid in source_ids:
            print(f"  - {sid}")
        confirm = input("\nAre you sure? (yes/no): ")
        if confirm.lower() != "yes":
            print("Cancelled.")
            sys.exit(0)

    try:
        result = delete_sources(args.notebook_id, source_ids)

        if args.json:
            print(json.dumps({"status": "deleted", "count": len(source_ids)}, indent=2))
        else:
            print(f"Successfully deleted {len(source_ids)} source(s).")

    except Exception as e:
        if args.json:
            print(json.dumps({"error": str(e)}, indent=2))
        else:
            print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
