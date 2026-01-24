# Contextual Learning Injection - Plan

**Build Type**: Build
**Status**: Planning

---

## Context

**Load Before Reading**:
- `01-planning/02-discovery.md` - Requirements and dependencies

---

## Approach

### High-Level Strategy

**CRITICAL INSIGHT**: Neuer User sagt NICHT "erstelle einen Skill" - er sagt "Ich brauche jeden Montag einen Report". Nexus Routing entscheidet, plan-build ist IMMER der erste Kontakt.

**Architectural Clarity** (See: 02-resources/nexus-architecture-clarity.md):
- BUILD = Process of creating capabilities (verb: "let's start building")
- SKILL = Executable capability (does the work on workspace materials)
- WORKSPACE = Context store + Build area + Material for skills
- plan-build = Gateway workflow for building ANY type
- Skills are ONE important BUILD TYPE (not opposite of builds)

**Gateway Lesson Konzept**: "Getting Started" erklärt Nexus als Building System - 8 Types you can build, with Skills being the most valuable for recurring work. NOT "builds vs skills" framing.

Erweitern des bestehenden PostToolUse Hook-Systems mit **situativen User-Choice Prompts**:

1. **Behalte alte MICRO_LESSONS** (hardcoded Text für memory, close-session)
2. **Füge LEARNING_SKILLS Dictionary hinzu** (nur 2 Auto-Trigger!)
3. **User-Controlled**: Hook fragt User ob er Lektion will (1: Load / 2: Skip now / 3: Skip forever)
4. **Injection Format**: Frage + Handling-Anweisungen (Claude entscheidet basierend auf User Choice)

### Architektur

```
User Action (z.B. "Erstelle ein Rezeptbuch")
    ↓
Nexus Routing → Lädt plan-build Skill
    ↓
Claude: Read tool → plan-build/SKILL.md
    ↓
PostToolUse Hook ausgeführt
    ↓
┌─────────────────────────────────────────┐
│ 1. Check LEARNING_SKILLS triggers      │
│    - plan-build detected?              │
│    - Flag: learn_builds_triggered?     │
│    ✓ YES → Proceed                     │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│ 2. Read Learning Skill Content         │
│    Path: 00-system/skills/learning/    │
│           learn-builds/SKILL.md         │
│    Content: ~250 lines                  │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│ 3. Inject via additionalContext        │
│    Format:                              │
│    🎯 FIRST TIME: BUILD PLANNING        │
│    Execute this contextual lesson NOW:  │
│    [FULL SKILL.MD CONTENT]              │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│ 4. Set Flag                             │
│    user-config.yaml:                    │
│    first_encounters:                    │
│      learn_builds_triggered: true       │
└─────────────────────────────────────────┘
    ↓
Claude receives additionalContext
    ↓
Claude executes learning skill INLINE
    ↓
User learns WHILE doing (Teach Through Doing!)
```

---

## Correctness Properties

**Property 1: Exactly-Once Execution**
For all learning skill triggers, the system SHALL inject the learning skill content exactly once per user (first encounter only).
**Validates**: REQ-1, REQ-4

**Property 2: Content Completeness**
For any triggered learning skill, the injected content SHALL be the complete, unmodified SKILL.md file content.
**Validates**: REQ-2

**Property 3: Flag Persistence**
For any learning skill injection, the corresponding flag SHALL be set to true BEFORE the hook exits, ensuring idempotency across restarts.
**Validates**: REQ-4

**Property 4: Backward Compatibility**
For all existing MICRO_LESSONS triggers, the system SHALL continue to function identically to pre-change behavior.
**Validates**: REQ-NF-2

---

## Key Decisions

| Decision | Choice | Rationale | Validates |
|----------|--------|-----------|-----------|
| **Number of Auto-Triggers** | Only 2 (getting-started + create-folders) | getting-started is GATEWAY lesson (Building System, 8 Types, Skills). Prevents nesting confusion. User says "Ich brauche Reports", NOT "erstelle Skill". | REQ-1, User Experience |
| **User Choice Model** | Ask user (1: Load / 2: Skip now / 3: Skip forever) | Respects user autonomy. No forced interruption. User controls learning pace. | REQ-5, User Experience |
| **Injection Format** | Prompt + Handling Instructions (NOT full content) | Smaller payload. Claude reads skill only if user chooses 1. No wasted file reads. | REQ-2, REQ-3, Performance |
| **Flag Setting** | Claude sets flag (not Hook) | Hook only offers. Claude sets flag if user chooses "skip forever". Flag stays false if "skip now" (ask again next time). | REQ-4 |
| **Gateway Lesson** | getting-started explains Building System | Teaches 8 Build Types with Skills as most important. NOT "builds vs skills" (confusing dichotomy). Optional deep-dives (learn-skills, learn-integrations) via manual trigger. | User Experience, Architectural Clarity |
| **Manual Deep-Dives** | learn-skills, learn-integrations, learn-nexus | User says "learn skills" when ready for deep-dive. Not auto-triggered via Hook. Prevents overwhelming new users. | User Experience |
| **Priority System** | LEARNING_SKILLS checked before MICRO_LESSONS | Learning prompts more valuable than micro-tips. Micro-lessons = fallback for simpler contexts. | REQ-5 |
| **Backward Compat** | Keep MICRO_LESSONS (memory_updated, close_session_used) | Preserves existing micro-lessons. No breaking changes. | REQ-NF-2 |

---

## Dependencies & Links

*Auto-populated from 02-discovery.md*

**Files to Modify**:
| File | Changes | Validates |
|------|---------|-----------|
| `.claude/hooks/post_tool_use.py` | Add LEARNING_SKILLS dict, add `load_learning_skill()` function, add trigger checking before MICRO_LESSONS | REQ-1, REQ-2, REQ-3, REQ-4, REQ-5 |
| `01-memory/user-config.yaml` | Add new flags: `getting_started_offered`, `create_folders_offered` | REQ-4 |
| `00-system/skills/learning/getting-started/SKILL.md` | CREATE NEW: Gateway lesson explaining Building System, 8 Types, Skills | Content |
| `00-system/core/nexus/templates/user-config.yaml` | Add same flags as template for new users | REQ-4 |

**Files to Read (at runtime)**:
| File | Purpose | Validates |
|------|---------|-----------|
| `00-system/skills/learning/getting-started/SKILL.md` | Gateway lesson: Building System, 8 Types, Skills | REQ-2 |
| `00-system/skills/learning/create-folders/SKILL.md` | Workspace setup lesson | REQ-2 |

**Manual Deep-Dive Skills** (NOT auto-triggered):
| File | Manual Trigger | Purpose |
|------|----------------|---------|
| `00-system/skills/learning/learn-skills/SKILL.md` | User says "learn skills" | Deep-dive: Skill-Worthiness Framework, Advanced Triggering |
| `00-system/skills/learning/learn-integrations/SKILL.md` | User says "learn integrations" | Deep-dive: MCP Protocol, Integration Best Practices |
| `00-system/skills/learning/learn-nexus/SKILL.md` | User says "learn nexus" | Deep-dive: Philosophy, Expert Patterns, System Mastery |

**External Systems**:
- None

---

## Implementation Details

### New Data Structure: LEARNING_SKILLS

**Only 2 Auto-Triggers** (Gateway + Workspace):

```python
LEARNING_SKILLS: Dict[str, Dict] = {
    'getting_started_offered': {
        'triggers': [
            lambda tool, path: (
                tool == 'Read' and
                'plan-build/SKILL.md' in path
            ),
        ],
        'skill_path': '00-system/skills/learning/getting-started/SKILL.md',
        'duration': '10-12 min',
        'topics': 'Building System, 8 Build Types, Skills as Executable Work, Workspace Role',
        'prompt_template': '''🎯 FIRST TIME: BUILDING WITH NEXUS

This is your first time building something in Nexus. Would you like me to:
1) Load the 10-12 min "Getting Started" lesson (covers: Building System, 8 Types you can build, Skills for recurring work)
2) Skip for now (I'll ask again next time)
3) Skip forever (don't ask again)

Choose 1, 2, or 3.

HANDLE USER CHOICE:

Choice 1 - Load lesson:
  - Read: {skill_path}
  - Execute the full lesson
  - Continue with plan-build after lesson completes

Choice 2 - Skip for now:
  - Do NOT modify user-config.yaml flags
  - Continue with plan-build immediately
  - Next time plan-build triggers, ask again

Choice 3 - Skip forever:
  - Edit 01-memory/user-config.yaml
  - Set first_encounters.getting_started_offered: true
  - Continue with plan-build immediately
  - Never ask again
'''
    },
    'create_folders_offered': {
        'triggers': [
            lambda tool, path: (
                tool == 'Write' and
                '04-workspace/' in path
            ),
        ],
        'skill_path': '00-system/skills/learning/create-folders/SKILL.md',
        'duration': '5 min',
        'topics': 'Workspace Structure Setup, Organization Patterns',
        'prompt_template': '''🎯 FIRST TIME: WORKSPACE USAGE

This is your first time using the workspace. Would you like me to:
1) Load the 5 min "Create Folders" lesson now (covers: Workspace Structure Setup, Organization)
2) Skip for now (I'll ask again next time)
3) Skip forever (don't ask again)

Choose 1, 2, or 3.

HANDLE USER CHOICE:
[Same handling logic as above]
'''
    },
}
```

**Manual Deep-Dives** (User says "learn skills", "learn integrations", "learn nexus"):
- These are NOT in PostToolUse Hook
- Available as regular skills via Nexus routing
- User triggers when they want deep-dive

### New Function: generate_learning_prompt()

```python
def generate_learning_prompt(skill_data: Dict) -> str:
    """
    Generate user-choice prompt with handling instructions.

    Does NOT load skill content yet - that happens if user chooses 1.
    Returns formatted prompt string.
    """
    return skill_data['prompt_template'].format(
        skill_path=skill_data['skill_path']
    )
```

**Why NOT load content immediately?**
- User might choose "skip" → wasted file read
- User-controlled → respects user autonomy
- Claude handles the loading based on user choice
- Smaller injection payload (prompt vs 200+ lines)

### Modified main() Flow

```python
def main():
    # ... existing setup ...

    config_path = Path('01-memory/user-config.yaml')

    # --- NEW: CHECK LEARNING SKILLS FIRST (higher priority) ---

    encounters = get_first_encounters(config_path)

    for skill_id, skill_data in LEARNING_SKILLS.items():
        # Skip if already offered/dismissed
        if encounters.get(skill_id, False):
            continue

        # Check triggers
        for trigger_fn in skill_data['triggers']:
            try:
                if trigger_fn(tool_name, file_path):
                    # Generate user-choice prompt (NOT loading skill yet!)
                    prompt = generate_learning_prompt(skill_data)

                    # Inject prompt with handling instructions
                    output = {
                        "hookSpecificOutput": {
                            "hookEventName": "PostToolUse",
                            "additionalContext": prompt
                        }
                    }
                    print(json.dumps(output), flush=True)
                    sys.exit(0)

                    # NOTE: Flag is NOT set here!
                    # Claude sets flag based on user choice (3 = skip forever)
            except Exception:
                continue

    # --- EXISTING: CHECK MICRO_LESSONS (fallback) ---
    lesson = check_micro_lesson(tool_name, tool_input, config_path)
    # ... rest of existing code ...
```

**Critical Change**: Hook does NOT set flag automatically. Claude sets flag only if user chooses "Skip forever" (option 3).

---

## Testing Strategy

### Property-Based Tests

| Property | Test Strategy |
|----------|---------------|
| P1: Exactly-Once Execution | Set flag to false, trigger twice, verify injection only on first trigger |
| P2: Content Completeness | Compare injected content with direct file read, verify identical |
| P3: Flag Persistence | Trigger learning skill, restart hook process, verify flag still true |
| P4: Backward Compatibility | Trigger old MICRO_LESSONS, verify identical behavior to baseline |

### Manual Tests

| Test Case | Steps | Expected Result |
|-----------|-------|-----------------|
| **learn-builds trigger** | 1. Set `learn_builds_triggered: false`<br>2. User says "create recipe book"<br>3. Routing loads plan-build<br>4. Hook runs | additionalContext contains full learn-builds/SKILL.md content |
| **learn-skills trigger** | 1. Set `learn_skills_triggered: false`<br>2. User says "create skill for weekly report"<br>3. Routing loads create-skill<br>4. Hook runs | additionalContext contains full learn-skills/SKILL.md content |
| **No re-trigger** | 1. Complete above test<br>2. Trigger same skill again | No injection (flag is true) |
| **Graceful failure** | 1. Rename SKILL.md temporarily<br>2. Trigger learning skill | Hook exits cleanly, no crash |

---

## Open Questions

| Question | Resolution | Validates |
|----------|------------|-----------|
| Token limits: Can we inject 200-400 line skills safely? | TEST FIRST with actual content. If issues, create truncated "micro" versions. | REQ-NF-1 |
| Will Claude reliably execute injected content? | Test with clear headers and instructions. Monitor real usage. | REQ-5 |
| How to test without real user sessions? | Manual flag manipulation + hook execution with mock tool_use input | All |
| Should we log learning skill injections? | YES - add to existing log_tool_use() for debugging | REQ-NF-1 |

---

*Execution steps in 04-steps.md*
