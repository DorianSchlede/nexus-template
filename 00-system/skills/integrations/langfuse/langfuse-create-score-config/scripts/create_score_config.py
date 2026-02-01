#!/usr/bin/env python3
"""Langfuse Create Score Config - Create a score configuration.

IMPORTANT: Validates config parameters BEFORE sending to API.
- CATEGORICAL requires --categories
- NUMERIC should have --min and --max (API accepts without, but creates unusable config)
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "langfuse-master" / "scripts"))
from langfuse_client import get_client, LangfuseAPIError


class ConfigValidationError(Exception):
    """Raised when score config parameters fail validation."""
    pass


def validate_config(data_type: str, min_value: float, max_value: float, categories: list) -> None:
    """Validate score config parameters before API call."""
    if data_type == "CATEGORICAL":
        if not categories or len(categories) < 2:
            raise ConfigValidationError(
                "CATEGORICAL config requires --categories with at least 2 values.\n"
                "Example: --categories 'failed,partial,complete,exceeded'"
            )
    elif data_type == "NUMERIC":
        if min_value is None or max_value is None:
            raise ConfigValidationError(
                "NUMERIC config should have --min and --max values.\n"
                "Example: --min 0 --max 100\n"
                "(API accepts without, but creates unusable config)"
            )
        if min_value >= max_value:
            raise ConfigValidationError(
                f"--min ({min_value}) must be less than --max ({max_value})"
            )
    elif data_type == "BOOLEAN":
        if categories or min_value is not None or max_value is not None:
            raise ConfigValidationError(
                "BOOLEAN config should not have --categories, --min, or --max"
            )


def create_score_config(
    name: str,
    data_type: str,
    min_value: float = None,
    max_value: float = None,
    categories: list = None,
    description: str = None,
    skip_validation: bool = False
) -> dict:
    # Validate before API call
    if not skip_validation:
        validate_config(data_type, min_value, max_value, categories)

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
    parser.add_argument("--categories", type=str, help="Comma-separated (e.g., 'failed,partial,complete')")
    parser.add_argument("--description", type=str)
    parser.add_argument("--skip-validation", action="store_true",
                        help="Skip client-side validation (use with caution!)")
    args = parser.parse_args()

    categories = args.categories.split(",") if args.categories else None

    try:
        result = create_score_config(
            name=args.name,
            data_type=args.data_type,
            min_value=args.min_value,
            max_value=args.max_value,
            categories=categories,
            description=args.description,
            skip_validation=args.skip_validation
        )
        print(json.dumps(result, indent=2, default=str))
    except ConfigValidationError as e:
        print(f"VALIDATION ERROR: {e}", file=sys.stderr)
        print("\nUse --skip-validation to bypass (may create unusable config)", file=sys.stderr)
        sys.exit(1)
    except LangfuseAPIError as e:
        print(f"API ERROR: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
