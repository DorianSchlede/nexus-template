"""Get specific Langfuse session.

Note: Returns session with traces but WITHOUT observations.
To get observations, use get_trace for each trace individually.
Supports file output with --output flag (useful for Windows unicode issues).
"""

import sys
import json
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "langfuse-master" / "scripts"))
from langfuse_client import get_client, LangfuseAPIError


def get_session(session_id: str) -> dict:
    """
    Get a specific session by ID.

    Note: Returns traces WITHOUT observations.
    Use get_trace for each trace to get observations.

    Args:
        session_id: The session ID (32-char hex)

    Returns:
        dict: Session details with traces array
    """
    client = get_client()
    return client.get(f"/sessions/{session_id}")


def main():
    parser = argparse.ArgumentParser(description="Get Langfuse session (traces without observations)")
    parser.add_argument("--id", required=True, help="Session ID (32-char hex)")
    parser.add_argument("--output", "-o", type=str, help="Output file (avoids unicode issues)")

    args = parser.parse_args()

    try:
        result = get_session(args.id)
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
