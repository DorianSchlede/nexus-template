#!/usr/bin/env python3
"""Langfuse Create Model."""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "langfuse-master" / "scripts"))
from langfuse_client import get_client


def create_model(
    name: str,
    match_pattern: str,
    unit: str = "TOKENS",
    input_price: float = None,
    output_price: float = None,
    total_price: float = None,
    tokenizer: str = None
) -> dict:
    client = get_client()
    data = {
        "modelName": name,
        "matchPattern": match_pattern,
        "unit": unit
    }
    if input_price is not None:
        data["inputPrice"] = input_price
    if output_price is not None:
        data["outputPrice"] = output_price
    if total_price is not None:
        data["totalPrice"] = total_price
    if tokenizer:
        data["tokenizerId"] = tokenizer
    return client.post("/models", data=data)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", type=str, required=True)
    parser.add_argument("--match-pattern", type=str, required=True)
    parser.add_argument("--unit", type=str, default="TOKENS", choices=["TOKENS", "CHARACTERS"])
    parser.add_argument("--input-price", type=float, default=None)
    parser.add_argument("--output-price", type=float, default=None)
    parser.add_argument("--total-price", type=float, default=None)
    parser.add_argument("--tokenizer", type=str, default=None, choices=["openai", "claude", "none"])
    args = parser.parse_args()
    result = create_model(
        name=args.name,
        match_pattern=args.match_pattern,
        unit=args.unit,
        input_price=args.input_price,
        output_price=args.output_price,
        total_price=args.total_price,
        tokenizer=args.tokenizer
    )
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
