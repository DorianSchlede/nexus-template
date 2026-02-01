#!/usr/bin/env python3
"""Create Langfuse dataset item.

Adds a test case to a dataset with input and expected output.
Validates JSON arguments before sending to API.
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "langfuse-master" / "scripts"))
from langfuse_client import get_client, LangfuseAPIError


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
        dataset_name: Dataset name (must exist)
        input_data: Input data for test case
        expected_output: Expected output (ground truth)
        metadata: Additional metadata
        item_id: Custom item ID (auto-generated if not provided)

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


def parse_json_arg(value: str, arg_name: str) -> dict:
    """Parse JSON argument with helpful error message."""
    try:
        return json.loads(value)
    except json.JSONDecodeError as e:
        print(f"JSON ERROR in --{arg_name}: {e}", file=sys.stderr)
        print(f"Value was: {value[:100]}{'...' if len(value) > 100 else ''}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Create a dataset item (test case)")
    parser.add_argument("--dataset", type=str, required=True, help="Dataset name")
    parser.add_argument("--input", type=str, required=True, help="Input data as JSON object")
    parser.add_argument("--expected", type=str, help="Expected output as JSON object")
    parser.add_argument("--metadata", type=str, help="Metadata as JSON object")
    parser.add_argument("--id", type=str, help="Custom item ID (UUID, auto-generated if not provided)")
    parser.add_argument("--output", "-o", type=str, help="Output file (avoids unicode issues)")

    args = parser.parse_args()

    # Parse JSON arguments with validation
    input_data = parse_json_arg(args.input, "input")
    expected = parse_json_arg(args.expected, "expected") if args.expected else None
    metadata = parse_json_arg(args.metadata, "metadata") if args.metadata else None

    try:
        result = create_dataset_item(
            dataset_name=args.dataset,
            input_data=input_data,
            expected_output=expected,
            metadata=metadata,
            item_id=args.id
        )

        json_output = json.dumps(result, indent=2, default=str, ensure_ascii=False)

        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(json_output)
            print(f"Output written to {args.output}", file=sys.stderr)
        else:
            print(json_output)

    except LangfuseAPIError as e:
        print(f"API ERROR: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
