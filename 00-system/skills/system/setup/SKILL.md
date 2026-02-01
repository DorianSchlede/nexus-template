---
name: setup
description: "setup, configure, first run, initial setup, configure settings"
---

# /setup - Post-Installation Configuration

Quick configuration that runs once after installation. Sets up permissions and transitions directly to onboarding.

## Purpose

The installer handles deterministic tasks (download, install dependencies). This skill:

1. **Asks about Permission Settings** - Explains why automatic permissions help
2. **Auto-configures VS Code** - Sets markdown preview settings automatically
3. **Marks setup complete** - Prevents re-running
4. **Transitions to onboarding** - Continues in same chat

## Triggers

- Automatically when SessionStart detects fresh install
- Manually via "setup" or "configure settings"

---

## Execution Workflow

### Step 1: Welcome

Display:

```
Welcome to Nexus!

One quick question before we start.
```

### Step 2: Permission Settings (ASK USER)

**Use AskUserQuestion** with clear explanation:

```
Question: "How should I handle permissions?"

Header: "Permissions"

Options:
1. Label: "Automatic (Recommended)"
   Description: "I can read, write, and run commands without asking each time.
                 This is how Nexus works best - smooth and uninterrupted.
                 You can change this anytime in .claude/settings.local.json"

2. Label: "Ask each time"
   Description: "I'll ask permission before every file edit or command.
                 More control, but many interruptions during workflows."
```

**If "Automatic":** Create `.claude/settings.local.json`:
```json
{
  "permissions": {
    "allow": ["Bash(*)", "Edit", "Write", "Read", "Glob", "Grep", "WebFetch", "WebSearch"]
  }
}
```

**If "Ask each time":** Skip file creation, user will be prompted for each tool.

### Step 3: VS Code Settings (AUTOMATIC)

Automatically create/update `.vscode/settings.json`:
```json
{
  "markdown.preview.breaks": true,
  "markdown.preview.typographer": true,
  "files.associations": {
    "*.md": "markdown"
  }
}
```

No question needed - these settings just improve markdown rendering.

### Step 4: Mark Setup Complete

Create marker file:
```bash
echo "setup_completed=$(date -u +%Y-%m-%dT%H:%M:%SZ)" > .claude/.setup_complete
```

### Step 5: Transition to Onboarding (SAME CHAT)

Display:
```
Done!

Now let's set up YOUR Nexus. This takes about 10 minutes.
```

Then **immediately continue** with the quick-start onboarding flow (Step 0: How Nexus Works).

DO NOT tell user to close chat. Continue in same session.

---

## Detection Logic (for SessionStart)

Fresh install detected when:
1. `.claude/.setup_complete` does NOT exist
2. `01-memory/user-config.yaml` exists (Nexus was downloaded)

After setup completes:
- `.claude/.setup_complete` exists → setup won't run again
- `onboarding.status == "not_started"` → onboarding starts

---

## Files Created

| File | When | Purpose |
|------|------|---------|
| `.claude/settings.local.json` | If user chooses "Automatic" | Permission bypass |
| `.vscode/settings.json` | Always | Markdown preview |
| `.claude/.setup_complete` | Always | Prevent re-run |

---

## Error Handling

| Issue | Solution |
|-------|----------|
| Can't write settings.local.json | Inform user, continue anyway |
| Can't write .vscode/settings.json | Inform user, continue anyway |
| User closes chat during setup | Next session detects incomplete, re-runs |

---

## Key Points

- **One question only** (permissions)
- **Clear explanation** of why automatic is better
- **No chat restart** - flows directly into onboarding
- **User can change later** - settings.local.json is editable
