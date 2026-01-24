# Contextual Learning Injection - Komplette Sequenz

**Build**: 03-contextual-learning-injection
**Purpose**: Automatisches Onboarding via Hook-basiertes Learning Injection
**Erstellt**: 2026-01-23

---

## Executive Summary

**Problem**: Neue User müssen manuell "learn builds" sagen - sie wissen nicht, dass sie das tun sollten.

**Lösung**: Hook erkennt "erste Begegnung" mit Build-System → bietet User sofort Learning Lesson an → User wählt (laden/skip now/skip forever).

**Innovation**: "Teach Through Doing" - User lernt WÄHREND er sein erstes Build plant, nicht vorher.

---

## System-Architektur Overview

```
User Action
    ↓
Nexus Routing → Load Skill
    ↓
Claude: Read tool → SKILL.md
    ↓
PostToolUse Hook (Python)
    ↓
┌─────────────────────────────────────┐
│ 1. Check Learning Triggers          │
│ 2. Check if already offered         │
│ 3. Generate user-choice prompt      │
│ 4. Inject via additionalContext     │
└─────────────────────────────────────┘
    ↓
Claude receives prompt
    ↓
Claude asks User: 1/2/3?
    ↓
User chooses → Claude handles
```

---

## Sequenz 1: Erster Build (learn-builds Auto-Trigger)

### User-Perspektive

```
User: "Ich brauche ein Rezeptbuch mit 100 Rezepten"

Claude (via Nexus Routing): [Erkennt: Build-Bedarf]
        → Lädt plan-build Skill
        → Read: 00-system/skills/builds/plan-build/SKILL.md

[Hook läuft im Hintergrund]

Claude: 🎯 FIRST TIME: BUILD PLANNING

        Das ist dein erstes Build. Möchtest du:
        1) Die 8-10min "Learn Builds" Lektion jetzt laden
           (erklärt: Builds vs Skills, Build-Struktur, Lifecycle)
        2) Jetzt überspringen (ich frage nächstes Mal nochmal)
        3) Für immer überspringen (nicht mehr fragen)

User: "1"

Claude: [Lädt 00-system/skills/learning/learn-builds/SKILL.md]
        [Führt komplette Learning Lesson aus]
        [Setzt user-config.yaml: learn_builds_offered: true]

        [Nach Lesson:]
        Jetzt zurück zu deinem Rezeptbuch-Build...
```

### Hook-Perspektive (post_tool_use.py)

```python
# Tool detected: Read
# Path: 00-system/skills/builds/plan-build/SKILL.md

def main():
    tool_name = os.environ.get('ANTHROPIC_TOOL_NAME')
    tool_input = json.loads(os.environ.get('ANTHROPIC_TOOL_INPUT', '{}'))
    file_path = tool_input.get('file_path', '')

    # --- STEP 1: Check Learning Skills (Priority) ---
    config_path = Path('01-memory/user-config.yaml')
    encounters = get_first_encounters(config_path)

    for skill_id, skill_data in LEARNING_SKILLS.items():
        # Check flag
        if encounters.get(skill_id, False):
            continue  # Already offered

        # Check triggers
        for trigger_fn in skill_data['triggers']:
            if trigger_fn(tool_name, file_path):
                # MATCH: plan-build detected!

                # Generate prompt
                prompt = generate_learning_prompt(skill_data)

                # Inject
                output = {
                    "hookSpecificOutput": {
                        "hookEventName": "PostToolUse",
                        "additionalContext": prompt
                    }
                }
                print(json.dumps(output), flush=True)
                sys.exit(0)

                # NOTE: Flag NOT set here!
                # Claude sets it if user chooses "3"

    # --- STEP 2: Fallback to Micro Lessons ---
    # (existing code continues...)
```

### Claude-Perspektive (additionalContext Injection)

```
[Claude führt: Read tool → plan-build/SKILL.md aus]

[Hook injiziert sofort danach:]

additionalContext = """
🎯 FIRST TIME: BUILD PLANNING

This is your first time planning a build. Would you like me to:
1) Load the 8-10 min "Learn Builds" lesson now
   (covers: Builds vs Skills, Decision Framework, Build Structure)
2) Skip for now (I'll ask again next time)
3) Skip forever (don't ask again)

Choose 1, 2, or 3.

HANDLE USER CHOICE:

Choice 1 - Load lesson:
  - Read: 00-system/skills/learning/learn-builds/SKILL.md
  - Execute the full lesson
  - Continue with plan-build after lesson completes

Choice 2 - Skip for now:
  - Do NOT modify user-config.yaml flags
  - Continue with plan-build immediately
  - Next time plan-build triggers, ask again

Choice 3 - Skip forever:
  - Edit 01-memory/user-config.yaml
  - Set first_encounters.learn_builds_offered: true
  - Continue with plan-build immediately
  - Never ask again
"""

[Claude sieht diesen Prompt zusätzlich zu seiner aktuellen Aufgabe]
[Claude zeigt User die Frage]
[Claude handled User-Wahl gemäß Anweisungen]
```

---

## Sequenz 2: Workspace Setup (create-folders Auto-Trigger)

### User-Perspektive

```
User: "Erstelle mir einen Ordner für Rezepte"

Claude: [Versteht: Workspace Organization]
        [Write tool → 04-workspace/rezepte/...]

[Hook läuft]

Claude: 🎯 FIRST TIME: WORKSPACE USAGE

        Das ist dein erstes Mal im Workspace. Möchtest du:
        1) Die 5min "Create Folders" Lektion jetzt laden
        2) Jetzt überspringen
        3) Für immer überspringen

User: "2"  (skip now)

Claude: Kein Problem! Ich erstelle den Ordner...
        [Setzt KEIN Flag - User wird nächstes Mal wieder gefragt]
```

### Hook-Trigger

```python
'create_folders_offered': {
    'triggers': [
        lambda tool, path: (
            tool == 'Write' and
            '04-workspace/' in path
        ),
    ],
    'skill_path': '00-system/skills/learning/create-folders/SKILL.md',
    'duration': '5 min',
    # ...
}
```

---

## Sequenz 3: Skip Forever Mechanismus

### User-Perspektive

```
User: "Erstelle einen Skill für wöchentliche Reports"

Claude: [Routing → create-skill]
        [Read: create-skill/SKILL.md]

[Hook würde learn-skills triggern, ABER...]

Claude: 🎯 FIRST TIME: SKILL CREATION
        [Frage 1/2/3]

User: "3"  (skip forever)

Claude: [Edit: 01-memory/user-config.yaml]
        [Setzt: learn_skills_offered: true]

        Verstanden! Ich erstelle den Skill ohne Lesson...
```

### Flag-Update (Claude macht das!)

```yaml
# 01-memory/user-config.yaml

first_encounters:
  memory_updated: true           # existing
  close_session_used: false      # existing
  learn_builds_offered: true     # NEW - User completed lesson
  learn_skills_offered: true     # NEW - User chose "skip forever"
  create_folders_offered: false  # NEW - not offered yet
```

**Kritisch**: Hook setzt Flag NICHT automatisch! Nur Claude setzt Flag wenn User "3" wählt.

---

## Daten-Strukturen

### LEARNING_SKILLS Dictionary (post_tool_use.py)

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
        'topics': 'Builds vs Skills, Decision Framework, Build Structure',
        'prompt_template': '''🎯 FIRST TIME: BUILD PLANNING
[... full prompt ...]'''
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
        'topics': 'Workspace Structure Setup, Organization',
        'prompt_template': '''🎯 FIRST TIME: WORKSPACE USAGE
[... full prompt ...]'''
    },
}
```

**Nur 2 Auto-Triggers!** Warum?

- `learn-builds`: Gateway Lesson - erklärt ALLES (auch Skills, Integrations)
- `create-folders`: Workspace Setup - separater Kontext

**Keine Auto-Triggers für**:
- `learn-skills`: Bereits in learn-builds erklärt
- `learn-integrations`: Bereits in learn-builds erklärt
- `learn-nexus`: Tiefe System-Mastery - User sagt manuell "learn nexus"

---

## Interaktions-Matrix

| User Action | Trigger | Prompt | Flag Setting |
|-------------|---------|--------|--------------|
| "create build" | plan-build geladen | learn-builds prompt (1/2/3) | Claude setzt bei "3" |
| User wählt "1" | - | Claude lädt + ausführt Lesson | Claude setzt nach Completion |
| User wählt "2" | - | Claude macht weiter | KEIN Flag (frag nächstes Mal) |
| User wählt "3" | - | Claude macht weiter | Claude setzt Flag = true |
| Nächstes "create build" | plan-build geladen | Flag = true → KEIN Prompt | - |
| First Write workspace | 04-workspace/ detected | create-folders prompt | Claude setzt bei "3" |

---

## Control Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│ User: "Ich brauche ein Rezeptbuch"                          │
└────────────────┬────────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────────────────┐
│ Nexus Routing (orchestrator.md)                             │
│   - Erkennt: Build-Bedarf                                    │
│   - Entscheidung: Load plan-build                            │
└────────────────┬────────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────────────────┐
│ Claude: Read tool                                            │
│   file_path: 00-system/skills/builds/plan-build/SKILL.md    │
└────────────────┬────────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────────────────┐
│ PostToolUse Hook (.claude/hooks/post_tool_use.py)           │
│                                                              │
│ STEP 1: Extract tool info                                   │
│   - tool_name = "Read"                                       │
│   - file_path = "...plan-build/SKILL.md"                    │
│                                                              │
│ STEP 2: Load user flags                                     │
│   - encounters = get_first_encounters()                      │
│   - learn_builds_offered = False                             │
│                                                              │
│ STEP 3: Check learning triggers                             │
│   - FOR each skill in LEARNING_SKILLS:                       │
│     - IF flag == False:                                      │
│       - FOR each trigger function:                           │
│         - IF trigger_fn(tool_name, file_path):              │
│           ✓ MATCH!                                           │
│                                                              │
│ STEP 4: Generate prompt                                     │
│   - prompt = generate_learning_prompt(skill_data)            │
│   - Contains: 1/2/3 choices + handling instructions         │
│                                                              │
│ STEP 5: Inject                                              │
│   - Output JSON to stdout                                    │
│   - hookSpecificOutput.additionalContext = prompt           │
│   - Exit hook                                                │
└────────────────┬────────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────────────────┐
│ Claude Code Extension                                        │
│   - Receives hook output                                     │
│   - Parses additionalContext                                 │
│   - Appends to Claude's context window                       │
└────────────────┬────────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────────────────┐
│ Claude (with injected context)                               │
│   - Sieht: Original task (plan build)                        │
│   - Sieht: Additional prompt (1/2/3 choice)                  │
│   - Zeigt User die Frage                                     │
└────────────────┬────────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────────────────┐
│ User: "1"                                                    │
└────────────────┬────────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────────────────┐
│ Claude: Handles Choice 1                                     │
│   - Read: 00-system/skills/learning/learn-builds/SKILL.md   │
│   - Execute full lesson                                      │
│   - Edit: 01-memory/user-config.yaml                         │
│   - Set: learn_builds_offered: true                          │
│   - Continue with plan-build                                 │
└─────────────────────────────────────────────────────────────┘
```

---

## Edge Cases & Handling

### Case 1: Skill-Datei fehlt

```python
try:
    prompt = generate_learning_prompt(skill_data)
    # Lädt Datei intern
except FileNotFoundError:
    # Graceful fallback
    log_error(f"Learning skill not found: {skill_path}")
    sys.exit(0)  # Kein Crash, einfach Skip
```

### Case 2: Multiple Triggers gleichzeitig

**Szenario**: User sagt "create build" UND es ist erstes Write in workspace.

**Lösung**: Priority System in Loop-Reihenfolge
```python
# Higher priority first in dict
LEARNING_SKILLS = {
    'learn_builds_offered': {...},      # Checked first
    'create_folders_offered': {...},    # Checked second
}
```

Nur ERSTER Match wird injiziert.

### Case 3: User unterbricht Lesson

**Szenario**: User wählt "1", bricht dann Lesson ab.

**Handling**:
- Flag wurde noch nicht gesetzt (Claude setzt erst nach Completion)
- Nächstes Mal plan-build → User wird wieder gefragt
- User kann dann "2" oder "3" wählen

### Case 4: Corrupted user-config.yaml

```python
try:
    encounters = get_first_encounters(config_path)
except yaml.YAMLError:
    # Fallback: Treat as all False (offer all lessons)
    encounters = {}
```

---

## Testing Scenarios

### Manual Test 1: Fresh User

```bash
# Setup
1. Delete 01-memory/user-config.yaml
2. Start fresh session
3. User: "create build for recipes"

# Expected
- Hook triggers on plan-build load
- Claude shows 1/2/3 prompt
- User chooses "1"
- Claude loads learn-builds
- Claude executes lesson
- Claude sets flag
- Claude continues with plan-build

# Verify
- cat 01-memory/user-config.yaml | grep "learn_builds_offered: true"
```

### Manual Test 2: Skip Now vs Skip Forever

```bash
# Test Skip Now
1. Set learn_builds_offered: false
2. User: "create build"
3. Claude asks 1/2/3
4. User: "2" (skip now)
5. Check flag → should be FALSE
6. User: "create build" (again)
7. Claude asks again → ✓

# Test Skip Forever
1. Set learn_builds_offered: false
2. User: "create build"
3. Claude asks 1/2/3
4. User: "3" (skip forever)
5. Check flag → should be TRUE
6. User: "create build" (again)
7. Claude does NOT ask → ✓
```

### Manual Test 3: Multiple Skills

```bash
# Test beide Auto-Triggers
1. Reset all flags to false
2. User: "create build"
   → learn-builds offered
3. User: "1" (complete lesson)
4. User: "create folder in workspace"
   → create-folders offered
5. User: "3" (skip forever)
6. Verify both flags set correctly
```

---

## Implementation Checklist

### Phase 1: Hook Modification
- [ ] Add LEARNING_SKILLS dictionary to post_tool_use.py
- [ ] Add generate_learning_prompt() function
- [ ] Add trigger checking logic (before MICRO_LESSONS)
- [ ] Test hook with mock tool input

### Phase 2: Config Updates
- [ ] Add flags to 01-memory/user-config.yaml template
- [ ] Add flags to 00-system/core/nexus/templates/user-config.yaml
- [ ] Verify backward compatibility (existing flags unaffected)

### Phase 3: Integration Testing
- [ ] Fresh user test (all flags false)
- [ ] Skip now test (flag stays false)
- [ ] Skip forever test (flag set true)
- [ ] Multiple triggers test
- [ ] Error handling test (missing file)

### Phase 4: Documentation
- [ ] Update README with new onboarding flow
- [ ] Add troubleshooting section
- [ ] Document flag meanings in user-config comments

---

## Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Auto-trigger accuracy | 100% | Manual testing with all trigger points |
| User choice handling | 100% | All 3 choices (1/2/3) work correctly |
| Flag persistence | 100% | Flags survive session restart |
| No false triggers | 100% | Non-learning skills don't trigger prompts |
| Backward compat | 100% | Existing MICRO_LESSONS still work |

---

## Risks Mitigation

| Risk | Mitigation |
|------|------------|
| Token limit exceeded | Prompts are small (~50 lines), full content only loaded on user "1" |
| User ignores prompt | They chose "2" → ask again next time |
| Hook crashes | Try-except all file operations, graceful exit |
| Claude misinterprets | Clear handling instructions in prompt template |

---

## Next Steps

1. **Implement Phase 1**: Modify post_tool_use.py
2. **Test locally**: Mock tool inputs
3. **Update configs**: Add flags
4. **Real-world test**: Fresh user flow
5. **Deploy**: Commit to repo

---

*Sequence documented. Ready for implementation.*
