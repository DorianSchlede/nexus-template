"""Get specific Langfuse trace."""

import sys
import json
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "langfuse-master" / "scripts"))
from langfuse_client import get_client


def get_trace(trace_id: str) -> dict:
    """
    Get a specific trace by ID.

    Args:
        trace_id: The trace ID

    Returns:
        dict: Trace details
    """
    client = get_client()
    return client.get(f"/traces/{trace_id}")


def main():
    parser = argparse.ArgumentParser(description="Get Langfuse trace")
    parser.add_argument("--id", required=True, help="Trace ID")

    args = parser.parse_args()
    result = get_trace(args.id)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
