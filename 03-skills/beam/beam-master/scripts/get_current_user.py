#!/usr/bin/env python3
"""
Get Current User

GET /v2/user/me - Retrieve current user profile.

Usage:
    python get_current_user.py
    python get_current_user.py --json
"""

import sys
import json
import argparse
from beam_client import get_client


def main():
    parser = argparse.ArgumentParser(description='Get current user profile')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()

    try:
        client = get_client()
        result = client.get('/v2/user/me')

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"User ID: {result.get('id', 'N/A')}")
            print(f"Email: {result.get('email', 'N/A')}")
            print(f"Name: {result.get('name', 'N/A')}")

    except Exception as e:
        if args.json:
            print(json.dumps({"error": str(e)}))
        else:
            print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
