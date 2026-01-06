#!/usr/bin/env python3
"""Langfuse Get Score Config - Get config by ID."""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "langfuse-master" / "scripts"))
from langfuse_client import get_client


def get_score_config(config_id: str) -> dict:
    client = get_client()
    return client.get(f"/score-configs/{config_id}")


def main():
    parser = argparse.ArgumentParser(description="Get a score config")
    parser.add_argument("--id", type=str, required=True)
    args = parser.parse_args()
    result = get_score_config(config_id=args.id)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
