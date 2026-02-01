#!/usr/bin/env python3
"""Langfuse Create Prompt - Create a new prompt in Langfuse."""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "langfuse-master" / "scripts"))
from langfuse_client import get_client


def create_prompt(
    name: str,
    prompt: str,
    prompt_type: str = "text",
    labels: list = None,
    config: dict = None
) -> dict:
    """
    Create a new prompt in Langfuse.

    Args:
        name: Unique prompt name
        prompt: Prompt content (text string or JSON for chat prompts)
        prompt_type: "text" or "chat"
        labels: List of labels (e.g., ["production", "v1"])
        config: Model configuration dict

    Returns:
        Created prompt object
    """
    client = get_client()

    data = {
        "name": name,
        "prompt": prompt,
        "type": prompt_type
    }

    if labels:
        data["labels"] = labels
    if config:
        data["config"] = config

    return client.post("/v2/prompts", data=data)


def main():
    parser = argparse.ArgumentParser(
        description="Create a new prompt in Langfuse"
    )
    parser.add_argument(
        "--name", type=str, required=True,
        help="Unique prompt name"
    )
    parser.add_argument(
        "--prompt", type=str, required=True,
        help="Prompt content (text or JSON for chat)"
    )
    parser.add_argument(
        "--type", dest="prompt_type", type=str, default="text",
        choices=["text", "chat"],
        help="Prompt type: text or chat (default: text)"
    )
    parser.add_argument(
        "--labels", type=str,
        help="Comma-separated labels (e.g., 'production,v1')"
    )
    parser.add_argument(
        "--config", type=str,
        help="Model config as JSON string"
    )

    args = parser.parse_args()

    # Parse labels
    labels = None
    if args.labels:
        labels = [l.strip() for l in args.labels.split(",")]

    # Parse config
    config = None
    if args.config:
        config = json.loads(args.config)

    # Parse prompt (could be JSON for chat type)
    prompt = args.prompt
    if args.prompt_type == "chat":
        try:
            prompt = json.loads(args.prompt)
        except json.JSONDecodeError:
            pass  # Keep as string if not valid JSON

    result = create_prompt(
        name=args.name,
        prompt=prompt,
        prompt_type=args.prompt_type,
        labels=labels,
        config=config
    )

    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
