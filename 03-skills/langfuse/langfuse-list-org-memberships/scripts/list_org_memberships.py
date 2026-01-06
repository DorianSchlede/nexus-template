#!/usr/bin/env python3
"""Langfuse List Organization Memberships."""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "langfuse-master" / "scripts"))
from langfuse_client import get_client


def list_org_memberships(org_id: str) -> dict:
    client = get_client()
    return client.get(f"/v2/organizations/{org_id}/memberships")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--org", type=str, required=True)
    args = parser.parse_args()
    result = list_org_memberships(org_id=args.org)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
