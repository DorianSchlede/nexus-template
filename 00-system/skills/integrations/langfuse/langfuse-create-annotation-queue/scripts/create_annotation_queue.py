#!/usr/bin/env python3
"""Langfuse Create Annotation Queue."""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "langfuse-master" / "scripts"))
from langfuse_client import get_client


def create_annotation_queue(name: str, description: str = None) -> dict:
    client = get_client()
    data = {"name": name}
    if description:
        data["description"] = description
    return client.post("/annotation-queues", data=data)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", type=str, required=True)
    parser.add_argument("--description", type=str)
    args = parser.parse_args()
    result = create_annotation_queue(name=args.name, description=args.description)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
