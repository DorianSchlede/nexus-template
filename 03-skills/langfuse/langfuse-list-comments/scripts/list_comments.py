#!/usr/bin/env python3
"""Langfuse List Comments."""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "langfuse-master" / "scripts"))
from langfuse_client import get_client


def list_comments(object_type: str, object_id: str, page: int = 1, limit: int = 50) -> dict:
    client = get_client()
    params = {
        "objectType": object_type,
        "objectId": object_id,
        "page": page,
        "limit": limit
    }
    return client.get("/comments", params=params)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--type", type=str, required=True, choices=["TRACE", "OBSERVATION"])
    parser.add_argument("--id", type=str, required=True)
    parser.add_argument("--page", type=int, default=1)
    parser.add_argument("--limit", type=int, default=50)
    args = parser.parse_args()
    result = list_comments(object_type=args.type, object_id=args.id, page=args.page, limit=args.limit)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
