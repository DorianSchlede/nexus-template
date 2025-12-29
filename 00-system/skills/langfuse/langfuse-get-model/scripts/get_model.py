"""Get specific Langfuse model."""

import sys
import json
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "langfuse-master" / "scripts"))
from langfuse_client import get_client


def get_model(model_id: str) -> dict:
    """
    Get a specific model by ID.

    Args:
        model_id: The model ID

    Returns:
        dict: Model details
    """
    client = get_client()
    return client.get(f"/models/{model_id}")


def main():
    parser = argparse.ArgumentParser(description="Get Langfuse model")
    parser.add_argument("--id", required=True, help="Model ID")

    args = parser.parse_args()
    result = get_model(args.id)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
