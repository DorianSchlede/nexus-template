#!/usr/bin/env python3
"""Langfuse List Score Configs - Get score configurations."""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "langfuse-master" / "scripts"))
from langfuse_client import get_client


def list_score_configs(limit: int = 50, page: int = None) -> dict:
    client = get_client()
    params = {"limit": limit}
    if page is not None:
        params["page"] = page
    return client.get("/score-configs", params=params)


def main():
    parser = argparse.ArgumentParser(description="List score configs")
    parser.add_argument("--limit", type=int, default=50)
    parser.add_argument("--page", type=int)
    args = parser.parse_args()
    result = list_score_configs(limit=args.limit, page=args.page)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
