# Nexus Operating System - Gemini Entry Point

## Startup

**Read the orchestrator for behavior rules:**
```
00-system/core/orchestrator.md
```

**Load context manually:**
```bash
python 00-system/core/nexus-loader.py --startup
```

## Actions Reference

| Action | Behavior |
|--------|----------|
| `display_menu` | Show Nexus menu, wait for user input |
| `continue_working` | Skip menu, continue from context |
| `load_and_execute_build` | Load and execute specified build |

Follow `instructions.action` from the loader output.