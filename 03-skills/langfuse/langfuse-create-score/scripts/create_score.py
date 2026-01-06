#!/usr/bin/env python3
"""Langfuse Create Score - Add score to trace/observation."""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "langfuse-master" / "scripts"))
from langfuse_client import get_client


def create_score(
    trace_id: str,
    name: str,
    value: float = None,
    observation_id: str = None,
    comment: str = None,
    config_id: str = None
) -> dict:
    client = get_client()
    data = {"traceId": trace_id, "name": name}
    if value is not None:
        data["value"] = value
    if observation_id:
        data["observationId"] = observation_id
    if comment:
        data["comment"] = comment
    if config_id:
        data["configId"] = config_id
    return client.post("/scores", data=data)


def main():
    parser = argparse.ArgumentParser(description="Create a score")
    parser.add_argument("--trace", type=str, required=True)
    parser.add_argument("--name", type=str, required=True)
    parser.add_argument("--value", type=float)
    parser.add_argument("--observation", type=str)
    parser.add_argument("--comment", type=str)
    parser.add_argument("--config-id", type=str)
    args = parser.parse_args()

    result = create_score(
        trace_id=args.trace,
        name=args.name,
        value=args.value,
        observation_id=args.observation,
        comment=args.comment,
        config_id=args.config_id
    )
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
