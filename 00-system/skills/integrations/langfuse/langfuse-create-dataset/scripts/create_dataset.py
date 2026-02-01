#!/usr/bin/env python3
"""Langfuse Create Dataset - Create a new dataset in Langfuse."""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "langfuse-master" / "scripts"))
from langfuse_client import get_client


def create_dataset(
    name: str,
    description: str = None,
    metadata: dict = None
) -> dict:
    """
    Create a new dataset in Langfuse.

    Args:
        name: Unique dataset name
        description: Dataset description
        metadata: Additional metadata dict

    Returns:
        Created dataset object
    """
    client = get_client()

    data = {"name": name}
    if description:
        data["description"] = description
    if metadata:
        data["metadata"] = metadata

    return client.post("/v2/datasets", data=data)


def main():
    parser = argparse.ArgumentParser(description="Create a dataset in Langfuse")
    parser.add_argument("--name", type=str, required=True, help="Dataset name")
    parser.add_argument("--description", type=str, help="Description")
    parser.add_argument("--metadata", type=str, help="Metadata as JSON")

    args = parser.parse_args()

    metadata = None
    if args.metadata:
        metadata = json.loads(args.metadata)

    result = create_dataset(
        name=args.name,
        description=args.description,
        metadata=metadata
    )
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
