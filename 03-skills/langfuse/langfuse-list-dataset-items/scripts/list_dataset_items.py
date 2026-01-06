#!/usr/bin/env python3
"""Langfuse List Dataset Items - Get items from a dataset."""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "langfuse-master" / "scripts"))
from langfuse_client import get_client


def list_dataset_items(
    dataset_name: str = None,
    limit: int = 50,
    page: int = None
) -> dict:
    """
    List dataset items.

    Args:
        dataset_name: Filter by dataset name
        limit: Maximum results
        page: Page number

    Returns:
        dict with 'data' (list of items) and 'meta'
    """
    client = get_client()

    params = {"limit": limit}
    if dataset_name:
        params["datasetName"] = dataset_name
    if page is not None:
        params["page"] = page

    return client.get("/dataset-items", params=params)


def main():
    parser = argparse.ArgumentParser(description="List dataset items")
    parser.add_argument("--dataset", type=str, help="Dataset name to filter")
    parser.add_argument("--limit", type=int, default=50, help="Max results")
    parser.add_argument("--page", type=int, help="Page number")

    args = parser.parse_args()
    result = list_dataset_items(
        dataset_name=args.dataset,
        limit=args.limit,
        page=args.page
    )
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
