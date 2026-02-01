# /maintain - Nexus Codebase Maintenance

## Overview
Validates maintenance operations, runs health checks, and helps keep the Nexus codebase clean and up-to-date. Combines deterministic maintenance scripts with intelligent analysis.

## Arguments
- `--interactive` or `-i`: Enable human-in-the-loop mode for guided maintenance

## Workflow

### Step 1: Check for Interactive Mode
```
IF arguments contain "--interactive" or "-i":
    → Execute interactive maintenance workflow (see below)
    → STOP here, do not continue to Step 2
```

### Step 2: Read Maintenance Log
Read the maintenance log to understand what the maintenance hook did:
```
File: .claude/logs/maintenance.log
```

If the log doesn't exist, inform the user they should run `just maintenance` or `claude --maintenance` first.

### Step 3: Additional Health Checks
Run checks beyond what the deterministic script does:

**Git Status:**
- Any uncommitted changes?
- Is the branch up to date with remote?
- Any stale branches to clean up?

**Dependency Health:**
- Are there any security vulnerabilities in dependencies?
- Are major version updates available?

**Nexus-Specific:**
- Any orphaned build directories?
- Is user-config.yaml valid?
- Are there stale session files?

**Disk Usage:**
- How much space is the .claude directory using?
- Are there large files that shouldn't be tracked?

### Step 4: Generate Report
Create a summary document at `.claude/logs/maintenance-report.md`:

```markdown
# Nexus Maintenance Report
Generated: [timestamp]

## Status: [HEALTHY | NEEDS_ATTENTION | ACTION_REQUIRED]

## Deterministic Checks (from script)
[Summarize what the maintenance script found]

## AI-Powered Analysis
[Additional findings from intelligent checks]

## Recommendations
[Prioritized list of actions]

## Metrics
- Total disk usage: X MB
- Session files: X (X old)
- Uncommitted changes: X files
```

### Step 5: Report to User
Display maintenance status:
- If healthy: Confirm everything looks good
- If issues found: Explain each and offer to help fix

---

## Interactive Maintenance Workflow

When `--interactive` is specified, guide the user through maintenance decisions:

### Question Set 1: Cleanup Scope
Ask the user:
1. "Should I clean up old session files (older than 7 days)?"
2. "Should I remove Python cache directories?"
3. "Should I clean up orphaned build directories?"

### Question Set 2: Updates
After cleanup:
1. "Should I update Python dependencies?"
2. "Should I reinstall the Nexus CLI tools?"
3. "Should I check for Nexus template updates?"

### Question Set 3: Git Maintenance
If git issues found:
1. "There are uncommitted changes. Should I show them?"
2. "There are stale branches. Should I list them for cleanup?"

### Interactive Flow
```
FOR each question set:
    → Ask questions using AskUserQuestion tool
    → Process responses
    → Run relevant maintenance tasks
    → Report progress
    → Move to next set
```

---

## Common Issues & Solutions

### Problem: Disk space running low
**Solution:**
1. Clean old sessions: `find .claude/sessions -mtime +7 -delete`
2. Clean Python cache: `find . -type d -name __pycache__ -exec rm -rf {} +`
3. Review and archive old builds

### Problem: Dependencies out of sync
**Solution:**
```bash
uv sync --reinstall
```

### Problem: Git working directory dirty
**Solution:**
Review changes and either commit or stash:
```bash
git status
git stash  # or git add . && git commit
```

### Problem: Orphaned build directories
**Solution:**
Review builds in `02-builds/active/` and archive completed ones:
```bash
mv 02-builds/active/old-build 02-builds/complete/
```

---

## Maintenance Schedule
Recommend running maintenance:
- **Weekly**: Dependency updates, cache cleanup
- **Monthly**: Full health check, git cleanup
- **Before major work**: Fresh environment validation

---

## Exit Conditions
- **Healthy**: All checks pass, no action needed
- **Needs Attention**: Minor issues, can be addressed later
- **Action Required**: Critical issues that should be fixed now

Always end by summarizing what was done and what (if anything) needs user attention.
