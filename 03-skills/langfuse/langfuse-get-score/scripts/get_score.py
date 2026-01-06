"""Get specific Langfuse score."""

import sys
import json
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "langfuse-master" / "scripts"))
from langfuse_client import get_client


def get_score(score_id: str) -> dict:
    """
    Get a specific score by ID.

    Args:
        score_id: The score ID

    Returns:
        dict: Score details
    """
    client = get_client()
    return client.get(f"/v2/scores/{score_id}")


def main():
    parser = argparse.ArgumentParser(description="Get Langfuse score")
    parser.add_argument("--id", required=True, help="Score ID")

    args = parser.parse_args()
    result = get_score(args.id)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
