#!/usr/bin/env python3
"""Langfuse Create Score - Add score to trace/observation.

Supports both NUMERIC and CATEGORICAL score types.
For CATEGORICAL scores, use --string-value with the category label.
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "langfuse-master" / "scripts"))
from langfuse_client import get_client


def create_score(
    trace_id: str,
    name: str,
    value: float = None,
    string_value: str = None,
    data_type: str = None,
    observation_id: str = None,
    comment: str = None,
    config_id: str = None
) -> dict:
    """Create a score on a trace or observation.

    For NUMERIC scores: use value (float)
    For CATEGORICAL scores: use string_value (category label)
    """
    client = get_client()
    data = {"traceId": trace_id, "name": name}

    # Handle CATEGORICAL vs NUMERIC
    if string_value is not None:
        data["stringValue"] = string_value
        data["dataType"] = data_type or "CATEGORICAL"
    elif value is not None:
        data["value"] = value
        if data_type:
            data["dataType"] = data_type

    if observation_id:
        data["observationId"] = observation_id
    if comment:
        data["comment"] = comment
    if config_id:
        data["configId"] = config_id
    return client.post("/scores", data=data)


def main():
    parser = argparse.ArgumentParser(description="Create a score")
    parser.add_argument("--trace", type=str, required=True, help="Trace ID")
    parser.add_argument("--name", type=str, required=True, help="Score name")
    parser.add_argument("--value", type=float, help="Numeric value (for NUMERIC scores)")
    parser.add_argument("--string-value", type=str, help="Category label (for CATEGORICAL scores)")
    parser.add_argument("--data-type", type=str, choices=["NUMERIC", "CATEGORICAL", "BOOLEAN"],
                        help="Score data type (auto-detected from value type)")
    parser.add_argument("--observation", type=str, help="Observation ID (optional)")
    parser.add_argument("--comment", type=str, help="Score comment")
    parser.add_argument("--config-id", type=str, help="Score config ID")
    args = parser.parse_args()

    result = create_score(
        trace_id=args.trace,
        name=args.name,
        value=args.value,
        string_value=args.string_value,
        data_type=args.data_type,
        observation_id=args.observation,
        comment=args.comment,
        config_id=args.config_id
    )
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
