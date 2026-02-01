#!/usr/bin/env python3
"""
Airtable Setup Wizard - Interactive setup for Airtable integration

Usage:
    python setup_airtable.py [--non-interactive]

Guides through:
1. Creating/entering Personal Access Token (PAT)
2. Testing API connection
3. Saving to .env
4. Discovering accessible bases
5. Saving context to 01-memory/integrations/
"""

import sys
import os
import argparse
from pathlib import Path

try:
    import requests
    import yaml
except ImportError as e:
    print(f"[ERROR] Missing dependency: {e.name}")
    print(f"Install with: pip install {e.name}")
    sys.exit(1)


def find_nexus_root():
    """Find Nexus root directory by looking for CLAUDE.md"""
    current = Path(__file__).resolve().parent
    for path in [current] + list(current.parents):
        if (path / 'CLAUDE.md').exists():
            return path
    return Path.cwd()


def print_header():
    """Print wizard header"""
    print()
    print("=" * 60)
    print("[*] AIRTABLE INTEGRATION SETUP WIZARD")
    print("=" * 60)
    print()


def get_api_key_interactive():
    """Guide user to get Personal Access Token interactively"""
    print("Step 1: Create Personal Access Token (PAT)")
    print("-" * 60)
    print()
    print("To create a PAT:")
    print()
    print("  1. Go to: https://airtable.com/create/tokens")
    print("  2. Click 'Create new token'")
    print("  3. Name it 'Nexus Integration'")
    print("  4. Add scopes:")
    print("     - data.records:read (required)")
    print("     - data.records:write (for creating/updating)")
    print("     - schema.bases:read (for schema discovery)")
    print("  5. Select which bases to grant access to")
    print("  6. Click 'Create token'")
    print("  7. Copy the token (starts with 'pat.')")
    print()

    while True:
        api_key = input("Enter your AIRTABLE_API_KEY (starts with 'pat.'): ").strip()

        if not api_key:
            print("[ERROR] API key cannot be empty")
            continue

        if not api_key.startswith('pat.'):
            print("[WARN] PAT should start with 'pat.'")
            print("       Old API keys (starting with 'key') are deprecated.")
            confirm = input("Continue anyway? (yes/no): ").strip().lower()
            if confirm != 'yes':
                continue

        return api_key


def test_api_connection(api_key):
    """Test Airtable API connection and return user info"""
    print()
    print("Step 2: Testing Connection")
    print("-" * 60)
    print()

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # Test 1: Get user info (whoami)
    print("[TEST 1/2] Testing API key...", end=" ", flush=True)
    try:
        response = requests.get(
            "https://api.airtable.com/v0/meta/whoami",
            headers=headers,
            timeout=10
        )

        if response.status_code == 200:
            user_data = response.json()
            email = user_data.get('email', 'Unknown')
            user_id = user_data.get('id', '')
            scopes = user_data.get('scopes', [])
            print(f"[OK] OK")
            print(f"         User: {email}")
            print(f"         Scopes: {len(scopes)} granted")
        elif response.status_code == 401:
            print("[ERROR] FAILED (Invalid API key)")
            return None, None, None
        elif response.status_code == 403:
            print("[ERROR] FAILED (Insufficient permissions)")
            return None, None, None
        else:
            print(f"[ERROR] FAILED ({response.status_code})")
            return None, None, None

    except requests.exceptions.Timeout:
        print("[ERROR] FAILED (Connection timeout)")
        return None, None, None
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] FAILED ({e})")
        return None, None, None

    # Test 2: List bases
    print("[TEST 2/2] Checking base access...", end=" ", flush=True)
    try:
        response = requests.get(
            "https://api.airtable.com/v0/meta/bases",
            headers=headers,
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            bases = data.get('bases', [])
            if bases:
                print(f"[OK] OK ({len(bases)} base(s) accessible)")
                for base in bases[:3]:
                    print(f"         - {base.get('name', 'Unnamed')}")
                if len(bases) > 3:
                    print(f"         ... and {len(bases) - 3} more")
            else:
                print("[!]  No bases accessible")
                print("         Add bases to your PAT at: https://airtable.com/create/tokens")
        else:
            print(f"[!]  Could not list bases ({response.status_code})")

    except requests.exceptions.RequestException as e:
        print(f"[!]  Base check failed ({e})")

    print()
    return user_id, email, scopes


def save_to_env(root, api_key):
    """Save API key to .env file"""
    print("Step 3: Saving to .env")
    print("-" * 60)
    print()

    env_path = root / '.env'

    # Read existing .env if it exists
    existing_lines = []
    if env_path.exists():
        with open(env_path, 'r', encoding='utf-8') as f:
            existing_lines = f.readlines()

    # Update or add key
    updated = []
    api_key_set = False

    for line in existing_lines:
        if line.strip().startswith('AIRTABLE_API_KEY='):
            updated.append(f'AIRTABLE_API_KEY={api_key}\n')
            api_key_set = True
        else:
            updated.append(line)

    # Add if not present
    if not api_key_set:
        # Add with a header if file doesn't have one
        if not existing_lines or not any('Airtable' in line for line in existing_lines):
            updated.append('\n# Airtable Integration\n')
        updated.append(f'AIRTABLE_API_KEY={api_key}\n')

    # Write updated .env
    with open(env_path, 'w', encoding='utf-8') as f:
        f.writelines(updated)

    print(f"[OK] Saved to: {env_path}")
    print()


def save_to_user_config(root, user_id, email):
    """Save user info to user-config.yaml (optional)"""
    print("Step 4: Saving to user-config.yaml")
    print("-" * 60)
    print()

    config_path = root / '01-memory' / 'user-config.yaml'

    if not config_path.exists():
        print(f"[!]  user-config.yaml not found at {config_path}")
        print("    Skipping user config update (optional)")
        print()
        return

    # Read existing config
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Handle YAML frontmatter
        if content.startswith('---'):
            parts = content.split('---', 2)
            yaml_content = parts[1] if len(parts) >= 2 else content
            footer = parts[2] if len(parts) >= 3 else ""
        else:
            yaml_content = content
            footer = ""

        config = yaml.safe_load(yaml_content) or {}

    except yaml.YAMLError as e:
        print(f"[ERROR] Could not parse user-config.yaml: {e}")
        return

    # Add Airtable user info at root level for quick access
    if user_id:
        config['airtable_user_id'] = user_id
    if email:
        config['airtable_user_email'] = email

    # Also save to integrations.airtable for structured access
    if 'integrations' not in config:
        config['integrations'] = {}

    config['integrations']['airtable'] = {
        'user_id': user_id,
        'user_email': email,
        'setup_complete': True
    }

    # Write updated config
    updated_yaml = yaml.dump(config, default_flow_style=False, sort_keys=False, allow_unicode=True)

    with open(config_path, 'w', encoding='utf-8') as f:
        f.write('---\n')
        f.write(updated_yaml)
        f.write('---\n')
        if footer:
            f.write(footer)

    print(f"[OK] Saved to: {config_path}")
    print()


def discover_bases(root, api_key):
    """Discover all accessible bases and save context"""
    print("Step 5: Discovering Bases")
    print("-" * 60)
    print()
    print("Running initial base discovery...", flush=True)

    # Check if discover_bases.py exists
    discover_script = root / '00-system' / 'skills' / 'airtable' / 'airtable-master' / 'scripts' / 'discover_bases.py'

    if discover_script.exists():
        import subprocess
        try:
            result = subprocess.run(
                [sys.executable, str(discover_script)],
                cwd=str(root),
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                print("[OK] Base discovery complete")
                # Print relevant lines from output
                for line in result.stdout.split('\n'):
                    if line.strip() and ('base' in line.lower() or 'saved' in line.lower() or 'found' in line.lower()):
                        print(f"   {line.strip()}")
            else:
                print("[!]  Discovery had issues (non-critical)")
                if result.stderr:
                    print(f"   {result.stderr[:200]}")
        except subprocess.TimeoutExpired:
            print("[!]  Discovery timed out (non-critical)")
        except Exception as e:
            print(f"[!]  Discovery failed: {e} (non-critical)")
    else:
        # Fallback: do inline discovery
        print("   (discover_bases.py not found, using inline discovery)")
        try:
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            response = requests.get(
                "https://api.airtable.com/v0/meta/bases",
                headers=headers,
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                bases = data.get('bases', [])

                # Save to context file
                integrations_dir = root / '01-memory' / 'integrations'
                integrations_dir.mkdir(exist_ok=True)

                context = {
                    'last_synced': str(Path(__file__).stat().st_mtime),
                    'bases': [
                        {
                            'id': b.get('id'),
                            'name': b.get('name'),
                            'permission_level': b.get('permissionLevel', 'unknown')
                        }
                        for b in bases
                    ]
                }

                context_path = integrations_dir / 'airtable-bases.yaml'
                with open(context_path, 'w', encoding='utf-8') as f:
                    yaml.dump(context, f, default_flow_style=False, allow_unicode=True)

                print(f"[OK] Found {len(bases)} base(s)")
                print(f"   Saved to: {context_path}")
        except Exception as e:
            print(f"[!]  Inline discovery failed: {e}")

    print()


def main():
    """Main wizard flow"""
    parser = argparse.ArgumentParser(description='Airtable Setup Wizard')
    parser.add_argument('--non-interactive', action='store_true',
                        help='Skip interactive prompts (requires AIRTABLE_API_KEY env var)')
    parser.add_argument('--api-key', type=str, help='API key (for non-interactive mode)')
    args = parser.parse_args()

    # Configure UTF-8 output for Windows
    if sys.stdout.encoding != 'utf-8':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except AttributeError:
            pass

    print_header()

    # Find Nexus root
    root = find_nexus_root()
    print(f"Nexus root: {root}")
    print()

    # Get API key
    if args.non_interactive:
        api_key = args.api_key or os.environ.get('AIRTABLE_API_KEY')
        if not api_key:
            print("[ERROR] --non-interactive requires --api-key or AIRTABLE_API_KEY env var")
            sys.exit(1)
        print(f"Using provided API key: {api_key[:10]}...")
    else:
        api_key = get_api_key_interactive()

    # Test connection
    user_id, email, scopes = test_api_connection(api_key)

    if not user_id:
        print()
        print("=" * 60)
        print("[ERROR] SETUP FAILED")
        print("=" * 60)
        print()
        print("Please check your API key and try again.")
        print("Get a new PAT at: https://airtable.com/create/tokens")
        sys.exit(1)

    # Save to .env
    save_to_env(root, api_key)

    # Save to user-config.yaml
    save_to_user_config(root, user_id, email)

    # Discover bases
    discover_bases(root, api_key)

    # Success summary
    print("=" * 60)
    print("[OK] SETUP COMPLETE!")
    print("=" * 60)
    print()
    print("Configuration saved:")
    print(f"  * .env -> AIRTABLE_API_KEY")
    if email:
        print(f"  * user-config.yaml -> airtable_user_id ({email})")
    print(f"  * 01-memory/integrations/airtable-bases.yaml -> Base context")
    print()
    print("You can now use Airtable skills:")
    print("  * airtable-query - Query records")
    print("  * airtable-connect - Connect to bases")
    print("  * airtable-sync - Sync records")
    print()
    print("Try it now:")
    print('  Say "query my Airtable" or "list Airtable bases"')
    print()

    sys.exit(0)


if __name__ == "__main__":
    main()
