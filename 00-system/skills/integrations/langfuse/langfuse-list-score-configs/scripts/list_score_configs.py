#!/usr/bin/env python3
"""List Langfuse score configs.

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


def list_score_configs(limit: int = 50, page: int = 1) -> dict:
    """
    List score configurations from Langfuse.

    Args:
        limit: Maximum number of results (max 100)
        page: Page number for pagination

    Returns:
        dict with 'data' (list of configs) and 'meta' (pagination)
    """
    client = get_client()
    params = {"limit": min(limit, 100), "page": page}
    return client.get("/score-configs", params=params)


def list_all_score_configs(limit: int = 100, max_pages: int = None) -> list:
    """Fetch all score configs across all pages.

    Args:
        limit: Items per page
        max_pages: Stop after N pages (None = all)

    Returns:
        List of all score configs
    """
    all_configs = []
    page = 1

    while True:
        result = list_score_configs(limit=limit, page=page)
        data = result.get("data", [])
        all_configs.extend(data)

        meta = result.get("meta", {})
        total_pages = meta.get("totalPages", 1)

        print(f"Fetched page {page}/{total_pages} ({len(data)} configs)", file=sys.stderr)

        if page >= total_pages:
            break
        if max_pages and page >= max_pages:
            print(f"Stopped at max_pages={max_pages}", file=sys.stderr)
            break

        page += 1

    print(f"Total: {len(all_configs)} configs", file=sys.stderr)
    return all_configs


def main():
    parser = argparse.ArgumentParser(description="List score configs")
    parser.add_argument("--limit", type=int, default=50, help="Max results per page")
    parser.add_argument("--page", type=int, default=1, help="Page number")
    parser.add_argument("--all", action="store_true", help="Fetch all pages")
    parser.add_argument("--max-pages", type=int, help="Max pages to fetch with --all")
    parser.add_argument("--output", "-o", type=str, help="Output file (avoids unicode issues)")

    args = parser.parse_args()

    try:
        if args.all:
            result = list_all_score_configs(limit=args.limit, max_pages=args.max_pages)
            output = {"data": result, "meta": {"totalItems": len(result)}}
        else:
            output = list_score_configs(limit=args.limit, page=args.page)

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
