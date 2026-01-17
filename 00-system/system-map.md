<nexus-system-map version="v4.0" updated="2026-01-07">
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
├── 00-system/
│   ├── core/
│   │   ├── orchestrator.md         # Behavior rules, routing
│   │   └── nexus-loader.py         # Context injection
│   └── skills/                     # System workflows
│
├── 01-memory/
│   ├── goals.md                    # User identity
│   └── session-reports/            # History
│
├── 02-builds/                    # BUILD mode work (active)
│   └── {ID}-{name}/
│       ├── 01-planning/            # 4 phases
│       └── 04-outputs/             # Deliverables
│
├── 03-skills/                      # EXECUTE mode work
│   └── {skill-name}/SKILL.md       # Workflows
│
├── 04-workspace/                   # User content
│   └── workspace-map.md            # Structure doc
│
└── 05-archived/                    # Completed builds
    └── {ID}-{name}/                # Archived build folders
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
| Active builds | `02-builds/{ID}-{name}/` |
| Workflows | `03-skills/{name}/SKILL.md` |
| User content | `04-workspace/` |
| Archived builds | `05-archived/{ID}-{name}/` |
</section>

<section id="cli">
## CLI Commands

```bash
# Load build context
python 00-system/core/nexus-loader.py --build {ID}

# Load skill
python 00-system/core/nexus-loader.py --skill {name}

# Discover skills in category
load-skill {category} --help
```
</section>

</nexus-system-map>
