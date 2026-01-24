# Gap Analysis: Current vs Desired Onboarding State

> **Date**: 2026-01-24
> **Purpose**: Identify gaps between current implementation and desired onboarding experience
> **Context**: Review of all system documentation before plan revision

---

## CURRENT IMPLEMENTATION (What Already Exists)

### SessionStart Hook
- **7 templates** with MECE priority system (Lines 269-292 in sessionstart-templates-analysis.md)
  - 5 startup templates (first_run, onboarding_incomplete, active_builds, fresh_workspace, system_ready)
  - 2 compact templates (planning, execution)
- **3-tier detection priority**: Session ID → Transcript parsing → Recent build
- **State-driven context injection**: Loads appropriate template based on flags
- **Performance**: <200ms execution time
- **File**: `.claude/hooks/session_start.py`

### 6 Existing Learning Skills
| Skill | Duration | Priority | Auto-Completes |
|-------|----------|----------|----------------|
| setup-memory | 10 min | critical | No |
| create-folders | 5-8 min | high | No |
| learn-builds | 8-10 min | high | ✓ (first_build_created) |
| learn-skills | 10-12 min | high | ✓ (first_task_executed) |
| learn-integrations | 10-12 min | high | No |
| learn-nexus | 15-18 min | medium | No |

**Total**: 58-70 minutes of learning content across 6 skills

### State Management
- **Single source of truth**: `learning_tracker.completed` in user-config.yaml
- **6 skill flags**: All boolean (true/false)
- **2 mandatory skills**: setup-memory (critical) + create-folders (high)
- **4 optional skills**: All others (suggested but skippable)
- **File**: `/01-memory/user-config.yaml` (lines 32-43)

### Template Routing Logic
```
Priority 0: startup_first_run → Shows "setup memory" CTA
Priority 1: startup_onboarding_incomplete → Dynamic pending list
Priority 2: startup_active_builds → Resume work CTA
Priority 3: startup_fresh_workspace → "Start first build" CTA
Priority 4: startup_system_ready → Open-ended "What would you like to work on?"
```

---

## DESIRED STATE (From User Feedback + Insights)

### Creator Requirements (From resume-context.md + discovery.md)
1. **No linear fixed onboarding** - Users might churn if forced through all steps
2. **Enforce first 2 steps** - "How It Works" + Setup Memory (mandatory)
3. **Roadmap optional** - Don't force long planning
4. **Core lessons**:
   - Session boundaries (1 topic per session, use close-session)
   - plan→build workflow (planning session → execution session)
5. **Use existing infrastructure** - Don't rebuild SessionStart hook
6. **15-30 min proper onboarding** - Not 3-10 min rushed

### User Testing Insights (From onboarding-core-insights.md)
1. **Progressive disclosure critical** (Insight #1)
   - Introduce concepts one at a time, not all at once
   - Don't show all phases upfront

2. **Explain "How It Works" FIRST** (Insight #2)
   - Teach 2 work modes (Build vs Execute) before anything else
   - Explain 5-folder structure (`00-system`, `01-memory`, `02-builds`, `03-skills`, `04-workspace`)
   - Introduce workspace map concept early

3. **Force planning before execution** (Insight #3)
   - People (and AI) jump to implementation too quickly
   - Structured planning process is the core innovation
   - Quality planning = better results

4. **Context organization must come early** (Insight #4)
   - Workspace map prevents AI from "shooting files everywhere"
   - Must be created early and kept updated
   - Auto-detect when outdated

5. **Language preference matters** (Insight #6)
   - Ask at the very start
   - Force consistent usage (no mixing)

6. **Quality over speed** (Insight #7)
   - 15-30 min proper setup leads to much better long-term results
   - Rushed 5-min onboarding = poor adoption

---

## GAP ANALYSIS

### ❌ CRITICAL GAPS (Must Build)

#### 1. "How Nexus Works" Skill MISSING
**Status**: Does NOT exist
**Location**: Should be `00-system/skills/learning/how-nexus-works/SKILL.md`

**What It Should Teach** (From onboarding-core-insights.md):
- Part 1: Two work modes (Build vs Execute) - 2 min
- Part 2: Five-folder structure - 2 min
- Part 3: Workspace map concept - 2 min
- Part 4: Language preference - 1 min
- **Total**: ~7 min

**Why Critical**:
> "Wir müssen irgendwie dieses 'How Nexus works' einführen... Da muss der Nutzer eingeführt werden." (Insight #2)

Users are jumping into tasks without understanding fundamentals. This MUST be the first onboarding step.

**Required Changes**:
- Create new skill file
- Add to ONBOARDING_SKILLS in `/00-system/core/nexus/config.py`
- Add `how_nexus_works: false` to user-config.yaml template
- Update startup_first_run template to route here (not setup-memory)

---

#### 2. First 2 Steps Not Enforced
**Current State**: Everything is optional (user can skip)
**Desired State**: Enforce "How It Works" + setup-memory before allowing work

**Implementation Gap**:
- SessionStart templates show suggestions but don't block
- No validation preventing users from starting builds without onboarding
- startup_system_ready (priority 4 fallback) allows work even if not onboarded

**Required Changes**:
- Modify template selection logic to block if first 2 not complete
- Add validation in plan-build skill: Check flags before allowing new build
- Update startup templates to make enforcement clear

---

#### 3. "Plan → Build" Workflow Not Taught
**Current State**: Implicit in build structure, never explicitly explained
**Desired State**: Users understand to plan in one session, execute in another

**Where It Should Be Taught**:
- Option 1: Add to "how-nexus-works" skill (Part 5)
- Option 2: Enhance learn-builds skill with workflow section
- Option 3: Both (brief in how-nexus-works, deep in learn-builds)

**Why Critical**:
> "Die allermeisten Leute sofort in die Umsetzung gehen. Und deswegen kriegen sie keine gute Ergebnisse." (Insight #3)

**Required Changes**:
- Add workflow teaching content to skill(s)
- Emphasize "Planning session → close-session → Execution session"
- Explain why this pattern produces better results

---

#### 4. "1 Topic Per Session" Not Taught
**Current State**: Not mentioned anywhere in onboarding
**Desired State**: Users understand clean context boundaries

**Why It Matters**:
- Better AI performance with focused context
- Cleaner session summaries
- Prevents context mixing and confusion

**Required Changes**:
- Add to close-session skill documentation
- Add to how-nexus-works or learn-builds
- Emphasize in session end messaging

---

### 🔧 NEEDS ENHANCEMENT (Improve Existing)

#### 5. setup-memory Skill Structure
**Current**: Language preference is step 2 (after welcome)
**Desired**: Language preference should be step 1 (before anything else)

**Additional Enhancement**:
- Emphasize "this defines scope of THIS Nexus instance"
- Make it clear: 1 instance = 1 user goal

**Files to Update**:
- `/00-system/skills/learning/setup-memory/SKILL.md` (lines 1-297)

---

#### 6. create-folders Workspace Map Emphasis
**Current**: Workspace map mentioned, but not emphasized
**Desired**: Make workspace map creation/update more prominent

**Why Critical**:
> "Der hat dann nämlich in alle Richtungen Files geschossen, wusste aber gar nicht, was er hat" (Insight #4)

**Required Changes**:
- Add explicit "workspace map is your AI's navigation guide" framing
- Show example of how AI uses map
- Emphasize keeping it updated

**Files to Update**:
- `/00-system/skills/learning/create-folders/SKILL.md` (lines 1-236)

---

#### 7. learn-builds Workflow Teaching
**Current**: Teaches build structure, lifecycle, decision framework
**Desired**: Also teach "plan → build" workflow pattern

**Required Changes**:
- Add new section: "The Planning Pattern"
- Explain: Session 1 (Planning) → close → Session 2 (Execution)
- Why it works better than doing both in one session

**Files to Update**:
- `/00-system/skills/learning/learn-builds/SKILL.md` (lines 1-160)

---

#### 8. SessionStart Template Routing
**Current**: startup_first_run routes to setup-memory
**Desired**: startup_first_run routes to how-nexus-works

**Required Changes**:
- Update `.claude/hooks/templates/startup_first_run.md` CTA
- Change from "setup memory" to "how nexus works"
- Update startup_onboarding_incomplete to check how_nexus_works flag

**Files to Update**:
- `.claude/hooks/templates/startup_first_run.md`
- `.claude/hooks/templates/startup_onboarding_incomplete.md`

---

### ✅ ALREADY GOOD (No Changes Needed)

1. **State management architecture** - Single source of truth works well
2. **MECE priority system** - Template selection logic is solid
3. **Auto-completion checkpoints** - learn-builds and learn-skills auto-complete on doing
4. **Progressive skill system** - 6 skills form clear learning path
5. **SessionStart hook infrastructure** - Robust, performant, well-documented
6. **3-tier detection priority** - Session ID → transcript → recent build is bulletproof

---

## PRIORITY RANKING

### Must Have (P0)
1. Create "how-nexus-works" skill
2. Update startup_first_run to route to how-nexus-works
3. Add how_nexus_works to state management (config.py, user-config.yaml)

### Should Have (P1)
4. Enhance setup-memory (language first, scope emphasis)
5. Enhance create-folders (workspace map emphasis)
6. Enhance learn-builds (add plan→build workflow)
7. Update SessionStart templates (onboarding_incomplete, etc.)

### Nice to Have (P2)
8. Add enforcement logic (block work until first 2 complete)
9. Add "1 topic per session" teaching
10. Update orchestrator.md skill catalog

---

## EFFORT ESTIMATION

| Task | Complexity | Time Est. |
|------|-----------|-----------|
| Create how-nexus-works skill | Medium | 2-3 hours |
| Update state management | Low | 30 min |
| Enhance 3 existing skills | Low-Medium | 2-3 hours |
| Update SessionStart templates | Low | 1 hour |
| Add enforcement logic | Medium | 2 hours |
| Testing & validation | Medium | 2 hours |
| **Total** | | **9-11 hours** |

---

## WHAT TO BUILD (Summary)

### Phase 1: New "How Nexus Works" Skill
- Create skill file with 4-part structure
- Add to system configuration
- Update templates to route here first

### Phase 2: Enhance Existing Skills
- setup-memory: Language first, scope emphasis
- create-folders: Workspace map prominence
- learn-builds: Add workflow teaching

### Phase 3: Update Templates & State
- Update startup templates
- Add enforcement logic (optional)
- Test complete flow

---

**Next Step**: Revise [03-plan.md](02-builds/04-improved-onboarding-design/01-planning/03-plan.md) with this analysis
