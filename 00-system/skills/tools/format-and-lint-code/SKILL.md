---
name: format-and-lint-code
description: "format code, lint code, pre-commit, before commit, code quality, auto-format"
---

# Format and Lint Code

Automatically formats and lints code before commits to maintain consistency and code quality.

## Purpose

Catch formatting issues and linting errors before they reach version control. Supports multiple languages and can be run manually or integrated into pre-commit hooks.

---

## Workflow

### Step 1: Initialize and Analyze

Ask user for context:
```
Which files should I format and lint?

Options:
1. All staged files (git status)
2. All files in a directory
3. Specific file list
4. All code files in build
```

### Step 2: Detect Languages and Tools

Based on file extensions, determine available tools:

**Supported Languages:**
- Python (black, flake8, isort, pylint)
- JavaScript/TypeScript (prettier, eslint)
- Go (gofmt, golint)
- Rust (rustfmt, clippy)
- JSON (prettier, jsonlint)
- YAML (yamllint)
- Markdown (markdownlint)
- Shell (shellcheck, shfmt)

Display detected tools:
```
📦 Detected Tools:
[OK] Python: black, flake8, isort
[OK] JavaScript: prettier, eslint
[OK] YAML: yamllint
```

### Step 3: Run Formatting

For each language/tool combination:

1. **Format (non-breaking)**
   - Run formatter with minimal configuration
   - Apply changes to files
   - Report what changed

```
🎨 Formatting...
[OK] Black: 3 files formatted (45 lines changed)
[OK] Prettier: 2 files formatted (18 lines changed)
[OK] isort: 3 files reformatted
```

### Step 4: Run Linting

For each language/tool:

1. **Lint and categorize issues**
   - Errors (must fix)
   - Warnings (should fix)
   - Info (nice to fix)

```
🔍 Linting Results:

ERRORS (must fix - 2):
  main.py:45:  E501 line too long (105 > 100)
  app.js:12:   SyntaxError near undefined

WARNINGS (should fix - 5):
  utils.py:8:   W503 line break before binary operator
  types.ts:22:  @typescript-eslint/no-explicit-any

INFO (nice to fix - 3):
  config.yaml:1: Comment formatting
```

### Step 5: Interactive Fix Suggestions

For each error/warning:

```
Fix suggestion for main.py:45?

Error: Line too long
Current:
  result = some_very_long_function_name(param1, param2, param3, param4)

Suggestion:
  result = some_very_long_function_name(
      param1, param2, param3, param4
  )

[auto] [ignore] [skip] [manual]
```

Options:
- `[auto]` - Apply automatic fix
- `[ignore]` - Mark as acknowledged but don't fix
- `[skip]` - Continue to next issue
- `[manual]` - Show file location for manual fix

### Step 6: Apply Fixes

Based on user selections:

```
Applying fixes...
[OK] Fixed 2 errors (auto-fixed)
[!] Flagged 5 warnings (acknowledged)
[INFO] Noted 3 info items
```

Generate summary:
```
Fixed Files:
- main.py (2 fixes)
- app.js (3 fixes)
- utils.py (1 acknowledged warning)

Remaining Issues:
- types.ts:22 - @typescript-eslint/no-explicit-any (flagged, not auto-fixable)
```

### Step 7: Pre-Commit Integration

Ask:
```
Ready to commit?

Options:
1. Stage fixed files and commit
2. Show diff before staging
3. Just format/lint without staging
4. Create pre-commit hook
```

**Option 1 - Stage & Commit:**
```
git add [formatted_files]
git commit -m "style: auto-format and lint code"
```

**Option 2 - Show Diff:**
```
Display git diff for each file
Ask: "Stage these changes? (yes/no)"
```

**Option 3 - No Staging:**
```
Files formatted. Run 'git add .' when ready.
```

**Option 4 - Install Hook:**
```
Create .git/hooks/pre-commit script that:
1. Runs format-and-lint on staged files
2. Blocks commit if errors found
3. Auto-fixes warnings
4. Allows manual override

Installation complete! Formatter will run automatically before commits.
```

---

## Configuration

### Default Settings

Create `.format-config.yaml` in build root:

```yaml
format_and_lint:
  # File patterns to include
  include:
    - "**/*.py"
    - "**/*.js"
    - "**/*.ts"
    - "**/*.json"
    - "**/*.yaml"

  # File patterns to skip
  exclude:
    - "**/node_modules/**"
    - "**/venv/**"
    - "**/.git/**"
    - "**/build/**"
    - "**/dist/**"

  # Tools configuration
  python:
    formatter: black
    max_line_length: 100
    linters: [flake8, pylint]

  javascript:
    formatter: prettier
    print_width: 100
    linters: [eslint]

  auto_fix: true  # Auto-fix fixable issues
  interactive: true  # Prompt for non-auto-fixable issues
```

### Tool-Specific Config

Respect existing config files in build:
- `pyproject.toml` / `setup.cfg` (Python)
- `.prettierrc` / `.eslintrc` (JavaScript)
- `golangci.yml` (Go)
- `rustfmt.toml` (Rust)
- `.yamllint` (YAML)

---

## Available Commands

**Run formatter only:**
```
format code --files [pattern]
```

**Run linter only:**
```
lint code --files [pattern]
```

**Format and lint:**
```
format and lint code
format and lint --files src/
format and lint --staged  # staged git files only
```

**Install pre-commit hook:**
```
format code --install-hook
```

**Generate report:**
```
format and lint --report  # Shows summary of all files
```

---

## Integration with Other Workflows

### Before Commits
```
git commit -m "message"
→ pre-commit hook runs format-and-lint
→ Blocks commit if errors found
→ User chooses: fix, override, or cancel commit
```

### In CI/CD
```
ci-lint job:
  - Runs linter in strict mode (warnings = errors)
  - Fails if issues found
  - Reports failures per file
  - Blocks merge if not passing
```

### In Builds
When used with execute-build skill:
```
Before ending build phase:
→ format and lint code --all
→ Verify all outputs are formatted
→ Add to final deliverables
```

---

## Error Handling

**If no tools detected:**
```
[!] No formatters/linters found for this language.

Detected files:
- .xaml (unsupported)
- .gradle (unsupported)

To add support:
1. Install tool: pip install [tool]
2. Add to .format-config.yaml
3. Retry
```

**If tool install fails:**
```
[ERROR] Could not install black

Options:
1. Install manually: pip install black
2. Skip this tool and continue
3. Abort
```

**If file cannot be parsed:**
```
[!] Skipped: main.js - Syntax error

Options:
1. Show syntax error details
2. Skip and continue
3. Manually fix and retry
```

---

## Notes

- Safe: All changes shown before applying
- Reversible: Can undo with git
- Customizable: Per-build configuration
- Efficient: Only processes changed files when possible
- Intelligent: Skips binary files automatically

---

## Next Steps

- **Single file?** → `format code --file path/to/file.py`
- **Whole build?** → `format code --all`
- **Pre-commit hook?** → `format code --install-hook`
- **Custom rules?** → Edit `.format-config.yaml`

