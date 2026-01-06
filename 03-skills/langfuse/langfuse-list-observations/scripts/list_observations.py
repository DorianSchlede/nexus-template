"""List Langfuse observations."""

import sys
import json
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "langfuse-master" / "scripts"))
from langfuse_client import get_client


def list_observations(
    limit: int = 50,
    cursor: str = None,
    trace_id: str = None,
    obs_type: str = None,
    name: str = None,
    from_start_time: str = None,
    to_start_time: str = None
) -> dict:
    """
    List observations from Langfuse.

    Args:
        limit: Max results per page
        cursor: Pagination cursor
        trace_id: Filter by trace ID
        obs_type: Filter by type (SPAN, GENERATION, EVENT)
        name: Filter by name
        from_start_time: Start time (ISO8601)
        to_start_time: End time (ISO8601)

    Returns:
        dict: Response with data and meta
    """
    client = get_client()

    params = {"limit": min(limit, 100)}

    if cursor:
        params["cursor"] = cursor
    if trace_id:
        params["traceId"] = trace_id
    if obs_type:
        params["type"] = obs_type
    if name:
        params["name"] = name
    if from_start_time:
        params["fromStartTime"] = from_start_time
    if to_start_time:
        params["toStartTime"] = to_start_time

    # Try v2 first, fall back to legacy if not available
    try:
        return client.get("/v2/observations", params=params)
    except Exception:
        # Legacy endpoint uses page-based pagination
        legacy_params = {"limit": params.get("limit", 50)}
        if trace_id:
            legacy_params["traceId"] = trace_id
        if obs_type:
            legacy_params["type"] = obs_type
        if name:
            legacy_params["name"] = name
        return client.get("/observations", params=legacy_params)


def main():
    parser = argparse.ArgumentParser(description="List Langfuse observations")
    parser.add_argument("--limit", type=int, default=50, help="Max results")
    parser.add_argument("--cursor", help="Pagination cursor")
    parser.add_argument("--trace-id", help="Filter by trace ID")
    parser.add_argument("--type", choices=["SPAN", "GENERATION", "EVENT"], help="Filter by type")
    parser.add_argument("--name", help="Filter by name")
    parser.add_argument("--from", dest="from_ts", help="Start time (ISO8601)")
    parser.add_argument("--to", dest="to_ts", help="End time (ISO8601)")

    args = parser.parse_args()

    result = list_observations(
        limit=args.limit,
        cursor=args.cursor,
        trace_id=args.trace_id,
        obs_type=args.type,
        name=args.name,
        from_start_time=args.from_ts,
        to_start_time=args.to_ts
    )

    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
