#!/usr/bin/env python3
"""
Refresh Beam Access Token

Refresh an expired access token.
POST /auth/refresh-token

Usage:
    python refresh_token.py --refresh-token TOKEN
    python refresh_token.py --refresh-token TOKEN --json
"""

import sys
import json
import argparse

BASE_URL = "https://api.beamstudio.ai"


def refresh_access_token(refresh_token):
    """Refresh access token"""
    import requests

    response = requests.post(
        f"{BASE_URL}/auth/refresh-token",
        json={"refreshToken": refresh_token},
        timeout=30
    )

    if response.status_code == 201:
        return response.json()
    else:
        raise Exception(f"Refresh failed: {response.status_code} - {response.text}")


def main():
    parser = argparse.ArgumentParser(description='Refresh Beam access token')
    parser.add_argument('--refresh-token', required=True, help='Refresh token')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()

    try:
        import requests
    except ImportError:
        print("Error: requests library not installed", file=sys.stderr)
        sys.exit(1)

    try:
        result = refresh_access_token(args.refresh_token)

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print("Token refreshed successfully!")
            print(f"New ID Token: {result['idToken'][:50]}...")

    except Exception as e:
        if args.json:
            print(json.dumps({"error": str(e)}))
        else:
            print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
