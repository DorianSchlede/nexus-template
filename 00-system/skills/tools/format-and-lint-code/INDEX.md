# Format and Lint Code Skill - Complete Index

Quick navigation guide for all skill files and documentation.

## Main Files

### Start Here
- **[README.md](README.md)** - Quick overview and getting started (5 min read)
- **[SKILL.md](SKILL.md)** - Complete skill workflow and instructions (15 min read)
- **[BUILD-SUMMARY.md](BUILD-SUMMARY.md)** - Summary of what was created (10 min read)

---

## For Different Users

### I want to USE this skill
1. Read: [README.md](README.md) (overview)
2. Read: [references/installation-guide.md](references/installation-guide.md) (setup)
3. Copy: [templates/.format-config.yaml.template](templates/.format-config.yaml.template)
4. Run: `format and lint code`

**Time to productive**: ~15 minutes

---

### I want to UNDERSTAND best practices
1. Read: [references/best-practices.md](references/best-practices.md)
   - Python guidelines (line length, imports, docstrings)
   - JavaScript/TypeScript guidelines (semicolons, commas, quotes)
   - Language-specific recommendations
   - Team workflows

2. Customize: [templates/.format-config.yaml.template](templates/.format-config.yaml.template)

**Time**: ~30 minutes

---

### I want to INSTALL tools for my language

**Python**:
```bash
pip install black flake8 pylint isort
```
See: [references/installation-guide.md](references/installation-guide.md#python)

**JavaScript/TypeScript**:
```bash
npm install -g prettier eslint
```
See: [references/installation-guide.md](references/installation-guide.md#javascripttypescript)

**Go**:
```bash
go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest
```
See: [references/installation-guide.md](references/installation-guide.md#go)

See [references/installation-guide.md](references/installation-guide.md) for all 9 languages.

---

### I want to INTEGRATE with my project

1. Copy config template:
   ```bash
   cp templates/.format-config.yaml.template .format-config.yaml
   ```

2. Edit `.format-config.yaml` with your project settings

3. Test locally:
   ```bash
   format and lint code --all
   ```

4. Install pre-commit hook (optional):
   ```bash
   format code --install-hook
   ```

See: [SKILL.md - Step 3: Pre-Commit Integration](SKILL.md#step-7-pre-commit-integration)

---

### I want to TEST this skill

See: [references/testing-guide.md](references/testing-guide.md)

Includes:
- 10 detailed test cases
- Performance benchmarks
- Automated pytest examples
- Regression test suite
- QA checklist

**Time to complete all tests**: ~2 hours

---

### I want to DEVELOP or EXTEND this skill

**Architecture**:
- [scripts/format_and_lint.py](scripts/format_and_lint.py) - Core Python implementation
  - `LanguageDetector` class - Detects languages and files
  - `ToolRunner` class - Executes formatters and linters

**Add new language**:
1. Add to `LANGUAGE_EXTENSIONS` dict in `format_and_lint.py`
2. Add tool handlers in `ToolRunner` class
3. Add configuration section in `.format-config.yaml.template`
4. Document in `best-practices.md`
5. Add test cases in `testing-guide.md`

**Add new tool**:
1. Implement `_run_{tool}()` method in `ToolRunner`
2. Handle tool-specific output format
3. Update tool availability in `TOOLS` dict
4. Add installation instructions in `installation-guide.md`

---

## File Reference

### Core Skill Definition
```
├── SKILL.md                          (The main skill - user interaction flow)
├── README.md                         (Quick start guide)
└── INDEX.md                          (This file)
```

### Implementation
```
scripts/
└── format_and_lint.py                (Python engine - 379 lines)
    ├── LanguageDetector              (Detects languages)
    ├── ToolRunner                    (Executes tools)
    └── generate_summary()            (Output formatting)
```

### Configuration Templates
```
templates/
├── .format-config.yaml.template      (Project configuration)
└── pre-commit.hook.template          (Git hook)
```

### Documentation
```
references/
├── installation-guide.md             (Setup for 9 languages)
├── best-practices.md                 (Professional guidelines)
├── testing-guide.md                  (Test suite & QA)
└── BUILD-SUMMARY.md                  (What was built)
```

---

## Supported Languages

| Language | Formatter | Linters | Guide |
|----------|-----------|---------|-------|
| Python | Black | Flake8, Pylint | [Install](references/installation-guide.md#python) • [Best Practices](references/best-practices.md#python) |
| JavaScript | Prettier | ESLint | [Install](references/installation-guide.md#javascripttypescript) • [Best Practices](references/best-practices.md#javascripttypescript) |
| TypeScript | Prettier | ESLint | [Install](references/installation-guide.md#javascripttypescript) • [Best Practices](references/best-practices.md#javascripttypescript) |
| Go | gofmt | golangci-lint | [Install](references/installation-guide.md#go) • [Best Practices](references/best-practices.md#go) |
| Rust | rustfmt | clippy | [Install](references/installation-guide.md#rust) • [Best Practices](references/best-practices.md#rust) |
| JSON | Prettier | jsonlint | [Install](references/installation-guide.md#json) |
| YAML | Prettier | yamllint | [Install](references/installation-guide.md#yaml) • [Best Practices](references/best-practices.md#yaml) |
| Markdown | Prettier | markdownlint | [Install](references/installation-guide.md#markdown) |
| Shell | shfmt | shellcheck | [Install](references/installation-guide.md#shell) |

---

## Quick Commands

```bash
# Detect languages and tools
format and lint code

# Format only staged git files (fast)
format and lint --staged

# Format specific directory
format and lint --files src/

# Format all files
format and lint code --all

# Interactive mode (prompt for each issue)
format and lint code --interactive

# Show detailed report
format and lint code --report

# Install pre-commit hook
format code --install-hook

# Run linting only (no formatting)
lint code --all

# Run formatting only
format code --all
```

---

## Common Scenarios

### Scenario 1: New Python Project
```bash
1. pip install black flake8 pylint isort
2. cp templates/.format-config.yaml.template .format-config.yaml
3. # Edit .format-config.yaml to customize
4. format and lint code --all
5. format code --install-hook
```

### Scenario 2: Existing Project with Mixed Languages
```bash
1. Install tools for each language (see installation-guide.md)
2. Copy config template
3. Edit to exclude node_modules, venv, etc.
4. Run: format and lint code --all
5. Commit .format-config.yaml
6. Set up CI/CD formatting checks
```

### Scenario 3: Pre-commit Hook for Team
```bash
1. Create .format-config.yaml in repo root
2. Commit to version control
3. Add to onboarding: "Run 'format code --install-hook'"
4. All developers have consistent formatting
```

### Scenario 4: Automated Formatting in CI
```bash
1. Add to CI pipeline:
   format and lint code --all --strict
2. Fail build if formatting errors found
3. Optional: Auto-commit fixes to PR
```

---

## Troubleshooting

### Tool Not Found
→ See: [references/installation-guide.md](references/installation-guide.md#troubleshooting)

### Configuration Not Working
→ See: [references/best-practices.md#issue-1-conflicting-rules](references/best-practices.md#issue-1-conflicting-rules)

### Pre-commit Hook Not Running
→ See: [SKILL.md - Error Handling](SKILL.md#error-handling)

### Performance Issues
→ See: [references/best-practices.md#performance-tips](references/best-practices.md#performance-tips)

### Language Not Supported
→ Contribute: [Add new language to format_and_lint.py](scripts/format_and_lint.py)

---

## Reading Order Recommendations

### For First-Time Users (30 minutes)
1. This INDEX (5 min)
2. [README.md](README.md) (10 min)
3. [references/installation-guide.md](references/installation-guide.md) - your language section (10 min)
4. Copy template and run

### For Team Leads (1 hour)
1. [README.md](README.md)
2. [SKILL.md](SKILL.md)
3. [references/best-practices.md](references/best-practices.md)
4. [BUILD-SUMMARY.md](BUILD-SUMMARY.md) - Architecture section

### For Developers (45 minutes)
1. [README.md](README.md)
2. [references/best-practices.md](references/best-practices.md) - your language section
3. [templates/.format-config.yaml.template](templates/.format-config.yaml.template)
4. Start using!

### For QA/Testing (2+ hours)
1. [references/testing-guide.md](references/testing-guide.md)
2. Run all test cases
3. File issues if any fail

### For Maintainers (2+ hours)
1. [BUILD-SUMMARY.md](BUILD-SUMMARY.md)
2. [scripts/format_and_lint.py](scripts/format_and_lint.py)
3. [references/testing-guide.md](references/testing-guide.md)
4. Review architecture and extend as needed

---

## Key Statistics

| Metric | Count |
|--------|-------|
| Total files | 9 |
| Lines of documentation | ~2,000 |
| Lines of Python code | 379 |
| Supported languages | 9 |
| Supported tools | 20+ |
| Configuration options | 50+ |
| Test cases | 10 |
| Installation guides | 9 |
| Code examples | 30+ |

---

## Next Steps

Choose your path:

- **Quick Start**: [README.md](README.md)
- **Install Tools**: [references/installation-guide.md](references/installation-guide.md)
- **Learn Best Practices**: [references/best-practices.md](references/best-practices.md)
- **Test Everything**: [references/testing-guide.md](references/testing-guide.md)
- **Understand Architecture**: [BUILD-SUMMARY.md](BUILD-SUMMARY.md)
- **View Complete Workflow**: [SKILL.md](SKILL.md)

---

**Status**: ✅ Skill ready for immediate use

**Version**: 1.0 (2026-01-07)

**Support**: Check troubleshooting sections in README.md and SKILL.md

