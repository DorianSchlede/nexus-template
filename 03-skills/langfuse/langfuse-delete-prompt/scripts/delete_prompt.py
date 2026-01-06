#!/usr/bin/env python3
"""Langfuse Delete Prompt - Delete a prompt by name."""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "langfuse-master" / "scripts"))
from langfuse_client import get_client


def delete_prompt(name: str) -> dict:
    """
    Delete a prompt from Langfuse by name.

    Args:
        name: Prompt name to delete

    Returns:
        Deletion confirmation
    """
    client = get_client()
    return client.delete(f"/v2/prompts/{name}")


def main():
    parser = argparse.ArgumentParser(
        description="Delete a prompt from Langfuse"
    )
    parser.add_argument(
        "--name", type=str, required=True,
        help="Prompt name to delete"
    )

    args = parser.parse_args()

    result = delete_prompt(name=args.name)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
