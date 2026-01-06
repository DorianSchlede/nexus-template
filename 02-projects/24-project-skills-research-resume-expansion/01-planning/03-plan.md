# Project Skills Research & Resume Expansion - Plan

**Last Updated**: 2026-01-03

---

## Approach

**Strategy**: Extend existing project skills with two major enhancements:

### 1. Research Phase Integration (create-project)
Insert optional research phase BEFORE planning in create-project workflow:
- Create research template (`template-research.md`)
- Add research workflow step after `init_project.py`
- Research outputs go to `02-resources/research.md`
- **Research includes**: Codebase search + External (GitHub, web, paper-search skill)
- Findings pre-populate `plan.md` Dependencies section
- User can skip if not needed (greenfield projects)

### 2. Resume State Mechanism (execute-project + nexus-loader)
Enable robust continuation after session compaction (200k tokens):
- Create `_resume.md` as **LOADING MANIFEST + VALIDATION GATE** (NOT a summary!)
- **NO duplication** of content from other files - only loading instructions
- **CRITICAL**: Contains `files_to_load[]` and `next_action` fields
- **AUTO-UPDATED**: On every task completion inside execute-project (NO close-session!)
- **AUTO-CONTINUE**: After compaction, AI auto-continues (user does NOT trigger resume)
- Loader detects active project → loads _resume.md → enforces validation → auto-executes skill

**Implementation Path**:
```
Phase 1: Research Templates
├─ Create research.md template
├─ Update create-project workflow
└─ Test with new project creation

Phase 2: Resume State Structure
├─ Design _resume.md YAML schema
├─ Define state update triggers
└─ Document loading sequences

Phase 3: Loader Integration
├─ Update nexus-loader.py for resume mode
├─ Add auto-skill-load logic
└─ Test resume flow end-to-end

Phase 4: Skill Updates
├─ Update create-project skill docs
├─ Update execute-project with resume updates
└─ Add close-session integration
```

---

## Key Decisions

### **Research Phase: Optional vs Mandatory**
**Decision**: Make research phase OPTIONAL with intelligent prompting
**Rationale**:
- Not all projects need research (simple, greenfield projects)
- Offer based on project type and complexity
- Research adds 5-15 min to planning but prevents rework
- User retains control over workflow

### **Resume State: Loading Manifest vs Summary**
**Decision**: `_resume.md` is a **LOADING MANIFEST + VALIDATION GATE**, NOT a summary
**Rationale**:
- **NO duplication** of content from other files
- ONLY contains: `files_to_load[]`, `next_action`, validation questions, minimal state
- Purpose: Enforce intelligent loading after compaction, not to repeat information
- Always current (auto-updated on every task completion)
- Prevents continuing without proper context loading

### **Resume Auto-Update: Embedded in execute-project**
**Decision**: Auto-update `_resume.md` on EVERY task completion inside execute-project
**Rationale**:
- NO manual triggers needed (no "save progress", NO close-session!)
- Always current, never stale
- Embedded directly in execute-project workflow (update after marking task complete)
- After compaction → auto-continue with current _resume.md state
- Seamless, zero user intervention

### **Compaction Resume: Auto-Continue Flow**
**Decision**: After compaction, AI auto-continues (user does NOT say "continue project 24")
**Rationale**:
- Compaction summary includes reference to active project
- Loader auto-detects active project from summary
- Loads _resume.md automatically
- Enforces validation gate (AI must answer questions before continuing)
- Auto-executes skill specified in `next_action`
- Zero friction, seamless continuation

---

## Resources Needed

**Tools/Access**:
- Python 3.x (existing)
- Access to modify 00-system/ files (have it)
- Test projects for validation

**People/Expertise**:
- User (you) for requirements validation
- Testing with real project scenarios

**Information/Data**:
- Complete understanding of nexus-loader.py internals ✅ (from research)
- Understanding of create-project workflow ✅ (from research)
- Understanding of execute-project workflow ✅ (from research)
- Hook system integration points (session_start, close-session)

---

## Dependencies & Links

**Files Impacted**:

**create-project Skill**:
- `00-system/skills/projects/create-project/SKILL.md` - Add research phase docs
- `00-system/skills/projects/create-project/references/workflows.md` - Insert research step
- `00-system/skills/projects/create-project/scripts/templates/template-research.md` - NEW template

**execute-project Skill**:
- `00-system/skills/projects/execute-project/SKILL.md` - Add resume state docs
- `00-system/skills/projects/execute-project/references/workflow.md` - Add resume loading step

**nexus-loader Core**:
- `00-system/core/nexus-loader.py` - Add resume + project combined mode
- `00-system/core/nexus/service.py` - Update startup() for resume handling
- `00-system/core/nexus/loaders.py` - Update load_project() to check _resume.md
- `00-system/core/nexus/state.py` - Add resume state detection logic

**close-session Skill**:
- REMOVED - No longer needed, all resume updates happen inside execute-project

**External Systems**:
- None (internal Nexus changes only)

**Related Projects**:
- Project 14: Advanced Hook System - May integrate resume triggers with hooks
- Project 17: Hook Pattern Research - Resume state could use hook patterns

**Skills/Workflows**:
- `create-project` - Primary skill being enhanced (research phase)
- `execute-project` - Primary skill being enhanced (auto-update resume on task completion)

---

## Open Questions

- [x] Where should research phase be inserted in create-project? → After init_project.py, before overview.md
- [x] Should research be mandatory or optional? → Optional with intelligent prompting
- [x] Where to store resume state? → `01-planning/_resume.md`
- [x] How should loader know what to load on resume? → `files_to_load[]` array in _resume.md YAML
- [x] How to auto-execute correct skill? → `next_action` field in _resume.md tells loader which skill
- [ ] Should _resume.md be created on project init or first execution? → Decide during implementation
- [ ] What's the minimum viable resume state (MVP)? → Define core fields vs nice-to-have
- [ ] How to handle backward compatibility with existing projects? → Need migration strategy

---

## Mental Models Applied

**Systems Thinking**:
Applied to understand how changes propagate through the system:
- create-project → init_project.py → templates → file creation
- execute-project → nexus-loader → _resume.md → auto-load
- Identified feedback loops: resume state updates → better continuity → less re-work

**Second-Order Thinking**:
Considered consequences of consequences:
- Research phase → better planning → fewer mid-execution surprises → faster completion
- Resume state → seamless continuation → longer-running projects feasible → more complex work possible
- Auto-load logic → less user explanation needed → better UX → more adoption

**Pre-Mortem Analysis**:
Imagined failure modes:
- **Risk**: Resume state becomes stale
  - **Mitigation**: Auto-update on EVERY task completion (no manual triggers, always current)
- **Risk**: _resume.md files_to_load points to deleted files
  - **Mitigation**: Loader handles missing files gracefully, logs warning
- **Risk**: Research phase adds too much friction to simple projects
  - **Mitigation**: Make optional, offer intelligently based on project type
- **Risk**: AI continues without loading proper context after compaction
  - **Mitigation**: Validation gate - AI must answer questions before continuing

**MECE Principle** (Mutually Exclusive, Collectively Exhaustive):
Broke down implementation into non-overlapping phases:
- Phase 1: Research templates (create-project only)
- Phase 2: Resume state structure (minimal manifest, no duplication)
- Phase 3: Loader integration (auto-detection, validation gate)
- Phase 4: Skill updates (execute-project auto-update, remove close-session)

Each phase is independent, together they cover the full scope.

---

*Next: Complete steps.md to break down execution*
