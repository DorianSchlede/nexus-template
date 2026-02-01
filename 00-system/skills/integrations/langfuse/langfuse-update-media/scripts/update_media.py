#!/usr/bin/env python3
"""Langfuse Update Media."""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "langfuse-master" / "scripts"))
from langfuse_client import get_client


def update_media(media_id: str, uploaded: bool = None) -> dict:
    client = get_client()
    data = {}
    if uploaded is not None:
        data["uploadedToGcs"] = uploaded
    return client.patch(f"/media/{media_id}", data=data)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--media", type=str, required=True)
    parser.add_argument("--uploaded", action="store_true", help="Mark as uploaded")
    args = parser.parse_args()
    result = update_media(media_id=args.media, uploaded=args.uploaded if args.uploaded else None)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
