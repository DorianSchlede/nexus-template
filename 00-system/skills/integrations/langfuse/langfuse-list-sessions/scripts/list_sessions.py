"""List Langfuse sessions.

Supports:
- Single page fetch (default)
- All pages with --all flag
- File output with --output flag (useful for Windows unicode issues)
"""

import sys
import json
import argparse
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "langfuse-master" / "scripts"))
from langfuse_client import get_client, LangfuseAPIError


def list_sessions(
    limit: int = 50,
    page: int = 1,
    from_timestamp: str = None,
    to_timestamp: str = None
) -> dict:
    """
    List sessions from Langfuse.

    Args:
        limit: Max results per page (max 100)
        page: Page number
        from_timestamp: Start time (ISO8601)
        to_timestamp: End time (ISO8601)

    Returns:
        dict: Response with data and meta
    """
    client = get_client()

    params = {"limit": min(limit, 100), "page": page}

    if from_timestamp:
        params["fromTimestamp"] = from_timestamp
    if to_timestamp:
        params["toTimestamp"] = to_timestamp

    return client.get("/sessions", params=params)


def list_all_sessions(
    limit: int = 100,
    max_pages: int = None,
    **filters
) -> list:
    """Fetch all sessions across all pages.

    Args:
        limit: Items per page
        max_pages: Stop after N pages (None = all)
        **filters: Filter parameters (from_timestamp, to_timestamp)

    Returns:
        List of all sessions
    """
    all_sessions = []
    page = 1

    while True:
        result = list_sessions(limit=limit, page=page, **filters)
        data = result.get("data", [])
        all_sessions.extend(data)

        meta = result.get("meta", {})
        total_pages = meta.get("totalPages", 1)

        print(f"Fetched page {page}/{total_pages} ({len(data)} sessions)", file=sys.stderr)

        if page >= total_pages:
            break
        if max_pages and page >= max_pages:
            print(f"Stopped at max_pages={max_pages}", file=sys.stderr)
            break

        page += 1

    print(f"Total: {len(all_sessions)} sessions", file=sys.stderr)
    return all_sessions


def main():
    parser = argparse.ArgumentParser(description="List Langfuse sessions")
    parser.add_argument("--limit", type=int, default=50, help="Max results per page")
    parser.add_argument("--page", type=int, default=1, help="Page number")
    parser.add_argument("--from", dest="from_ts", help="Start time (ISO8601)")
    parser.add_argument("--to", dest="to_ts", help="End time (ISO8601)")
    parser.add_argument("--all", action="store_true", help="Fetch all pages (not just one)")
    parser.add_argument("--max-pages", type=int, help="Max pages to fetch with --all")
    parser.add_argument("--output", "-o", type=str, help="Output file (avoids unicode issues)")

    args = parser.parse_args()

    try:
        if args.all:
            # Fetch all pages
            result = list_all_sessions(
                limit=args.limit,
                max_pages=args.max_pages,
                from_timestamp=args.from_ts,
                to_timestamp=args.to_ts
            )
            output = {"data": result, "meta": {"totalItems": len(result)}}
        else:
            # Single page
            output = list_sessions(
                limit=args.limit,
                page=args.page,
                from_timestamp=args.from_ts,
                to_timestamp=args.to_ts
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
