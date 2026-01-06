#!/usr/bin/env python3
"""Langfuse Delete Dataset Run - Delete a run."""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "langfuse-master" / "scripts"))
from langfuse_client import get_client


def delete_dataset_run(dataset_name: str, run_name: str) -> dict:
    """
    Delete a dataset run.

    Args:
        dataset_name: Dataset name
        run_name: Run name to delete

    Returns:
        Deletion confirmation
    """
    client = get_client()
    return client.delete(f"/datasets/{dataset_name}/runs/{run_name}")


def main():
    parser = argparse.ArgumentParser(description="Delete a dataset run")
    parser.add_argument("--dataset", type=str, required=True, help="Dataset name")
    parser.add_argument("--run", type=str, required=True, help="Run name")

    args = parser.parse_args()
    result = delete_dataset_run(dataset_name=args.dataset, run_name=args.run)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
