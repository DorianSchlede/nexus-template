# Best Practices - Format and Lint Code

Guidelines and patterns for effective code formatting and linting workflows.

## General Principles

### 1. Format Before Lint

Run formatters first, then linters. Formatters fix style automatically, reducing false linting warnings.

```bash
# Good: Format first
black *.py && flake8 *.py

# Worse: Lint then format
flake8 *.py && black *.py  # black will undo flake8 analysis
```

### 2. Configure Project Defaults

Add configuration files to version control so all contributors use the same rules.

```bash
# Recommended files to commit
.format-config.yaml
.prettierrc.json
.eslintrc.json
.pylintrc
.flake8
.yamllint
.markdownlint.json
.git/hooks/pre-commit  # or use package like pre-commit
```

### 3. Use Pre-commit Hooks

Prevent commits with formatting/linting issues before they reach the repository.

```bash
# Install hook
format code --install-hook

# Automatically runs before each commit
git commit -m "message"
# → Hook runs formatters and linters
# → Blocks if errors found
```

### 4. Exclude Non-Critical Files

Don't lint generated, vendor, or dependency files.

```yaml
# .format-config.yaml
exclude:
  - "**/node_modules/**"
  - "**/venv/**"
  - "**/build/**"
  - "**/dist/**"
  - "**/vendor/**"
  - "**/.git/**"
  - "**/migrations/**"
```

### 5. Start Strict, Relax Only When Needed

Begin with strict rules, disable specific rules only with justification.

```python
# Good: Explicit disable with reason
# pylint: disable=too-many-arguments
def process_data(a, b, c, d, e, f, g):
    """Process data with many params for legacy compatibility."""
    ...

# Avoid: Blanket disables
# pylint: disable=all
```

---

## Language-Specific Best Practices

### Python

#### Line Length

**Recommendation**: 100 characters

Why 100 over 79?
- Modern monitors are wider
- 79 is Python 3 default but 100 is industry standard
- Balances readability with legacy flexibility

```python
# ✓ Good: Respects 100-char limit
result = some_function(param1, param2, param3)

# ✗ Avoid: Unnecessary split at 79
result = some_function(
    param1,
    param2,
    param3,
)
```

#### Import Organization

Use `isort` with Black-compatible profile:

```toml
[tool.isort]
profile = "black"
line_length = 100
multi_line_mode = 3  # Vertical Hanging Indent
```

Order:
1. Standard library
2. Third-party
3. Local application

```python
# Standard library
import os
import sys

# Third-party
import requests
import pandas as pd

# Local
from myapp import utils
```

#### Docstrings

Use Google style for consistency:

```python
def process_data(items: List[str]) -> Dict[str, Any]:
    """Process a list of items.

    Args:
        items: List of item identifiers.

    Returns:
        Dictionary mapping items to processed results.

    Raises:
        ValueError: If items list is empty.
    """
    if not items:
        raise ValueError("Items cannot be empty")
    ...
```

#### String Quotes

Choose and stick with one style:

```python
# Black default: Double quotes
message = "Hello world"

# Alternatively: Single quotes
message = 'Hello world'

# Not both!
message = "Hello" + 'world'  # ✗ Inconsistent
```

---

### JavaScript/TypeScript

#### Line Width

**Recommendation**: 100 characters

```javascript
// ✓ Good: Under 100 chars
const result = fetchData(userId, startDate, endDate);

// ✗ Avoid: Unnecessary breaks
const result = fetchData(
  userId,
  startDate,
  endDate
);
```

#### Semicolons

**Recommendation**: Always use semicolons

```javascript
// ✓ Good: Explicit semicolons
const name = 'John';
const age = 30;

// Avoid: ASI (Automatic Semicolon Insertion) issues
const name = 'John'
const age = 30  // Can cause issues
```

#### Trailing Commas

**Recommendation**: Use trailing commas (helps with git diffs)

```javascript
// ✓ Good: Trailing comma
const obj = {
  name: 'John',
  age: 30,
};

// Diff shows clearer intent:
// + age: 30,
// + city: 'NYC',

// Without trailing comma:
// - age: 30
// + age: 30,
// + city: 'NYC',
```

#### Arrow Function Parentheses

**Recommendation**: Always use parentheses

```javascript
// ✓ Consistent
const numbers = [1, 2, 3].map((x) => x * 2);

// ✗ Inconsistent
const numbers = [1, 2, 3].map(x => x * 2);
```

#### Import/Export Ordering

```javascript
// 1. External packages
import React from 'react';
import axios from 'axios';

// 2. Internal components
import Header from './Header';
import Footer from './Footer';

// 3. Utils
import { formatDate } from './utils';

// 4. Styles
import styles from './App.css';
```

---

### YAML

#### Indentation

**Recommendation**: 2 spaces (not tabs)

```yaml
# ✓ Good
services:
  api:
    port: 3000
    debug: true

# ✗ Bad: 4 spaces
services:
    api:
        port: 3000
```

#### Line Length

**Recommendation**: 120 characters max

```yaml
# ✓ Good: Under 120
description: "Process data from external source and store in database"

# Can be one line for short values
name: api-service
port: 3000
```

#### Comments

Use comments for non-obvious configuration:

```yaml
# Database connection
database:
  host: localhost
  # Maximum connections to prevent resource exhaustion
  max_connections: 100
  # Must be at least 16 for security
  min_password_length: 16
```

---

### Go

#### Line Length

**Recommendation**: 100 characters (Go convention: actual code, not 80)

#### Naming

```go
// ✓ Good: Clear, idiomatic names
func (u *User) String() string {
    return fmt.Sprintf("%s (%d)", u.Name, u.Age)
}

// Interface names end with -er
type Reader interface {
    Read(p []byte) (n int, err error)
}
```

#### Error Handling

```go
// ✓ Good: Explicit error handling
if err != nil {
    return fmt.Errorf("failed to read file: %w", err)
}

// Package-level context
if err != nil {
    log.Fatal(err)
}
```

---

### Rust

#### Line Length

**Recommendation**: 100 characters

```toml
[target.rustfmt]
edition = "2021"
max_width = 100
```

#### Doc Comments

Use `///` for public APIs:

```rust
/// Processes user data and returns result.
///
/// # Arguments
/// * `user_id` - The ID of the user to process
///
/// # Returns
/// A Result containing the processed data or an error
pub fn process_user(user_id: u32) -> Result<Data, Error> {
    // ...
}
```

---

## Workflow Integration

### Before Committing

```bash
# 1. Format code
format code --all

# 2. Review changes
git diff

# 3. Stage if happy
git add .

# 4. Commit (hook will run checks)
git commit -m "feat: add user authentication"
```

### During Code Review

```bash
# Mention code style in reviews
"Run `format code --file src/auth.ts` to fix formatting"

# Don't discuss style if it can be automated
# Use `format code --install-hook` to prevent future issues
```

### CI/CD Integration

```yaml
# .github/workflows/lint.yml
name: Lint and Format

on: [pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run format and lint
        run: format code --all --strict
```

---

## Common Issues and Fixes

### Issue 1: Conflicting Rules

**Problem**: Black wants line length 100, ESLint wants 80

**Solution**: Align line length across all tools

```json
// .prettierrc.json
{
  "printWidth": 100
}
```

```ini
# .flake8
max-line-length = 100
```

```toml
# pyproject.toml
[tool.black]
line-length = 100
```

### Issue 2: Tool-Specific Disables Scattered

**Problem**: `# noqa`, `# pylint: disable`, `# eslint-disable` everywhere

**Solution**: Disable at configuration level when possible

```ini
# .flake8 - disable in config instead of code
extend-ignore = E203, W503
```

### Issue 3: Pre-commit Hook Blocking Legitimate Code

**Problem**: Emergency hotfix is blocked by style formatting

**Solution**: Override when necessary

```bash
# Bypass pre-commit hook (only when necessary!)
git commit --no-verify -m "hotfix: critical bug"
```

### Issue 4: Different Styles Across Team

**Problem**: Mix of spaces/tabs, single/double quotes

**Solution**: Commit `.format-config.yaml` and run `format code --all` before first commit

```bash
# On new project setup
cp .format-config.yaml.template .format-config.yaml
format code --all
git add . && git commit -m "style: format entire codebase"
```

---

## Team Guidelines

### When Formatting is Done

- ✓ Before committing (via pre-commit hook)
- ✓ In CI/CD pipeline (blocking on failure)
- ✓ Before code review (reduce reviewer burden)
- ✓ Automated (no manual debates about style)

### When NOT to Format

- ✗ Don't use `--no-verify` casually
- ✗ Don't have mixed formatters (black AND autopep8)
- ✗ Don't commit unformatted code to main

### Review Checklist

```markdown
- [ ] Code is formatted (run `format code --all`)
- [ ] No linting errors (ESLint/Flake8 pass)
- [ ] Imports are sorted (isort/import-sort)
- [ ] Configuration is committed (.format-config.yaml)
```

---

## Performance Tips

### 1. Format Only Changed Files

```bash
# Faster: Only staged files
format code --staged

# Slower: Entire project
format code --all
```

### 2. Run Formatters in Parallel

```bash
# Slow: Sequential
black . && prettier . && isort .

# Fast: Parallel (in script)
black . & prettier . & isort . & wait
```

### 3. Cache Lint Results

Tools like ESLint support caching:

```bash
eslint --cache .  # Uses .eslintcache
```

---

## Next Steps

1. **Review your project**: Do you have consistent style rules?
2. **Install hooks**: Run `format code --install-hook`
3. **Configure tools**: Copy `.format-config.yaml.template` and customize
4. **Test locally**: Run `format code --all` on a branch
5. **Update CI/CD**: Add format checks to pipeline

