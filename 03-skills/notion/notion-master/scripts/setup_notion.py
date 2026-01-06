#!/usr/bin/env python3
"""
Notion Setup Wizard - Interactive setup for Notion integration

Usage:
    python setup_notion.py

Guides through:
1. Getting/entering API key
2. Entering database ID
3. Testing connection
4. Saving to .env
5. Getting user ID
6. Saving to user-config.yaml
"""

import sys
import os
from pathlib import Path

try:
    import requests
    import yaml
except ImportError:
    print("[ERROR] Missing dependencies")
    print("Install with: pip install requests pyyaml")
    sys.exit(1)


def find_nexus_root():
    """Find Nexus root directory"""
    current = Path.cwd()
    for path in [current] + list(current.parents):
        if (path / 'CLAUDE.md').exists():
            return path
    return current


def print_header():
    """Print wizard header"""
    print("=" * 60)
    print("🔧 NOTION INTEGRATION SETUP WIZARD")
    print("=" * 60)
    print()


def get_api_key():
    """Guide user to get API key"""
    print("Step 1: Get Notion API Key")
    print("-" * 60)
    print()
    print("Choose one option:")
    print()
    print("  Option A: Use shared team API key (recommended)")
    print("    → Ask your team admin for the NOTION_API_KEY")
    print("    → This is the simplest setup")
    print()
    print("  Option B: Create your own integration")
    print("    → Go to: https://www.notion.so/my-integrations")
    print("    → Click 'New integration'")
    print("    → Name: 'Nexus' (or your preferred name)")
    print("    → Copy the 'Internal Integration Secret'")
    print("    → Note: Only workspace admins can create integrations")
    print()

    while True:
        api_key = input("Enter your NOTION_API_KEY (starts with 'secret_'): ").strip()

        if not api_key:
            print("[ERROR] API key cannot be empty")
            continue

        if not api_key.startswith('secret_'):
            print("[WARN] API key should start with 'secret_'")
            confirm = input("Continue anyway? (yes/no): ").strip().lower()
            if confirm != 'yes':
                continue

        return api_key


def get_database_id():
    """Get database ID"""
    print()
    print("Step 2: Enter Database ID")
    print("-" * 60)
    print()
    print("For Beam Nexus Skills database, use:")
    print("  2bc2cadf-bbbc-80be-af8a-d45dfc8dfa2e")
    print()
    print("Or enter a different database ID if needed.")
    print()

    database_id = input("Enter NOTION_DATABASE_ID [default: 2bc2cadf-bbbc-80be-af8a-d45dfc8dfa2e]: ").strip()

    if not database_id:
        database_id = "2bc2cadf-bbbc-80be-af8a-d45dfc8dfa2e"

    return database_id


def test_api_connection(api_key, database_id):
    """Test API key and database access"""
    print()
    print("Step 3: Testing Connection")
    print("-" * 60)
    print()

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Notion-Version": "2022-06-28"
    }

    # Test 1: Get user info
    print("[TEST 1/2] Testing API key...", end=" ")
    try:
        response = requests.get("https://api.notion.com/v1/users/me", headers=headers, timeout=10)

        if response.status_code == 200:
            user_data = response.json()
            user_name = user_data.get('name', 'Unknown')
            user_id = user_data.get('id')
            print(f"✅ OK (Connected as: {user_name})")
            print()
        elif response.status_code == 401:
            print("❌ FAILED (Invalid API key)")
            return None, None
        else:
            print(f"❌ FAILED ({response.status_code})")
            return None, None

    except requests.exceptions.RequestException as e:
        print(f"❌ FAILED ({e})")
        return None, None

    # Test 2: Check database access
    print("[TEST 2/2] Testing database access...", end=" ")
    try:
        db_url = f"https://api.notion.com/v1/databases/{database_id}"
        response = requests.get(db_url, headers=headers, timeout=10)

        if response.status_code == 200:
            db_data = response.json()
            db_title = db_data.get('title', [{}])[0].get('plain_text', 'Unknown')
            print(f"✅ OK (Database: {db_title})")
            print()
        elif response.status_code == 404:
            print("❌ FAILED (Database not found or not accessible)")
            print()
            print("If using your own integration, you need to:")
            print("1. Open the database in Notion")
            print("2. Click '...' → 'Connections'")
            print("3. Add your integration")
            return user_id, user_name
        else:
            print(f"❌ FAILED ({response.status_code})")
            return user_id, user_name

    except requests.exceptions.RequestException as e:
        print(f"❌ FAILED ({e})")
        return user_id, user_name

    return user_id, user_name


def save_to_env(root, api_key, database_id):
    """Save configuration to .env file"""
    print("Step 4: Saving to .env")
    print("-" * 60)
    print()

    env_path = root / '.env'

    # Read existing .env if it exists
    existing_lines = []
    if env_path.exists():
        with open(env_path, 'r', encoding='utf-8') as f:
            existing_lines = f.readlines()

    # Update or add keys
    updated = []
    api_key_set = False
    db_id_set = False

    for line in existing_lines:
        if line.strip().startswith('NOTION_API_KEY='):
            updated.append(f'NOTION_API_KEY={api_key}\n')
            api_key_set = True
        elif line.strip().startswith('NOTION_SKILLS_DB_ID=') or line.strip().startswith('NOTION_DATABASE_ID='):
            updated.append(f'NOTION_SKILLS_DB_ID={database_id}\n')
            db_id_set = True
        else:
            updated.append(line)

    # Add if not present
    if not api_key_set:
        updated.append(f'\n# Notion Integration\nNOTION_API_KEY={api_key}\n')
    if not db_id_set:
        updated.append(f'NOTION_SKILLS_DB_ID={database_id}\n')

    # Write updated .env
    with open(env_path, 'w', encoding='utf-8') as f:
        f.writelines(updated)

    print(f"✅ Saved to: {env_path}")
    print()


def save_to_user_config(root, user_id, user_name, database_id):
    """Save user info to user-config.yaml"""
    print("Step 5: Saving to user-config.yaml")
    print("-" * 60)
    print()

    config_path = root / '01-memory' / 'user-config.yaml'

    if not config_path.exists():
        print(f"[WARN] user-config.yaml not found at {config_path}")
        print("[INFO] Skipping user config update")
        return

    # Read existing config
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

    try:
        config = yaml.safe_load(yaml_content) or {}
    except yaml.YAMLError:
        print("[ERROR] Could not parse user-config.yaml")
        return

    # Add notion_user_id and notion_user_name at ROOT level (required by check_notion_config.py)
    config['notion_user_id'] = user_id
    config['notion_user_name'] = user_name

    # Also save to integrations.notion for structured access
    if 'integrations' not in config:
        config['integrations'] = {}

    config['integrations']['notion'] = {
        'user_id': user_id,
        'user_name': user_name,
        'database_id': database_id,
        'setup_complete': True
    }

    # Write updated config
    updated_yaml = yaml.dump(config, default_flow_style=False, sort_keys=False)

    with open(config_path, 'w', encoding='utf-8') as f:
        f.write('---\n')
        f.write(updated_yaml)
        f.write('---\n')
        if footer:
            f.write(footer)

    print(f"✅ Saved to: {config_path}")
    print()


def main():
    """Main wizard flow"""
    # Configure UTF-8 output
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

    # Step 1: Get API key
    api_key = get_api_key()

    # Step 2: Get database ID
    database_id = get_database_id()

    # Step 3: Test connection
    user_id, user_name = test_api_connection(api_key, database_id)

    if not user_id:
        print()
        print("=" * 60)
        print("❌ SETUP FAILED")
        print("=" * 60)
        print()
        print("Please check your API key and try again.")
        sys.exit(1)

    # Step 4: Save to .env
    save_to_env(root, api_key, database_id)

    # Step 5: Save to user-config.yaml
    save_to_user_config(root, user_id, user_name, database_id)

    # Step 6: Run database discovery (auto-populate context)
    print("Step 6: Discovering Databases")
    print("-" * 60)
    print()
    print("Running initial database discovery...")
    print()

    discover_script = root / '00-system' / 'skills' / 'notion-master' / 'scripts' / 'discover_databases.py'
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
                print("✅ Database discovery complete")
                # Extract database count from output
                for line in result.stdout.split('\n'):
                    if 'database' in line.lower() and ('found' in line.lower() or 'saved' in line.lower()):
                        print(f"   {line.strip()}")
            else:
                print("⚠️  Discovery had issues (non-critical)")
                print("   Run manually: python 00-system/skills/notion-master/scripts/discover_databases.py")
        except subprocess.TimeoutExpired:
            print("⚠️  Discovery timed out (non-critical)")
        except Exception as e:
            print(f"⚠️  Discovery failed: {e} (non-critical)")
    else:
        print("⚠️  discover_databases.py not found")
    print()

    # Success summary
    print("=" * 60)
    print("✅ SETUP COMPLETE!")
    print("=" * 60)
    print()
    print("Configuration saved:")
    print(f"  • .env → NOTION_API_KEY, NOTION_SKILLS_DB_ID")
    print(f"  • user-config.yaml → notion_user_id ({user_name})")
    print(f"  • 01-memory/integrations/notion-databases.yaml → Database context")
    print()
    print("You can now use:")
    print("  • query-notion-db")
    print("  • import-skill-to-nexus")
    print("  • export-skill-to-notion")
    print()
    print("Try it now:")
    print('  Say "query notion skills" or "find Beam AI skills"')
    print()

    sys.exit(0)


if __name__ == "__main__":
    main()
