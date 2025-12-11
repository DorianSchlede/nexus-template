#!/usr/bin/env python3
"""
Beam Setup Wizard

Interactive setup for Beam AI integration.
Guides through API key and workspace ID configuration.

Usage:
    python setup_beam.py
"""

import os
import sys
from pathlib import Path

# Find project root
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent.parent.parent.parent
ENV_FILE = PROJECT_ROOT / ".env"

BASE_URL = "https://api.beamstudio.ai"


def print_banner():
    """Print setup wizard banner"""
    print("\n" + "=" * 50)
    print("     Beam AI Setup Wizard")
    print("=" * 50 + "\n")


def get_existing_env_vars():
    """Load existing .env variables"""
    env_vars = {}
    if ENV_FILE.exists():
        with open(ENV_FILE, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, _, value = line.partition('=')
                    env_vars[key.strip()] = value.strip().strip('"\'')
    return env_vars


def update_env_file(key, value):
    """Update or add a key in .env file"""
    lines = []
    key_found = False

    if ENV_FILE.exists():
        with open(ENV_FILE, 'r') as f:
            lines = f.readlines()

        # Update existing key
        for i, line in enumerate(lines):
            if line.strip().startswith(f"{key}="):
                lines[i] = f"{key}={value}\n"
                key_found = True
                break

    # Add new key if not found
    if not key_found:
        if lines and not lines[-1].endswith('\n'):
            lines.append('\n')
        lines.append(f"{key}={value}\n")

    # Write back
    with open(ENV_FILE, 'w') as f:
        f.writelines(lines)


def test_api_key(api_key):
    """Test if API key is valid"""
    try:
        import requests
        response = requests.post(
            f"{BASE_URL}/auth/access-token",
            json={"apiKey": api_key},
            timeout=10
        )
        return response.status_code == 201
    except Exception as e:
        print(f"Error testing API key: {e}")
        return False


def test_workspace(api_key, workspace_id):
    """Test if workspace is accessible"""
    try:
        import requests

        # Get access token
        auth_response = requests.post(
            f"{BASE_URL}/auth/access-token",
            json={"apiKey": api_key},
            timeout=10
        )
        if auth_response.status_code != 201:
            return False

        token = auth_response.json().get('idToken')

        # Try listing agents
        response = requests.get(
            f"{BASE_URL}/agent",
            headers={
                'Authorization': f'Bearer {token}',
                'current-workspace-id': workspace_id
            },
            timeout=10
        )
        return response.status_code == 200
    except Exception as e:
        print(f"Error testing workspace: {e}")
        return False


def main():
    print_banner()

    # Check for requests library
    try:
        import requests
    except ImportError:
        print("Error: 'requests' library not installed")
        print("Install with: pip install requests")
        sys.exit(1)

    existing_vars = get_existing_env_vars()

    # Step 1: API Key
    print("Step 1: Beam API Key")
    print("-" * 30)
    print("\nTo get your API key:")
    print("  1. Log into Beam AI (app.beam.ai)")
    print("  2. Go to Settings → API Keys")
    print("  3. Click 'Create API Key'")
    print("  4. Copy the key (starts with 'bm_key_')")

    existing_key = existing_vars.get('BEAM_API_KEY', '')
    if existing_key and existing_key.startswith('bm_key_'):
        print(f"\nExisting API key found: {existing_key[:15]}...")
        use_existing = input("Use existing key? (y/n): ").strip().lower()
        if use_existing == 'y':
            api_key = existing_key
        else:
            api_key = input("\nEnter your Beam API key: ").strip()
    else:
        api_key = input("\nEnter your Beam API key: ").strip()

    # Validate API key format
    if not api_key.startswith('bm_key_'):
        print("\n⚠️  Warning: API key should start with 'bm_key_'")
        proceed = input("Proceed anyway? (y/n): ").strip().lower()
        if proceed != 'y':
            print("Setup cancelled.")
            sys.exit(1)

    # Test API key
    print("\nTesting API key...")
    if test_api_key(api_key):
        print("✅ API key is valid!")
        update_env_file('BEAM_API_KEY', api_key)
    else:
        print("❌ API key test failed")
        print("Please verify your API key and try again")
        sys.exit(1)

    # Step 2: Workspace ID
    print("\n" + "-" * 30)
    print("Step 2: Workspace ID")
    print("-" * 30)
    print("\nTo find your Workspace ID:")
    print("  1. In Beam, go to Settings → Workspace")
    print("  2. Copy the Workspace ID (UUID format)")
    print("  Or check URL: app.beam.ai/workspace/{workspace-id}/...")

    existing_workspace = existing_vars.get('BEAM_WORKSPACE_ID', '')
    if existing_workspace:
        print(f"\nExisting workspace ID found: {existing_workspace}")
        use_existing = input("Use existing workspace ID? (y/n): ").strip().lower()
        if use_existing == 'y':
            workspace_id = existing_workspace
        else:
            workspace_id = input("\nEnter your Workspace ID: ").strip()
    else:
        workspace_id = input("\nEnter your Workspace ID: ").strip()

    # Test workspace access
    print("\nTesting workspace access...")
    if test_workspace(api_key, workspace_id):
        print("✅ Workspace is accessible!")
        update_env_file('BEAM_WORKSPACE_ID', workspace_id)
    else:
        print("⚠️  Could not verify workspace access")
        print("This might be due to:")
        print("  - Invalid workspace ID")
        print("  - No access permissions")
        print("  - Network issues")
        save_anyway = input("\nSave configuration anyway? (y/n): ").strip().lower()
        if save_anyway == 'y':
            update_env_file('BEAM_WORKSPACE_ID', workspace_id)
        else:
            print("Setup cancelled.")
            sys.exit(1)

    # Done
    print("\n" + "=" * 50)
    print("✅ Setup Complete!")
    print("=" * 50)
    print(f"\nConfiguration saved to: {ENV_FILE}")
    print("\nYou can now use Beam skills:")
    print("  - 'list beam agents'")
    print("  - 'create beam task'")
    print("  - 'get agent analytics'")
    print("\nTo verify setup, run:")
    print("  python 00-system/skills/beam/beam-master/scripts/check_beam_config.py")
    print()


if __name__ == "__main__":
    main()
