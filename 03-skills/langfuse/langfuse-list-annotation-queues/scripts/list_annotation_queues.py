#!/usr/bin/env python3
"""Langfuse List Annotation Queues."""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "langfuse-master" / "scripts"))
from langfuse_client import get_client


def list_annotation_queues(limit: int = 50, page: int = None) -> dict:
    client = get_client()
    params = {"limit": limit}
    if page:
        params["page"] = page
    return client.get("/annotation-queues", params=params)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=50)
    parser.add_argument("--page", type=int)
    args = parser.parse_args()
    result = list_annotation_queues(limit=args.limit, page=args.page)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
