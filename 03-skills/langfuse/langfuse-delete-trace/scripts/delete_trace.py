#!/usr/bin/env python3
"""Langfuse Delete Trace."""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "langfuse-master" / "scripts"))
from langfuse_client import get_client


def delete_trace(trace_id: str) -> dict:
    client = get_client()
    return client.delete(f"/traces/{trace_id}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", type=str, required=True)
    args = parser.parse_args()
    result = delete_trace(trace_id=args.id)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
