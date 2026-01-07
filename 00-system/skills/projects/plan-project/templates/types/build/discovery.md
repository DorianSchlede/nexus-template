# {{project_name}} - Discovery

**Project Type**: Build
**Purpose**: Surface requirements and dependencies before planning

---

## Requirements (EARS Format)

*All requirements MUST follow EARS patterns. See references/ears-patterns.md for templates.*

### Functional Requirements

**REQ-1**: {{ears_pattern}}

**REQ-2**: {{ears_pattern}}

**REQ-3**: {{ears_pattern}}

### Non-Functional Requirements

**REQ-NF-1**: {{ears_pattern}}

**REQ-NF-2**: {{ears_pattern}}

### Quality Checklist (INCOSE)

*Verify each requirement meets INCOSE quality rules:*

- [ ] All requirements use EARS patterns (THE/WHEN/WHILE/IF/WHERE)
- [ ] No vague terms (quickly, adequate, reasonable, user-friendly)
- [ ] No pronouns (it, them, they) - specific names used
- [ ] Each requirement independently testable
- [ ] Active voice throughout
- [ ] No escape clauses (where possible, if feasible)
- [ ] Solution-free (what, not how)

---

## Dependencies

*Files, systems, APIs this project will touch*

### Files to Modify

| File | Changes Needed |
|------|----------------|
| {{file_path}} | {{change_description}} |

### Files to Create

| File | Purpose |
|------|---------|
| {{file_path}} | {{purpose}} |

### External Systems

- {{system_1}}: {{how_used}}
- {{system_2}}: {{how_used}}

---

## Existing Patterns

*Skills, templates, code to reuse*

| Pattern | Location | Reuse Strategy |
|---------|----------|----------------|
| {{pattern}} | {{location}} | {{strategy}} |

---

## Risks & Unknowns

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| {{risk}} | Low/Medium/High | Low/Medium/High | {{mitigation}} |

### Open Questions

- [ ] {{question_1}}
- [ ] {{question_2}}

---

*This discovery document is MANDATORY. It preserves intelligence across compaction.*
*Auto-populate 03-plan.md Dependencies section from findings above.*
