# Onboarding Redesign - Plan

**Build Type**: Build
**Status**: Planning

---

## Context

**Load Before Reading**:
- `01-planning/02-discovery.md` - Requirements and dependencies

---

## Approach

Enhance the existing PostToolUse hook to detect first-time encounters with Nexus concepts and inject contextual micro-lessons. The approach uses a centralized detection system with state persistence in user-config.yaml.

```
┌─────────────────────────────────────────────────────────────────┐
│                     PostToolUse Hook Flow                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Claude calls tool (Write/Read)                                 │
│         │                                                       │
│         ▼                                                       │
│  ┌─────────────────────┐                                       │
│  │ post_tool_use.py    │                                       │
│  │ receives JSON stdin │                                       │
│  └─────────────────────┘                                       │
│         │                                                       │
│         ▼                                                       │
│  ┌─────────────────────┐    ┌──────────────────────┐           │
│  │ Existing logic      │────│ session_id injection │           │
│  │ (keep unchanged)    │    │ tool use logging     │           │
│  └─────────────────────┘    └──────────────────────┘           │
│         │                                                       │
│         ▼                                                       │
│  ┌─────────────────────┐    ┌──────────────────────┐           │
│  │ NEW: Lesson check   │────│ check_micro_lesson() │           │
│  │                     │    │ check_anti_pattern() │           │
│  └─────────────────────┘    └──────────────────────┘           │
│         │                                                       │
│         ▼                                                       │
│  ┌─────────────────────┐    ┌──────────────────────┐           │
│  │ Read user-config    │────│ first_encounters:    │           │
│  │                     │    │   build_created: F   │           │
│  └─────────────────────┘    └──────────────────────┘           │
│         │                                                       │
│         ▼                                                       │
│  ╔═════════════════════╗                                       │
│  ║ Match trigger?      ║                                       │
│  ║ Already seen?       ║                                       │
│  ╚═════════════════════╝                                       │
│         │                                                       │
│    YES  │  NO                                                   │
│         ▼                                                       │
│  ┌─────────────────────┐    ┌──────────────────────┐           │
│  │ Update config flag  │────│ build_created: true  │           │
│  │ Output JSON         │    │ additionalContext    │           │
│  └─────────────────────┘    └──────────────────────┘           │
│         │                                                       │
│         ▼                                                       │
│  Claude sees lesson in <system-reminder>                        │
│  Incorporates naturally into response                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Correctness Properties

*Universal quantifications for property-based testing. Each property must hold for ALL valid inputs.*

**Property 1: Single Lesson Display**
For all tool uses that trigger a lesson, the lesson SHALL appear exactly once across all sessions.
**Validates**: REQ-1, REQ-2, REQ-3, REQ-4, REQ-5

**Property 2: Flag Persistence**
For any lesson shown, the corresponding first_encounters flag SHALL be set to true before hook exits.
**Validates**: REQ-1 through REQ-5

**Property 3: Graceful Degradation**
For any error during lesson detection, the hook SHALL exit with code 0 and not output lesson content.
**Validates**: REQ-NF-2

**Property 4: No Side Effects on Non-Match**
For any tool use that does not match a trigger, the hook SHALL not modify user-config.yaml.
**Validates**: All

---

## Key Decisions

| Decision | Choice | Rationale | Validates |
|----------|--------|-----------|-----------|
| State storage location | user-config.yaml | Already exists, loaded every session, user-editable | REQ-1 through REQ-6 |
| Trigger matching | Lambda functions | Composable, testable, can combine tool + path conditions | REQ-1 through REQ-6 |
| YAML parsing method | Regex patterns | Avoids PyYAML dependency, handles edge cases gracefully | REQ-NF-1, REQ-NF-2 |
| Lesson format | Box-drawn borders | Visually distinct, scannable, non-intrusive | REQ-NF-3 |
| Error handling | Silent exit(0) | Never block Claude's operation for optional feature | REQ-NF-2 |

---

## Dependencies & Links

*Auto-populated from 02-discovery.md*

**Files to Modify**:
| File | Changes | Validates |
|------|---------|-----------|
| `.claude/hooks/post_tool_use.py` | Add MICRO_LESSONS dict, check_micro_lesson(), check_anti_pattern(), output logic | REQ-1 through REQ-6 |
| `01-memory/user-config.yaml` | Add first_encounters and anti_patterns_warned sections | REQ-1 through REQ-6 |
| `00-system/core/nexus/templates/user-config.yaml` | Add template sections for new installs | REQ-1 through REQ-6 |
| `00-system/core/orchestrator.md` | Add contextual-teaching section | Documentation |

**Files to Create**:
None - all modifications to existing files.

**External Systems**:
- Claude Code hook infrastructure: Provides stdin JSON, processes stdout JSON

---

## Testing Strategy

### Property-Based Tests

| Property | Test Strategy |
|----------|---------------|
| P1: Single Lesson Display | Create build twice, verify lesson appears only first time |
| P2: Flag Persistence | Check user-config.yaml after lesson trigger, verify flag is true |
| P3: Graceful Degradation | Send malformed JSON, verify exit code 0 and no output |
| P4: No Side Effects | Trigger non-matching tool, verify config unchanged |

### Unit Tests

| Component | Test Cases |
|-----------|------------|
| check_micro_lesson() | Match each trigger, no-match case, already-seen case |
| check_anti_pattern() | Match "report-jan", "task-1", "week-2", "v3"; no-match "career-plan" |
| get_first_encounters() | Parse valid YAML, handle missing section, handle malformed file |
| update_config_flag() | Add new flag, update existing flag, create missing section |

### Manual Testing Checklist

- [ ] Fresh install: Create first build - see build lesson
- [ ] Same session: Create second build - no lesson
- [ ] Fresh install: Load first skill - see skill lesson
- [ ] Save to workspace first time - see workspace lesson
- [ ] Update goals.md first time - see memory lesson
- [ ] Use close-session first time - see close session lesson
- [ ] Create "report-january" build - see anti-pattern warning
- [ ] Create "report-february" after warning - no second warning

---

## Mental Model Outputs

### Pre-Mortem Analysis Applied

**Imagined Failure**: "The micro-lesson system shipped but nobody noticed the lessons"

**Why it failed:**
1. Lessons were too long and Claude summarized them away
2. Visual formatting didn't stand out in terminal
3. Lessons fired at wrong moment (before action completed)

**Mitigations added:**
- Box-drawn borders (━━━) for visual distinction
- 6 lines max per lesson
- Trigger on Write/Read completion, not before

### First Principles Analysis Applied

**What is truly essential?**
1. Detect first-time action (not second, third, etc.)
2. Inject brief explanation (not tutorial)
3. Persist "shown" state across sessions
4. Never break existing functionality

**What can we remove?**
- Complex YAML parsing (use regex)
- Multiple lessons per session (one is enough)
- Blocking behavior (just inject context)

---

## Open Questions

*Questions that need resolution before or during execution.*

| Question | Resolution | Validates |
|----------|------------|-----------|
| Should build lesson fire on overview.md or any planning file? | Any file in 01-planning/ for reliability | REQ-1 |
| What if user-config.yaml doesn't exist? | Return empty dict, don't create file | REQ-NF-2 |
| Should integration lesson be included in Phase 1? | No, defer to Phase 2 (nice-to-have) | - |

---

*Execution steps in 04-steps.md*
