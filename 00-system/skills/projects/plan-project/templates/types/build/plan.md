# {{project_name}} - Plan

**Project Type**: Build
**Status**: Planning

---

## Context

**Load Before Reading**:
- `01-planning/02-discovery.md` - Requirements and dependencies

---

## Approach

*High-level strategy for implementing this project.*

{{approach_description}}

```
{{architecture_diagram}}
```

---

## Correctness Properties

*Universal quantifications for property-based testing. Each property must hold for ALL valid inputs.*

**Property 1: {{property_name}}**
For all {{inputs}}, the system {{guarantee}}.
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

*Auto-populated from 02-discovery.md*

**Files to Modify**:
| File | Changes | Validates |
|------|---------|-----------|
| {{file}} | {{changes}} | REQ-{{number}} |

**Files to Create**:
| File | Purpose | Validates |
|------|---------|-----------|
| {{file}} | {{purpose}} | REQ-{{number}} |

**External Systems**:
- {{system}}: {{usage}}

---

## Testing Strategy

### Property-Based Tests

| Property | Test Strategy |
|----------|---------------|
| P1: {{name}} | {{how_to_test}} |
| P2: {{name}} | {{how_to_test}} |

### Unit Tests

| Component | Test Cases |
|-----------|------------|
| {{component}} | {{cases}} |

---

## Open Questions

*Questions that need resolution before or during execution.*

| Question | Resolution | Validates |
|----------|------------|-----------|
| {{question}} | {{answer_or_pending}} | REQ-{{number}} |

---

*Execution steps in 04-steps.md*
