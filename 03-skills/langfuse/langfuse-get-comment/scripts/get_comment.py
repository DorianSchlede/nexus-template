#!/usr/bin/env python3
"""Langfuse Get Comment."""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "langfuse-master" / "scripts"))
from langfuse_client import get_client


def get_comment(comment_id: str) -> dict:
    client = get_client()
    return client.get(f"/comments/{comment_id}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--comment", type=str, required=True)
    args = parser.parse_args()
    result = get_comment(comment_id=args.comment)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
