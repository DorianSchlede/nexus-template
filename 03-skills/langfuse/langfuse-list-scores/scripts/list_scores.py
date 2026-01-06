"""List Langfuse scores."""

import sys
import json
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "langfuse-master" / "scripts"))
from langfuse_client import get_client


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
        limit: Max results per page
        cursor: Pagination cursor
        trace_id: Filter by trace ID
        observation_id: Filter by observation ID
        name: Filter by score name
        source: Filter by source (API, EVAL, ANNOTATION)

    Returns:
        dict: Response with data and meta
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
    except Exception:
        # Legacy endpoint uses page-based pagination
        legacy_params = {"limit": params.get("limit", 50), "page": 1}
        if trace_id:
            legacy_params["traceId"] = trace_id
        if observation_id:
            legacy_params["observationId"] = observation_id
        if name:
            legacy_params["name"] = name
        return client.get("/scores", params=legacy_params)


def main():
    parser = argparse.ArgumentParser(description="List Langfuse scores")
    parser.add_argument("--limit", type=int, default=50, help="Max results")
    parser.add_argument("--cursor", help="Pagination cursor")
    parser.add_argument("--trace-id", help="Filter by trace ID")
    parser.add_argument("--observation-id", help="Filter by observation ID")
    parser.add_argument("--name", help="Filter by score name")
    parser.add_argument("--source", choices=["API", "EVAL", "ANNOTATION"], help="Filter by source")

    args = parser.parse_args()

    result = list_scores(
        limit=args.limit,
        cursor=args.cursor,
        trace_id=args.trace_id,
        observation_id=args.observation_id,
        name=args.name,
        source=args.source
    )

    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
