#!/usr/bin/env python3
"""
Airtable Configuration Checker

Pre-flight validation for Airtable integration.
Run this before any Airtable operation.

Usage:
    python check_airtable_config.py [--verbose]

Exit codes:
    0 = All configured and working
    1 = Partial config (API works but missing optional fields)
    2 = Config incomplete or API test failed
"""

import os
import sys
import argparse

# Find Nexus root (walk up until we find CLAUDE.md)
def find_nexus_root():
    current = os.path.dirname(os.path.abspath(__file__))
    while current != os.path.dirname(current):
        if os.path.exists(os.path.join(current, 'CLAUDE.md')):
            return current
        current = os.path.dirname(current)
    return None

NEXUS_ROOT = find_nexus_root()
if not NEXUS_ROOT:
    print("❌ Error: Could not find Nexus root (no CLAUDE.md found)")
    sys.exit(2)

sys.path.insert(0, NEXUS_ROOT)

try:
    import yaml
    import requests
except ImportError as e:
    print(f"❌ Missing dependency: {e.name}")
    print(f"   Run: pip install {e.name}")
    sys.exit(2)


def load_env():
    """Load environment variables from .env file."""
    env_path = os.path.join(NEXUS_ROOT, '.env')
    env_vars = {}

    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip().strip('"\'')
                    os.environ[key.strip()] = value.strip().strip('"\'')

    return env_vars


def load_user_config():
    """Load user configuration from user-config.yaml."""
    config_path = os.path.join(NEXUS_ROOT, '01-memory', 'user-config.yaml')

    if not os.path.exists(config_path):
        return None

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Handle YAML frontmatter
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 2:
                    content = parts[1]
            return yaml.safe_load(content)
    except yaml.YAMLError:
        return None


def check_env_file(verbose=False):
    """Check .env file for required variables."""
    env_path = os.path.join(NEXUS_ROOT, '.env')

    if not os.path.exists(env_path):
        print("      ❌ .env file not found")
        print(f"         Create at: {env_path}")
        return False

    env_vars = load_env()

    # Required variable
    api_key = env_vars.get('AIRTABLE_API_KEY', '')

    if not api_key:
        print("      ❌ AIRTABLE_API_KEY not set in .env")
        return False

    # Validate format (PAT should start with pat.)
    if not api_key.startswith('pat.'):
        print("      ⚠️  API key doesn't start with 'pat.'")
        print("         Note: API keys (deprecated) start with 'key'")
        print("         Personal Access Tokens start with 'pat.'")
        if verbose:
            print(f"         Current prefix: {api_key[:6]}...")

    print("      ✅ .env file configured")
    return True


def check_user_config(verbose=False):
    """Check user-config.yaml for Airtable settings."""
    config = load_user_config()

    if config is None:
        print("      ⚠️  user-config.yaml not found or invalid")
        print("         (Optional: used for default base)")
        return 'partial'

    # Check for Airtable settings
    user_id = config.get('airtable_user_id')
    default_base = config.get('airtable_default_base')

    if user_id or default_base:
        if default_base:
            print(f"      ✅ Default base configured: {default_base[:15]}...")
        else:
            print(f"      ✅ User config present (no default base)")
        return True
    else:
        print("      ℹ️  No Airtable settings in user-config.yaml")
        print("         (Optional: airtable_default_base)")
        return 'partial'


def check_api_connection(verbose=False):
    """Test Airtable API connection."""
    api_key = os.environ.get('AIRTABLE_API_KEY')

    if not api_key:
        print("      ❌ No API key available")
        return False

    try:
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }

        # Test with whoami endpoint
        response = requests.get(
            'https://api.airtable.com/v0/meta/whoami',
            headers=headers,
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            email = data.get('email', 'unknown')
            scopes = data.get('scopes', [])
            print(f"      ✅ API connection successful")
            print(f"         User: {email}")
            if verbose:
                print(f"         Scopes: {', '.join(scopes[:5])}{'...' if len(scopes) > 5 else ''}")
            return True
        elif response.status_code == 401:
            print("      ❌ API key invalid (401 Unauthorized)")
            print("         Check AIRTABLE_API_KEY in .env")
            return False
        elif response.status_code == 403:
            print("      ❌ API key lacks permissions (403 Forbidden)")
            return False
        else:
            print(f"      ❌ API returned status {response.status_code}")
            if verbose:
                print(f"         Response: {response.text[:200]}")
            return False

    except requests.exceptions.Timeout:
        print("      ❌ API connection timed out")
        print("         Check internet connection")
        return False
    except requests.exceptions.RequestException as e:
        print(f"      ❌ API connection failed: {e}")
        return False


def check_base_access(verbose=False):
    """Check if we can access at least one base."""
    api_key = os.environ.get('AIRTABLE_API_KEY')

    if not api_key:
        return False

    try:
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }

        response = requests.get(
            'https://api.airtable.com/v0/meta/bases',
            headers=headers,
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            bases = data.get('bases', [])
            if bases:
                print(f"      ✅ Base access confirmed ({len(bases)} base(s))")
                if verbose:
                    for base in bases[:3]:
                        print(f"         - {base.get('name', 'Unnamed')}")
                    if len(bases) > 3:
                        print(f"         ... and {len(bases) - 3} more")
                return True
            else:
                print("      ⚠️  No bases accessible")
                print("         Add bases to your PAT at:")
                print("         https://airtable.com/create/tokens")
                return 'partial'
        else:
            print(f"      ❌ Could not list bases: {response.status_code}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"      ❌ Base check failed: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description='Check Airtable configuration')
    parser.add_argument('--verbose', '-v', action='store_true', help='Show detailed output')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()

    results = {
        'env_file': False,
        'user_config': False,
        'api_connection': False,
        'base_access': False
    }

    print()
    print("[1/4] Checking .env file...")
    results['env_file'] = check_env_file(args.verbose)

    print("[2/4] Checking user-config.yaml...")
    user_result = check_user_config(args.verbose)
    results['user_config'] = user_result == True

    print("[3/4] Testing Airtable API connection...")
    if results['env_file']:
        results['api_connection'] = check_api_connection(args.verbose)
    else:
        print("      ⏭️  Skipped (no API key)")

    print("[4/4] Checking base access...")
    if results['api_connection']:
        base_result = check_base_access(args.verbose)
        results['base_access'] = base_result == True
    else:
        print("      ⏭️  Skipped (no API connection)")

    print()

    # Determine exit code
    if results['env_file'] and results['api_connection']:
        if results['base_access']:
            print("✅ Airtable configuration complete!")
            exit_code = 0
        else:
            print("✅ Airtable API connected (no bases accessible)")
            print("   Add bases to your PAT to use full functionality")
            exit_code = 1
    else:
        print("❌ Airtable configuration incomplete")
        print()
        print("To fix:")
        if not results['env_file']:
            print("  1. Create .env with: AIRTABLE_API_KEY=pat.xxxxx...")
            print("     Get token from: https://airtable.com/create/tokens")
        if not results['api_connection']:
            print("  2. Verify API key is valid")
        print()
        print("See: 00-system/skills/notion/airtable-master/references/setup-guide.md")
        exit_code = 2

    if args.json:
        import json
        print(json.dumps(results, indent=2))

    sys.exit(exit_code)


if __name__ == '__main__':
    main()
