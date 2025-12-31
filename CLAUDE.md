# ⚠️ MANDATORY: RUN NEXUS LOADER FIRST ⚠️

**BEFORE doing ANYTHING else, you MUST run the startup script. No exceptions.**

```bash
python 00-system/core/nexus-loader.py --startup
```

**After Context Summary** (if user message starts with "This session is being continued from a previous conversation"):
```bash
python 00-system/core/nexus-loader.py --resume
```

---

The loader output tells you exactly what to do next. Follow its instructions.

---

## Context Preservation (BEFORE context runs out)

When working on a project and context is getting full, **UPDATE the project's `_resume.md`** with:

```yaml
---
updated: "YYYY-MM-DDTHH:MM:SS"
phase: "analysis" | "synthesis" | "planning" | "execution"
last_skill: "skill-name-here"
project_id: "XX-project-name"
---
```

This ensures the next session loads the correct skill automatically.

**Location**: `02-projects/{project-id}/_resume.md`
