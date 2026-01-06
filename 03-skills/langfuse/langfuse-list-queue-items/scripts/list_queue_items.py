#!/usr/bin/env python3
"""Langfuse List Queue Items."""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "langfuse-master" / "scripts"))
from langfuse_client import get_client


def list_queue_items(queue_id: str, limit: int = 50) -> dict:
    client = get_client()
    return client.get(f"/annotation-queues/{queue_id}/items", params={"limit": limit})


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--queue", type=str, required=True)
    parser.add_argument("--limit", type=int, default=50)
    args = parser.parse_args()
    result = list_queue_items(queue_id=args.queue, limit=args.limit)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
