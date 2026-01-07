# {{project_name}} - Plan

**Project Type**: Skill
**Status**: Planning

---

## Context

**Load Before Reading**:
- `01-planning/02-discovery.md` - Skill requirements and anatomy

---

## Approach

*How will this skill be implemented?*

{{approach_description}}

### Workflow Outline

```
User invokes "{{trigger}}"
    │
    ├── Step 1: {{step_description}}
    ├── Step 2: {{step_description}}
    └── Step 3: {{step_description}}
```

---

## Correctness Properties

*Universal quantifications for property-based testing.*

**Property 1: {{property_name}}**
For all valid invocations, the skill {{guarantee}}.
**Validates**: REQ-{{numbers}}

**Property 2: {{property_name}}**
For any {{condition}}, {{invariant_statement}}.
**Validates**: REQ-{{numbers}}

---

## Key Decisions

| Decision | Choice | Rationale | Validates |
|----------|--------|-----------|-----------|
| {{decision}} | {{choice}} | {{why}} | REQ-{{number}} |

---

## Dependencies & Links

**Files to Create**:
| File | Purpose | Validates |
|------|---------|-----------|
| `{{skill_slug}}/SKILL.md` | Main workflow | REQ-{{number}} |
| `{{skill_slug}}/scripts/{{name}}.py` | Helper script | REQ-{{number}} |

**External Systems**:
- {{system}}: {{usage}}

---

## Testing Strategy

### Property-Based Tests

| Property | Test Strategy |
|----------|---------------|
| P1: {{name}} | {{how_to_test}} |
| P2: {{name}} | {{how_to_test}} |

### Manual Tests

| Scenario | Expected Outcome |
|----------|------------------|
| {{invocation}} | {{result}} |

---

## Open Questions

| Question | Resolution | Validates |
|----------|------------|-----------|
| {{question}} | {{answer_or_pending}} | REQ-{{number}} |

---

*Execution steps in 04-steps.md*
