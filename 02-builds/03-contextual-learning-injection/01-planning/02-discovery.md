# Contextual Learning Injection - Discovery

**Build Type**: Build
**Purpose**: Surface trigger points and map learning skills to contextual injection system

---

## Trigger-Punkt-Mapping

### Learning Skills & Ihre Trigger

| Learning Skill | Trigger-Punkt | Trigger-Code | Priorität |
|----------------|---------------|--------------|-----------|
| **learn-builds** | plan-build Skill geladen | `tool == 'Read' and 'plan-build/SKILL.md' in path` | HIGH |
| **learn-skills** | create-skill Skill geladen | `tool == 'Read' and 'create-skill/SKILL.md' in path` | HIGH |
| **learn-integrations** | add-integration/connect-* geladen | `tool == 'Read' and ('add-integration' in path or 'connect-' in path)` | HIGH |
| **create-folders** | Erstes Write in workspace | `tool == 'Write' and '04-workspace/' in path` | MEDIUM |
| **learn-nexus** | Kein natürlicher Tool-Trigger | SessionStart Hook nach 3+ Sessions? | LOW |
| **setup-memory** | Erste Session | SessionStart Hook (out of scope) | N/A |

---

## Requirements (EARS Format)

### Functional Requirements

**REQ-1 (Ubiquitous)**: THE system SHALL detect when a user triggers a learning-worthy skill for the first time.

**REQ-2 (Event-Driven)**: WHEN a learning skill trigger is detected AND the corresponding flag is false, THE system SHALL read the complete SKILL.md content from the learning skill directory.

**REQ-3 (Event-Driven)**: WHEN learning skill content is loaded, THE system SHALL inject it into additionalContext with a header indicating "FIRST TIME" execution mode.

**REQ-4 (Ubiquitous)**: THE system SHALL set the corresponding flag to true in user-config.yaml AFTER injection to prevent re-triggering.

**REQ-5 (Ubiquitous)**: THE injected context SHALL instruct Claude to execute the learning skill inline as part of the current workflow.

### Non-Functional Requirements

**REQ-NF-1 (Performance)**: THE system SHALL complete trigger detection and content injection within 100ms of tool execution.

**REQ-NF-2 (Compatibility)**: THE system SHALL maintain backward compatibility with existing MICRO_LESSONS (hardcoded text tips).

**REQ-NF-3 (Maintainability)**: THE mapping between triggers and learning skills SHALL be declaratively defined in a data structure, not scattered in conditional logic.

### Quality Checklist (INCOSE)

- [x] All requirements use EARS patterns (THE/WHEN/WHILE/IF/WHERE)
- [x] No vague terms (quickly, adequate, reasonable, user-friendly)
- [x] No pronouns (it, them, they) - specific names used
- [x] Each requirement independently testable
- [x] Active voice throughout
- [x] No escape clauses (where possible, if feasible)
- [x] Solution-free (what, not how)

---

## Dependencies

### Files to Modify

| File | Changes Needed |
|------|----------------|
| `.claude/hooks/post_tool_use.py` | Add learning skill trigger system, file reading logic |
| `01-memory/user-config.yaml` | Add new flags: `learn_builds_triggered`, `learn_skills_triggered`, etc. |

### Files to Read (Learning Skills)

| File | Purpose |
|------|---------|
| `00-system/skills/learning/learn-builds/SKILL.md` | Build learning content (8-10 min) |
| `00-system/skills/learning/learn-skills/SKILL.md` | Skill learning content (10-12 min) |
| `00-system/skills/learning/learn-integrations/SKILL.md` | Integration learning content (10-12 min) |
| `00-system/skills/learning/create-folders/SKILL.md` | Workspace setup content |

### External Systems

- None (pure local file system operations)

---

## Existing Patterns

| Pattern | Location | Reuse Strategy |
|---------|----------|----------------|
| Trigger detection lambda functions | `post_tool_use.py:36-42` | Extend with new triggers |
| Flag checking | `post_tool_use.py:176-221` | Reuse existing `get_first_encounters()` |
| Flag updating | `post_tool_use.py:223-271` | Reuse existing `update_config_flag()` |
| additionalContext injection | `post_tool_use.py:440-447` | Reuse existing JSON output format |
| Hardcoded MICRO_LESSONS | `post_tool_use.py:34-138` | Keep for backward compat, add new LEARNING_SKILLS dict |

---

## Risks & Unknowns

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Learning skill content too large for additionalContext | Medium | High | Test with actual content length; consider truncated "micro" versions |
| Claude ignores injected skill instructions | Low | High | Clear header: "🎯 FIRST TIME - Execute this lesson NOW" |
| Token limit exceeded in conversation | Medium | Medium | Monitor token usage; learning skills are 200-400 lines |
| Multiple triggers fire simultaneously | Low | Low | Priority system: show only highest-priority trigger |
| File read errors (SKILL.md not found) | Low | Medium | Graceful fallback to simple text tip |

### Open Questions

- [x] Sollen wir vollständigen Skill-Inhalt injizieren oder gekürzte Version? → **Vollständig, da User das "erste Mal" erlebt**
- [x] Wo definieren wir Trigger-Mapping? post_tool_use.py oder in SKILL.md? → **post_tool_use.py (zentral)**
- [ ] Wie testen wir das System ohne echte User-Interaktion?
- [ ] Was passiert wenn Learning Skill Datei fehlt oder korrupt ist?

---

*This discovery document is MANDATORY. It preserves intelligence across compaction.*
*Auto-populate 03-plan.md Dependencies section from findings above.*
