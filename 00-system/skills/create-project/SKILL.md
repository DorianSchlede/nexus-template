---
name: create-project
description: Create new temporal work projects with AI-guided planning and structure. Load when user mentions "create project", "new project", or "start something new". Guides through collaborative project definition, folder creation, task breakdown, and system integration using mental models.
---

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ CRITICAL EXECUTION REQUIREMENTS ⚠️

WORKFLOW: Structure FIRST, content SECOND

MANDATORY STEPS (DO NOT SKIP):
1. ✅ Create TodoWrite with ALL steps
2. ✅ Ask project name
3. ✅ RUN init_project.py IMMEDIATELY (creates all files)
4. ✅ Display created structure
5. ✅ Load overview.md → Fill in TODOs → PAUSE → User confirms
6. ✅ Load requirements.md → Fill in TODOs → PAUSE → User confirms
7. ✅ Load design.md → Fill in TODOs → PAUSE → User confirms
8. ✅ Load tasks.md → Fill in TODOs → PAUSE → User confirms
9. ✅ Close session

ANTI-PATTERN (DO NOT DO THIS):
❌ Skip running init_project.py
❌ Try to create files manually
❌ Generate content before structure exists
❌ Skip pauses between documents
❌ Complete skill in single response

CORRECT PATTERN (DO THIS):
✅ TodoWrite → Ask name → RUN SCRIPT → Files created
✅ Then: Load overview.md → Fill TODOs → PAUSE → Confirm
✅ Then: Load requirements.md → Fill TODOs → PAUSE → Confirm
✅ Then: Load design.md → Fill TODOs → PAUSE → Confirm
✅ Then: Load tasks.md → Fill TODOs → PAUSE → Confirm
✅ Then: Close session

SCRIPT RUNS FIRST - ALWAYS!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Create Project

Collaborative project design with step-by-step interactive elicitation using mental models.

## Purpose

The `create-project` skill creates project structure and guides you through collaborative planning. The workflow: **Create structure FIRST** (via script), **THEN** fill in the templates together.

**Key Features:**
- **Script-Generated Structure**: All files created immediately from templates
- **Collaborative Completion**: AI helps you fill in the TODO prompts
- **Mental Model-Guided**: Use proven frameworks when needed
- **Mandatory Pauses**: Review each document before proceeding
- **Separate Session Principle**: Project created now, executed later

---

## Two Modes

This skill operates in two modes based on system state:

### 1. Workspace Setup Mode
**When**: `User-Folders/` directory doesn't exist, but `01-memory/goals.md` has content
**Purpose**: Create initial workspace folder structure (10-15 min)
**Workflow**: See [workflows.md#workspace-setup](references/workflows.md#workspace-setup-workflow)

### 2. Project Creation Mode
**When**: `User-Folders/` exists and user wants to create a new project
**Purpose**: Full collaborative project planning (20-30 min)
**Workflow**: See [workflows.md#project-creation](references/workflows.md#project-creation-workflow)

---

## Mode Detection Logic

**CRITICAL**: Before starting any workflow, detect which mode to use.

1. **Check for User-Folders/**:
   ```bash
   ls -d User-Folders/ 2>/dev/null
   ```
   - IF exists → **PROJECT_CREATION mode**
   - IF not exists → Check next condition

2. **Check 01-memory/goals.md**:
   - Load: `01-memory/goals.md`
   - IF file has content (not just headers) → **WORKSPACE_SETUP mode**
   - IF file empty or missing → **PROJECT_CREATION mode** (but warn about uninitialized system)

**Decision Tree**:
```
User-Folders/ exists?
├── YES → PROJECT_CREATION mode
└── NO → goals.md has content?
    ├── YES → WORKSPACE_SETUP mode
    └── NO → PROJECT_CREATION mode (with warning)
```

---

## Quick Start

### The One True Workflow: Script-First

**There is only ONE way to create projects** - always run the script first, then collaboratively fill in the templates:

**Step 1: Run Script (< 1 minute)** ⚡
- Run `scripts/init_project.py "Project Name" --path 02-projects`
- Auto-generates empty project with all planning files
- Creates 4 numbered folders with template files

**Step 2: Collaborative Planning (15-30 minutes)** 🤔
- Load each planning file and fill in TODO prompts together
- AI guides you through planning with mental models and questions
- Mandatory pauses between documents for review

**Step 3: Save & Execute Later** 💾
- Close session to save progress
- Execute project in a separate session with clean context

### Workflow Steps

1. **Detect mode** using logic above (Workspace Setup vs Project Creation)
2. **Run init_project.py** to create structure immediately
3. **Display** created structure
4. **Load workflow** from [workflows.md](references/workflows.md)
5. **Load mental models** from [mental-models.md](references/mental-models.md) when needed
6. **Follow workflow step-by-step** with mandatory pauses
7. **Close session** to save state

---

## Mental Models

This skill uses mental model-guided elicitation for requirements, design, and tasks.

**Key Principle**: Let the user PICK the mental model(s) they want to use!

**Complete Catalog**: See [mental-models.md](references/mental-models.md)

**Categories Available** (30+ models):
- Cognitive Models (First Principles, Systems Thinking, etc.)
- Collaborative Models (Stakeholder Mapping, etc.)
- Diagnostic Models (Root Cause Analysis, Pre-Mortem, etc.)
- Strategic Models (SWOT, PESTLE, etc.)
- Analytical Models (Decision Matrix, Cost-Benefit, etc.)
- Creative Models (Design Thinking, SCAMPER, etc.)
- Operational Models (Kanban, OKR, Lean Canvas, etc.)
- Validation Models (Hypothesis Testing, Red Team, etc.)

**Selection Guidance**: See [mental-models.md#mental-model-selection-matrix](references/mental-models.md#mental-model-selection-matrix)

---

## Resources

### scripts/
- **init_project.py**: ⚡ NEW! Quick project template generator
  - Auto-generates empty project with all planning files
  - Auto-assigns next available project ID
  - Creates overview.md, requirements.md, design.md, tasks.md from templates
  - Perfect for: When you want structure now, fill in details later
  - Usage: `python scripts/init_project.py "Project Name" --path 02-projects`

- **create-project.py**: Legacy script for manual folder creation
  - Creates `02-projects/{ID}-{name}/` with proper structure
  - Requires manual ID specification
  - Usage: `python scripts/create-project.py <name> --id <ID>`

### references/
- **workflows.md**: Complete interactive planning workflows for both modes (with TOC)
- **mental-models.md**: Full mental models catalog (30+ models with TOC)
- **project-schema.yaml**: YAML frontmatter schema documentation

---

## Error Handling

### Invalid Project ID/Name
- Explain validation rule clearly
- Show example of correct format
- Suggest correction

### Project Already Exists
- Inform user project exists
- Offer options: different name, different ID, or load existing

### Memory Files Missing
- Warn user: "Memory files not initialized"
- Suggest: "Please run 00-setup-memory project first"
- DO NOT create project

### User Abandons Mid-Creation
- Save partial work to temp file
- Inform: "Progress saved. Say 'continue project creation' to resume."

### User Skips Review
- Remind: "It's important we get this right!"
- Gently insist on review before proceeding

---

## Why This Design?

**Why Interactive?**
- Quality over speed: Thoughtful planning prevents rework
- User ownership: Collaborative design ensures buy-in
- Learning: Mental models teach strategic thinking
- Accuracy: Pauses catch issues early

**Why Mandatory Pauses?**
- Validation: User confirms understanding before proceeding
- Iteration: Catch issues before they cascade
- Ownership: User feels involved, not just spectator
- Quality: Better planning = smoother execution

**Why Separate Session?**
- Context management: Clean boundaries between planning and execution
- Focus: Execution session loads only execution context
- Memory: close-session properly saves state between phases
- UX: Matches natural work rhythm (plan now, execute later)

---

**Integration**:
- close-session automatically updates project-map.md every session
- validate-system checks project structure integrity
- Skills can reference project outputs in their workflows

---

**Remember**: This is a COLLABORATIVE DESIGN SESSION, not a quick generation tool. The time invested in thorough planning pays dividends during execution!
