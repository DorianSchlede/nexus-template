#!/usr/bin/env python3
"""
Notion Configuration Checker - Pre-flight validation for Notion API setup

Usage:
    python check_notion_config.py [--json]

Returns:
    Exit code 0 if all configured, 1 if partial config, 2 if not configured

With --json flag, outputs structured JSON for AI consumption including:
- status: "configured" | "partial" | "not_configured"
- missing: list of missing items
- fix_instructions: step-by-step fix instructions
- env_template: ready-to-use .env content template

The AI can use this JSON to intelligently guide the user through fixing issues.
"""

import sys
import os
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


def check_env_file():
    """Check if .env file exists and has required variables"""
    env_path = NEXUS_ROOT / '.env'

    result = {
        'exists': False,
        'path': str(env_path),
        'has_api_key': False,
        'has_db_id': False,
        'missing': [],
        'env_vars': {}
    }

    if not env_path.exists():
        result['missing'] = ['NOTION_API_KEY', 'NOTION_SKILLS_DB_ID']
        return False, "❌ .env file not found", result

    result['exists'] = True

    # Read .env file
    env_vars = {}
    try:
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip().strip('"\'')
    except Exception as e:
        return False, f"❌ Error reading .env: {e}", result

    result['env_vars'] = {k: v[:10] + '...' if len(v) > 10 else v for k, v in env_vars.items()}

    # Check for required variables
    missing = []
    if 'NOTION_API_KEY' not in env_vars or not env_vars['NOTION_API_KEY']:
        missing.append('NOTION_API_KEY')
    else:
        result['has_api_key'] = True

    if 'NOTION_SKILLS_DB_ID' not in env_vars or not env_vars['NOTION_SKILLS_DB_ID']:
        missing.append('NOTION_SKILLS_DB_ID')
    else:
        result['has_db_id'] = True

    result['missing'] = missing

    if missing:
        return False, f"❌ Missing in .env: {', '.join(missing)}", result

    # Return full env vars for API testing
    result['env_vars_full'] = env_vars
    return True, "✅ .env file configured", result


def check_user_config():
    """Check if user-config.yaml has notion_user_id"""
    user_config_path = NEXUS_ROOT / '01-memory' / 'user-config.yaml'

    result = {
        'exists': False,
        'path': str(user_config_path),
        'has_user_id': False,
        'user_name': None
    }

    if not user_config_path.exists():
        return False, "⚠️  user-config.yaml not found (optional for query/import)", result

    result['exists'] = True

    try:
        import yaml
    except ImportError:
        return False, "⚠️  PyYAML not installed (run: pip install pyyaml)", result

    try:
        with open(user_config_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Handle YAML frontmatter
        if content.startswith('---'):
            parts = content.split('---', 2)
            yaml_content = parts[1] if len(parts) >= 2 else content
        else:
            yaml_content = content

        config = yaml.safe_load(yaml_content)
    except Exception as e:
        return False, f"❌ Error reading user-config.yaml: {e}", result

    if not config:
        return False, "⚠️  user-config.yaml is empty", result

    # Check root-level notion_user_id first
    notion_user_id = config.get('notion_user_id')
    notion_user_name = config.get('notion_user_name', 'Unknown')

    # Fallback to integrations.notion.user_id
    if not notion_user_id:
        integrations = config.get('integrations', {})
        notion_config = integrations.get('notion', {})
        notion_user_id = notion_config.get('user_id')
        notion_user_name = notion_config.get('user_name', 'Unknown')

    if not notion_user_id:
        return False, "⚠️  notion_user_id not set in user-config.yaml (required for export)", result

    result['has_user_id'] = True
    result['user_name'] = notion_user_name
    return True, f"✅ User configured: {notion_user_name}", result


def test_notion_api(api_key):
    """Test Notion API connection"""
    result = {
        'connected': False,
        'user_name': None,
        'user_id': None,
        'error': None
    }

    try:
        import requests
    except ImportError:
        result['error'] = "requests library not installed"
        return False, "⚠️  requests library not installed (run: pip install requests)", result

    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Notion-Version": "2022-06-28"
        }

        response = requests.get(
            "https://api.notion.com/v1/users/me",
            headers=headers,
            timeout=10
        )

        if response.status_code == 200:
            user_data = response.json()
            user_name = user_data.get('name', 'Unknown')
            user_id = user_data.get('id')
            result['connected'] = True
            result['user_name'] = user_name
            result['user_id'] = user_id
            return True, f"✅ API connection successful ({user_name})", result
        elif response.status_code == 401:
            result['error'] = "Invalid API key (401 Unauthorized)"
            return False, "❌ API key is invalid (401 Unauthorized)", result
        else:
            result['error'] = f"API returned HTTP {response.status_code}"
            return False, f"❌ API test failed (HTTP {response.status_code})", result

    except requests.exceptions.Timeout:
        result['error'] = "Connection timeout"
        return False, "❌ API request timed out (check internet connection)", result
    except requests.exceptions.RequestException as e:
        result['error'] = str(e)
        return False, f"❌ API request failed: {e}", result
    except Exception as e:
        result['error'] = str(e)
        return False, f"❌ Unexpected error: {e}", result


def build_json_output(env_result, user_result, api_result, env_ok, user_ok, api_ok):
    """Build comprehensive JSON output for AI consumption"""

    # Determine overall status
    if env_ok and api_ok:
        status = "configured" if user_ok else "partial"
    else:
        status = "not_configured"

    # Build missing items list
    missing = []
    if not env_result.get('exists'):
        missing.append({'item': '.env file', 'required': True})
    else:
        for m in env_result.get('missing', []):
            missing.append({'item': m, 'required': True, 'location': '.env'})

    if not user_result.get('has_user_id'):
        missing.append({'item': 'notion_user_id', 'required': False, 'location': 'user-config.yaml', 'note': 'Only needed for export'})

    # Build fix instructions
    fix_instructions = []
    env_template_lines = []

    if 'NOTION_API_KEY' in env_result.get('missing', []) or not env_result.get('exists'):
        fix_instructions.append({
            'step': 1,
            'action': 'Get Notion API Key',
            'details': [
                'Option A: Ask your team admin for the shared NOTION_API_KEY',
                'Option B: Create your own at https://www.notion.so/my-integrations',
                '  - Click "New integration"',
                '  - Name it "Nexus"',
                '  - Copy the "Internal Integration Secret"'
            ]
        })
        env_template_lines.append('NOTION_API_KEY=secret_YOUR_API_KEY_HERE')

    if 'NOTION_SKILLS_DB_ID' in env_result.get('missing', []) or not env_result.get('exists'):
        fix_instructions.append({
            'step': 2,
            'action': 'Add Database ID (Beam Nexus Skills)',
            'details': [
                'Use the default Beam Nexus Skills database ID:',
                '2bc2cadf-bbbc-80be-af8a-d45dfc8dfa2e'
            ]
        })
        env_template_lines.append('NOTION_SKILLS_DB_ID=2bc2cadf-bbbc-80be-af8a-d45dfc8dfa2e')

    if not user_result.get('has_user_id') and not user_ok:
        fix_instructions.append({
            'step': 3,
            'action': 'Get your Notion User ID (optional, for export)',
            'details': [
                'Run the setup wizard which will auto-detect your user ID:',
                'python 00-system/skills/notion/notion-master/scripts/setup_notion.py'
            ]
        })

    output = {
        'status': status,
        'exit_code': 0 if status == 'configured' else (1 if status == 'partial' else 2),
        'checks': {
            'env_file': {
                'ok': env_ok,
                'path': env_result.get('path'),
                'exists': env_result.get('exists'),
                'has_api_key': env_result.get('has_api_key'),
                'has_db_id': env_result.get('has_db_id')
            },
            'user_config': {
                'ok': user_ok,
                'path': user_result.get('path'),
                'exists': user_result.get('exists'),
                'has_user_id': user_result.get('has_user_id'),
                'user_name': user_result.get('user_name')
            },
            'api_connection': {
                'ok': api_ok,
                'connected': api_result.get('connected') if api_result else False,
                'user_name': api_result.get('user_name') if api_result else None,
                'error': api_result.get('error') if api_result else None
            }
        },
        'missing': missing,
        'fix_instructions': fix_instructions if fix_instructions else None,
        'env_template': '\n'.join(env_template_lines) if env_template_lines else None,
        'setup_wizard': 'python 00-system/skills/notion/notion-master/scripts/setup_notion.py',
        'ai_action': get_ai_action(status, missing)
    }

    return output


def get_ai_action(status, missing):
    """Return recommended action for AI to take"""
    if status == 'configured':
        return 'proceed_with_operation'
    elif status == 'partial':
        return 'proceed_with_warning'  # Can query/import but not export
    else:
        # Check what's missing
        missing_items = [m['item'] for m in missing]
        if 'NOTION_API_KEY' in missing_items:
            return 'prompt_for_api_key'
        elif '.env file' in missing_items:
            return 'create_env_file'
        else:
            return 'run_setup_wizard'


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Check Notion configuration')
    parser.add_argument('--json', action='store_true', help='Output as JSON for AI consumption')
    args = parser.parse_args()

    # Configure UTF-8 output
    if sys.stdout.encoding != 'utf-8':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except AttributeError:
            pass

    # Run checks
    env_ok, env_msg, env_result = check_env_file()
    user_ok, user_msg, user_result = check_user_config()

    # Test API if we have the key
    api_ok = False
    api_result = None
    if env_ok and 'env_vars_full' in env_result:
        api_ok, api_msg, api_result = test_notion_api(env_result['env_vars_full'].get('NOTION_API_KEY', ''))

    # JSON output mode
    if args.json:
        output = build_json_output(env_result, user_result, api_result, env_ok, user_ok, api_ok)
        print(json.dumps(output, indent=2))
        sys.exit(output['exit_code'])

    # Human-readable output mode
    print("="*60)
    print("🔍 NOTION CONFIGURATION CHECK")
    print("="*60)
    print()

    all_ok = True

    # Check .env file
    print("[1/3] Checking .env file...")
    print(f"      {env_msg}")
    if not env_ok:
        all_ok = False
    print()

    # Check user-config.yaml
    print("[2/3] Checking user-config.yaml...")
    print(f"      {user_msg}")
    if not user_ok:
        print("      💡 This is optional for query/import, but required for export")
    print()

    # Test API if we have the key
    print("[3/3] Testing Notion API connection...")
    if env_ok:
        print(f"      {api_msg if api_result else '⏭️  Skipped (no API key)'}")
        if not api_ok:
            all_ok = False
    else:
        print("      ⏭️  Skipped (no API key found)")
        all_ok = False
    print()

    # Summary
    print("="*60)
    if all_ok and user_ok:
        print("✅ ALL CHECKS PASSED")
        print()
        print("You're ready to use Notion skills:")
        print("  • query-notion-db - Query skills database")
        print("  • import-skill-to-nexus - Import skills from Notion")
        print("  • export-skill-to-notion - Export skills to Notion")
        print("="*60)
        sys.exit(0)
    elif all_ok and not user_ok:
        print("⚠️  PARTIAL CONFIGURATION")
        print()
        print("You can use:")
        print("  ✅ query-notion-db - Query skills database")
        print("  ✅ import-skill-to-nexus - Import skills from Notion")
        print("  ❌ export-skill-to-notion - Requires notion_user_id")
        print()
        print("To enable export, add notion_user_id to 01-memory/user-config.yaml")
        print("="*60)
        sys.exit(1)
    else:
        print("❌ CONFIGURATION INCOMPLETE")
        print()
        print("To set up Notion integration:")
        print("  1. Run: python 00-system/skills/notion/notion-master/scripts/setup_notion.py")
        print("  2. Or manually add to .env:")
        print("     NOTION_API_KEY=your-api-key-here")
        print("     NOTION_SKILLS_DB_ID=2bc2cadf-bbbc-80be-af8a-d45dfc8dfa2e")
        print("="*60)
        sys.exit(2)


if __name__ == "__main__":
    main()
