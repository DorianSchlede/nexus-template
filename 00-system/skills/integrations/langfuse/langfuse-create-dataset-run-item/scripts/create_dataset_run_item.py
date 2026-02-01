#!/usr/bin/env python3
"""Langfuse Create Dataset Run Item - Link trace to dataset item."""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "langfuse-master" / "scripts"))
from langfuse_client import get_client


def create_dataset_run_item(
    run_name: str,
    dataset_item_id: str,
    trace_id: str = None,
    observation_id: str = None
) -> dict:
    """
    Create a dataset run item (link trace to dataset item).

    Args:
        run_name: Run name
        dataset_item_id: Dataset item ID
        trace_id: Trace ID to link
        observation_id: Observation ID to link

    Returns:
        Created run item object
    """
    client = get_client()

    data = {
        "runName": run_name,
        "datasetItemId": dataset_item_id
    }
    if trace_id:
        data["traceId"] = trace_id
    if observation_id:
        data["observationId"] = observation_id

    return client.post("/dataset-run-items", data=data)


def main():
    parser = argparse.ArgumentParser(description="Create a dataset run item")
    parser.add_argument("--run", type=str, required=True, help="Run name")
    parser.add_argument("--dataset-item", type=str, required=True, help="Dataset item ID")
    parser.add_argument("--trace", type=str, help="Trace ID")
    parser.add_argument("--observation", type=str, help="Observation ID")

    args = parser.parse_args()
    result = create_dataset_run_item(
        run_name=args.run,
        dataset_item_id=args.dataset_item,
        trace_id=args.trace,
        observation_id=args.observation
    )
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
