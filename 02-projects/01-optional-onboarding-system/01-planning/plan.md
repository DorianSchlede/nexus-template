# Optional Onboarding System - Plan

**Last Updated**: 2025-12-10
**Version**: 2.0 (aligned with requirements.md v2.0)

---

## Approach

Three-phase implementation combining B5 (Smart Defaults), B3 (Onboarding-as-Skills), and Progressive Disclosure:

**Phase 1: Smart Defaults (B5)**
1. Add smart default templates to nexus-loader.py
2. Implement template detection (`smart_default: true` flag)
3. Add `create_smart_defaults()` function
4. Modify state detection to recognize `first_time_with_defaults`
5. Auto-create files when memory folder is empty

**Phase 2: Skills Conversion (B3)**
1. Create **5** new skill directories (using create-skill workflow)
2. Write SKILL.md for each with YAML v2.0 format (only name + description)
3. Extract reference files from teaching content
4. Update orchestrator to suggest skills instead of forcing projects
5. Archive original onboarding projects

**Phase 3: Progressive Disclosure**
1. Add learning_tracker schema to user-config.yaml
2. Implement context-aware skill suggestions in orchestrator
3. Define update triggers for each component

---

## Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Template detection method | YAML `smart_default: true` flag | Machine-parseable, explicit, easy to remove when personalized |
| Default language | English | Most common, user can change in first interaction |
| Onboarding status | `skipped` instead of tracking | Simpler state machine, user opted to skip by working immediately |
| Skills independence | Soft dependencies only | Each skill works alone but offers better experience with prerequisites |
| Close-session teaching | Keep in all skills | Critical habit, must be reinforced regardless of entry point |
| Original projects | Archive (don't delete) | Preserves rollback capability, reference for content |
| Number of skills | 5 (added learn-projects) | Projects are fundamental - deserve dedicated teaching |
| Skill creation method | Use create-skill workflow | Consistency, leverages init_skill.py tooling |
| YAML format | v2.0 (name + description only) | Minimal metadata, progressive disclosure |
| Menu header | Modern 3-line horizontal bar | Professional, less screen space, modern CLI feel |
| Learning tracker | user-config.yaml extension | Single source of truth for user state |

---

## Resources Needed

**Tools/Access**:
- Python 3.x (for nexus-loader.py modifications)
- File system access (create skill directories)

**Information/Data**:
- Onboarding project content (overview.md, steps.md, design.md)
- Teaching scripts (02-resources/teaching-scripts.md)
- Existing skill patterns (create-skill, create-project)

---

## Dependencies & Links

**Files Impacted**:
- `00-system/core/nexus-loader.py` - Add smart defaults, modify state detection
- `00-system/core/orchestrator.md` - Update menu display, remove forced onboarding
- `00-system/core/init-memory.py` - Reference for template patterns
- `01-memory/user-config.yaml` - Simplify onboarding tracking

**New Files to Create** (5 skills via create-skill workflow):
- `00-system/skills/setup-goals/SKILL.md`
- `00-system/skills/setup-goals/references/*`
- `00-system/skills/setup-workspace/SKILL.md`
- `00-system/skills/setup-workspace/references/*`
- `00-system/skills/learn-skills/SKILL.md`
- `00-system/skills/learn-skills/references/*`
- `00-system/skills/learn-projects/SKILL.md` **(NEW)**
- `00-system/skills/learn-projects/references/*` **(NEW)**
- `00-system/skills/learn-nexus/SKILL.md`
- `00-system/skills/learn-nexus/references/*`

**Source Content**:
- `02-projects/00-onboarding/00-define-goals/` → setup-goals skill
- `02-projects/00-onboarding/01-first-project/` → setup-workspace skill (project structure)
- `02-projects/00-onboarding/01-first-project/` → learn-projects skill (project concepts) **(NEW)**
- `02-projects/00-onboarding/02-first-skill/` → learn-skills skill
- `02-projects/00-onboarding/03-system-mastery/` → learn-nexus skill

**Skills/Workflows Used**:
- `create-project` skill - Used by setup-workspace
- `create-skill` skill - Used by learn-skills
- `close-session` skill - Called at end of each onboarding skill

---

## State Machine Design

**Current States**:
```
first_time_setup → Forces Project 00
onboarding_in_progress → Forces next project
operational → Shows menu
```

**New States**:
```
first_time_with_defaults → Shows menu + suggests onboarding
onboarding_in_progress → (Optional) continues if user started
operational → Shows menu
```

**State Detection Flow**:
```python
if not files_exist['goals']:
    create_smart_defaults()
    # Refresh file checks

if is_template_file(goals.md):
    state = 'first_time_with_defaults'
    action = 'display_menu'
    suggest_onboarding = True
elif incomplete_onboarding_projects:
    state = 'onboarding_in_progress'
    action = 'load_and_execute_project'  # Only if user started
else:
    state = 'operational'
    action = 'display_menu'
```

---

## Open Questions

- [x] How to detect "filled" vs "template" state? → `smart_default: true` flag
- [x] Should skills be independent? → Yes, with soft dependencies
- [x] What about backward compatibility? → Old `[TODO:` pattern also detected
- [x] Should we keep onboarding progress tracking in user-config? → Use learning_tracker schema
- [x] How aggressive should contextual prompts be? → Configurable via suggestion_preference
- [x] How do we update learning_tracker? → Defined in REQ-PD-004 (WHO/WHEN/HOW)
- [x] Who creates the skills? → Use create-skill workflow (init_skill.py)

---

## Mental Models Applied

**First Principles**:
- What's the minimum viable first experience? → Show menu, let user work
- Why do we force onboarding? → Historical, not technically required
- What value does onboarding provide? → Learning, personalization (both optional)

**Pre-Mortem**:
- Risk: Users skip and get confused later → Mitigate with contextual help triggers
- Risk: Breaking existing installations → Backward compatibility checks
- Risk: Losing pedagogical value → Preserve content in skills

**Stakeholder Mapping**:
- New users: Want guidance → Skills available on demand
- Power users: Want speed → Smart defaults, immediate work
- System maintainers: Want clean code → Simpler state machine

---

## Template Designs

### Smart Default goals.md
```markdown
---
smart_default: true
created: {date}
---
# Your Goals

> Smart defaults active. Personalize through onboarding or edit directly.

## Current Role
[Your role]

## Short-Term Goal (3 months)
[Your goal]

## Long-Term Vision (1-3 years)
[Your vision]

**Tip**: Say "setup goals" for guided personalization.
```

### Smart Default user-config.yaml
```yaml
---
smart_default: true
user_preferences:
  language: "English"
  timezone: ""
  date_format: "YYYY-MM-DD"
  system:
    python_cmd: "{auto-detected}"
onboarding:
  status: "skipped"
created: {date}
---
```

---

## The 5 Onboarding Skills

| Skill | Triggers | Duration | Source | Teaches |
|-------|----------|----------|--------|---------|
| setup-goals | "setup goals", "define goals", "personalize nexus" | 8-10 min | Project 00 | Goal-setting, CAVE pedagogy |
| setup-workspace | "setup workspace", "configure workspace" | 10-14 min | Project 01 (structure) | Folder structure, workspace-map.md |
| learn-projects | "learn projects", "understand projects", "project tutorial" | 8-10 min | Project 01 (concepts) | Projects vs Skills, create-project |
| learn-skills | "learn skills", "skill tutorial", "create skill help" | 12-15 min | Project 02 | Skill creation, automation patterns |
| learn-nexus | "learn nexus", "system mastery", "AI collaboration" | 16-18 min | Project 03 | Pitfalls, AI patterns, expert collab |

**Skill YAML v2.0 Format** (only name + description):
```yaml
---
name: skill-name-hyphen-case
description: Comprehensive description with trigger keywords naturally embedded. Load when user says "trigger phrase", "alternative phrase". Include what it does and when to use it.
---
```

---

## Learning Tracker Schema

**Location**: `01-memory/user-config.yaml`

```yaml
learning_tracker:
  completed:
    setup-goals: false
    setup-workspace: false
    learn-skills: false
    learn-projects: false
    learn-nexus: false
  dismissed:
    setup-goals: 0
    setup-workspace: 0
    learn-skills: 0
    learn-projects: 0
    learn-nexus: 0
  last_suggested:
    setup-goals: null
    setup-workspace: null
    learn-skills: null
    learn-projects: null
    learn-nexus: null
  suggestion_preference: "normal"  # off, minimal, normal, proactive
  session_count: 0
  workflow_patterns: {}
  common_mistakes: {}
```

**WHO updates WHAT**:
| Component | Updates | When |
|-----------|---------|------|
| nexus-loader.py | session_count | On --startup |
| Each onboarding skill | completed[skill] | At skill completion |
| Orchestrator/Menu | dismissed, last_suggested | When user declines suggestion |
| close-session skill | workflow_patterns, common_mistakes | During session close |

---

## Modern Menu Header Design

**Replace ASCII art banner** with clean 3-line design:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 NEXUS • Self-Evolving Work Organization
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Rationale**:
- Professional appearance
- Reduced screen space (3 lines vs 8 lines)
- Better compatibility with narrow terminals
- Modern CLI aesthetic (matches popular tools)

---

*See requirements.md for complete specification and steps.md for execution tasks*
