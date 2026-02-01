#!/usr/bin/env python3
"""Langfuse Delete Score - Delete a score."""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "langfuse-master" / "scripts"))
from langfuse_client import get_client


def delete_score(score_id: str) -> dict:
    client = get_client()
    return client.delete(f"/scores/{score_id}")


def main():
    parser = argparse.ArgumentParser(description="Delete a score")
    parser.add_argument("--id", type=str, required=True)
    args = parser.parse_args()
    result = delete_score(score_id=args.id)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
