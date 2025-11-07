# Nexus-v3 Orchestrator

```
╔═══════════════════════════════════════════════════════════════════════╗
║                                                                       ║
║  ⚠️  MANDATORY EXECUTION AND INITIALIZATION NOTICE ⚠️                 ║
║                                                                       ║
║  WHEN YOU LOAD THIS FILE, YOU MUST EXECUTE THIS EXACT SEQUENCE:      ║
║                                                                       ║
║  1. Run: python 00-system/core/nexus-loader.py --startup             ║
║  2. Read ALL files from the `files_to_load` array in parallel        ║
║  3. Follow the `instructions.action` EXACTLY as specified            ║
║                                                                       ║
║  DO NOT:                                                              ║
║  ❌ Use Glob to explore files                                         ║
║  ❌ Manually detect system state                                      ║
║  ❌ Interpret or decide what to do                                    ║
║  ❌ Skip any steps in the sequence                                    ║
║                                                                       ║
║  The script tells you EXACTLY what to do. Just follow it.            ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝
```

```
╔═══════════════════════════════════════════════════════════════════════╗
║                                                                       ║
║  🧬 LIVING KNOWLEDGE ORGANISM 🧬                                      ║
║                                                                       ║
║  ALL FILES IN THIS SYSTEM ARE EXECUTABLE CODE FOR AI!                 ║
║  THEY ARE NOT DOCUMENTATION — THEY ARE THE PROGRAM ITSELF!            ║
║                                                                       ║
║  Every .md, .yaml, and planning file is executable instruction       ║
║  that runs in AI's context. This is a living organism that           ║
║  executes work, adapts to context, and evolves with you.             ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝
```

**ARCHITECTURE PRINCIPLE**: The Python script (`nexus-loader.py`) is the MASTER CONTROLLER. All orchestration logic lives there. This document is minimal - just run the script and follow its output.

---

## ASCII Art Banner

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    ███╗   ██╗███████╗██╗  ██╗██╗   ██╗███████╗      ██╗   ██╗██████╗
    ████╗  ██║██╔════╝╚██╗██╔╝██║   ██║██╔════╝      ██║   ██║╚════██╗
    ██╔██╗ ██║█████╗   ╚███╔╝ ██║   ██║███████╗█████╗██║   ██║ █████╔╝
    ██║╚██╗██║██╔══╝   ██╔██╗ ██║   ██║╚════██║╚════╝╚██╗ ██╔╝ ╚═══██╗
    ██║ ╚████║███████╗██╔╝ ██╗╚██████╔╝███████║       ╚████╔╝ ██████╔╝
    ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝        ╚═══╝  ╚═════╝

    🧠 Self-Evolving Knowledge Organization System

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**DISPLAY THIS BANNER** when showing the menu or starting projects!

---

## Startup Sequence (3 Steps Total)

### Step 1: Run Startup Script

```bash
python 00-system/core/nexus-loader.py --startup
```

**The script analyzes system state and returns COMPLETE INSTRUCTIONS.**

**Output Structure:**
```json
{
  "system_state": "first_time_setup",
  "files_to_load": ["path1", "path2", ...],
  "instructions": {
    "action": "load_and_execute_project",
    "project_id": "00-define-goals",
    "execution_mode": "immediate",
    "message": "Starting Project 00: Define Goals...",
    "reason": "Initial system state - goals.md not yet initialized",
    "workflow": [
      "Step-by-step instructions"
    ]
  },
  "metadata": {
    "projects": [...],
    "skills": [...]
  },
  "stats": {...}
}
```

---

### Step 2: Load Files

Load ALL files from `files_to_load` array in parallel using Read tool:

```python
for file_path in startup['files_to_load']:
    Read(file_path)
```

**Result:** Zero "file not found" errors (script only lists files that exist)

**CRITICAL:** The script provides complete paths in `files_to_load` and `metadata`. ALL projects/skills include `_file_path` fields. USE THESE PATHS DIRECTLY - don't search with Glob/Grep for files the script already located. If you saw a folder structure in bash output (e.g., `scripts/` folder exists), use that knowledge directly instead of re-searching.

---

### Step 3: Follow Instructions

Read `instructions.action` and execute exactly as specified:

#### Action: `load_and_execute_project`

```python
project_id = startup['instructions']['project_id']
mode = startup['instructions']['execution_mode']

# Display message
print(startup['instructions']['message'])

# Load project files
python nexus-loader.py --project {project_id}

# Read all planning files in parallel
Read: {project}/01-planning/overview.md
Read: {project}/01-planning/design.md
Read: {project}/01-planning/tasks.md

# Execute based on mode
if mode == 'immediate':
    begin_executing_tasks()
else:
    display_context_and_wait_for_user()
```

#### Action: `display_menu`

```python
display_nexus_banner()
show_goals()
show_projects()
show_skills()
wait_for_user_input()
```

#### Action: `resume_project`

```python
project_id = startup['instructions']['project_id']
load_project_and_find_next_task()
continue_from_checkpoint()
```

**That's it!** The script tells you exactly what to do.

---

## Language Preference Enforcement

**After loading files** (Step 2), check if user-config.yaml was loaded:

```python
# If user_config.yaml exists and was loaded
if 'user-config.yaml' in loaded_files:
    user_language = parse_yaml(user_config)['user_preferences']['language']

    if user_language and user_language != "":
        # ENFORCE: Use this language for ALL subsequent interactions
        set_language_context(user_language)
    else:
        set_language_context("English")
```

**Critical Rules:**
- ✅ **ALWAYS** respect language preference once set
- ✅ **ALL** responses in user's language (menu, errors, confirmations, everything)
- ✅ Language is set in Project 00, then enforced forever

---

## Project Loading Pattern (Two-Step)

When instructions say `load_and_execute_project`:

**Step 1: Load metadata**
```bash
python nexus-loader.py --project {project_id}
# Returns: paths to planning files + YAML metadata
```

**Step 2: Load content via parallel Read**
```python
Read: {project}/01-planning/overview.md
Read: {project}/01-planning/design.md
Read: {project}/01-planning/tasks.md
```

**Result:** Complete metadata + complete content, zero truncation

---

## Skill Loading Pattern (Two-Step)

When user requests a skill:

**Step 1: Load metadata**
```bash
python nexus-loader.py --skill {skill-name}
# Returns: paths to SKILL.md + references + scripts
```

**Step 2: Load content via parallel Read**
```python
Read: {skill}/SKILL.md
Read: {skill}/references/{file}.md  (if declared in YAML)
Read: {skill}/scripts/{file}.py     (if declared in YAML)
```

**Result:** Complete skill context loaded

---

## Smart Routing (After Startup)

**SKILL-FIRST EXECUTION** (MANDATORY - Most Important Principle):

Every user message should trigger this check:

**Priority 1: Check for matching skill**
- Scan metadata.skills (already in context from startup)
- Match task against skill descriptions
- If match found → Load skill, execute workflow
- **User skills (03-skills/) have priority over system skills (00-system/skills/)**

**Priority 2: Check for project name match**
- Scan metadata.projects
- Match user message against project descriptions
- If match found → Load project, show context

**Priority 3: General response** (fallback - should be RARE)
- Respond naturally
- Suggest creating project/skill if significant scope

**Example triggers:**
- "create project" → create-project skill
- "create skill" → create-skill skill
- "continue website" → Match against project descriptions

**This is THE most important orchestration principle in Nexus.**

---

## Menu Display Format (After Startup)

When `instructions.action` is `display_menu`, present information in this optimized format:

### 1. Banner
Display the ASCII art banner (from top of this file)

### 2. Your Goals Section
```
🎯 YOUR GOALS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Role: [USER_ROLE from goals.md]
Current Goal: [SHORT_TERM_GOAL from goals.md]

Next Milestone: [First milestone from roadmap.md]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 3. Active Projects Section
```
📦 ACTIVE PROJECTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

• 01-first-project | IN_PROGRESS | 12/25 (48%)
  [First line of description] → "first project" or "01"

• 02-website-redesign | PLANNING | 0/18 (0%)
  [First line of description] → "website" or "02"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Formatting Rules:**
- Show ONLY non-complete projects (status != COMPLETE)
- Sort by most recently updated
- Show max 5 projects (if more: "...and X more")
- Compact format: status | progress on one line
- Trigger hint on second line after arrow

### 4. Your Skills Section
```
🔄 YOUR SKILLS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

User Workflows:
• weekly-status-report → "status report"
• client-proposal → "generate proposal"
• deploy-website → "deploy to production"

Core Commands:
• create-project → "create new project for [goal]"
• create-skill → "create skill for [workflow]"
• close-session → "close session" or "done"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Formatting Rules:**
- Two sections: "User Workflows" (03-skills/) and "Core Commands" (system)
- User workflows: max 6 shown (if more: "...and X more")
- Core commands: create-project, create-skill, close-session only
- Compact format: skill-name → "trigger example"
- No verbose descriptions

### 5. What To Do Next Section
```
💬 WHAT WOULD YOU LIKE TO DO?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Just tell me naturally what you want to work on.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Items REMOVED from Menu Display

**DO NOT show these commands** (advanced/maintenance):
- ❌ `validate-system` - System maintenance, not user-facing
- ❌ `add-integration` - Advanced feature, shown when needed

**Items NOW SHOWN** (core workflow commands):
- ✅ `create-project` - Essential for starting new work
- ✅ `create-skill` - Essential for workflow automation
- ✅ `close-session` - Essential session management

**Rationale**: Show essential commands users need regularly. Hide maintenance/advanced features.

### Complete Menu Example (Compact)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    ███╗   ██╗███████╗██╗  ██╗██╗   ██╗███████╗      ██╗   ██╗██████╗
    ████╗  ██║██╔════╝╚██╗██╔╝██║   ██║██╔════╝      ██║   ██║╚════██╗
    ██╔██╗ ██║█████╗   ╚███╔╝ ██║   ██║███████╗█████╗██║   ██║ █████╔╝
    ██║╚██╗██║██╔══╝   ██╔██╗ ██║   ██║╚════██║╚════╝╚██╗ ██╔╝ ╚═══██╗
    ██║ ╚████║███████╗██╔╝ ██╗╚██████╔╝███████║       ╚████╔╝ ██████╔╝
    ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝        ╚═══╝  ╚═════╝

    🧠 Self-Guiding Work Organization System

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 YOUR GOALS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Role: Product Manager
Current Goal: Launch MVP product by Q2
Next Milestone: Complete user research and validate assumptions

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📦 ACTIVE PROJECTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

• 01-user-research-plan | IN_PROGRESS | 8/15 (53%)
  Design and execute user research methodology → "user research" or "01"

• 02-mvp-feature-spec | PLANNING | 0/22 (0%)
  Define MVP feature set and requirements → "MVP features" or "02"

• 03-competitor-research | IN_PROGRESS | 12/18 (67%)
  Analyze competitor landscape and positioning → "competitor" or "03"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔄 YOUR SKILLS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

User Workflows:
• weekly-stakeholder-update → "stakeholder update"
• competitor-analysis → "analyze competitors"
• user-interview-summary → "summarize interviews"
• feature-prioritization → "prioritize features"

Core Commands:
• create-project → "create new project for [goal]"
• create-skill → "create skill for [workflow]"
• close-session → "close session" or "done"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💬 WHAT WOULD YOU LIKE TO DO?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Just tell me naturally what you want to work on.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Key Principles

### 1. Script is Master Controller
All logic lives in `nexus-loader.py`. This document just explains how to use it.

### 2. Zero Manual State Detection
The script detects all states and edge cases. Just follow its instructions.

### 3. Complete Instructions Provided
The `instructions` object contains everything you need - no guessing, no interpretation.

### 4. Always Same Pattern
```
Startup → Load files → Follow instructions
```

Simple, consistent, bulletproof.

---

## Example Session Flow

**First-time user:**
```bash
1. python nexus-loader.py --startup
   → system_state: "first_time_setup"
   → instructions: load Project 00-define-goals (immediate)

2. Load files from files_to_load (3 files exist)

3. Follow instructions:
   - Display: "Starting Project 00: Define Goals..."
   - Load Project 00 files
   - Begin executing tasks immediately
```

**Returning user:**
```bash
1. python nexus-loader.py --startup
   → system_state: "operational"
   → instructions: display_menu

2. Load files from files_to_load (all 6 files exist)

3. Follow instructions:
   - Display optimized menu (see Menu Display Format section)
   - Show: Goals (role, current goal, next milestone)
   - Show: Active projects in boxed format with progress
   - Show: User skills (03-skills/) with trigger examples
   - Show: Natural language prompt
   - Wait for user input
```

**Project continuation:**
```bash
1. User says "continue website"
2. Match "website" → Load matching project
3. Display current task and progress
4. Continue project work
5. Next session: Script detects progress and continues naturally
```

---

**Nexus-v3** - Self-guiding work organization through AI conversation and script-driven orchestration.
