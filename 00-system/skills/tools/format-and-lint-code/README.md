# Format and Lint Code Skill

Automatically formats and lints code across multiple languages before commits.

## Overview

This Nexus skill provides an integrated workflow for:
- **Formatting**: Automatic code style fixes (Black, Prettier, gofmt, rustfmt)
- **Linting**: Code quality checks and warnings (ESLint, Flake8, Pylint)
- **Pre-commit Integration**: Optional automatic checks before committing
- **Multi-language Support**: Python, JavaScript, TypeScript, Go, Rust, JSON, YAML, Shell

## Quick Start

### 1. Install Tools

Choose formatters/linters for your languages:

```bash
# Python
pip install black flake8 pylint isort

# JavaScript/TypeScript
npm install -g prettier eslint

# See references/installation-guide.md for all languages
```

### 2. Run in Current Project

```bash
# Format and lint all files
format and lint code

# Format only staged git files
format and lint --staged

# Format specific directory
format and lint --files src/
```

### 3. Install Pre-Commit Hook (Optional)

```bash
format code --install-hook
```

Now formatting and linting runs automatically before each commit.

## Workflow

The skill follows this process:

```
Analyze Project
    ↓
Detect Languages
    ↓
Run Formatters
    ↓
Run Linters
    ↓
Show Results
    ↓
Interactive Fixes
    ↓
Stage & Commit (Optional)
```

## Features

### Language Detection

Automatically detects languages in your project:

```
📦 Detected Tools:
✓ Python: black, flake8, isort (3 files)
✓ JavaScript: prettier, eslint (2 files)
✓ YAML: yamllint (1 file)
```

### Formatting

Automatic fixes for:
- Line length violations
- Indentation inconsistencies
- Quote style (single vs double)
- Trailing whitespace
- Import organization
- Bracket spacing
- And more...

### Linting

Catches issues like:
- Unused variables
- Missing docstrings
- Type errors
- Complex code
- Security issues
- Style violations
- And more...

### Interactive Fixes

For non-auto-fixable issues:

```
⚠ Warning: Line too long (105 > 100)

Current:
  result = some_very_long_function_name(param1, param2, param3)

Suggestion:
  result = some_very_long_function_name(
      param1, param2, param3
  )

[auto-fix] [ignore] [skip] [manual]
```

## Configuration

### Project Configuration

Create `.format-config.yaml` in your project root:

```yaml
format_and_lint:
  include:
    - "**/*.py"
    - "**/*.js"
    - "**/*.ts"

  exclude:
    - "**/node_modules/**"
    - "**/venv/**"
    - "**/.git/**"

  python:
    formatter: black
    max_line_length: 100
    linters: [flake8, pylint]

  javascript:
    formatter: prettier
    print_width: 100
    linters: [eslint]
```

See `templates/.format-config.yaml.template` for complete configuration options.

### Tool-Specific Config

Respect existing configuration files:
- `pyproject.toml` (Python - Black, isort)
- `setup.cfg` (Python - Flake8)
- `.prettierrc.json` (JavaScript/TypeScript)
- `.eslintrc.json` (JavaScript/TypeScript)
- `.flake8` (Python)
- `.yamllint` (YAML)
- `rustfmt.toml` (Rust)

## Usage Examples

### Format All Code

```bash
format and lint code

# Options:
# --all              : All files
# --staged           : Git staged files only
# --files [pattern]  : Specific files/directories
```

### Format Before Commit

```bash
# Option 1: Manual check before commit
format code --files .
git diff  # review changes
git add .
git commit -m "message"

# Option 2: Automatic via pre-commit hook
format code --install-hook
git commit -m "message"  # hook runs automatically
```

### CI/CD Integration

```yaml
# .github/workflows/lint.yml
name: Code Quality

on: [pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run format and lint
        run: format and lint code --all --strict
```

### Fix Issues in Specific File

```bash
format code --file src/auth.ts

# Shows issues, prompts for fixes
# Applies fixes to that file only
```

### Generate Report

```bash
format and lint code --report

# Outputs summary of all issues by file and type
```

## Understanding Output

### Formatting Results

```
🎨 Formatting...
✓ Black: 3 files formatted (45 lines changed)
✓ Prettier: 2 files formatted (18 lines changed)
✓ isort: 3 files reformatted (9 imports organized)
```

### Linting Results

```
🔍 Linting Results:

ERRORS (must fix - 2):
  main.py:45:  E501 line too long (105 > 100)
  app.js:12:   SyntaxError: Unexpected token

WARNINGS (should fix - 5):
  utils.py:8:   W503 line break before binary operator
  types.ts:22:  @typescript-eslint/no-explicit-any

INFO (nice to fix - 3):
  config.yaml:1: Comment formatting
```

### Summary

```
Summary of Changes:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Files Formatted:
  ✓ src/main.py (2 fixes)
  ✓ src/app.js (3 fixes)
  ✓ config.yaml (1 fix)

Remaining Issues:
  ⚠ types.ts:22 - needs explicit type annotation
  ⚠ handler.py:15 - complexity warning (flagged)

Total: 6 auto-fixed, 5 flagged, 0 errors
```

## Supported Languages

| Language | Formatter | Linters | Version |
|----------|-----------|---------|---------|
| Python | Black | Flake8, Pylint, PyRight | py3.7+ |
| JavaScript | Prettier | ESLint | ES2020+ |
| TypeScript | Prettier | ESLint | 4.0+ |
| Go | gofmt | golangci-lint | 1.16+ |
| Rust | rustfmt | clippy | 1.56+ |
| JSON | Prettier | jsonlint | - |
| YAML | Prettier | yamllint | - |
| Markdown | Prettier | markdownlint | - |
| Shell | shfmt | shellcheck | - |

## Pre-Commit Hook

Automatically runs format/lint checks before commits:

```bash
# Install hook
format code --install-hook

# From then on, every commit triggers:
$ git commit -m "feature: add auth"
Running format and lint checks...
✓ All checks passed! ✓
[main a1b2c3d] feature: add auth
```

If issues are found:

```bash
Running format and lint checks...
❌ Some checks failed

Errors found in:
  src/api.py - 2 formatting issues

Options:
1. Review and fix manually
2. Run 'format and lint --fix' to auto-fix
3. Use 'git commit --no-verify' to skip (not recommended!)
```

## File Structure

```
format-and-lint-code/
├── SKILL.md                    # Main skill definition
├── README.md                   # This file
├── scripts/
│   └── format_and_lint.py      # Main Python script
├── templates/
│   ├── .format-config.yaml.template
│   └── pre-commit.hook.template
└── references/
    ├── installation-guide.md   # Complete setup instructions
    ├── best-practices.md       # Guidelines and patterns
    └── [config examples]
```

## Troubleshooting

### Tool Not Found

```bash
# Python: Install with pip
pip install black flake8 pylint isort

# JavaScript: Install with npm
npm install -g prettier eslint

# See installation-guide.md for complete setup
```

### Pre-commit Hook Not Running

```bash
# Make hook executable
chmod +x .git/hooks/pre-commit

# Test hook manually
.git/hooks/pre-commit
```

### Conflicting Rules

**Problem**: Different tools have conflicting configuration

**Solution**: Align settings in `.format-config.yaml`

```yaml
python:
  black:
    line_length: 100
flake8:
  max_line_length: 100  # Must match black
```

### Want to Skip Hook for Emergency Fix

```bash
# Bypass pre-commit hook (use sparingly!)
git commit --no-verify -m "hotfix: critical bug"
```

## Next Steps

1. **Install tools**: `pip install black flake8` (or your languages)
2. **Copy config**: `cp templates/.format-config.yaml.template .format-config.yaml`
3. **Test locally**: `format and lint code`
4. **Install hook**: `format code --install-hook`
5. **Commit config**: `git add .format-config.yaml && git commit`

## Learn More

- **Installation**: See `references/installation-guide.md`
- **Best Practices**: See `references/best-practices.md`
- **Configuration**: See `templates/.format-config.yaml.template`

## Support

For issues with specific tools:
- Black: https://black.readthedocs.io/
- Prettier: https://prettier.io/
- ESLint: https://eslint.org/
- Flake8: https://flake8.pycqa.org/

