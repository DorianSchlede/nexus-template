"""List Langfuse models."""

import sys
import json
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "langfuse-master" / "scripts"))
from langfuse_client import get_client


def list_models(limit: int = 50, page: int = 1) -> dict:
    """
    List models from Langfuse.

    Args:
        limit: Max results per page
        page: Page number

    Returns:
        dict: Response with data and meta
    """
    client = get_client()
    params = {"limit": min(limit, 100), "page": page}
    return client.get("/models", params=params)


def main():
    parser = argparse.ArgumentParser(description="List Langfuse models")
    parser.add_argument("--limit", type=int, default=50, help="Max results")
    parser.add_argument("--page", type=int, default=1, help="Page number")

    args = parser.parse_args()
    result = list_models(limit=args.limit, page=args.page)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
