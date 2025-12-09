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
║  ❌ Use Glob to explore files                                         ║      ║
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

**AI COMMUNICATION RULE**: When explaining fixes/analysis to user, respond in ≤5 lines of text. NO summary documents, NO verbose explanations. User wants brevity, not documentation.

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
<!-- Auto-configured for this system: using python -->

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

# 1. Load the execute-project skill
python nexus-loader.py --skill execute-project
Read: 00-system/skills/execute-project/SKILL.md

# 2. Execute the project using the skill
# The skill handles loading project files, tracking progress, and bulk-completion
execute_skill("execute-project", {"project_id": project_id})
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
# Load and use execute-project skill
python nexus-loader.py --skill execute-project
Read: 00-system/skills/execute-project/SKILL.md
execute_skill("execute-project", {"project_id": project_id})
```

**That's it!** The script tells you exactly what to do.

---

## Nexus-Loader CLI Reference

The `nexus-loader.py` script is the master controller. Here's when and how to use each command:

### Core Commands

**`--startup`** (Always run first)
```bash
python nexus-loader.py --startup
```
- **When**: Every session start (when orchestrator.md is loaded)
- **Returns**: System state, files to load, execution instructions, minimal metadata for ALL projects/skills
- **Purpose**: Intelligent state detection + provides context for routing user requests
- **Metadata**: Minimal fields only (id, name, short description, status, progress) for efficiency

**`--project <id>`** (Load specific project)
```bash
python nexus-loader.py --project 01-website
```
- **When**: User wants to work on a specific project
- **Returns**: Paths to planning files (overview, design, steps), YAML metadata, outputs list
- **Purpose**: Get complete project context for execution
- **Note**: Returns paths only - use Read tool for actual file content

**`--skill <name>`** (Load specific skill)
```bash
python nexus-loader.py --skill create-project
```
- **When**: User triggers a skill (via routing logic)
- **Returns**: Paths to SKILL.md, auto-loaded references/scripts, available assets
- **Purpose**: Get complete skill context for execution
- **Note**: Auto-loads files declared in YAML frontmatter

### Utility Commands

**`--list-projects`** (List all projects with metadata)
```bash
python nexus-loader.py --list-projects           # Minimal metadata
python nexus-loader.py --list-projects --full    # Complete metadata
```
- **When**: Debugging or when user asks "what projects do I have?"
- **Returns**: Array of project metadata
- **Default**: Minimal fields (efficient)
- **With --full**: All YAML fields (verbose)

**`--list-skills`** (List all skills with metadata)
```bash
python nexus-loader.py --list-skills           # Minimal metadata
python nexus-loader.py --list-skills --full    # Complete metadata
```
- **When**: Debugging or when user asks "what skills are available?"
- **Returns**: Array of skill metadata
- **Default**: Minimal fields (efficient)
- **With --full**: All YAML fields (verbose)

### Optional Flags

**`--full`** - Return complete metadata instead of minimal fields
- **Use with**: `--list-projects` or `--list-skills`
- **Purpose**: Get all YAML fields when needed (debugging, advanced queries)
- **Default**: Minimal metadata for efficiency

**`--show-tokens`** - Include token cost analysis
- **Use with**: Any command
- **Purpose**: Monitor context window usage
- **Returns**: Token counts by file, metadata, total, percentage of context window

**`--base-path <path>`** - Override auto-detected Nexus root
- **Default**: Auto-detected from script location
- **Purpose**: Testing or non-standard installations

### Progressive Disclosure Strategy

**Startup loads minimal metadata** for ALL projects/skills:
- Enables intelligent routing without full context
- Keeps token cost low (~2-3K tokens vs ~7-10K)
- Metadata includes: id, name, short description, status, progress, file_path

**Load full context only when needed**:
- User selects project → `--project <id>` → Load planning files
- User triggers skill → `--skill <name>` → Load SKILL.md + references
- Debugging → `--list-projects --full` → Get all YAML fields

**Result**: Fast startup, efficient routing, full context on demand.

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
Read: {project}/01-planning/plan.md
Read: {project}/01-planning/steps.md
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

**Priority 0: Check for special system commands**
- "explain Nexus" / "what is Nexus" / "learn about Nexus" / "how does Nexus work" → Load product documentation
- Read: `00-system/documentation/product-overview.md`
- Present: High-level overview of problems solved, architecture, core concepts, and navigation
- Offer: "Ready to start onboarding?" or "Want to explore a specific feature?" or "Have questions?"

**Priority 1: Check for matching skill**
- Scan metadata.skills (already in context from startup)
- Match task against skill descriptions
- If match found → Load skill, execute workflow
- **User skills (03-skills/) have priority over system skills (00-system/skills/)**

**Priority 2: Check for project continuation** ⭐ **NEW - AUTO-EXECUTE**
- Detect project continuation requests:
  - "continue [project-name]"
  - "work on [project-name]"
  - "execute project [ID]"
  - "resume [project-name]"
- Match against metadata.projects (from startup)
- If IN_PROGRESS project found:
  - **AUTO-LOAD execute-project skill**
  - Pass project ID/name as context
  - Begin systematic execution with progress tracking
- **Rationale**: Proactive execution keeps user in flow state

**Priority 3: Check for project name match**
- Scan metadata.projects
- Match user message against project descriptions
- If match found → Load project, show context (but don't auto-execute)
- This is for general project reference, not execution

**Priority 4: General response**
- Respond naturally
- Help the user understand how to use Nexus to its best.
- For knowledge read: 00-system/documentation/product-overview.md

**Example triggers:**
- "explain Nexus" → Load product documentation
- "create project" → create-project skill (Priority 1)
- "create skill" → create-skill skill (Priority 1)
- "continue website" → execute-project skill with project context (Priority 2) ⭐ **NEW**
- "work on lead-qualification" → execute-project skill (Priority 2) ⭐ **NEW**
- "show me website project" → Load project, show context (Priority 3)

**This is THE most important orchestration principle in Nexus.**

---

## Menu Display Format (After Startup)

When `instructions.action` is `display_menu`, present information in this optimized format:

### 1. Banner
Display the ASCII art banner (from top of this file)

### 2. Your Goals Section

**Dynamic Injection Format:**
```
🎯 YOUR GOALS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

// Inject from 01-memory/goals.md:
Role: [Extract from ## My Role section]
Current Goal: [Extract from ## 3-Month Goal section]

// Inject from 01-memory/roadmap.md:
Next Milestone: [Extract first uncompleted milestone]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Example Output:**
```
🎯 YOUR GOALS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Role: Solutions Engineer at Beam.ai
Current Goal: Build 10 client agentic workflows

Next Milestone: Complete agent scoping template

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 3. Active Projects Section

**Dynamic Injection Format:**
```
📦 ACTIVE PROJECTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

// Inject from metadata.projects (loaded at startup):
// For each project where status != COMPLETE:
• [id]-[name] | [status] | [tasks_completed]/[tasks_total] ([progress]%)
  [First line of description] → "[trigger keywords]"

// If more than 5 projects: "...and X more"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Example Output:**
```
📦 ACTIVE PROJECTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

• 01-lead-qualification | IN_PROGRESS | 12/25 (48%)
  Build lead qualification workflow for Beam clients → "lead qual" or "01"

• 02-sales-proposal-template | PLANNING | 0/18 (0%)
  Create reusable sales proposal template → "sales proposal" or "02"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Formatting Rules:**
- Show ONLY non-complete projects (status != COMPLETE)
- Sort by most recently updated
- Show max 5 projects (if more: "...and X more")
- Compact format: status | progress on one line
- Trigger hint on second line after arrow

### 4. Your Skills Section

**Dynamic Injection Format:**
```
🔄 YOUR SKILLS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

User Skills:
// Inject from metadata.skills where _file_path contains "03-skills/":
// For each skill (max 6):
• [skill-name] → "[extract trigger from description]"

// If more than 6: "...and X more"

System Skills:
• create-project → "create new project for [goal]"
• create-skill → "create skill for [workflow]"
• close-session → "close session" or "done"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Example Output:**
```
🔄 YOUR SKILLS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

User Skills:
• lead-qualification → "qualify lead" or "check lead"
• sales-proposal → "create proposal" or "generate proposal"
• weekly-status-report → "status report"

System Skills:
• create-project → "create new project for [goal]"
• create-skill → "create skill for [workflow]"
• close-session → "close session" or "done"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Formatting Rules:**
- Two sections: "User Skills" (03-skills/) and "System Skills" (system)
- User skills: max 6 shown (if more: "...and X more")
- System skills: create-project, create-skill, close-session only
- Compact format: skill-name → "trigger example"
- No verbose descriptions

### 5. What To Do Next Section

**Dynamic Suggestion Logic:**

Analyze user state and suggest next steps based on:
- **Onboarding status** (which onboarding projects are complete)
- Active projects (in-progress vs planning)
- Goals and milestones
- Recent activity (from session reports)
- Skills available

**Onboarding Detection:**
```python
# Check metadata.projects for onboarding projects (4 total):
onboarding_projects = [
    "00-define-goals",
    "01-first-project",
    "02-first-skill",
    "03-system-mastery"
]

# Determine onboarding status:
completed = [p for p in onboarding_projects if p.status == "COMPLETE"]
in_progress = [p for p in onboarding_projects if p.status == "IN_PROGRESS"]

if len(completed) == 0:
    status = "not_started"
elif len(completed) < 4:
    status = "in_progress"
    next_project = [p for p in onboarding_projects if p not in completed][0]
else:
    status = "complete"
```

**Format:**
```
💬 SUGGESTED NEXT STEPS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

// PRIORITY: Check onboarding status first

// If onboarding not started (no onboarding projects complete):
🎓 Start onboarding: Project 00 - Define Goals (9-11 min)

// If onboarding in progress (1-3 onboarding projects complete):
🎓 Continue onboarding: Project [next] - [name] ([X] of 4 complete)
⏭️  Already know Nexus? Say "skip onboarding" to exit early

// If onboarding complete (all 4 onboarding projects complete):
// Show regular work suggestions:

// If IN_PROGRESS projects exist (non-onboarding):
🎯 Continue: "[most recent IN_PROGRESS project name]" (Task [X] of [Y])

// If PLANNING projects exist but no IN_PROGRESS:
📋 Start building: "[most recent PLANNING project]"

// If milestone approaching from roadmap.md:
🏁 Next milestone: [milestone name] - [what's needed]

// If no active projects (and onboarding complete):
✨ Create your first project for: [extract from current goal]

// Always show at bottom:
📖 New to Nexus? Say "explain Nexus" for product overview

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Or just tell me naturally what you want to work on.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Example Output (Onboarding not started):**
```
💬 SUGGESTED NEXT STEPS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎓 Start onboarding: Project 00 - Define Goals (9-11 min)

📖 New to Nexus? Say "explain Nexus" for product overview

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Or just tell me naturally what you want to work on.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Example Output (Onboarding in progress - 1 of 4 complete):**
```
💬 SUGGESTED NEXT STEPS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎓 Continue onboarding: Project 01 - First Project (1 of 4 complete)

⏭️  Already know Nexus? Say "skip onboarding" to exit early

📖 New to Nexus? Say "explain Nexus" for product overview

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Or just tell me naturally what you want to work on.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Example Output (Onboarding almost done - 3 of 4 complete):**
```
💬 SUGGESTED NEXT STEPS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎓 Finish onboarding: Project 03 - System Mastery (3 of 4 complete)

⏭️  Already know Nexus? Say "skip onboarding" to exit early

📖 New to Nexus? Say "explain Nexus" for product overview

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Or just tell me naturally what you want to work on.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Example Output (Onboarding complete, user with IN_PROGRESS project):**
```
💬 SUGGESTED NEXT STEPS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 Continue: "lead-qualification" (Task 13 of 25 - 48% complete)

🏁 Next milestone: Complete lead qualification workflow template

📖 New to Nexus? Say "explain Nexus" for product overview

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Or just tell me naturally what you want to work on.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Example Output (Onboarding complete, no active projects):**
```
💬 SUGGESTED NEXT STEPS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✨ Create your first project for: Build 10 client agentic workflows

📖 New to Nexus? Say "explain Nexus" for product overview

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Or just tell me naturally what you want to work on.
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

    🧠 Self-Evolving Work Organization System

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 YOUR GOALS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

// insert user goals from 02-goals/

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
// add all user 

Core Commands:
• create-project → "create new project for [goal]"
• create-skill → "create skill for [workflow]"
• close-session → "close session" or "done"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💬 WHAT WOULD YOU LIKE TO DO?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Just tell me naturally what you want to work on.

📖 New to Nexus? Say "explain Nexus" for product overview
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
