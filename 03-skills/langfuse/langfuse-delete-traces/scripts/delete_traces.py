#!/usr/bin/env python3
"""Langfuse Bulk Delete Traces."""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "langfuse-master" / "scripts"))
from langfuse_client import get_client


def delete_traces(trace_ids: list = None, filter_obj: dict = None) -> dict:
    client = get_client()
    data = {}
    if trace_ids:
        data["traceIds"] = trace_ids
    if filter_obj:
        data["filter"] = filter_obj
    return client.delete("/traces", params=data)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ids", type=str, help="Comma-separated trace IDs")
    parser.add_argument("--filter", type=str, help="JSON filter object")
    args = parser.parse_args()

    trace_ids = args.ids.split(",") if args.ids else None
    filter_obj = json.loads(args.filter) if args.filter else None

    result = delete_traces(trace_ids=trace_ids, filter_obj=filter_obj)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
