#!/usr/bin/env python3
"""
Slack Configuration Checker

Pre-flight validation for Slack integration.
Checks .env for required variables and tests API connection.

Usage:
    python check_slack_config.py          # Human-readable output
    python check_slack_config.py --json   # JSON output for AI consumption

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

def find_project_root():
    """Find Nexus project root by looking for CLAUDE.md or .env"""
    current = SCRIPT_DIR
    for _ in range(10):  # Max 10 levels up
        if (current / 'CLAUDE.md').exists():
            return current
        if (current / '.env').exists():
            return current
        parent = current.parent
        if parent == current:  # Reached filesystem root
            break
        current = parent
    # Fallback: use current working directory if it has .env
    cwd = Path.cwd()
    if (cwd / '.env').exists():
        return cwd
    if (cwd / 'CLAUDE.md').exists():
        return cwd
    # Last resort: assume script is in standard location
    return SCRIPT_DIR.parent.parent.parent.parent.parent

PROJECT_ROOT = find_project_root()
ENV_FILE = PROJECT_ROOT / ".env"

BASE_URL = "https://slack.com/api"


def load_env_file():
    """Load environment variables from .env file"""
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
    """Check .env file exists and has required variables"""
    result = {
        "ok": False,
        "path": str(ENV_FILE),
        "exists": ENV_FILE.exists(),
        "has_user_token": False,
        "has_client_id": False,
        "has_client_secret": False,
        "token_type": None
    }

    if not ENV_FILE.exists():
        return result

    env_vars = load_env_file()

    user_token = env_vars.get('SLACK_USER_TOKEN', '') or os.getenv('SLACK_USER_TOKEN', '')
    client_id = env_vars.get('SLACK_CLIENT_ID', '') or os.getenv('SLACK_CLIENT_ID', '')
    client_secret = env_vars.get('SLACK_CLIENT_SECRET', '') or os.getenv('SLACK_CLIENT_SECRET', '')

    result["has_user_token"] = bool(user_token) and user_token.startswith('xoxp-')
    result["has_client_id"] = bool(client_id)
    result["has_client_secret"] = bool(client_secret)

    if user_token:
        if user_token.startswith('xoxp-'):
            result["token_type"] = "user"
        elif user_token.startswith('xoxb-'):
            result["token_type"] = "bot"
        else:
            result["token_type"] = "unknown"

    result["ok"] = result["has_user_token"]

    return result


def test_api_connection():
    """Test API connection by calling auth.test"""
    result = {
        "ok": False,
        "connected": False,
        "user": None,
        "team": None,
        "scopes": [],
        "error": None
    }

    try:
        import requests
    except ImportError:
        result["error"] = "requests library not installed"
        return result

    env_vars = load_env_file()
    user_token = env_vars.get('SLACK_USER_TOKEN', '') or os.getenv('SLACK_USER_TOKEN', '')

    if not user_token:
        result["error"] = "No user token available"
        return result

    try:
        # Test authentication
        response = requests.post(
            f"{BASE_URL}/auth.test",
            headers={
                'Authorization': f'Bearer {user_token}',
                'Content-Type': 'application/json'
            },
            timeout=10
        )

        data = response.json()

        if data.get('ok'):
            result["ok"] = True
            result["connected"] = True
            result["user"] = data.get('user')
            result["user_id"] = data.get('user_id')
            result["team"] = data.get('team')
            result["team_id"] = data.get('team_id')

            # Get scopes from response headers
            scopes_header = response.headers.get('x-oauth-scopes', '')
            result["scopes"] = [s.strip() for s in scopes_header.split(',') if s.strip()]
        else:
            result["error"] = data.get('error', 'Unknown error')

    except requests.exceptions.Timeout:
        result["error"] = "Connection timeout"
    except requests.exceptions.ConnectionError:
        result["error"] = "Cannot connect to Slack API"
    except Exception as e:
        result["error"] = str(e)

    return result


def check_required_scopes(current_scopes):
    """Check if required scopes are present"""
    required_scopes = [
        'channels:read',
        'chat:write',
        'users:read'
    ]

    recommended_scopes = [
        'channels:history',
        'groups:read',
        'groups:history',
        'im:read',
        'im:history',
        'files:read',
        'files:write',
        'search:read',
        'reactions:read',
        'reactions:write'
    ]

    missing_required = [s for s in required_scopes if s not in current_scopes]
    missing_recommended = [s for s in recommended_scopes if s not in current_scopes]

    return {
        "has_required": len(missing_required) == 0,
        "missing_required": missing_required,
        "missing_recommended": missing_recommended
    }


def get_status_and_action(env_check, api_check, scope_check=None):
    """Determine overall status and recommended AI action"""

    if env_check["ok"] and api_check["ok"]:
        if scope_check and not scope_check.get("has_required", True):
            return "partial", 1, "check_scopes"
        return "configured", 0, "proceed_with_operation"

    if not env_check["exists"]:
        return "not_configured", 2, "run_oauth_setup"

    if not env_check["has_user_token"]:
        if env_check["has_client_id"] and env_check["has_client_secret"]:
            return "not_configured", 2, "run_oauth_setup"
        return "not_configured", 2, "create_slack_app"

    if env_check["token_type"] == "bot":
        return "wrong_token_type", 2, "run_oauth_setup"

    if not api_check["ok"]:
        error = api_check.get("error", "")
        if error in ["token_revoked", "invalid_auth"]:
            return "token_invalid", 2, "run_oauth_setup"
        return "partial", 1, "check_connection"

    return "configured", 0, "proceed_with_operation"


def get_missing_items(env_check, api_check):
    """Get list of missing configuration items"""
    missing = []

    if not env_check["exists"]:
        missing.append({
            "item": ".env file",
            "required": True,
            "location": str(ENV_FILE)
        })

    if not env_check["has_user_token"]:
        missing.append({
            "item": "SLACK_USER_TOKEN",
            "required": True,
            "location": ".env",
            "note": "User OAuth token (xoxp-) from OAuth flow"
        })

    if not env_check["has_client_id"]:
        missing.append({
            "item": "SLACK_CLIENT_ID",
            "required": False,
            "location": ".env",
            "note": "Required for OAuth setup flow"
        })

    if not env_check["has_client_secret"]:
        missing.append({
            "item": "SLACK_CLIENT_SECRET",
            "required": False,
            "location": ".env",
            "note": "Required for OAuth setup flow"
        })

    return missing


def get_fix_instructions(env_check, api_check):
    """Get step-by-step fix instructions"""
    instructions = []
    step = 1

    if not env_check["has_client_id"] or not env_check["has_client_secret"]:
        instructions.append({
            "step": step,
            "action": "Create a Slack App",
            "details": [
                "Go to https://api.slack.com/apps",
                "Click 'Create New App' -> 'From scratch'",
                "Name it (e.g., 'Nexus Integration')",
                "Select your workspace"
            ]
        })
        step += 1

        instructions.append({
            "step": step,
            "action": "Configure User OAuth scopes",
            "details": [
                "Go to OAuth & Permissions",
                "Under 'User Token Scopes', add:",
                "  - channels:read, channels:history",
                "  - chat:write",
                "  - users:read",
                "  - (add more as needed)"
            ]
        })
        step += 1

        instructions.append({
            "step": step,
            "action": "Get credentials",
            "details": [
                "Go to Basic Information",
                "Copy Client ID and Client Secret",
                "Add to .env file"
            ]
        })
        step += 1

    if not env_check["has_user_token"]:
        instructions.append({
            "step": step,
            "action": "Run OAuth setup",
            "details": [
                "Run: python 00-system/skills/slack/slack-master/scripts/setup_slack.py",
                "Follow the prompts to authorize",
                "Token will be saved to .env"
            ]
        })
        step += 1

    return instructions


def print_human_output(env_check, api_check, status, missing, scope_check=None):
    """Print human-readable output"""

    print("\n" + "=" * 50)
    print("Slack Configuration Check")
    print("=" * 50 + "\n")

    # Environment file
    if env_check["exists"]:
        print(f"[OK] .env file found: {env_check['path']}")
    else:
        print(f"[X] .env file not found: {env_check['path']}")

    # User Token
    if env_check["has_user_token"]:
        print(f"[OK] SLACK_USER_TOKEN configured (type: {env_check['token_type']})")
    else:
        if env_check["token_type"] == "bot":
            print("[X] Found bot token (xoxb-) but need user token (xoxp-)")
        else:
            print("[X] SLACK_USER_TOKEN missing or invalid")

    # Client credentials
    if env_check["has_client_id"]:
        print("[OK] SLACK_CLIENT_ID configured")
    else:
        print("[!] SLACK_CLIENT_ID not set (needed for OAuth setup)")

    if env_check["has_client_secret"]:
        print("[OK] SLACK_CLIENT_SECRET configured")
    else:
        print("[!] SLACK_CLIENT_SECRET not set (needed for OAuth setup)")

    # API Connection
    if api_check["ok"]:
        print(f"[OK] API connection successful")
        print(f"    User: {api_check.get('user')} ({api_check.get('user_id')})")
        print(f"    Team: {api_check.get('team')} ({api_check.get('team_id')})")
        if api_check.get('scopes'):
            print(f"    Scopes: {len(api_check['scopes'])} configured")
    else:
        error = api_check.get("error", "Unknown error")
        print(f"[X] API connection failed: {error}")

    # Scope check
    if scope_check:
        if scope_check["has_required"]:
            print("[OK] Required scopes present")
        else:
            print("[X] Missing required scopes:")
            for scope in scope_check["missing_required"]:
                print(f"    - {scope}")

        if scope_check["missing_recommended"]:
            print("[!] Missing recommended scopes:")
            for scope in scope_check["missing_recommended"][:5]:
                print(f"    - {scope}")
            if len(scope_check["missing_recommended"]) > 5:
                print(f"    ... and {len(scope_check['missing_recommended']) - 5} more")

    print("\n" + "-" * 50)

    # Overall status
    if status == "configured":
        print("\n[OK] ALL CHECKS PASSED")
        print("You're ready to use Slack skills")
    elif status == "partial":
        print("\n[!] PARTIAL CONFIGURATION")
        print("Some features may not work")
    else:
        print("\n[X] SETUP REQUIRED")
        print("\nMissing configuration:")
        for item in missing:
            required = "required" if item.get("required") else "optional"
            print(f"  - {item['item']} ({required}): {item.get('note', '')}")

        print("\nTo fix:")
        print("  1. Run: python 00-system/skills/slack/slack-master/scripts/setup_slack.py")
        print("  2. Or see: 00-system/skills/slack/slack-master/references/setup-guide.md")

    print()


def main():
    parser = argparse.ArgumentParser(description='Check Slack configuration')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()

    # Run checks
    env_check = check_env_file()
    api_check = test_api_connection()

    # Check scopes if connected
    scope_check = None
    if api_check["ok"] and api_check.get("scopes"):
        scope_check = check_required_scopes(api_check["scopes"])

    # Determine status
    status, exit_code, ai_action = get_status_and_action(env_check, api_check, scope_check)
    missing = get_missing_items(env_check, api_check)
    fix_instructions = get_fix_instructions(env_check, api_check)

    if args.json:
        # JSON output for AI consumption
        output = {
            "status": status,
            "exit_code": exit_code,
            "ai_action": ai_action,
            "checks": {
                "env_file": env_check,
                "api_connection": api_check,
                "scopes": scope_check
            },
            "missing": missing,
            "fix_instructions": fix_instructions,
            "env_template": "SLACK_USER_TOKEN=xoxp-YOUR-USER-TOKEN\nSLACK_CLIENT_ID=your-client-id\nSLACK_CLIENT_SECRET=your-client-secret",
            "setup_wizard": "python 00-system/skills/slack/slack-master/scripts/setup_slack.py"
        }
        print(json.dumps(output, indent=2))
    else:
        # Human-readable output
        print_human_output(env_check, api_check, status, missing, scope_check)

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
