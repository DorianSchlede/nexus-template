#!/usr/bin/env python3
"""Langfuse Create Score - Add score to trace/observation.

Supports both NUMERIC and CATEGORICAL score types.
For CATEGORICAL scores, use --string-value with the category label.

IMPORTANT: This script validates CATEGORICAL values BEFORE sending to the API.
Langfuse API does NOT validate - it accepts invalid values and creates garbage data.
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "langfuse-master" / "scripts"))
from langfuse_client import get_client


# ============================================================================
# SCORE CONFIG REGISTRY - Known configs with validation rules
# ============================================================================
# CRITICAL: Langfuse API accepts ANY value without validation!
# We MUST validate client-side to prevent garbage data.

SCORE_CONFIGS = {
    # Quality Dimensions (7)
    "goal_achievement": {
        "id": "68cfd90c-8c9e-4907-808d-869ccd9a4c07",
        "type": "CATEGORICAL",
        "categories": ["failed", "partial", "complete", "exceeded"],
    },
    "tool_efficiency": {
        "id": "84965473-0f54-4248-999e-7b8627fc9c29",
        "type": "NUMERIC",
        "min": 0,
        "max": 1,
    },
    "process_adherence": {
        "id": "651fc213-4750-4d4e-8155-270235c7cad8",
        "type": "NUMERIC",
        "min": 0,
        "max": 1,
    },
    "context_efficiency": {
        "id": "ae22abed-bd4a-4926-af74-8d71edb1925d",
        "type": "NUMERIC",
        "min": 0,
        "max": 1,
    },
    "error_handling": {
        "id": "96c290b7-e3a6-4caa-bace-93cf55f70f1c",
        "type": "CATEGORICAL",
        "categories": ["poor", "struggled", "recovered", "prevented"],
    },
    "output_quality": {
        "id": "d33b1fbf-d3c6-458c-90ca-0b515fe09aed",
        "type": "NUMERIC",
        "min": 0,
        "max": 1,
    },
    "overall_quality": {
        "id": "793f09d9-0053-4310-ad32-00dc06c69a71",
        "type": "NUMERIC",
        "min": 0,
        "max": 1,
    },
    # Meta Scores (3)
    "root_cause_issues": {
        "id": "669bead7-1936-4fc4-bae8-e7814c9eab04",
        "type": "CATEGORICAL",
        "categories": ["none", "tool_misuse", "process_violation", "context_waste", "error_cascade", "output_quality", "multiple"],
    },
    "session_improvements": {
        "id": "2e87193b-c853-4955-b2f0-9fa572531681",
        "type": "CATEGORICAL",
        "categories": ["none", "minor", "moderate", "significant", "critical"],
    },
    "session_notes": {
        "id": "67640329-0c03-4be6-bc9f-49765a0462b5",
        "type": "NUMERIC",
        "min": 0,
        "max": 1,  # Use value=1 with rich comment/metadata
    },
}

# Reverse lookup: config_id -> config_name
CONFIG_ID_TO_NAME = {cfg["id"]: name for name, cfg in SCORE_CONFIGS.items()}


class ValidationError(Exception):
    """Raised when score value fails validation."""
    pass


def validate_score(config_id: str, value, string_value: str = None) -> None:
    """Validate score value against config rules.

    Raises ValidationError if validation fails.
    Does nothing if config_id is not in registry (allows unknown configs).
    """
    if config_id not in CONFIG_ID_TO_NAME:
        # Unknown config - skip validation, let API handle it
        return

    config_name = CONFIG_ID_TO_NAME[config_id]
    config = SCORE_CONFIGS[config_name]

    if config["type"] == "CATEGORICAL":
        # For CATEGORICAL, check string_value or value (when value is string)
        actual_value = string_value if string_value is not None else value

        if actual_value is None:
            raise ValidationError(
                f"CATEGORICAL score '{config_name}' requires a value. "
                f"Valid options: {config['categories']}"
            )

        if str(actual_value) not in config["categories"]:
            raise ValidationError(
                f"Invalid value '{actual_value}' for CATEGORICAL score '{config_name}'. "
                f"Valid options: {config['categories']}"
            )

    elif config["type"] == "NUMERIC":
        if value is None:
            raise ValidationError(
                f"NUMERIC score '{config_name}' requires a numeric value "
                f"between {config['min']} and {config['max']}"
            )

        try:
            num_value = float(value)
        except (TypeError, ValueError):
            raise ValidationError(
                f"NUMERIC score '{config_name}' requires a number, got '{value}'"
            )

        if num_value < config["min"] or num_value > config["max"]:
            raise ValidationError(
                f"Value {num_value} out of range for '{config_name}'. "
                f"Must be between {config['min']} and {config['max']}"
            )


def create_score(
    trace_id: str,
    name: str,
    value: float = None,
    string_value: str = None,
    data_type: str = None,
    observation_id: str = None,
    comment: str = None,
    config_id: str = None,
    metadata: dict = None,
    skip_validation: bool = False
) -> dict:
    """Create a score on a trace or observation.

    For NUMERIC scores: use value (float)
    For CATEGORICAL scores: use string_value (category label)

    Args:
        metadata: Optional dict of structured metadata (no size limit beyond 1MB request)
        skip_validation: If True, skip client-side validation (use with caution!)
    """
    # Validate BEFORE sending to API (Langfuse doesn't validate!)
    if config_id and not skip_validation:
        validate_score(config_id, value, string_value)

    client = get_client()
    data = {"traceId": trace_id, "name": name}

    # Handle value and string_value
    # For CATEGORICAL with configId: use string label as value, don't set dataType
    # For CATEGORICAL without configId: set dataType explicitly
    if string_value is not None and config_id:
        # With configId, use string label as value (Langfuse infers type from config)
        data["value"] = string_value
    elif string_value is not None:
        # Without configId, set both value and stringValue
        data["stringValue"] = string_value
        if value is not None:
            data["value"] = value
        if data_type:
            data["dataType"] = data_type
        else:
            data["dataType"] = "CATEGORICAL"
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
    if metadata:
        data["metadata"] = metadata
    return client.post("/scores", data=data)


def main():
    parser = argparse.ArgumentParser(description="Create a score")
    parser.add_argument("--trace", type=str, help="Trace ID (required unless --list-configs)")
    parser.add_argument("--name", type=str, help="Score name (required unless --list-configs)")
    parser.add_argument("--value", type=float, help="Numeric value (for NUMERIC scores)")
    parser.add_argument("--string-value", type=str, help="Category label (for CATEGORICAL scores)")
    parser.add_argument("--data-type", type=str, choices=["NUMERIC", "CATEGORICAL", "BOOLEAN"],
                        help="Score data type (auto-detected from value type)")
    parser.add_argument("--observation", type=str, help="Observation ID (optional)")
    parser.add_argument("--comment", type=str, help="Score comment")
    parser.add_argument("--config-id", type=str, help="Score config ID")
    parser.add_argument("--metadata", type=str,
                        help="JSON metadata object (e.g., '{\"key\": \"value\"}' or @file.json)")
    parser.add_argument("--skip-validation", action="store_true",
                        help="Skip client-side validation (use with caution!)")
    parser.add_argument("--list-configs", action="store_true",
                        help="List all known score configs and exit")
    args = parser.parse_args()

    # List configs if requested
    if args.list_configs:
        print("Known Score Configs:")
        print("=" * 60)
        for name, cfg in SCORE_CONFIGS.items():
            if cfg["type"] == "CATEGORICAL":
                print(f"\n{name} (CATEGORICAL)")
                print(f"  ID: {cfg['id']}")
                print(f"  Categories: {cfg['categories']}")
            else:
                print(f"\n{name} (NUMERIC)")
                print(f"  ID: {cfg['id']}")
                print(f"  Range: {cfg['min']} - {cfg['max']}")
        return

    # Validate required args for score creation
    if not args.trace or not args.name:
        parser.error("--trace and --name are required for score creation")

    # Parse metadata if provided
    metadata = None
    if args.metadata:
        if args.metadata.startswith("@"):
            # Load from file
            metadata_file = args.metadata[1:]
            try:
                with open(metadata_file, "r", encoding="utf-8") as f:
                    metadata = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError) as e:
                print(f"Error loading metadata file: {e}", file=sys.stderr)
                sys.exit(1)
        else:
            # Parse as JSON string
            try:
                metadata = json.loads(args.metadata)
            except json.JSONDecodeError as e:
                print(f"Invalid JSON in --metadata: {e}", file=sys.stderr)
                sys.exit(1)

    try:
        result = create_score(
            trace_id=args.trace,
            name=args.name,
            value=args.value,
            string_value=args.string_value,
            data_type=args.data_type,
            observation_id=args.observation,
            comment=args.comment,
            config_id=args.config_id,
            metadata=metadata,
            skip_validation=args.skip_validation
        )
        print(json.dumps(result, indent=2, default=str))
    except ValidationError as e:
        print(f"VALIDATION ERROR: {e}", file=sys.stderr)
        print("\nUse --list-configs to see valid options", file=sys.stderr)
        print("Use --skip-validation to bypass (creates garbage data!)", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
