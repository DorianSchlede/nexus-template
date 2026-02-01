#!/usr/bin/env python3
"""List Langfuse prompts.

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


def list_prompts(
    limit: int = 50,
    page: int = 1,
    name: str = None,
    label: str = None,
    tag: str = None,
    from_time: str = None,
    to_time: str = None
) -> dict:
    """
    List prompts from Langfuse.

    Args:
        limit: Maximum number of results (max 100)
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

    params = {"limit": min(limit, 100), "page": page}
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


def list_all_prompts(
    limit: int = 100,
    max_pages: int = None,
    **filters
) -> list:
    """Fetch all prompts across all pages.

    Args:
        limit: Items per page
        max_pages: Stop after N pages (None = all)
        **filters: Filter parameters (name, label, tag, from_time, to_time)

    Returns:
        List of all prompts
    """
    all_prompts = []
    page = 1

    while True:
        result = list_prompts(limit=limit, page=page, **filters)
        data = result.get("data", [])
        all_prompts.extend(data)

        meta = result.get("meta", {})
        total_pages = meta.get("totalPages", 1)

        print(f"Fetched page {page}/{total_pages} ({len(data)} prompts)", file=sys.stderr)

        if page >= total_pages:
            break
        if max_pages and page >= max_pages:
            print(f"Stopped at max_pages={max_pages}", file=sys.stderr)
            break

        page += 1

    print(f"Total: {len(all_prompts)} prompts", file=sys.stderr)
    return all_prompts


def main():
    parser = argparse.ArgumentParser(description="List prompts from Langfuse")
    parser.add_argument("--limit", type=int, default=50, help="Max results per page")
    parser.add_argument("--page", type=int, default=1, help="Page number")
    parser.add_argument("--name", type=str, help="Filter by prompt name")
    parser.add_argument("--label", type=str, help="Filter by label (e.g., 'production')")
    parser.add_argument("--tag", type=str, help="Filter by tag")
    parser.add_argument("--from", dest="from_time", type=str, help="Filter prompts updated after (ISO8601)")
    parser.add_argument("--to", dest="to_time", type=str, help="Filter prompts updated before (ISO8601)")
    parser.add_argument("--all", action="store_true", help="Fetch all pages")
    parser.add_argument("--max-pages", type=int, help="Max pages to fetch with --all")
    parser.add_argument("--output", "-o", type=str, help="Output file (avoids unicode issues)")

    args = parser.parse_args()

    try:
        if args.all:
            result = list_all_prompts(
                limit=args.limit,
                max_pages=args.max_pages,
                name=args.name,
                label=args.label,
                tag=args.tag,
                from_time=args.from_time,
                to_time=args.to_time
            )
            output = {"data": result, "meta": {"totalItems": len(result)}}
        else:
            output = list_prompts(
                limit=args.limit,
                page=args.page,
                name=args.name,
                label=args.label,
                tag=args.tag,
                from_time=args.from_time,
                to_time=args.to_time
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
