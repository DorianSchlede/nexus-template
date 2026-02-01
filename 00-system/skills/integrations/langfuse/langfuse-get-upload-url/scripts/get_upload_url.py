#!/usr/bin/env python3
"""Langfuse Get Upload URL."""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "langfuse-master" / "scripts"))
from langfuse_client import get_client


def get_upload_url(trace_id: str, field: str, content_type: str, observation_id: str = None) -> dict:
    client = get_client()
    data = {
        "traceId": trace_id,
        "field": field,
        "contentType": content_type
    }
    if observation_id:
        data["observationId"] = observation_id
    return client.post("/media", data=data)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--trace", type=str, required=True)
    parser.add_argument("--observation", type=str, default=None)
    parser.add_argument("--field", type=str, required=True, choices=["input", "output", "metadata"])
    parser.add_argument("--type", type=str, required=True, help="Content type (e.g., image/png)")
    args = parser.parse_args()
    result = get_upload_url(
        trace_id=args.trace,
        field=args.field,
        content_type=args.type,
        observation_id=args.observation
    )
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
