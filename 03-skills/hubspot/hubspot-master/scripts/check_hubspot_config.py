#!/usr/bin/env python3
"""
HubSpot Configuration Checker

Pre-flight validation for HubSpot integration.
Checks .env for required variables and tests API connection.

Usage:
    python check_hubspot_config.py          # Human-readable output
    python check_hubspot_config.py --json   # JSON output for AI consumption

Exit codes:
    0 - All checks passed
    1 - Partial config (can proceed with warning)
    2 - Not configured (setup required)
"""

import os
import sys
import json
import argparse
from pathlib import Path

# Find project root (where .env lives)
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent.parent.parent.parent  # hubspot-master/scripts -> Nexus-v4
ENV_FILE = PROJECT_ROOT / ".env"

BASE_URL = "https://api.hubapi.com"


def load_env_file():
    """Load environment variables from .env file."""
    env_vars = {}
    if ENV_FILE.exists():
        with open(ENV_FILE, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, _, value = line.partition('=')
                    env_vars[key.strip()] = value.strip().strip('"\'')
    return env_vars


def check_env_file():
    """Check .env file exists and has required variables."""
    result = {
        "ok": False,
        "path": str(ENV_FILE),
        "exists": ENV_FILE.exists(),
        "has_access_token": False,
        "token_format_valid": False
    }

    if not ENV_FILE.exists():
        return result

    env_vars = load_env_file()

    access_token = env_vars.get('HUBSPOT_ACCESS_TOKEN', '') or os.getenv('HUBSPOT_ACCESS_TOKEN', '')

    result["has_access_token"] = bool(access_token)
    result["token_format_valid"] = access_token.startswith('pat-') if access_token else False
    result["ok"] = result["has_access_token"] and result["token_format_valid"]

    return result


def test_api_connection():
    """Test API connection by making a simple request."""
    result = {
        "ok": False,
        "connected": False,
        "error": None
    }

    try:
        import requests
    except ImportError:
        result["error"] = "requests library not installed"
        return result

    env_vars = load_env_file()
    access_token = env_vars.get('HUBSPOT_ACCESS_TOKEN', '') or os.getenv('HUBSPOT_ACCESS_TOKEN', '')

    if not access_token:
        result["error"] = "No access token available"
        return result

    try:
        # Test with a simple contacts list call (limit 1)
        response = requests.get(
            f"{BASE_URL}/crm/v3/objects/contacts",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            },
            params={"limit": 1},
            timeout=10
        )

        if response.status_code == 200:
            result["ok"] = True
            result["connected"] = True
        elif response.status_code == 401:
            result["error"] = "Invalid or expired access token"
        elif response.status_code == 403:
            # May still be connected, just missing scope
            result["connected"] = True
            result["error"] = "Missing required scope (contacts.read)"
        else:
            result["error"] = f"API returned status {response.status_code}"

    except requests.exceptions.Timeout:
        result["error"] = "Connection timeout"
    except requests.exceptions.ConnectionError:
        result["error"] = "Cannot connect to HubSpot API"
    except Exception as e:
        result["error"] = str(e)

    return result


def get_status_and_action(env_check, api_check):
    """Determine overall status and recommended AI action."""

    if env_check["ok"] and api_check["ok"]:
        return "configured", 0, "proceed_with_operation"

    if not env_check["exists"]:
        return "not_configured", 2, "create_env_file"

    if not env_check["has_access_token"]:
        return "not_configured", 2, "prompt_for_access_token"

    if not env_check["token_format_valid"]:
        return "not_configured", 2, "prompt_for_access_token"

    if not api_check["ok"] and api_check["connected"]:
        # Connected but missing scopes
        return "partial", 1, "add_missing_scopes"

    if not api_check["ok"]:
        return "partial", 1, "verify_token"

    return "configured", 0, "proceed_with_operation"


def get_missing_items(env_check):
    """Get list of missing configuration items."""
    missing = []

    if not env_check["exists"]:
        missing.append({
            "item": ".env file",
            "required": True,
            "location": str(ENV_FILE)
        })

    if not env_check["has_access_token"]:
        missing.append({
            "item": "HUBSPOT_ACCESS_TOKEN",
            "required": True,
            "location": ".env",
            "note": "Private App access token from HubSpot"
        })
    elif not env_check["token_format_valid"]:
        missing.append({
            "item": "HUBSPOT_ACCESS_TOKEN",
            "required": True,
            "location": ".env",
            "note": "Token should start with 'pat-' (Private App Token)"
        })

    return missing


def get_fix_instructions(missing, api_check):
    """Get step-by-step fix instructions."""
    instructions = []
    step = 1

    for item in missing:
        if item["item"] == ".env file":
            instructions.append({
                "step": step,
                "action": "Create .env file",
                "details": [
                    f"Create file at: {ENV_FILE}",
                    "Add your HubSpot credentials"
                ]
            })
            step += 1
        elif item["item"] == "HUBSPOT_ACCESS_TOKEN":
            instructions.append({
                "step": step,
                "action": "Get HubSpot Private App Token",
                "details": [
                    "Log into HubSpot",
                    "Go to Settings → Integrations → Private Apps",
                    "Create a new Private App (or use existing)",
                    "Select required scopes (contacts, companies, deals)",
                    "Copy the access token (starts with 'pat-')"
                ]
            })
            step += 1

    if api_check and api_check.get("error") == "Missing required scope (contacts.read)":
        instructions.append({
            "step": step,
            "action": "Add missing scopes",
            "details": [
                "Go to your Private App settings in HubSpot",
                "Add the required scopes:",
                "  - crm.objects.contacts.read",
                "  - crm.objects.companies.read",
                "  - crm.objects.deals.read",
                "Re-create the access token after adding scopes"
            ]
        })

    return instructions


def print_human_output(env_check, api_check, status, missing):
    """Print human-readable output."""

    print("\n" + "=" * 50)
    print("HubSpot Configuration Check")
    print("=" * 50 + "\n")

    # Environment file
    if env_check["exists"]:
        print(f"[OK] .env file found: {env_check['path']}")
    else:
        print(f"[X] .env file not found: {env_check['path']}")

    # Access Token
    if env_check["has_access_token"]:
        if env_check["token_format_valid"]:
            print("[OK] HUBSPOT_ACCESS_TOKEN configured (valid format)")
        else:
            print("[!] HUBSPOT_ACCESS_TOKEN found but invalid format (should start with 'pat-')")
    else:
        print("[X] HUBSPOT_ACCESS_TOKEN missing")

    # API Connection
    if api_check["ok"]:
        print("[OK] API connection successful")
    elif api_check["connected"]:
        print(f"[!] API connected but: {api_check.get('error', 'Unknown issue')}")
    else:
        error = api_check.get("error", "Unknown error")
        print(f"[X] API connection failed: {error}")

    print("\n" + "-" * 50)

    # Overall status
    if status == "configured":
        print("\n[OK] ALL CHECKS PASSED")
        print("You're ready to use HubSpot skills")
    elif status == "partial":
        print("\n[!] PARTIAL CONFIGURATION")
        print("Some features may not work")
    else:
        print("\n[X] SETUP REQUIRED")
        print("\nMissing configuration:")
        for item in missing:
            print(f"  - {item['item']}: {item.get('note', '')}")

        print("\nTo fix:")
        print("  1. Run: python 00-system/skills/hubspot/hubspot-master/scripts/setup_hubspot.py")
        print("  2. Or manually add to .env:")
        print("     HUBSPOT_ACCESS_TOKEN=pat-na1-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx")

    print()


def main():
    parser = argparse.ArgumentParser(description='Check HubSpot configuration')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()

    # Run checks
    env_check = check_env_file()
    api_check = test_api_connection()

    # Determine status
    status, exit_code, ai_action = get_status_and_action(env_check, api_check)
    missing = get_missing_items(env_check)
    fix_instructions = get_fix_instructions(missing, api_check)

    if args.json:
        # JSON output for AI consumption
        output = {
            "status": status,
            "exit_code": exit_code,
            "ai_action": ai_action,
            "checks": {
                "env_file": env_check,
                "api_connection": api_check
            },
            "missing": missing,
            "fix_instructions": fix_instructions,
            "env_template": "HUBSPOT_ACCESS_TOKEN=pat-na1-YOUR_TOKEN_HERE",
            "setup_wizard": "python 00-system/skills/hubspot/hubspot-master/scripts/setup_hubspot.py"
        }
        print(json.dumps(output, indent=2))
    else:
        # Human-readable output
        print_human_output(env_check, api_check, status, missing)

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
