#!/usr/bin/env python3
"""Langfuse Metrics."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "langfuse-master" / "scripts"))
from langfuse_client import get_client


def get_metrics() -> dict:
    client = get_client()
    return client.get("/metrics")


def main():
    result = get_metrics()
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
