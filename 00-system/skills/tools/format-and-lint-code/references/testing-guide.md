# Testing Guide - Format and Lint Code

Complete testing procedures for the format-and-lint-code skill.

## Test Environment Setup

### Prerequisites

```bash
# Create test directory
mkdir test-format-lint
cd test-format-lint

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # or 'venv\Scripts\activate' on Windows

# Install dependencies
pip install black flake8 pylint isort
npm install -g prettier eslint
```

### Test Build Structure

```
test-format-lint/
├── python_files/
│   ├── simple.py
│   ├── complex.py
│   └── syntax_error.py
├── js_files/
│   ├── simple.js
│   └── complex.ts
├── config_files/
│   ├── bad.yaml
│   └── bad.json
├── .format-config.yaml
└── expected_results/
    ├── simple_py_expected.txt
    └── ...
```

---

## Test Cases

### Test 1: Basic Python Formatting

**Objective**: Verify Black formatter works correctly

**Input File** (`python_files/simple.py`):
```python
def hello(name):
    """Say hello."""
    print(f"Hello, {name}!")

result=hello("World")  # Bad spacing
```

**Expected Output After Formatting**:
```python
def hello(name):
    """Say hello."""
    print(f"Hello, {name}!")


result = hello("World")  # Fixed spacing
```

**Test Steps**:
1. Run: `format and lint code --files python_files/simple.py`
2. Verify: Spacing around `=` is fixed
3. Verify: Blank lines before function are correct (2 blank lines at module level)

**Pass Criteria**:
- [ ] Spacing fixed (result = not result=)
- [ ] Blank lines correct
- [ ] File modified
- [ ] Linting passes with no errors

---

### Test 2: JavaScript/TypeScript Linting

**Objective**: Verify ESLint catches common JS issues

**Input File** (`js_files/simple.js`):
```javascript
function getData() {
    const unusedVar = "not used";  // Unused variable
    return fetch('/api')
        .then(r => r.json())  // Arrow function rules
        .then(data => console.log(data))
}
```

**Expected Linting Issues**:
- `no-unused-vars`: unusedVar is defined but never used
- `arrow-parens`: Arrow function parameters should have parens: `(r) =>`

**Test Steps**:
1. Run: `format and lint code --files js_files/simple.js`
2. Verify: ESLint output shows both issues
3. Verify: Severity levels are correct (warnings, not errors)

**Pass Criteria**:
- [ ] ESLint runs successfully
- [ ] Both issues detected
- [ ] Severity levels correct
- [ ] Line numbers match

---

### Test 3: Multi-Language Detection

**Objective**: Verify language detection across mixed build

**Input Files**:
```
.
├── main.py
├── config.yaml
├── script.sh
├── app.js
└── data.json
```

**Test Steps**:
1. Run: `format and lint code --all`
2. Verify output shows:
   ```
   📦 Detected Languages:
   [OK] Python: 1 file
   [OK] JavaScript: 1 file
   [OK] YAML: 1 file
   [OK] Shell: 1 file
   [OK] JSON: 1 file
   ```

**Pass Criteria**:
- [ ] All 5 languages detected
- [ ] File count correct for each
- [ ] Appropriate tools shown for each language

---

### Test 4: Configuration File Respect

**Objective**: Verify tool-specific configs are respected

**Setup**:
Create `pyproject.toml`:
```toml
[tool.black]
line-length = 88  # Different from default 100
```

**Input File** (`example.py`):
```python
# 89 character line (would fail with 88, pass with 100)
this_is_a_very_long_variable_name_that_exceeds_88_chars_but_not_100_characters_total = 1
```

**Test Steps**:
1. Run: `format and lint code --files example.py`
2. Verify: Black respects line-length of 88 from pyproject.toml
3. Verify: Would fail formatting (line is 89 chars, exceeds 88)

**Pass Criteria**:
- [ ] pyproject.toml settings read
- [ ] 88-char limit applied (not 100)
- [ ] Formatting shows violation

---

### Test 5: Pre-commit Hook Installation

**Objective**: Verify hook installation and execution

**Test Steps**:
1. Initialize git repo: `git init`
2. Run: `format code --install-hook`
3. Verify: `.git/hooks/pre-commit` created
4. Verify: Hook is executable: `ls -l .git/hooks/pre-commit`
5. Create test file with formatting issues: `bad_format.py`
6. Stage file: `git add bad_format.py`
7. Try to commit: `git commit -m "test"`
8. Verify: Hook runs and prevents commit (or auto-fixes)

**Pass Criteria**:
- [ ] Hook file created
- [ ] Hook executable
- [ ] Hook runs on commit attempt
- [ ] Auto-fixes applied (if configured)
- [ ] Commit blocked on errors (if configured)

---

### Test 6: Exclude Patterns

**Objective**: Verify files matching exclude patterns are skipped

**Setup**:
Create build with:
```
.
├── src/
│   └── main.py          # Should format
├── node_modules/
│   └── package.py       # Should skip
└── .format-config.yaml
```

`.format-config.yaml`:
```yaml
format_and_lint:
  exclude:
    - "**/node_modules/**"
```

**Test Steps**:
1. Run: `format and lint code --all`
2. Verify output doesn't include `node_modules/package.py`
3. Add formatting error to `node_modules/package.py`
4. Run again, verify still skipped

**Pass Criteria**:
- [ ] node_modules files skipped
- [ ] src/ files processed
- [ ] Output confirms skip reason

---

### Test 7: Interactive Mode

**Objective**: Verify interactive prompts work correctly

**Test Steps**:
1. Create file with mixed issues:
   - Some auto-fixable (spacing, quotes)
   - Some that need user decision (line too long)

2. Run: `format and lint code --interactive`

3. At each prompt, test:
   - `[auto-fix]` - Applies automatic fix
   - `[skip]` - Continues without fixing
   - `[manual]` - Shows location for manual fix

**Pass Criteria**:
- [ ] Prompts appear for each issue
- [ ] [auto-fix] option works
- [ ] [skip] option skips to next
- [ ] [manual] shows file location
- [ ] Final report accurate

---

### Test 8: Error Handling

**Objective**: Verify graceful error handling

#### Test 8a: Syntax Error in File

**Input**: Python file with syntax error
```python
def broken(:
    pass
```

**Expected Behavior**:
- Skip file with message: "[!] Skipped: broken.py - Syntax error"
- Continue with other files
- Show in final report

**Pass Criteria**:
- [ ] Skipped gracefully
- [ ] Clear error message
- [ ] Processing continues

#### Test 8b: Tool Not Installed

**Scenario**: Run with formatter not installed

**Expected Behavior**:
```
[!] Tool not found: prettier

Install with: npm install -g prettier
Continue without this tool? (yes/no)
```

**Pass Criteria**:
- [ ] Clear error message
- [ ] Installation instructions provided
- [ ] Option to continue or abort

#### Test 8c: Permission Denied

**Scenario**: Read-only file

**Expected Behavior**:
```
[!] Permission denied: readonly.js
Skipping...
```

**Pass Criteria**:
- [ ] Graceful skip
- [ ] Clear reason
- [ ] Continue processing other files

---

### Test 9: Report Generation

**Objective**: Verify report output format and accuracy

**Test Steps**:
1. Create build with multiple issues
2. Run: `format and lint code --report`
3. Verify report includes:
   - Languages detected
   - Files processed
   - Issues by category (errors, warnings, info)
   - Summary statistics
   - Recommendations

**Expected Report Format**:
```
Format & Lint Report
════════════════════════════════════════

Languages Detected:
  Python: 5 files (5 issues)
  JavaScript: 3 files (8 issues)

Issues by Severity:
  Errors: 3
  Warnings: 8
  Info: 2

Top Issues:
  1. Line too long (4 occurrences)
  2. Unused variable (3 occurrences)
  3. Missing docstring (2 occurrences)

Recommendations:
  1. Run: black src/
  2. Run: isort src/
  3. Review unused imports in src/api.py
```

**Pass Criteria**:
- [ ] Report includes all sections
- [ ] Statistics accurate
- [ ] Recommendations relevant
- [ ] Output is readable

---

### Test 10: Git Integration

**Objective**: Verify --staged flag works with git

**Test Steps**:
1. Initialize git repo
2. Create files with issues
3. Stage some files: `git add some_files`
4. Run: `format and lint code --staged`
5. Verify: Only staged files processed
6. Run: `format and lint code --all`
7. Verify: All files processed

**Pass Criteria**:
- [ ] --staged processes only staged files
- [ ] --all processes all files
- [ ] File counts accurate
- [ ] Git detection works

---

## Performance Tests

### Test P1: Large File Set

**Objective**: Verify performance with 100+ files

**Setup**:
- Create 100 Python files with various issues
- Mix of sizes (1KB to 10KB)

**Test Steps**:
1. Run: `format and lint code --all`
2. Measure execution time
3. Should complete in < 30 seconds

**Pass Criteria**:
- [ ] Completes in reasonable time
- [ ] Memory usage reasonable
- [ ] All files processed

---

## Regression Test Suite

Run these after any code changes:

```bash
#!/bin/bash

echo "Running regression test suite..."

# Test 1: Basic Python
python -m format_and_lint python_files/simple.py
[ $? -eq 0 ] && echo "[OK] Test 1 passed" || echo "[FAIL] Test 1 FAILED"

# Test 2: JavaScript
node -e "require('eslint-cli').execute('js_files/simple.js')"
[ $? -eq 0 ] && echo "[OK] Test 2 passed" || echo "[FAIL] Test 2 FAILED"

# Test 3: Multi-language
python -m format_and_lint .
[ $? -eq 0 ] && echo "[OK] Test 3 passed" || echo "[FAIL] Test 3 FAILED"

echo "Regression suite complete"
```

---

## Automated Testing with pytest

Create `tests/test_format_lint.py`:

```python
import subprocess
import tempfile
import os
from pathlib import Path

class TestFormatLint:
    def test_python_formatting(self):
        """Test Python file formatting."""
        code = "x=1"  # Bad spacing
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            f.flush()

            result = subprocess.run(
                ['python', '-m', 'format_and_lint', f.name],
                capture_output=True
            )

            assert result.returncode == 0
            with open(f.name) as rf:
                content = rf.read()
                assert 'x = 1' in content or content.strip() == ''

        os.unlink(f.name)

    def test_language_detection(self):
        """Test language detection."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create test files
            Path(tmpdir, 'test.py').write_text('print("hi")')
            Path(tmpdir, 'test.js').write_text('console.log("hi")')

            result = subprocess.run(
                ['python', '-m', 'format_and_lint', '--detect', tmpdir],
                capture_output=True,
                text=True
            )

            assert 'Python' in result.stdout
            assert 'JavaScript' in result.stdout
```

Run tests:
```bash
pytest tests/test_format_lint.py -v
```

---

## Manual QA Checklist

Before release, verify:

- [ ] All 10 test cases pass
- [ ] Performance test < 30 seconds for 100 files
- [ ] No regressions from previous version
- [ ] Documentation accurate
- [ ] Code examples work as documented
- [ ] Error messages clear and helpful
- [ ] Pre-commit hook installation works
- [ ] Config file templates valid
- [ ] Works on macOS, Linux, Windows
- [ ] Handles all documented languages

