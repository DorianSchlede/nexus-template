# Improved Onboarding Design - Execution Steps

**Build Type**: Strategy
**Status**: Planning Complete → Ready for Execution
**Date**: 2026-01-24

---

## Overview

This build has **3 major checkpoints** with **22 total tasks** across 7 phases.

Each checkpoint is independently testable and deliverable. You can pause after any checkpoint and resume in a new session.

**Total Estimated Time**: 15-20 hours of implementation work

---

## CHECKPOINT 1: Skills & Templates Work

**Goal**: Core onboarding skills exist and can be triggered. Heroic intro displays correctly.

**Deliverables**:
- ✅ how-nexus-works skill loadable
- ✅ setup-system skill loadable
- ✅ Heroic intro displays with personality
- ✅ Language selection works
- ✅ Fork decision routes correctly

**Estimated Time**: 6-8 hours

---

### Phase 1: Core Skills (Priority 1)

#### Task 1: Create how-nexus-works Skill

**File**: `00-system/skills/learning/how-nexus-works/SKILL.md`

**Steps**:
- [ ] Create skill directory structure
- [ ] Write YAML metadata (name, description, onboarding: true, duration: "7 min")
- [ ] Write Part 1: Two work modes (BUILD 🔨 vs WORK 💼)
- [ ] Write Part 2: Four pillars (01-memory, 02-builds, 03-skills, 04-workspace)
- [ ] Write Part 3: Core innovation (collaborative planning, AI navigation, continuity)
- [ ] Write Part 4: Session boundaries (1 topic per session)
- [ ] Write Part 5: Build workflow (plan → close → execute)
- [ ] Write end message ("SESSION COMPLETE ✓" with session boundary teaching)
- [ ] Test: Load skill manually, verify content flows naturally

**Reference**: Complete content in `02-resources/complete-specification.md` lines 144-287

**Validation**:
```bash
# Test loading
python 00-system/core/nexus-loader.py --skill how-nexus-works

# Expected: Skill loads, displays Part 1-5, ends with session boundary message
```

---

#### Task 2: Create setup-system Skill

**File**: `00-system/skills/learning/setup-system/SKILL.md`

**Steps**:
- [ ] Create skill directory structure
- [ ] Write YAML metadata (name, description, cross_session_continuity: true)
- [ ] Write pre-execution logic (auto-create onboarding project)
- [ ] Write STEP 1: Context Upload (optional file upload + SubAgent trigger)
- [ ] Write STEP 2: Core Question ("Who are you OR what do you want to build?")
- [ ] Write STEP 3: Generate Roadmap (AI generates 3-7 items)
- [ ] Write STEP 4: Create Workspace Structure (folders + workspace-map.md)
- [ ] Write STEP 5: Initiate Projects (full scaffold, only overview.md filled)
- [ ] Write STEP 6: Save Everything (goals.md, roadmap.md, archive onboarding)
- [ ] Write STEP 7: End Session (session boundary teaching)
- [ ] Add state tracking logic (setup_system_state.step_completed)
- [ ] Add resume logic (check step_completed, resume from step + 1)
- [ ] Test: Load skill, verify each step can be executed

**Reference**: Complete flow in `02-resources/complete-specification.md` lines 290-1204

**Validation**:
```bash
# Test loading
python 00-system/core/nexus-loader.py --skill setup-system

# Expected: Skill loads, shows STEP 1/7, can progress through steps
```

---

#### Task 3: Create SubAgent Prompt File

**File**: `00-system/core/nexus/prompts/subagent-file-analysis.md`

**Steps**:
- [ ] Create prompts directory if not exists
- [ ] Write prompt header (You are analyzing user files...)
- [ ] Write INPUT section (what SubAgent receives)
- [ ] Write YOUR TASK section (4 steps)
- [ ] Write OUTPUT CONTRACT section (complete JSON schema)
- [ ] Write IMPORTANT RULES section (5 rules)
- [ ] Write EXAMPLES section (good vs bad summaries)
- [ ] Add integration opportunity examples
- [ ] Test: Verify prompt is clear and complete

**Reference**: Complete prompt in `02-resources/complete-specification.md` lines 609-729

**Validation**:
```bash
# Verify file exists and is readable
cat 00-system/core/nexus/prompts/subagent-file-analysis.md

# Expected: Complete prompt with examples
```

---

### Phase 2: Templates & Copy (Priority 1)

#### Task 4: Write Heroic Intro Copy

**File**: `.claude/hooks/templates/startup_first_run.md`

**Steps**:
- [ ] Read existing startup_first_run.md
- [ ] Add ASCII art header (Nexus banner)
- [ ] Add "Welcome to Nexus (Powered by Claude Code)" line
- [ ] Add "ChatGPT gives you answers. Nexus builds you SYSTEMS." tagline
- [ ] Add 5 named real-world systems with icons:
  - [ ] 🔬 "MedScan" with dad's MRI story
  - [ ] 💼 "JobTracker" with girlfriend's job search story
  - [ ] 🏃 "FitPlan" with smartwatch connection story
  - [ ] 📝 "ContentEngine" with LinkedIn production story
  - [ ] 🗺️ "ProductOS" with PM roadmap story
- [ ] Add "Used throughout our company" paragraph
- [ ] Add "Why? Because this COMPOUNDS." closing
- [ ] Verify personality and authenticity (no BS marketing)
- [ ] Test: Display in terminal, verify ASCII renders correctly

**Reference**: Complete copy in `02-resources/complete-specification.md` lines 9-74

**Validation**:
```bash
# Test rendering
cat .claude/hooks/templates/startup_first_run.md

# Expected: Heroic intro with ASCII art, real stories, personality
```

---

#### Task 5: Add Language Selection

**File**: `.claude/hooks/templates/startup_first_run.md` (after heroic intro)

**Steps**:
- [ ] Add language selection screen after heroic intro
- [ ] Add options 1-7 (English, Deutsch, Español, Français, Italiano, 日本語, 中文)
- [ ] Add option 8: "Other (type your language)"
- [ ] Add instruction: "(All future sessions will use this language)"
- [ ] Add logic: If 8 selected → ask for custom language
- [ ] Add state update: `onboarding.language_preference = <selected>`
- [ ] Test: Select each option, verify state saves

**Reference**: Language selection in `02-resources/complete-specification.md` lines 76-105

**Validation**:
```bash
# Test flow
# Expected: Can select 1-7 (predefined) or 8 (custom input)
# State saves to user-config.yaml
```

---

#### Task 6: Add Fork Decision

**File**: `.claude/hooks/templates/startup_first_run.md` (after language)

**Steps**:
- [ ] Add fork decision screen after language selection
- [ ] Add option 1: "Show me how Nexus works (~7 min guided tour)"
- [ ] Add option 2: "Set up my system now (skip tour, dive in)"
- [ ] Add routing logic:
  - [ ] If 1: Set chosen_path="tour", load how-nexus-works
  - [ ] If 2: Set chosen_path="direct", load setup-system
- [ ] Add state updates: `onboarding.chosen_path` and `onboarding.status`
- [ ] Test: Both paths route correctly

**Reference**: Fork decision in `02-resources/complete-specification.md` lines 107-141

**Validation**:
```bash
# Test both paths
# Path 1: Loads how-nexus-works skill
# Path 2: Loads setup-system skill
```

---

### CHECKPOINT 1 VALIDATION

**Before marking complete, verify**:

- [ ] **Skill Loading**: Both skills load without errors
  ```bash
  python 00-system/core/nexus-loader.py --skill how-nexus-works
  python 00-system/core/nexus-loader.py --skill setup-system
  ```

- [ ] **Heroic Intro**: Displays correctly with ASCII art, real stories, personality

- [ ] **Language Selection**: Can select 1-8, saves to user-config.yaml

- [ ] **Fork Decision**: Routes to correct skill based on choice

- [ ] **Content Quality**: Read through all content, verify tone and clarity

**Checkpoint 1 Complete**: Core content exists and is loadable ✓

---

## CHECKPOINT 2: State & SubAgents Work

**Goal**: Onboarding state persists across sessions. SubAgent file analysis works.

**Deliverables**:
- ✅ Session compaction mid-onboarding resumes correctly
- ✅ State transitions validated (tour_complete → setup, etc.)
- ✅ SubAgent KB-based assignment works
- ✅ File analysis produces quality output

**Estimated Time**: 6-8 hours

---

### Phase 3: State & Infrastructure (Priority 2)

#### Task 7: Update user-config.yaml Schema

**File**: `00-system/core/nexus/templates/user-config.yaml`

**Steps**:
- [ ] Add `onboarding.language_preference` field (null | "en" | "de" | ...)
- [ ] Add `onboarding.chosen_path` field (null | "tour" | "direct")
- [ ] Add `onboarding.in_progress_skill` field (null | "how-nexus-works" | "setup-system")
- [ ] Add `onboarding.setup_system_state` object with 8 fields:
  - [ ] step_completed: 0
  - [ ] files_uploaded: false
  - [ ] file_analysis_done: false
  - [ ] role_captured: false
  - [ ] goals_captured: false
  - [ ] roadmap_created: false
  - [ ] workspace_created: false
  - [ ] projects_initiated: false
- [ ] Add `learning_tracker.completed.how_nexus_works: false`
- [ ] Add `learning_tracker.completed.create_roadmap: false`
- [ ] Update status enum to include all 7 values
- [ ] Test: Verify schema valid, defaults load

**Reference**: Complete schema in `02-resources/complete-specification.md` lines 1260-1304

**Validation**:
```bash
# Verify template is valid YAML
python -c "import yaml; yaml.safe_load(open('00-system/core/nexus/templates/user-config.yaml'))"

# Expected: No errors
```

---

#### Task 8: Implement SessionStart Onboarding Resume

**File**: `.claude/hooks/session_start.py`

**Steps**:
- [ ] Add `determine_onboarding_action()` function
- [ ] Check for `in_progress_skill` (cross-session continuity)
- [ ] If setup-system: Resume from `step_completed + 1`
- [ ] If how-nexus-works: Resume skill normally
- [ ] Route based on `onboarding.status`:
  - [ ] "not_started" → show_heroic_intro()
  - [ ] "tour_complete" → load_setup_system_mandatory()
  - [ ] "system_setup_complete" → show_roadmap_and_suggest_first_build()
  - [ ] "complete" → normal_menu()
- [ ] Add onboarding resume mode to context builder
- [ ] Create new template: `compact_onboarding_resume.md`
- [ ] Test: Session compaction mid-setup-system resumes correctly

**Reference**: Resume logic in `02-resources/complete-specification.md` lines 1308-1393

**Validation**:
```bash
# Test scenario:
# 1. Start setup-system
# 2. Complete Step 2
# 3. Force session compaction
# 4. Resume

# Expected: Resumes at Step 3, has all context
```

---

#### Task 9: Add Onboarding Project Auto-Creation

**File**: `00-system/skills/learning/setup-system/SKILL.md` (pre-execution)

**Steps**:
- [ ] Add pre-execution function `initialize_setup_system()`
- [ ] Create folder: `02-builds/00-onboarding-session/01-planning/`
- [ ] Create folder: `02-builds/00-onboarding-session/02-resources/`
- [ ] Create folder: `02-builds/00-onboarding-session/03-working/`
- [ ] Create folder: `02-builds/00-onboarding-session/04-outputs/`
- [ ] Create file: `01-planning/01-overview.md` with purpose
- [ ] Create file: `01-planning/04-steps.md` with 7-step checklist
- [ ] Create symlink: `03-working/input/ → 04-workspace/input/`
- [ ] Set active build to "00-onboarding-session"
- [ ] Test: Pre-execution creates structure correctly

**Reference**: Pre-execution in `02-resources/complete-specification.md` lines 307-367

**Validation**:
```bash
# After loading setup-system skill
ls -la 02-builds/00-onboarding-session/

# Expected: 4 folders + 2 files created
```

---

### Phase 4: SubAgent Logic (Priority 2)

#### Task 10: Implement KB-based Agent Assignment

**File**: `00-system/skills/learning/setup-system/SKILL.md` (Step 1 logic)

**Steps**:
- [ ] Add function `calculate_agent_count(total_kb)`
- [ ] Implement formula:
  ```python
  if total_kb < 1000: agent_count = 1
  elif total_kb < 3000: agent_count = 2
  elif total_kb < 5000: agent_count = 3
  elif total_kb < 10000: agent_count = 5
  elif total_kb < 20000: agent_count = 8
  else: agent_count = min(ceil(total_kb / 2500), 10)
  ```
- [ ] Add logic to scan `04-workspace/input/` and calculate total KB
- [ ] Add logic to distribute files to agents (balance KB)
- [ ] Test with various file sizes (10KB, 1MB, 5MB, 20MB)

**Reference**: KB calculation in `02-resources/complete-specification.md` lines 470-486

**Validation**:
```bash
# Test cases:
# 500 KB total → 1 agent
# 2 MB total → 2 agents
# 8 MB total → 5 agents
# 25 MB total → 10 agents
```

---

#### Task 11: Implement Auto-File-Splitting

**File**: `00-system/skills/learning/setup-system/SKILL.md` (Step 1 logic)

**Steps**:
- [ ] Add function `split_file_into_chunks(file_path, max_kb=1500, overlap_lines=50)`
- [ ] Detect files >2MB
- [ ] Split into chunks with overlap for context preservation
- [ ] Track chunks as separate "files" for SubAgent assignment
- [ ] Mark chunks with `is_chunk: true` flag
- [ ] Test with large PDFs and spreadsheets

**Reference**: Auto-splitting in `02-resources/complete-specification.md` lines 417-430

**Validation**:
```bash
# Test with 5MB PDF
# Expected: Split into 3-4 chunks, each <2MB with overlap
```

---

#### Task 12: Implement Thematic Clustering

**File**: `00-system/skills/learning/setup-system/SKILL.md` (Step 1 logic)

**Steps**:
- [ ] Add function `cluster_files_by_theme(files)`
- [ ] Implement pattern matching:
  - [ ] "client" or "customer" → "clients"
  - [ ] "sales" or "proposal" → "sales"
  - [ ] "research" or "paper" → "research"
  - [ ] "financial" or "invoice" → "finance"
  - [ ] Code extensions (.py, .js, .ts) → "code"
  - [ ] Default → "general"
- [ ] Show clusters to user for confirmation
- [ ] Allow user to suggest different clustering
- [ ] Test with mixed file types

**Reference**: Clustering in `02-resources/complete-specification.md` lines 436-469

**Validation**:
```bash
# Test with:
# - 3 client files
# - 2 sales files
# - 1 research file

# Expected: 3 clusters (clients, sales, research)
```

---

#### Task 13: Create Synthesis Logic

**File**: `00-system/skills/learning/setup-system/SKILL.md` (Step 1 logic)

**Steps**:
- [ ] Add function `synthesize_agent_results(results)`
- [ ] Combine all `file_analyses` arrays
- [ ] Merge `professional_context` (take most detailed for each field)
- [ ] Dedupe `integration_opportunities` by (name, type)
- [ ] Merge `workspace_structure_suggestion` folders (dedupe by path)
- [ ] Save unified result to `02-builds/00-onboarding-session/02-resources/file-analysis.json`
- [ ] Generate human-readable summary → `file-analysis-summary.md`
- [ ] Test with 2-3 agent results

**Reference**: Synthesis in `02-resources/complete-specification.md` lines 533-607

**Validation**:
```bash
# Mock 2 agent results
# Expected: Unified JSON with deduped integrations, merged contexts
```

---

### CHECKPOINT 2 VALIDATION

**Before marking complete, verify**:

- [ ] **Cross-Session Resume**: Start setup-system → compact mid-step → resume correctly

- [ ] **State Transitions**: Test all status transitions
  ```
  not_started → tour_in_progress → tour_complete → setup_in_progress → system_setup_complete
  ```

- [ ] **SubAgent Assignment**: Test with various KB sizes, verify correct agent count

- [ ] **File Splitting**: Test with >2MB file, verify chunks created with overlap

- [ ] **Clustering**: Test with mixed files, verify correct theme assignment

- [ ] **Synthesis**: Test with multiple agent outputs, verify deduping and merging

**Checkpoint 2 Complete**: State management and SubAgent logic work ✓

---

## CHECKPOINT 3: Complete & Tested

**Goal**: Full end-to-end onboarding tested and ready to ship.

**Deliverables**:
- ✅ Project scaffolding works
- ✅ All 3 paths tested (tour, direct, with files)
- ✅ Edge cases handled
- ✅ Documentation updated
- ✅ Ready for production

**Estimated Time**: 3-4 hours

---

### Phase 5: Project Scaffolding (Priority 3)

#### Task 14: Implement Full Scaffold Creation

**File**: `00-system/skills/learning/setup-system/SKILL.md` (Step 5 logic)

**Steps**:
- [ ] Add function `initiate_projects(roadmap, goals, file_analysis)`
- [ ] For each roadmap item:
  - [ ] Generate project_id (e.g., "01-sales-playbook")
  - [ ] Create 4 folders (01-planning, 02-resources, 03-working, 04-outputs)
  - [ ] Create empty templates (discovery.md, plan.md, steps.md)
  - [ ] Create resume-context.md with dependencies
- [ ] Test with 3-item roadmap

**Reference**: Scaffolding in `02-resources/complete-specification.md` lines 970-1020

**Validation**:
```bash
# After Step 5 complete
ls 02-builds/

# Expected: 01-item1/, 02-item2/, 03-item3/ with full structure
```

---

#### Task 15: Implement overview.md AI Generation

**File**: `00-system/skills/learning/setup-system/SKILL.md` (Step 5 logic)

**Steps**:
- [ ] Add function `generate_overview(item, goals, file_analysis)`
- [ ] AI generates:
  - [ ] Purpose (2-3 sentences from rationale)
  - [ ] Success criteria (3 measurable outcomes)
  - [ ] Context (relation to user goal + file insights)
- [ ] Include dependencies from roadmap
- [ ] Test AI generation quality with various item types

**Reference**: Overview generation in `02-resources/complete-specification.md` lines 1022-1088

**Validation**:
```bash
# Check quality of generated overview.md
cat 02-builds/01-item/01-planning/01-overview.md

# Expected: Specific, actionable, contextual
```

---

#### Task 16: Add Dependency Tracking

**File**: `00-system/skills/learning/setup-system/SKILL.md` (Step 3-5 logic)

**Steps**:
- [ ] In roadmap generation: Track dependencies between items
- [ ] In overview.md: Include dependencies section
- [ ] In resume-context.md: Mark dependent items
- [ ] Order roadmap by dependencies (foundational first)
- [ ] Test with 5-item roadmap with 2-3 dependencies

**Reference**: Dependencies in `02-resources/complete-specification.md` lines 827-864

**Validation**:
```bash
# Verify dependency order
# Item with dependencies should come AFTER its dependencies
```

---

### Phase 6: Testing & Polish (Priority 3)

#### Task 17: End-to-End Flow Testing

**Steps**:
- [ ] **Test Path A: Tour → Setup**
  - [ ] Fresh install → Heroic intro → Language (en) → Fork (1-Tour)
  - [ ] how-nexus-works loads → Complete 5 parts → Session ends
  - [ ] New session → setup-system auto-loads → Complete 7 steps
  - [ ] Verify: goals.md, roadmap.md, workspace-map.md created
  - [ ] Verify: Project scaffolds created

- [ ] **Test Path B: Direct Setup**
  - [ ] Fresh install → Heroic intro → Language (de) → Fork (2-Direct)
  - [ ] setup-system loads → Skip file upload → Complete 7 steps
  - [ ] Verify: Same outputs as Path A

- [ ] **Test Path C: Setup with File Upload**
  - [ ] Fresh install → Fork (2-Direct)
  - [ ] setup-system → Upload 5 files (2MB total)
  - [ ] SubAgent analysis runs (2 agents)
  - [ ] Verify: file-analysis.json created
  - [ ] Verify: Files organized into folders
  - [ ] Complete remaining steps

- [ ] **Test Session Boundaries**
  - [ ] Each skill ends with session boundary teaching
  - [ ] Verify message: "Open a NEW chat/session"
  - [ ] No "say close" messaging anywhere

**Validation Checklist**:
- [ ] All 3 paths complete without errors
- [ ] Time to complete <20 min for each path
- [ ] All expected files created
- [ ] Session boundary teaching displayed

---

#### Task 18: Edge Case Testing

**Steps**:
- [ ] **Session Compaction Mid-Setup**
  - [ ] Start setup-system → Complete Step 3
  - [ ] Force session compaction (or wait for auto-compact)
  - [ ] Resume → Verify starts at Step 4
  - [ ] Verify all state preserved

- [ ] **No Files Uploaded**
  - [ ] setup-system Step 1 → Choose "Skip"
  - [ ] Verify Step 2 continues normally
  - [ ] Verify workspace structure still generated (from roadmap themes)

- [ ] **User Modifies Roadmap**
  - [ ] setup-system Step 3 → AI suggests roadmap
  - [ ] User says "add item" or "remove item"
  - [ ] Verify changes applied correctly

- [ ] **Very Large File Upload**
  - [ ] Upload 25MB file
  - [ ] Verify auto-split into chunks
  - [ ] Verify 10 agents assigned
  - [ ] Verify synthesis works

- [ ] **Language: Other**
  - [ ] Language selection → Choose "8-Other"
  - [ ] Enter "Portuguese"
  - [ ] Verify saves to config
  - [ ] Verify subsequent messages respect preference

**Validation Checklist**:
- [ ] All edge cases handled gracefully
- [ ] No errors or crashes
- [ ] State always consistent

---

#### Task 19: Language Audit

**Steps**:
- [ ] **Remove "say close" everywhere**
  - [ ] Search codebase for "say close" or "say 'close'"
  - [ ] Replace all with "open a NEW chat/session"
  - [ ] Verify in: how-nexus-works, setup-system, templates

- [ ] **Verify "open NEW chat" messaging**
  - [ ] End of how-nexus-works skill
  - [ ] End of setup-system skill
  - [ ] End of first build (learn-builds)
  - [ ] Consistent phrasing everywhere

- [ ] **Era 3 Language Compliance**
  - [ ] "YOUR system" not "the system"
  - [ ] "You built" not "AI created"
  - [ ] "Build YOUR system" not "Get help"
  - [ ] Ownership language throughout

- [ ] **Test Translations** (if time permits)
  - [ ] Select German → Verify German responses
  - [ ] Select Spanish → Verify Spanish responses
  - [ ] Custom language → Verify Claude tries its best

**Validation Checklist**:
- [ ] No "say close" found
- [ ] All session ends have "open NEW chat" message
- [ ] Era 3 language used consistently
- [ ] Language preference respected

---

### Phase 7: Documentation & Launch (Priority 3)

#### Task 20: Update System Documentation

**Steps**:
- [ ] **Update skill catalog**
  - [ ] Add how-nexus-works to ONBOARDING_SKILLS in config.py
  - [ ] Add setup-system (replace old setup-memory, create-folders entries)
  - [ ] Remove create-roadmap as separate skill
  - [ ] Update orchestrator.md skill list

- [ ] **Update CLAUDE.md** (if needed)
  - [ ] Document onboarding changes
  - [ ] Update getting started section
  - [ ] Reference new skills

- [ ] **Create migration notes**
  - [ ] Document for existing users
  - [ ] Explain new onboarding flow
  - [ ] How to "reset onboarding" if desired

**Validation Checklist**:
- [ ] Skill catalog accurate
- [ ] CLAUDE.md updated
- [ ] Migration notes clear

---

#### Task 21: Verify Complete Specification

**Steps**:
- [ ] Read complete-specification.md
- [ ] Verify all components implemented
- [ ] Check for any missing pieces
- [ ] Update specification if needed

**Validation Checklist**:
- [ ] All 12 components from plan implemented
- [ ] Specification matches reality
- [ ] No discrepancies

---

#### Task 22: Final Validation

**Steps**:
- [ ] **Fresh Installation Test**
  - [ ] Delete 01-memory/user-config.yaml
  - [ ] Start new session
  - [ ] Complete full onboarding (choose Path A)
  - [ ] Measure time: Should be <20 min
  - [ ] Verify all outputs correct

- [ ] **User Acceptance**
  - [ ] Have creator (Dorian) test both paths
  - [ ] Collect feedback
  - [ ] Fix any issues

- [ ] **Performance Check**
  - [ ] SessionStart hook <200ms
  - [ ] SubAgent analysis reasonable time
  - [ ] No noticeable lag

**Validation Checklist**:
- [ ] Fresh install works perfectly
- [ ] Creator approves
- [ ] Performance acceptable
- [ ] Ready to ship ✓

---

### CHECKPOINT 3 VALIDATION

**Before marking complete, verify**:

- [ ] **Project Scaffolding**: Creates full structure with quality overview.md

- [ ] **All Paths Tested**: Tour, Direct, With Files all work end-to-end

- [ ] **Edge Cases**: Session compaction, no files, large files all handled

- [ ] **Language Audit**: No "say close", all "open NEW chat", Era 3 compliant

- [ ] **Documentation**: Skills cataloged, CLAUDE.md updated, migration notes written

- [ ] **Fresh Install**: Creator tests and approves

**Checkpoint 3 Complete**: Fully tested and ready to ship ✓

---

## Rollout Plan

Once all 3 checkpoints complete:

### Week 1: Internal Testing
- [ ] Deploy to internal test instance
- [ ] Have 2-3 team members complete onboarding
- [ ] Collect feedback
- [ ] Fix any issues

### Week 2: Soft Launch
- [ ] Deploy to new user signups only
- [ ] Monitor completion rates
- [ ] Watch for errors/crashes
- [ ] Iterate based on data

### Week 3: Full Rollout
- [ ] Deploy to all users
- [ ] Offer existing users "reset onboarding" option
- [ ] Monitor metrics:
  - [ ] Completion rate >90%
  - [ ] Time to complete <20 min
  - [ ] Return rate >80%

---

## Notes

**Session Management**:
- You can pause after any checkpoint and resume in a new session
- Each checkpoint is independently testable
- Mark tasks [x] as you complete them
- Update resume-context.md at each checkpoint

**Testing Strategy**:
- Test continuously during implementation (don't wait until end)
- Each task has validation steps
- Each checkpoint has comprehensive validation
- Fresh install test is final gate

**Quality Gates**:
- Checkpoint 1: Can load and display all content
- Checkpoint 2: State persistence and SubAgents work
- Checkpoint 3: Full tested and creator-approved

---

**Status**: Ready for Execution
**Next**: Start Checkpoint 1, Task 1 (Create how-nexus-works skill)
**Last Updated**: 2026-01-24
