# Nexus Orchestrator

```
    ███╗   ██╗███████╗██╗  ██╗██╗   ██╗███████╗
    ████╗  ██║██╔════╝╚██╗██╔╝██║   ██║██╔════╝
    ██╔██╗ ██║█████╗   ╚███╔╝ ██║   ██║███████╗
    ██║╚██╗██║██╔══╝   ██╔██╗ ██║   ██║╚════██║
    ██║ ╚████║███████╗██╔╝ ██╗╚██████╔╝███████║
    ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝ 

         Your 10x Operating System
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
| **0. Integration Exists** | "add/integrate [name]" where name is in `stats.configured_integrations` | Redirect to `{name}-connect` skill, explain it's already built |
| **1. Skill Match** | Message matches any skill description in `metadata.skills` | Load skill → Execute workflow |
| **2. Project Reference** | User mentions ANY project by name, ID, or number | **ALWAYS** load `execute-project` skill first |
| **3. General** | No match | Respond naturally. For Nexus questions → `00-system/documentation/product-overview.md` |

---

### ⚠️ Core Skill Matching (Semantic, Not Just Keywords)

Don't just match keywords - **understand user intent**:

| Skill | Intent Signal | Check First |
|-------|--------------|-------------|
| `create-project` | User wants to START something NEW with a deliverable | Is this new work? No existing project matches? |
| `execute-project` | User references EXISTING project | Does name/ID match `metadata.projects`? |
| `create-skill` | User wants to AUTOMATE repeating work | Is this a pattern they do regularly? |

**Decision flow:**
1. Check if user mentions existing project name/ID → `execute-project`
2. Check if user wants to create new finite work → `create-project`
3. Check if user wants to automate patterns → `create-skill`
4. Match against skill descriptions in `metadata.skills`

**Key distinction:**
- "work on website" + website project exists → `execute-project`
- "work on website" + no website project → `create-project` (suggest)

---

### Learning Skills - Use `stats.pending_onboarding`

The loader returns `stats.pending_onboarding[]` - use this data to suggest at contextually relevant moments:

| If pending... | Suggest when user... |
|---------------|---------------------|
| `setup_memory` | First session, asks about personalization |
| `learn_projects` | Creates first project, confused about projects |
| `learn_skills` | Creates first skill, describes repeating work |
| `learn_integrations` | Mentions external tool (Notion, Slack, GitHub) |

**Intent matching** - understand what user means, not just keywords:
- "what's the difference between projects and skills" → `learn-projects`
- "I use Notion for my tasks" → suggest `learn-integrations`

---

### NEVER Do

- ❌ Read project files directly → use `execute-project`
- ❌ Create project/skill folders directly → use create skills
- ❌ Auto-load learning skills → suggest, user decides

---

## Menu Display (when `action = display_menu`)

**⚠️ CRITICAL: Output the ENTIRE menu (banner + content) inside ONE markdown code block.**

### Step 1: Check `stats.display_hints` FIRST

Before rendering the menu, check `stats.display_hints[]` for critical items:

```json
"display_hints": [
  "SHOW_UPDATE_BANNER: v0.11.0 → v0.12.0",
  "ONBOARDING_INCOMPLETE: 3 skills pending",
  "PROMPT_SETUP_GOALS: Goals not yet personalized"
]
```

| Hint | Action |
|------|--------|
| `SHOW_UPDATE_BANNER: vX → vY` | Display update banner at top of menu |
| `ONBOARDING_INCOMPLETE: N skills` | Emphasize onboarding in suggested steps |
| `PROMPT_SETUP_GOALS` | Add "setup memory" to suggestions |
| `PROMPT_SETUP_WORKSPACE` | Add "setup workspace" to suggestions |

### Step 2: Render Menu

Use data from `nexus-loader.py` output: `stats`, `metadata.projects`, `metadata.skills`

~~~
```
    ███╗   ██╗███████╗██╗  ██╗██╗   ██╗███████╗
    ████╗  ██║██╔════╝╚██╗██╔╝██║   ██║██╔════╝
    ██╔██╗ ██║█████╗   ╚███╔╝ ██║   ██║███████╗
    ██║╚██╗██║██╔══╝   ██╔██╗ ██║   ██║╚════██║
    ██║ ╚████║███████╗██╔╝ ██╗╚██████╔╝███████║
    ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝ v4

[If stats.update_available=true:]
⚡ UPDATE AVAILABLE: v{stats.update_info.local_version} → v{stats.update_info.upstream_version}
   Say 'update nexus' to get latest improvements

🧠 MEMORY
   [If stats.goals_personalized=false: "Not configured ▸ 'setup memory'"]
   [If stats.goals_personalized=true: "Role: {role}" and "Focus: {goal}"]

📦 PROJECTS
   [If stats.total_projects=0: "None yet ▸ 'create project'"]
   [If projects exist: List non-COMPLETE, max 5:
    "• {name} | {status} | {progress}%"
    If >5: "+{N} more"]

🔧 SKILLS  [{total_skills} available ▸ 'list skills']
   [If stats.user_skills>0: "Custom: {names}"]
   [If stats.user_skills=0: "No custom skills ▸ 'create skill' or 'search skill library'"]
   Core: Create Project, Create Skill, Setup Memory, Update Workspace Map

📁 WORKSPACE
   [If stats.workspace_configured=false: "Not configured ▸ 'setup workspace'"]
   [If stats.workspace_configured=true: "Configured ▸ 'validate workspace' to sync"]

🔌 INTEGRATIONS
   [Build from stats.configured_integrations array:]
   - Active: {list where active=true, comma-separated} (or "None" if empty)
   - Available: {list where active=false, comma-separated} ▸ 'connect {name}'
   - 'add integration' for new services

💡 SUGGESTED NEXT STEPS
   [Number sequentially starting from 1. Show ALL applicable:]

   Onboarding sequence (show unconfigured ones):
   - goals_personalized=false → "[N]. 'setup memory' - teach Nexus about you"
   - workspace_configured=false → "[N]. 'setup workspace' - organize your files"
   - learning_completed.learn_integrations=false → "[N]. 'learn integrations' - connect external tools"
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

## Proactive Onboarding (HIGH PRIORITY)

**nexus-loader.py returns `stats.pending_onboarding`** - a list of incomplete onboarding skills.

### How It Works

1. **Check `stats.pending_onboarding`** on startup - if NOT empty, onboarding is incomplete
2. **Suggest at natural moments** - don't interrupt, wait for relevant context
3. **Load when user explicitly asks** - match their message against skill descriptions
4. **Never auto-load** - always let user decide

### Suggestion Triggers

| Skill | Natural Moments to Suggest |
|-------|---------------------------|
| `setup-memory` | First session, user mentions "personalize", "my role", "about me", goals not configured |
| `setup-workspace` | User asks about files/folders/organization, after setup-memory completes |
| `learn-projects` | User says "create project" for first time, confused about project vs skill |
| `learn-skills` | User says "create skill" for first time, describes repeating work pattern |
| `learn-integrations` | User mentions external tool (Notion, Slack, GitHub, etc.), asks about connecting |
| `learn-nexus` | After other onboarding complete, user asks philosophical questions about system |

### Example Suggestions

**Before first project:**
```
💡 Before creating your first project, would you like a quick 8-minute tutorial?
Say 'learn projects' to understand projects vs skills, or 'skip' to create directly.
```

**When user mentions external tool:**
```
💡 You mentioned Notion. Want to learn how Nexus connects to external tools?
Say 'learn integrations' (10 min) or continue with your current task.
```

**When user describes repeating work:**
```
💡 I notice this sounds like repeating work. Skills are perfect for automating patterns.
Say 'learn skills' to understand when to create them, or 'skip' to continue.
```

### DO NOT Suggest When

- `stats.onboarding_complete: true` (all done!)
- User is mid-task and focused on execution
- User explicitly said "skip" or dismissed suggestion
- Same suggestion was made recently in conversation

### Priority Order

1. **Critical**: `setup-memory` - suggest first session, most impactful
2. **High**: `setup-workspace`, `learn-projects`, `learn-skills`, `learn-integrations`
3. **Medium**: `learn-nexus` - only after core onboarding complete

---

## Session End Behavior

### Gentle Reminders
When user signals they're wrapping up (e.g., "thanks", "that's all", "I'm done for now"):
- Gently remind: "Want me to save your session progress? Say 'done' to capture what we accomplished."
- Don't force it — if user says "no" or ignores, respect that

### Auto-Trigger Signals
Auto-trigger `close-session` skill when:
- User explicitly says "done", "close session", "wrap up", "finished"
- A project reaches 100% completion
- A major skill workflow completes (create-project, setup-memory, etc.)

### Why This Matters
Without `close-session`:
- Progress isn't saved to session reports
- Learnings aren't captured
- Next session loses context

---

**Need more detail?** See [System Map](../system-map.md) for complete structure and CLI reference.
