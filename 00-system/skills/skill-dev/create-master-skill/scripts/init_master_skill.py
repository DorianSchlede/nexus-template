#!/usr/bin/env python3
"""
Initialize Master Skill Structure

Creates the folder structure and initial files for a new master skill.
Templates are populated with integration-specific placeholders.

Usage:
    python init_master_skill.py <integration-name> [--path PATH]

Example:
    python init_master_skill.py airtable
    python init_master_skill.py slack --path 00-system/skills

Arguments:
    integration-name    Name of the integration (lowercase, hyphenated)
    --path PATH         Base path for skill (default: 00-system/skills)
"""

import os
import sys
import argparse
import shutil
from datetime import datetime

# Find Nexus root
def find_nexus_root():
    current = os.path.dirname(os.path.abspath(__file__))
    while current != os.path.dirname(current):
        if os.path.exists(os.path.join(current, 'CLAUDE.md')):
            return current
        current = os.path.dirname(current)
    return None

NEXUS_ROOT = find_nexus_root()
if not NEXUS_ROOT:
    print("❌ Error: Could not find Nexus root")
    sys.exit(1)

TEMPLATES_DIR = os.path.join(NEXUS_ROOT, '00-system', 'skills', 'skill-dev', 'create-master-skill', 'templates')


def validate_name(name):
    """Validate integration name."""
    # Lowercase, hyphenated, no special chars
    import re
    if not re.match(r'^[a-z][a-z0-9-]*$', name):
        return False
    return True


def create_folder_structure(base_path, integration_name):
    """Create the master skill folder structure."""
    skill_path = os.path.join(base_path, f'{integration_name}-master')

    # Check if already exists
    if os.path.exists(skill_path):
        print(f"❌ Skill already exists: {skill_path}")
        return None

    # Create directories
    dirs = [
        skill_path,
        os.path.join(skill_path, 'references'),
        os.path.join(skill_path, 'scripts'),
        os.path.join(skill_path, 'tests'),
    ]

    for d in dirs:
        os.makedirs(d, exist_ok=True)

    return skill_path


def get_replacements(integration_name):
    """Get template replacement values."""
    title = integration_name.replace('-', ' ').title()

    return {
        '{{INTEGRATION}}': integration_name,
        '{{INTEGRATION_TITLE}}': title,
        '{{INTEGRATION_UPPER}}': integration_name.upper().replace('-', '_'),
        '{{DATE}}': datetime.now().strftime('%Y-%m-%d'),
        '{{STATUS}}': 'Development',

        # Placeholders for manual filling
        '{{CHILD_SKILL_1}}': f'{integration_name}-query',
        '{{CHILD_SKILL_1_DESC}}': 'Query and search operations',
        '{{CHILD_SKILL_2}}': f'{integration_name}-sync',
        '{{CHILD_SKILL_2_DESC}}': 'Import/export operations',
        '{{CHILD_SKILL_3}}': f'{integration_name}-manage',
        '{{CHILD_SKILL_3_DESC}}': 'Management operations',
        '{{NUM_SKILLS}}': '3',

        '{{RESOURCE_TYPE}}': 'resource',
        '{{RESOURCE_SINGULAR}}': 'Resource',
        '{{RESOURCE_PLURAL}}': 'Resources',
        '{{RESOURCE_PLURAL_LOWER}}': 'resources',
        '{{RESOURCE_UPPER}}': 'RESOURCE',
        '{{RESOURCE_ID_NAME}}': 'Resource ID',
        '{{RESOURCE_ENDPOINT}}': 'resources',

        '{{API_BASE_URL}}': f'https://api.{integration_name}.com/v1',
        '{{API_VERSION_INFO}}': 'Versioned via URL path (v1, v2)',
        '{{AUTH_METHOD}}': 'Bearer Token',
        '{{AUTH_DESCRIPTION}}': 'API key passed as Bearer token in Authorization header.',
        '{{AUTH_HEADER_FORMAT}}': 'Bearer {api_key}',
        '{{AUTH_EXAMPLE}}': 'Bearer sk_xxx...',
        '{{API_KEY_FORMAT}}': 'sk_xxxxxxxxxxxxx',
        '{{API_KEY_PREFIX}}': 'sk_',
        '{{API_KEY_URL}}': f'https://{integration_name}.com/settings/api',
        '{{API_KEY_INSTRUCTIONS}}': 'Navigate to API section and generate a new key',
        '{{API_KEY_PLACEHOLDER}}': '{api_key}',
        '{{API_TEST_ENDPOINT}}': f'https://api.{integration_name}.com/v1/users/me',

        '{{ADDITIONAL_HEADERS}}': '',
        '{{ADDITIONAL_HEADERS_DICT}}': '',
        '{{ADDITIONAL_ENV_VARS}}': '',
        '{{ADDITIONAL_REQUIRED_VARS}}': '',
        '{{OPTIONAL_ENV_VARS}}': '',
        '{{OPTIONAL_ENV_VARS_LIST}}': '',

        '{{EXAMPLE_USER_REQUEST}}': f'query my {integration_name} data',
        '{{EXAMPLE_ENDPOINT}}': 'users/me',
        '{{EXAMPLE_ID}}': 'abc123',

        '{{ADDITIONAL_REFERENCES}}': '',
        '{{ADDITIONAL_SCRIPTS}}': '',
        '{{OPERATION_2}}': 'import/export',
        '{{OPERATION_3}}': 'management',

        '{{PERMISSION_SOLUTION}}': 'Verify API key has required permissions',
        '{{STATUS_PAGE_URL}}': f'https://status.{integration_name}.com',
        '{{OFFICIAL_API_DOCS_URL}}': f'https://developers.{integration_name}.com/api',
        '{{OFFICIAL_AUTH_DOCS_URL}}': f'https://developers.{integration_name}.com/auth',
        '{{OFFICIAL_RATE_DOCS_URL}}': f'https://developers.{integration_name}.com/rate-limits',
        '{{OFFICIAL_CHANGELOG_URL}}': f'https://developers.{integration_name}.com/changelog',
        '{{COMMUNITY_URL}}': f'https://community.{integration_name}.com',

        '{{USER_ID_FORMAT}}': 'user_xxxxxxxx',
        '{{GET_USER_CURL}}': f'curl "https://api.{integration_name}.com/v1/users/me" -H "Authorization: Bearer $API_KEY"',
        '{{TEST_CONNECTION_CURL}}': f'curl "https://api.{integration_name}.com/v1/users/me" -H "Authorization: Bearer ${{INTEGRATION_UPPER}}_API_KEY"',
        '{{TEST_RESOURCE_CURL}}': f'curl "https://api.{integration_name}.com/v1/resources" -H "Authorization: Bearer ${{INTEGRATION_UPPER}}_API_KEY"',
        '{{SUCCESS_RESPONSE_EXAMPLE}}': '{"id": "...", "name": "...", "type": "user"}',
        '{{RESOURCE_SUCCESS_EXAMPLE}}': '{"data": [...], "has_more": false}',

        '{{EXTRACT_IDENTIFIER}}': 'data.get("name", data.get("id", "unknown"))',

        # Placeholders for research-filled values
        '{{LIST_PARAMS}}': '| limit | integer | No | Max results (default 100) |',
        '{{LIST_RESPONSE_EXAMPLE}}': '{"data": [...], "has_more": false}',
        '{{GET_RESPONSE_EXAMPLE}}': '{"id": "...", "name": "...", ...}',
        '{{CREATE_REQUEST_EXAMPLE}}': '{"name": "New Resource", ...}',
        '{{CREATE_CURL_DATA}}': '{"name": "New Resource"}',
        '{{CREATE_RESPONSE_EXAMPLE}}': '{"id": "...", "name": "New Resource", ...}',
        '{{UPDATE_METHOD}}': 'PATCH',
        '{{UPDATE_REQUEST_EXAMPLE}}': '{"name": "Updated Name"}',
        '{{UPDATE_CURL_DATA}}': '{"name": "Updated Name"}',

        '{{FILTER_SYNTAX_DESCRIPTION}}': 'Filters are passed as query parameters or in request body.',
        '{{FILTER_OPERATORS}}': '| equals | Exact match | field=value |',
        '{{FILTER_EXAMPLE}}': 'curl "...?status=active"',

        '{{SORT_DESCRIPTION}}': 'Results can be sorted by field name.',
        '{{SORT_EXAMPLE}}': 'curl "...?sort=created_at&order=desc"',

        '{{PAGINATION_DESCRIPTION}}': 'Cursor-based pagination with has_more indicator.',
        '{{PAGINATION_PARAMS}}': '| limit | Max results per page |\n| cursor | Pagination cursor |',
        '{{PAGINATION_EXAMPLE}}': 'curl "...?limit=10&cursor=xxx"',

        '{{RATE_LIMIT_TABLE}}': '| Requests per minute | 100 |',
        '{{RATE_LIMIT_HEADERS}}': 'X-RateLimit-Remaining: 99\nX-RateLimit-Reset: 1234567890',
        '{{RATE_REMAINING_HEADER}}': 'X-RateLimit-Remaining',
        '{{RETRY_AFTER_HEADER}}': 'Retry-After',

        '{{PATTERN_1_NAME}}': 'Batch Operations',
        '{{PATTERN_1_DESCRIPTION}}': 'Process multiple items in a single request.',
        '{{PATTERN_1_EXAMPLE}}': 'curl -X POST "...batch" -d \'{"items": [...]}\'',
        '{{PATTERN_2_NAME}}': 'Webhooks',
        '{{PATTERN_2_DESCRIPTION}}': 'Subscribe to real-time events.',
        '{{PATTERN_2_EXAMPLE}}': 'curl -X POST "...webhooks" -d \'{"url": "..."}\'',

        '{{PROPERTY_TYPES_TABLE}}': '| string | Text value | "text" | "text" |',

        '{{CHILD_SKILL_2_ERRORS}}': '| Import failed | Source unavailable | Check source status |',
        '{{CHILD_SKILL_3_ERRORS}}': '| Update failed | Validation error | Check field values |',

        # Discovery script placeholders
        '{{PAGINATION_INIT}}': 'cursor = None',
        '{{PAGINATION_URL}}': 'url = f"{API_BASE_URL}/resources" + (f"?cursor={cursor}" if cursor else "")',
        '{{REQUEST_METHOD}}': 'get',
        '{{REQUEST_KWARGS}}': '',
        '{{EXTRACT_RESULTS}}': 'data.get("data", [])',
        '{{EXTRACT_ID}}': 'item.get("id")',
        '{{EXTRACT_NAME}}': 'item.get("name", "Unnamed")',
        '{{ADDITIONAL_FIELDS}}': '',
        '{{PAGINATION_CHECK}}': 'has_more = data.get("has_more", False)',
        '{{PAGINATION_UPDATE}}': 'cursor = data.get("next_cursor")',
        '{{SCHEMA_ENDPOINT}}': 'resources',
        '{{EXTRACT_SCHEMA}}': 'data.get("properties", {})',
    }


def process_template(template_path, output_path, replacements):
    """Process a template file with replacements."""
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()

    for key, value in replacements.items():
        content = content.replace(key, value)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)


def create_master_skill(integration_name, base_path):
    """Create a new master skill from templates."""
    print(f"\n🔧 Creating {integration_name}-master skill...")
    print(f"   Base path: {base_path}")

    # Validate name
    if not validate_name(integration_name):
        print(f"❌ Invalid name: {integration_name}")
        print("   Use lowercase letters, numbers, and hyphens only")
        print("   Must start with a letter")
        return None

    # Create folder structure
    skill_path = create_folder_structure(base_path, integration_name)
    if not skill_path:
        return None

    print(f"   ✓ Created folder structure")

    # Get replacements
    replacements = get_replacements(integration_name)

    # Process templates
    templates = [
        ('SKILL.md.template', 'SKILL.md'),
        ('setup-guide.md.template', 'references/setup-guide.md'),
        ('api-reference.md.template', 'references/api-reference.md'),
        ('error-handling.md.template', 'references/error-handling.md'),
        ('check_config.py.template', f'scripts/check_{integration_name.replace("-", "_")}_config.py'),
        ('discover_resources.py.template', 'scripts/discover_resources.py'),
    ]

    for template_name, output_name in templates:
        template_path = os.path.join(TEMPLATES_DIR, template_name)
        output_path = os.path.join(skill_path, output_name)

        if os.path.exists(template_path):
            process_template(template_path, output_path, replacements)
            print(f"   ✓ Created {output_name}")
        else:
            print(f"   ⚠️  Template not found: {template_name}")

    # Create tests README
    tests_readme = os.path.join(skill_path, 'tests', 'README.md')
    with open(tests_readme, 'w', encoding='utf-8') as f:
        f.write(f"""# {integration_name.replace('-', ' ').title()} Master Tests

## Running Tests

```bash
python run_tests.py           # All tests
python run_tests.py --quick   # Quick smoke tests
```

## Test Categories

- **config**: Configuration validation
- **discovery**: Resource discovery
- **api**: API operations

## Adding Tests

Add test functions to `run_tests.py` following the existing patterns.
""")
    print(f"   ✓ Created tests/README.md")

    # Create basic test runner
    test_runner = os.path.join(skill_path, 'tests', 'run_tests.py')
    with open(test_runner, 'w', encoding='utf-8') as f:
        f.write(f'''#!/usr/bin/env python3
"""Basic test runner for {integration_name}-master skill."""

import os
import sys
import subprocess

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.join(SKILL_DIR, 'scripts')


def test_config_script_exists():
    """Test that config script exists."""
    script = os.path.join(SCRIPTS_DIR, 'check_{integration_name.replace("-", "_")}_config.py')
    assert os.path.exists(script), f"Script not found: {{script}}"
    print("✓ Config script exists")


def test_discover_script_exists():
    """Test that discover script exists."""
    script = os.path.join(SCRIPTS_DIR, 'discover_resources.py')
    assert os.path.exists(script), f"Script not found: {{script}}"
    print("✓ Discover script exists")


def test_references_exist():
    """Test that reference files exist."""
    refs_dir = os.path.join(SKILL_DIR, 'references')
    required = ['setup-guide.md', 'api-reference.md', 'error-handling.md']

    for ref in required:
        path = os.path.join(refs_dir, ref)
        assert os.path.exists(path), f"Reference not found: {{path}}"
        print(f"✓ {{ref}} exists")


def main():
    print(f"\\n🧪 Testing {integration_name}-master skill...\\n")

    tests = [
        test_config_script_exists,
        test_discover_script_exists,
        test_references_exist,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"❌ {{test.__name__}}: {{e}}")
            failed += 1

    print(f"\\n📊 Results: {{passed}} passed, {{failed}} failed")
    sys.exit(0 if failed == 0 else 1)


if __name__ == '__main__':
    main()
''')
    print(f"   ✓ Created tests/run_tests.py")

    print(f"\n✅ Created: {skill_path}")
    print(f"\n📝 Next steps:")
    print(f"   1. Review and fill in placeholders in SKILL.md")
    print(f"   2. Complete setup-guide.md with actual API docs")
    print(f"   3. Fill api-reference.md from research")
    print(f"   4. Update scripts with real API endpoints")
    print(f"   5. Run tests: python {skill_path}/tests/run_tests.py")

    return skill_path


def main():
    parser = argparse.ArgumentParser(
        description='Initialize a new master skill structure',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python init_master_skill.py airtable
    python init_master_skill.py google-sheets
    python init_master_skill.py slack --path 00-system/skills
        """
    )
    parser.add_argument('integration', help='Integration name (lowercase, hyphenated)')
    parser.add_argument('--path', default=os.path.join(NEXUS_ROOT, '00-system', 'skills'),
                        help='Base path for skill creation')

    args = parser.parse_args()

    # Ensure path is absolute
    if not os.path.isabs(args.path):
        args.path = os.path.join(NEXUS_ROOT, args.path)

    # Create the skill
    result = create_master_skill(args.integration, args.path)

    sys.exit(0 if result else 1)


if __name__ == '__main__':
    main()
