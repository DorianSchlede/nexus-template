<nexus-system-map version="v4.1" updated="2026-02-01">
<!--
================================================================================
NEXUS SYSTEM MAP - STRUCTURE REFERENCE
================================================================================
Purpose: Navigate Nexus structure and file locations
For AI behavior rules: See orchestrator.md
================================================================================
-->

<section id="structure">
## Core Structure

```
Nexus/
├── 00-system/                      # SYSTEM LAYER (don't modify)
│   ├── core/
│   │   ├── orchestrator.md         # Behavior rules, routing
│   │   ├── nexus-loader.py         # Context injection CLI
│   │   └── nexus/                  # Python modules
│   │       ├── config.py           # Path constants
│   │       ├── loaders.py          # Build/skill loaders
│   │       └── state.py            # State management
│   ├── documentation/              # System docs
│   │   ├── framework-overview.md   # Architecture guide
│   │   └── structure.md            # Folder conventions
│   └── skills/                     # System workflows
│       ├── builds/                 # plan-build, execute-build, archive-build
│       ├── integrations/           # *-connect, *-master skills
│       ├── learning/               # Onboarding & tutorials
│       ├── skill-dev/              # create-skill, import-skill
│       ├── system/                 # close-session, update-nexus
│       └── tools/                  # mental-models, format-code
│
├── 01-memory/                      # PERSISTENCE LAYER
│   ├── goals.md                    # User identity & objectives
│   ├── user-config.yaml            # Preferences, learning tracker
│   ├── core-learnings.md           # Accumulated insights
│   ├── integrations/               # Service configs (langfuse.yaml, etc.)
│   └── session-reports/            # Session history
│
├── 02-builds/                      # BUILD MODE WORK
│   ├── active/                     # Currently active builds
│   │   └── {ID}-{name}/
│   │       ├── 01-planning/        # Purpose, plan, steps
│   │       │   ├── 01-overview.md      # YAML metadata + purpose
│   │       │   ├── 02-discovery.md     # Research, questions
│   │       │   ├── 03-plan.md          # Approach, decisions
│   │       │   ├── 04-steps.md         # Execution checklist
│   │       │   └── resume-context.md   # Cross-session continuity
│   │       ├── 02-resources/       # Reference materials
│   │       ├── 03-working/         # Work in progress
│   │       └── 04-outputs/         # Final deliverables
│   └── complete/                   # Archived/completed builds
│
├── 03-skills/                      # USER SKILLS (your automations)
│   └── {skill-name}/
│       ├── SKILL.md                # YAML metadata + workflow
│       ├── scripts/                # Executable Python (optional)
│       ├── references/             # Supporting docs (optional)
│       └── assets/                 # Templates, files (optional)
│
└── 04-workspace/                   # USER CONTENT
    └── workspace-map.md            # Structure documentation
```
</section>

<section id="execution-flow">
## Execution Flow

```
Session Starts
     ↓
Hook Injects Context (<200ms)
- orchestrator.md (behavior)
- skills catalog (what's available)
- active builds (current work)
- user goals (identity)
- dynamic instructions (what to do next)
     ↓
Claude Executes
- If BUILD work → plan-build or execute-build
- If EXECUTE work → load skill
- If unclear → display menu
```
</section>

<section id="quick-decisions">
## Quick Decisions

| User Says | You Do |
|-----------|--------|
| "Build X" / "Create X" | plan-build |
| "Continue build 29" | execute-build |
| "Send slack message" | Load skill |
| "What can you do?" | Display menu |
</section>

<section id="file-locations">
## File Locations

| Need | Path |
|------|------|
| Behavior rules | `00-system/core/orchestrator.md` |
| User identity | `01-memory/goals.md` |
| User preferences | `01-memory/user-config.yaml` |
| Learnings | `01-memory/core-learnings.md` |
| Integration configs | `01-memory/integrations/*.yaml` |
| Active builds | `02-builds/active/{ID}-{name}/` |
| Completed builds | `02-builds/complete/{ID}-{name}/` |
| System skills | `00-system/skills/{category}/{name}/SKILL.md` |
| User skills | `03-skills/{name}/SKILL.md` |
| User content | `04-workspace/` |
| Workspace index | `04-workspace/workspace-map.md` |
</section>

<section id="workspace-map">
## Workspace Map

The `04-workspace/workspace-map.md` is a **dynamic index** that AI reads every session:

- **You organize**: Place files however you want in 04-workspace/
- **AI reads map**: Understands your structure from the map file
- **Skills auto-save**: Outputs land in documented locations
- **Builds deliver here**: Final deliverables go to 04-outputs/ then here

**Update it**: Say "update workspace map" after reorganizing files.
</section>

<section id="resume-context">
## Resume Context

Each build's `01-planning/resume-context.md` enables cross-session continuity:

```markdown
## Current State
[What's done, what's in progress]

## Next Actions
[Immediate next steps when resuming]

## Key Decisions
[Important choices made during this build]

## Blockers/Questions
[Anything blocking progress]
```

Updated by execute-build skill at session end or when context compacts.
</section>

<section id="cli">
## Nexus CLI

Nexus provides `nexus-*` commands via uv (not Claude Code's Skill system):

```bash
# Context Loading
uv run nexus-load --startup        # Session start context
uv run nexus-load --build {ID}     # Load build by ID
uv run nexus-load --skill {name}   # Load skill by name
uv run nexus-load --list-builds    # List all builds
uv run nexus-load --list-skills    # List all skills

# Build Management
uv run nexus-init-build "Name"     # Create new build
uv run nexus-bulk-complete ...     # Mark tasks complete
uv run nexus-update-resume ...     # Update resume-context

# Mental Models
uv run nexus-mental-models --format list    # List models
uv run nexus-mental-models --category X     # Filter by category

# Skill Development
uv run nexus-init-skill "Name"     # Create new skill
uv run nexus-validate-skill ...    # Validate skill
```

SessionStart hook calls these automatically. Manual use is for debugging.
</section>

</nexus-system-map>
