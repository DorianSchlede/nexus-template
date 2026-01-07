---
session_id: ""
session_ids: []
resume_schema_version: "2.0"
last_updated: "2026-01-07T20:40:00Z"

# PROJECT
project_id: "43-agent-eval-enhancement-with-prompt-tuner-patterns"
project_name: "Agent Eval Enhancement with Prompt-Tuner Patterns"
project_type: "build"
current_phase: "execution"

# LOADING - Updated dynamically
next_action: "execute-project"
files_to_load:
  - "01-planning/04-steps.md"
  - "02-resources/source-reference/"

# SKILL TRACKING (v2.3 simplified - optional)
# current_skill: ""

# DISCOVERY STATE
rediscovery_round: 0
discovery_complete: true

# PROGRESS
current_section: 1
current_task: 1
total_tasks: 66
tasks_completed: 0
---

## Progress Summary

**Project Type**: build
**Phase**: Execution - Phase 1

### Source Resources Copied

All source files copied from `mutagent-monorepo/prompt-tuner/` to `02-resources/source-reference/`:

```
source-reference/
├── failure-analysis/
│   ├── failure-analysis-prompt.ts   # CIA Agent prompt
│   ├── failure-analysis-schema.ts   # Zod output schema
│   └── prompt-failure-modes.ts      # TypeScript interfaces
├── success-analysis/
│   ├── success-analysis-prompt.ts   # Pattern Analyst prompt
│   ├── success-analysis-schema.ts   # Zod output schema
│   └── prompt-success-modes.ts      # TypeScript interfaces
├── eval-criteria/
│   ├── eval-criteria-prompt.ts      # G-Eval derivation prompt
│   └── eval-criteria-schema.ts      # Zod output schema
└── shared/
    └── shared-analysis-schemas.ts   # PromptSection, PromptVariable, etc.
```

### Current Phase: 1 - Extract and Adapt Prompts

**Next Task**: 1.1 Extract Failure Analysis Prompt
- Create `02-resources/extracted-prompts/failure-analysis.md`
- Adapt terminology: PromptSection → AgentInstruction, etc.

### Key Deliverables

**2 New Subagents**:
- `agent-failure-analyzer.md` - Root cause analysis with 9-category taxonomy
- `agent-success-analyzer.md` - Success pattern identification

**3 New Skills**:
- `analyze-agent-failures` - Skill for failure analysis
- `analyze-agent-successes` - Skill for success analysis
- `derive-eval-criteria` - Skill for criteria generation

**1 Enhanced Subagent**:
- `test-case-analyzer.md` - Add root cause analysis

### Next Steps

Continue with Phase 1.1: Extract and adapt failure analysis prompt.

---

*Auto-updated by execute-project skill on task/section completion*
