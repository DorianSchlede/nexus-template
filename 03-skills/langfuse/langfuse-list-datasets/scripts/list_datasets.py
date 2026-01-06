#!/usr/bin/env python3
"""Langfuse List Datasets - Get list of datasets from Langfuse."""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "langfuse-master" / "scripts"))
from langfuse_client import get_client


def list_datasets(limit: int = 50, page: int = None) -> dict:
    """
    List datasets from Langfuse.

    Args:
        limit: Maximum number of results
        page: Page number for pagination

    Returns:
        dict with 'data' (list of datasets) and 'meta' (pagination)
    """
    client = get_client()

    params = {"limit": limit}
    if page is not None:
        params["page"] = page

    return client.get("/v2/datasets", params=params)


def main():
    parser = argparse.ArgumentParser(description="List datasets from Langfuse")
    parser.add_argument("--limit", type=int, default=50, help="Max results")
    parser.add_argument("--page", type=int, help="Page number")

    args = parser.parse_args()
    result = list_datasets(limit=args.limit, page=args.page)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
