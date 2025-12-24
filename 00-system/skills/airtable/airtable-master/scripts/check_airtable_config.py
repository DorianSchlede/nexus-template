#!/usr/bin/env python3
"""
Airtable Configuration Checker

Pre-flight validation for Airtable integration.
Run this before any Airtable operation.

Usage:
    python check_airtable_config.py [--verbose] [--json]

Exit codes:
    0 = All configured and working
    1 = Partial config (API works but missing optional fields or no bases)
    2 = Config incomplete or API test failed

With --json flag, outputs structured JSON for AI consumption including:
- status: "configured" | "partial" | "not_configured"
- missing: list of missing items
- fix_instructions: step-by-step fix instructions
- env_template: ready-to-use .env content template

The AI can use this JSON to intelligently guide the user through fixing issues.
"""

import os
import sys
import json
import argparse
from pathlib import Path


def find_nexus_root():
    """Find Nexus root directory by looking for CLAUDE.md"""
    current = Path(__file__).resolve().parent
    for path in [current] + list(current.parents):
        if (path / 'CLAUDE.md').exists():
            return path
    return Path.cwd()


NEXUS_ROOT = find_nexus_root()

try:
    import yaml
    import requests
except ImportError as e:
    # In JSON mode, output error as JSON
    if '--json' in sys.argv:
        print(json.dumps({
            'status': 'error',
            'error': f'Missing dependency: {e.name}',
            'fix': f'pip install {e.name}'
        }))
    else:
        print(f"❌ Missing dependency: {e.name}")
        print(f"   Run: pip install {e.name}")
    sys.exit(2)


def load_env():
    """Load environment variables from .env file."""
    env_path = NEXUS_ROOT / '.env'
    env_vars = {}

    if env_path.exists():
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
    config_path = NEXUS_ROOT / '01-memory' / 'user-config.yaml'

    if not config_path.exists():
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
    env_path = NEXUS_ROOT / '.env'

    result = {
        'exists': False,
        'path': str(env_path),
        'has_api_key': False,
        'api_key_format_ok': False,
        'missing': []
    }

    if not env_path.exists():
        result['missing'] = ['AIRTABLE_API_KEY']
        return False, "❌ .env file not found", result

    result['exists'] = True
    env_vars = load_env()

    # Required variable
    api_key = env_vars.get('AIRTABLE_API_KEY', '')

    if not api_key:
        result['missing'] = ['AIRTABLE_API_KEY']
        return False, "❌ AIRTABLE_API_KEY not set in .env", result

    result['has_api_key'] = True

    # Validate format (PAT should start with pat.)
    if api_key.startswith('pat.'):
        result['api_key_format_ok'] = True
    else:
        result['api_key_format_warning'] = "API key doesn't start with 'pat.' (old key format?)"

    return True, "✅ .env file configured", result


def check_user_config(verbose=False):
    """Check user-config.yaml for Airtable settings."""
    config_path = NEXUS_ROOT / '01-memory' / 'user-config.yaml'

    result = {
        'exists': False,
        'path': str(config_path),
        'has_user_id': False,
        'has_default_base': False,
        'user_email': None,
        'default_base': None
    }

    config = load_user_config()

    if config is None:
        return 'partial', "⚠️  user-config.yaml not found or invalid", result

    result['exists'] = True

    # Check for Airtable settings
    user_id = config.get('airtable_user_id')
    user_email = config.get('airtable_user_email')
    default_base = config.get('airtable_default_base')

    if user_id:
        result['has_user_id'] = True
    if user_email:
        result['user_email'] = user_email
    if default_base:
        result['has_default_base'] = True
        result['default_base'] = default_base

    if user_id or default_base:
        msg = f"✅ User config present"
        if default_base:
            msg += f" (default base: {default_base[:15]}...)"
        return True, msg, result
    else:
        return 'partial', "ℹ️  No Airtable settings in user-config.yaml (optional)", result


def check_api_connection(verbose=False):
    """Test Airtable API connection."""
    api_key = os.environ.get('AIRTABLE_API_KEY')

    result = {
        'connected': False,
        'user_id': None,
        'user_email': None,
        'scopes': [],
        'error': None
    }

    if not api_key:
        result['error'] = "No API key available"
        return False, "❌ No API key available", result

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
            result['connected'] = True
            result['user_id'] = data.get('id')
            result['user_email'] = data.get('email', 'unknown')
            result['scopes'] = data.get('scopes', [])
            return True, f"✅ API connection successful ({result['user_email']})", result
        elif response.status_code == 401:
            result['error'] = "Invalid API key (401 Unauthorized)"
            return False, "❌ API key invalid (401 Unauthorized)", result
        elif response.status_code == 403:
            result['error'] = "Insufficient permissions (403 Forbidden)"
            return False, "❌ API key lacks permissions (403 Forbidden)", result
        else:
            result['error'] = f"API returned status {response.status_code}"
            return False, f"❌ API returned status {response.status_code}", result

    except requests.exceptions.Timeout:
        result['error'] = "Connection timeout"
        return False, "❌ API connection timed out", result
    except requests.exceptions.RequestException as e:
        result['error'] = str(e)
        return False, f"❌ API connection failed: {e}", result


def check_base_access(verbose=False):
    """Check if we can access at least one base."""
    api_key = os.environ.get('AIRTABLE_API_KEY')

    result = {
        'has_bases': False,
        'base_count': 0,
        'bases': [],
        'error': None
    }

    if not api_key:
        result['error'] = "No API key"
        return False, "❌ No API key", result

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
            result['base_count'] = len(bases)
            result['bases'] = [{'id': b.get('id'), 'name': b.get('name')} for b in bases[:10]]

            if bases:
                result['has_bases'] = True
                return True, f"✅ Base access confirmed ({len(bases)} base(s))", result
            else:
                return 'partial', "⚠️  No bases accessible", result
        else:
            result['error'] = f"Could not list bases: {response.status_code}"
            return False, f"❌ Could not list bases: {response.status_code}", result

    except requests.exceptions.RequestException as e:
        result['error'] = str(e)
        return False, f"❌ Base check failed: {e}", result


def build_json_output(env_result, user_result, api_result, base_result, env_ok, user_ok, api_ok, base_ok):
    """Build comprehensive JSON output for AI consumption"""

    # Determine overall status
    if env_ok and api_ok and base_ok:
        status = "configured"
    elif env_ok and api_ok:
        status = "partial"  # API works but no bases
    else:
        status = "not_configured"

    # Build missing items list
    missing = []
    if not env_result.get('exists'):
        missing.append({'item': '.env file', 'required': True})
    elif not env_result.get('has_api_key'):
        missing.append({'item': 'AIRTABLE_API_KEY', 'required': True, 'location': '.env'})

    if base_ok != True and base_result:
        missing.append({
            'item': 'Base access',
            'required': False,
            'note': 'Add bases to your PAT at https://airtable.com/create/tokens'
        })

    # Build fix instructions
    fix_instructions = []
    env_template_lines = []

    if not env_result.get('has_api_key') or not env_result.get('exists'):
        fix_instructions.append({
            'step': 1,
            'action': 'Create Personal Access Token (PAT)',
            'details': [
                'Go to: https://airtable.com/create/tokens',
                'Click "Create new token"',
                'Name it "Nexus Integration"',
                'Add scopes: data.records:read, data.records:write, schema.bases:read',
                'Select bases to grant access to',
                'Click "Create token"',
                'Copy the token (starts with "pat.")'
            ]
        })
        env_template_lines.append('AIRTABLE_API_KEY=pat.YOUR_TOKEN_HERE')

    if base_ok == 'partial':
        fix_instructions.append({
            'step': 2,
            'action': 'Grant base access to PAT',
            'details': [
                'Go to: https://airtable.com/create/tokens',
                'Click on your token',
                'Under "Access", click "Add a base"',
                'Select the bases you want to access',
                'Click "Save"'
            ]
        })

    # Determine exit code
    if status == 'configured':
        exit_code = 0
    elif status == 'partial':
        exit_code = 1
    else:
        exit_code = 2

    output = {
        'status': status,
        'exit_code': exit_code,
        'checks': {
            'env_file': {
                'ok': env_ok,
                'path': env_result.get('path'),
                'exists': env_result.get('exists'),
                'has_api_key': env_result.get('has_api_key'),
                'api_key_format_ok': env_result.get('api_key_format_ok'),
                'format_warning': env_result.get('api_key_format_warning')
            },
            'user_config': {
                'ok': user_ok == True,
                'path': user_result.get('path'),
                'exists': user_result.get('exists'),
                'has_user_id': user_result.get('has_user_id'),
                'user_email': user_result.get('user_email'),
                'default_base': user_result.get('default_base')
            },
            'api_connection': {
                'ok': api_ok,
                'connected': api_result.get('connected') if api_result else False,
                'user_email': api_result.get('user_email') if api_result else None,
                'scopes': api_result.get('scopes', []) if api_result else [],
                'error': api_result.get('error') if api_result else None
            },
            'base_access': {
                'ok': base_ok == True,
                'has_bases': base_result.get('has_bases') if base_result else False,
                'base_count': base_result.get('base_count', 0) if base_result else 0,
                'bases': base_result.get('bases', []) if base_result else []
            }
        },
        'missing': missing,
        'fix_instructions': fix_instructions if fix_instructions else None,
        'env_template': '\n'.join(env_template_lines) if env_template_lines else None,
        'setup_wizard': 'python 00-system/skills/airtable/airtable-master/scripts/setup_airtable.py',
        'ai_action': get_ai_action(status, missing)
    }

    return output


def get_ai_action(status, missing):
    """Return recommended action for AI to take"""
    if status == 'configured':
        return 'proceed_with_operation'
    elif status == 'partial':
        return 'proceed_with_warning'  # API works but limited
    else:
        # Check what's missing
        missing_items = [m['item'] for m in missing]
        if 'AIRTABLE_API_KEY' in missing_items or '.env file' in missing_items:
            return 'prompt_for_api_key'
        else:
            return 'run_setup_wizard'


def main():
    parser = argparse.ArgumentParser(description='Check Airtable configuration')
    parser.add_argument('--verbose', '-v', action='store_true', help='Show detailed output')
    parser.add_argument('--json', action='store_true', help='Output as JSON for AI consumption')
    args = parser.parse_args()

    # Configure UTF-8 output
    if sys.stdout.encoding != 'utf-8':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except AttributeError:
            pass

    # Run checks
    env_ok, env_msg, env_result = check_env_file(args.verbose)
    user_ok, user_msg, user_result = check_user_config(args.verbose)

    # Test API if we have the key
    api_ok = False
    api_result = None
    base_ok = False
    base_result = None

    if env_ok:
        api_ok, api_msg, api_result = check_api_connection(args.verbose)
        if api_ok:
            base_ok, base_msg, base_result = check_base_access(args.verbose)

    # JSON output mode
    if args.json:
        output = build_json_output(
            env_result, user_result, api_result, base_result,
            env_ok, user_ok, api_ok, base_ok
        )
        print(json.dumps(output, indent=2))
        sys.exit(output['exit_code'])

    # Human-readable output mode
    print()
    print("[1/4] Checking .env file...")
    print(f"      {env_msg}")
    if env_result.get('api_key_format_warning'):
        print(f"      ⚠️  {env_result['api_key_format_warning']}")

    print("[2/4] Checking user-config.yaml...")
    print(f"      {user_msg}")

    print("[3/4] Testing Airtable API connection...")
    if env_ok:
        print(f"      {api_msg}")
        if api_ok and args.verbose and api_result:
            scopes = api_result.get('scopes', [])
            if scopes:
                print(f"         Scopes: {', '.join(scopes[:5])}{'...' if len(scopes) > 5 else ''}")
    else:
        print("      ⏭️  Skipped (no API key)")

    print("[4/4] Checking base access...")
    if api_ok:
        print(f"      {base_msg}")
        if base_ok and args.verbose and base_result:
            for base in base_result.get('bases', [])[:3]:
                print(f"         - {base.get('name', 'Unnamed')}")
            if base_result.get('base_count', 0) > 3:
                print(f"         ... and {base_result['base_count'] - 3} more")
    else:
        print("      ⏭️  Skipped (no API connection)")

    print()

    # Determine exit code and summary
    if env_ok and api_ok and base_ok == True:
        print("✅ Airtable configuration complete!")
        print()
        print("You're ready to use Airtable skills.")
        sys.exit(0)
    elif env_ok and api_ok:
        print("⚠️  Airtable partially configured")
        print()
        print("API connection works, but no bases accessible.")
        print("Add bases to your PAT at: https://airtable.com/create/tokens")
        sys.exit(1)
    else:
        print("❌ Airtable configuration incomplete")
        print()
        print("To fix:")
        if not env_ok:
            print("  1. Create .env with: AIRTABLE_API_KEY=pat.xxxxx...")
            print("     Get token from: https://airtable.com/create/tokens")
        else:
            print("  1. Verify API key is valid")
        print()
        print("Or run the setup wizard:")
        print("  python 00-system/skills/notion/airtable-master/scripts/setup_airtable.py")
        sys.exit(2)


if __name__ == '__main__':
    main()
