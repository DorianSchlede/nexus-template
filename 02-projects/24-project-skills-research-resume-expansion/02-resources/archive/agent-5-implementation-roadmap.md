# Agent 5: Implementation Roadmap & Migration Guide

**Agent**: Implementation Roadmap Architect
**Date**: 2026-01-03
**Mission**: Complete implementation plan with dependencies, critical path, testing strategy, and rollback plans

---

## Executive Summary

This roadmap synthesizes outputs from Agents 1-4 into a complete implementation plan with:
- **Phase-by-phase execution** with clear dependencies
- **Critical path analysis** identifying bottlenecks and blockers
- **Testing strategy** with checkpoints between phases
- **Rollback procedures** for safe reversion
- **Migration guide** for ~20 existing projects

**Estimated Timeline**: 3-5 implementation sessions
**Risk Level**: Medium (existing projects continue working, new features are additive)

---

## Critical Dependencies & Execution Order

### Dependency Graph

```
Phase 1: PreCompact Hook (Agent 1)
    ↓
Phase 2: SessionStart Hook (Agent 2)  ← DEPENDS ON Phase 1 output (precompact_state.json)
    ↓
Phase 3: Testing & Validation         ← DEPENDS ON Phases 1+2 working together
    ↓
Phase 4A: Research Templates (Agent 4)  ← INDEPENDENT, can run in parallel
Phase 4B: Loader Refactoring (Agent 3)  ← INDEPENDENT, can run after Phase 3
    ↓
Phase 5: Integration & End-to-End Testing
    ↓
Phase 6: Migration & Deployment
```

**Critical Path**: Phase 1 → Phase 2 → Phase 3 → Phase 5 (longest dependency chain)
**Parallel Work**: Phase 4A (Research Templates) can be done anytime after Phase 3
**Optimization**: Phase 4B (Loader Refactoring) should wait until hooks are stable

---

## Phase 1: PreCompact Hook Implementation

**Goal**: Implement transcript-based project detection and precompact_state.json output

**Dependencies**: None (starting point)

**Inputs**: Agent 1's design for transcript parsing and project detection

**Tasks**:
1. Update `.claude/hooks/save_resume_state.py` with transcript parsing logic
2. Implement `detect_active_project_from_transcript()` function
3. Add regex patterns for all tool call types (Read, Write, Edit, Bash, Skill)
4. Implement confidence scoring system (high/medium/low)
5. Create fallback chain (transcript → cache → filesystem)
6. Output `precompact_state.json` to `00-system/.cache/`

**Key Files Modified**:
- `.claude/hooks/save_resume_state.py` (REPLACE existing implementation)

**Testing Checkpoints**:
```bash
# 1. Test transcript parsing with mock transcript
python .claude/hooks/save_resume_state.py < test_precompact_input.json

# 2. Verify precompact_state.json created
cat 00-system/.cache/precompact_state.json

# 3. Verify JSON structure
jq . 00-system/.cache/precompact_state.json

# Expected output:
{
  "active_project": "24-project-skills-research-resume-expansion",
  "confidence": "high",
  "detection_method": "transcript",
  "last_skill": "execute-project",
  "phase": "execution",
  "timestamp": "2026-01-03T14:30:00"
}
```

**Success Criteria**:
- [ ] Transcript parsing correctly identifies project from Read/Write/Edit tool calls
- [ ] Confidence scoring works (high for explicit paths, medium for inferred, low for ambiguous)
- [ ] Fallback chain works when transcript parsing fails
- [ ] precompact_state.json created with correct schema
- [ ] NO breaking changes to existing functionality

**Rollback Plan**:
```bash
# If Phase 1 breaks PreCompact hook:
git checkout .claude/hooks/save_resume_state.py
# Restart Claude Code to reload hook
```

**Estimated Time**: 1-2 hours

---

## Phase 2: SessionStart Hook Enhancement

**Goal**: Inject MANDATORY file loading instructions based on precompact_state.json

**Dependencies**:
- **CRITICAL**: Phase 1 MUST be complete (requires precompact_state.json)
- SessionStart hook must be able to read precompact_state.json

**Inputs**:
- Agent 2's design for SessionStart hook enhancement
- `precompact_state.json` from Phase 1

**Tasks**:
1. Read existing `.claude/hooks/session_start.py` (line 206 insertion point)
2. Add precompact_state.json detection logic
3. Implement _resume.md file loading
4. Create CATASTROPHIC instruction template with emoji warnings
5. Inject mandatory file list from `files_to_load[]` array
6. Add validation gate enforcement
7. Error handling for missing files/projects

**Key Files Modified**:
- `.claude/hooks/session_start.py` (INSERT after line 206)

**Code Insertion Point** (after line 206):
```python
# After line 206 in session_start.py:
# full_context = load_full_startup_context(project_dir)
# context["nexus_data"] = full_context

# INSERT HERE:
# Check for precompact_state.json and inject resume instructions
precompact_state_file = Path(project_dir) / "00-system" / ".cache" / "precompact_state.json"
if precompact_state_file.exists():
    try:
        precompact_data = json.loads(precompact_state_file.read_text(encoding="utf-8"))
        active_project = precompact_data.get("active_project")

        if active_project:
            # Load _resume.md
            resume_file = Path(project_dir) / "02-projects" / active_project / "01-planning" / "_resume.md"

            if resume_file.exists():
                # Parse YAML frontmatter for files_to_load
                resume_content = resume_file.read_text(encoding="utf-8")

                # Inject MANDATORY loading instructions
                mandatory_instructions = f"""
🚨🚨🚨 CATASTROPHIC ERROR PREVENTION 🚨🚨🚨

ACTIVE PROJECT DETECTED: {active_project}

YOU MUST IMMEDIATELY:
1. Read {resume_file} FIRST
2. Load ALL files listed in files_to_load[] (in parallel)
3. Answer ALL validation questions before continuing
4. Execute the skill specified in next_action

IF YOU DO NOT FOLLOW THESE STEPS, YOU WILL BREAK THE PROJECT.
THIS IS NOT OPTIONAL. THIS IS MANDATORY.

Resume file: {resume_file}
"""
                context["nexus_data"]["resume_instructions"] = mandatory_instructions
                context["nexus_data"]["active_project"] = active_project
                context["nexus_data"]["resume_file"] = str(resume_file)

    except Exception as e:
        # Graceful degradation - don't break session if resume detection fails
        pass
```

**Testing Checkpoints**:
```bash
# 1. Simulate PreCompact by creating precompact_state.json
echo '{"active_project":"24-project-skills-research-resume-expansion","confidence":"high"}' > 00-system/.cache/precompact_state.json

# 2. Restart Claude Code session (triggers SessionStart hook)

# 3. Verify instructions injected
cat 00-system/.cache/session_start_output.log | grep -A 10 "CATASTROPHIC"

# 4. Check that resume_instructions present in context
cat 00-system/.cache/context_startup.json | jq '.nexus_data.resume_instructions'

# Expected: Should see CATASTROPHIC ERROR PREVENTION message
```

**Success Criteria**:
- [ ] SessionStart hook reads precompact_state.json
- [ ] _resume.md file detected and parsed
- [ ] MANDATORY loading instructions injected into context
- [ ] Instructions include files_to_load[], validation gate, next_action
- [ ] Error handling prevents session crash if resume detection fails
- [ ] NO breaking changes to existing startup flow

**Rollback Plan**:
```bash
# If Phase 2 breaks SessionStart:
git checkout .claude/hooks/session_start.py

# Delete problematic precompact_state.json
rm 00-system/.cache/precompact_state.json

# Restart Claude Code
```

**Estimated Time**: 2-3 hours

---

## Phase 3: Testing & Validation (Phases 1+2 Together)

**Goal**: Validate complete PreCompact → SessionStart flow end-to-end

**Dependencies**:
- Phase 1 complete
- Phase 2 complete

**Test Scenarios**:

### Scenario 1: Normal Project Resume
```bash
# Setup
1. Start with Project 24 loaded
2. Simulate work (read/write some files)
3. Manually trigger PreCompact hook (or wait for 200k tokens)
4. Verify precompact_state.json created
5. Restart session (triggers SessionStart)
6. Verify CATASTROPHIC instructions appear
7. Verify files loaded correctly
8. Continue work seamlessly
```

### Scenario 2: No Active Project
```bash
# Setup
1. Start fresh session with NO project loaded
2. Trigger PreCompact
3. Verify precompact_state.json shows no active project
4. Restart session
5. Verify NO CATASTROPHIC instructions (normal startup)
```

### Scenario 3: Missing _resume.md
```bash
# Setup
1. Delete Project 24's _resume.md
2. Load Project 24
3. Trigger PreCompact
4. Restart session
5. Verify graceful degradation (warning, not crash)
6. Verify fallback to normal project loading
```

### Scenario 4: Corrupted precompact_state.json
```bash
# Setup
1. Manually corrupt precompact_state.json (invalid JSON)
2. Restart session
3. Verify SessionStart doesn't crash
4. Verify fallback to normal startup
```

**Testing Checklist**:
- [ ] PreCompact hook creates valid precompact_state.json
- [ ] SessionStart hook reads precompact_state.json
- [ ] CATASTROPHIC instructions injected for active project
- [ ] Files loaded from files_to_load[] array
- [ ] Validation gate enforced (AI reads validation questions)
- [ ] next_action skill auto-executed
- [ ] Graceful degradation for missing/corrupt files
- [ ] NO breaking changes to existing projects
- [ ] Performance acceptable (< 2 seconds for hook execution)

**Success Criteria**:
- [ ] All 4 test scenarios pass
- [ ] No crashes or errors in normal flow
- [ ] Graceful degradation in error scenarios
- [ ] Resume flow is seamless and automatic

**Rollback Plan**:
```bash
# If Phase 3 reveals critical bugs:
git checkout .claude/hooks/save_resume_state.py
git checkout .claude/hooks/session_start.py
rm 00-system/.cache/precompact_state.json
# Restart Claude Code
```

**Estimated Time**: 2-3 hours

---

## Phase 4A: Research Templates (Agent 4)

**Goal**: Create research template system for different project types

**Dependencies**: None (INDEPENDENT - can run in parallel)

**Inputs**: Agent 4's design for research template variants

**Tasks**:
1. Create `00-system/skills/projects/create-project/scripts/templates/template-research-build.md`
2. Create `00-system/skills/projects/create-project/scripts/templates/template-research-analysis.md`
3. Create `00-system/skills/projects/create-project/scripts/templates/template-research-simple.md`
4. Add template selection logic to create-project workflow
5. Update `00-system/skills/projects/create-project/SKILL.md` with research phase docs
6. Update `00-system/skills/projects/create-project/references/workflows.md`

**Key Files Created**:
- `template-research-build.md` (for implementation projects)
- `template-research-analysis.md` (for research/analysis projects)
- `template-research-simple.md` (for greenfield projects)

**Key Files Modified**:
- `00-system/skills/projects/create-project/SKILL.md`
- `00-system/skills/projects/create-project/references/workflows.md`

**Template Structure** (example for build template):
```markdown
# {Project Name} - Research

## Codebase Analysis
**Search Patterns**: [What to grep for]
**Files to Review**: [What to read]
**Dependencies**: [What files/skills are involved]

## External Research
**GitHub**: [Relevant repositories]
**Documentation**: [API docs, library docs]
**Papers**: [Academic papers if relevant]

## Integration Points
**Skills**: [What skills can be reused]
**Integrations**: [What external services involved]
**Configurations**: [What configs need updating]

## Findings Summary
[Key insights to inform planning]
```

**Testing Checkpoints**:
```bash
# 1. Test template creation
python 00-system/skills/projects/create-project/scripts/init_project.py --type Build --name "Test Project"

# 2. Verify research template offered
# (Manual test - run create-project skill)

# 3. Verify research findings populate plan.md Dependencies
# (Manual test - complete research phase)
```

**Success Criteria**:
- [ ] 3 research templates created (build, analysis, simple)
- [ ] Template selection logic works based on project type
- [ ] Research phase is optional (user can skip)
- [ ] Research findings correctly populate plan.md Dependencies section
- [ ] Documentation updated with research phase workflow

**Rollback Plan**:
```bash
# If research templates cause issues:
rm 00-system/skills/projects/create-project/scripts/templates/template-research-*.md
git checkout 00-system/skills/projects/create-project/SKILL.md
git checkout 00-system/skills/projects/create-project/references/workflows.md
```

**Estimated Time**: 1-2 hours

---

## Phase 4B: Loader Refactoring (Agent 3)

**Goal**: Remove --resume flag and simplify loader (optional optimization)

**Dependencies**:
- Phase 3 complete (hooks must be stable)
- Recommended: Wait until Phases 1-3 proven in production

**Inputs**: Agent 3's design for loader simplification

**Rationale**:
- Since SessionStart hook now handles resume detection automatically
- The `--resume` flag becomes redundant
- Simplification reduces complexity and maintenance burden

**Tasks**:
1. Remove `--resume` flag from `nexus-loader.py` CLI
2. Remove resume_mode parameter from `nexus/service.py` startup()
3. Update CLI help text
4. Add deprecation warnings (if keeping flag for backward compatibility)
5. Update documentation

**Key Files Modified**:
- `00-system/core/nexus-loader.py`
- `00-system/core/nexus/service.py`
- `00-system/core/nexus/loaders.py`

**Approach**: DEPRECATION FIRST (safer than immediate removal)

**Phase 4B-1: Add Deprecation Warnings**
```python
# In nexus-loader.py
if args.resume:
    print("WARNING: --resume flag is deprecated. Resume is now handled automatically by SessionStart hook.", file=sys.stderr)
    print("This flag will be removed in the next version.", file=sys.stderr)
    # Continue with normal behavior (ignore flag)
```

**Phase 4B-2: Remove Flag (after 1-2 weeks)**
```python
# Remove --resume from argparse
# Remove resume_mode parameter from startup()
# Update all documentation
```

**Testing Checkpoints**:
```bash
# 1. Test loader without --resume flag
python 00-system/core/nexus-loader.py --project 24

# 2. Test with --resume flag (should warn)
python 00-system/core/nexus-loader.py --resume --project 24
# Expected: Warning message, but still works

# 3. Verify documentation updated
grep -r "\-\-resume" 00-system/documentation/
# Expected: No references (or only in migration notes)
```

**Success Criteria**:
- [ ] --resume flag deprecated with warnings
- [ ] All functionality works without --resume
- [ ] Documentation updated
- [ ] Backward compatibility maintained during deprecation period
- [ ] NO breaking changes to existing workflows

**Rollback Plan**:
```bash
# If refactoring breaks loader:
git checkout 00-system/core/nexus-loader.py
git checkout 00-system/core/nexus/service.py
git checkout 00-system/core/nexus/loaders.py
```

**Estimated Time**: 1-2 hours (deprecation), 1 hour (removal after testing period)

**RECOMMENDATION**: Wait 1-2 weeks after Phase 3 deployment before starting Phase 4B

---

## Phase 5: Integration & End-to-End Testing

**Goal**: Validate complete system with real-world scenarios

**Dependencies**:
- Phase 1 complete
- Phase 2 complete
- Phase 3 complete
- Phase 4A complete (if doing research templates)

**Test Scenarios**:

### Scenario 1: New Project with Research Phase
```bash
# 1. Create new project
python 00-system/core/nexus-loader.py --skill create-project

# 2. Select "Build" type
# 3. Choose to include research phase
# 4. Complete research (codebase + external)
# 5. Verify research findings populate plan.md
# 6. Complete planning
# 7. Verify _resume.md created
# 8. Start execution
# 9. Complete 5 tasks
# 10. Verify _resume.md updated with current_task
# 11. Simulate compaction (trigger PreCompact hook)
# 12. Restart session
# 13. Verify seamless continuation from task 6
```

### Scenario 2: Existing Project Resume
```bash
# 1. Load existing project (e.g., Project 24)
# 2. Complete some tasks
# 3. Verify _resume.md updated
# 4. Simulate compaction
# 5. Restart session
# 6. Verify CATASTROPHIC instructions appear
# 7. Verify files loaded correctly
# 8. Continue from correct task
```

### Scenario 3: Multiple Session Cycles
```bash
# 1. Start Project 24
# 2. Complete 3 tasks
# 3. Compact
# 4. Resume (should continue at task 4)
# 5. Complete 3 more tasks
# 6. Compact again
# 7. Resume (should continue at task 7)
# 8. Verify no degradation over multiple cycles
```

### Scenario 4: Error Recovery
```bash
# 1. Delete _resume.md mid-session
# 2. Complete tasks (should create new _resume.md)
# 3. Compact
# 4. Resume (should work with newly created _resume.md)
```

**Performance Benchmarks**:
- [ ] PreCompact hook executes in < 500ms
- [ ] SessionStart hook executes in < 2 seconds
- [ ] Resume detection accuracy > 95%
- [ ] Zero crashes in normal operation
- [ ] Graceful degradation in error cases

**Success Criteria**:
- [ ] All 4 scenarios pass
- [ ] Performance benchmarks met
- [ ] No breaking changes to existing projects
- [ ] Resume flow is seamless and invisible to user
- [ ] Documentation is complete and accurate

**Rollback Plan**:
```bash
# If integration testing reveals critical issues:
git checkout .claude/hooks/save_resume_state.py
git checkout .claude/hooks/session_start.py
git checkout 00-system/skills/projects/create-project/
rm 00-system/.cache/precompact_state.json
# Restart Claude Code
```

**Estimated Time**: 3-4 hours

---

## Phase 6: Migration & Deployment

**Goal**: Migrate existing projects and deploy to production

**Dependencies**: Phase 5 complete (all testing passed)

**Migration Strategy**: ZERO BREAKING CHANGES

**Existing Projects Status**:
```bash
# Count existing projects
ls -1 02-projects/ | wc -l
# Output: ~20 projects

# Check which have _resume.md
find 02-projects/ -name "_resume.md" | wc -l
# Output: Currently only Project 24
```

**Migration Approach**: OPT-IN (no forced migration)

### Migration Option 1: Automatic (Recommended)
**When**: First time execute-project runs on existing project
**Action**: Auto-create _resume.md with sensible defaults
**Risk**: Low (new file, no changes to existing files)

```python
# In execute-project skill:
if not _resume_file_exists():
    create_initial_resume_md(
        project_id=project_id,
        phase=detect_current_phase(),  # research/planning/execution
        files_to_load=get_default_files_for_phase()
    )
```

### Migration Option 2: Manual (Optional)
**When**: User explicitly requests migration
**Action**: Run migration script to add _resume.md to all projects

```bash
# Migration script (optional, for power users)
python 00-system/scripts/migrate_projects_add_resume.py

# Dry run first
python 00-system/scripts/migrate_projects_add_resume.py --dry-run

# Actual migration
python 00-system/scripts/migrate_projects_add_resume.py --execute
```

### Migration Option 3: Do Nothing (Default)
**When**: User never runs execute-project on old projects
**Action**: Nothing (projects continue working without _resume.md)
**Risk**: Zero (backward compatibility maintained)

**Recommended Approach**: Option 1 (Automatic on first use)

**Migration Checklist**:
- [ ] Create migration script (optional)
- [ ] Test migration on 1 project first
- [ ] Verify migrated project works with resume flow
- [ ] Verify unmigrated projects still work (backward compatibility)
- [ ] Document migration process
- [ ] Update CHANGELOG.md

**Deployment Steps**:
1. **Pre-Deployment**:
   ```bash
   # Create git checkpoint
   git add .
   git commit -m "feat: Add resume state system with PreCompact/SessionStart hooks"
   git tag v1.0-resume-system
   ```

2. **Deploy Hooks**:
   ```bash
   # Hooks are automatically loaded by Claude Code
   # No deployment needed, just commit to git
   ```

3. **Deploy Templates**:
   ```bash
   # Research templates are automatically available
   # Test with new project creation
   ```

4. **Verify Deployment**:
   ```bash
   # 1. Check hooks loaded
   ls -la .claude/hooks/

   # 2. Check templates exist
   ls -la 00-system/skills/projects/create-project/scripts/templates/

   # 3. Test end-to-end
   # (Create new project, complete some work, trigger compaction, resume)
   ```

5. **Post-Deployment Monitoring**:
   ```bash
   # Monitor hook logs
   tail -f 00-system/.cache/session_start_output.log

   # Monitor precompact_state.json
   watch -n 5 cat 00-system/.cache/precompact_state.json
   ```

**Rollback Procedure** (if deployment fails):
```bash
# 1. Revert to checkpoint
git checkout v1.0-resume-system~1  # One commit before

# 2. Clean up cache
rm 00-system/.cache/precompact_state.json
rm 00-system/.cache/context_startup*.json

# 3. Restart Claude Code
# (Hooks will reload from git)

# 4. Verify rollback successful
# (Test normal project loading works)
```

**Success Criteria**:
- [ ] Migration completed for target projects
- [ ] All existing projects still work (backward compatibility)
- [ ] New projects use resume system by default
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Git tagged with version

**Estimated Time**: 2-3 hours

---

## Critical Path Analysis

### Longest Dependency Chain (Critical Path)
```
Phase 1 (2h) → Phase 2 (3h) → Phase 3 (3h) → Phase 5 (4h) → Phase 6 (3h) = 15 hours
```

### Bottlenecks
1. **Phase 2 depends on Phase 1** - Cannot parallelize
2. **Phase 3 depends on Phase 2** - Must test hooks together
3. **Phase 5 depends on all previous phases** - Final integration testing

### Parallel Opportunities
- **Phase 4A (Research Templates)** can be done anytime (2 hours saved if parallel)
- **Phase 4B (Loader Refactoring)** can be done after Phase 3 (optional, not on critical path)

### Optimized Timeline
```
Session 1 (4h): Phase 1 + Phase 2
Session 2 (5h): Phase 3 + Phase 4A (parallel)
Session 3 (4h): Phase 5
Session 4 (3h): Phase 6
Session 5 (2h): Phase 4B (optional cleanup)

Total: 15-18 hours across 4-5 sessions
```

---

## Testing Strategy

### Unit Testing (Per Phase)
Each phase has its own testing checkpoints (see individual phases above)

### Integration Testing (Phase 5)
- Test hooks together (PreCompact → SessionStart)
- Test with real projects (new and existing)
- Test error scenarios (missing files, corrupt data)

### Regression Testing (Ongoing)
```bash
# Test existing functionality still works
python 00-system/core/nexus-loader.py --project 24
python 00-system/core/nexus-loader.py --skill create-project

# Verify no breaking changes
python 00-system/tests/test_loader.py  # (if tests exist)
```

### User Acceptance Testing (UAT)
- Create new project with research phase
- Execute project to mid-point
- Trigger compaction
- Verify seamless resume
- User confirms experience is improved

---

## Rollback Strategy

### Per-Phase Rollbacks
See individual phases for specific rollback procedures.

### Complete System Rollback
```bash
# 1. Revert all hook changes
git checkout .claude/hooks/save_resume_state.py
git checkout .claude/hooks/session_start.py

# 2. Revert template changes
git checkout 00-system/skills/projects/create-project/

# 3. Clean up cache files
rm 00-system/.cache/precompact_state.json
rm 00-system/.cache/context_startup*.json

# 4. Remove _resume.md files (if causing issues)
find 02-projects/ -name "_resume.md" -type f -delete

# 5. Restart Claude Code
# (Hooks reload, system back to pre-implementation state)

# 6. Verify system operational
python 00-system/core/nexus-loader.py --project 24
```

### Rollback Safety
- **Git checkpoints** at each phase
- **Backup critical files** before modification
- **Graceful degradation** built into hooks (errors don't crash sessions)
- **Backward compatibility** maintained (old projects still work)

### Rollback Testing
Before starting implementation:
```bash
# 1. Create backup branch
git checkout -b backup-pre-resume-system

# 2. Practice rollback on test branch
git checkout -b test-rollback
# ... make changes ...
git checkout backup-pre-resume-system
# ... verify system still works ...

# 3. Delete test branch
git branch -D test-rollback
```

---

## Migration Guide for Existing Projects

### Current State
- **20 existing projects** in `02-projects/`
- **Only Project 24** currently has `_resume.md`
- **All other projects** use legacy approach (no resume state)

### Migration Options

#### Option 1: Do Nothing (Backward Compatible)
**Projects without _resume.md continue working normally**
- No migration needed
- Resume system only activates when _resume.md exists
- Projects gradually migrate as they're worked on

**Pros**:
- Zero risk
- No user action required
- Graceful adoption

**Cons**:
- Resume system not available for old projects until first use

#### Option 2: Auto-Migrate on First Use (Recommended)
**When execute-project runs, auto-create _resume.md if missing**

**Implementation**:
```python
# In execute-project skill:
def ensure_resume_file(project_path, project_id):
    resume_file = project_path / "01-planning" / "_resume.md"

    if not resume_file.exists():
        # Auto-create minimal _resume.md
        phase = detect_current_phase(project_path)  # research/planning/execution

        content = f"""---
resume_version: 1.0
last_updated: {datetime.now().isoformat()}
project_id: {project_id}
current_phase: {phase}
next_action: execute-project
files_to_load:
  - 01-planning/overview.md
  - 01-planning/plan.md
  - 01-planning/steps.md
---

# Validation Gate

Before continuing, verify you understand:
1. What problem are we solving? (from overview.md)
2. What is next task? (from steps.md)
3. What is the approach? (from plan.md)

If cannot answer → re-read files_to_load
"""
        resume_file.write_text(content, encoding="utf-8")
        return True
    return False
```

**Pros**:
- Automatic, zero friction
- Resume system available immediately
- No breaking changes

**Cons**:
- Creates new file (minor)

#### Option 3: Batch Migration Script (Power Users)
**Run script to add _resume.md to all projects at once**

**Script**: `00-system/scripts/migrate_projects_add_resume.py`
```python
#!/usr/bin/env python3
"""
Batch migration script to add _resume.md to all existing projects.
"""

import sys
from pathlib import Path

def migrate_all_projects(dry_run=True):
    projects_dir = Path("02-projects")

    for project_dir in projects_dir.iterdir():
        if not project_dir.is_dir():
            continue

        planning_dir = project_dir / "01-planning"
        if not planning_dir.exists():
            continue

        resume_file = planning_dir / "_resume.md"
        if resume_file.exists():
            print(f"SKIP: {project_dir.name} (already has _resume.md)")
            continue

        if dry_run:
            print(f"WOULD CREATE: {resume_file}")
        else:
            # Create _resume.md (same as Option 2)
            print(f"CREATED: {resume_file}")

if __name__ == "__main__":
    dry_run = "--dry-run" in sys.argv
    migrate_all_projects(dry_run=dry_run)
```

**Usage**:
```bash
# Dry run first (see what would change)
python 00-system/scripts/migrate_projects_add_resume.py --dry-run

# Actual migration
python 00-system/scripts/migrate_projects_add_resume.py --execute
```

**Pros**:
- All projects migrated at once
- Consistent state across all projects
- User has full control

**Cons**:
- Requires manual action
- Higher risk (batch operation)

### Recommended Migration Path

**For Production**: Use **Option 2** (Auto-Migrate on First Use)

**Reasoning**:
- Zero user friction
- Gradual adoption
- Backward compatible
- Low risk

**For Power Users**: Optionally provide **Option 3** script

### Migration Testing

**Test Plan**:
1. **Test with unmigrated project**:
   ```bash
   # Load old project without _resume.md
   python 00-system/core/nexus-loader.py --project 07
   # Verify it works normally

   # Run execute-project
   python 00-system/core/nexus-loader.py --skill execute-project
   # Verify _resume.md auto-created

   # Trigger compaction
   # Restart session
   # Verify resume works
   ```

2. **Test with already-migrated project**:
   ```bash
   # Load Project 24 (already has _resume.md)
   python 00-system/core/nexus-loader.py --project 24
   # Verify existing _resume.md not overwritten
   ```

3. **Test backward compatibility**:
   ```bash
   # Delete _resume.md from Project 24
   rm 02-projects/24-project-skills-research-resume-expansion/01-planning/_resume.md

   # Load project
   python 00-system/core/nexus-loader.py --project 24
   # Verify it still works (fallback to normal loading)
   ```

### Migration Rollback

If migration causes issues:
```bash
# 1. Delete all auto-created _resume.md files
find 02-projects/ -name "_resume.md" -newer 2026-01-03 -type f -delete

# 2. Restore from git if needed
git checkout 02-projects/*/01-planning/_resume.md

# 3. Verify projects work normally
```

---

## Risk Assessment & Mitigation

### High-Risk Items
1. **PreCompact hook crashes** → Blocks all session compactions
   - **Mitigation**: Extensive error handling, graceful degradation
   - **Rollback**: Git revert hook, restart Claude Code

2. **SessionStart hook crashes** → Blocks all new sessions
   - **Mitigation**: Try/except around all resume detection logic
   - **Rollback**: Git revert hook, restart Claude Code

3. **Transcript parsing false positives** → Wrong project detected
   - **Mitigation**: Confidence scoring, fallback chain
   - **Testing**: Extensive testing with edge cases

### Medium-Risk Items
1. **_resume.md corruption** → Resume fails
   - **Mitigation**: YAML validation, fallback to normal loading
   - **Recovery**: Delete _resume.md, auto-recreate on next use

2. **files_to_load[] points to deleted files** → Load fails
   - **Mitigation**: Error handling, skip missing files
   - **Recovery**: Update _resume.md manually

3. **Performance degradation** → Hooks too slow
   - **Mitigation**: Benchmark testing, optimize regex patterns
   - **Acceptance**: < 2 seconds for SessionStart, < 500ms for PreCompact

### Low-Risk Items
1. **Research templates not used** → No impact
   - **Mitigation**: Make optional, user can skip
   - **Recovery**: N/A (feature can be ignored)

2. **Loader refactoring breaks CLI** → Users confused
   - **Mitigation**: Deprecation period with warnings
   - **Rollback**: Revert loader changes

---

## Success Metrics

### Functional Metrics
- [ ] **Resume accuracy**: > 95% correct project detection
- [ ] **Zero crashes**: No hook-related session crashes
- [ ] **Backward compatibility**: 100% of old projects still work
- [ ] **Auto-continue success**: > 90% successful resumes after compaction

### Performance Metrics
- [ ] **PreCompact hook**: < 500ms execution time
- [ ] **SessionStart hook**: < 2 seconds execution time
- [ ] **Resume detection**: < 100ms for transcript parsing
- [ ] **File loading**: < 1 second for typical files_to_load[]

### User Experience Metrics
- [ ] **Seamless resume**: User doesn't notice compaction happened
- [ ] **Zero manual triggers**: No "continue project X" needed
- [ ] **Research adoption**: > 50% of new projects use research phase
- [ ] **Documentation clarity**: Users can self-serve without asking questions

---

## Post-Implementation Maintenance

### Monitoring
```bash
# 1. Check hook logs daily
tail -f 00-system/.cache/session_start_output.log

# 2. Monitor precompact_state.json accuracy
cat 00-system/.cache/precompact_state.json

# 3. Track resume success rate
grep "CATASTROPHIC" 00-system/.cache/session_start_output.log | wc -l
```

### Debugging Common Issues

**Issue 1: Resume not working**
```bash
# Check precompact_state.json exists
cat 00-system/.cache/precompact_state.json

# Check _resume.md exists
ls -la 02-projects/*/01-planning/_resume.md

# Check SessionStart log
cat 00-system/.cache/session_start_output.log | grep -A 20 "CATASTROPHIC"
```

**Issue 2: Wrong project detected**
```bash
# Check transcript parsing
cat ~/.claude/projects/*/transcript.jsonl | grep "02-projects"

# Check confidence score
cat 00-system/.cache/precompact_state.json | jq '.confidence'

# If low confidence, check fallback chain worked
cat 00-system/.cache/precompact_state.json | jq '.detection_method'
```

**Issue 3: Files not loading**
```bash
# Check files_to_load array
cat 02-projects/*/01-planning/_resume.md | grep "files_to_load:" -A 5

# Verify files exist
for file in $(cat 02-projects/24-*/01-planning/_resume.md | grep "  -" | sed 's/  - //'); do
    ls -la "02-projects/24-*/$file"
done
```

### Version Updates

**When to update resume_version**:
- Schema changes (new fields added/removed)
- Breaking changes to validation gate
- Major refactoring

**Update procedure**:
```yaml
# In _resume.md template
resume_version: 1.1  # Increment minor version

# Add migration notes in code
if resume_version < 1.1:
    upgrade_resume_to_v1_1()
```

---

## Conclusion

This implementation roadmap provides:
- **Clear execution order** with dependency tracking
- **Testing checkpoints** at every phase
- **Rollback procedures** for safe reversion
- **Migration guide** for existing projects
- **Risk mitigation** strategies
- **Success metrics** for validation

**Total Implementation Time**: 15-18 hours across 4-5 sessions
**Risk Level**: Medium (mitigated by extensive testing and rollback plans)
**Impact**: High (enables seamless long-running projects across compaction boundaries)

**Next Steps**:
1. Review this roadmap with stakeholders
2. Begin Phase 1 (PreCompact Hook) implementation
3. Checkpoint at each phase completion
4. Celebrate when complete!

---

**Roadmap Status**: Ready for implementation
**Last Updated**: 2026-01-03
**Agent**: Implementation Roadmap Architect (Agent 5)
