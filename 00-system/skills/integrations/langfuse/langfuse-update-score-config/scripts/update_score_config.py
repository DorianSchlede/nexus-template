#!/usr/bin/env python3
"""Langfuse Update Score Config - Update a config.

Note: You can only update description and archived status.
Categories, min/max values cannot be changed after creation.
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "langfuse-master" / "scripts"))
from langfuse_client import get_client, LangfuseAPIError


def update_score_config(config_id: str, description: str = None, is_archived: bool = None) -> dict:
    """Update a score config.

    Note: Can only update description and archived status.
    """
    client = get_client()
    data = {}
    if description is not None:
        data["description"] = description
    if is_archived is not None:
        data["isArchived"] = is_archived

    if not data:
        raise ValueError("Must provide at least one field to update (--description, --archive, or --unarchive)")

    return client.patch(f"/score-configs/{config_id}", data=data)


def main():
    parser = argparse.ArgumentParser(description="Update a score config")
    parser.add_argument("--id", type=str, required=True, help="Score config ID")
    parser.add_argument("--description", type=str, help="New description")
    parser.add_argument("--archive", action="store_true", help="Archive the config")
    parser.add_argument("--unarchive", action="store_true", help="Unarchive the config")
    args = parser.parse_args()

    # Check for conflicting flags
    if args.archive and args.unarchive:
        parser.error("Cannot use both --archive and --unarchive")

    # Determine is_archived value
    is_archived = None
    if args.archive:
        is_archived = True
    elif args.unarchive:
        is_archived = False

    # Require at least one update
    if not args.description and is_archived is None:
        parser.error("Must provide at least one field to update (--description, --archive, or --unarchive)")

    try:
        result = update_score_config(
            config_id=args.id,
            description=args.description,
            is_archived=is_archived
        )
        print(json.dumps(result, indent=2, default=str))
    except LangfuseAPIError as e:
        print(f"API ERROR: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
