#!/usr/bin/env python3
"""Langfuse Update Prompt Version - Update labels on a prompt version."""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "langfuse-master" / "scripts"))
from langfuse_client import get_client


def update_prompt_version(
    name: str,
    version: int,
    labels: list = None
) -> dict:
    """
    Update labels on a prompt version.

    Args:
        name: Prompt name
        version: Version number to update
        labels: List of labels to set

    Returns:
        Updated prompt version object
    """
    client = get_client()

    data = {}
    if labels is not None:
        data["labels"] = labels

    return client.patch(f"/v2/prompts/{name}/versions/{version}", data=data)


def main():
    parser = argparse.ArgumentParser(
        description="Update labels on a prompt version"
    )
    parser.add_argument(
        "--name", type=str, required=True,
        help="Prompt name"
    )
    parser.add_argument(
        "--version", type=int, required=True,
        help="Version number to update"
    )
    parser.add_argument(
        "--labels", type=str,
        help="Comma-separated labels to set"
    )

    args = parser.parse_args()

    # Parse labels
    labels = None
    if args.labels:
        labels = [l.strip() for l in args.labels.split(",")]

    result = update_prompt_version(
        name=args.name,
        version=args.version,
        labels=labels
    )

    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
