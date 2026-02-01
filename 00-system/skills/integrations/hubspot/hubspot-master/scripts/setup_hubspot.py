#!/usr/bin/env python3
"""
HubSpot Setup Wizard

Interactive setup for HubSpot integration.
Guides user through Private App token setup and validates configuration.

Usage:
    python setup_hubspot.py
"""

import os
import sys
from pathlib import Path

# Find project root
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent.parent.parent.parent
ENV_FILE = PROJECT_ROOT / ".env"

BASE_URL = "https://api.hubapi.com"


def print_banner():
    """Print setup banner."""
    print("\n" + "=" * 60)
    print("  HubSpot Integration Setup Wizard")
    print("=" * 60 + "\n")


def print_instructions():
    """Print setup instructions."""
    print("To use the HubSpot integration, you need a Private App access token.\n")
    print("STEP 1: Create a Private App in HubSpot")
    print("-" * 40)
    print("  1. Log into HubSpot")
    print("  2. Go to Settings (gear icon)")
    print("  3. Navigate to: Integrations -> Private Apps")
    print("  4. Click 'Create a private app'")
    print("  5. Name it: 'Nexus Integration'")
    print()
    print("STEP 2: Configure Scopes")
    print("-" * 40)
    print("  Select these scopes:")
    print("  CRM:")
    print("    [x] crm.objects.contacts.read")
    print("    [x] crm.objects.contacts.write")
    print("    [x] crm.objects.companies.read")
    print("    [x] crm.objects.companies.write")
    print("    [x] crm.objects.deals.read")
    print("    [x] crm.objects.deals.write")
    print("  Engagements:")
    print("    [x] crm.objects.emails.read/write")
    print("    [x] crm.objects.calls.read/write")
    print("    [x] crm.objects.notes.read/write")
    print("    [x] crm.objects.meetings.read/write")
    print()
    print("STEP 3: Get Your Token")
    print("-" * 40)
    print("  1. Click 'Create app'")
    print("  2. Copy the access token")
    print("  3. Token starts with 'pat-na1-...' or 'pat-eu1-...'")
    print()


def get_access_token():
    """Prompt user for access token."""
    print("Enter your HubSpot Private App access token:")
    print("(Paste and press Enter)")
    print()

    token = input("> ").strip()

    if not token:
        print("\n[ERROR] No token provided")
        return None

    if not token.startswith('pat-'):
        print("\n[WARNING] Token doesn't start with 'pat-'")
        print("HubSpot Private App tokens should start with 'pat-na1-' or 'pat-eu1-'")
        confirm = input("Continue anyway? (y/n): ").strip().lower()
        if confirm != 'y':
            return None

    return token


def test_token(token):
    """Test the token with a simple API call."""
    try:
        import requests
    except ImportError:
        print("\n[ERROR] requests library not installed")
        print("Run: pip install requests")
        return False

    print("\nTesting connection...")

    try:
        response = requests.get(
            f"{BASE_URL}/crm/v3/objects/contacts",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            },
            params={"limit": 1},
            timeout=10
        )

        if response.status_code == 200:
            print("[OK] Connection successful!")
            return True
        elif response.status_code == 401:
            print("[ERROR] Invalid token - authentication failed")
            return False
        elif response.status_code == 403:
            print("[WARNING] Token valid but missing some scopes")
            print("You may need to add more scopes in HubSpot Private App settings")
            return True  # Still save the token
        else:
            print(f"[ERROR] API returned status {response.status_code}")
            try:
                error = response.json()
                print(f"Message: {error.get('message', 'Unknown error')}")
            except:
                pass
            return False

    except requests.exceptions.Timeout:
        print("[ERROR] Connection timeout")
        return False
    except requests.exceptions.ConnectionError:
        print("[ERROR] Cannot connect to HubSpot API")
        return False
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        return False


def save_to_env(token):
    """Save token to .env file."""
    print("\nSaving to .env file...")

    # Read existing .env content
    existing_content = ""
    if ENV_FILE.exists():
        with open(ENV_FILE, 'r') as f:
            existing_content = f.read()

    # Check if HUBSPOT_ACCESS_TOKEN already exists
    lines = existing_content.split('\n')
    new_lines = []
    token_found = False

    for line in lines:
        if line.strip().startswith('HUBSPOT_ACCESS_TOKEN='):
            new_lines.append(f'HUBSPOT_ACCESS_TOKEN={token}')
            token_found = True
        else:
            new_lines.append(line)

    # Add token if not found
    if not token_found:
        # Add a newline before if file doesn't end with one
        if new_lines and new_lines[-1].strip():
            new_lines.append('')
        new_lines.append(f'HUBSPOT_ACCESS_TOKEN={token}')

    # Write back
    with open(ENV_FILE, 'w') as f:
        f.write('\n'.join(new_lines))

    print(f"[OK] Token saved to {ENV_FILE}")


def main():
    print_banner()
    print_instructions()

    # Get token
    token = get_access_token()
    if not token:
        print("\nSetup cancelled.")
        sys.exit(1)

    # Test token
    if not test_token(token):
        retry = input("\nSave token anyway? (y/n): ").strip().lower()
        if retry != 'y':
            print("\nSetup cancelled.")
            sys.exit(1)

    # Save token
    save_to_env(token)

    print("\n" + "=" * 60)
    print("  Setup Complete!")
    print("=" * 60)
    print("\nYou can now use HubSpot commands like:")
    print("  - 'list contacts'")
    print("  - 'search companies'")
    print("  - 'create deal'")
    print()


if __name__ == "__main__":
    main()
