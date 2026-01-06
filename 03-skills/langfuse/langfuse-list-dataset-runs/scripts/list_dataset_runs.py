#!/usr/bin/env python3
"""Langfuse List Dataset Runs - Get runs for a dataset."""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "langfuse-master" / "scripts"))
from langfuse_client import get_client


def list_dataset_runs(name: str, limit: int = 50, page: int = None) -> dict:
    """
    List runs for a dataset.

    Args:
        name: Dataset name
        limit: Maximum results
        page: Page number

    Returns:
        dict with 'data' (list of runs) and 'meta'
    """
    client = get_client()

    params = {"limit": limit}
    if page is not None:
        params["page"] = page

    return client.get(f"/datasets/{name}/runs", params=params)


def main():
    parser = argparse.ArgumentParser(description="List dataset runs")
    parser.add_argument("--name", type=str, required=True, help="Dataset name")
    parser.add_argument("--limit", type=int, default=50, help="Max results")
    parser.add_argument("--page", type=int, help="Page number")

    args = parser.parse_args()
    result = list_dataset_runs(name=args.name, limit=args.limit, page=args.page)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
