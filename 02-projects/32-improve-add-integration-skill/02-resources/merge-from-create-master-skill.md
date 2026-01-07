# Components to Merge from create-master-skill

**Created**: 2026-01-07
**Source**: `00-system/skills/skill-dev/create-master-skill/`

---

## Overview

`create-master-skill` has 5 high-value components that `add-integration` lacks.
This document details what to copy and how to adapt.

---

## 1. Test Templates (HIGH PRIORITY)

### Source Files

```
create-master-skill/scripts/init_master_skill.py
  → Generates tests/run_tests.py
  → Generates tests/README.md
```

### What to Create in add-integration

**New template**: `templates/tests/run_tests.py.template`

```python
#!/usr/bin/env python3
"""Test runner for {{SERVICE_NAME}} integration skills."""

import os
import sys
import subprocess

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.join(SKILL_DIR, 'scripts')


def test_config_script_exists():
    """Test that config script exists."""
    script = os.path.join(SCRIPTS_DIR, 'check_{{SERVICE_SLUG}}_config.py')
    assert os.path.exists(script), f"Script not found: {script}"
    print("✓ Config script exists")


def test_config_script_runs():
    """Test that config script executes without error."""
    script = os.path.join(SCRIPTS_DIR, 'check_{{SERVICE_SLUG}}_config.py')
    result = subprocess.run([sys.executable, script, '--json'],
                          capture_output=True, text=True)
    # Should return valid JSON even if config missing
    assert result.returncode in [0, 1], f"Script crashed: {result.stderr}"
    print("✓ Config script runs")


def test_api_client_exists():
    """Test that API client exists."""
    client = os.path.join(SCRIPTS_DIR, '{{SERVICE_SLUG}}_client.py')
    assert os.path.exists(client), f"Client not found: {client}"
    print("✓ API client exists")


def test_api_client_imports():
    """Test that API client imports without error."""
    sys.path.insert(0, SCRIPTS_DIR)
    try:
        import {{SERVICE_SLUG}}_client
        print("✓ API client imports")
    except ImportError as e:
        raise AssertionError(f"Import failed: {e}")


def test_references_exist():
    """Test that reference files exist."""
    refs_dir = os.path.join(SKILL_DIR, 'references')
    required = ['setup-guide.md', 'api-reference.md', 'error-handling.md']

    for ref in required:
        path = os.path.join(refs_dir, ref)
        assert os.path.exists(path), f"Reference not found: {path}"
        print(f"✓ {ref} exists")


def main():
    print(f"\n🧪 Testing {{SERVICE_NAME}} integration...\n")

    tests = [
        test_config_script_exists,
        test_config_script_runs,
        test_api_client_exists,
        test_api_client_imports,
        test_references_exist,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"❌ {test.__name__}: {e}")
            failed += 1

    print(f"\n📊 Results: {passed} passed, {failed} failed")
    sys.exit(0 if failed == 0 else 1)


if __name__ == '__main__':
    main()
```

**New template**: `templates/tests/README.md.template`

```markdown
# {{SERVICE_NAME}} Integration Tests

## Running Tests

```bash
python run_tests.py           # All tests
python run_tests.py --quick   # Quick smoke tests
```

## Test Categories

- **config**: Configuration validation
- **client**: API client functionality
- **references**: Documentation completeness

## Adding Tests

Add test functions to `run_tests.py` following the existing patterns.
```

### Update scaffold_integration.py

Add to `create_master_skill()` function:
```python
# Create tests directory
tests_dir = os.path.join(master_path, 'tests')
os.makedirs(tests_dir, exist_ok=True)

# Generate test files
create_file_from_template('tests/run_tests.py.template',
                         os.path.join(tests_dir, 'run_tests.py'),
                         replacements)
create_file_from_template('tests/README.md.template',
                         os.path.join(tests_dir, 'README.md'),
                         replacements)
```

---

## 2. Research Checklist (HIGH PRIORITY)

### Source File

```
create-master-skill/references/research-checklist.md (353 lines)
```

### What to Copy

**Copy to**: `add-integration/references/research-checklist.md`

This provides 10 comprehensive search areas vs add-integration's 2-3:

1. API Documentation (official docs)
2. API Reference (endpoints, methods)
3. Authentication Patterns (OAuth, API keys)
4. Common Operations (CRUD examples)
5. Error Handling (codes, recovery)
6. Rate Limits (throttling, backoff)
7. SDK/Libraries (Python packages)
8. Best Practices (patterns, anti-patterns)
9. Webhooks/Events (real-time updates)
10. Data Models (schemas, types)

### Update SKILL.md

Add to Step 3 (Web Search):
```markdown
### Step 3: Web Search for API Documentation

**Reference**: See `references/research-checklist.md` for comprehensive search guide.

Run these searches:
1. "{service} API documentation official"
2. "{service} API authentication"
3. "{service} API error codes"
...
```

---

## 3. Master Skill Patterns (MEDIUM PRIORITY)

### Source File

```
create-master-skill/references/master-skill-patterns.md (278 lines)
```

### What to Copy

**Copy to**: `add-integration/references/master-skill-patterns.md`

Documents:
- DRY architecture rationale
- Folder structure patterns
- SKILL.md patterns
- Script patterns
- Anti-patterns to avoid
- Context reduction metrics

### Why Useful

Users creating integrations will understand WHY the 3-tier pattern exists and how to maintain it.

---

## 4. Discover Resources Script (MEDIUM PRIORITY)

### Source File

```
create-master-skill/templates/discover_resources.py.template (229 lines)
```

### What to Copy

**Copy to**: `add-integration/templates/discover_resources.py.template`

This script helps users discover what resources exist in their account after setup:
- Lists all databases (Airtable)
- Lists all workspaces (Notion)
- Lists all projects (Langfuse)

### Update scaffold_integration.py

Add to `create_master_skill()`:
```python
# Generate discover script
create_file_from_template('discover_resources.py.template',
                         os.path.join(scripts_dir, f'discover_{slug}_resources.py'),
                         replacements)
```

---

## 5. Validation Tooling (LOW PRIORITY)

### Concept from create-master-skill

The skill emphasizes validation:
- Check all templates filled
- Verify Python syntax
- Test generated scripts

### What to Add to add-integration

**New script**: `scripts/validate_integration.py`

```python
#!/usr/bin/env python3
"""Validate generated integration structure."""

import os
import sys
import ast
import json

def validate_integration(service_slug, base_path):
    """Validate integration structure is complete and correct."""

    errors = []
    warnings = []

    skill_path = os.path.join(base_path, service_slug)

    # Check master skill
    master_path = os.path.join(skill_path, f'{service_slug}-master')
    if not os.path.exists(master_path):
        errors.append(f"Missing: {master_path}")
    else:
        # Check required files
        required = [
            'SKILL.md',
            f'scripts/{service_slug}_client.py',
            f'scripts/check_{service_slug}_config.py',
            'references/setup-guide.md',
        ]
        for req in required:
            if not os.path.exists(os.path.join(master_path, req)):
                errors.append(f"Missing: {master_path}/{req}")

    # Check connect skill
    connect_path = os.path.join(skill_path, f'{service_slug}-connect')
    if not os.path.exists(connect_path):
        errors.append(f"Missing: {connect_path}")

    # Validate Python syntax
    for root, dirs, files in os.walk(skill_path):
        for f in files:
            if f.endswith('.py'):
                path = os.path.join(root, f)
                try:
                    with open(path) as fp:
                        ast.parse(fp.read())
                except SyntaxError as e:
                    errors.append(f"Syntax error in {path}: {e}")

    # Check for unfilled placeholders
    for root, dirs, files in os.walk(skill_path):
        for f in files:
            if f.endswith('.md') or f.endswith('.py'):
                path = os.path.join(root, f)
                with open(path) as fp:
                    content = fp.read()
                    if '{{' in content and '}}' in content:
                        warnings.append(f"Unfilled placeholders in {path}")

    return errors, warnings

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: validate_integration.py <service_slug>")
        sys.exit(1)

    service_slug = sys.argv[1]
    base_path = os.path.join(os.path.dirname(__file__), '..', '..', '..')

    errors, warnings = validate_integration(service_slug, base_path)

    if errors:
        print("❌ ERRORS:")
        for e in errors:
            print(f"  - {e}")

    if warnings:
        print("⚠️ WARNINGS:")
        for w in warnings:
            print(f"  - {w}")

    if not errors and not warnings:
        print("✅ Integration validated successfully!")

    sys.exit(1 if errors else 0)
```

---

## Implementation Order

| Priority | Component | Effort | Impact |
|----------|-----------|--------|--------|
| 1 | Test templates | 2 hrs | HIGH - enables quality checks |
| 2 | Research checklist | 1 hr | HIGH - better API discovery |
| 3 | Master skill patterns | 30 min | MEDIUM - documentation |
| 4 | Discover resources | 2 hrs | MEDIUM - user convenience |
| 5 | Validation script | 2 hrs | LOW - developer tooling |

**Total**: ~8 hours

---

## Checklist

- [ ] Copy test templates to add-integration
- [ ] Update scaffold to generate tests
- [ ] Copy research-checklist.md
- [ ] Update SKILL.md Step 3 to reference checklist
- [ ] Copy master-skill-patterns.md
- [ ] Copy discover_resources.py.template
- [ ] Update scaffold to generate discover script
- [ ] Create validate_integration.py
- [ ] Test all changes end-to-end
