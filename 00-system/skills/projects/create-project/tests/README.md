# Unit Tests for init_project.py

## Overview

Comprehensive test suite for the project initialization script, ensuring correct project structure creation, naming, and template generation.

## Test Coverage

### Name Sanitization Tests (`TestProjectNameSanitization`)
- ✅ Convert to lowercase
- ✅ Replace spaces with hyphens
- ✅ Remove special characters
- ✅ Collapse multiple hyphens
- ✅ Remove leading/trailing hyphens
- ✅ Remove unicode characters
- ✅ Preserve numbers
- ✅ Handle empty after sanitization
- ✅ Handle complex mixed inputs

### Project ID Assignment Tests (`TestProjectIDAssignment`)
- ✅ Return "01" for first project
- ✅ Increment IDs sequentially
- ✅ Handle non-sequential existing IDs
- ✅ Maintain zero-padding for single digits
- ✅ Handle double-digit IDs correctly
- ✅ Ignore non-matching directory names
- ✅ Handle nonexistent directory

### Project Initialization Tests (`TestProjectInitialization`)
- ✅ Create complete project structure
- ✅ Create all required directories (01-04)
- ✅ Create all planning files from templates
- ✅ Populate overview.md with project info
- ✅ Create steps.md with checkbox tasks
- ✅ Include mental models section in plan.md
- ✅ Assign sequential IDs to multiple projects
- ✅ Fail gracefully on duplicate project names
- ✅ Fail gracefully on invalid names
- ✅ Handle complex project names

### Template Content Tests (`TestTemplateContent`)
- ✅ Generate valid YAML frontmatter
- ✅ Include all phases (Phase 1-4) in steps.md
- ✅ Include Dependencies & Links section
- ✅ Ensure all files have substantial content

## Running Tests

### Run all tests:
```bash
cd "00-system/skills/create-project/tests"
python test_init_project.py
```

### Expected output:
```
test_basic_lowercase (test_init_project.TestProjectNameSanitization) ... ok
test_complex_project_name (test_init_project.TestProjectInitialization) ... ok
test_create_basic_project (test_init_project.TestProjectInitialization) ... ok
...
----------------------------------------------------------------------
Ran 31 tests in 0.234s

OK
```

## Test Fixtures

Tests use temporary directories with mock project structures created and destroyed for each test.

## What's Tested

| Feature | Test Coverage |
|---------|---------------|
| Name sanitization | 9 tests |
| ID assignment | 7 tests |
| Project initialization | 10 tests |
| Template content | 5 tests |
| **Total** | **31 tests** |

## Project Structure Verification

Tests verify the complete structure created by init_project.py:

```
NN-project-name/
├── 01-planning/
│   ├── overview.md      ✅ YAML + purpose + success criteria
│   ├── plan.md          ✅ Approach + mental models + dependencies
│   └── steps.md         ✅ Phase 1-4 + checkbox tasks
├── 02-resources/        ✅ Empty folder ready for reference materials
├── 03-working/          ✅ Empty folder for work-in-progress
└── 04-outputs/          ✅ Empty folder for final deliverables
```

## Name Sanitization Examples

| Input | Expected Output |
|-------|-----------------|
| `"My Project"` | `"my-project"` |
| `"Lead Qualification System v2.0"` | `"lead-qualification-system-v20"` |
| `"Project@123!"` | `"project123"` |
| `"---Project---"` | `"project"` |
| `"@#$%^&*()"` | `""` (invalid) |

## ID Assignment Examples

| Existing Projects | Next ID |
|-------------------|---------|
| None | `"01"` |
| `01-project` | `"02"` |
| `01, 02, 03` | `"04"` |
| `01, 05, 03` | `"06"` (max + 1) |
| `09-project` | `"10"` (handles double digits) |

## Template Validation

Tests verify that generated files contain required sections:

### overview.md:
- ✅ YAML frontmatter (id, name, status, description, created)
- ✅ Purpose section
- ✅ Success Criteria section
- ✅ Context section
- ✅ Timeline section

### plan.md:
- ✅ Approach section
- ✅ Key Decisions section
- ✅ Resources Needed section
- ✅ Dependencies & Links section
- ✅ Open Questions section
- ✅ Mental Models Applied section

### steps.md:
- ✅ Phase 1: Setup & Planning
- ✅ Phase 2: [User-defined]
- ✅ Phase 3: [User-defined]
- ✅ Phase 4: Testing & Launch
- ✅ Checkbox tasks (- [ ]) throughout

## Adding New Tests

When adding new functionality to init_project.py:

1. Add test case to appropriate test class
2. Run tests to verify passing
3. Update this README with new coverage

Example:
```python
def test_new_template_section(self):
    """Should include new section in template"""
    result = init_project("Test Project", str(self.projects_path))
    content = (result / "01-planning" / "plan.md").read_text()

    self.assertIn("## New Section", content)
```

## CI/CD Integration

These tests can be integrated into CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Run init_project tests
  run: |
    cd "00-system/skills/create-project/tests"
    python test_init_project.py
```

## Edge Cases Tested

- ✅ Special characters in names
- ✅ Unicode characters
- ✅ Empty names after sanitization
- ✅ Duplicate project names
- ✅ Non-sequential existing project IDs
- ✅ Nonexistent target directories
- ✅ Very long project names
- ✅ Numbers and mixed case

## Maintenance

- **Update frequency**: After any changes to init_project.py or templates
- **Test duration**: ~0.2-0.6 seconds
- **Dependencies**: Python 3.8+ standard library only
- **Temp directory cleanup**: Automatic (setUp/tearDown)
