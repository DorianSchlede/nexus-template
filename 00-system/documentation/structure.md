# Nexus-v3 Complete Structure Documentation

**Comprehensive documentation of all folders, files, purposes, and contents**

**Last Updated**: 2025-11-03

---

## Table of Contents

1. [Root Level](#root-level)
2. [.claude/ - Claude Code Configuration](#claude---claude-code-configuration)
3. [00-system/ - System Framework](#00-system---system-framework)
4. [01-memory/ - Context Persistence](#01-memory---context-persistence)
5. [02-builds/ - Temporal Work](#02-builds---temporal-work)
6. [03-skills/ - User Skills](#03-skills---user-skills)
7. [04-workspace/ - User Content](#04-workspace---user-content)

---

## Root Level

### Files

#### README.md
**Purpose**: Primary entry point documentation for the Nexus-v3 system

**Contents**:
- What is Nexus-v3 (conversational work organization system)
- Key features (builds, skills, memory, navigation, auto-detection)
- Quick start guide (load claude.md, follow onboarding)
- System requirements (Claude AI, optional Python/MCP)
- Folder structure overview
- How it works (builds, skills, memory, system skills)
- Onboarding journey (5 builds, ~1.5-2 hours total)
- Key commands (create build, create skill, validate, done)
- Design philosophy (simplicity, guidance through structure, context preservation, progressive disclosure)
- Optional features (Python hooks, MCP integrations)
- Troubleshooting guide
- Version information

**Key Sections**:
- Overview of all 5 system skills
- Detailed onboarding journey timeline
- Complete folder structure diagram
- Support resources

---

#### CLAUDE.md
**Purpose**: Initialization file for Claude AI - loads the orchestrator

**Contents**:
- Ultra-simple initialization instructions
- Link to orchestrator: `00-system/core/orchestrator.md`
- Explains the initialization sequence:
  1. Orchestrator guides initialization
  2. Run startup script: `nexus-load --startup`
  3. Display dynamic menu
  4. Begin working

**Usage**: Load this file in Claude Desktop or Claude Code to start a session

**Philosophy**: Minimal entry point - delegates to orchestrator for all logic

---

## .claude/ - Claude Code Configuration

### Purpose
Configuration folder for Claude Code integration

### Files

#### settings.local.json
**Purpose**: Local Claude Code settings (user-specific, not committed to git)

**Typical Contents**:
- Editor preferences
- Workspace-specific settings
- Local paths and configurations

**Note**: This file is user-specific and typically gitignored

---

## 00-system/ - System Framework

### Purpose
Core framework infrastructure - all built-in system components

### Structure
```
00-system/
├── system-map.md           # Master navigation hub
├── core/                   # Core infrastructure
├── documentation/          # System documentation
├── scripts/                # Utility scripts
└── skills/                 # Built-in system skills (7 skills)
```

---

### 00-system/system-map.md

**Purpose**: Master navigation hub for the entire Nexus-v3 system

**Contents**:
- Complete system overview
- Navigation hub with links to all maps
- Core capabilities explanation
- Detailed folder structure with descriptions
- Core entities documentation (Builds, Skills, Memory)
- Core infrastructure explanation (nexus-loader.py, orchestrator.md)
- YAML metadata format documentation
- System skills reference table
- Auto-generation explanation (metadata scanning, progressive disclosure)
- File naming conventions
- Startup loading sequence
- Support & resources section

**Key Features**:
- Central intelligence for system navigation
- Links to all 4 navigation maps (system, memory, build, workspace)
- Complete YAML format examples for both builds and skills
- Progressive disclosure philosophy explained
- Token budget monitoring information

**Loaded**: Every session via `--startup` command

---

### 00-system/core/

**Purpose**: Core infrastructure components that run the system

#### orchestrator.md

**Purpose**: AI decision logic and routing - defines how Claude processes user requests

**Contents**:
- **Design Principle**: Ultra-simple, no complex state detection, state logic in data files
- **Initialization Sequence**:
  - Step 1: Run startup script (loads 5 core files + generates metadata)
  - Step 2: Display dynamic menu (based on loaded content)
  - Step 3: Smart routing (skills → builds → state checks → session end → general work)
  - Step 4: Context loading rules
- **3-State Model**:
  - Goals empty → Run 00-define-goals build
  - Goals set + no workspace → Create workspace structure
  - Both exist → System operational
- **Smart Routing Logic**:
  1. Match against skill triggers (from system-map.md)
  2. Match against build names (from build-map.md)
  3. Check initialization state (simple 3-state)
  4. Check session end signals (done, finish, close)
  5. Handle general work requests
- **Special Handling**: plan-build skill warning system (enforce collaborative design)
- **Context Loading Rules**: What to load always, what to load on-demand, what never to load
- **Error Handling**: Missing files, user confusion, system issues
- **Using nexus-loader.py**: All available commands and why to use the script
- **Critical Principles**:
  - NO complex conditional logic in orchestrator
  - State in data files (build-map.md), not code
  - Dynamic menu based on file content
  - Always load same files at initialization
- **Example Session Flows**: First time user, workspace setup, operational state

**Key Philosophy**:
- Orchestrator is ultra-minimal - it loads data and routes commands
- Actual guidance/logic lives in build files themselves
- State detection from data files, not hard-coded logic

**Location Note**: Lives in `core/` because it's fundamental infrastructure, loaded every session

---

#### nexus-loader.py

**Purpose**: Python script for loading context and generating metadata

**What It Does**:
- Loads core files at session start (5 files)
- Scans all builds in `02-builds/` for YAML metadata
- Scans all skills in `00-system/skills/` and `03-skills/` for YAML metadata
- Generates current timestamp
- Returns structured JSON output
- Monitors token budget (warns if >7,000 tokens)
- Provides on-demand loading for specific builds/skills
- Auto-loads skill resources (references, scripts, assets)

**Commands**:
```bash
# Session startup (5 files + metadata generation)
nexus-load --startup

# Load specific build (all planning files + metadata)
nexus-load --build {build-id}

# Load specific skill (SKILL.md + auto-load declared resources)
nexus-load --skill {skill-name}

# List all builds (YAML metadata only, no file contents)
nexus-load --list-builds

# List all skills (YAML metadata only, no file contents)
nexus-load --list-skills

# Show token usage breakdown
nexus-load --show-tokens
```

**Output Format**:
```json
{
  "loaded_at": "2025-11-03T12:22:48",
  "bundle": "startup",
  "files": { /* file contents */ },
  "metadata": {
    "builds": [ /* build YAML data */ ],
    "skills": [ /* skill YAML data */ ]
  },
  "stats": { /* counts and totals */ }
}
```

**Benefits**:
- [OK] Structured JSON output (consistent format)
- [OK] Automatic YAML parsing (no manual frontmatter extraction)
- [OK] Auto-detection triggers extracted from descriptions
- [OK] Task counting and progress calculation
- [OK] Auto-loading of skill resources
- [OK] Token budget monitoring
- [OK] Timestamp generation
- [OK] Stats aggregation

**Key Principle**: Use this script for ALL context loading - never use Glob or manual file reads

---

### 00-system/documentation/

**Purpose**: System documentation and guides

#### framework-overview.md

**Purpose**: Complete master guide to understanding the entire Nexus-v3 system

**Contents** (584 lines):
- **What is Nexus-v3**: Self-guiding work organization through AI
- **Core Philosophy**: YAML-driven, progressive disclosure, state in data, context preservation, self-documenting
- **The Four Navigation Maps**:
  1. System Map - Framework structure
  2. Memory Map - Context persistence
  3. Build Map - System state and current focus
  4. Workspace Map - Custom folder structure
- **System Structure**: Complete folder hierarchy with descriptions
- **How It All Works Together**: Session start → during work → session end flows
- **Key Concepts**:
  - Builds (temporal work with lifecycle)
  - Skills (reusable workflows with V2.0 format)
  - Memory (context persistence)
  - Auto-Detection (YAML-driven matching)
- **Getting Started**: First session guide, typical session flow
- **Core Infrastructure**: nexus-loader.py and orchestrator.md explained
- **Documentation Reference**: Where to find all docs
- **Design Principles**: 5 core principles explained
- **Key Terminology**: Glossary of terms
- **System Workflows**: Creating build, creating skill, working on build, ending session
- **Why Nexus-v3**: Problems it solves, key benefits
- **Need Help**: Navigation, building, understanding

**Target Audience**: New users and anyone wanting to understand the system deeply

**Recommended Reading**: Start here if new to Nexus-v3

---

#### yaml-quick-reference.md

**Purpose**: Quick reference guide for V2.0 skill YAML format

**Contents**:
- V2.0 format specification (minimal metadata)
- Required fields: name, description
- Description field best practices (trigger phrases)
- Example skill YAML
- Progressive disclosure explanation
- Common patterns
- What NOT to include (deprecated V1 fields)

**Target Audience**: Users creating new skills

**Use Case**: Quick lookup when creating skills

---

#### skill-file-format.md

**Purpose**: Specification for .skill file packaging format

**Contents**:
- .skill file structure (ZIP format)
- Required files (SKILL.md)
- Optional folders (references/, scripts/, assets/)
- Packaging guidelines
- Distribution format
- Installation process

**Target Audience**: Advanced users distributing skills

**Use Case**: Packaging skills for sharing

---

#### archived/

**Purpose**: Historical documentation (deprecated or superseded)

**Contents**:
- `skill-yaml-migration.md` - Guide for migrating V1 to V2 format (516 lines, obsolete)
- `yaml-specification.md` - Complete V1 YAML specification (422 lines, superseded by yaml-quick-reference.md)

**Note**: These files are preserved for historical reference but no longer used

**Reason for Archival**: Applied "Just-In-Time Documentation" pattern - moved guidance into workflows, reduced docs from 6 files (2,100 lines) to 3 files (800 lines)

---

### 00-system/scripts/

**Purpose**: Utility scripts for system maintenance

#### validate-tasks.py

**Purpose**: Python script to validate task checkbox counts against YAML metadata

**What It Does**:
- Scans all build tasks.md files
- Counts checkboxes (total and completed)
- Compares against YAML metadata in overview.md
- Reports discrepancies
- Validates data integrity

**Usage**: Run during system validation to ensure task tracking accuracy

**Invoked By**: validate-system skill

---

### 00-system/skills/

**Purpose**: Built-in system skills (7 core skills)

**Philosophy**: These are system-level skills that maintain framework integrity. User skills go in `03-skills/`.

---

#### add-integration/

**Purpose**: Guide MCP server setup to connect external tools

**Trigger**: "add integration", "connect tool", "setup MCP", "integrate with"

**Files**:
- `SKILL.md` - Main skill workflow
- `references/integration-ideas.md` - Curated list of useful integrations
- `references/mcp-guide.md` - Complete MCP server guide
- `references/mcp-introduction.md` - Introduction to MCP concept
- `references/mcp-setup-guide.md` - Step-by-step setup instructions
- `references/troubleshooting-guide.md` - Common issues and solutions

**What It Does**:
1. Explains MCP (Model Context Protocol)
2. Guides through integration selection (GitHub, Slack, Notion, Google Drive, etc.)
3. Walks through installation process
4. Helps with credential setup
5. Tests connection
6. Documents integration in core-learnings.md

**Use Case**: Connect Nexus to external tools and services

---

#### archive-build/

**Purpose**: Move completed builds to `_archived/` folder for clean build list

**Trigger**: "archive build", "archive [build-name]", "move to archived"

**Files**:
- `SKILL.md` - Main skill workflow

**What It Does**:
1. Confirms build is COMPLETE
2. Moves build folder to `02-builds/_archived/`
3. Updates build-map.md
4. Cleans up active build list
5. Preserves build for historical reference

**Use Case**: Maintain clean active build list by archiving completed work

---

#### close-session/

**Purpose**: End session, update memory, save progress, clean temporary files

**Trigger**: "done", "finish", "complete", "close", "wrap up", "end session", or when any system skill/build completes

**Files**:
- `SKILL.md` - Main skill workflow
- `references/` - Additional documentation

**What It Does**:
1. Asks which tasks were completed in current session
2. Updates task checkboxes in tasks.md
3. Recalculates task counts and progress
4. Updates build-map.md (current focus, recent decisions)
5. Generates session report in session-reports/
6. Cleans temporary working files
7. Preserves all context for next session

**Key Feature**: Automatically ensures context persistence

**Philosophy**: Every session should end with close-session to maintain system integrity

---

#### plan-build/

**Purpose**: Create new temporal work builds with AI-guided collaborative planning

**Trigger**: "create build", "new build", "start something new"

**Files**:
- `SKILL.md` - Main skill workflow (collaborative design session)
- `build-schema.yaml` - Complete build YAML specification
- `references/advanced-elicitation.md` - Advanced questioning techniques
- `references/build-creation-workflow.md` - Detailed workflow documentation
- `references/workspace-setup-workflow.md` - Special workflow for first-time workspace setup
- `scripts/plan-build.py` - Python script for folder creation and file generation

**What It Does**:
1. **CRITICAL**: Initializes TodoWrite (MANDATORY first step)
2. **Interactive Elicitation**: Asks deep questions about build purpose, success criteria, constraints
3. **Mental Model Application**: Uses first-principles thinking, systems thinking, etc.
4. **Collaborative Document Creation**:
   - overview.md (with YAML metadata)
   - requirements.md
   - design.md
   - tasks.md (checkbox list)
5. **MANDATORY PAUSES**: User must review each document before proceeding
6. **User Confirmation**: Required before each step
7. Creates folder structure: `02-builds/{ID}-{name}/01-planning/`, `02-working/`, `03-outputs/`
8. Updates build-map.md

**Special Handling**: Orchestrator displays critical warning before loading this skill to enforce collaborative design philosophy

**Philosophy**: Builds are created through collaborative design sessions, NOT solo generation. AI must engage user interactively.

**Warning System**:
```
-------------------------------------------------------
[!] CRITICAL: plan-build is a COLLABORATIVE DESIGN SESSION
-------------------------------------------------------
This skill REQUIRES:
1. [OK] TodoWrite initialization (Step 1 - MANDATORY)
2. [OK] Interactive elicitation with user (NOT solo generation)
3. [OK] MANDATORY PAUSES after each document (user must review)
4. [OK] User confirmation before proceeding to next step

Do NOT:
[ERROR] Skip TodoWrite
[ERROR] Generate all documents at once
[ERROR] Proceed without user confirmation
[ERROR] Skip mental model application
```

---

#### create-skill/

**Purpose**: Create new reusable skills with AI-guided workflow extraction

**Trigger**: "create skill", "save workflow", "make this reusable"

**Files**:
- `SKILL.md` - Main skill workflow
- `references/description-guide.md` - How to write effective descriptions
- `references/error-scenarios.md` - Common errors and how to avoid them
- `references/naming-guidelines.md` - Skill naming best practices
- `references/skill-format-template.md` - Template for skill structure
- `references/splitting-large-skills.md` - When and how to split skills
- `scripts/create-skill.py` - Python script for skill creation
- `scripts/migrate-skill-yaml.py` - Migrate V1 to V2 format
- `scripts/package-skill.py` - Package skill as .skill file for distribution
- `scripts/validate-skill.py` - Validate skill format and metadata

**What It Does**:
1. **Extraction Mode**: Analyzes chat history to extract workflow pattern
2. **From-Scratch Mode**: Guides user through workflow definition
3. **Intelligent Naming**: Suggests verb-based names (e.g., "generate-report", "analyze-data")
4. **V2.0 Format**: Creates minimal YAML (name + description only)
5. **Progressive Disclosure**: Recommends references/ folder for detailed docs
6. **Workflow Writing**: Guides clear, actionable workflow steps
7. Creates folder structure: `03-skills/{skill-name}/SKILL.md`, optional `references/`, `scripts/`, `assets/`
8. Automatic system integration (skill appears in metadata scan)

**Philosophy**: Skills capture reusable workflows after doing something 2-3 times

**Best Practices**:
- Verb-based names (action-focused)
- Clear trigger phrases in description
- Keep SKILL.md under 500 lines
- Use references/ for detailed documentation
- Test workflow before finalizing

---

#### update-tasks/

**Purpose**: Quick task checkbox updates for current build without closing session

**Trigger**: "update tasks", "check off tasks", "mark tasks complete", "mark tasks done"

**Files**:
- `SKILL.md` - Main skill workflow

**What It Does**:
1. Identifies current build from build-map.md
2. Displays current tasks from tasks.md
3. Asks which tasks to mark complete
4. Updates checkboxes in tasks.md
5. Recalculates progress in overview.md YAML
6. Continues session (does NOT close)

**Use Case**: Mid-session progress updates without full session closure

**Difference from close-session**:
- update-tasks = quick task update, continue working
- close-session = end session, full memory update, session report

---

#### validate-system/

**Purpose**: Validate Nexus-v3 system integrity and auto-fix common issues

**Trigger**: "validate system", "check system", "fix problems"

**Files**:
- `SKILL.md` - Main skill workflow
- `references/validation-checks.md` - Complete list of validation checks
- `references/report-templates.md` - Templates for validation reports

**What It Does**:
1. **Folder Structure Checks**: Verifies all required folders exist
2. **Metadata Validation**: Checks YAML format in builds and skills
3. **Task Tracking**: Runs validate-tasks.py to verify checkbox counts
4. **Framework Consistency**: Ensures maps are up-to-date
5. **Auto-Repair**: Recreates missing template files
6. **Hook Execution**: Runs any Python validation hooks in hooks/
7. **Comprehensive Report**: Shows all issues found and fixed

**Validation Checks**:
- Required folders (00-system, 01-memory, 02-builds, 03-skills, 04-workspace)
- Required files (system-map.md, memory-map.md, build-map.md, goals.md, workspace-map.md)
- YAML frontmatter format
- Task checkbox counts vs metadata
- Navigation map accuracy
- File naming conventions

**Auto-Fix Capabilities**:
- Creates missing folders
- Recreates template files
- Fixes malformed YAML
- Regenerates maps from metadata

**Use Case**:
- Troubleshooting system issues
- After manual file edits
- Periodic system health checks
- Recovery from errors

---

## 01-memory/ - Context Persistence

### Purpose
Context persistence across AI sessions - "Never start from scratch"

### Structure
```
01-memory/
├── memory-map.md           # Navigation hub for memory system
├── goals.md                # User objectives and success criteria
├── roadmap.md              # Short/long-term plans
├── core-learnings.md       # Patterns and insights
└── session-reports/        # Historical session summaries
```

---

### memory-map.md

**Purpose**: Navigation hub for the memory system

**Contents**:
- Memory files overview (goals, roadmap, core-learnings, session-reports)
- Links to related maps (system, build, workspace)
- How memory works (session start, during work, session end)
- Maintenance philosophy (living documentation)

**Key Principle**: Memory is living documentation that evolves over time

**Loaded**: Every session via `--startup` command

---

### goals.md

**Purpose**: User objectives and success criteria

**Initial State**: Placeholder template prompting user to run 00-define-goals build

**Contents After Initialization**:
- What you want to achieve
- Why it matters to you
- What success looks like
- Your work context (role, pattern, workload, challenges)

**Updated**:
- During 00-define-goals build (first time)
- Manually as goals evolve
- Via close-session when major shifts occur

**Use Case**: Provides context for all AI sessions about user's objectives

**Loaded**: Every session via `--startup` command

---

### roadmap.md

**Purpose**: Short and long-term plans

**Contents**:
- Next 30/60/90 day priorities
- Future ideas and possibilities
- Strategic direction
- Milestones and timeframes

**Updated**:
- During strategic planning discussions
- Via close-session when plans shift
- Manually when reviewing progress

**Use Case**: Maintains strategic context across sessions

**Loaded**: On-demand during strategic discussions

---

### core-learnings.md

**Purpose**: Patterns, insights, and best practices discovered

**Contents**:
- **Patterns Discovered**: Workflows that work well
- **Best Practices**: Personal operating procedures validated through use
- **System Preferences**: How user prefers Nexus to work
- **Integrations**: MCP integrations documentation
- **Optimization Suggestions**: AI-observed improvement opportunities

**Updated**: Via close-session skill when insights emerge

**Philosophy**: Accumulates knowledge over time - system learns what works for user

**Use Case**: Preserves institutional knowledge across sessions

**Loaded**: On-demand when relevant patterns identified

---

### session-reports/

**Purpose**: Historical work summaries (chronological archive)

**Contents**: Individual markdown files, one per session

**File Format**: `YYYY-MM-DD-{brief-description}.md`

**Each Report Contains**:
- Session date and duration
- Builds worked on
- Tasks completed
- Decisions made
- Insights discovered
- Next steps

**Created By**: close-session skill (automatic)

**Use Case**:
- Review past work
- Understand build history
- Track long-term progress
- Search for previous decisions

**Note**: Build historical record over time - searchable archive

---

#### .gitkeep

**Purpose**: Preserve empty directory in git

**Reason**: Git doesn't track empty folders, .gitkeep ensures session-reports/ exists

---

#### Example Session Reports

**2025-11-02-documentation-reorganization.md**: Documentation cleanup session
**2025-11-02-session.md**: General work session
**2025-11-02-task-tracking-fix.md**: Task tracking system fix

---

## 02-builds/ - Temporal Work

### Purpose
Organize temporal work with beginning, middle, and end

### Structure
```
02-builds/
├── build-map.md              # System state and current focus
├── {ID}-{name}/                # Individual builds
│   ├── 01-planning/
│   │   ├── overview.md         # YAML metadata + description
│   │   ├── requirements.md
│   │   ├── design.md
│   │   └── tasks.md            # Checkbox task list
│   ├── 02-working/             # Work-in-progress files
│   └── 03-outputs/             # Final deliverables
└── _archived/                  # Completed builds
```

---

### build-map.md

**Purpose**: Track system state, current focus, and recent decisions

**Contents**:
- **System State**: Logic for initialization detection (3-state model)
  - IF goals.md missing/empty → Uninitialized → Load 00-define-goals
  - IF onboarding not complete → Load current onboarding build
  - IF onboarding complete → System operational
- **Current Focus**:
  - Last updated timestamp
  - Active build name
  - Context description
- **Recent Decisions**: Chronological log of important decisions with dates and rationale
- **Notes**: Metadata generation explanation

**Key Principle**: Contains state detection logic, not the orchestrator

**Updated**: By close-session skill after every session

**Loaded**: Every session via `--startup` command

**Example Recent Decision**:
```
- **2025-11-02**: Documentation reorganization - Applied "Just-In-Time Documentation" pattern:
  moved description-guide and splitting-large-skills into create-skill/references/,
  archived yaml-specification.md (422 lines) and yaml-migration guide (516 lines),
  created yaml-quick-reference.md (50 lines). Reduced docs from 6 files (2,100 lines)
  to 3 files (800 lines). Guidance now embedded in workflows where needed.
```

---

### Build Structure: {ID}-{name}/

**Naming Convention**: `{ID}-{name}`
- ID: Zero-padded numeric (00, 01, ..., 10, 11)
- Name: lowercase-with-hyphens
- Example: `05-website-development`

---

#### 01-planning/

**Purpose**: All planning documents (source of truth for build)

##### overview.md

**Purpose**: Build overview with YAML metadata

**YAML Frontmatter**:
```yaml
---
id: 05-website-development
name: Website Development
status: IN_PROGRESS
description: Load when user mentions "website", "web dev", "homepage"
created: 2025-11-01
last_worked: 2025-11-03
progress: 0.35
tasks_completed: 3
tasks_total: 8
tags: [web, design]
related_builds: [03-branding]
load_with: ["planning/requirements.md", "planning/design.md", "planning/tasks.md"]
---
```

**Markdown Content**:
- Build overview and purpose
- Success criteria
- Constraints and assumptions
- Timeline

**Key Fields**:
- `description`: Used for auto-detection (AI matches user messages against this)
- `status`: PLANNING, IN_PROGRESS, COMPLETE
- `progress`: Auto-calculated from tasks (0.0 to 1.0)
- `tasks_completed` / `tasks_total`: Auto-counted from tasks.md checkboxes

**Updated**:
- Created by plan-build skill
- Progress auto-updated by close-session and update-tasks skills
- Status manually updated or via close-session

---

##### requirements.md

**Purpose**: Detailed requirements and specifications

**Contents**:
- Functional requirements
- Non-functional requirements
- User stories or use cases
- Acceptance criteria
- Dependencies

**Created By**: plan-build skill (collaborative session)

---

##### design.md

**Purpose**: Design decisions and approach

**Contents**:
- Architecture decisions
- Technology choices
- Design patterns
- Interface designs
- Data models

**Created By**: plan-build skill (collaborative session)

---

##### tasks.md

**Purpose**: Checkbox task list (single source of truth for progress)

**Format**:
```markdown
# Tasks

## Phase 1: Planning
- [x] Define requirements
- [x] Create design mockups
- [ ] Review with stakeholders

## Phase 2: Development
- [ ] Build homepage
- [ ] Implement navigation
- [ ] Add contact form
```

**Key Principle**: Checkbox state is THE source of truth
- `[ ]` = incomplete task
- `[x]` = completed task

**Counted By**: nexus-loader.py automatically counts checkboxes

**Updated By**:
- close-session skill (marks tasks complete)
- update-tasks skill (mid-session updates)
- Manual edits

**Used For**: Progress calculation, current task identification

---

#### 02-working/

**Purpose**: Work-in-progress files (temporary workspace)

**Contents**:
- Draft documents
- Code in progress
- Temporary notes
- Intermediate outputs

**Cleaned By**: close-session skill (moves completed items to outputs)

**Note**: Ephemeral folder - contents change frequently

---

#### 03-outputs/

**Purpose**: Final deliverables and completed work

**Contents**:
- Completed documents
- Final code
- Reports
- Deliverables

**Note**: Permanent archive - preserved after build completion

---

### Example Builds in Template

#### 00-define-goals/

**Purpose**: Onboarding build - initialize memory system

**Trigger**: "build", "00-define-goals", "define goals"

**Tasks** (17 tasks):
1. Learn what Builds are
2. Learn what Skills are
3. Learn what Memory is
4. Discovery questions (role, work pattern, workload, challenges)
5. Define goals (objectives, success metrics)
6. Set up Memory files

**Status**: PLANNING (template state)

**Duration**: 15-20 minutes

**Outcome**: Initialized goals.md with user objectives

---

#### 01-build-nexus-v3/

**Purpose**: Meta-build for building the Nexus-v3 system itself

**Trigger**: "nexus", "build build", "nexus-v3", "template system"

**Tasks**: 624 tasks (extensive system build)

**Status**: IN_PROGRESS

**Contains**: Complete build history and outputs in 03-outputs/

**Outputs**:
- ai-focused-framework-complete.md
- folder-reorganization-complete.md
- framework-cleanup-complete.md
- nexus-v3-reorganization-complete.md
- refinements-summary.md
- root-reorganization-complete.md
- script-cleanup-executed.md
- script-cleanup-recommendations.md
- VALIDATION-REPORT.md
- yaml-integration-complete.md

**Note**: This is the build that created the template you're using

---

#### 06-yaml-metadata-integration/

**Purpose**: Integrate YAML metadata system

**Trigger**: "yaml", "yaml metadata", "06-yaml-metadata-integration"

**Tasks**: 97 tasks

**Status**: PLANNING

**Outputs**: Scripts for metadata handling (load-metadata.py, query-metadata.py, regenerate-maps.py)

---

#### 07-claude-skill-adaptation/

**Purpose**: Adapt Claude Skill System to Nexus

**Trigger**: "claude skill", "adapt skill system", "upgrade skills", "07-claude-skill-adaptation"

**Tasks**: 346 tasks

**Status**: PLANNING

**Contains**: References folder with Claude skill system research

---

#### 90-improvements/

**Purpose**: System improvements and enhancements

**Trigger**: "improvements", "loading sequence", "system issues", "nexus issues"

**Tasks**: 203 tasks

**Status**: PLANNING

**Use Case**: Tracking system enhancements and fixes

---

#### 99-improvements/

**Purpose**: Additional improvements tracking (alternative tracking)

**Tasks**: Multiple planning files

**Status**: PLANNING

**Outputs**:
- bugs.md - Bug tracking
- enhancements.md - Enhancement ideas
- ux-feedback.md - User experience feedback

---

### _archived/

**Purpose**: Completed builds (historical archive)

**Structure**: Same as active builds

**Moved By**: archive-build skill

**Contains**:
- 01-setup-structure (archived onboarding build)
- 02-practice-build (archived onboarding build)
- 03-practice-skill (archived onboarding build)
- 04-complete-setup (archived onboarding build)

**Use Case**: Preserve completed work while keeping active build list clean

---

## 03-skills/ - User Skills

### Purpose
User-created custom workflows (reusable skills)

### Structure
```
03-skills/
├── skill-map.md                # Auto-generated skills list
└── {skill-name}/               # Individual skills
    ├── SKILL.md                # YAML metadata + workflow
    ├── references/             # (optional) Detailed documentation
    ├── scripts/                # (optional) Automation code
    └── assets/                 # (optional) Files
```

---

### skill-map.md

**Purpose**: Auto-generated list of user skills

**Initial State**: Empty template ("No user skills yet")

**Contents After Skills Created**:
- List of all user skills from 03-skills/
- Skill names and brief descriptions
- Last updated timestamp

**Generated By**: close-session skill (automatic)

**Note**: System skills are documented in system-map.md, not here

**Use Case**: Quick reference of available user skills

---

### User Skill Structure: {skill-name}/

**Naming Convention**: `{skill-name}`
- Format: lowercase-with-hyphens
- Prefer verb-based names: `generate-report`, `analyze-data`, `create-proposal`

---

#### SKILL.md

**Purpose**: Main skill file with V2.0 YAML metadata and workflow

**V2.0 YAML Format** (minimal metadata):
```yaml
---
name: weekly-status-report
description: Load when user says "status report", "weekly update", "progress summary". Generate comprehensive weekly work summary with completed tasks, decisions made, and next steps.
---
```

**Required Fields**:
- `name`: Skill identifier (matches folder name)
- `description`: Natural language description with trigger phrases

**Markdown Content**:
- Clear workflow steps
- Numbered or bulleted instructions
- Expected inputs and outputs
- Examples if helpful

**Best Practices**:
- Keep under 500 lines
- Use references/ for detailed documentation
- Clear, actionable steps
- Include trigger phrases in description

**Created By**: create-skill skill

---

#### references/ (optional)

**Purpose**: Detailed documentation that doesn't fit in SKILL.md

**Contents**:
- Extended guides
- Background information
- Examples and templates
- Best practices

**Loaded**: On-demand via `load_references` in YAML (if using legacy format) or manually requested

**Philosophy**: Progressive disclosure - detailed docs loaded only when needed

---

#### scripts/ (optional)

**Purpose**: Automation code (Python, shell, etc.)

**Contents**:
- Python scripts for automation
- Shell scripts for system tasks
- Helper utilities

**Loaded**: On-demand via `load_scripts` in YAML (if using legacy format) or manually requested

**Use Case**: Skills that need programmatic automation

---

#### assets/ (optional)

**Purpose**: Files needed by the skill

**Contents**:
- Templates
- Configuration files
- Data files
- Images or media

**Loaded**: On-demand via `load_assets` in YAML (if using legacy format) or manually requested

**Use Case**: Skills that need supplementary files

---

## 04-workspace/ - User Content

### Purpose
User-defined custom folder structure for organizing their work

### Structure
```
04-workspace/
├── workspace-map.md        # User's custom folder guide
└── [User's folders]/       # Custom organization (clients, research, templates, etc.)
```

---

### workspace-map.md

**Purpose**: Document user's custom folder structure

**Initial State**: Template with example structure

**Contents After Setup**:
- User's folder structure diagram
- Folder descriptions (purpose of each folder)
- Organizational philosophy
- Tips for maintenance

**Example Structure**:
```
04-workspace/
├── Clients/              # Client builds and deliverables
│   ├── acme-corp/        # Acme Corporation (2024-2025)
│   └── beta-inc/         # Beta Inc partnership
├── Research/             # Industry research and competitive analysis
└── Templates/            # Reusable templates and resources
```

**Created By**: plan-build skill during workspace setup (Session 2)

**Updated**: Manually by user when reorganizing workspace

**Loaded**: Every session via `--startup` command

**Key Principle**: Workspace is YOURS - organize however makes sense for your work

---

### User Folders

**Created By**: User via plan-build skill or manually

**Contents**: Whatever the user needs

**Common Patterns**:
- Clients/ - Client work organization
- Builds/ - Real-world builds (not Nexus builds)
- Research/ - Reference materials
- Templates/ - Reusable templates
- Archive/ - Historical files

**Note**: This is the user's content area - completely flexible

---

## Design Patterns and Principles

### 1. Progressive Disclosure

**Philosophy**: Load minimum at start, more context just-in-time

**Implementation**:
- **Session Start**: Only 5 files + metadata (~7,000 tokens)
- **Skill Trigger**: SKILL.md loaded + auto-load resources
- **Build Work**: Full planning files loaded on-demand
- **Strategic Discussion**: Roadmap/learnings loaded when needed

**Benefit**: Efficient token usage, faster initialization

---

### 2. YAML-Driven Auto-Detection

**Philosophy**: Everything has metadata describing when to load it

**Implementation**:
- `description` field contains trigger phrases
- AI matches user messages against descriptions
- Context loads automatically when match found

**Example**:
```yaml
description: Load when user mentions "website", "web dev", "homepage"
```
User says: "let's work on the homepage"
→ AI loads website build automatically

---

### 3. State in Data Files

**Philosophy**: Logic lives in data files, not code

**Implementation**:
- build-map.md contains state detection logic
- tasks.md checkboxes are source of truth for progress
- Orchestrator reads data and follows instructions

**Benefit**: System behavior is transparent and editable

---

### 4. Context Preservation

**Philosophy**: Never start from scratch - preserve all context

**Implementation**:
- close-session skill updates memory after every session
- Session reports build historical archive
- Build files preserve all decisions
- core-learnings accumulates patterns over time

**Benefit**: Each session builds on previous work

---

### 5. Self-Documenting

**Philosophy**: System generates navigation from metadata

**Implementation**:
- nexus-loader.py scans YAML metadata at runtime
- Maps generated from file structure
- Always shows current state (no stale maps)

**Benefit**: Documentation is always accurate

---

## Token Budget Management

### Session Startup

**Loaded Files** (~7,000 tokens):
- system-map.md (~12,500 chars)
- memory-map.md (~2,000 chars)
- build-map.md (~2,800 chars)
- goals.md (~300 chars initially)
- workspace-map.md (~2,000 chars)

**Metadata** (variable):
- Builds: ~200 tokens per build YAML
- Skills: ~100 tokens per skill YAML

**Warning Threshold**: >7,000 tokens from metadata (3.5% of 200K context)

---

### On-Demand Loading

**Build Load** (~5,000-10,000 tokens):
- overview.md (~500-1,000 tokens)
- requirements.md (~1,000-3,000 tokens)
- design.md (~1,000-3,000 tokens)
- tasks.md (~500-2,000 tokens)

**Skill Load** (~2,000-5,000 tokens):
- SKILL.md (~2,000-5,000 tokens)
- References (if requested): Variable
- Scripts (if requested): Variable

---

### Best Practices

1. **Keep Skills Under 500 Lines**: Use references/ for detailed docs
2. **Break Large Builds into Phases**: Reduce task list size
3. **Archive Completed Builds**: Keep active list small
4. **Use Progressive Disclosure**: Don't load everything upfront
5. **Monitor Token Usage**: Use `--show-tokens` to check

---

## File Naming Conventions

### Builds
- Format: `{ID}-{name}`
- ID: Zero-padded (00, 01, ..., 10, 11)
- Name: lowercase-with-hyphens
- Examples: `05-website-development`, `10-client-onboarding`

### Skills
- Format: `{skill-name}`
- Name: lowercase-with-hyphens
- Prefer verb-based: `generate-report`, `analyze-data`, `create-proposal`
- Examples: `weekly-status-report`, `client-proposal-generator`

### User Folders
- Recommendation: lowercase-with-hyphens (consistency)
- Flexible: User chooses their convention

### Memory Files
- Fixed names: `goals.md`, `roadmap.md`, `core-learnings.md`
- Session reports: `YYYY-MM-DD-{description}.md`

---

## Summary Statistics

### Total System Files
- **Root**: 2 files (README.md, CLAUDE.md)
- **00-system**: ~50+ files (core infrastructure, 7 skills, documentation)
- **01-memory**: 4 core files + session reports folder
- **02-builds**: 1 map + 6 example builds + archived builds
- **03-skills**: 1 map (template for user skills)
- **04-workspace**: 1 map (user's custom structure)

### System Skills
7 built-in skills:
1. add-integration
2. archive-build
3. close-session
4. plan-build
5. create-skill
6. update-tasks
7. validate-system

### Core Infrastructure
- 1 Python loader script (nexus-loader.py)
- 1 orchestrator document (orchestrator.md)
- 4 navigation maps (system, memory, build, workspace)
- 1 master guide (framework-overview.md)

### Documentation
- 3 active docs (framework-overview, yaml-quick-reference, skill-file-format)
- 2 archived docs (yaml-specification, skill-yaml-migration)

---

## Version History

**Nexus-v3** - November 2025
- V2.0 skill format (minimal YAML)
- Progressive disclosure architecture
- YAML-driven auto-detection
- 4 specialized navigation maps
- Ultra-simple orchestrator
- Token budget optimization

**Key Improvements from Previous Versions**:
- Reduced metadata complexity (V2.0 format)
- Separated navigation into 4 specialized maps
- Moved core infrastructure to core/ folder
- Applied "Just-In-Time Documentation" pattern
- Enhanced task tracking automation
- Added archive-build skill
- Added update-tasks skill

---

## Quick Reference

### Essential Files to Load
1. **Session Start**: Run `nexus-load --startup`
2. **Read Orchestrator**: [00-system/core/orchestrator.md](00-system/core/orchestrator.md)
3. **Master Guide**: [00-system/documentation/framework-overview.md](00-system/documentation/framework-overview.md)

### Essential Maps
1. **System Map**: [00-system/system-map.md](00-system/system-map.md)
2. **Memory Map**: [01-memory/memory-map.md](01-memory/memory-map.md)
3. **Build Map**: [02-builds/build-map.md](02-builds/build-map.md)
4. **Workspace Map**: [04-workspace/workspace-map.md](04-workspace/workspace-map.md)

### Key Commands
- Session start: `nexus-load --startup`
- Create build: User says "create build"
- Create skill: User says "create skill"
- Validate system: User says "validate system"
- End session: User says "done for now"

---

**END OF STRUCTURE DOCUMENTATION**

This document provides complete documentation of all folders, subfolders, files, purposes, and core contents of the Nexus-v3 template system.
