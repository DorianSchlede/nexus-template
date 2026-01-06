#!/usr/bin/env python3
"""Langfuse Get Dataset Item - Get item by ID."""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "langfuse-master" / "scripts"))
from langfuse_client import get_client


def get_dataset_item(item_id: str) -> dict:
    """
    Get a dataset item by ID.

    Args:
        item_id: Item ID

    Returns:
        Item object
    """
    client = get_client()
    return client.get(f"/dataset-items/{item_id}")


def main():
    parser = argparse.ArgumentParser(description="Get a dataset item")
    parser.add_argument("--id", type=str, required=True, help="Item ID")

    args = parser.parse_args()
    result = get_dataset_item(item_id=args.id)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
