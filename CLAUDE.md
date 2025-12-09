# MANDATORY Initialization

**EVERY SESSION MUST START WITH THIS EXACT SEQUENCE:**

```bash
python 00-system/core/nexus-loader.py --startup
```

Then read ALL files from the `files_to_load` array returned by the script.

**The orchestrator contains the complete instructions:**
[00-system/core/orchestrator.md](00-system/core/orchestrator.md)

---

## CRITICAL: Context Compaction Rules

**Whenever the current session is being compacted/summarized, COPY THE FOLLOWING BLOCK VERBATIM into the TOP of the summary. Do NOT paraphrase. Do NOT summarize. COPY EXACTLY:**

```
═══════════════════════════════════════════════════════════════════════════
CORE REQUIREMENT FOR NEXT AI INSTANCE - EXECUTE BEFORE ANY RESPONSE:
═══════════════════════════════════════════════════════════════════════════

1. RUN THE STARTUP SCRIPT:
   python 00-system/core/nexus-loader.py --startup

2. READ ALL FILES from the `files_to_load` array in the script output

3. FOLLOW the `instructions.action` from the script output

This initializes the Nexus system with:
- Memory files (goals.md, roadmap.md, user-config.yaml)
- System maps and routing logic
- Project/skill metadata for intelligent routing

WITHOUT THIS INITIALIZATION, you are just a generic Claude session with no context.
═══════════════════════════════════════════════════════════════════════════
```

**^^^ COPY THAT ENTIRE BLOCK VERBATIM ^^^**

**THEN, append to the summary:**
- Current project state (project ID, phase, task number if active)
- Onboarding progress (which of 4 onboarding projects completed)
- Any pending user requests that weren't completed

**WHY THIS MATTERS:**
- The nexus-loader.py script detects system state and returns exactly what files to load
- Without running it, AI doesn't know user goals, active projects, or available skills
- The system breaks completely for users mid-workflow if this is missing
