#!/usr/bin/env python3
"""Langfuse Create Score Config - Create a score configuration."""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "langfuse-master" / "scripts"))
from langfuse_client import get_client


def create_score_config(
    name: str,
    data_type: str,
    min_value: float = None,
    max_value: float = None,
    categories: list = None,
    description: str = None
) -> dict:
    client = get_client()
    data = {"name": name, "dataType": data_type}
    if min_value is not None:
        data["minValue"] = min_value
    if max_value is not None:
        data["maxValue"] = max_value
    if categories:
        data["categories"] = [{"label": c, "value": i} for i, c in enumerate(categories)]
    if description:
        data["description"] = description
    return client.post("/score-configs", data=data)


def main():
    parser = argparse.ArgumentParser(description="Create a score config")
    parser.add_argument("--name", type=str, required=True)
    parser.add_argument("--data-type", type=str, required=True, choices=["NUMERIC", "CATEGORICAL", "BOOLEAN"])
    parser.add_argument("--min", type=float, dest="min_value")
    parser.add_argument("--max", type=float, dest="max_value")
    parser.add_argument("--categories", type=str, help="Comma-separated")
    parser.add_argument("--description", type=str)
    args = parser.parse_args()

    categories = args.categories.split(",") if args.categories else None
    result = create_score_config(
        name=args.name,
        data_type=args.data_type,
        min_value=args.min_value,
        max_value=args.max_value,
        categories=categories,
        description=args.description
    )
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
