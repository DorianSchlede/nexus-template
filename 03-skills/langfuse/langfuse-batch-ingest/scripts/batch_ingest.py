#!/usr/bin/env python3
"""Langfuse Batch Ingest."""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "langfuse-master" / "scripts"))
from langfuse_client import get_client


def batch_ingest(batch: list) -> dict:
    client = get_client()
    data = {"batch": batch}
    return client.post("/ingestion", data=data)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=str, help="JSON file with batch array")
    parser.add_argument("--batch", type=str, help="JSON string of batch array")
    args = parser.parse_args()

    if args.file:
        with open(args.file, "r") as f:
            batch = json.load(f)
    elif args.batch:
        batch = json.loads(args.batch)
    else:
        print("Error: Provide --file or --batch", file=sys.stderr)
        sys.exit(1)

    result = batch_ingest(batch=batch)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
