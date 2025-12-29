"""Get specific Langfuse observation."""

import sys
import json
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "langfuse-master" / "scripts"))
from langfuse_client import get_client


def get_observation(observation_id: str) -> dict:
    """
    Get a specific observation by ID.

    Args:
        observation_id: The observation ID

    Returns:
        dict: Observation details
    """
    client = get_client()
    return client.get(f"/observations/{observation_id}")


def main():
    parser = argparse.ArgumentParser(description="Get Langfuse observation")
    parser.add_argument("--id", required=True, help="Observation ID")

    args = parser.parse_args()
    result = get_observation(args.id)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
