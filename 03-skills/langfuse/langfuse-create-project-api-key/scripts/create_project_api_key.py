#!/usr/bin/env python3
"""Langfuse Create Project API Key."""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "langfuse-master" / "scripts"))
from langfuse_client import get_client


def create_project_api_key(project_id: str, note: str = None) -> dict:
    client = get_client()
    data = {}
    if note:
        data["note"] = note
    return client.post(f"/v2/projects/{project_id}/api-keys", data=data)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", type=str, required=True)
    parser.add_argument("--note", type=str, default=None)
    args = parser.parse_args()
    result = create_project_api_key(project_id=args.project, note=args.note)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
