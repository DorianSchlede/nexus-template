#!/usr/bin/env python3
"""
Share a NotebookLM notebook with other users.

Usage:
    python share_notebook.py --notebook-id "abc123" --email "user@example.com" --role READER
    python share_notebook.py --notebook-id "abc123" --email "user@example.com" --role WRITER --json
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


def share_notebook(notebook_id: str, email: str, role: str) -> dict:
    """
    Share a notebook with a user.

    Args:
        notebook_id: The notebook ID
        email: User email address
        role: OWNER, WRITER, READER, or NOT_SHARED

    Returns:
        dict with result
    """
    client = get_client()
    data = {
        "shareSettings": [
            {
                "email": email,
                "role": role.upper()
            }
        ]
    }
    return client.post(f"/notebooks/{notebook_id}:share", data)


def main():
    parser = argparse.ArgumentParser(description="Share a NotebookLM notebook")
    parser.add_argument("--notebook-id", required=True, help="Notebook ID")
    parser.add_argument("--email", required=True, help="User email address")
    parser.add_argument("--role", required=True, choices=["OWNER", "WRITER", "READER", "NOT_SHARED"],
                        help="Access role")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    try:
        result = share_notebook(args.notebook_id, args.email, args.role)

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"Notebook shared successfully!")
            print(f"  Email: {args.email}")
            print(f"  Role: {args.role}")

    except Exception as e:
        if args.json:
            print(json.dumps({"error": str(e)}, indent=2))
        else:
            print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
