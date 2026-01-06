#!/usr/bin/env python3
"""Langfuse Update Queue Item."""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "langfuse-master" / "scripts"))
from langfuse_client import get_client


def update_queue_item(queue_id: str, item_id: str, status: str = None) -> dict:
    client = get_client()
    data = {}
    if status:
        data["status"] = status
    return client.patch(f"/annotation-queues/{queue_id}/items/{item_id}", data=data)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--queue", type=str, required=True)
    parser.add_argument("--item", type=str, required=True)
    parser.add_argument("--status", type=str, choices=["PENDING", "IN_PROGRESS", "COMPLETED"])
    args = parser.parse_args()
    result = update_queue_item(queue_id=args.queue, item_id=args.item, status=args.status)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
