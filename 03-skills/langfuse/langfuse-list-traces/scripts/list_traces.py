"""List Langfuse traces."""

import sys
import json
import argparse
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "langfuse-master" / "scripts"))
from langfuse_client import get_client


def list_traces(
    limit: int = 50,
    page: int = 1,
    user_id: str = None,
    session_id: str = None,
    name: str = None,
    from_timestamp: str = None,
    to_timestamp: str = None,
    order_by: str = None,
    order: str = "desc"
) -> dict:
    """
    List traces from Langfuse.

    Args:
        limit: Max results per page (max 100)
        page: Page number
        user_id: Filter by user ID
        session_id: Filter by session ID
        name: Filter by trace name
        from_timestamp: Start time (ISO8601)
        to_timestamp: End time (ISO8601)
        order_by: Sort field
        order: Sort direction (asc/desc)

    Returns:
        dict: Response with data and meta
    """
    client = get_client()

    params = {"limit": min(limit, 100), "page": page}

    if user_id:
        params["userId"] = user_id
    if session_id:
        params["sessionId"] = session_id
    if name:
        params["name"] = name
    if from_timestamp:
        params["fromTimestamp"] = from_timestamp
    if to_timestamp:
        params["toTimestamp"] = to_timestamp
    if order_by:
        params["orderBy"] = order_by
    if order:
        params["order"] = order

    return client.get("/traces", params=params)


def main():
    parser = argparse.ArgumentParser(description="List Langfuse traces")
    parser.add_argument("--limit", type=int, default=50, help="Max results")
    parser.add_argument("--page", type=int, default=1, help="Page number")
    parser.add_argument("--user-id", help="Filter by user ID")
    parser.add_argument("--session-id", help="Filter by session ID")
    parser.add_argument("--name", help="Filter by trace name")
    parser.add_argument("--from", dest="from_ts", help="Start time (ISO8601)")
    parser.add_argument("--to", dest="to_ts", help="End time (ISO8601)")
    parser.add_argument("--order-by", help="Sort field")
    parser.add_argument("--order", choices=["asc", "desc"], default="desc")

    args = parser.parse_args()

    result = list_traces(
        limit=args.limit,
        page=args.page,
        user_id=args.user_id,
        session_id=args.session_id,
        name=args.name,
        from_timestamp=args.from_ts,
        to_timestamp=args.to_ts,
        order_by=args.order_by,
        order=args.order
    )

    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
