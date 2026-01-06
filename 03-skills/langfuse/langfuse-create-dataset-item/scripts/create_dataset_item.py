#!/usr/bin/env python3
"""Langfuse Create Dataset Item - Add item to a dataset."""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "langfuse-master" / "scripts"))
from langfuse_client import get_client


def create_dataset_item(
    dataset_name: str,
    input_data: dict,
    expected_output: dict = None,
    metadata: dict = None,
    item_id: str = None
) -> dict:
    """
    Create a dataset item.

    Args:
        dataset_name: Dataset name
        input_data: Input data for test case
        expected_output: Expected output (ground truth)
        metadata: Additional metadata
        item_id: Custom item ID

    Returns:
        Created item object
    """
    client = get_client()

    data = {
        "datasetName": dataset_name,
        "input": input_data
    }
    if expected_output:
        data["expectedOutput"] = expected_output
    if metadata:
        data["metadata"] = metadata
    if item_id:
        data["id"] = item_id

    return client.post("/dataset-items", data=data)


def main():
    parser = argparse.ArgumentParser(description="Create a dataset item")
    parser.add_argument("--dataset", type=str, required=True, help="Dataset name")
    parser.add_argument("--input", type=str, required=True, help="Input as JSON")
    parser.add_argument("--expected", type=str, help="Expected output as JSON")
    parser.add_argument("--metadata", type=str, help="Metadata as JSON")
    parser.add_argument("--id", type=str, help="Custom item ID")

    args = parser.parse_args()

    input_data = json.loads(args.input)
    expected = json.loads(args.expected) if args.expected else None
    metadata = json.loads(args.metadata) if args.metadata else None

    result = create_dataset_item(
        dataset_name=args.dataset,
        input_data=input_data,
        expected_output=expected,
        metadata=metadata,
        item_id=args.id
    )
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
