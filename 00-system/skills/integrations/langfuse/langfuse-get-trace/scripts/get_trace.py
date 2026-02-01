"""Get specific Langfuse trace.

Returns trace WITH observations (unlike list endpoints).
Supports file output with --output flag (useful for Windows unicode issues).
"""

import sys
import json
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "langfuse-master" / "scripts"))
from langfuse_client import get_client, LangfuseAPIError


def get_trace(trace_id: str) -> dict:
    """
    Get a specific trace by ID.

    Note: This endpoint returns observations, unlike list endpoints.

    Args:
        trace_id: The trace ID (UUID)

    Returns:
        dict: Trace details including observations array
    """
    client = get_client()
    return client.get(f"/traces/{trace_id}")


def main():
    parser = argparse.ArgumentParser(description="Get Langfuse trace (includes observations)")
    parser.add_argument("--id", required=True, help="Trace ID (UUID)")
    parser.add_argument("--output", "-o", type=str, help="Output file (avoids unicode issues)")

    args = parser.parse_args()

    try:
        result = get_trace(args.id)
        json_output = json.dumps(result, indent=2, default=str, ensure_ascii=False)

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
