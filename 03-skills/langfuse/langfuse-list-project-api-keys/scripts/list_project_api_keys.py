#!/usr/bin/env python3
"""Langfuse List Project API Keys."""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "langfuse-master" / "scripts"))
from langfuse_client import get_client


def list_project_api_keys(project_id: str) -> dict:
    client = get_client()
    return client.get(f"/v2/projects/{project_id}/api-keys")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", type=str, required=True)
    args = parser.parse_args()
    result = list_project_api_keys(project_id=args.project)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
