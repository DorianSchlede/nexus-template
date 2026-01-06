#!/usr/bin/env python3
"""
NotebookLM Enterprise Configuration Checker

Pre-flight validation for NotebookLM Enterprise integration.
Checks for gcloud CLI, project configuration, and tests API connection.

Usage:
    python check_notebooklm_config.py           # Human-readable output
    python check_notebooklm_config.py --json    # JSON output for AI parsing
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent.parent.parent.parent
ENV_FILE = PROJECT_ROOT / ".env"


def load_env():
    """Load environment variables from .env"""
    env_vars = {}
    if ENV_FILE.exists():
        with open(ENV_FILE, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, _, value = line.partition('=')
                    env_vars[key.strip()] = value.strip().strip('"\'')
    return env_vars


def check_gcloud():
    """Check if gcloud CLI is installed and authenticated"""
    try:
        # Check if gcloud exists
        result = subprocess.run(
            ['gcloud', '--version'],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            return {"installed": False, "authenticated": False, "error": "gcloud not found"}

        # Check if authenticated
        result = subprocess.run(
            ['gcloud', 'auth', 'print-access-token'],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            return {"installed": True, "authenticated": False, "error": "Not authenticated"}

        # Get current project
        result = subprocess.run(
            ['gcloud', 'config', 'get-value', 'project'],
            capture_output=True,
            text=True
        )
        project = result.stdout.strip() if result.returncode == 0 else None

        return {"installed": True, "authenticated": True, "project": project}

    except FileNotFoundError:
        return {"installed": False, "authenticated": False, "error": "gcloud CLI not found"}


def check_config():
    """Check NotebookLM configuration status"""
    env_vars = load_env()
    gcloud_status = check_gcloud()

    result = {
        "status": "configured",
        "exit_code": 0,
        "ai_action": "proceed_with_operation",
        "gcloud": gcloud_status,
        "missing": [],
        "present": [],
        "fix_instructions": [],
        "env_template": """# NotebookLM Enterprise Configuration
GOOGLE_CLOUD_PROJECT_NUMBER=your_project_number
NOTEBOOKLM_LOCATION=global
NOTEBOOKLM_ENDPOINT_LOCATION=global""",
        "setup_wizard": f"python {SCRIPT_DIR}/setup_notebooklm.py"
    }

    # Check gcloud first
    if not gcloud_status.get("installed"):
        result["status"] = "not_configured"
        result["exit_code"] = 1
        result["ai_action"] = "install_gcloud"
        result["missing"].append({
            "item": "gcloud CLI",
            "required": True,
            "description": "Google Cloud SDK command-line tool",
            "location": "system"
        })
        result["fix_instructions"].append(
            "Install Google Cloud SDK: https://cloud.google.com/sdk/docs/install"
        )
        return result

    if not gcloud_status.get("authenticated"):
        result["status"] = "not_configured"
        result["exit_code"] = 1
        result["ai_action"] = "run_gcloud_auth"
        result["missing"].append({
            "item": "gcloud authentication",
            "required": True,
            "description": "gcloud CLI authentication",
            "location": "system"
        })
        result["fix_instructions"].append("Run: gcloud auth login")
        return result

    # Check required environment variables
    required_vars = [
        ("GOOGLE_CLOUD_PROJECT_NUMBER", "Your Google Cloud project number (not ID)"),
        ("NOTEBOOKLM_LOCATION", "Data storage location (e.g., global)"),
        ("NOTEBOOKLM_ENDPOINT_LOCATION", "API endpoint prefix (us, eu, or global)"),
    ]

    for var_name, description in required_vars:
        value = env_vars.get(var_name) or os.getenv(var_name)
        if value:
            result["present"].append({
                "item": var_name,
                "description": description,
                "value": value
            })
        else:
            result["missing"].append({
                "item": var_name,
                "required": var_name == "GOOGLE_CLOUD_PROJECT_NUMBER",
                "description": description,
                "location": ".env"
            })

    # Determine status and action
    if any(m["required"] for m in result["missing"]):
        result["status"] = "not_configured"
        result["exit_code"] = 2
        result["ai_action"] = "configure_project"
        result["fix_instructions"].append(
            "Get your project number from: https://console.cloud.google.com/home/dashboard"
        )
        result["fix_instructions"].append(
            "Add to .env: GOOGLE_CLOUD_PROJECT_NUMBER=your_number"
        )

    return result


def test_connection(env_vars):
    """Test API connection"""
    try:
        import requests

        project_number = env_vars.get('GOOGLE_CLOUD_PROJECT_NUMBER') or os.getenv('GOOGLE_CLOUD_PROJECT_NUMBER')
        location = env_vars.get('NOTEBOOKLM_LOCATION') or os.getenv('NOTEBOOKLM_LOCATION') or 'global'
        endpoint_location = env_vars.get('NOTEBOOKLM_ENDPOINT_LOCATION') or os.getenv('NOTEBOOKLM_ENDPOINT_LOCATION') or 'global'

        if not project_number:
            return {"success": False, "error": "No project number"}

        # Get access token
        result = subprocess.run(
            ['gcloud', 'auth', 'print-access-token'],
            capture_output=True,
            text=True,
            check=True
        )
        token = result.stdout.strip()

        # Try to list notebooks (may return empty list, that's OK)
        prefix = f"{endpoint_location}-" if endpoint_location != 'global' else 'global-'
        url = f"https://{prefix}discoveryengine.googleapis.com/v1alpha/projects/{project_number}/locations/{location}/notebooks:listRecentlyViewed"

        response = requests.get(
            url,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            },
            timeout=30
        )

        if response.status_code == 200:
            return {"success": True, "message": "API connection successful"}
        elif response.status_code == 403:
            return {"success": False, "error": "Permission denied - enable NotebookLM Enterprise API in Cloud Console"}
        else:
            return {"success": False, "error": f"HTTP {response.status_code}: {response.text[:200]}"}

    except subprocess.CalledProcessError as e:
        return {"success": False, "error": f"gcloud error: {e.stderr}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def main():
    parser = argparse.ArgumentParser(description="Check NotebookLM Enterprise configuration")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--test", action="store_true", help="Test API connection")
    args = parser.parse_args()

    result = check_config()

    if args.test and result["status"] == "configured":
        env_vars = load_env()
        test_result = test_connection(env_vars)
        result["connection_test"] = test_result
        if not test_result.get("success"):
            result["status"] = "connection_failed"
            result["exit_code"] = 3

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        # Human-readable output
        print("NotebookLM Enterprise Configuration Status")
        print("=" * 45)

        # gcloud status
        print(f"\ngcloud CLI: {'Installed' if result['gcloud'].get('installed') else 'NOT INSTALLED'}")
        print(f"gcloud Auth: {'Authenticated' if result['gcloud'].get('authenticated') else 'NOT AUTHENTICATED'}")
        if result['gcloud'].get('project'):
            print(f"gcloud Project: {result['gcloud']['project']}")

        print()

        if result["status"] == "configured":
            print("Status: CONFIGURED")
            print()
            print("Environment variables:")
            for item in result["present"]:
                print(f"  {item['item']}: {item['value']}")

            if "connection_test" in result:
                print()
                if result["connection_test"]["success"]:
                    print("Connection: OK")
                else:
                    print(f"Connection: FAILED - {result['connection_test']['error']}")
        else:
            print("Status: NOT CONFIGURED")
            print()
            if result["missing"]:
                print("Missing:")
                for item in result["missing"]:
                    req = " (required)" if item.get("required") else ""
                    print(f"  {item['item']}{req}: {item['description']}")
            print()
            print("To fix:")
            for instruction in result["fix_instructions"]:
                print(f"  - {instruction}")
            print()
            print(f"Or run: {result['setup_wizard']}")

    sys.exit(result["exit_code"])


if __name__ == "__main__":
    main()
