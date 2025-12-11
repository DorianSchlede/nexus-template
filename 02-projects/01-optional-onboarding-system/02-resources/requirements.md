# Optional Onboarding System - Requirements Document

**Version**: 2.0
**Created**: 2025-12-10
**Last Updated**: 2025-12-10
**Status**: COMPLETE - Ready for Implementation

---

## 1. Executive Summary

### 1.1 Problem Statement

The current Nexus onboarding system **forces** new users through a 4-project sequence (35-50 minutes) before they can do ANY work. This creates:

- **Friction**: Power users who know what they want can't start immediately
- **Drop-off**: Users abandon Nexus before experiencing its value
- **Rigidity**: No path for users who prefer learning-by-doing
- **Context waste**: Forces immediate context loading when user may not need it

### 1.2 Solution Overview

Transform the onboarding from forced projects to an optional, skill-based system:

| Component | Description |
|-----------|-------------|
| **B5: Smart Defaults** | Auto-create minimal template files on first run |
| **B3: Onboarding-as-Skills** | Convert 4 forced projects to **5** optional skills |
| **Progressive Disclosure** | Contextually suggest onboarding skills when beneficial |
| **Modern Menu Design** | Replace ASCII art banner with clean, professional header |

### 1.3 Success Criteria Summary

- Fresh install shows menu in <2 seconds (not forced onboarding)
- System works immediately with zero personalization
- Onboarding content preserved and accessible on-demand
- Existing installations continue to work unchanged
- All skills created using `create-skill` workflow

---

## 2. Functional Requirements

### 2.1 B5: Smart Defaults System

#### REQ-B5-001: Automatic File Creation
**Priority**: CRITICAL

When `01-memory/goals.md` does not exist, the system MUST automatically create:
- `01-memory/goals.md` (with `smart_default: true` flag)
- `01-memory/user-config.yaml` (with defaults + learning_tracker)
- `01-memory/memory-map.md` (static documentation)
- `01-memory/core-learnings.md` (empty starter)
- `01-memory/session-reports/` directory

**Implementation Location**: `nexus-loader.py` lines 34-60 (after MANDATORY_MAPS)

**Acceptance Criteria**:
- [ ] Files created on first `--startup` run
- [ ] No user interaction required
- [ ] Operation completes in <500ms
- [ ] Idempotent (safe to run multiple times)

#### REQ-B5-002: Template Detection
**Priority**: CRITICAL

The system MUST distinguish between:
- **Template files**: Created by smart defaults, not personalized
- **Personalized files**: User has filled in real content

**Detection Methods**:
1. Primary: YAML frontmatter `smart_default: true` flag
2. Fallback: Pattern matching for `[TODO: Set in onboarding` text
3. Edge case: Empty content detection

**Function Signatures**:
```python
def is_template_file(file_path: Path, content: Optional[str] = None) -> bool
def _is_template_yaml(file_path: Path, content: str) -> bool
def _is_template_markdown(content: str) -> bool
```

**Acceptance Criteria**:
- [ ] `is_template_file(path)` returns `True` for smart default files
- [ ] `is_template_file(path)` returns `False` for personalized files
- [ ] Backward compatible with old TODO pattern detection
- [ ] Handles missing files gracefully

#### REQ-B5-003: Smart Default Content
**Priority**: HIGH

Template files MUST include:
- YAML frontmatter with `smart_default: true` and creation date
- Placeholder content that clearly indicates "not yet personalized"
- Helpful tip pointing to relevant onboarding skill

**goals.md Template**:
```markdown
---
smart_default: true
created: {date}
---
# Your Goals

> Smart defaults active. Personalize anytime or edit directly.

## Current Role
[Your role]

## Short-Term Goal (3 months)
[Your goal]

## Long-Term Vision (1-3 years)
[Your vision]

💡 Say "setup goals" for guided personalization (9 min).
```

**user-config.yaml Template**:
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
  suggestion_preference: "normal"
  session_count: 0

created: {date}
---
```

**Acceptance Criteria**:
- [ ] All templates include `smart_default: true`
- [ ] Placeholder text is clear and concise
- [ ] Skill trigger hints are accurate
- [ ] Python command auto-detected correctly
- [ ] Learning tracker schema included

#### REQ-B5-004: New System State
**Priority**: CRITICAL

Add new state `first_time_with_defaults` between `first_time_setup` and `operational`:

**State Detection Logic** (nexus-loader.py lines 306-389):
```python
if not files_exist['goals']:
    create_smart_defaults(base_path)
    result['system_state'] = 'first_time_with_defaults'
elif is_template_file(optional_files['goals']):
    result['system_state'] = 'first_time_with_defaults'
else:
    # Continue to existing onboarding/operational logic
```

**State Behavior**:
- Action: `display_menu` (NOT `load_and_execute_project`)
- Flag: `suggest_onboarding: True` in instructions
- Menu: Shows "Quick Start Mode" notice

**Acceptance Criteria**:
- [ ] State correctly detected after smart default creation
- [ ] Menu displayed instead of forced project
- [ ] `suggest_onboarding` flag set in JSON output
- [ ] User can work immediately after state detection

---

### 2.2 B3: Onboarding-as-Skills System

#### REQ-B3-001: Skill Creation Method
**Priority**: CRITICAL

**All 5 onboarding skills MUST be created using the `create-skill` skill workflow**:

1. Run `scripts/init_skill.py <skill-name> --path 00-system/skills`
2. Follow 8-step workflow from create-skill SKILL.md
3. Validate with `scripts/quick_validate.py`
4. Package with `scripts/package_skill.py` (optional)

**YAML Format** (v2.0 - only 2 fields allowed):
```yaml
---
name: skill-name-hyphen-case
description: Comprehensive description with trigger keywords naturally embedded. Load when user says "trigger phrase", "alternative phrase". Include what it does and when to use it.
---
```

**Acceptance Criteria**:
- [ ] All skills created via init_skill.py
- [ ] YAML has ONLY `name` and `description` fields
- [ ] Name is hyphen-case (no underscores, camelCase)
- [ ] Description includes triggers naturally
- [ ] Validates with quick_validate.py

#### REQ-B3-002: Skill Directory Structure
**Priority**: HIGH

Create **5** new skills in `00-system/skills/`:

| Skill Name | Directory | Duration |
|------------|-----------|----------|
| setup-goals | `00-system/skills/setup-goals/` | 9-12 min |
| setup-workspace | `00-system/skills/setup-workspace/` | 12-15 min |
| learn-skills | `00-system/skills/learn-skills/` | 12-15 min |
| **learn-projects** | `00-system/skills/learn-projects/` | 10-12 min |
| learn-nexus | `00-system/skills/learn-nexus/` | 15-18 min |

Each skill directory structure:
```
00-system/skills/{skill-name}/
├── SKILL.md (YAML frontmatter + workflow, <500 lines)
└── references/ (teaching content, loaded on-demand)
    ├── workflow.md (if complex multi-step)
    ├── examples.md (domain-specific examples)
    └── {topic}.md (additional reference material)
```

**Acceptance Criteria**:
- [ ] All 5 directories created via init_skill.py
- [ ] SKILL.md files under 500 lines
- [ ] References extracted from teaching-scripts.md
- [ ] Skills load correctly via `--skill {name}`

#### REQ-B3-003: Skill Triggers (Embedded in Description)
**Priority**: HIGH

**Triggers are NOT a separate YAML field** - they are embedded naturally in the description:

| Skill | Description Pattern |
|-------|---------------------|
| setup-goals | "Load when user says 'setup goals', 'define goals', 'set my goals', or 'initialize memory'. Guide through goal definition and memory file creation." |
| setup-workspace | "Load when user mentions 'setup workspace', 'create workspace', 'first project', or 'organize folders'. Create folder structure and workspace-map.md." |
| learn-skills | "Load when user says 'learn skills', 'first skill', 'skill tutorial', or 'how to create skills'. Teach workflow identification and skill creation." |
| learn-projects | "Load when user mentions 'learn projects', 'project tutorial', 'how projects work', or 'project vs skill'. Teach project creation and management." |
| learn-nexus | "Load when user says 'learn nexus', 'system mastery', 'AI collaboration', or 'nexus tutorial'. Teach AI patterns and expert collaboration." |

**Acceptance Criteria**:
- [ ] Triggers work via natural language matching
- [ ] Triggers work case-insensitively
- [ ] No conflicts with existing skills
- [ ] Description test: "If user says X, would Claude pick this skill?"

#### REQ-B3-004: Skill Independence (Soft Dependencies)
**Priority**: HIGH

Skills MUST work independently with **soft dependencies only**:

- Each skill provides value alone
- Skills may SUGGEST other skills but never REQUIRE them
- Prerequisites checked and offered, not enforced

**Soft Prerequisite Pattern**:
```markdown
## Prerequisites Check

Before starting, check if dependencies are met:

1. **Check goals.md**:
   - If `is_template_file(goals.md)`:
     Display: "💡 I notice your goals aren't set yet. Would you like to:
     1. Set up goals first (recommended, 9 min)
     2. Continue directly to [this skill]"
   - If personalized: Continue directly

2. **User chooses**: Always allow proceeding without prerequisite
```

**Acceptance Criteria**:
- [ ] Each skill executable without completing others
- [ ] Soft prerequisite checks in SKILL.md
- [ ] User can always proceed or redirect
- [ ] No blocking dependencies

#### REQ-B3-005: Pedagogical Preservation
**Priority**: HIGH

All onboarding content MUST be preserved from source projects:

| Source Project | Target Skill | Key Content |
|----------------|--------------|-------------|
| 00-define-goals | setup-goals | Goal elicitation, AI suggestions, memory init |
| 01-first-project | setup-workspace | Projects vs Skills framework, workspace design |
| 02-first-skill | learn-skills | Workflow identification, 3-criteria evaluation |
| N/A (new) | learn-projects | Project creation, planning, execution |
| 03-system-mastery | learn-nexus | AI patterns (19% False Progress), collaboration |

**Must Preserve**:
- CAVE Framework (Concrete-Action-Value-Explanation) ordering
- Close-session habit teaching (in ALL skills - Step 8)
- Hands-on exercises with user's actual content
- AI behavioral pattern warnings with research citations
- Vocabulary budgeting (4-5 terms per skill max)

**Reference Files to Extract**:
- `teaching-scripts.md` → Domain examples, discovery questions
- `steps.md` from each project → Task breakdowns
- `design.md` from each project → CAVE implementation guides

**Acceptance Criteria**:
- [ ] All CAVE patterns retained
- [ ] Close-session as mandatory final step
- [ ] Learning exercises preserved
- [ ] Research citations maintained (19%, 21%, 16%)
- [ ] Vocabulary limits documented

#### REQ-B3-006: Skill Workflow Structure
**Priority**: HIGH

Each skill MUST follow the standard workflow pattern:

```markdown
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ CRITICAL EXECUTION REQUIREMENTS ⚠️

MANDATORY STEPS (DO NOT SKIP):
1. ✅ Initialize TodoWrite with all steps
2. ✅ Check soft prerequisites
3. ✅ [Skill-specific steps]
...
8. ✅ Close session (ALWAYS)

ANTI-PATTERN (DO NOT DO THIS):
❌ Skip prerequisite check
❌ Skip close-session
❌ Complete in single response
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Workflow

### Step 1: Initialize TodoWrite
[Create task tracking before starting...]

### Step 2: Prerequisites Check
[Soft dependency check with user choice...]

### Step 3-7: [Skill-Specific Work]
[Main teaching content...]

### Step 8: Close Session (MANDATORY)
```bash
python 00-system/core/nexus-loader.py --skill close-session
```
Saves progress, updates learning tracker, preserves context.
```

**Acceptance Criteria**:
- [ ] All skills have TodoWrite as Step 1
- [ ] All skills have close-session as final step
- [ ] Anti-patterns documented
- [ ] User display blocks use consistent format

---

### 2.3 Progressive Disclosure System

#### REQ-PD-001: Contextual Trigger System
**Priority**: MEDIUM

System MUST suggest relevant skills at key moments:

**State-Based Triggers** (High Priority):
| Situation | Suggested Skill | Detection |
|-----------|-----------------|-----------|
| First run with defaults | setup-goals | `system_state == 'first_time_with_defaults'` |
| Creating project without goals | setup-goals | `is_template_file(goals.md)` AND "create project" |
| No workspace folder | setup-workspace | `!exists(04-workspace/)` AND user starts work |
| Skill creation attempt | learn-skills | User mentions "create skill" without prior skill |
| Project confusion | learn-projects | User asks "project vs skill" or similar |

**Pattern-Based Triggers** (Medium Priority):
| Pattern | Suggested Skill | Detection |
|---------|-----------------|-----------|
| Workflow repetition | learn-skills | Same 3+ step pattern detected 2x |
| Project/Skill confusion | learn-projects | User creates project for repeatable work |
| AI confusion | learn-nexus | User asks "how does X work" >2 times |

**Time-Based Triggers** (Lower Priority):
| Timing | Suggested Skill | Detection |
|--------|-----------------|-----------|
| 7+ days since last session | Any incomplete | `days_since_last_session > 7` |
| 5+ sessions without goals | setup-goals | `session_count >= 5` AND `is_template_file(goals.md)` |

**Acceptance Criteria**:
- [ ] State-based triggers fire correctly
- [ ] Pattern-based triggers detect repetition
- [ ] Suggestions are non-blocking
- [ ] User can dismiss and continue

#### REQ-PD-002: Suggestion Format
**Priority**: MEDIUM

Contextual suggestions MUST be:
- **Non-intrusive**: Single line, integrated with content
- **Dismissable**: User can ignore and continue
- **Helpful**: Include benefit and time estimate

**Suggestion Formats**:
```
# Soft Suggestion (inline)
💡 Tip: Your goals aren't personalized yet. Say "setup goals" (9 min) or continue as-is.

# Contextual Suggestion (after action)
💡 I noticed you're creating a project. Want to learn about projects first? (10 min)
   Say "learn projects" or continue with project creation.

# Time-Based Suggestion (session start)
👋 Welcome back! You've used Nexus 5 times now. Ready to personalize your goals? (9 min)
```

**Acceptance Criteria**:
- [ ] Suggestions follow consistent format
- [ ] Never block user action
- [ ] Benefit and time stated clearly
- [ ] Emoji usage consistent (💡 for tips, 👋 for welcome)

#### REQ-PD-003: Learning Tracker Schema
**Priority**: HIGH

Track user's onboarding progress in `user-config.yaml`:

```yaml
learning_tracker:
  # Completion status for each skill
  completed:
    setup-goals: false
    setup-workspace: false
    learn-skills: false
    learn-projects: false
    learn-nexus: false

  # Dismissal count (re-suggest after 3 dismissals only if pattern detected)
  dismissed:
    setup-goals: 0
    setup-workspace: 0
    learn-skills: 0
    learn-projects: 0
    learn-nexus: 0

  # Last suggestion timestamp (prevent spam)
  last_suggested:
    setup-goals: null
    setup-workspace: null
    learn-skills: null
    learn-projects: null
    learn-nexus: null

  # User preference for suggestion frequency
  suggestion_preference: "normal"  # "normal", "minimal", "off"

  # Session tracking for time-based triggers
  session_count: 0

  # Workflow patterns detected (for learn-skills trigger)
  workflow_patterns: {}

  # Common mistakes detected (for learn-nexus trigger)
  common_mistakes: {}
```

**Acceptance Criteria**:
- [ ] Schema added to user-config.yaml template
- [ ] Tracks completion state per skill
- [ ] Tracks dismissal count per skill
- [ ] Respects user preference setting
- [ ] Increments session_count on each startup

#### REQ-PD-004: Learning Tracker Update Mechanism
**Priority**: HIGH

**WHEN to Update**:

| Event | Update Action | Updater |
|-------|---------------|---------|
| Skill completion | Set `completed[skill]: true` | The skill itself (Step 8) |
| Suggestion dismissed | Increment `dismissed[skill]` | Orchestrator/Menu |
| Suggestion shown | Update `last_suggested[skill]` | Orchestrator/Menu |
| Session start | Increment `session_count` | nexus-loader.py |
| Workflow detected | Add to `workflow_patterns` | close-session (Step 5c) |
| Mistake detected | Add to `common_mistakes` | close-session (Step 5c) |

**WHO Updates**:

| Component | Responsibility |
|-----------|----------------|
| **nexus-loader.py** | Increment `session_count` on `--startup` |
| **Each onboarding skill** | Set own `completed[skill]: true` at end |
| **Orchestrator/Menu** | Track `dismissed` and `last_suggested` |
| **close-session skill** | Detect patterns and mistakes |

**HOW to Update** (Implementation):

```python
# In nexus-loader.py load_startup():
def update_session_count(user_config_path):
    """Increment session count on each startup"""
    config = yaml.safe_load(open(user_config_path))
    if 'learning_tracker' not in config:
        config['learning_tracker'] = DEFAULT_LEARNING_TRACKER
    config['learning_tracker']['session_count'] += 1
    yaml.dump(config, open(user_config_path, 'w'))

# In each onboarding skill SKILL.md (Step 8):
"""
### Step 8: Mark Complete and Close Session

1. Update learning tracker:
   - Read user-config.yaml
   - Set `learning_tracker.completed.{skill-name}: true`
   - Write user-config.yaml

2. Run close-session skill
"""

# In orchestrator menu display:
"""
If suggestion dismissed:
1. Read user-config.yaml
2. Increment `learning_tracker.dismissed.{skill-name}`
3. Update `learning_tracker.last_suggested.{skill-name}` to now
4. Write user-config.yaml
"""
```

**Guidance Rules**:
- **Automatic**: Session count, pattern detection, mistake detection
- **Manual confirmation**: Skill completion (user completes skill)
- **Implicit**: Dismissal (user ignores suggestion)
- **Never re-suggest** if: `dismissed[skill] >= 3` AND `suggestion_preference != "normal"`
- **Always re-suggest** if: Pattern detected that skill would help

**Acceptance Criteria**:
- [ ] Session count incremented on every startup
- [ ] Skill completion tracked automatically
- [ ] Dismissals tracked and respected
- [ ] Pattern detection feeds into suggestions
- [ ] User can set preference to "minimal" or "off"

#### REQ-PD-005: Suggestion Frequency Control
**Priority**: MEDIUM

**Frequency Rules**:

| Preference | Behavior |
|------------|----------|
| `"normal"` | Suggest on every relevant trigger |
| `"minimal"` | Suggest only on strong triggers (state-based) |
| `"off"` | Never suggest (user must explicitly request) |

**Cool-Down Rules**:
- Same skill: Don't re-suggest within 24 hours
- Any skill: Max 2 suggestions per session
- Dismissed 3x: Only re-suggest if strong pattern detected

**Implementation**:
```python
def should_suggest(skill_name, learning_tracker, trigger_strength):
    """Determine if suggestion should be shown"""
    pref = learning_tracker['suggestion_preference']

    if pref == 'off':
        return False

    if pref == 'minimal' and trigger_strength != 'strong':
        return False

    # Check cool-down (24 hours)
    last = learning_tracker['last_suggested'].get(skill_name)
    if last and (now - last) < timedelta(hours=24):
        return False

    # Check dismissal threshold
    dismissed = learning_tracker['dismissed'].get(skill_name, 0)
    if dismissed >= 3 and trigger_strength != 'pattern_detected':
        return False

    return True
```

**Acceptance Criteria**:
- [ ] Preference setting respected
- [ ] Cool-down period enforced
- [ ] Dismissal threshold respected
- [ ] Strong triggers override limits

---

### 2.4 Orchestrator & Menu Updates

#### REQ-ORCH-001: Modern Menu Header Design
**Priority**: HIGH

**Replace ASCII art banner** with clean, professional header:

**Current** (REMOVE - 8+ lines):
```
    ███╗   ██╗███████╗██╗  ██╗██╗   ██╗███████╗
    ...etc...
```

**New** (3 lines):
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 NEXUS • Self-Evolving Work Organization
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Benefits**:
- Saves 5+ lines of vertical space
- Professional and modern appearance
- Works in all terminal widths
- Maintains branding

**Acceptance Criteria**:
- [ ] Old ASCII banner removed from orchestrator.md
- [ ] New header implemented (3 lines max)
- [ ] Consistent with section separators (━)
- [ ] Works in narrow terminals (80 chars)

#### REQ-ORCH-002: Menu Display for New State
**Priority**: HIGH

When `system_state == "first_time_with_defaults"`:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 NEXUS • Self-Evolving Work Organization
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚀 QUICK START MODE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Smart defaults active. You can work immediately!

💡 Optional: Say "setup goals" to personalize (9 min)

🎯 YOUR GOALS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Role: [Your role]
Goal: [Your goal]

📦 PROJECTS & 🔄 SKILLS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

No projects yet. Say "create project" to start.

System Skills:
• create-project → "new project"
• create-skill → "new skill"

💬 WHAT WOULD YOU LIKE TO DO?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Just tell me what you want to work on.
```

**Acceptance Criteria**:
- [ ] Quick Start Mode notice visible for new state
- [ ] Onboarding suggestion present (non-blocking)
- [ ] Menu sections display correctly
- [ ] Natural language prompt at bottom

#### REQ-ORCH-003: Remove Forced Onboarding
**Priority**: CRITICAL

Modify orchestrator to NEVER force onboarding projects:

**Current Behavior** (REMOVE from nexus-loader.py lines 306-319):
```python
if not files_exist['goals']:
    result['system_state'] = 'first_time_setup'
    result['instructions'] = {
        'action': 'load_and_execute_project',
        'project_id': '00-define-goals',
        ...
    }
```

**New Behavior**:
```python
if not files_exist['goals']:
    create_smart_defaults(base_path)
    result['system_state'] = 'first_time_with_defaults'
    result['instructions'] = {
        'action': 'display_menu',
        'suggest_onboarding': True,
        'message': 'Quick Start Mode - Smart defaults active'
    }
```

**Acceptance Criteria**:
- [ ] No forced project loading for new users
- [ ] Menu always shown first
- [ ] Onboarding available on request only
- [ ] `suggest_onboarding` flag in JSON output

#### REQ-ORCH-004: Routing Priority Update
**Priority**: MEDIUM

Update skill routing priority in orchestrator.md:

| Priority | Category | Examples |
|----------|----------|----------|
| 0 | Special commands | "explain Nexus", "what is Nexus" |
| 0.5 | **Onboarding skills** (NEW) | "setup goals", "learn projects" |
| 1 | User skills | 03-skills/* |
| 2 | System skills | 00-system/skills/* |
| 3 | Project continuation | "continue X", "work on Y" |
| 4 | General response | Natural conversation |

**Acceptance Criteria**:
- [ ] Onboarding skill triggers recognized at Priority 0.5
- [ ] User skills still take priority over system skills
- [ ] No conflicts with existing routing
- [ ] "setup goals" routes to setup-goals skill (not create-project)

---

## 3. Non-Functional Requirements

### 3.1 Performance

| Requirement | Target | Measurement |
|-------------|--------|-------------|
| Smart default creation | <500ms | Time from detection to files created |
| Template detection | <100ms | Time for is_template_file() |
| Total startup | <2 seconds | Time from --startup to JSON output |
| SKILL.md size | <500 lines | Line count per skill |
| Token efficiency | <2000 tokens/skill | Estimated token count |

### 3.2 Compatibility

| Requirement | Details |
|-------------|---------|
| Backward compatibility | Existing installations work unchanged |
| Old pattern detection | `[TODO: Set in onboarding` still detected |
| JSON output format | No breaking changes |
| Platform support | Windows, macOS, Linux |
| Python version | 3.8+ |

### 3.3 Maintainability

| Requirement | Implementation |
|-------------|----------------|
| Code organization | Smart default logic in dedicated functions |
| Template constants | Defined at top of nexus-loader.py |
| Skill creation | All skills via create-skill workflow |
| Documentation | CLAUDE.md, product-overview.md updated |

---

## 4. Constraints

### 4.1 Technical Constraints
- Must work with Python 3.8+
- No new external dependencies
- Must fit within existing file structure
- Skills must validate with quick_validate.py

### 4.2 Design Constraints
- Preserve CAVE pedagogical framework
- Maintain close-session habit teaching
- Keep skill-first execution principle
- YAML v2.0 format (only name + description)

### 4.3 Scope Constraints
- Phase 1: Core B5 + B3 + Menu redesign
- Phase 2: Full progressive disclosure system
- Out of scope: Multi-language templates

---

## 5. Dependencies

### 5.1 Internal Dependencies

| Dependency | Type | Description |
|------------|------|-------------|
| nexus-loader.py | Modify | Add smart defaults + state detection |
| orchestrator.md | Modify | Update menu display + routing + header |
| create-skill | Use | Create all 5 onboarding skills |
| init_skill.py | Execute | Initialize skill directories |
| quick_validate.py | Execute | Validate skill YAML |
| teaching-scripts.md | Source | Content for skill references |
| close-session | Integrate | Final step in all skills |

### 5.2 External Dependencies
- None (self-contained system)

---

## 6. Acceptance Testing

### 6.1 Fresh Install Test
```
1. Delete 01-memory/ folder
2. Run: python nexus-loader.py --startup
3. Expected:
   - Files created in 01-memory/
   - learning_tracker in user-config.yaml
   - system_state = "first_time_with_defaults"
   - action = "display_menu"
   - suggest_onboarding = true
   - Menu displayed (not forced project)
```

### 6.2 Idempotent Creation Test
```
1. Run --startup twice
2. Expected:
   - Second run detects existing files
   - No duplicate creation
   - No errors
   - session_count incremented to 2
```

### 6.3 Template Detection Test
```
1. With smart default goals.md:
   is_template_file(goals.md) == True
2. After removing smart_default flag:
   is_template_file(goals.md) == False
3. With old TODO pattern:
   is_template_file(old_goals.md) == True
```

### 6.4 Skill Loading Test
```
For each skill in [setup-goals, setup-workspace, learn-skills, learn-projects, learn-nexus]:
1. Run: python nexus-loader.py --skill {skill}
2. Expected: Skill loads correctly with references
3. Verify: YAML validates with quick_validate.py
```

### 6.5 Learning Tracker Test
```
1. Complete setup-goals skill
2. Check user-config.yaml
3. Expected: learning_tracker.completed.setup-goals == true
4. Dismiss setup-workspace suggestion 3x
5. Expected: learning_tracker.dismissed.setup-workspace == 3
```

### 6.6 Trigger Routing Test
```
1. "setup goals" → setup-goals skill
2. "learn projects" → learn-projects skill
3. "learn skills" → learn-skills skill
4. "create project" → create-project skill (NOT setup-workspace)
5. "how do projects work" → learn-projects skill
```

### 6.7 Backward Compatibility Test
```
1. Use existing installation with completed onboarding
2. Run --startup
3. Expected:
   - system_state = "operational"
   - Normal menu displayed
   - No regression in behavior
   - No learning_tracker required for existing users
```

---

## 7. Risks and Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Breaking existing installations | HIGH | LOW | Backward compatibility testing, fallback detection |
| Users skip and get confused | MEDIUM | MEDIUM | Progressive disclosure triggers, contextual help |
| Pedagogical value lost | HIGH | LOW | Preserve CAVE framework, all content in skills |
| Template detection false positives | MEDIUM | LOW | Multiple detection methods (YAML + pattern) |
| Skills not discoverable | MEDIUM | MEDIUM | Menu hints, contextual suggestions, routing priority |
| Learning tracker data loss | MEDIUM | LOW | Graceful defaults, migration path |
| create-skill workflow changes | LOW | LOW | Use stable v2.0 format |

---

## 8. Implementation Phases

### Phase 1: Core Implementation
- [ ] B5 Smart Defaults in nexus-loader.py
  - [ ] Template constants (SMART_DEFAULT_GOALS, etc.)
  - [ ] is_template_file() function
  - [ ] create_smart_defaults() function
  - [ ] State detection updates
- [ ] 5 onboarding skills created via create-skill
  - [ ] setup-goals
  - [ ] setup-workspace
  - [ ] learn-skills
  - [ ] learn-projects
  - [ ] learn-nexus
- [ ] Orchestrator updates
  - [ ] New header design (remove ASCII art)
  - [ ] first_time_with_defaults state handling
  - [ ] Routing priority update
- [ ] Basic testing

### Phase 2: Progressive Disclosure
- [ ] Learning tracker implementation
  - [ ] Schema in user-config.yaml
  - [ ] Session count increment
  - [ ] Completion tracking
  - [ ] Dismissal tracking
- [ ] Contextual triggers
  - [ ] State-based triggers
  - [ ] Pattern-based triggers
- [ ] Suggestion display
  - [ ] Format implementation
  - [ ] Cool-down logic
- [ ] Extended testing

### Phase 3: Cleanup & Polish
- [ ] Archive original onboarding projects
- [ ] Deprecate skip-onboarding skill
- [ ] Update all project planning files
- [ ] Documentation updates
- [ ] Migration notes for users

---

## 9. Glossary

| Term | Definition |
|------|------------|
| Smart Defaults | Auto-created template files that let system work immediately |
| Template File | A file with `smart_default: true` flag or `[TODO:` placeholder |
| Personalized File | A file where user has added real content |
| CAVE Framework | Concrete-Action-Value-Explanation pedagogical pattern |
| Progressive Disclosure | Revealing information when contextually appropriate |
| Skill-First Execution | Routing principle where skills have priority over projects |
| Learning Tracker | Schema in user-config.yaml tracking onboarding progress |
| Soft Dependency | Skill suggests but doesn't require another skill first |

---

## 10. Appendix

### A. State Machine Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        SYSTEM STATES                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  [No Memory Files]                                               │
│        │                                                         │
│        ▼                                                         │
│  create_smart_defaults()                                        │
│        │                                                         │
│        ▼                                                         │
│  ┌─────────────────────────┐                                    │
│  │first_time_with_defaults │                                    │
│  │ • display_menu          │                                    │
│  │ • suggest_onboarding    │                                    │
│  │ • learning_tracker init │                                    │
│  └────────────┬────────────┘                                    │
│               │                                                  │
│    ┌──────────┴──────────┐                                      │
│    │                     │                                       │
│    ▼                     ▼                                       │
│  [User works]      [User completes                              │
│  [immediately]      onboarding skills]                          │
│    │                     │                                       │
│    └──────────┬──────────┘                                      │
│               │                                                  │
│               ▼                                                  │
│  ┌─────────────┐                                                │
│  │ operational │                                                │
│  │ • display_menu                                               │
│  │ • full functionality                                         │
│  │ • learning_tracker active                                    │
│  └─────────────┘                                                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### B. Skill Creation Workflow (via create-skill)

```
For each skill:
1. python scripts/init_skill.py {skill-name} --path 00-system/skills
2. Edit SKILL.md:
   - YAML frontmatter (name + description only)
   - Workflow sections
   - Prerequisites check
   - Close-session final step
3. Create references/:
   - Extract from teaching-scripts.md
   - Extract from source project design.md
4. Validate: python scripts/quick_validate.py 00-system/skills/{skill-name}
5. Test: python nexus-loader.py --skill {skill-name}
```

### C. Learning Tracker Update Flow

```
Session Start (nexus-loader.py --startup)
├── Increment session_count
├── Check suggestion triggers
│   ├── State-based triggers
│   ├── Pattern-based triggers (from close-session)
│   └── Time-based triggers
└── Display menu with appropriate suggestions

During Session
├── User completes skill → Mark completed[skill] = true
├── User dismisses suggestion → Increment dismissed[skill]
└── User works normally → No tracker update

Session End (close-session)
├── Detect workflow patterns → Add to workflow_patterns
├── Detect mistakes → Add to common_mistakes
└── Save all tracker updates to user-config.yaml
```

### D. Skill Content Sources

| Skill | Source Files | Key Content |
|-------|--------------|-------------|
| setup-goals | `00-define-goals/` | Goal elicitation, AI suggestions, memory init |
| setup-workspace | `01-first-project/` | Projects vs Skills, workspace design |
| learn-skills | `02-first-skill/` | Workflow ID, 3-criteria, trigger phrases |
| learn-projects | NEW | Project creation, planning, execution |
| learn-nexus | `03-system-mastery/` | AI patterns, collaboration, pitfalls |

### E. Modern Menu Header Alternatives

**Selected Design**:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 NEXUS • Self-Evolving Work Organization
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Alternative 1** (Minimal):
```
NEXUS v4 • Self-Evolving Work Organization
```

**Alternative 2** (Box):
```
┌─ NEXUS ─────────────────────────────────────────────────────┐
│ Self-Evolving Work Organization                              │
└──────────────────────────────────────────────────────────────┘
```

---

*This document defines the complete requirements for transforming Nexus from forced onboarding to optional, skill-based onboarding with progressive disclosure.*
