# Research Findings: Project Skills Architecture

**Research Date**: 2026-01-03
**Purpose**: Deep understanding of create-project and execute-project skills for expansion

---

## Current Architecture Overview

### create-project Skill

**Location**: `00-system/skills/projects/create-project/`

**Current Workflow**: Type Selection → Planning → Document Creation
1. Offer project types (Build, Research, Strategy, Content, Process, Generic)
2. Get project name from user
3. Run `init_project.py` script to create structure
4. Fill `overview.md` collaboratively
5. Fill `plan.md` with mental models
6. Fill `steps.md` with execution breakdown
7. Trigger close-session

**Key Script**: `init_project.py`
- Auto-assigns next available project ID
- Creates 4 directories: 01-planning/, 02-resources/, 03-working/, 04-outputs/
- Generates 3 planning files: overview.md, plan.md, steps.md
- Supports type-specific templates (template-{type}.md)

**Templates**:
```python
OVERVIEW_TEMPLATE - Purpose, Success Criteria, Context, Timeline
PLAN_TEMPLATE - Approach, Decisions, Resources, Dependencies, Open Questions, Mental Models
STEPS_TEMPLATE - Phase-based checklist with [ ] checkboxes
```

**Type-Specific Sections**: Loaded from `scripts/templates/template-{type}.md` and injected into plan.md

---

### execute-project Skill

**Location**: `00-system/skills/projects/execute-project/`

**Current Workflow**: 7-Step Execution Process
1. Initialize TodoWrite with ALL workflow steps
2. Load project context via nexus-loader.py
3. Identify current phase/section
4. Execute work with continuous tracking
5. Incremental progress updates
6. Handle partial completion (pause/resume)
7. Project completion and close-session

**Key Integration**:
- Uses `nexus-loader.py --project [ID]` to load project context
- Uses `bulk-complete.py` for batch task completion
- Reads steps.md/tasks.md to track progress
- Updates YAML metadata in overview.md

**Progress Tracking**:
- Parses checkbox tasks: `- [ ]` (uncompleted) vs `- [x]` (completed)
- Section-based completion for large projects
- Auto-validates after bulk-complete

---

### nexus-loader.py Architecture

**Location**: `00-system/core/nexus-loader.py`

**Modes**:
1. `--startup`: Load full session context (orchestrator.md, memory, metadata)
2. `--resume`: Resume after compaction (skip menu, continue working)
3. `--project [ID]`: Load specific project files
4. `--skill [name]`: Load specific skill files
5. `--metadata`: Load only project/skill metadata

**Resume Mode (`--resume`)**:
- Currently: Sets `resume_mode=True` in service.startup()
- Returns: `instructions.action = "continue_working"`
- Missing: No structured resume state loading mechanism

**Project Loading** (`--project [ID]`):
```python
def load_project(project_id: str, part: int = 0):
    # Returns:
    # - file_paths: All planning files
    # - yaml_metadata: Extracted frontmatter
    # - output_files: Files in 04-outputs/
    # - _usage.recommended_reads: List of paths to read
```

---

## Gaps Identified

### 1. No Research Phase in create-project
**Current**: Jumps directly from Type Selection → Planning
**Need**: Research Phase BEFORE planning
- Explore existing patterns in codebase
- Identify dependencies and related files
- Research domain/technical requirements
- Output to structured research document

### 2. Resume Functionality is Minimal
**Current**: `--resume` mode only sets flag and changes menu action
**Need**: Structured resume state mechanism
- Where was user in project workflow?
- What section/task was active?
- What decisions were made?
- What context is critical to continue?

### 3. No Compaction Detection
**Current**: No awareness of when conversation is about to be compacted (200k tokens)
**Need**: Mechanism to detect compaction and trigger resume state save

### 4. Loading Sequence Not Defined
**Current**: AI must figure out what to load after compaction
**Need**: Clear rules for what files/context to load in what order

---

## Research Phase Design Proposal

### Where to Insert
**Before** Step 5 (Fill overview.md) in create-project workflow:

```
1. Type Selection
2. Get project name
3. Run init_project.py (create structure)
4. **NEW: Research Phase** ← INSERT HERE
5. Fill overview.md
6. Fill plan.md
7. Fill steps.md
8. Close session
```

### Research Phase Workflow
1. **Offer research option**: "Would you like to research before planning? (5-15 min)"
2. **If yes**: Load research template
3. **Execute research tasks**:
   - Grep codebase for related files
   - Scan existing skills for reuse
   - Check integration configs (Airtable, MCP servers, etc.)
   - Identify technical dependencies
4. **Document findings** in `02-resources/research.md`
5. **Use findings** to pre-populate plan.md dependencies

### Research Template Structure
```markdown
# {Project Name} - Research

## Domain Research
[What exists in the codebase related to this domain?]

## Dependency Analysis
[What files, skills, systems are involved?]

## Pattern Discovery
[Are there existing patterns to follow?]

## Technical Requirements
[What technical constraints or requirements?]

## Findings Summary
[Key insights to inform planning]
```

---

## Resume State Design Proposal

### Where to Store
**Option 1**: `01-planning/_resume.md` (single file)
**Option 2**: `01-planning/resume/` directory (multiple states)
**Recommended**: Option 1 for simplicity

### Resume State Structure
```yaml
---
resume_version: 1.0
last_updated: 2026-01-03T12:00:00
current_phase: execution  # research | planning | execution
current_skill: execute-project
project_id: 24-project-skills-research-resume-expansion
session_count: 3
total_tokens_used: 185000  # Track for compaction detection
---

# Resume State

## Current Location
- **Workflow Step**: Step 4 - Execute Section 2
- **Current Section**: Section 2 - Implementation
- **Next Task**: Task 15 - "Implement scoring logic"
- **Progress**: 14/40 tasks (35%)

## Session History
1. Session 1: Created project, completed research phase
2. Session 2: Completed overview.md and plan.md
3. Session 3 (current): Executing implementation phase

## Critical Context
[Key decisions, assumptions, or context needed to continue]

## Loading Sequence
When resuming, load in this order:
1. This resume file (_resume.md)
2. overview.md (understand purpose)
3. plan.md (understand approach)
4. steps.md (see all tasks and current progress)
5. Relevant files in 03-working/ or 04-outputs/
```

### When to Update Resume State
1. **After each major phase transition** (research → planning → execution)
2. **Before close-session** (capture current state)
3. **After bulk-complete** (update progress)
4. **When approaching token limit** (manual trigger or auto-detect)

---

## Loading Sequence Rules

### Standard Project Load (execute-project)
1. Run `nexus-loader.py --project [ID]`
2. Read `recommended_reads` in parallel:
   - overview.md (purpose, goals)
   - plan.md (approach, decisions)
   - steps.md (tasks, progress)

### Resume After Compaction
1. Run `nexus-loader.py --resume --project [ID]` (NEW flag combo)
2. Read `_resume.md` FIRST (get current state)
3. Read only files needed based on current phase:
   - If research phase: research.md
   - If planning phase: overview.md, plan.md
   - If execution phase: overview.md, plan.md, steps.md
4. Skip menu, continue from current task

---

## Integration Points

### create-project Changes
1. Add research phase step after init_project.py
2. Create research template
3. Update SKILL.md workflow documentation
4. Update references/workflows.md

### execute-project Changes
1. Add resume state creation/update logic
2. Update nexus-loader.py integration
3. Add compaction detection (token count tracking)
4. Update SKILL.md workflow documentation

### nexus-loader.py Changes
1. Add `--resume` + `--project` combined mode
2. Add resume state loading logic
3. Return resume-specific instructions
4. Update NexusService.load_project() to check for _resume.md

---

## Next Steps for Planning

1. Design research template (structure and prompts)
2. Design resume state structure (YAML + markdown)
3. Define compaction detection mechanism
4. Map out all code changes needed
5. Plan implementation phases

---

**Status**: Research in progress, agents still analyzing system
**Next**: Wait for agent outputs, then synthesize complete plan
