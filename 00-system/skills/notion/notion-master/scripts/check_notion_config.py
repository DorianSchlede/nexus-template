#!/usr/bin/env python3
"""
Notion Configuration Checker - Pre-flight validation for Notion API setup

Usage:
    python check_notion_config.py

Returns:
    Exit code 0 if all configured, 1 if missing config, 2 if API test failed
"""

import sys
import os
from pathlib import Path


def check_env_file():
    """Check if .env file exists and has required variables"""
    env_path = Path.cwd() / '.env'

    if not env_path.exists():
        return False, "❌ .env file not found", []

    # Read .env file
    env_vars = {}
    try:
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip()
    except Exception as e:
        return False, f"❌ Error reading .env: {e}", []

    # Check for required variables
    missing = []
    if 'NOTION_API_KEY' not in env_vars or not env_vars['NOTION_API_KEY']:
        missing.append('NOTION_API_KEY')
    if 'NOTION_SKILLS_DB_ID' not in env_vars or not env_vars['NOTION_SKILLS_DB_ID']:
        missing.append('NOTION_SKILLS_DB_ID')

    if missing:
        return False, f"❌ Missing in .env: {', '.join(missing)}", []

    return True, "✅ .env file configured", env_vars


def check_user_config():
    """Check if user-config.yaml has notion_user_id"""
    user_config_path = Path.cwd() / '01-memory' / 'user-config.yaml'

    if not user_config_path.exists():
        return False, "⚠️  user-config.yaml not found (optional for query/import)", []

    try:
        import yaml
    except ImportError:
        return False, "⚠️  PyYAML not installed (run: pip install pyyaml)", []

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
        return False, f"❌ Error reading user-config.yaml: {e}", []

    if not config:
        return False, "⚠️  user-config.yaml is empty", []

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
        return False, "⚠️  notion_user_id not set in user-config.yaml (required for export)", []

    return True, f"✅ User configured: {notion_user_name}", config


def test_notion_api(api_key):
    """Test Notion API connection"""
    try:
        import requests
    except ImportError:
        return False, "⚠️  requests library not installed (run: pip install requests)", None

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
            return True, f"✅ API connection successful ({user_name})", user_data
        elif response.status_code == 401:
            return False, "❌ API key is invalid (401 Unauthorized)", None
        else:
            return False, f"❌ API test failed (HTTP {response.status_code})", None

    except requests.exceptions.Timeout:
        return False, "❌ API request timed out (check internet connection)", None
    except requests.exceptions.RequestException as e:
        return False, f"❌ API request failed: {e}", None
    except Exception as e:
        return False, f"❌ Unexpected error: {e}", None


def main():
    """Main entry point"""
    # Configure UTF-8 output
    if sys.stdout.encoding != 'utf-8':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except AttributeError:
            pass

    print("="*60)
    print("🔍 NOTION CONFIGURATION CHECK")
    print("="*60)
    print()

    all_ok = True
    env_vars = {}

    # Check .env file
    print("[1/3] Checking .env file...")
    env_ok, env_msg, env_data = check_env_file()
    print(f"      {env_msg}")
    if env_ok:
        env_vars = env_data
    else:
        all_ok = False
    print()

    # Check user-config.yaml
    print("[2/3] Checking user-config.yaml...")
    user_ok, user_msg, user_data = check_user_config()
    print(f"      {user_msg}")
    if not user_ok:
        print("      💡 This is optional for query/import, but required for export")
    print()

    # Test API if we have the key
    print("[3/3] Testing Notion API connection...")
    if env_ok and 'NOTION_API_KEY' in env_vars:
        api_ok, api_msg, api_data = test_notion_api(env_vars['NOTION_API_KEY'])
        print(f"      {api_msg}")
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
        print("  1. Run: python 00-system/skills/notion-master/scripts/setup_notion.py")
        print("  2. Or manually add to .env:")
        print("     NOTION_API_KEY=your-api-key-here")
        print("     NOTION_SKILLS_DB_ID=2bc2cadf-bbbc-80be-af8a-d45dfc8dfa2e")
        print("="*60)
        sys.exit(2)


if __name__ == "__main__":
    main()
