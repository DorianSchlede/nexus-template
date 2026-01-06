"""Get specific Langfuse session."""

import sys
import json
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "langfuse-master" / "scripts"))
from langfuse_client import get_client


def get_session(session_id: str) -> dict:
    """
    Get a specific session by ID.

    Args:
        session_id: The session ID

    Returns:
        dict: Session details with traces
    """
    client = get_client()
    return client.get(f"/sessions/{session_id}")


def main():
    parser = argparse.ArgumentParser(description="Get Langfuse session")
    parser.add_argument("--id", required=True, help="Session ID")

    args = parser.parse_args()
    result = get_session(args.id)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
