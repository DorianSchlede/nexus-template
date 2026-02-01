#!/usr/bin/env python3
"""Langfuse Get Media."""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "langfuse-master" / "scripts"))
from langfuse_client import get_client


def get_media(media_id: str) -> dict:
    client = get_client()
    return client.get(f"/media/{media_id}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--media", type=str, required=True)
    args = parser.parse_args()
    result = get_media(media_id=args.media)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
