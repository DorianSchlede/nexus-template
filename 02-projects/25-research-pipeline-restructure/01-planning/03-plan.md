# Discovery Step Implementation - Plan

**Last Updated**: 2026-01-04

---

## Approach

Insert a 5-minute discovery step BEFORE planning: "Let me scan for dependencies to avoid mid-project surprises."

**Focus** (tight, not broad):
- **Dependencies** - Files, systems, APIs this project touches
- **Patterns** - Skills, templates, code to reuse
- **Risks** - What could derail? What's unknown?

**Workflow**:
```
init_project.py → Discovery → overview.md → plan.md → steps.md
     ↓                ↓
  creates:        creates:
  structure +     01-planning/discovery.md
  resume-context  → auto-populates plan.md Dependencies
```

---

## Key Decisions

| Decision | Choice | Why |
|----------|--------|-----|
| Proposal | Always propose | Consistent, no guessing |
| Time | 5-15 min max | Prevents scope creep |
| Name | `discovery.md` | Avoids Research-type confusion |
| Location | `01-planning/` | Part of planning |
| Output | → plan.md Dependencies | Immediate value |
| Mode | AI-driven, user reviews | Fast, low friction |

---

## Dependencies

**Modify**:
- `create-project/SKILL.md` - Add to CRITICAL EXECUTION REQUIREMENTS
- `create-project/references/workflows.md` - Insert Step 4.5

**Create**:
- `create-project/scripts/templates/discovery-template.md`

**Related**: Project 24 (parent - research scope extracted here)

---

## Pre-Mortem

| Risk | Prevention |
|------|------------|
| Users skip | "5 min to avoid surprises" value prop |
| Output unused | Auto-populate Dependencies |
| Takes too long | Hard time-box |
| Feels like busywork | ACTIONABLE findings only |

---

*Next: Phase 2 Implementation*
