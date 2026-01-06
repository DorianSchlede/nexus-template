#!/usr/bin/env python3
"""Langfuse Get Queue Item."""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "langfuse-master" / "scripts"))
from langfuse_client import get_client


def get_queue_item(queue_id: str, item_id: str) -> dict:
    client = get_client()
    return client.get(f"/annotation-queues/{queue_id}/items/{item_id}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--queue", type=str, required=True)
    parser.add_argument("--item", type=str, required=True)
    args = parser.parse_args()
    result = get_queue_item(queue_id=args.queue, item_id=args.item)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
