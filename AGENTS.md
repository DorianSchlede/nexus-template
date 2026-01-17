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

**MANDATORY After Context Summary** (resuming from summary):
```bash
python 00-system/core/nexus-loader.py --resume
```

## Step 3: Follow `instructions.action`

| Action | Behavior |
|--------|----------|
| `display_menu` | Show Nexus menu, wait for user input |
| `continue_working` | Skip menu, continue from summary context |
| `load_and_execute_build` | Load and execute specified build |

**The `--resume` flag returns `continue_working` action** - this tells you to skip the menu and continue working based on the summary instructions.

## Step 4: Process user message

After initialization, respond to the user's actual request.

---

**DO THIS BEFORE RESPONDING TO THE USER OR DOING ANY OTHER ACTIONS.**