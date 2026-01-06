#!/usr/bin/env python3
"""Langfuse Get Prompt - Get a specific prompt by name."""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "langfuse-master" / "scripts"))
from langfuse_client import get_client


def get_prompt(
    name: str,
    version: int = None,
    label: str = None
) -> dict:
    """
    Get a prompt from Langfuse by name.

    Args:
        name: Prompt name
        version: Specific version number (optional)
        label: Label to fetch (optional)

    Returns:
        Prompt object with content and metadata
    """
    client = get_client()

    params = {}
    if version is not None:
        params["version"] = version
    if label:
        params["label"] = label

    return client.get(f"/v2/prompts/{name}", params=params if params else None)


def main():
    parser = argparse.ArgumentParser(
        description="Get a prompt from Langfuse by name"
    )
    parser.add_argument(
        "--name", type=str, required=True,
        help="Prompt name"
    )
    parser.add_argument(
        "--version", type=int,
        help="Specific version number"
    )
    parser.add_argument(
        "--label", type=str,
        help="Label to fetch (e.g., 'production')"
    )

    args = parser.parse_args()

    result = get_prompt(
        name=args.name,
        version=args.version,
        label=args.label
    )

    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
