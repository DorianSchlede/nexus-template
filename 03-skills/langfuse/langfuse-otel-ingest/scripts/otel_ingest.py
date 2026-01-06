#!/usr/bin/env python3
"""Langfuse OpenTelemetry Ingest."""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "langfuse-master" / "scripts"))
from langfuse_client import get_client


def otel_ingest(resource_spans: list) -> dict:
    client = get_client()
    data = {"resourceSpans": resource_spans}
    return client.post("/otel/v1/traces", data=data)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=str, help="JSON file with OTLP spans")
    parser.add_argument("--spans", type=str, help="JSON string of resource spans")
    args = parser.parse_args()

    if args.file:
        with open(args.file, "r") as f:
            data = json.load(f)
            resource_spans = data.get("resourceSpans", data)
    elif args.spans:
        resource_spans = json.loads(args.spans)
    else:
        print("Error: Provide --file or --spans", file=sys.stderr)
        sys.exit(1)

    result = otel_ingest(resource_spans=resource_spans)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
