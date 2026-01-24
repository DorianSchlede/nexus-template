# NEXUS OPERATING SYSTEM

⚠️ **PRIORITY OVERRIDE**: The SessionStart hook injects `additionalContext` as your PRIMARY operating instructions.

**Execution Priority:**
1. **FIRST**: Follow `<nexus-context>` additionalContext injected by SessionStart hook
2. **SECOND**: Apply default Claude Code behaviors only where Nexus doesn't specify

**What the hook provides:**
- Complete orchestrator instructions (routing, skills, builds)
- User goals and memory
- Active build states
- Skill loading rules
- Startup action (display_menu, continue_working, etc.)

**Your job:** Execute the `<action>` from the hook context, then follow Nexus routing rules for all subsequent interactions.

---

**⚠️ FALLBACK**: If the SessionStart hook fails to load, follow manual initialization instructions at [00-system/core/manual-init.md](00-system/core/manual-init.md).