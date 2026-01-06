#!/usr/bin/env python3
"""
List HeyReach LinkedIn Accounts

Usage:
    python list_accounts.py [--json]
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from heyreach_client import get_client, HeyReachError


def list_accounts():
    client = get_client()
    return client.post("/li_account/GetAll", {})


def main():
    parser = argparse.ArgumentParser(description='List LinkedIn accounts')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()

    try:
        result = list_accounts()

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            accounts = result.get("items", result) if isinstance(result, dict) else result
            if not isinstance(accounts, list):
                accounts = [accounts] if accounts else []

            print(f"Found {len(accounts)} LinkedIn accounts:\n")

            for i, acc in enumerate(accounts, 1):
                print(f"{i}. {acc.get('name', 'Unnamed')}")
                print(f"   Status: {acc.get('status', 'UNKNOWN')}")
                print(f"   LinkedIn: {acc.get('linkedInUrl', 'N/A')}")
                print(f"   ID: {acc.get('id', 'N/A')}\n")

    except HeyReachError as e:
        if args.json:
            print(json.dumps({"error": True, "status_code": e.status_code, "message": e.message}, indent=2))
        else:
            print(f"Error ({e.status_code}): {e.message}")
        sys.exit(1)
    except ValueError as e:
        if args.json:
            print(json.dumps({"error": True, "message": str(e)}, indent=2))
        else:
            print(f"Config Error: {e}")
        sys.exit(2)


if __name__ == "__main__":
    main()
