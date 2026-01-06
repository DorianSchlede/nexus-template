# Final Design - Project Skills Research & Resume Expansion

**Date**: 2026-01-03
**Status**: Design Revised - Based on Cross-Validation Findings
**Revision**: v1.1 - Incorporates 11 CRITICAL issues from cross-reference agents

---

## ✅ CRITICAL FINDINGS - ALL RESOLVED

**11 CRITICAL issues identified** during cross-validation - **ALL RESOLVED** as of Session 9 (2026-01-04).
See **[implementation-blockers.md](implementation-blockers.md)** for resolution details.

**Key Schema Corrections** (IMPLEMENTED):
1. ✅ **precompact_state.json uses FLAT schema**: `active_project_id` (top-level) - Validated in Phase 0.3
2. ✅ **PreCompact hook returns `{}`** and writes to file - Understood for Phase 1 implementation
3. ✅ **Performance targets**: <50ms PreCompact, <200ms SessionStart - Documented in schemas
4. ✅ **Phase 0 (Schema Design) COMPLETE** - Sessions 8-9 (6h elapsed)
5. ✅ **execute-project integration** for research templates - Scoped for Phase 4A

**Phase 0 Status** (Session 9):
- [x] Phase 0.0: 3 validation blockers FIXED (25 min)
- [x] Phase 0.1: Schema documentation COMPLETE (2h)
- [x] Phase 0.2: Migration decision confirmed (Option B)
- [x] Phase 0.3: All 14 tests PASSING (3h)
- [x] Phase 0.4: 0 CRITICAL blockers found (1h)
- [ ] Phase 0.5: Documentation updates (in progress)
- [ ] Phase 0.6: Migration script (2h remaining)

---

## Critical Requirements (MANDATORY)

### 1. Research Phase
- **NOT just codebase** - includes external research:
  - Codebase: Grep, Glob, file reads
  - GitHub: gh CLI, web fetch
  - Web: WebSearch, WebFetch
  - Academic: paper-search skill
- **Optional**: User can skip for simple projects
- **Output**: `01-planning/research.md` (NOT 02-resources!) → feeds into `plan.md` Dependencies
- **Integration**: execute-project MUST read research.md and populate plan.md Dependencies section

**CORRECTED from cross-validation**: Research location is `01-planning/research.md` because it contains FINDINGS (planning artifact), not raw materials. Raw materials (papers, data) go to `02-resources/`.

### 2. Resume State (`resume-context.md`)

**NAMING DECISION** (Confirmed 2026-01-04): **`resume-context.md`** (NOT `_resume.md`)
- Clearer naming that reflects purpose (context loader, not resume)
- Requires migration of 20+ existing `_resume.md` files
- Migration strategy documented below

**CRITICAL UNDERSTANDING**:
```
resume-context.md = LOADING MANIFEST + VALIDATION GATE
resume-context.md ≠ Summary or duplicate content
```

**Purpose**:
- Tell loader EXACTLY what files to load after compaction
- Enforce validation before continuing (AI must answer questions)
- Minimal state only (no duplication of other files)

**Auto-Updated**:
- ✅ On EVERY task completion inside execute-project
- ✅ After section completion
- ✅ After phase transitions
- ❌ NO close-session (removed entirely!)
- ❌ NO manual "save progress" triggers

**Structure** (REVISED based on schema validation):
```yaml
---
# LOADING MANIFEST
resume_schema_version: "1.0"  # Changed from resume_version
last_updated: "2026-01-03T14:30:00"

# PROJECT IDENTIFICATION
project_id: "24-project-skills-research-resume-expansion"
project_name: "Project Skills Research & Resume Expansion"  # NEW field
current_phase: execution  # research | planning | execution

# AUTO-LOAD INSTRUCTIONS
next_action: execute-project
files_to_load:
  - 01-planning/overview.md
  - 01-planning/plan.md
  - 01-planning/steps.md

# EXECUTION STATE (MINIMAL - NO DUPLICATION!)
current_section: 2
current_task: 15
progress: "14/40 tasks complete"
---

# Validation Gate

Before continuing, you MUST verify you understand:

1. **Project Purpose** (from [overview.md](overview.md)):
   - What problem are we solving?
   - What is the success criterion?

2. **Current Location** (from [steps.md](steps.md)):
   - What phase are we in?
   - What is the next task?

3. **Approach** (from [plan.md](plan.md)):
   - What is the implementation strategy?

**If you cannot answer these questions, STOP and re-read files_to_load.**

---

*This file is auto-updated on every task completion by execute-project skill.*
```

**Schema Validation** (Phase 0 Complete):
- ✅ **JSON Schema**: `00-system/.schemas/resume_context_v1.json` - Formal validation rules
- ✅ **Example File**: `02-resources/examples/example-resume-context.md` - Complete reference example
- ✅ **Test Coverage**: 14/14 tests passing (100%) - See `03-working/test-results.md`
- ✅ **Field Validation**: All 10 required fields validated (resume_schema_version, project_id, project_name, current_phase, next_action, files_to_load, current_section, current_task, progress, last_updated)

**Migration from `_resume.md`** (Phase 0.6):
- Current system has 20+ projects with `_resume.md` files
- Migration script created: `03-working/migrate_resume_files.py`
- Migration fixes applied in Session 8 (3 blockers resolved)
- Backward compatibility: SessionStart reads both `resume-context.md` and `_resume.md` during transition
- See FINAL-DESIGN lines 204-356 for migration script design

### 3. Auto-Continue After Compaction

**CORRECTED Flow** (based on hook-guides patterns):
1. Compaction happens at 200k tokens
2. **PreCompact hook fires** BEFORE compaction
   - Parses transcript JSONL for active project
   - Writes `00-system/.cache/precompact_state.json` with **FLAT schema** (validated in Phase 0.3)
     - ✅ **JSON Schema**: `00-system/.schemas/precompact_state_v1.json`
     - ✅ **Example File**: `02-resources/examples/example-precompact-state.json`
     - ✅ **FLAT Enforcement**: `active_project_id` at top level (NOT nested)
   - **MUST return `{}`** (empty object) - cannot inject context
   - **MUST execute in <50ms**
3. Conversation summarized
4. **SessionStart hook fires** on resume
   - Receives `source` field from Claude Code (`source: "resume"` or `"compact"`)
   - ✅ **Source Detection Validated**: Test 2 confirms `source="clear"` excluded
   - Reads `precompact_state.json` (if exists) using FLAT schema
   - Loads `resume-context.md` from detected project (falls back to `_resume.md` during migration)
   - **Injects CATASTROPHIC instructions** via `additionalContext`
   - **MUST execute in <200ms**
5. AI receives mandatory loading instructions
6. AI reads files from `files_to_load[]`
7. AI answers validation questions (gate enforcement)
8. AI auto-executes skill from `next_action`
9. Seamless continuation from exact point

**Key Architecture Correction** (from cross-reference-agent-3):
- Hooks **RECEIVE** `source` field from Claude Code (don't detect it from files)
- PreCompact writes state for **PROJECT detection** (not session source)
- SessionStart reads state for **resume context injection**

**No User Trigger Needed** - fully automatic!

---

## Implementation Phases (REVISED)

### Phase 0: Schema Design & Validation (NEW - CRITICAL)
**Time**: 2 hours
**Dependencies**: None
**Risk**: LOW
**Criticality**: CRITICAL (prevents rework)

**Goal**: Define all data contracts before implementation starts

**Tasks**:
1. Define precompact_state.json schema (**FLAT structure**)
   ```json
   {
     "active_project_id": "24-project-...",  // FLAT (not nested)
     "confidence": "high" | "medium" | "low",
     "detection_method": "transcript" | "cache" | "fallback",
     "timestamp": "2026-01-03T14:00:00"
   }
   ```
2. Define _resume.md YAML frontmatter schema
3. Create schema validation tests
4. Document data contracts:
   - Agent 1 (PreCompact) → precompact_state.json → Agent 2 (SessionStart)
   - Agent 4 (research.md) → execute-project → plan.md
   - execute-project → _resume.md (auto-update)

**Success Criteria**:
- [ ] Schemas documented with JSON Schema / YAML Schema
- [ ] Validation tests written and passing
- [ ] Agent 1 and Agent 2 designs updated to use flat schema
- [ ] No ambiguity in field names, types, or structure

**MUST COMPLETE BEFORE Phase 1**

---

### Phase 0.6: Migration Strategy for Existing Projects (NEW - CRITICAL)
**Time**: 2 hours (ADDED to Phase 0)
**Dependencies**: Phase 0.2 decision confirmed
**Risk**: MEDIUM (affects 20+ existing projects)
**Criticality**: HIGH (prevents broken projects)

**Goal**: Migrate existing `_resume.md` files to new `resume-context.md` schema without breaking projects

**Current State** (from codebase validation):
- 20+ projects have `_resume.md` files in `01-planning/`
- Current schema uses `resume_version`, lacks `project_name`, lacks validation gate
- Current PreCompact hook writes `_resume.md` (must be updated to write `resume-context.md`)
- Current SessionStart hook does NOT read `_resume.md` (new functionality)

**Migration Approach**:

**Phase 0.6a: Create Migration Script** (1 hour)
```python
# File: 02-projects/24-.../03-working/migrate_resume_files.py

def get_project_name(project_id):
    """Extract project name from overview.md with fallback."""
    overview_path = Path("02-projects") / project_id / "01-planning" / "overview.md"
    try:
        import frontmatter
        post = frontmatter.load(overview_path)
        return post.metadata.get("name", project_id.replace("-", " ").title())
    except Exception:
        # Fallback: convert project ID to title case
        return project_id.replace("-", " ").title()

def migrate_project_resume(project_path):
    """Migrate _resume.md → resume-context.md with schema updates."""
    old_file = project_path / "01-planning" / "_resume.md"
    new_file = project_path / "01-planning" / "resume-context.md"

    if not old_file.exists():
        return "SKIP: No _resume.md found"

    if new_file.exists():
        return "SKIP: resume-context.md already exists"

    # 1. Read old YAML frontmatter
    import frontmatter
    try:
        post = frontmatter.load(old_file)
        old_metadata = post.metadata
        old_body = post.content
    except Exception as e:
        return f"ERROR: Failed to parse {old_file}: {e}"

    # 2. Transform schema
    new_metadata = {
        "resume_schema_version": "1.0",  # NEW field
        "last_updated": old_metadata.get("updated", old_metadata.get("last_updated")),
        "project_id": old_metadata.get("project_id"),
        "project_name": get_project_name(old_metadata["project_id"]),  # NEW from overview.md
        "current_phase": old_metadata.get("phase", "execution"),
        "next_action": old_metadata.get("last_skill", "execute-project"),
        "files_to_load": old_metadata.get("files_to_load", [
            "01-planning/overview.md",
            "01-planning/plan.md",
            "01-planning/steps.md"
        ]),
        "current_section": old_metadata.get("current_section", 1),
        "current_task": old_metadata.get("current_task", 1),
        "progress": old_metadata.get("progress", "In progress")
    }

    # 3. Add validation gate if missing
    if "Validation Gate" not in old_body:
        validation_gate = """# Validation Gate

Before continuing, you MUST verify you understand:

1. **Project Purpose** (from [overview.md](overview.md)):
   - What problem are we solving?
   - What is the success criterion?

2. **Current Location** (from [steps.md](steps.md)):
   - What phase are we in?
   - What is the next task?

3. **Approach** (from [plan.md](plan.md)):
   - What is the implementation strategy?

**If you cannot answer these questions, STOP and re-read files_to_load.**

---

*This file is auto-updated on every task completion by execute-project skill.*
"""
        # APPEND validation gate to preserve existing content
        new_body = old_body + "\n\n" + validation_gate if old_body.strip() else validation_gate
    else:
        new_body = old_body

    # 4. Write new file
    new_post = frontmatter.Post(new_body, **new_metadata)
    frontmatter.dump(new_post, new_file)

    # 5. Keep old file as backup (for rollback)
    backup_file = project_path / "01-planning" / "_resume.md.backup"
    old_file.rename(backup_file)

    return f"SUCCESS: Migrated {old_file} → {new_file}"

# Run on all projects
projects_dir = Path("02-projects")
results = []
for project_dir in projects_dir.glob("*-*"):
    result = migrate_project_resume(project_dir)
    results.append((project_dir.name, result))
    print(f"{project_dir.name}: {result}")
```

**Phase 0.6b: Update Hooks for Backward Compatibility** (30 min)
```python
# SessionStart hook must check BOTH names during migration
def load_resume_file(project_path):
    """Load resume file, checking both new and old names."""
    new_file = project_path / "01-planning" / "resume-context.md"
    old_file = project_path / "01-planning" / "_resume.md"

    if new_file.exists():
        try:
            return frontmatter.load(new_file)  # Prefer new name
        except Exception as e:
            logging.error(f"Failed to parse {new_file}: {e}")
            return None
    elif old_file.exists():
        # Backward compatibility - read old file
        logging.warning(f"Using legacy _resume.md for {project_path.name} - run migration")
        try:
            return frontmatter.load(old_file)
        except Exception as e:
            logging.error(f"Failed to parse {old_file}: {e}")
            return None
    else:
        return None  # No resume file
```

**Phase 0.6c: Test Migration** (30 min)
- Test migration script on 3 sample projects
- Verify schema transformation correct
- Verify backup files created
- Test SessionStart reads both old and new files
- Verify rollback works (restore from .backup)

**Migration Timeline**:
1. **Phase 0**: Create and test migration script
2. **Phase 2**: Run migration on all projects AFTER SessionStart hook updated
3. **Phase 5**: Deprecation warning for old `_resume.md` files
4. **Phase 6**: Remove backward compatibility (resume-context.md only)

**Rollback Plan**:
```bash
# If migration fails, rollback:
find 02-projects -name "resume-context.md" -delete
find 02-projects -name "_resume.md.backup" -exec bash -c 'mv "$0" "${0%.backup}"' {} \;
```

**Success Criteria**:
- [ ] Migration script created and tested
- [ ] All 20+ projects migrated successfully
- [ ] No broken projects (all resume files readable)
- [ ] Backup files created for rollback
- [ ] SessionStart hook reads both old and new names

**Updated Phase 0 Duration**: 6-8 hours → **8-10 hours** (includes migration)

---

### Phase 1: PreCompact Hook Implementation (CORRECTED)
**Time**: 3 hours (increased from 2h)
**Dependencies**: Phase 0 complete

**Goal**: Implement transcript-based project detection using Phase 0 schema

**Tasks**:
1. Update `.claude/hooks/save_resume_state.py`
2. Implement transcript parsing (Agent 1 design)
3. Implement confidence scoring
4. **Output precompact_state.json using Phase 0 FLAT schema**
5. **MUST return `{}`** (empty object) - write to file, don't return JSON
6. **Add secret redaction** (API keys, tokens, credentials)
7. **Optimize to <50ms** (NOT <500ms)

**Key Corrections**:
```python
# WRONG (Agent 1 original):
return {
    "hookSpecificOutput": {
        "precompact_state": {...}  # Cannot inject context!
    }
}

# CORRECT:
# Write to file
Path("00-system/.cache/precompact_state.json").write_text(json.dumps({
    "active_project_id": project_id,  # FLAT schema
    "confidence": "high",
    "detection_method": "transcript",
    "timestamp": now()
}))

# Return empty object
return {}
```

**Performance Target**: <50ms (hook-guides requirement)

---

### Phase 2: SessionStart Hook Enhancement (CORRECTED)
**Time**: 4 hours (increased from 3h)
**Dependencies**: Phase 1 complete + Phase 0 schemas

**Goal**: Inject MANDATORY loading instructions using Phase 0 schemas

**Tasks**:
1. Read existing session_start.py (line 206 insertion point)
2. Add precompact_state.json detection (read **FLAT schema**)
3. **Add session source detection** (exclude `source: "clear"`)
4. Implement YAML parser for _resume.md
5. Implement catastrophic instructions builder
6. Add error handling for all failure modes
7. **Optimize to <200ms** (NOT <2 seconds)

**Key Corrections**:
```python
# Read FLAT schema (NOT nested):
precompact_state = json.load(f)
active_project_id = precompact_state.get("active_project_id")  # FLAT
confidence = precompact_state.get("confidence")

# Add session source detection:
if source == "clear":
    # User explicitly cleared context - DON'T attempt resume
    resume_mode = False
elif source in ("resume", "compact"):
    resume_mode = True
else:
    resume_mode = False
```

**Performance Target**: <200ms (hook-guides requirement)

---

### Phase 3: Hook Integration Testing (EXPANDED)
**Time**: 4 hours (increased from 3h)
**Dependencies**: Phases 1+2 complete

**Goal**: Validate complete PreCompact → SessionStart flow + performance

**Tasks**:
1. **Schema compatibility tests** (Phase 1 → Phase 2 round-trip)
2. **Performance benchmarks** (<50ms PreCompact, <200ms SessionStart)
3. All 4 scenarios from Agent 5
4. **NEW**: Multiple projects in transcript (Agent 1 test case)
5. **NEW**: YAML parsing edge cases (unicode, malformed, missing fields)
6. **NEW**: Session source detection (resume vs. clear)

**Testing Checklist**:
- [ ] Schema compatibility (Agent 1 output → Agent 2 input)
- [ ] PreCompact performance <50ms
- [ ] SessionStart performance <200ms
- [ ] Normal resume flow works
- [ ] Missing _resume.md handled gracefully
- [ ] Corrupted precompact_state.json handled
- [ ] Multiple projects in transcript (most recent wins)
- [ ] Source="clear" does NOT trigger resume

---

### Phase 4A: Research Templates + execute-project Integration (CORRECTED)
**Time**: 3 hours (increased from 2h)
**Dependencies**: Phase 3 complete
**Criticality**: MEDIUM

**Goal**: Create research template system AND integrate with execute-project

**Tasks**:
1. Create template-research-build.md
2. Create template-research-analysis.md
3. Create template-research-simple.md
4. Add template selection logic to create-project
5. **CRITICAL**: Update execute-project skill to read research.md
6. **CRITICAL**: Implement research.md → plan.md Dependencies population
7. **CRITICAL**: Test research → plan.md integration
8. Update SKILL.md documentation
9. Update workflows.md with Step 4.5

**Key Correction**: Phase 4A is **NOT independent** - requires execute-project changes to be usable!

```python
# execute-project MUST implement:
def populate_plan_dependencies_from_research(project_path):
    research_file = project_path / "01-planning" / "research.md"
    if not research_file.exists():
        return  # No research, skip

    # Parse research.md summary section
    findings = extract_research_findings(research_file)

    # Update plan.md Dependencies section
    dependencies_text = format_dependencies_from_research(findings)
    update_plan_md_section(plan_file, "Dependencies & Links", dependencies_text)
```

---

### Phase 4B: Loader Refactoring (OPTIONAL - Deferred)
**Time**: 2 hours
**Dependencies**: Phase 6 complete + 1-2 weeks production validation
**Risk**: LOW (Agent 3 correct)
**Criticality**: LOW (truly optional cleanup)

**Goal**: Clean up --resume flag after hooks proven stable

**Tasks**:
1. **Validate no external dependencies** (search codebase for `--resume` usage)
2. Remove --resume from nexus-loader.py
3. Add deprecation warning to service.startup(resume_mode=True)
4. Update documentation

**DEFERRED to END** - wait for production validation before cleanup

---

### Phase 5: Integration & End-to-End Testing (EXPANDED)
**Time**: 5 hours (increased from 4h)
**Dependencies**: Phases 1-4A complete

**Goal**: Validate complete system with real-world scenarios + migration

**Tasks**:
1. All scenarios from Agent 5 (new project, existing project, multiple cycles, error recovery)
2. **NEW**: Research integration scenario (research → resume → continue)
3. **NEW**: Migration testing (test with 3-5 existing projects)
4. **NEW**: Performance testing under load (large transcripts, many files)
5. **NEW**: Rollback testing (verify each phase can revert safely)

---

### Phase 6: Migration & Deployment (EXPANDED)
**Time**: 3 hours
**Dependencies**: Phase 5 complete

**Goal**: Deploy to production with migration strategy

**Tasks**:
1. **NEW**: Update documentation (7 files per Agent 3)
2. Create migration guide (with version migration, deprecation timeline)
3. Test auto-migration on first use
4. **NEW**: Set up monitoring/telemetry
5. Create git checkpoint
6. Deploy hooks + templates
7. Verify deployment
8. **NEW**: Post-deployment monitoring (24h observation)

---

## Files to Create/Modify (UPDATED)

### NEW Files
- `00-system/.schemas/precompact_state_v1.json` (Phase 0.1 - JSON Schema)
- `00-system/.schemas/resume_context_v1.json` (Phase 0.1 - JSON Schema)
- `02-projects/24-.../03-working/test_schemas.py` (Phase 0.3 - validation tests)
- `02-projects/24-.../03-working/test_integration.py` (Phase 0.3 - integration tests)
- `02-projects/24-.../03-working/migrate_resume_files.py` (Phase 0.6 - migration script)
- `00-system/skills/projects/create-project/scripts/templates/template-research-build.md`
- `00-system/skills/projects/create-project/scripts/templates/template-research-analysis.md`
- `00-system/skills/projects/create-project/scripts/templates/template-research-simple.md`
- `02-projects/{ID}/01-planning/resume-context.md` (template - NEW NAME)
- `02-projects/{ID}/01-planning/research.md` (from template)

### MODIFY Files
- `.claude/hooks/save_resume_state.py` (Phase 1 - write resume-context.md, FLAT schema, return `{}`, <50ms)
- `.claude/hooks/session_start.py` (Phase 2 - read resume-context.md with fallback, source detection, <200ms)
- `00-system/skills/projects/create-project/SKILL.md` (add research phase docs)
- `00-system/skills/projects/create-project/references/workflows.md` (insert research step)
- `00-system/skills/projects/execute-project/SKILL.md` (add auto-update resume-context.md + validation + research integration)
- `00-system/core/nexus/service.py` (resume detection + validation enforcement)
- `00-system/core/nexus/loaders.py` (parse resume-context.md, return instructions)

### MIGRATE Files (Phase 0.6)
- `02-projects/*/01-planning/_resume.md` → `resume-context.md` (20+ files)
- Schema transformation: `resume_version` → `resume_schema_version`, add `project_name`, add validation gate
- Backup old files as `_resume.md.backup` for rollback

### REMOVE References
- All close-session integration mentions
- All manual "save progress" triggers
- All token tracking for compaction detection (not needed - auto-continue)

---

## Key Decisions Summary (UPDATED)

| Decision | Rationale | Correction |
|----------|-----------|------------|
| Research includes external sources | Not limited to codebase - GitHub, web, papers too | ✓ Confirmed |
| Research location: 01-planning/ | Findings are planning artifacts, not raw materials | ✓ Confirmed by Agent 4 |
| **resume-context.md (NOT _resume.md)** | Clearer naming, requires migration of 20+ projects | **CONFIRMED 2026-01-04 (Option B)** |
| resume-context.md is manifest, not summary | NO duplication - only loading instructions | ✓ Confirmed |
| FLAT schema for precompact_state.json | Agent 1 → Agent 2 compatibility | **CRITICAL CORRECTION** |
| PreCompact returns `{}` | Hook output cannot contain JSON | **CRITICAL CORRECTION** |
| Performance: <50ms / <200ms | Hook-guides requirements | **CRITICAL CORRECTION** |
| Phase 0 (Schema Design) first | Prevents rework during implementation | **CRITICAL ADDITION** |
| Migration with backward compatibility | SessionStart reads both old and new names during transition | **NEW (Phase 0.6)** |
| Auto-update on task completion | Always current, no manual triggers, no close-session | ✓ Confirmed |
| Auto-continue after compaction | No user trigger needed - seamless, automatic | ✓ Confirmed |
| Validation gate enforced | AI must answer questions before continuing work | ✓ Confirmed |

---

## Success Criteria (REVISED)

**Research Phase**:
- [ ] Can research codebase + external sources
- [ ] Research location: `01-planning/research.md`
- [ ] execute-project populates plan.md Dependencies from research
- [ ] User can skip if not needed

**Resume State**:
- [ ] resume-context.md is minimal manifest (no duplication)
- [ ] Auto-updates on every task completion
- [ ] Contains files_to_load[] and next_action
- [ ] Uses validated YAML schema from Phase 0
- [ ] All 20+ existing `_resume.md` files migrated successfully

**PreCompact Hook**:
- [ ] Returns `{}` (empty object)
- [ ] Writes precompact_state.json with FLAT schema
- [ ] Executes in <50ms
- [ ] Includes secret redaction

**SessionStart Hook**:
- [ ] Reads FLAT schema from precompact_state.json
- [ ] Detects source (excludes "clear")
- [ ] Injects catastrophic instructions
- [ ] Executes in <200ms

**Auto-Continue Flow**:
- [ ] After compaction, AI auto-continues
- [ ] Loader auto-detects active project
- [ ] Validation gate enforces context loading
- [ ] Seamless continuation from exact point

---

## Anti-Patterns (DO NOT DO) - UPDATED

❌ Put summaries or duplicated content in resume-context.md
❌ Use close-session for resume updates
❌ Require manual "save progress" triggers
❌ Require user to say "continue project X" after compaction
❌ Allow AI to continue without answering validation questions
❌ Limit research to only codebase (must include external!)
❌ **Use nested schema for precompact_state.json** (MUST be flat)
❌ **Return JSON in PreCompact hook output** (MUST return `{}`}
❌ **Exceed performance budgets** (50ms/200ms are hard limits)
❌ **Skip Phase 0** (schema design MUST happen first)
❌ **Treat Phase 4A as independent** (requires execute-project integration)
❌ **Skip migration** (20+ projects must be migrated with backups)
❌ **Hard-code _resume.md name** (use resume-context.md with backward compat during migration)

---

## Timeline (REVISED v2 - WITH MIGRATION)

| Original Estimate | With Critical Fixes | With Migration (Option B) | Total Increase |
|------------------|---------------------|---------------------------|----------------|
| 15-18 hours | 28-32 hours | **33-37 hours** | +85-105% |

**Migration adds +2 hours to Phase 0**:
- Phase 0.6a: Create migration script (1h)
- Phase 0.6b: Add backward compatibility (30min)
- Phase 0.6c: Test migration (30min)

**Updated Sessions**:
- Session 1 (5h): Phase 0 (8-10h total, split across 2 sessions)
- Session 2 (5h): Phase 0 complete + Phase 1 start
- Session 3 (4h): Phase 2
- Session 4 (4h): Phase 3
- Session 5 (4h): Phase 4A
- Session 6 (5h): Phase 5 (includes running migration on all projects)
- Session 7 (3h): Phase 6
- Session 8 (2h): Phase 4B (optional, 1-2 weeks later)

**Critical Path**:
1. **Phase 0.1-0.5**: Schema design & validation (6-8h)
2. **Phase 0.6**: Migration strategy & testing (2h) ← **NEW**
3. **Phase 1-2**: Hook implementation (7h)
4. **Phase 5**: Run migration on all 20+ projects (included in 5h)
5. **Phase 6**: Remove backward compatibility after validation

---

**Status**: Design Revised v2 - Option B (resume-context.md) confirmed
**Next Step**: Execute Phase 0 (Schema Design + Migration)
**Confidence**: HIGH (all 11 critical issues + migration strategy documented)
