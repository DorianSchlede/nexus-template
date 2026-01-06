#!/usr/bin/env python3
"""Langfuse Create Comment."""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "langfuse-master" / "scripts"))
from langfuse_client import get_client


def create_comment(object_type: str, object_id: str, content: str, author_user_id: str = None) -> dict:
    client = get_client()
    data = {
        "objectType": object_type,
        "objectId": object_id,
        "content": content
    }
    if author_user_id:
        data["authorUserId"] = author_user_id
    return client.post("/comments", data=data)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--type", type=str, required=True, choices=["TRACE", "OBSERVATION"])
    parser.add_argument("--id", type=str, required=True)
    parser.add_argument("--content", type=str, required=True)
    parser.add_argument("--author", type=str, default=None)
    args = parser.parse_args()
    result = create_comment(
        object_type=args.type,
        object_id=args.id,
        content=args.content,
        author_user_id=args.author
    )
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
