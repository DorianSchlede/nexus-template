#!/usr/bin/env python3
"""Langfuse Update Score Config - Update a config."""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "langfuse-master" / "scripts"))
from langfuse_client import get_client


def update_score_config(config_id: str, description: str = None, is_archived: bool = None) -> dict:
    client = get_client()
    data = {}
    if description:
        data["description"] = description
    if is_archived is not None:
        data["isArchived"] = is_archived
    return client.patch(f"/score-configs/{config_id}", data=data)


def main():
    parser = argparse.ArgumentParser(description="Update a score config")
    parser.add_argument("--id", type=str, required=True)
    parser.add_argument("--description", type=str)
    parser.add_argument("--archived", action="store_true")
    args = parser.parse_args()
    result = update_score_config(
        config_id=args.id,
        description=args.description,
        is_archived=args.archived if args.archived else None
    )
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
