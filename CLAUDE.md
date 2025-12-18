# ⚠️ CRITICAL: INITIALIZATION REQUIRED ⚠️

**THIS FILE IS LOADED AT THE START OF EVERY SESSION AND AFTER EVERY CONTEXT SUMMARY!**

# ⚠️ LOADING SEQUENCE (ALWAYS RUN) ⚠️

## Step 1: Read orchestrator (ALWAYS)
```
00-system/core/orchestrator.md
```

## Step 2: Run startup script (ALWAYS)

**Fresh Session** (first message):
```bash
python 00-system/core/nexus-loader.py --startup
```

**MANDATORY After Context Summary** (MANDATORY IF INITIAL USER CONTENT STARTS WITH: "This session is being continued from a previous conversation that ran out of context. The conversation is summarized below:"):
```bash
python 00-system/core/nexus-loader.py --resume
```

## Step 3: Follow `instructions.action`

| Action | Behavior |
|--------|----------|
| `display_menu` | Show Nexus menu, wait for user input |
| `continue_working` | Skip menu, continue from summary context |
| `load_and_execute_project` | Load and execute specified project |

**The `--resume` flag returns `continue_working` action** - this tells you to skip the menu and continue working based on the summary instructions.

## Step 4: Process user message

After initialization, respond to the user's actual request.

---

## ⚠️ HARD RULES (NEVER SKIP)

These rules override all other behavior:

1. **Project reference → execute-project**: ANY mention of a project by name/ID/number → load `execute-project` skill FIRST. Never read project files directly.

2. **"create project" → create-project**: ALWAYS load `create-project` skill. Never create project folders directly.

3. **"create skill" → create-skill**: ALWAYS load `create-skill` skill. Never create skill folders directly.

4. **Learning triggers → load learning skill**: When user says "learn X", "setup X", or matches a learning skill trigger → load that skill from `00-system/skills/learning/`.

---

**DO THIS BEFORE RESPONDING TO THE USER OR DOING ANY OTHER ACTIONS.**
