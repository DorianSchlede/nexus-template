---
name: reset-instance
description: "reset instance, reset nexus, start fresh, clean slate, factory reset."
---

# Reset Instance

Reset Nexus to initial "clean" state for testing, demos, or recovery.

**Warning**: Destructive action - all builds and progress deleted.

## Arguments

| Flag | Purpose |
|------|---------|
| `--dry-run` | Preview changes without executing |
| `--keep-builds` | Preserve builds and roadmap (only reset memory/config) |
| `--include-skills` | Also clear user skills in 03-skills/ |

---

## Workflow

### Step 1: Parse Arguments

Detect from user input:
- `--dry-run` / "preview" / "show what would change"
- `--include-skills` / "include skills" / "reset skills too"

### Step 2: Scan Instance

```bash
uv run python 00-system/skills/system/reset-instance/scripts/reset_instance.py scan
```

Returns JSON manifest of files/folders to restore, delete, preserve.

### Step 3: Display Confirmation

```
====================================================
RESET INSTANCE - Confirmation Required
====================================================

RESTORE to templates:
  - 01-memory/goals.md, user-config.yaml, core-learnings.md
  - 04-workspace/workspace-map.md

DELETE:
  - 02-builds/active/* ({N} builds)
  - 02-builds/complete/* ({N} builds)
  - 01-memory/roadmap.yaml, session-reports/*, input/
  - .claude/.setup_complete

PRESERVE (never touched):
  - 00-system/, 03-skills/, .git/, .env

{if --include-skills: ALSO DELETE 03-skills/*}
====================================================
```

### Step 4: Handle Dry-Run

If `--dry-run`: Display "DRY RUN COMPLETE - No changes made" and exit.

### Step 5: Require Confirmation

```
Type "yes" or "reset" to confirm (anything else cancels):
```

- `yes`/`reset` → Continue
- Anything else → "Cancelled. No changes made." → Exit

### Step 6: Execute Reset

```bash
uv run python 00-system/skills/system/reset-instance/scripts/reset_instance.py execute [--include-skills]
```

Script performs (in order):
1. Delete builds, roadmap, session-reports, input/, .setup_complete
2. Clear 03-skills/* (if --include-skills)
3. Restore memory files from templates
4. Restore workspace-map.md from template

Show progress: `[OK] Cleared...` for each operation.

### Step 7: Display Summary

```
RESET COMPLETE - Instance at initial state.
Next: Say "hi" to begin onboarding.
```

---

## File Mappings

| Template Source | Target |
|-----------------|--------|
| `00-system/core/nexus/templates/goals.md` | `01-memory/goals.md` |
| `00-system/core/nexus/templates/user-config.yaml` | `01-memory/user-config.yaml` |
| `00-system/core/nexus/templates/core-learnings.md` | `01-memory/core-learnings.md` |
| `00-system/core/nexus/templates/workspace-map.md` | `04-workspace/workspace-map.md` |

## Never Touch

`00-system/`, `.git/`, `.env`, `pyproject.toml`, `01-memory/memory-map.md`

---

## Error Handling

| Error | Response |
|-------|----------|
| Template missing | Abort with error |
| Permission denied | Show file, suggest fix |
| Partial failure | Report successes and failures |

---

**Use with caution - no undo!**
