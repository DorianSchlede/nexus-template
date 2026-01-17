# Onboarding Redesign - Discovery

**Build Type**: Build
**Purpose**: Surface requirements and dependencies before planning

---

## Requirements (EARS Format)

*All requirements MUST follow EARS patterns. See references/ears-patterns.md for templates.*

### Functional Requirements

**REQ-1**: WHEN the Write tool creates a file in `02-builds/*/01-planning/` for the first time, THE PostToolUse hook SHALL inject the build_created micro-lesson into Claude's context.

**REQ-2**: WHEN the Read tool loads a `SKILL.md` file from `03-skills/` or `00-system/skills/` for the first time, THE PostToolUse hook SHALL inject the skill_loaded micro-lesson into Claude's context.

**REQ-3**: WHEN the Write tool creates a file in `04-workspace/` for the first time, THE PostToolUse hook SHALL inject the workspace_used micro-lesson into Claude's context.

**REQ-4**: WHEN the Write tool modifies `01-memory/goals.md` or `01-memory/core-learnings.md` for the first time, THE PostToolUse hook SHALL inject the memory_updated micro-lesson into Claude's context.

**REQ-5**: WHEN the Read tool loads `close-session/SKILL.md` for the first time, THE PostToolUse hook SHALL inject the close_session_used micro-lesson into Claude's context.

**REQ-6**: WHEN the Write tool creates a build with a repeated naming pattern (ends with `-jan`, `-1`, `-week1`, `-v2`), THE PostToolUse hook SHALL inject an anti-pattern warning into Claude's context.

### Non-Functional Requirements

**REQ-NF-1**: THE PostToolUse hook SHALL complete micro-lesson detection within 50ms to avoid perceptible delay.

**REQ-NF-2**: THE PostToolUse hook SHALL exit with code 0 on any error to prevent blocking Claude's operation.

**REQ-NF-3**: THE micro-lesson content SHALL be readable within 15 seconds (max 6 lines of text).

### Quality Checklist (INCOSE)

*Verify each requirement meets INCOSE quality rules:*

- [x] All requirements use EARS patterns (THE/WHEN/WHILE/IF/WHERE)
- [x] No vague terms (quickly, adequate, reasonable, user-friendly)
- [x] No pronouns (it, them, they) - specific names used
- [x] Each requirement independently testable
- [x] Active voice throughout
- [x] No escape clauses (where possible, if feasible)
- [x] Solution-free (what, not how)

---

## Dependencies

*Files, systems, APIs this build will touch*

### Files to Modify

| File | Changes Needed |
|------|----------------|
| `.claude/hooks/post_tool_use.py` | Add micro-lesson detection logic, trigger functions, additionalContext output |
| `01-memory/user-config.yaml` | Add first_encounters and anti_patterns_warned sections |
| `00-system/core/nexus/templates/user-config.yaml` | Add template for new sections (for fresh installs) |
| `00-system/core/orchestrator.md` | Add contextual-teaching section explaining how lessons work |

### Files to Create

| File | Purpose |
|------|---------|
| None | All changes modify existing files |

### External Systems

- Claude Code hook infrastructure: Receives JSON stdin, outputs JSON stdout with additionalContext
- user-config.yaml: State persistence for first_encounters flags

---

## Existing Patterns

*Skills, templates, code to reuse*

| Pattern | Location | Reuse Strategy |
|---------|----------|----------------|
| JSON stdin parsing | `.claude/hooks/post_tool_use.py:53-61` | Extend existing main() function |
| Session ID injection | `.claude/hooks/post_tool_use.py:14-50` | Keep intact, add lesson logic after |
| additionalContext output | `.claude/hooks/session_start.py:921-944` | Copy JSON output format pattern |
| YAML flag reading | `.claude/hooks/utils/` | Use regex pattern from existing code |

---

## Risks & Unknowns

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Hook slows down tool execution | Low | High | Keep detection logic O(1), exit early on already-seen lessons |
| YAML parsing breaks on malformed config | Medium | Medium | Use regex instead of full YAML parser, handle exceptions gracefully |
| Lesson content too long, Claude ignores | Low | Medium | Test with real sessions, keep to 6 lines max |
| Multiple lessons fire in same session | Low | Low | Only one lesson per tool use, first match wins |

### Open Questions

- [x] How does additionalContext injection work? (Answered: JSON stdout with hookSpecificOutput.additionalContext)
- [x] Where to store first_encounters state? (Answered: user-config.yaml)
- [x] Should lessons block tool execution? (Answered: No, just inject context)

---

## Technical Findings from Investigation

### Hook Input Format
```json
{
  "hook_event_name": "PostToolUse",
  "session_id": "uuid",
  "tool_name": "Write|Read|Bash|...",
  "tool_input": {"file_path": "..."},
  "tool_result": {...}
}
```

### Required Output Format for Injection
```json
{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "━━━ QUICK TIP: BUILDS ━━━..."
  }
}
```

### Trigger Detection Logic
```python
MICRO_LESSONS = {
    'build_created': {
        'triggers': [
            lambda tool, path: (
                tool == 'Write' and
                '02-builds/' in path and
                ('overview.md' in path or '/01-planning/' in path)
            ),
        ],
        'content': '...'
    },
    # ... more lessons
}
```

---

*This discovery document is MANDATORY. It preserves intelligence across compaction.*
*Auto-populate 03-plan.md Dependencies section from findings above.*
