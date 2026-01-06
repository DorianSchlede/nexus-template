"""List Langfuse sessions."""

import sys
import json
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "langfuse-master" / "scripts"))
from langfuse_client import get_client


def list_sessions(
    limit: int = 50,
    page: int = 1,
    from_timestamp: str = None,
    to_timestamp: str = None
) -> dict:
    """
    List sessions from Langfuse.

    Args:
        limit: Max results per page
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


def main():
    parser = argparse.ArgumentParser(description="List Langfuse sessions")
    parser.add_argument("--limit", type=int, default=50, help="Max results")
    parser.add_argument("--page", type=int, default=1, help="Page number")
    parser.add_argument("--from", dest="from_ts", help="Start time (ISO8601)")
    parser.add_argument("--to", dest="to_ts", help="End time (ISO8601)")

    args = parser.parse_args()

    result = list_sessions(
        limit=args.limit,
        page=args.page,
        from_timestamp=args.from_ts,
        to_timestamp=args.to_ts
    )

    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
