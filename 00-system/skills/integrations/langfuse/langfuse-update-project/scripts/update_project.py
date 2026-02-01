#!/usr/bin/env python3
"""Langfuse Update Project."""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "langfuse-master" / "scripts"))
from langfuse_client import get_client


def update_project(project_id: str, name: str = None) -> dict:
    client = get_client()
    data = {}
    if name:
        data["name"] = name
    return client.put(f"/v2/projects/{project_id}", data=data)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", type=str, required=True)
    parser.add_argument("--name", type=str, default=None)
    args = parser.parse_args()
    result = update_project(project_id=args.project, name=args.name)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
