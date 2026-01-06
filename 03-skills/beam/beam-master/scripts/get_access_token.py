#!/usr/bin/env python3
"""
Get Beam Access Token

Exchange API key for access token.
POST /auth/access-token

Usage:
    python get_access_token.py
    python get_access_token.py --json
"""

import os
import sys
import json
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent.parent.parent.parent
ENV_FILE = PROJECT_ROOT / ".env"
BASE_URL = "https://api.beamstudio.ai"


def load_env():
    """Load environment variables"""
    env_vars = {}
    if ENV_FILE.exists():
        with open(ENV_FILE, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, _, value = line.partition('=')
                    env_vars[key.strip()] = value.strip().strip('"\'')
    return env_vars


def get_access_token(api_key):
    """Exchange API key for access token"""
    import requests

    response = requests.post(
        f"{BASE_URL}/auth/access-token",
        json={"apiKey": api_key},
        timeout=30
    )

    if response.status_code == 201:
        return response.json()
    else:
        raise Exception(f"Auth failed: {response.status_code} - {response.text}")


def main():
    parser = argparse.ArgumentParser(description='Get Beam access token')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()

    try:
        import requests
    except ImportError:
        print("Error: requests library not installed", file=sys.stderr)
        sys.exit(1)

    env_vars = load_env()
    api_key = env_vars.get('BEAM_API_KEY') or os.getenv('BEAM_API_KEY')

    if not api_key:
        print("Error: BEAM_API_KEY not found", file=sys.stderr)
        sys.exit(1)

    try:
        result = get_access_token(api_key)

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print("Access token obtained successfully!")
            print(f"ID Token: {result['idToken'][:50]}...")
            print(f"Refresh Token: {result['refreshToken'][:50]}...")

    except Exception as e:
        if args.json:
            print(json.dumps({"error": str(e)}))
        else:
            print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
