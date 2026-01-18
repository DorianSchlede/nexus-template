# State System Refactor - Plan

**Build Type**: Build
**Status**: Planning

---

## Context

**Load Before Reading**:
- `01-planning/02-discovery.md` - Requirements and dependencies

---

## Approach

Establish `learning_tracker.completed` in user-config.yaml as the SINGLE SOURCE OF TRUTH for onboarding state. Remove all redundant detection methods.

```
BEFORE (messy):
┌─────────────────┐   ┌────────────────────┐   ┌──────────────────┐
│ is_template_file│   │ check_workspace_   │   │ learning_tracker │
│ (smart_default) │   │ configured()       │   │ .completed       │
└────────┬────────┘   └─────────┬──────────┘   └────────┬─────────┘
         │                      │                       │
         ▼                      ▼                       ▼
    CONFLICT! Different sources give different answers!

AFTER (clean):
┌──────────────────────────────────────────────────────────────────┐
│                  learning_tracker.completed                       │
│  setup_memory: true/false | create_folders: true/false | etc.   │
└──────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                   SINGLE SOURCE OF TRUTH
```

---

## Correctness Properties

**Property 1: State Consistency**
For all valid user-config.yaml files, the system derives the same onboarding state regardless of file template status.
**Validates**: REQ-1, REQ-3

**Property 2: Menu Accuracy**
For any value of `learning_tracker.completed.create_folders`, the menu displays the corresponding status correctly.
**Validates**: REQ-2

---

## Key Decisions

| Decision | Choice | Rationale | Validates |
|----------|--------|-----------|-----------|
| Single source of truth | user-config.yaml `learning_tracker.completed` | Only reliable record of "user completed skill X" | REQ-1 |
| Keep is_template_file() | Yes, for validation/logging only | Useful for debugging, but not for state | REQ-3 |
| Remove check_* functions | Yes | They use wrong detection method | REQ-1, REQ-NF-1 |

---

## Dependencies & Links

**Files to Modify**:
| File | Changes | Validates |
|------|---------|-----------|
| `00-system/core/nexus/state.py` | Remove check_workspace_configured(), check_goals_personalized() | REQ-1, REQ-NF-1 |
| `.claude/hooks/session_start.py` | Use learning_tracker for goals_personalized and workspace_configured | REQ-1, REQ-2 |

**Files to Create**:
None

**External Systems**:
None

---

## Testing Strategy

### Property-Based Tests

| Property | Test Strategy |
|----------|---------------|
| P1: State Consistency | Test with various user-config.yaml values, verify same state output |
| P2: Menu Accuracy | Test hook output for each combination of learning_tracker values |

### Unit Tests

| Component | Test Cases |
|-----------|------------|
| extract_learning_completed() | Missing file, empty file, partial data, complete data |
| Session hook state detection | All combinations of learning_tracker.completed values |

---

## Open Questions

| Question | Resolution | Validates |
|----------|------------|-----------|
| Should we migrate old configs? | No, extract_learning_completed() has defaults | REQ-1 |

---

*Execution steps in 04-steps.md*
