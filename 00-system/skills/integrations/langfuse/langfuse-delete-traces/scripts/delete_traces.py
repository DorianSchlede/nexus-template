#!/usr/bin/env python3
"""Langfuse Bulk Delete Traces.

WARNING: This is a DESTRUCTIVE operation. Deleted traces cannot be recovered.
Deletion is QUEUED - traces may take several seconds to actually disappear.
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "langfuse-master" / "scripts"))
from langfuse_client import get_client, LangfuseAPIError


def delete_traces(trace_ids: list = None, filter_obj: dict = None) -> dict:
    """Delete multiple traces by IDs or filter.

    WARNING: Deletion is queued and may take ~5s to complete.
    """
    if not trace_ids and not filter_obj:
        raise ValueError("Must provide either trace_ids or filter_obj")

    client = get_client()
    data = {}
    if trace_ids:
        data["traceIds"] = trace_ids
    if filter_obj:
        data["filter"] = filter_obj
    return client.delete("/traces", params=data)


def main():
    parser = argparse.ArgumentParser(
        description="Bulk delete traces (DESTRUCTIVE - cannot be undone)"
    )
    parser.add_argument("--ids", type=str, help="Comma-separated trace IDs")
    parser.add_argument("--filter", type=str, help="JSON filter object (e.g., '{\"sessionId\": \"abc\"}')")
    parser.add_argument("--confirm", action="store_true",
                        help="Skip confirmation prompt (for scripting)")
    args = parser.parse_args()

    # Require at least one of --ids or --filter
    if not args.ids and not args.filter:
        parser.error("Must provide --ids or --filter (or both)")

    trace_ids = args.ids.split(",") if args.ids else None
    filter_obj = json.loads(args.filter) if args.filter else None

    # Show what will be deleted
    if trace_ids:
        print(f"Will delete {len(trace_ids)} trace(s): {trace_ids[:5]}{'...' if len(trace_ids) > 5 else ''}")
    if filter_obj:
        print(f"Will delete traces matching filter: {filter_obj}")

    # Confirm unless --confirm flag is set
    if not args.confirm:
        response = input("Type 'DELETE' to confirm: ")
        if response != "DELETE":
            print("Aborted.")
            sys.exit(0)

    try:
        result = delete_traces(trace_ids=trace_ids, filter_obj=filter_obj)
        print(json.dumps(result, indent=2, default=str))
        print("\nNote: Deletion is QUEUED. Traces may take ~5s to disappear.")
    except LangfuseAPIError as e:
        print(f"API ERROR: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
