#!/usr/bin/env python3
"""Langfuse Delete Queue Assignment."""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "langfuse-master" / "scripts"))
from langfuse_client import get_client


def delete_queue_assignment(queue_id: str, user_email: str) -> dict:
    client = get_client()
    return client.delete(f"/annotation-queues/{queue_id}/assignments", params={"userEmail": user_email})


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--queue", type=str, required=True)
    parser.add_argument("--user", type=str, required=True)
    args = parser.parse_args()
    result = delete_queue_assignment(queue_id=args.queue, user_email=args.user)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
