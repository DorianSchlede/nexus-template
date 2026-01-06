#!/usr/bin/env python3
"""
HeyReach Configuration Checker

Validates HeyReach API configuration and provides actionable guidance.
Returns JSON output for AI consumption.

Usage:
    python check_heyreach_config.py [--json]

Exit codes:
    0 = Configured and working
    1 = Partial configuration (needs fixes)
    2 = Not configured
"""

import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent.parent.parent.parent
ENV_FILE = PROJECT_ROOT / ".env"


def check_config():
    """Check HeyReach configuration status."""
    result = {
        "configured": False,
        "api_key_found": False,
        "api_key_valid": None,
        "env_file_exists": ENV_FILE.exists(),
        "issues": [],
        "ai_action": None
    }

    # Check if .env exists
    if not ENV_FILE.exists():
        result["issues"].append("No .env file found")
        result["ai_action"] = "create_env_file"
        return result

    # Load .env
    env_vars = {}
    with open(ENV_FILE, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, _, value = line.partition('=')
                env_vars[key.strip()] = value.strip().strip('"\'')

    # Check for API key
    api_key = env_vars.get('HEYREACH_API_KEY', '')

    if not api_key:
        result["issues"].append("HEYREACH_API_KEY not found in .env")
        result["ai_action"] = "prompt_for_api_key"
        return result

    result["api_key_found"] = True

    # Validate API key format (basic check)
    if len(api_key) < 10:
        result["issues"].append("API key appears too short")
        result["ai_action"] = "verify_api_key"
        return result

    # Test API connection
    try:
        import requests
        response = requests.get(
            "https://api.heyreach.io/api/public/auth/CheckApiKey",
            headers={"X-API-KEY": api_key},
            timeout=10
        )

        if response.status_code == 200:
            result["api_key_valid"] = True
            result["configured"] = True
            result["ai_action"] = "proceed_with_operation"
        elif response.status_code == 401:
            result["api_key_valid"] = False
            result["issues"].append("API key is invalid or expired")
            result["ai_action"] = "prompt_for_api_key"
        elif response.status_code == 403:
            result["api_key_valid"] = False
            result["issues"].append("API key lacks required permissions")
            result["ai_action"] = "verify_api_key"
        else:
            result["issues"].append(f"Unexpected response: {response.status_code}")
            result["ai_action"] = "verify_api_key"

    except requests.exceptions.Timeout:
        result["issues"].append("Connection timeout - HeyReach API may be down")
        result["ai_action"] = "retry_later"
    except requests.exceptions.ConnectionError:
        result["issues"].append("Cannot connect to HeyReach API")
        result["ai_action"] = "check_network"
    except ImportError:
        result["issues"].append("requests library not installed")
        result["ai_action"] = "install_requests"
    except Exception as e:
        result["issues"].append(f"Unexpected error: {str(e)}")
        result["ai_action"] = "verify_api_key"

    return result


def main():
    parser = argparse.ArgumentParser(description='Check HeyReach configuration')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()

    result = check_config()

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print("HeyReach Configuration Check")
        print("=" * 40)
        print(f"Configured: {'Yes' if result['configured'] else 'No'}")
        print(f"API Key Found: {'Yes' if result['api_key_found'] else 'No'}")
        print(f"API Key Valid: {result['api_key_valid']}")
        print(f".env Exists: {'Yes' if result['env_file_exists'] else 'No'}")

        if result["issues"]:
            print("\nIssues:")
            for issue in result["issues"]:
                print(f"  - {issue}")

        if result["ai_action"]:
            print(f"\nRecommended Action: {result['ai_action']}")

    # Exit codes
    if result["configured"]:
        sys.exit(0)
    elif result["api_key_found"]:
        sys.exit(1)
    else:
        sys.exit(2)


if __name__ == "__main__":
    main()
