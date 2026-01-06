#!/usr/bin/env python3
"""Langfuse Create Queue Assignment."""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "langfuse-master" / "scripts"))
from langfuse_client import get_client


def create_queue_assignment(queue_id: str, user_email: str) -> dict:
    client = get_client()
    data = {"userEmail": user_email}
    return client.post(f"/annotation-queues/{queue_id}/assignments", data=data)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--queue", type=str, required=True)
    parser.add_argument("--user", type=str, required=True)
    args = parser.parse_args()
    result = create_queue_assignment(queue_id=args.queue, user_email=args.user)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
