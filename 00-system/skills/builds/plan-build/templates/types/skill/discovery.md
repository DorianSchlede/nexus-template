# {{build_name}} - Discovery

**Build Type**: Skill
**Purpose**: Define skill requirements and discover dependencies

---

## Skill Definition

### Skill Identity

| Attribute | Value |
|-----------|-------|
| Name | {{skill_name}} |
| Slug | {{skill_slug}} |
| Category | {{category}} |
| Complexity | Simple / Medium / Complex |

### Triggers

*Phrases that invoke this skill:*

- "{{trigger_1}}"
- "{{trigger_2}}"
- "{{trigger_3}}"

---

## Requirements (EARS Format)

*All requirements MUST follow EARS patterns. See references/ears-patterns.md for templates.*

### Functional Requirements

**REQ-1**: WHEN user invokes {{skill_name}}, THE skill SHALL {{behavior}}

**REQ-2**: {{ears_pattern}}

**REQ-3**: {{ears_pattern}}

### Non-Functional Requirements

**REQ-NF-1**: THE skill SKILL.md SHALL be under 200 lines

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

## Skill Anatomy

### Structure

```
{{skill_slug}}/
├── SKILL.md              # Workflow definition
├── scripts/              # Python helpers (if needed)
│   └── {{script_name}}.py
├── references/           # Supporting docs (if needed)
│   └── {{reference}}.md
└── assets/               # Static files (if needed)
```

### Resources Needed

| Resource Type | Needed? | Purpose |
|---------------|---------|---------|
| Scripts | Yes/No | {{purpose}} |
| References | Yes/No | {{purpose}} |
| Assets | Yes/No | {{purpose}} |

---

## Dependencies

### Existing Skills to Reference

| Skill | What to Reuse |
|-------|---------------|
| {{skill_name}} | {{pattern_or_approach}} |

### External Systems

- {{system_1}}: {{how_used}}
- {{system_2}}: {{how_used}}

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
