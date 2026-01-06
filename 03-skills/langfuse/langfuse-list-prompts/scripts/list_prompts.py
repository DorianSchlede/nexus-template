#!/usr/bin/env python3
"""Langfuse List Prompts - Get list of prompts from Langfuse."""

import argparse
import json
import sys
from pathlib import Path

# Add langfuse-master scripts to path for shared client
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "langfuse-master" / "scripts"))
from langfuse_client import get_client


def list_prompts(
    limit: int = 50,
    page: int = None,
    name: str = None,
    label: str = None,
    tag: str = None,
    from_time: str = None,
    to_time: str = None
) -> dict:
    """
    List prompts from Langfuse.

    Args:
        limit: Maximum number of results (default 50, max 100)
        page: Page number for pagination
        name: Filter by prompt name
        label: Filter by label (e.g., "production")
        tag: Filter by tag
        from_time: Filter prompts updated after this time (ISO8601)
        to_time: Filter prompts updated before this time (ISO8601)

    Returns:
        dict with 'data' (list of prompts) and 'meta' (pagination info)
    """
    client = get_client()

    params = {"limit": limit}
    if page is not None:
        params["page"] = page
    if name:
        params["name"] = name
    if label:
        params["label"] = label
    if tag:
        params["tag"] = tag
    if from_time:
        params["fromUpdatedAt"] = from_time
    if to_time:
        params["toUpdatedAt"] = to_time

    return client.get("/v2/prompts", params=params)


def main():
    parser = argparse.ArgumentParser(
        description="List prompts from Langfuse"
    )
    parser.add_argument(
        "--limit", type=int, default=50,
        help="Maximum number of results (default 50)"
    )
    parser.add_argument(
        "--page", type=int,
        help="Page number for pagination"
    )
    parser.add_argument(
        "--name", type=str,
        help="Filter by prompt name"
    )
    parser.add_argument(
        "--label", type=str,
        help="Filter by label (e.g., 'production')"
    )
    parser.add_argument(
        "--tag", type=str,
        help="Filter by tag"
    )
    parser.add_argument(
        "--from", dest="from_time", type=str,
        help="Filter prompts updated after this time (ISO8601)"
    )
    parser.add_argument(
        "--to", dest="to_time", type=str,
        help="Filter prompts updated before this time (ISO8601)"
    )

    args = parser.parse_args()

    result = list_prompts(
        limit=args.limit,
        page=args.page,
        name=args.name,
        label=args.label,
        tag=args.tag,
        from_time=args.from_time,
        to_time=args.to_time
    )

    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
