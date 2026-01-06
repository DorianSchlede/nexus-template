#!/usr/bin/env python3
"""
Beam Configuration Checker

Pre-flight validation for Beam AI integration.
Checks .env for required variables and tests API connection.

Usage:
    python check_beam_config.py          # Human-readable output
    python check_beam_config.py --json   # JSON output for AI consumption

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
PROJECT_ROOT = SCRIPT_DIR.parent.parent.parent.parent.parent  # beam-master/scripts -> Nexus-v4
ENV_FILE = PROJECT_ROOT / ".env"

BASE_URL = "https://api.beamstudio.ai"


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
        "has_api_key": False,
        "has_workspace_id": False
    }

    if not ENV_FILE.exists():
        return result

    env_vars = load_env_file()

    api_key = env_vars.get('BEAM_API_KEY', '') or os.getenv('BEAM_API_KEY', '')
    workspace_id = env_vars.get('BEAM_WORKSPACE_ID', '') or os.getenv('BEAM_WORKSPACE_ID', '')

    result["has_api_key"] = bool(api_key) and api_key.startswith('bm_key_')
    result["has_workspace_id"] = bool(workspace_id)
    result["ok"] = result["has_api_key"] and result["has_workspace_id"]

    return result


def test_api_connection():
    """Test API connection by getting access token"""
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
    api_key = env_vars.get('BEAM_API_KEY', '') or os.getenv('BEAM_API_KEY', '')

    if not api_key:
        result["error"] = "No API key available"
        return result

    try:
        response = requests.post(
            f"{BASE_URL}/auth/access-token",
            json={"apiKey": api_key},
            timeout=10
        )

        if response.status_code == 201:
            result["ok"] = True
            result["connected"] = True
        elif response.status_code == 401:
            result["error"] = "Invalid API key"
        else:
            result["error"] = f"API returned status {response.status_code}"

    except requests.exceptions.Timeout:
        result["error"] = "Connection timeout"
    except requests.exceptions.ConnectionError:
        result["error"] = "Cannot connect to Beam API"
    except Exception as e:
        result["error"] = str(e)

    return result


def get_status_and_action(env_check, api_check):
    """Determine overall status and recommended AI action"""

    if env_check["ok"] and api_check["ok"]:
        return "configured", 0, "proceed_with_operation"

    if not env_check["exists"]:
        return "not_configured", 2, "create_env_file"

    if not env_check["has_api_key"]:
        return "not_configured", 2, "prompt_for_api_key"

    if not env_check["has_workspace_id"]:
        return "partial", 1, "prompt_for_workspace_id"

    if not api_check["ok"]:
        return "partial", 1, "run_setup_wizard"

    return "configured", 0, "proceed_with_operation"


def get_missing_items(env_check):
    """Get list of missing configuration items"""
    missing = []

    if not env_check["exists"]:
        missing.append({
            "item": ".env file",
            "required": True,
            "location": str(ENV_FILE)
        })

    if not env_check["has_api_key"]:
        missing.append({
            "item": "BEAM_API_KEY",
            "required": True,
            "location": ".env",
            "note": "API key from Beam workspace settings"
        })

    if not env_check["has_workspace_id"]:
        missing.append({
            "item": "BEAM_WORKSPACE_ID",
            "required": True,
            "location": ".env",
            "note": "Workspace ID from Beam settings"
        })

    return missing


def get_fix_instructions(missing):
    """Get step-by-step fix instructions"""
    instructions = []
    step = 1

    for item in missing:
        if item["item"] == ".env file":
            instructions.append({
                "step": step,
                "action": "Create .env file",
                "details": [
                    f"Create file at: {ENV_FILE}",
                    "Add your Beam credentials"
                ]
            })
        elif item["item"] == "BEAM_API_KEY":
            instructions.append({
                "step": step,
                "action": "Get Beam API key",
                "details": [
                    "Log into Beam AI (app.beam.ai)",
                    "Go to Settings → API Keys",
                    "Create new API key",
                    "Copy key (starts with bm_key_)"
                ]
            })
        elif item["item"] == "BEAM_WORKSPACE_ID":
            instructions.append({
                "step": step,
                "action": "Get Workspace ID",
                "details": [
                    "In Beam, go to Settings → Workspace",
                    "Copy your Workspace ID (UUID format)"
                ]
            })
        step += 1

    return instructions


def print_human_output(env_check, api_check, status, missing):
    """Print human-readable output"""

    print("\n" + "=" * 50)
    print("Beam Configuration Check")
    print("=" * 50 + "\n")

    # Environment file
    if env_check["exists"]:
        print(f"[OK] .env file found: {env_check['path']}")
    else:
        print(f"[X] .env file not found: {env_check['path']}")

    # API Key
    if env_check["has_api_key"]:
        print("[OK] BEAM_API_KEY configured")
    else:
        print("[X] BEAM_API_KEY missing or invalid")

    # Workspace ID
    if env_check["has_workspace_id"]:
        print("[OK] BEAM_WORKSPACE_ID configured")
    else:
        print("[X] BEAM_WORKSPACE_ID missing")

    # API Connection
    if api_check["ok"]:
        print("[OK] API connection successful")
    else:
        error = api_check.get("error", "Unknown error")
        print(f"[X] API connection failed: {error}")

    print("\n" + "-" * 50)

    # Overall status
    if status == "configured":
        print("\n[OK] ALL CHECKS PASSED")
        print("You're ready to use Beam skills")
    elif status == "partial":
        print("\n[!] PARTIAL CONFIGURATION")
        print("Some features may not work")
    else:
        print("\n[X] SETUP REQUIRED")
        print("\nMissing configuration:")
        for item in missing:
            print(f"  - {item['item']}: {item.get('note', '')}")

        print("\nTo fix:")
        print("  1. Run: python 00-system/skills/beam/beam-master/scripts/setup_beam.py")
        print("  2. Or manually add to .env:")
        print("     BEAM_API_KEY=bm_key_your_key_here")
        print("     BEAM_WORKSPACE_ID=your-workspace-id")

    print()


def main():
    parser = argparse.ArgumentParser(description='Check Beam configuration')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()

    # Run checks
    env_check = check_env_file()
    api_check = test_api_connection()

    # Determine status
    status, exit_code, ai_action = get_status_and_action(env_check, api_check)
    missing = get_missing_items(env_check)
    fix_instructions = get_fix_instructions(missing)

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
            "env_template": "BEAM_API_KEY=bm_key_YOUR_API_KEY_HERE\nBEAM_WORKSPACE_ID=your-workspace-id",
            "setup_wizard": "python 00-system/skills/beam/beam-master/scripts/setup_beam.py"
        }
        print(json.dumps(output, indent=2))
    else:
        # Human-readable output
        print_human_output(env_check, api_check, status, missing)

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
