#!/usr/bin/env python3
"""Langfuse Delete Trace.

WARNING: This is a DESTRUCTIVE operation. Deleted traces cannot be recovered.
Note: API returns success even for nonexistent IDs (queued deletion).
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "langfuse-master" / "scripts"))
from langfuse_client import get_client, LangfuseAPIError


def delete_trace(trace_id: str) -> dict:
    """Delete a single trace.

    WARNING: API returns success even for nonexistent IDs.
    """
    client = get_client()
    return client.delete(f"/traces/{trace_id}")


def main():
    parser = argparse.ArgumentParser(
        description="Delete a trace (DESTRUCTIVE - cannot be undone)"
    )
    parser.add_argument("--id", type=str, required=True, help="Trace ID to delete")
    parser.add_argument("--confirm", action="store_true",
                        help="Skip confirmation prompt (for scripting)")
    args = parser.parse_args()

    print(f"Will delete trace: {args.id}")

    # Confirm unless --confirm flag is set
    if not args.confirm:
        response = input("Type 'DELETE' to confirm: ")
        if response != "DELETE":
            print("Aborted.")
            sys.exit(0)

    try:
        result = delete_trace(trace_id=args.id)
        print(json.dumps(result, indent=2, default=str))
        print("\nNote: Deletion is QUEUED. Trace may take ~5s to disappear.")
        print("Warning: API returns success even for nonexistent IDs.")
    except LangfuseAPIError as e:
        print(f"API ERROR: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
