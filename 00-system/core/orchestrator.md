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

**Output this EXACTLY as shown, preserving line breaks. Replace bracketed values with actual data.**

```
🧠 MEMORY
   [If goals empty: "Empty ▸ say 'setup goals' to teach me about you"]
   [If goals set: "Role: {role}" and "Goal: {goal}"]

📦 PROJECTS
   [If none: "None yet ▸ say 'create project' to start something"]
   [If exists: "• {name} | {status} | {progress}% ▸ '{trigger}'" per project, max 5]

🔧 SKILLS
   [If user skills: "User: {names}"]
   System: create-project, create-skill, close-session

📁 WORKSPACE [SKIP THIS SECTION ENTIRELY if workspace IS configured]
   Not configured ▸ say "setup workspace" to organize your files

💬 WHAT'S NEXT?
   [First applicable: IN_PROGRESS suggestion OR PLANNING suggestion OR "What would you like to work on?"]

Say "explain Nexus" for help ▸ or just tell me what to do!
```

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
