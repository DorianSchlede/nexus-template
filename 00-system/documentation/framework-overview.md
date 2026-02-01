# Nexus Framework Overview

**The complete guide to understanding how Nexus works.**

> **Start Here**: If you're new to Nexus, this document explains the entire system and how all pieces fit together.

---

## 🧬 Living Knowledge Organism

```
╔═══════════════════════════════════════════════════════════════════════╗
║                                                                       ║
║  ALL FILES IN THIS SYSTEM ARE EXECUTABLE — NOT DOCUMENTATION!         ║
║                                                                       ║
║  Every .md file, .yaml config, and planning document is designed     ║
║  to be READ, LOADED, and EXECUTED by AI in conversation.             ║
║                                                                       ║
║  This is not a static knowledge base. It's a living, breathing       ║
║  organism that guides you through work, adapts to your context,      ║
║  and evolves with every interaction.                                 ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝
```

---

## [TARGET] What is Nexus?

**Nexus is a self-guiding work organization system** that runs entirely through conversation with Claude AI. It helps you:

- **Track temporal work** with builds (planning → execution → outputs)
- **Capture reusable workflows** with skills
- **Preserve context** across AI sessions with memory
- **Auto-detect what to load** via YAML-driven metadata
- **Never start from scratch** - the system remembers everything

### Core Philosophy

1. **Instruction-Driven**: Python script analyzes state and returns complete instructions (no AI interpretation)
2. **YAML-Driven**: Everything has metadata that describes when to load it
3. **Progressive Disclosure**: Load minimum at start, more context just-in-time
4. **State in Data**: Logic lives in data files, not code
5. **Context Preservation**: All context is saved, nothing is lost between sessions
6. **Self-Documenting**: System generates navigation from file metadata
7. **Skill-First Execution**: Skills have priority over builds in routing

---

## 🗺️ The Three Navigation Maps

Nexus has **3 specialized maps** that guide you through different aspects of the system:

### 1. [System Map](../system-map.md) [STATS]

**What it covers**: System framework and structure

**Use it for**:
- Understanding the folder structure
- Finding system skills (plan-build, create-skill, etc.)
- Learning how the loader and orchestrator work
- Seeing the complete system architecture

**Key sections**:
- System structure diagram
- Core infrastructure (loader, orchestrator)
- System skills reference (152 across 7 categories)
- YAML metadata formats
- Startup loading sequence

---

### 2. [Memory Map](../../01-memory/memory-map.md) 🧠

**What it covers**: Context persistence system

**Use it for**:
- Understanding how memory works
- Finding your goals, roadmap, and learnings
- Locating session reports
- Understanding what gets saved automatically

**Key files**:
- `goals.md` - Your objectives and success criteria
- `user-config.yaml` - Preferences, learning tracker
- `core-learnings.md` - Patterns and insights
- `integrations/` - Service configs (langfuse.yaml, etc.)

---

### 3. [Workspace Map](../../04-workspace/workspace-map.md) 🗺️

**What it covers**: Your custom folder structure

**Use it for**:
- Navigating your personal workspace
- Understanding your custom folder organization
- Finding client folders, research, templates, etc.

**Created during**: Build 01 (First Build) during onboarding

---

## [DIR] System Structure

```
Nexus/
│
├── CLAUDE.md                   [GO] LOAD THIS TO START!
│
├── 00-system/                  [STATS] SYSTEM FRAMEWORK
│   ├── system-map.md               Master system navigation
│   ├── core/                       Core infrastructure
│   │   ├── orchestrator.md             AI decision logic (minimal)
│   │   └── nexus-loader.py             Context loading + decision engine
│   ├── skills/                     System skills (152 across 7 categories)
│   │   ├── builds/                 plan-build, execute-build, archive-build
│   │   ├── integrations/           8 integrations (119 skills)
│   │   ├── learning/               Onboarding & tutorials
│   │   ├── skill-dev/              create-skill, import-skill
│   │   ├── system/                 close-session, list-skills
│   │   └── tools/                  mental-models, format-code
│   └── documentation/              System documentation
│       ├── framework-overview.md (THIS FILE)
│       └── product-overview.md
│
├── 01-memory/                  🧠 CONTEXT PERSISTENCE
│   ├── memory-map.md               Memory system navigation
│   ├── goals.md                    Your objectives
│   ├── user-config.yaml            Preferences & learning tracker
│   ├── core-learnings.md           Patterns & insights
│   └── integrations/               Service configs (langfuse.yaml, etc.)
│
├── 02-builds/                [LIST] TEMPORAL WORK
│   ├── active/                     Active builds in progress
│   │   └── {ID}-{name}/
│   │       ├── 01-planning/
│   │       │   ├── 01-overview.md      YAML metadata + purpose + success criteria
│   │       │   ├── 02-discovery.md     Research + questions + dependencies
│   │       │   ├── 03-plan.md          Approach + decisions + mental models
│   │       │   ├── 04-steps.md         Execution checklist with phases
│   │       │   └── resume-context.md   Cross-session continuity
│   │       ├── 02-resources/       Reference materials
│   │       ├── 03-working/         Work-in-progress files
│   │       └── 04-outputs/         Final deliverables
│   └── complete/                   Completed/archived builds
│       └── {ID}-{name}/
│
├── 03-skills/                  [SYNC] USER SKILLS (custom workflows)
│   └── {skill-name}/
│       ├── SKILL.md                YAML metadata + workflow
│       ├── references/             (optional) Detailed docs
│       ├── scripts/                (optional) Automation
│       └── assets/                 (optional) Files
│
└── 04-workspace/               🗺️ USER CONTENT
    ├── workspace-map.md            Your custom folder guide
    └── [Your folders]/             Clients, research, templates, etc.
```

---

## [GO] Instruction-Driven Architecture (Critical)

### The Master Controller Pattern

**Key Principle**: The Python script (`nexus-loader.py`) is the MASTER CONTROLLER. All orchestration logic lives there.

The script doesn't just return file lists - it returns **COMPLETE INSTRUCTIONS**:

```json
{
  "system_state": "first_time_with_defaults",
  "memory_content": {
    "system-map.md": "...(embedded content)...",
    "goals.md": "...(embedded content)...",
    "user-config.yaml": "...(embedded content)..."
  },
  "instructions": {
    "action": "display_menu",
    "suggest_onboarding": true,
    "message": "Welcome to Nexus! Quick Start Mode active.",
    "reason": "Smart defaults created - system ready for immediate use"
  },
  "metadata": {
    "builds": [...],
    "skills": [...]
  }
}
```

### Why This Matters

**Traditional Approach** (Error-Prone):
```
AI → Detect state → Guess what to do → Load files → Execute
```

**Nexus Approach** (Bulletproof):
```
Script → Analyze state → Return instructions → AI follows exactly
```

**Benefits**:
- [OK] **Zero interpretation** - AI doesn't guess, just executes
- [OK] **Zero manual state detection** - Script handles all edge cases
- [OK] **Deterministic behavior** - Same state = Same instructions
- [OK] **Easy debugging** - Instructions are explicit and visible
- [OK] **Simple orchestrator.md** - Just "follow the instructions"

---

## 🔌 Lifecycle Hooks System

Nexus uses **6 lifecycle hooks** to inject context automatically:

| Hook | When | Purpose |
|------|------|---------|
| **SessionStart** | Session begins | Load orchestrator, goals, builds, skills |
| **SessionEnd** | Session closes | Save learnings, create report |
| **PreToolUse** | Before tool runs | Validate operations |
| **PostToolUse** | After tool runs | Micro-teaching moments |
| **PreCompact** | Context compacting | Save resume state |
| **UserPromptSubmit** | User sends message | Route to skill/build |

**Configuration**: `.claude/settings.json` contains hook definitions.

**No manual commands needed** - hooks handle context injection automatically.

---

## [SYNC] The Startup Pattern

**EVERY session follows this pattern (handled by SessionStart hook):**

### Step 1: Hook Fires Automatically

SessionStart hook runs `nexus-load --startup` automatically:

The script analyzes system state and returns:
- `system_state` - Current state (first_time_with_defaults, operational, operational_with_active_builds)
- `memory_content` - Dictionary of file contents (already embedded, keyed by filename)
- `instructions` - Complete instructions for what to do next
- `metadata` - Builds and skills metadata (YAML scan)
- `stats` - System statistics and flags for menu display

---

### Step 2: Use Embedded Content

The `memory_content` dictionary contains file contents already loaded - no separate Read calls needed:

```python
# Content is already embedded in the response
goals_content = startup['memory_content']['goals.md']
config_content = startup['memory_content']['user-config.yaml']
```

**Result**: Zero "file not found" errors (script only lists files that exist)

---

### Step 3: Follow Instructions

Read `instructions.action` and execute exactly as specified:

#### Action: `load_and_execute_build`

```python
build_id = startup['instructions']['build_id']
mode = startup['instructions']['execution_mode']

# Display message
print(startup['instructions']['message'])

# Load build files
nexus-load --build {build_id}

# Read all planning files in parallel
Read: {build}/01-planning/overview.md
Read: {build}/01-planning/plan.md
Read: {build}/01-planning/steps.md

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
show_builds()
show_skills()
wait_for_user_input()
```

**That's it!** The script tells you exactly what to do. No guessing, no interpretation.

---

## 🎓 The Onboarding System (Optional Skills)

> **Updated 2025-12:** Nexus now uses **optional skill-based onboarding** instead of forced builds. Smart defaults are auto-created on first run, so users can start working immediately.

### Quick Start Mode (New Default)

First-time users get **smart defaults** automatically created:
- `01-memory/goals.md` - Template with placeholder goals
- `01-memory/user-config.yaml` - Default configuration
- `01-memory/core-learnings.md` - Empty learnings file
- `01-memory/memory-map.md` - Memory navigation

**Result**: User sees menu immediately and can start working. No forced onboarding!

### 6 Optional Onboarding Skills

When ready to learn, users can invoke any skill by trigger phrase:

| Skill | Trigger Phrases | Duration |
|-------|-----------------|----------|
| **setup-memory** | "setup memory", "personalize" | 8-10 min |
| **create-folders** | "create folders", "setup workspace" | 5-8 min |
| **learn-integrations** | "learn integrations", "connect tools" | 10-12 min |
| **learn-builds** | "learn builds", "how do builds work" | 8-10 min |
| **learn-skills** | "learn skills", "how do skills work" | 10-12 min |
| **learn-nexus** | "learn nexus", "system mastery" | 15-18 min |

**Total if all completed**: ~55 minutes (but completely optional!)

### Legacy Onboarding (4 Builds)

The original 4-build onboarding still exists for users who prefer structured learning:

### Build 00: Define Goals (8-10 min) - V2.0 Redesign

**Status**: First onboarding build
**Philosophy**: **CONCRETE BEFORE ABSTRACT**

#### V2.0 Improvements

| Metric | V1.0 (Old) | V2.0 (New) | Impact |
|--------|-----------|-----------|--------|
| **Time** | 12-15 min | 8-10 min | 33% faster |
| **Vocabulary** | 15+ terms | 4 terms | 73% reduction |
| **Tasks** | 40 | 16 | 60% fewer |
| **Structure** | Abstract→Concrete | Concrete→Abstract | Grounded learning |
| **Time to value** | 12 min | 5 min | 58% faster |
| **Drop-off risk** | 35-45% | <15% | 70% improvement |

#### The Journey

**Section 0: Welcome + Language (30 seconds)**
- Simple welcome
- Language selection (enforced for ALL subsequent interactions)
- NO system complexity before context exists

**Section 1: Your Goals (5 minutes) - CONCRETE FIRST**
- What do you do? (role + work pattern)
- 3-month goal + AI suggests metrics
- 6-12 month vision + AI suggests milestones
- Confirm understanding
- **AI Suggestion Framework**: Suggest, don't prescribe. Always allow refinement.

**Section 2: Optional Context (15 seconds) - FYI ONLY**
- Brief mention of `00-input/` folder
- NO stopping, NO checking, NO pressure

**Section 3: Create Your Workspace (2 minutes) - ACTION**
- Execute `init-memory.py` with user's actual content
- Show file tree (visual confirmation)
- Brief explanations of each file
- **Experience before explanation**

**Section 4: Understanding Memory (2 minutes) - EXPLANATION**
- Explain what just happened (grounded in experience)
- Show the value (tomorrow's persistence)
- Connect to user's goal
- Introduce 4 terms: Memory, Goals, Sessions, close-session

**Section 5: Close-Session Habit (2 minutes) - CRITICAL**
- Introduce the most important habit
- Explain what close-session does
- Practice it RIGHT NOW (immediate practice)
- Execute and show it working

**Section 6: What's Next (1 minute)**
- Preview the 3 remaining sessions
- Show progress made today
- Clear next step

#### What Gets Created

By the end of Build 00:
- [OK] `01-memory/goals.md` - YOUR role, work pattern, goals
- [OK] `01-memory/roadmap.md` - YOUR milestones, metrics, priorities
- [OK] `01-memory/user-config.yaml` - YOUR language and preferences
- [OK] `01-memory/core-learnings.md` - Insight capture template
- [OK] `01-memory/session-reports/` - Session summary folder

**All files contain YOUR actual content—no placeholders!**

#### Design Principles Applied

**Learning Science**:
- **Bloom's Taxonomy**: Start at "Knowledge" level (your goals), not "Analysis" (system architecture)
- **Constructivist Learning**: Experience before explanation (grounded learning)
- **Problem-Based Learning**: Need (your goals) drives solution discovery
- **Cognitive Load Theory**: 4 terms total respects working memory limits (Miller's Law)
- **Ebbinghaus Forgetting Curve**: Experience + immediate practice = 80% retention
- **Peak-End Rule**: Peak = goals captured in 5 min, End = close-session works perfectly

---

### Build 01: First Build (10-12 min)

**Status**: Second onboarding build
**Focus**: Workspace structure + Create first real build

**What You'll Do**:
- Create workspace structure using just-in-time organization
- Learn Builds vs Skills decision framework
- Use `plan-build` skill to create first real build
- Apply build planning with AI guidance

**What Gets Created**:
- [OK] `04-workspace/` custom folder structure
- [OK] `04-workspace/workspace-map.md` with your organization
- [OK] Your first real build tailored to your goals

---

### Build 02: First Skill (15 min)

**Status**: Third onboarding build (was Build 03 before consolidation)
**Focus**: Skill creation + Workflow automation

**What You'll Do**:
- Learn what skills are (reusable workflows)
- Use `create-skill` skill to capture a workflow
- AI suggests skill name based on your description
- Practice executing your first skill

**What Gets Created**:
- [OK] Your first custom skill in `03-skills/`
- [OK] Understanding of workflow automation

---

### Build 03: System Mastery (10 min)

**Status**: Fourth and final onboarding build
**Focus**: Review + AI collaboration awareness

**What You'll Do**:
- Review complete setup (goals, workspace, builds, skills)
- Learn 3 system pitfalls using YOUR actual entities
- Learn 2 AI behavioral patterns (False Progress 19%, Incomplete Reading)
- Practice detection exercises with YOUR builds
- Confirm two-layer mastery (system + AI collaboration)
- Graduate with AI awareness superpowers!

**Outcome**:
- [OK] Onboarding complete
- [OK] System mastery confirmed
- [OK] AI collaboration awareness established
- [OK] Ready for operational mode

---

## [SYNC] How It All Works Together

### Session Start (Instruction-Driven)

```
1. Run: nexus-load --startup
   ↓
2. Script analyzes system state:
   - Check if goals.md exists
   - Check if onboarding complete
   - Check for current focus
   - Detect system state
   ↓
3. Script returns instructions:
   {
     "system_state": "operational",
     "memory_content": {
       "system-map.md": "...(embedded)...",
       "goals.md": "...(embedded)...",
       "user-config.yaml": "...(embedded)..."
     },
     "instructions": {
       "action": "display_menu"
     },
     "metadata": {
       "builds": [...],
       "skills": [...]
     }
   }
   ↓
4. AI uses memory_content (already embedded)
   ↓
5. AI follows instructions (display_menu):
   - Show Nexus banner
   - Show your goals
   - Show active builds
   - Show available skills
   - Wait for user input
```

### During Work (Skill-First Execution)

**Priority 1: Check for matching skill** (MOST IMPORTANT)

```
User: "generate status report"
  ↓
AI scans metadata.skills:
  - Match "status report" → weekly-status-report skill
  ↓
Load skill:
  nexus-load --skill weekly-status-report
  ↓
Read: 03-skills/weekly-status-report/SKILL.md
  ↓
Execute workflow in SKILL.md
```

**Priority 2: Check for build name match**

```
User: "continue working on website"
  ↓
AI scans metadata.builds:
  - Match "website" → 05-website-development
  ↓
Load build:
  nexus-load --build 05-website-development
  ↓
Read in parallel:
  - 02-builds/05-website-development/01-planning/overview.md
  - 02-builds/05-website-development/01-planning/plan.md
  - 02-builds/05-website-development/01-planning/steps.md
  ↓
Show: Next unchecked task
  ↓
User works on task
  ↓
Context flows to build files
```

**Priority 3: General response** (Fallback - should be RARE)

```
User: "What's the weather like?"
  ↓
No skill match, no build match
  ↓
Respond naturally + suggest creating build/skill if needed
```

**This priority order is THE most important orchestration principle in Nexus.**

### Session End (close-session skill)

```
User: "done for now"
  ↓
AI triggers: close-session skill
  ↓
Skill workflow:
  1. Update task progress:
     - Mark completed tasks with [x]
     - Calculate progress percentage
  ↓
  2. Create session report:
     - 01-memory/session-reports/{date}.md
     - Summary of work done
     - Decisions made
     - Next steps
  ↓
  4. Clean temp files (if any)
  ↓
  5. Confirm: "Session closed. Progress saved!"
  ↓
All context preserved for next session
```

---

## [TARGET] Key Concepts

### 1. Builds (Temporal Work)

**Purpose**: Organize work with a beginning, middle, and end

**Structure**:
- `01-planning/` - Purpose, plan, execution steps (overview.md, plan.md, steps.md)
- `02-resources/` - Reference materials
- `03-working/` - Work-in-progress files
- `04-outputs/` - Final deliverables

**Lifecycle**: PLANNING → IN_PROGRESS → COMPLETING → COMPLETE → ARCHIVED

**State Source**: Checkbox list in `steps.md`

**Planning Files**:
- **01-overview.md**: Purpose, success criteria, context (YAML frontmatter)
- **02-discovery.md**: Research, questions, dependencies
- **03-plan.md**: Approach, decisions, mental models applied
- **04-steps.md**: Execution checklist broken down into phases
- **resume-context.md**: Cross-session continuity state

**YAML Metadata** (in overview.md):
```yaml
---
id: 05-website-development
name: Website Development
status: IN_PROGRESS
description: Load when user mentions "website", "web dev", "homepage"
created: 2025-11-01
last_worked: 2025-11-04
tags: [web, design]
---
```

**Note**: `tasks_total`, `tasks_completed`, and `progress` are **calculated automatically** by nexus-loader from steps.md checkboxes. **Do NOT store in YAML**.

---

### 2. Skills (Reusable Workflows)

**Purpose**: Capture repeatable workflows for common tasks

**Structure**:
- `SKILL.md` - Main workflow (<500 lines)
- `references/` - Detailed documentation
- `scripts/` - Automation code
- `assets/` - Files needed by skill

**V2.0 YAML Format** (minimal metadata):
```yaml
---
name: weekly-status-report
description: Load when user says "status report", "weekly update", "progress summary". Generate comprehensive weekly work summary with completed tasks, decisions made, and next steps.
---
```

**Progressive Disclosure**:
1. **Metadata** (always loaded) - name + description (~50 tokens)
2. **SKILL.md** (loaded when triggered) - main workflow
3. **References** (loaded on-demand) - detailed docs

**Priority**: User skills (03-skills/) have priority over system skills (00-system/skills/)

---

### 3. Memory (Context Persistence)

**Purpose**: Never start from scratch - preserve all context

**What gets saved**:
- **Goals**: Your objectives and success criteria
- **Roadmap**: Short/long-term plans
- **Learnings**: Patterns, insights, best practices
- **Session Reports**: Historical work summaries
- **Build State**: What you were working on
- **User Config**: Language and preferences

**Auto-Updated By**: close-session skill at end of each session

**Key Principle**: Context is cumulative - builds over time

---

### 4. Auto-Detection (YAML-Driven)

**How it works**:

1. **Everything has metadata** (YAML frontmatter)
2. **Description field** contains trigger phrases
3. **AI matches** user message against descriptions
4. **Loads context** when match found

**Example**:

```yaml
# In 02-builds/05-website-development/01-planning/overview.md
---
description: Load when user mentions "website", "web dev", "homepage", "site"
---
```

```
User: "let's work on the homepage"
  ↓
AI matches "homepage" → Loads website build
```

---

### 5. Mental Models (Thinking Frameworks)

**Purpose**: Library of 90+ thinking frameworks across 12 categories for structured planning and decision-making.

**Architecture**:
- **Skill**: `00-system/skills/tools/mental-models/SKILL.md` - Workflow and usage
- **Models**: `00-system/mental-models/models/{category}/` - 59 individual model files
- **Scanner**: `uv run nexus-mental-models --format brief` - Lists all models with paths

**Categories** (12):
analytical, cognitive, collaborative, communication, creative, diagnostic, learning, operational, probability-risk, strategic, time-resource, validation

**YAML Frontmatter Format** (in mental model files):
```yaml
---
name: First Principles
category: cognitive
tier: 1
best_for: Novel builds, challenging assumptions
questions:
  - What are we assuming here?
  - What would we do if starting from scratch?
  - What's the fundamental truth we can build on?
---
```

**Offering Pattern** (used in plan-build, execute-build):
```markdown
AI runs: nexus-mental-models
  ↓
AI reviews JSON output with all available models
  ↓
AI offers 2-3 relevant models to user:

"For your Build/Create build, I recommend:

1. **First Principles** – Strip assumptions, find fundamental truths
   Best for: Novel builds, challenging assumptions

2. **Pre-Mortem** – Imagine failure modes before implementation
   Best for: High-stakes builds, risk mitigation

Which approach(es) sound most useful? Or we can combine them!"
  ↓
User picks: "First Principles + Pre-Mortem"
  ↓
AI loads: mental-models/references/cognitive-models.md (First Principles section)
AI loads: mental-models/references/diagnostic-models.md (Pre-Mortem section)
  ↓
AI applies questions from selected models to fill plan.md
```

**Integration Points**:
- **plan-build**: MANDATORY mental model selection during plan.md phase
- **execute-build**: Offered at key decision points (section completion, risk assessment)
- **create-skill**: Offered for workflow design decisions

**Token Efficiency**:
- Metadata only: ~50 tokens (always available)
- Selected models: ~2K tokens (loaded on-demand)
- Full catalog: ~15K tokens (never loaded entirely)

**See**: [`mental-models skill`](../skills/tools/mental-models/SKILL.md) for usage

---

### 6. Bulk-Complete Automation (Task Tracking)

**Purpose**: Automatic task completion when work is done, eliminating manual checkbox tedium.

**How It Works**:
```
Build work completed this session
  ↓
close-session skill detects completion signals:
  - "done", "finished", "complete"
  - All tasks in section executed
  - User confirms work is done
  ↓
Auto-runs bulk-complete script:
  nexus-bulk-complete --build [ID] --all --no-confirm
  ↓
Validates: Re-reads file to confirm completion
  ↓
Reports: "[OK] VALIDATED: 40/40 tasks now complete (100%)"
```

**Script Options**:
```bash
# Complete all tasks (build finished)
nexus-bulk-complete --build 01 --all --no-confirm

# Complete specific phase (phase done)
nexus-bulk-complete --build 01 --section "Phase 2"

# Complete task range (selective)
nexus-bulk-complete --build 01 --tasks 1-5,7,10-15

# Interactive mode (pick tasks)
nexus-bulk-complete --build 01
```

**Safety Features**:
- **Threshold**: Requires context signal (completion detected, not random)
- **Validation**: Re-reads file after completion to confirm
- **Fallback**: Manual Edit tool if script fails
- **Confirmation**: Optional `--no-confirm` flag (safe for auto-triggers)

**Time Savings**: 5-10 minutes per build (eliminates manual checkbox marking)

**Integration Points**:
- **close-session**: Auto-runs bulk-complete when build complete (Step 2)
- **execute-build**: Offers bulk-complete after each section
- **Manual trigger**: "bulk complete [build]" or "mark all tasks done"

**See**: [`bulk-complete skill`](../skills/bulk-complete/SKILL.md) for complete usage

---

### 7. Dynamic Template System (Build Types)

**Purpose**: Type-specific plan.md templates that eliminate the blank page problem with domain-specific structure.

**6 Build Types**:
| Type | Best For | Template Sections |
|------|----------|-------------------|
| **Build/Create** | Software, features, products | Technical Architecture, Implementation Strategy, Integration Points |
| **Research/Analysis** | Investigations, studies | Research Questions, Data Sources, Analysis Framework |
| **Strategy/Planning** | Roadmaps, decisions | Stakeholder Analysis, Options Evaluation, Decision Framework |
| **Content/Creative** | Writing, design, media | Audience, Format, Distribution Channels |
| **Process/Workflow** | Automation, optimization | Current State, Bottlenecks, Improvement Plan |
| **Generic** | Anything else | Flexible structure |

**Type Selection Workflow** (in plan-build):
```
AI: "What type of build is this?"
  ↓
Offer 6 types with brief descriptions
  ↓
User selects: "Build/Create"
  ↓
init_build.py generates plan.md with Build-specific sections:
  ## Technical Architecture
  ## Implementation Strategy
  ## Integration Points
  ## Testing Approach
  ## Deployment Plan
```

**Template Injection** (init_build.py):
```python
def create_plan_template(build_type):
    templates = {
        'build': BUILD_TEMPLATE,      # Technical sections
        'research': RESEARCH_TEMPLATE, # Analysis sections
        'strategy': STRATEGY_TEMPLATE, # Decision sections
        'content': CONTENT_TEMPLATE,   # Creative sections
        'process': PROCESS_TEMPLATE,   # Workflow sections
        'generic': GENERIC_TEMPLATE    # Flexible sections
    }
    return templates.get(build_type, GENERIC_TEMPLATE)
```

**Benefits**:
- **Better planning quality**: Domain-specific prompts guide thinking
- **Faster planning**: Pre-filled sections reduce blank page paralysis
- **Encoded expertise**: Templates capture best practices for each type
- **Consistency**: All Build builds have same structure

**Template Files Location**:
```
00-system/skills/plan-build/scripts/templates/
├── template-build.md
├── template-research.md
├── template-strategy.md
├── template-content.md
├── template-process.md
└── template-generic.md
```

**When to Use Each Type**:
- **Build**: New feature, software build, product development
- **Research**: Market research, technical investigation, user study
- **Strategy**: Quarterly planning, organizational decision, roadmap
- **Content**: Blog post, documentation, video script
- **Process**: Workflow automation, process optimization, efficiency
- **Generic**: Unclear scope, mixed types, or unusual builds

**See**: [`plan-build skill`](../skills/plan-build/SKILL.md) for complete workflow

---

## [*] Core Infrastructure

### nexus-loader.py

**Location**: `00-system/core/nexus-loader.py`

**What it does**:
- Analyzes system state
- Returns complete instructions (instruction-driven architecture)
- Loads core files at session start
- Scans all builds and skills for metadata
- Provides context loading on-demand
- Monitors token budget
- Returns structured JSON

**Commands**:
```bash
nexus-load --startup          # Load session context + return instructions
nexus-load --list-builds      # Scan build metadata
nexus-load --list-skills      # Scan skill metadata
nexus-load --build 05         # Load specific build
nexus-load --skill close-session  # Load specific skill
nexus-load --show-tokens      # Display token costs
```

**Output Structure**:
```json
{
  "loaded_at": "2025-11-05T01:05:54",
  "bundle": "startup",
  "system_state": "operational",
  "memory_content": {
    "system-map.md": "...(embedded content)...",
    "goals.md": "...(embedded content)..."
  },
  "instructions": {
    "action": "display_menu",
    "message": "...",
    "reason": "..."
  },
  "metadata": {
    "builds": [...],
    "skills": [...]
  },
  "stats": {
    "files_embedded": 3,
    "total_builds": 8,
    "total_skills": 12
  }
}
```

---

### orchestrator.md

**Location**: `00-system/core/orchestrator.md`

**What it does**:
- Documents AI decision logic (minimal)
- Explains three-step startup sequence
- Describes skill-first execution priority
- Shows build/skill loading patterns
- Provides response formatting guidelines
- Emphasizes menu display format

**Design Principle**: Ultra-simple. State lives in data files, not code. Python script is master controller.

**Key Sections**:
- Startup Sequence (3 steps)
- Language Preference Enforcement
- Build Loading Pattern (two-step)
- Skill Loading Pattern (two-step)
- Smart Routing (skill-first execution)
- Menu Display Format

---

---

## 🤖 System Skills (152 Across 7 Categories)

**Location**: `00-system/skills/` (NOT in 03-skills/)

### Builds (3 skills)
| Skill | Purpose | Trigger |
|-------|---------|---------|
| **plan-build** | Create new builds with AI-guided planning | "plan build", "new build" |
| **execute-build** | Execute build work systematically | "continue [build]", "work on" |
| **archive-build** | Archive completed builds | "archive build" |

### Learning (10 skills)
| Skill | Purpose | Trigger |
|-------|---------|---------|
| **setup-memory** | Configure goals and preferences | "setup memory" |
| **create-folders** | Set up workspace folders | "create folders" |
| **learn-integrations** | Learn how to connect external tools | "learn integrations" |
| **learn-builds** | Learn build system | "learn builds" |
| **learn-skills** | Learn skill system | "learn skills" |
| **learn-nexus** | System mastery tutorial | "learn nexus" |
| **how-nexus-works** | System tour | "how nexus works" |
| **quick-start** | 10-15 min quickstart | "quick start" |
| **analyze-context** | Upload files for AI analysis | "analyze context" |
| **create-roadmap** | Create prioritized roadmap | "create roadmap" |

### Integrations (119 skills across 8 services)
| Service | Skills | Trigger |
|---------|--------|---------|
| **HubSpot** | 24 | "hubspot", CRM operations |
| **Langfuse** | 55 | "langfuse", LLM tracing |
| **Google** | 12 | Gmail, Docs, Sheets, Calendar, Drive, Tasks |
| **Slack** | 3 | "slack", messaging |
| **Airtable** | 2 | "airtable", database |
| **HeyReach** | 2 | "heyreach", LinkedIn outreach |
| **NotebookLM** | 2 | "notebooklm", audio overview |
| **Gemini** | 3 | Image generation |

### Skill Development (6 skills)
| Skill | Purpose | Trigger |
|-------|---------|---------|
| **create-skill** | Create reusable workflows | "create skill" |
| **create-master-skill** | Create shared integration library | "create master skill" |
| **import-skill** | Import external skills | "import skill" |
| **share-skill** | Share skills to database | "share skill" |
| **search-skill-database** | Find existing skills | "search skills" |
| **validate-skill-functionality** | Validate skill execution | "validate skill" |

### System (8 skills)
| Skill | Purpose | Trigger |
|-------|---------|---------|
| **close-session** | End session, save progress | "done", "finish", "close" |
| **list-skills** | Show available skills | "list skills" |
| **update-workspace-map** | Sync workspace map | "update workspace map" |
| **add-integration** | Guide MCP server setup | "add integration" |
| **explain-nexus** | Explain system | "explain nexus" |
| **update-nexus** | Check for updates | "update nexus" |
| **setup** | Initial configuration | "setup" |
| **validate-docs-implementation** | Check docs vs code | "validate docs" |

### Tools (3 skills)
| Skill | Purpose | Trigger |
|-------|---------|---------|
| **mental-models** | Access 90+ thinking frameworks | "mental model" |
| **format-and-lint-code** | Code formatting | "format code" |
| **generate-philosophy-doc** | Generate philosophy docs | "generate philosophy" |

**Note**: All skills use V2.0 format (name + description only)

---

## 📖 Documentation Reference

### For Understanding the System

- **[Framework Overview](framework-overview.md)** (THIS FILE) - Complete system guide
- **[System Map](../system-map.md)** - System structure and architecture
- **[Orchestrator](../core/orchestrator.md)** - AI decision logic (minimal, instruction-driven)
- **[Memory Map](../../01-memory/memory-map.md)** - Context persistence

### For Building Skills

- **[Skill File Format](skill-file-format.md)** - .skill packaging specification
- **create-skill skill** - Use the create-skill skill for guided skill creation with built-in best practices

### For Development

- **Build Schema**: `../skills/plan-build/build-schema.yaml`
- **Onboarding Builds**: Check `02-builds/00-define-goals/` through `03-system-mastery/` for complete designs

---

## 💡 Design Principles

### 1. Instruction-Driven Architecture

**Principle**: Python script analyzes state and returns complete instructions. AI follows exactly.

**Why**: Zero interpretation, zero ambiguity, deterministic behavior, easy debugging.

**Example**: Script returns `"action": "load_and_execute_build"` with complete workflow steps.

---

### 2. YAML-Driven Auto-Detection

**Principle**: Everything has metadata describing when to load it. AI matches user messages against descriptions.

**Why**: Context loads automatically. No manual routing. Self-documenting.

**Example**: Build description "Load when user mentions 'website'" → User says "website" → Build loads.

---

### 3. Skill-First Execution

**Principle**: Skills have priority over builds in routing. User skills have priority over system skills.

**Why**: Reusable workflows are more valuable than one-off build work. Encourages workflow capture.

**Example**: "status report" matches skill → Executes skill (doesn't search builds first).

---

### 4. Progressive Disclosure

**Principle**: Load minimum at start (just metadata), more context just-in-time (when needed).

**Why**: Efficient token usage. Fast startup. Context loads when relevant.

**Example**: Metadata (~50 tokens) always loaded. SKILL.md (~2000 tokens) loaded when triggered.

---

### 5. State in Data Files

**Principle**: System state tracked in YAML metadata. Task progress tracked in steps.md checkboxes. No logic in code.

**Why**: Transparent. Inspectable. Debuggable. AI can read state directly.

**Example**: System state tracked in user-config.yaml and build metadata, not in Python variables.

---

### 6. Context Preservation

**Principle**: Nothing is lost between sessions. All work saved automatically. Session reports build historical record.

**Why**: Never start from scratch. Cumulative learning. Historical awareness.

**Example**: close-session updates memory, saves progress, creates session report.

---

### 7. Concrete Before Abstract (Onboarding)

**Principle**: Experience first, explanation after. Value delivery before feature teaching.

**Why**: Grounded learning. Higher retention. Lower cognitive load. Better engagement.

**Example**: Build 00 captures goals (5 min) BEFORE explaining system architecture.

---

## 🎓 Key Terminology

| Term | Definition |
|------|------------|
| **Build** | Temporal work with beginning, middle, end (e.g., client website) |
| **Skill** | Reusable workflow for repetitive tasks (e.g., weekly report) |
| **Memory** | Context persistence system (goals, learnings, session reports) |
| **YAML Frontmatter** | Metadata at top of files (between `---` markers) |
| **Auto-Detection** | System automatically loads context based on YAML descriptions |
| **Progressive Disclosure** | Load minimum first, more context on-demand |
| **Session** | Single conversation with AI (start → work → close) |
| **Context** | All information relevant to current work |
| **Instruction-Driven** | Script returns complete instructions, AI follows exactly |
| **Skill-First** | Skills have priority over builds in routing |
| **Onboarding** | 4-build journey (00-03) to learn system (35-40 min) |

---

## [SYNC] System Workflows

### Creating a Build

```
User: "I want to create a build"
  ↓
AI triggers: plan-build skill
  ↓
Step 1: Offer build type
  - Build/Create
  - Research/Analysis
  - Strategy/Planning
  - Content/Creative
  - Process/Workflow
  ↓
Step 2: Run init_build.py (auto-assigns ID, creates structure)
  ↓
Creates:
  └── 02-builds/{ID}-{name}/
      ├── 01-planning/
      │   ├── overview.md (YAML + purpose + success criteria + context)
      │   ├── plan.md (approach + decisions + dependencies)
      │   └── steps.md (execution checklist)
      ├── 02-resources/
      ├── 03-working/
      └── 04-outputs/
  ↓
Step 3: Collaborative Planning (20-30 min)
  - Fill overview.md (purpose, success criteria)
  - Fill plan.md with mental models:
    * Socratic questioning
    * Devil's Advocate
    * Dependency research
  - Fill steps.md (execution checklist)
  - Mandatory pauses between documents
  ↓
Step 4: Close session (save for later execution)
  ↓
Build metadata auto-detected on next startup
```

### Creating a Skill

```
User: "I want to create a skill"
  ↓
AI triggers: create-skill skill
  ↓
Interactive wizard:
  1. Skill purpose
  2. AI suggests skill name
  3. Workflow steps
  4. Optional: references, scripts, assets
  ↓
Creates:
  └── 03-skills/{skill-name}/
      ├── SKILL.md (V2.0 YAML + workflow)
      ├── references/ (if needed)
      ├── scripts/ (if needed)
      └── assets/ (if needed)
  ↓
Auto-detected: Next session, skill available in metadata
```

### Working on a Build

```
User: "continue working on website"
  ↓
AI matches "website" against build descriptions
  ↓
Loads: nexus-load --build 05-website-development
  ↓
Reads in parallel:
  ├── overview.md
  ├── plan.md
  └── steps.md
  ↓
Shows: Next unchecked step
  ↓
User completes work
  ↓
Context saved to build files (03-working/, 04-outputs/)
```

### Ending a Session

```
User: "done for now"
  ↓
AI triggers: close-session skill
  ↓
Skill workflow:
  1. Update steps.md (mark completed steps with [x])
  2. Create session report (session-reports/{date}.md)
  3. Update core-learnings.md if insights captured
  4. Confirm completion
  ↓
Session complete - all context preserved
```

---

## 🌟 Why Nexus?

### Problems It Solves

[ERROR] **Without Nexus**:
- Start every AI session from scratch
- Repeat context manually
- Lose track of progress
- Forget what you were working on
- No reusable workflows
- Manual build management overhead

[OK] **With Nexus**:
- Resume exactly where you left off
- Context loads automatically (instruction-driven)
- Progress tracked automatically (steps.md)
- Always know current focus (via nexus-loader.py)
- Capture and reuse workflows (skills)
- Zero-overhead organization (YAML-driven)

### Key Benefits

1. **Never Repeat Context** - System remembers everything (memory files)
2. **Instruction-Driven** - Script tells AI exactly what to do (zero ambiguity)
3. **Auto-Detection** - Right context loads automatically (YAML descriptions)
4. **Skill-First** - Reusable workflows prioritized over one-off work
5. **Progress Tracking** - Always know what's done/next (checkbox tasks)
6. **Workflow Capture** - Reuse successful patterns (skills)
7. **Historical Record** - Session reports build over time
8. **Pedagogical Onboarding** - Learn through experience, not explanation (35-40 min)

---

## [GO] Getting Started

### First-Time User Journey (Quick Start)

**Step 1: Load CLAUDE.md**
```
In Claude Desktop or Claude Code:
Load: Nexus-v4/CLAUDE.md
```

**Step 2: Smart Defaults Auto-Created**
```
Script detects: No goals.md exists
Action: Creates smart default files automatically
Script returns: "system_state": "first_time_with_defaults"
Instructions: Display menu with onboarding suggestions
```

**Step 3: Start Working Immediately!**
```
AI shows: Menu with your builds, skills, and suggestions
User: Start working OR learn the system with optional skills
```

**Optional: Learn the System** (when ready)
- Say "setup goals" → Personalize your goals (8-10 min)
- Say "setup workspace" → Configure your folders (5-8 min)
- Say "learn integrations" → Connect external tools (10-12 min)
- Say "learn builds" → Understand build workflow (8-10 min)
- Say "learn skills" → Create reusable workflows (10-12 min)
- Say "learn nexus" → Advanced system mastery (15-18 min)

**Step 4: Operational!**
```
After personalizing goals:
Script returns: "system_state": "operational"
Instructions: Display menu
AI shows: YOUR goals, builds, skills, current focus
User: Work naturally with full context preservation
```

### Typical Operational Session

```
1. AI runs: nexus-load --startup
2. AI loads: 5 core files + metadata
3. AI displays: Goals, builds, skills, current focus
4. User says: "work on website"
5. AI matches: website build → Loads context
6. User works: AI assists with full context
7. User says: "done"
8. AI triggers: close-session → Saves everything
9. Next session: Resume exactly where you left off
```

---

## 📞 Need Help?

### Navigation

- Lost? Check the [System Map](../system-map.md)
- Need context? Check the [Memory Map](../../01-memory/memory-map.md)
- How does orchestration work? Check the [Orchestrator](../core/orchestrator.md)

### Building

- Creating skills? Use the **create-skill** skill for guided workflow with built-in best practices
- Packaging skills? See [Skill File Format](skill-file-format.md)

### Understanding

- How does it work? Read this document (you're here!)
- How do I start? See "Getting Started" section above
- What's the philosophy? See "Design Principles" section above
- What's the onboarding like? See "The Onboarding Journey" section above

---

## 🔮 Advanced Topics

### Language-First Architecture

Language selection happens in first 30 seconds of Build 00 and is enforced for ALL subsequent interactions. Stored in `01-memory/user-config.yaml`.

Supported: English, Deutsch, Español, Français, 中文, 日本語, Português, Italiano, and more.

### AI Suggestion Framework

5-step collaborative pattern used in onboarding:
1. User provides context
2. AI synthesizes and suggests 2-3 options
3. Ask for resonance ("What resonates with you?")
4. User refines
5. Capture refined version (NOT AI's suggestion)

**Philosophy**: Invitation, not instruction. Collaborative, not prescriptive.

### Token Budget Management

nexus-loader.py monitors total metadata tokens and warns if >7,000 (3.5% of context window).

Progressive disclosure keeps startup lean:
- Metadata: ~50 tokens per skill/build
- SKILL.md: ~2000 tokens (loaded when triggered)
- References: Variable (loaded on-demand)

### Archiving Completed Builds

Use `archive-build` skill to move completed builds to `02-builds/complete/`.

Benefits:
- Cleaner build list
- Historical record preserved
- Can unarchive if needed

---

**Nexus** - Self-guiding work organization through AI conversation and instruction-driven automation.

**Never start from scratch. Always resume where you left off. Let the system remember for you.**

---

**Version**: 5.0
**Last Updated**: 2026-02-01
**Status**: Production Ready
**Major Changes in V5.0**:
- **Lifecycle Hooks System** - 6 hooks (SessionStart, SessionEnd, PreToolUse, PostToolUse, PreCompact, UserPromptSubmit)
- **152 System Skills** - Expanded from 25 to 152 across 7 categories
- **8 Integration Ecosystems** - HubSpot, Langfuse, Google, Slack, Airtable, HeyReach, NotebookLM, Gemini
- **90+ Mental Models** - Expanded from 59 thinking frameworks
- **Build Structure Update** - Numbered planning files (01-overview, 02-discovery, 03-plan, 04-steps)
- **resume-context.md** - Cross-session continuity for builds

**Previous V4.0 Changes**:
- Optional Onboarding System - Smart defaults auto-created, no forced onboarding
- Quick Start Mode - Users can work immediately on first run
- Modern Menu Header - Replaced ASCII art with 3-line header
- Progressive Disclosure - Context-aware skill suggestions via learning_tracker

**Previous V3.0 Changes**:
- Mental Models Framework (Section 5) - thinking frameworks with 3-tier system
- Bulk-Complete Automation (Section 6) - Automatic task completion with validation
- Dynamic Template System (Section 7) - 6 build types with type-specific templates
