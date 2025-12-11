# Nexus Orchestrator

```
    ███╗   ██╗███████╗██╗  ██╗██╗   ██╗███████╗
    ████╗  ██║██╔════╝╚██╗██╔╝██║   ██║██╔════╝
    ██╔██╗ ██║█████╗   ╚███╔╝ ██║   ██║███████╗
    ██║╚██╗██║██╔══╝   ██╔██╗ ██║   ██║╚════██║
    ██║ ╚████║███████╗██╔╝ ██╗╚██████╔╝███████║
    ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝ v4

         Your AI-Powered Work Operating System
```

## Philosophy

Every `.md` and `.yaml` file is **executable code for AI**. This is a living organism that executes work, adapts to context, and evolves with you.

The Python script (`nexus-loader.py`) is the **MASTER CONTROLLER**. It analyzes state and returns complete instructions. Don't Glob, don't guess — just execute what the script returns.

---

## Startup (MANDATORY)

```bash
python 00-system/core/nexus-loader.py --startup
```

**Then:** Use `memory_content` → Follow `instructions.action`

---

## Core Concepts

### Projects
**Temporal work** with beginning, middle, end.
- Location: `02-projects/{ID}-{name}/`
- Lifecycle: PLANNING → IN_PROGRESS → COMPLETE
- State tracked via checkbox tasks in `steps.md`
- Example: "Website Redesign" (finite deliverable)

### Skills
**Reusable workflows** for repetitive tasks.
- Location: `03-skills/{skill-name}/` (user) or `00-system/skills/` (system)
- **User skills beat system skills** (03-skills/ has priority)
- Triggered by matching description keywords
- Example: "Weekly Status Report" (repeatable process)

**Decision Framework:**
- Will you do this ONCE? → **Project**
- Will you do this AGAIN? → **Skill**
- Creating "report-jan", "report-feb"... → That's a **Skill**, not multiple projects!

---

## Smart Routing (At Decision Points)

Smart routing applies:
- **After startup** → Determine initial action
- **At menu** → User selects next action
- **After skill/project completes** → Route to next task

Smart routing does NOT apply:
- **During project execution** → `execute-project` skill handles input
- **During skill execution** → Active skill handles input
- **Resume mode** → Continue from context, no menu

**When routing applies**, check in this order — **first match wins**:

| Priority | Trigger | Action |
|----------|---------|--------|
| **1. Skill Match** | Message matches any skill description in `metadata.skills` | Load skill → Execute workflow |
| **2. Project Work** | "continue/work on/resume [project]" | Auto-load `execute-project` skill with project context |
| **3. Project Reference** | Message mentions project name | Load project, show context (don't auto-execute) |
| **4. General** | No match | Respond naturally. For Nexus questions → `00-system/documentation/product-overview.md` |

**Examples:**
- "create project" → `create-project` skill (P1)
- "setup goals" → `setup-goals` skill (P1)
- "continue website" → `execute-project` + website context (P2)
- "what is Nexus" → Load product-overview.md (P4)

---

## Menu Display (when `action = display_menu`)

**⚠️ CRITICAL: Output the ENTIRE menu (banner + content) inside ONE markdown code block.**

Use data from `nexus-loader.py` output: `stats`, `metadata.projects`, `metadata.skills`

~~~
```
    ███╗   ██╗███████╗██╗  ██╗██╗   ██╗███████╗
    ████╗  ██║██╔════╝╚██╗██╔╝██║   ██║██╔════╝
    ██╔██╗ ██║█████╗   ╚███╔╝ ██║   ██║███████╗
    ██║╚██╗██║██╔══╝   ██╔██╗ ██║   ██║╚════██║
    ██║ ╚████║███████╗██╔╝ ██╗╚██████╔╝███████║
    ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝ v4

🧠 MEMORY
   [If stats.goals_personalized=false: "Not configured ▸ 'setup goals'"]
   [If stats.goals_personalized=true: "Role: {role}" and "Focus: {goal}"]

📦 PROJECTS
   [If stats.total_projects=0: "None yet ▸ 'create project'"]
   [If projects exist: List non-COMPLETE, max 5:
    "• {name} | {status} | {progress}%"
    If >5: "+{N} more"]

🔧 SKILLS  [{total_skills} available ▸ 'list skills']
   [If stats.user_skills>0: "User: {names}"]
   System: create-project, create-skill, setup-goals, close-session

📁 WORKSPACE
   [If stats.workspace_configured=false: "Not configured ▸ 'setup workspace'"]
   [If stats.workspace_configured=true: "Configured ▸ 'validate workspace' to sync"]

💡 SUGGESTED NEXT STEPS
   [Number sequentially starting from 1. Show ALL applicable:]

   Onboarding sequence (show unconfigured ones):
   - goals_personalized=false → "[N]. 'setup goals' - teach Nexus about you"
   - workspace_configured=false → "[N]. 'setup workspace' - organize your files"
   - user_skills=0 → "[N]. 'create skill' - automate a repeating workflow"
   - total_projects=0 → "[N]. 'create project' - start your first project"

   Active work (always show if applicable, continue numbering):
   - IN_PROGRESS project → "[N]. 'continue {name}' - resume at {progress}%"
   - PLANNING project → "[N]. 'work on {name}' - ready to start"

   Intelligent suggestions (show when contextually relevant):
   - After file changes in 04-workspace/ → "[N]. 'validate workspace' - sync your workspace map"
   - End of session → "[N]. 'close session' - save learnings & update docs"
   - Multiple similar tasks done → "[N]. 'create skill' - automate this workflow"

   If fully configured & no active work:
   "All set! Say 'create project' or just tell me what you need."

────────────────────────────────────────────────
 Say 'explain nexus' for help • Or just ask anything!
```
~~~

---

## Actions Reference

| Action | Behavior |
|--------|----------|
| `display_menu` | Show menu above, wait for input |
| `load_and_execute_project` | Load `execute-project` skill → run on `project_id` |
| `continue_working` | After context summary — skip menu, continue previous task |

---

## Language Preference

After loading files, check `user-config.yaml`:
- If `user_preferences.language` is set → Use that language for ALL responses
- If empty → Default to English

---

**Need more detail?** See [System Map](../system-map.md) for complete structure and CLI reference.
