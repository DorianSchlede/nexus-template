# Unit Tests for bulk-complete.py

## Overview

Comprehensive test suite for the bulk task completion script, ensuring reliable operation across both new (steps.md) and legacy (tasks.md) project formats.

## Test Coverage

### File Detection Tests (`TestFileDetection`)
- ✅ Prefer steps.md when both files exist
- ✅ Fall back to tasks.md for legacy projects
- ✅ Return None when neither file exists
- ✅ Handle edge cases

### Task Extraction Tests (`TestTaskExtraction`)
- ✅ Extract uncompleted tasks correctly
- ✅ Handle mixed completed/uncompleted tasks
- ✅ Case-insensitive completion markers ([x] and [X])
- ✅ Indented task support
- ✅ Empty content handling

### Task Counting Tests (`TestTaskCounting`)
- ✅ Count all uncompleted tasks
- ✅ Count all completed tasks
- ✅ Count mixed task states

### Section Extraction Tests (`TestSectionExtraction`)
- ✅ Extract tasks from "Section N" format (legacy)
- ✅ Extract tasks from "Phase N" format (new)
- ✅ Handle section headers with colons
- ✅ Extract last section (no next section boundary)
- ✅ Return empty set for nonexistent sections

### Range Selection Tests (`TestRangeSelection`)
- ✅ Parse single task numbers
- ✅ Parse task ranges (1-5)
- ✅ Parse multiple ranges and numbers (1-3,7,10-12)
- ✅ Ignore out-of-bounds tasks
- ✅ Handle invalid formats gracefully
- ✅ Handle overlapping ranges

### Integration Tests (`TestIntegration`)
- ✅ Detect and use steps.md for new projects
- ✅ Detect and use tasks.md for legacy projects
- ✅ Count tasks correctly in new format
- ✅ Extract Phase tasks from new projects

## Running Tests

### Run all tests:
```bash
cd "00-system/skills/close-session/tests"
python test_bulk_complete_tasks.py
```

### Expected output:
```
test_count_all_completed (test_bulk_complete_tasks.TestTaskCounting) ... ok
test_count_all_uncompleted (test_bulk_complete_tasks.TestTaskCounting) ... ok
test_count_mixed (test_bulk_complete_tasks.TestTaskCounting) ... ok
...
----------------------------------------------------------------------
Ran 35 tests in 0.123s

OK
```

## Test Fixtures

The tests use temporary directories with mock project structures:

### New Project Format (steps.md):
```
01-new-project/
  01-planning/
    steps.md          # Phase 1, Phase 2, Phase 3 format
```

### Legacy Project Format (tasks.md):
```
00-onboarding/
  01-planning/
    tasks.md          # Section 0, Section 1 format
```

## What's Tested

| Feature | Test Coverage |
|---------|---------------|
| File detection | 4 tests |
| Task extraction | 5 tests |
| Task counting | 3 tests |
| Section parsing | 5 tests |
| Range selection | 6 tests |
| Integration | 4 tests |
| **Total** | **27 tests** |

## Version Compatibility

These tests verify that `bulk-complete-v2.py` works correctly with:

✅ **New projects** (created by init_project.py)
- Uses steps.md
- Phase 1, Phase 2, Phase 3 naming
- Created after 2025-01-20

✅ **Legacy projects** (onboarding, older projects)
- Uses tasks.md
- Section 0, Section 1 naming
- Created before 2025-01-20

✅ **Backward compatibility**
- All existing projects continue to work
- No breaking changes

## Adding New Tests

When adding new functionality to bulk-complete.py:

1. Add test case to appropriate test class
2. Run tests to verify passing
3. Update this README with new coverage

Example:
```python
def test_new_feature(self):
    """Should handle new feature correctly"""
    # Arrange
    content = "..."

    # Act
    result = new_function(content)

    # Assert
    self.assertEqual(result, expected)
```

## CI/CD Integration

These tests can be integrated into CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Run bulk-complete tests
  run: |
    cd "00-system/skills/close-session/tests"
    python test_bulk_complete_tasks.py
```

## Maintenance

- **Update frequency**: After any changes to bulk-complete.py
- **Test duration**: ~0.1-0.5 seconds
- **Dependencies**: Python 3.8+ standard library only
