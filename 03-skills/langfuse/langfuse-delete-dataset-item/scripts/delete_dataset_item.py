#!/usr/bin/env python3
"""Langfuse Delete Dataset Item - Delete item by ID."""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "langfuse-master" / "scripts"))
from langfuse_client import get_client


def delete_dataset_item(item_id: str) -> dict:
    """
    Delete a dataset item.

    Args:
        item_id: Item ID to delete

    Returns:
        Deletion confirmation
    """
    client = get_client()
    return client.delete(f"/dataset-items/{item_id}")


def main():
    parser = argparse.ArgumentParser(description="Delete a dataset item")
    parser.add_argument("--id", type=str, required=True, help="Item ID")

    args = parser.parse_args()
    result = delete_dataset_item(item_id=args.id)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
