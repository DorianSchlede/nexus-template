#!/usr/bin/env python3
"""Langfuse Delete Project API Key."""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "langfuse-master" / "scripts"))
from langfuse_client import get_client


def delete_project_api_key(project_id: str, api_key_id: str) -> dict:
    client = get_client()
    return client.delete(f"/v2/projects/{project_id}/api-keys/{api_key_id}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", type=str, required=True)
    parser.add_argument("--key", type=str, required=True)
    args = parser.parse_args()
    result = delete_project_api_key(project_id=args.project, api_key_id=args.key)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
