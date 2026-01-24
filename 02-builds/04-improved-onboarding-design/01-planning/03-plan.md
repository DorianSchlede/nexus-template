# Improved Onboarding Design - Complete Plan

**Build Type**: Strategy
**Status**: Planning Complete
**Date**: 2026-01-24

---

## Executive Summary

We're redesigning Nexus onboarding to teach users the core mental model (BUILD systems vs WORK with them) while avoiding churn through flexible, state-driven flows. The approach combines a heroic intro with real examples, optional tour, merged setup process, and intelligent SubAgent file analysis.

**Key Innovation**: Fork decision allows users to choose their path (tour vs direct setup), respecting learning styles while ensuring proper system initialization.

---

## What We're Building

### 1. NEW: Heroic Intro (Real Examples)

**Location**: `.claude/hooks/templates/startup_first_run.md`

**Content** (complete copy in [complete-specification.md](../02-resources/complete-specification.md)):
```
    ███╗   ██╗███████╗██╗  ██╗██╗   ██╗███████╗
         Welcome to Nexus
         (Powered by Claude Code)

ChatGPT gives you answers.
Nexus and Claude Code build you SYSTEMS.

Here's what people have actually built:

  🔬 "MedScan" - Medical Research Platform
  💼 "JobTracker" - Application Automation
  🏃 "FitPlan" - Personal Performance Lab
  📝 "ContentEngine" - LinkedIn Production System
  🗺️ "ProductOS" - Strategy & Roadmap System

[Full copy with dad's MRI story, girlfriend's job tracker, etc.]
```

**Design Principles**:
- Real examples only (no BS marketing)
- Named systems with icons (MedScan, JobTracker, etc.)
- Personality and authenticity ("my dad", "my girlfriend")
- Emphasis on COMPOUNDS (key differentiator)
- "Welcome to Nexus (Powered by Claude Code)" not "NEW ERA"

---

### 2. NEW: Language Selection

**When**: Immediately after heroic intro, before anything else

**Display**:
```
What language do you want to work in?

1. English
2. Deutsch
3. Español
4. Français
5. Italiano
6. 日本語
7. 中文

(All future sessions will use this language)
```

**State**: `onboarding.language_preference: "en" | "de" | ...`

---

### 3. NEW: Fork Decision

**Display**:
```
How do you want to start?

1. Show me how Nexus works (~7 min guided tour)
   → Learn the system, then setup in next session

2. Set up my system now (skip tour, dive in)
   → Quick setup, learn as you go

Choose 1 or 2:
```

**Routing**:
- Path A (Tour): Load `how-nexus-works` skill → End session → Session 2 loads `setup-system`
- Path B (Direct): Load `setup-system` skill immediately

**Why This Matters**: Respects different learning styles, prevents churn from forced linear flow

---

### 4. NEW: how-nexus-works Skill

**File**: `00-system/skills/learning/how-nexus-works/SKILL.md`

**Duration**: ~7 minutes

**Content Structure**:
1. **Part 1**: Two work modes (BUILD 🔨 vs WORK 💼) - 2 min
2. **Part 2**: Four pillars (01-memory, 02-builds, 03-skills, 04-workspace) - 2 min
3. **Part 3**: Core innovation (collaborative planning, AI navigation, continuity) - 1 min
4. **Part 4**: Session boundaries (1 topic per session, clean context) - 1 min
5. **Part 5**: Build workflow (plan session → close → execute session) - 1 min

**End Message**:
```
SESSION COMPLETE ✓

Your progress saves automatically.

IMPORTANT: Clean session boundaries matter in Nexus.
Each session = one focus.

This session: System learning (DONE)
Next session: Set up your goals and build your first system

→ Open a NEW chat/session when ready to continue
```

**State Update**:
- `onboarding.status: "tour_complete"`
- `learning_tracker.completed.how_nexus_works: true`

**Why Critical**: User testing showed "explain how it works FIRST" is essential (Insight #2 from onboarding-core-insights)

---

### 5. NEW: setup-system Skill (Merged)

**File**: `00-system/skills/learning/setup-system/SKILL.md`

**Duration**: 10-15 minutes (with file upload)

**Merges**: Old setup-memory + create-roadmap + create-folders skills into ONE

**Pre-Execution**: Auto-creates onboarding project (`02-builds/00-onboarding-session/`)

#### Flow (7 Steps):

**STEP 1: Context Upload (Optional)**
- User can upload files to `04-workspace/input/`
- Triggers SubAgent analysis (see SubAgent Strategy below)
- Or skip entirely

**STEP 2: Core Question**
- "Who are you, OR what do you want to achieve/build?"
- Extracts: role, short-term goal, long-term vision, system type
- Follow-up questions if needed

**STEP 3: Generate Roadmap**
- AI generates 3-7 roadmap items from goals + file insights
- User confirms/refines
- Output: roadmap.md

**STEP 4: Create Workspace Structure**
- AI suggests folder structure from roadmap themes + file analysis
- User confirms/refines
- Creates folders + workspace-map.md
- Moves files from input/ to organized locations

**STEP 5: Initiate Projects**
- Creates full scaffold for each roadmap item:
  - 4 folders (01-planning, 02-resources, 03-working, 04-outputs)
  - Fills ONLY 01-overview.md (AI-generated purpose + success criteria)
  - Empty templates for discovery.md, plan.md, steps.md
  - resume-context.md with dependencies

**STEP 6: Save Everything**
- goals.md → 01-memory/
- roadmap.md → 01-memory/
- workspace-map.md → 04-workspace/
- Archive onboarding project → 05-archived/

**STEP 7: End Session**
- Teach session boundaries
- Prompt: "Open a NEW chat/session when ready"

**Cross-Session Continuity**:
```yaml
setup_system_state:
  step_completed: 0-7  # Resume from last completed step
  files_uploaded: bool
  file_analysis_done: bool
  role_captured: bool
  goals_captured: bool
  roadmap_created: bool
  workspace_created: bool
  projects_initiated: bool
```

**Why Merged**: User feedback "I dont want linear fixed onboarding" + reducing session count from 3-4 to 1

---

### 6. NEW: SubAgent File Analysis

**Trigger**: When user uploads files in setup-system Step 1

**Assignment Logic** (KB-based, NOT file count):
```python
if total_kb < 1000: agent_count = 1
elif total_kb < 3000: agent_count = 2
elif total_kb < 5000: agent_count = 3
elif total_kb < 10000: agent_count = 5
elif total_kb < 20000: agent_count = 8
else: agent_count = min(ceil(total_kb / 2500), 10)
```

**Key Features**:
- Auto-split files >2MB to avoid context window issues
- Thematic clustering by filename patterns (ask user to confirm)
- Parallel execution (up to 10+ agents, no hard limit)
- Unlimited agents possible (scales with content)

**Prompt File**: `00-system/core/nexus/prompts/subagent-file-analysis.md`

**Output Contract** (per agent):
```json
{
  "file_analyses": [
    {
      "filename": "...",
      "path": "...",
      "type": "document|spreadsheet|code|data",
      "summary_short": "One sentence",
      "summary_detailed": "2-4 sentences with specifics (names, amounts, entities)",
      "theme": "clients|sales|research|finance|code|general",
      "detected_entities": ["names", "companies", "amounts"],
      "suggested_folder": "clients/acme/"
    }
  ],
  "professional_context": {
    "role": "Best guess or null",
    "domain": "Industry or null",
    "skills": ["skill1", "skill2"]
  },
  "integration_opportunities": [
    {
      "name": "HubSpot CRM",
      "type": "CRM|Email|Calendar|...",
      "evidence": "Found config/hubspot.json with API credentials",
      "suggestion": "Connect to auto-sync client data for proposals"
    }
  ],
  "workspace_structure_suggestion": {
    "folders": [
      {
        "path": "clients/",
        "purpose": "Why this folder",
        "subfolders": ["acme/", "beta/"]
      }
    ]
  }
}
```

**Synthesis**: Combine all agent outputs → `02-builds/00-onboarding-session/02-resources/file-analysis.json`

**Why Critical**: Users with existing work need file organization help (Insight #4: workspace map prevents "shooting files everywhere")

---

### 7. NEW: Onboarding Project Approach

**Structure**:
```
02-builds/00-onboarding-session/
├── 01-planning/
│   ├── 01-overview.md (purpose: "Set up YOUR Nexus system")
│   └── 04-steps.md (onboarding checklist)
│
├── 02-resources/
│   ├── file-analysis.json (SubAgent output - full detail)
│   └── file-analysis-summary.md (human-readable)
│
├── 03-working/
│   └── input/ → symlink to 04-workspace/input/
│
└── 04-outputs/
    ├── goals.md (moves to 01-memory/)
    ├── roadmap.md (moves to 01-memory/)
    └── workspace-structure.md (proposed folders)
```

**Lifecycle**:
1. Created automatically when setup-system starts
2. SubAgent saves analysis to 02-resources/
3. During setup: files moved from input/ → organized folders
4. After complete: Archived to 05-archived/

**Why This Works**:
- Follows system patterns (it's a build!)
- Traceable (can review analysis later)
- Clean lifecycle (active → archived)
- No redundant file_map.md in 01-memory/

---

### 8. NEW: Full Project Scaffolding

**What Gets Created** (for each roadmap item):
```
02-builds/XX-name/
├── 01-planning/
│   ├── 01-overview.md (FILLED by AI)
│   ├── 02-discovery.md (EMPTY - template)
│   ├── 03-plan.md (EMPTY - template)
│   ├── 04-steps.md (EMPTY - template)
│   └── resume-context.md (standard)
├── 02-resources/
├── 03-working/
└── 04-outputs/
```

**01-overview.md Contents** (AI-generated):
- Purpose (from roadmap rationale)
- Success criteria (3 measurable outcomes)
- Context (user goal + file insights)
- Dependencies (from roadmap)
- Next steps (how to start)

**Why Full Scaffold**: Users see their roadmap as REAL (not just a list), reduces friction to start first build

---

### 9. UPDATED: State Management Schema

```yaml
onboarding:
  status:
    - "not_started"
    - "tour_in_progress"
    - "tour_complete"
    - "setup_in_progress"
    - "system_setup_complete"
    - "first_build_started"
    - "complete"

  in_progress_skill: null | "how-nexus-works" | "setup-system"

  language_preference: null | "en" | "de" | "es" | "fr" | "it" | "ja" | "zh"
  chosen_path: null | "tour" | "direct"

  setup_system_state:
    step_completed: 0-7
    files_uploaded: bool
    file_analysis_done: bool
    role_captured: bool
    goals_captured: bool
    roadmap_created: bool
    workspace_created: bool
    projects_initiated: bool

learning_tracker:
  completed:
    how_nexus_works: false  # NEW
    setup_memory: false
    create_roadmap: false  # NEW (merged into setup-system)
    create_folders: false
    learn_builds: false
    learn_skills: false
    learn_integrations: false
    learn_nexus: false
```

---

### 10. UPDATED: SessionStart Resume Logic

```python
def determine_onboarding_action(session_source, onboarding_state):
    # Check in-progress skill (cross-session continuity)
    if onboarding_state["in_progress_skill"]:
        if skill == "setup-system":
            # Resume from specific step
            step = onboarding_state["setup_system_state"]["step_completed"]
            return resume_skill("setup-system", step + 1)
        else:
            return resume_skill(skill)

    # Route based on status
    status = onboarding_state["status"]

    if status == "not_started":
        return show_heroic_intro()

    elif status == "tour_complete":
        return load_setup_system_mandatory()

    elif status == "system_setup_complete":
        return show_roadmap_and_suggest_first_build()

    elif status == "complete":
        return normal_menu()
```

**Why Critical**: Session compaction mid-onboarding must resume correctly (user concern from conversation)

---

### 11. UPDATED: SessionStart Templates

**Files to Update**:
- `startup_first_run.md` → Add heroic intro + language + fork
- `startup_onboarding_incomplete.md` → Check how_nexus_works flag
- `startup_active_builds.md` → No changes
- `startup_fresh_workspace.md` → No changes
- `startup_system_ready.md` → No changes
- `compact_planning.md` → No changes
- `compact_execution.md` → No changes

---

### 12. NEW: Session Boundary Teaching

**When Taught**:
1. End of how-nexus-works skill
2. End of setup-system skill
3. End of first build (in learn-builds explanation)

**Message Template**:
```
SESSION COMPLETE ✓

Your progress saves automatically.

IMPORTANT: Clean session boundaries matter in Nexus.
Each session = one focus.

This session: [what was accomplished]
Next session: [what comes next]

→ Open a NEW chat/session when ready to continue
```

**Don't Say**: "Say 'close' to end session"
**Do Say**: "Open a NEW chat/session"

**Why Critical**: User testing showed "1 topic per session" is core lesson (Insight from conversation)

---

## What We're NOT Doing

❌ No separate file_map.md in 01-memory/ (use onboarding project)
❌ No mandatory linear flow after fork (allows choice)
❌ No file count limits for SubAgents (KB-based, scales beyond 10)
❌ No "say close" messaging (confusing, just say "new chat")
❌ No default menu blocking (after setup complete, normal operation)
❌ No separate create-folders skill (merged into setup-system)
❌ No separate create-roadmap skill (merged into setup-system)

---

## Implementation Strategy

### Phase 1: Core Skills (Priority 1)

**Tasks**:
1. Create `how-nexus-works` skill file
   - Write 5-part content
   - Add metadata (onboarding: true, duration: 7 min)
   - Test flow and messaging

2. Create `setup-system` skill file
   - Write 7-step flow
   - Add cross-session state tracking
   - Implement auto-project creation
   - Test each step independently

3. Create SubAgent prompt file
   - Write complete analysis prompt
   - Define output contract
   - Add examples (good vs bad)

**Checkpoint**: Skills loadable and executable

---

### Phase 2: Templates & Copy (Priority 1)

**Tasks**:
4. Write heroic intro copy
   - Add to startup_first_run.md
   - Verify ASCII art renders correctly
   - Test personality and tone

5. Update SessionStart templates
   - startup_first_run: heroic intro + language + fork
   - startup_onboarding_incomplete: add how_nexus_works check
   - Test all 7 templates still work

6. Create language selection screen
   - Add to startup_first_run after intro
   - Test language persistence

**Checkpoint**: Templates render correctly, copy feels right

---

### Phase 3: State & Infrastructure (Priority 2)

**Tasks**:
7. Update user-config.yaml schema
   - Add onboarding.language_preference
   - Add onboarding.chosen_path
   - Add onboarding.setup_system_state (8 fields)
   - Add learning_tracker.completed.how_nexus_works
   - Add learning_tracker.completed.create_roadmap

8. Implement SessionStart resume logic
   - Add onboarding_action detection
   - Test tour_complete → setup-system flow
   - Test system_setup_complete → roadmap flow
   - Test cross-session continuity (setup-system mid-step)

9. Add onboarding project auto-creation
   - Trigger when setup-system starts
   - Create 4 folders + symlink
   - Write overview.md + steps.md
   - Test lifecycle (create → use → archive)

**Checkpoint**: State transitions work correctly across sessions

---

### Phase 4: SubAgent Logic (Priority 2)

**Tasks**:
10. Implement KB-based agent assignment
    - Calculate total_kb from files
    - Apply agent count formula
    - Test with various file sizes

11. Implement auto-file-splitting
    - Detect files >2MB
    - Split with overlap for context
    - Test with large PDFs/spreadsheets

12. Implement thematic clustering
    - Filename pattern matching
    - User confirmation dialog
    - Custom clustering option

13. Create synthesis logic
    - Combine multiple agent outputs
    - Dedupe integrations
    - Merge professional context
    - Save to file-analysis.json + summary.md

**Checkpoint**: SubAgent analysis produces useful results

---

### Phase 5: Project Scaffolding (Priority 3)

**Tasks**:
14. Implement full scaffold creation
    - 4 folders per project
    - Empty template files
    - resume-context.md

15. Implement overview.md template with AI generation
    - Purpose from roadmap
    - Success criteria (AI generates 3 items)
    - Context with dependencies
    - Test quality of AI-generated content

16. Add dependency tracking
    - Parse roadmap dependencies
    - Include in overview.md
    - Test dependency ordering

**Checkpoint**: Projects scaffold correctly, overview quality high

---

### Phase 6: Testing & Polish (Priority 3)

**Tasks**:
17. End-to-end flow testing
    - Path A: Tour → setup
    - Path B: Direct setup
    - Path C: Setup with file upload (SubAgents)
    - Test session boundaries and resumption

18. Edge case testing
    - Session compaction mid-setup-system
    - No files uploaded (skip Step 1)
    - User modifies roadmap/folders
    - Very large file upload (>20MB)

19. Language audit
    - Remove "say close" everywhere
    - Verify "open NEW chat" messaging
    - Check Era 3 language compliance
    - Test German/Spanish translations

**Checkpoint**: All flows work, no critical bugs

---

### Phase 7: Documentation & Launch (Priority 3)

**Tasks**:
20. Update system documentation
    - Document new skills in catalog
    - Update CLAUDE.md if needed
    - Create migration notes for existing users

21. Create complete-specification.md archive
    - Already exists, verify completeness
    - Reference from plan.md

22. Final validation
    - Run through fresh installation
    - Measure time (should be <20 min total)
    - User acceptance testing

**Checkpoint**: Ready to ship

---

## Success Metrics

**Onboarding Completion**:
- Setup-system completion rate: >90%
- Time to complete setup-system: <15 min (with files), <10 min (without)
- User returns for Session 2: >80%

**Quality**:
- Heroic intro → fork decision: <5% drop-off
- Fork decision split: 40/60 tour vs direct (validate assumptions)
- SubAgent analysis quality: User satisfaction >85%
- First build started within 24h: >60%

**Cross-Session**:
- Session compaction mid-setup: Resume successful >95%
- State tracking accuracy: 100%

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Users skip tour, get lost later | Include mini-explanations in setup-system, learn-builds auto-loads after first build |
| setup-system too long (churn) | Make file upload optional, allow skip on roadmap refinement |
| SubAgent analysis fails/slow | Graceful degradation: Skip analysis, generate basic structure |
| Session boundary not understood | Repeat teaching at every skill end, detect topic switches |
| Language preference ignored | Validate at every session start, prominent in UI |

---

## Dependencies

**Requires**:
- SessionStart hook must support onboarding_action routing
- User-config.yaml must support new schema
- SubAgent launching infrastructure (Task tool)
- File operations (create, move, symlink)

**Blocks**:
- Other onboarding improvements (this is foundation)

**Related**:
- Build 03 (contextual-learning-injection) provides complementary teaching

---

## Rollout Plan

**Phase 1**: New users only
- Fresh installations get new flow
- Existing users see old menu (check onboarding_complete flag)

**Phase 2**: Migration offer
- Offer existing users to "reset onboarding" and try new flow
- Preserve their existing builds/skills

**Phase 3**: Full rollout
- After 2 weeks of monitoring
- All users default to new flow

---

## Complete Specification Reference

All details (exact copy, complete code, templates) documented in:
- [complete-specification.md](../02-resources/complete-specification.md) (30+ KB)
- [decisions-log.md](../02-resources/decisions-log.md)

This plan is the STRATEGY.
Specification is the COMPLETE IMPLEMENTATION DETAILS.

---

**Plan Status**: COMPLETE AND APPROVED
**Next**: Execute implementation (04-steps.md)
**Last Updated**: 2026-01-24
