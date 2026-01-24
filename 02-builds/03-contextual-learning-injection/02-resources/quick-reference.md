# Contextual Learning Injection - Quick Reference

**Build**: 03-contextual-learning-injection
**Status**: PLANNING → Ready for Implementation
**Erstellt**: 2026-01-23

---

## 🎯 Core Concept (30 Sekunden)

**Was**: Hook-System, das automatisch Learning Skills beim ersten Kontakt anbietet
**Wie**: PostToolUse Hook erkennt Trigger → User-Choice Prompt (1/2/3) → Claude handled
**Warum**: "Teach Through Doing" - User lernt WÄHREND er arbeitet, nicht vorher

---

## 📦 Auto-Trigger Skills (Nur 2!)

| Skill | Trigger | Duration | Reason |
|-------|---------|----------|--------|
| **learn-builds** | First `plan-build` load | 8-10 min | Gateway Lesson (erklärt ALLES) |
| **create-folders** | First `04-workspace/` write | 5 min | Workspace Setup (separater Kontext) |

**NICHT auto-triggered**:
- learn-skills → Schon in learn-builds erklärt
- learn-integrations → Schon in learn-builds erklärt
- learn-nexus → Deep-Dive, User sagt manuell "learn nexus"

---

## 🔄 User Journey (3 Schritte)

### 1. Trigger Detection
```
User: "create recipe book"
  → Nexus Routing: plan-build
  → Read: plan-build/SKILL.md
  → Hook: MATCH!
```

### 2. User Choice
```
Claude: 🎯 FIRST TIME: BUILD PLANNING
        1) Load 8-10min lesson
        2) Skip now (ask again)
        3) Skip forever (don't ask)
```

### 3. Handling
```
Choice 1: Load + Execute + Set Flag
Choice 2: Continue (Flag stays FALSE)
Choice 3: Continue + Set Flag
```

---

## 🏗️ Implementation Checklist

### Files to Modify
- [ ] `.claude/hooks/post_tool_use.py`
  - Add `LEARNING_SKILLS` dictionary
  - Add `generate_learning_prompt()` function
  - Add trigger checking (before MICRO_LESSONS)

- [ ] `01-memory/user-config.yaml`
  - Add flags: `learn_builds_offered`, `create_folders_offered`

- [ ] `00-system/core/nexus/templates/user-config.yaml`
  - Add same flags (for new users)

### Testing Plan
1. Fresh user test (all flags false)
2. Choice 1 test (load + execute)
3. Choice 2 test (skip now → ask again)
4. Choice 3 test (skip forever → never ask)
5. Multiple triggers test
6. Error handling test

---

## 🎨 Key Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Auto-Triggers | Only 2 | learn-builds = Gateway (explains all), prevents nesting |
| User Control | Ask 1/2/3 | Respects autonomy, no forced interruption |
| Injection Format | Prompt only | Small payload, Claude loads content if needed |
| Flag Setting | Claude sets | Hook only offers, Claude handles based on choice |
| Priority | Learning > Micro | Learning context more valuable than tips |

---

## 🔍 Critical Properties

**P1: Exactly-Once Execution**
For all learning skills, inject exactly once per user (first encounter only)

**P2: Content Completeness**
For any triggered skill, inject complete SKILL.md content (if user chooses 1)

**P3: Flag Persistence**
For any injection, flag set BEFORE hook exits (idempotent across restarts)

**P4: Backward Compatibility**
For all existing MICRO_LESSONS, maintain identical behavior

---

## 📊 State Diagram (Simplified)

```
NEVER OFFERED (Flag: False)
    ↓ Trigger detected
PROMPT SHOWN
    ↓ User responds
    ├─ Choice 1 → COMPLETED (Flag: True)
    ├─ Choice 2 → NEVER OFFERED (Flag: False) ← Ask again!
    └─ Choice 3 → DISMISSED (Flag: True)
```

---

## 🚨 Edge Cases

| Case | Handling |
|------|----------|
| Skill file missing | Graceful fallback (log + exit, no crash) |
| Multiple triggers | Priority system (first in dict wins) |
| User interrupts lesson | Flag not set yet → ask again next time |
| Corrupted config | Default to all False (offer all lessons) |

---

## 📁 Documentation Files

| File | Purpose |
|------|---------|
| [sequence-documentation.md](sequence-documentation.md) | Complete sequence flows + scenarios |
| [visual-flow.md](visual-flow.md) | Diagrams + state machines |
| [learning-skills-mapping.md](learning-skills-mapping.md) | Skill trigger mapping |
| [quick-reference.md](quick-reference.md) | This file (cheat sheet) |

Planning docs:
- [01-overview.md](../01-planning/01-overview.md) - Build purpose
- [02-discovery.md](../01-planning/02-discovery.md) - Requirements (EARS)
- [03-plan.md](../01-planning/03-plan.md) - Architecture + decisions
- [04-steps.md](../01-planning/04-steps.md) - Execution phases

---

## 🛠️ Code Snippets (Key Parts)

### LEARNING_SKILLS Structure
```python
LEARNING_SKILLS: Dict[str, Dict] = {
    'learn_builds_offered': {
        'triggers': [
            lambda tool, path: (
                tool == 'Read' and
                'plan-build/SKILL.md' in path
            ),
        ],
        'skill_path': '00-system/skills/learning/learn-builds/SKILL.md',
        'duration': '8-10 min',
        'prompt_template': '''🎯 FIRST TIME: BUILD PLANNING
[User choice 1/2/3 + handling instructions]'''
    },
}
```

### Hook Main Flow
```python
def main():
    # Extract tool info
    tool_name = os.environ.get('ANTHROPIC_TOOL_NAME')
    file_path = tool_input.get('file_path', '')

    # Load config
    encounters = get_first_encounters(config_path)

    # Check learning triggers (BEFORE micro lessons!)
    for skill_id, skill_data in LEARNING_SKILLS.items():
        if encounters.get(skill_id, False):
            continue  # Already offered

        for trigger_fn in skill_data['triggers']:
            if trigger_fn(tool_name, file_path):
                # MATCH! Inject prompt
                prompt = generate_learning_prompt(skill_data)
                output = {
                    "hookSpecificOutput": {
                        "hookEventName": "PostToolUse",
                        "additionalContext": prompt
                    }
                }
                print(json.dumps(output), flush=True)
                sys.exit(0)

    # Fallback to micro lessons...
```

### Prompt Template (Choice Handling)
```
🎯 FIRST TIME: BUILD PLANNING

Choose 1, 2, or 3.

HANDLE USER CHOICE:

Choice 1 - Load lesson:
  - Read: {skill_path}
  - Execute the full lesson
  - Continue with plan-build after

Choice 2 - Skip for now:
  - Do NOT modify config flags
  - Continue immediately
  - Next time: ask again

Choice 3 - Skip forever:
  - Edit: 01-memory/user-config.yaml
  - Set: {skill_id}: true
  - Continue immediately
  - Never ask again
```

---

## ✅ Success Metrics

| Metric | Target | Test |
|--------|--------|------|
| Auto-trigger accuracy | 100% | All trigger points tested |
| User choice handling | 100% | All 3 choices work |
| Flag persistence | 100% | Survives restart |
| No false triggers | 100% | Non-learning skills don't trigger |
| Backward compat | 100% | MICRO_LESSONS unchanged |

---

## 📞 Next Steps (Implementation)

1. **Phase 1: Hook Modification**
   - Code LEARNING_SKILLS dict
   - Code generate_learning_prompt()
   - Add trigger checking logic
   - Test with mock input

2. **Phase 2: Config Updates**
   - Add flags to user-config.yaml
   - Add flags to template
   - Verify backward compat

3. **Phase 3: Integration Testing**
   - Fresh user test
   - All 3 choices
   - Multiple triggers
   - Error scenarios

4. **Phase 4: Documentation**
   - Update README
   - Add troubleshooting
   - Document flag meanings

---

## 🎓 Learning Resources

**Read first**: [sequence-documentation.md](sequence-documentation.md)
- User journeys
- Hook perspective
- Claude perspective
- All scenarios

**Then**: [visual-flow.md](visual-flow.md)
- Flow diagrams
- State machines
- Error paths
- Timeline

**Reference**: [03-plan.md](../01-planning/03-plan.md)
- Full architecture
- Correctness properties
- All decisions + rationale

---

*Quick reference complete. Ready to code.*
