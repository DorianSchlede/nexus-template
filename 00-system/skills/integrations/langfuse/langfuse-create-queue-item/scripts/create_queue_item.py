#!/usr/bin/env python3
"""Langfuse Create Queue Item."""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "langfuse-master" / "scripts"))
from langfuse_client import get_client


def create_queue_item(queue_id: str, trace_id: str, observation_id: str = None) -> dict:
    client = get_client()
    data = {"traceId": trace_id}
    if observation_id:
        data["observationId"] = observation_id
    return client.post(f"/annotation-queues/{queue_id}/items", data=data)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--queue", type=str, required=True)
    parser.add_argument("--trace", type=str, required=True)
    parser.add_argument("--observation", type=str)
    args = parser.parse_args()
    result = create_queue_item(queue_id=args.queue, trace_id=args.trace, observation_id=args.observation)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
