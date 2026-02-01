"""List Langfuse scores.

Supports:
- Single page fetch (default)
- All pages with --all flag (cursor-based pagination)
- File output with --output flag (useful for Windows unicode issues)
"""

import sys
import json
import argparse
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "langfuse-master" / "scripts"))
from langfuse_client import get_client, LangfuseAPIError


def list_scores(
    limit: int = 50,
    cursor: str = None,
    trace_id: str = None,
    observation_id: str = None,
    name: str = None,
    source: str = None
) -> dict:
    """
    List scores from Langfuse.

    Args:
        limit: Max results per page (max 100)
        cursor: Pagination cursor
        trace_id: Filter by trace ID
        observation_id: Filter by observation ID
        name: Filter by score name
        source: Filter by source (API, EVAL, ANNOTATION)

    Returns:
        dict: Response with data and meta (includes nextCursor)
    """
    client = get_client()

    params = {"limit": min(limit, 100)}

    if cursor:
        params["cursor"] = cursor
    if trace_id:
        params["traceId"] = trace_id
    if observation_id:
        params["observationId"] = observation_id
    if name:
        params["name"] = name
    if source:
        params["source"] = source

    # Try v2 first, fall back to legacy if not available
    try:
        return client.get("/v2/scores", params=params)
    except LangfuseAPIError as e:
        if e.status_code == 404:
            # Legacy endpoint uses page-based pagination
            legacy_params = {"limit": params.get("limit", 50), "page": 1}
            if trace_id:
                legacy_params["traceId"] = trace_id
            if observation_id:
                legacy_params["observationId"] = observation_id
            if name:
                legacy_params["name"] = name
            return client.get("/scores", params=legacy_params)
        raise


def list_all_scores(
    limit: int = 100,
    max_iterations: int = None,
    **filters
) -> list:
    """Fetch all scores using cursor-based pagination.

    Args:
        limit: Items per page
        max_iterations: Stop after N pages (None = all)
        **filters: Filter parameters (trace_id, observation_id, name, source)

    Returns:
        List of all scores
    """
    all_scores = []
    cursor = None
    iteration = 0

    while True:
        result = list_scores(limit=limit, cursor=cursor, **filters)
        data = result.get("data", [])
        all_scores.extend(data)
        iteration += 1

        # Get next cursor from meta
        meta = result.get("meta", {})
        next_cursor = meta.get("nextCursor")

        print(f"Fetched page {iteration} ({len(data)} scores, total: {len(all_scores)})", file=sys.stderr)

        if not next_cursor:
            break
        if max_iterations and iteration >= max_iterations:
            print(f"Stopped at max_iterations={max_iterations}", file=sys.stderr)
            break

        cursor = next_cursor

    print(f"Total: {len(all_scores)} scores", file=sys.stderr)
    return all_scores


def main():
    parser = argparse.ArgumentParser(description="List Langfuse scores")
    parser.add_argument("--limit", type=int, default=50, help="Max results per page")
    parser.add_argument("--cursor", help="Pagination cursor")
    parser.add_argument("--trace-id", help="Filter by trace ID")
    parser.add_argument("--observation-id", help="Filter by observation ID")
    parser.add_argument("--name", help="Filter by score name")
    parser.add_argument("--source", choices=["API", "EVAL", "ANNOTATION"], help="Filter by source")
    parser.add_argument("--all", action="store_true", help="Fetch all pages (cursor-based)")
    parser.add_argument("--max-pages", type=int, help="Max pages to fetch with --all")
    parser.add_argument("--output", "-o", type=str, help="Output file (avoids unicode issues)")

    args = parser.parse_args()

    try:
        if args.all:
            # Fetch all pages using cursor pagination
            result = list_all_scores(
                limit=args.limit,
                max_iterations=args.max_pages,
                trace_id=args.trace_id,
                observation_id=args.observation_id,
                name=args.name,
                source=args.source
            )
            output = {"data": result, "meta": {"totalItems": len(result)}}
        else:
            # Single page
            output = list_scores(
                limit=args.limit,
                cursor=args.cursor,
                trace_id=args.trace_id,
                observation_id=args.observation_id,
                name=args.name,
                source=args.source
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
