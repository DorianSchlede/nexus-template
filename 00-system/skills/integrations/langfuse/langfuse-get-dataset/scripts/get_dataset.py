#!/usr/bin/env python3
"""Langfuse Get Dataset - Get a dataset by name."""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "langfuse-master" / "scripts"))
from langfuse_client import get_client


def get_dataset(name: str) -> dict:
    """
    Get a dataset from Langfuse by name.

    Args:
        name: Dataset name

    Returns:
        Dataset object with items
    """
    client = get_client()
    return client.get(f"/v2/datasets/{name}")


def main():
    parser = argparse.ArgumentParser(description="Get a dataset from Langfuse")
    parser.add_argument("--name", type=str, required=True, help="Dataset name")

    args = parser.parse_args()
    result = get_dataset(name=args.name)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
