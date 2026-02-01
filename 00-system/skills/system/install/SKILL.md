# /install - Nexus Installation & Validation

## Overview
Validates the Nexus installation, reports on setup status, and helps resolve any issues. Combines deterministic setup scripts with intelligent validation and troubleshooting.

## Arguments
- `--interactive` or `-i`: Enable human-in-the-loop mode for guided setup

## Workflow

### Step 1: Check for Interactive Mode
```
IF arguments contain "--interactive" or "-i":
    → Execute interactive installation workflow (see below)
    → STOP here, do not continue to Step 2
```

### Step 2: Read Installation Log
Read the installation log to understand what the setup hook did:
```
File: .claude/logs/install.log
```

If the log doesn't exist, inform the user they should run `just init` or `claude --init` first.

### Step 3: Validate Installation
Verify each component is properly installed:

**Prerequisites:**
- [ ] Python 3.x available
- [ ] uv package manager available
- [ ] Git available

**Nexus Structure:**
- [ ] `00-system/core/orchestrator.md` exists
- [ ] `01-memory/` directory exists
- [ ] `02-builds/` directory exists
- [ ] `00-system/skills/` directory exists

**Python Environment:**
- [ ] `pyproject.toml` exists
- [ ] Dependencies installed (check with `uv sync --dry-run`)

**CLI Tools:**
- [ ] `nexus-session-start` command available
- [ ] `nexus-post-tool-use` command available

### Step 4: Generate Report
Create a summary document at `.claude/logs/install-report.md`:

```markdown
# Nexus Installation Report
Generated: [timestamp]

## Status: [SUCCESS | PARTIAL | FAILED]

## Prerequisites
- Python: [version or missing]
- uv: [version or missing]
- Git: [version or missing]

## Nexus Components
[List each component with [OK] or [FAIL]]

## Issues Found
[List any problems]

## Recommended Actions
[Steps to fix any issues]
```

### Step 5: Report to User
Display the installation status clearly:
- If all checks pass: Confirm success
- If issues found: Explain each issue and how to fix it

---

## Interactive Installation Workflow

When `--interactive` is specified, guide the user through setup with questions:

### Question Set 1: Environment
Ask the user:
1. "Have you installed Python 3.8+ on this machine?"
2. "Have you installed the uv package manager?"
3. "Do you want me to attempt automatic installation of missing tools?"

### Question Set 2: Configuration
After prerequisites are confirmed:
1. "What is your preferred text editor for Nexus files?" (VS Code / Other)
2. "Would you like to configure VS Code settings for markdown preview?"

### Question Set 3: Verification
After installation steps:
1. "Should I run a test to verify everything works?"
2. "Do you want me to display the Nexus main menu after setup?"

### Interactive Flow
```
FOR each question set:
    → Ask questions using AskUserQuestion tool
    → Process responses
    → Run relevant setup steps
    → Report progress
    → Move to next set
```

---

## Common Issues & Solutions

### Problem: uv not found
**Solution:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
Then restart terminal or source shell config.

### Problem: Python dependencies fail
**Solution:**
```bash
uv sync --reinstall
```

### Problem: CLI tools not found
**Solution:**
```bash
uv tool install . --force
```
Ensure `~/.local/bin` is in PATH.

### Problem: Nexus structure incomplete
**Solution:**
Verify this is a valid Nexus clone. If files are missing, re-clone:
```bash
git clone https://github.com/DorianSchlede/nexus-template.git
```

---

## Exit Conditions
- **Success**: All checks pass, report generated
- **Partial**: Some checks fail but Nexus is usable
- **Failed**: Critical components missing

Always end by asking if the user needs help with any specific issue.
