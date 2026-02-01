#!/usr/bin/env python3
"""List Langfuse dataset items.

Supports:
- Single page fetch (default)
- All pages with --all flag
- File output with --output flag (useful for Windows unicode issues)
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "langfuse-master" / "scripts"))
from langfuse_client import get_client, LangfuseAPIError


def list_dataset_items(
    dataset_name: str = None,
    limit: int = 50,
    page: int = 1
) -> dict:
    """
    List dataset items.

    Args:
        dataset_name: Filter by dataset name
        limit: Maximum results (max 100)
        page: Page number

    Returns:
        dict with 'data' (list of items) and 'meta'
    """
    client = get_client()

    params = {"limit": min(limit, 100), "page": page}
    if dataset_name:
        params["datasetName"] = dataset_name

    return client.get("/dataset-items", params=params)


def list_all_dataset_items(
    dataset_name: str = None,
    limit: int = 100,
    max_pages: int = None
) -> list:
    """Fetch all dataset items across all pages.

    Args:
        dataset_name: Filter by dataset name
        limit: Items per page
        max_pages: Stop after N pages (None = all)

    Returns:
        List of all dataset items
    """
    all_items = []
    page = 1

    while True:
        result = list_dataset_items(dataset_name=dataset_name, limit=limit, page=page)
        data = result.get("data", [])
        all_items.extend(data)

        meta = result.get("meta", {})
        total_pages = meta.get("totalPages", 1)

        print(f"Fetched page {page}/{total_pages} ({len(data)} items)", file=sys.stderr)

        if page >= total_pages:
            break
        if max_pages and page >= max_pages:
            print(f"Stopped at max_pages={max_pages}", file=sys.stderr)
            break

        page += 1

    print(f"Total: {len(all_items)} items", file=sys.stderr)
    return all_items


def main():
    parser = argparse.ArgumentParser(description="List dataset items")
    parser.add_argument("--dataset", type=str, help="Dataset name to filter")
    parser.add_argument("--limit", type=int, default=50, help="Max results per page")
    parser.add_argument("--page", type=int, default=1, help="Page number")
    parser.add_argument("--all", action="store_true", help="Fetch all pages")
    parser.add_argument("--max-pages", type=int, help="Max pages to fetch with --all")
    parser.add_argument("--output", "-o", type=str, help="Output file (avoids unicode issues)")

    args = parser.parse_args()

    try:
        if args.all:
            result = list_all_dataset_items(
                dataset_name=args.dataset,
                limit=args.limit,
                max_pages=args.max_pages
            )
            output = {"data": result, "meta": {"totalItems": len(result)}}
        else:
            output = list_dataset_items(
                dataset_name=args.dataset,
                limit=args.limit,
                page=args.page
            )

        json_output = json.dumps(output, indent=2, default=str, ensure_ascii=False)

        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(json_output)
            print(f"Output written to {args.output}", file=sys.stderr)
        else:
            print(json_output)

    except LangfuseAPIError as e:
        print(f"API ERROR: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
