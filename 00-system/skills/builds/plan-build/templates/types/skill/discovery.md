# {{build_name}} - Discovery

**Build Type**: Skill
**Purpose**: Define skill requirements and discover dependencies

---

## Discovery Questions

*Answers from Phase 2a - understand what user wants to build*

### What Skill Are You Creating?

{{skill_description}}

### What Problem Does This Solve?

{{problem_statement}}

### When Should This Skill Trigger?

{{trigger_scenarios}}

### Constraints & Requirements

- {{constraint_1}}
- {{constraint_2}}

### What Does Success Look Like?

{{success_criteria}}

---

## AI Codebase Research

*Findings from Phase 2b automated exploration*

### Files Analyzed

**Complexity Assessment**: Simple / Medium / Complex
**Agents Used**: {{agent_count}}
**Files Found**: {{file_count}}

### Similar Skills Found

| Skill | Location | Relevance |
|-------|----------|-----------|
| {{skill_name}} | {{location}} | {{how_similar}} |

### Existing Patterns

*What exists currently that relates to this skill*

{{existing_patterns_summary}}

### Impact Assessment

*How this skill affects existing code*

{{impact_summary}}

---

## AI Web Research (Optional)

*Best practices from web search - skip if not requested*

### Queries Performed

1. {{query_1}}
2. {{query_2}}
3. {{query_3}}

### Best Practices Found

| Practice | Source | Relevance |
|----------|--------|-----------|
| {{practice}} | {{source_url}} | {{relevance}} |

### Recommendations

- {{recommendation_1}}
- {{recommendation_2}}

---

## Related Builds & Skills

*Existing work that relates to this skill*

### Related Builds

| Build | Status | Relevance |
|-------|--------|-----------|
| {{build_id}} | {{status}} | {{why_related}} |

### Related Skills

| Skill | Location | How to Reuse |
|-------|----------|--------------|
| {{skill_name}} | {{location}} | {{reuse_strategy}} |

---

## Follow-up Questions

*Type-specific questions from Phase 2c, informed by research findings*
*If new areas discovered → loop back to AI Research (max 2 loops)*

### Skill Definition

#### Skill Identity

| Attribute | Value |
|-----------|-------|
| Name | {{skill_name}} |
| Slug | {{skill_slug}} |
| Category | {{category}} |
| Complexity | Simple / Medium / Complex |

#### Triggers

*Phrases that invoke this skill:*

- "{{trigger_1}}"
- "{{trigger_2}}"
- "{{trigger_3}}"

---

### Requirements (EARS Format)

*All requirements MUST follow EARS patterns. See references/ears-patterns.md for templates.*

#### Functional Requirements

**REQ-1**: WHEN user invokes {{skill_name}}, THE skill SHALL {{behavior}}

**REQ-2**: {{ears_pattern}}

**REQ-3**: {{ears_pattern}}

#### Non-Functional Requirements

**REQ-NF-1**: THE skill SKILL.md SHALL be under 200 lines

**REQ-NF-2**: {{ears_pattern}}

#### Quality Checklist (INCOSE)

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
