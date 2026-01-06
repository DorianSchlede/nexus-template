#!/usr/bin/env python3
"""Langfuse Health Check."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "langfuse-master" / "scripts"))
from langfuse_client import get_client


def health_check() -> dict:
    client = get_client()
    return client.get("/health")


def main():
    result = health_check()
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
