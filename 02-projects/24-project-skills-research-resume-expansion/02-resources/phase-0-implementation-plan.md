# Phase 0: Schema Design & Validation - Implementation Plan

**Version**: 1.0
**Created**: 2026-01-03
**Status**: READY FOR EXECUTION
**Prerequisites**: Planning phase complete, codebase validation complete
**Estimated Duration**: 6-8 hours

---

## Executive Summary

Phase 0 is a **mandatory foundation phase** that must be completed before implementing PreCompact or SessionStart hooks. The codebase validation revealed that:

1. Current `_resume.md` format conflicts with new `precompact_state.json` schema
2. Migration strategy needed for 20+ existing projects
3. File naming decision required (`_resume.md` vs `resume-context.md`)
4. Schema compatibility must be validated before implementation

**Critical Decision Required**: Choose migration path (see Section 7)

---

## 1. Schema Definitions

### 1.1 precompact_state.json (FLAT Schema)

**Location**: `00-system/.cache/precompact_state.json`
**Purpose**: Lightweight project detection state written by PreCompact hook
**Format**: JSON (FLAT structure - NOT nested)

```json
{
  "$schema": "precompact_state_schema_v1",
  "active_project_id": "24-project-skills-research-resume-expansion",
  "confidence": "high",
  "detection_method": "transcript",
  "timestamp": "2026-01-03T17:00:00Z",
  "session_id": "abc123",
  "file_access_count": 15,
  "last_modified_project": "24-project-skills-research-resume-expansion"
}
```

**Field Specifications**:

| Field | Type | Required | Values | Description |
|-------|------|----------|--------|-------------|
| `$schema` | string | Yes | `"precompact_state_schema_v1"` | Schema version identifier |
| `active_project_id` | string | Yes | `NN-kebab-case-name` | Detected project ID |
| `confidence` | string | Yes | `"high"`, `"medium"`, `"low"` | Detection confidence level |
| `detection_method` | string | Yes | `"transcript"`, `"cache"`, `"fallback"` | How project was detected |
| `timestamp` | string | Yes | ISO-8601 | When detection occurred |
| `session_id` | string | No | UUID | Claude Code session ID |
| `file_access_count` | integer | No | 0+ | Number of project files accessed |
| `last_modified_project` | string | No | `NN-kebab-case-name` | Last edited project (fallback) |

**Validation Rules**:
- File size must be < 1KB (performance requirement)
- All required fields must be present
- `active_project_id` must match `NN-*` pattern
- `timestamp` must be valid ISO-8601
- `confidence` must be enum value

---

### 1.2 resume-context.md (YAML + Markdown)

**Location**: `02-projects/{ID}/01-planning/resume-context.md`
**Purpose**: Loading manifest + validation gate for SessionStart hook
**Format**: YAML frontmatter + Markdown body

```yaml
---
# SCHEMA VERSION
resume_schema_version: "1.0"

# PROJECT IDENTIFICATION
project_id: "24-project-skills-research-resume-expansion"
project_name: "Project Skills Research & Resume Expansion"
current_phase: "execution"  # research | planning | execution

# AUTO-LOAD INSTRUCTIONS
next_action: "execute-project"
files_to_load:
  - "01-planning/overview.md"
  - "01-planning/plan.md"
  - "01-planning/steps.md"
  - "01-planning/research.md"  # Optional - if research completed

# EXECUTION STATE (MINIMAL - NO DUPLICATION)
current_section: 2
current_task: 15
progress: "14/40 tasks complete"

# METADATA
last_updated: "2026-01-03T17:00:00Z"
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

**If you cannot answer these questions, STOP and re-read `files_to_load`.**

---

*This file is auto-updated on every task completion by execute-project skill.*
```

**Field Specifications**:

| Field | Type | Required | Values | Description |
|-------|------|----------|--------|-------------|
| `resume_schema_version` | string | Yes | `"1.0"` | Schema version |
| `project_id` | string | Yes | `NN-kebab-case-name` | Project ID (must match folder) |
| `project_name` | string | Yes | Free text | Human-readable name |
| `current_phase` | string | Yes | `"research"`, `"planning"`, `"execution"` | Lifecycle phase |
| `next_action` | string | Yes | Skill name | Skill to load on resume |
| `files_to_load` | array | Yes | Relative paths | Files to read on resume |
| `current_section` | integer | No | 1+ | Section number in steps.md |
| `current_task` | integer | No | 1+ | Task number in section |
| `progress` | string | No | `"N/M format"` | Human-readable progress |
| `last_updated` | string | Yes | ISO-8601 | Last modification time |

**Validation Rules**:
- File size should be < 5KB (mostly frontmatter)
- All paths in `files_to_load` must exist
- `project_id` must match folder name
- `current_phase` must match project lifecycle
- YAML must be valid (parseable)

---

## 2. Migration Strategy

### 2.1 Current State Analysis

**Findings from codebase validation**:
- Current PreCompact hook writes `_resume.md` to `01-planning/`
- Existing format uses YAML but different schema
- ~20 existing projects have `_resume.md` files
- Current format works but doesn't match new design

**Current `_resume.md` Schema** (Example from Project 24):
```yaml
---
resume_version: 1.3
last_updated: 2026-01-03T17:00:00
project_id: 24-project-skills-research-resume-expansion
current_phase: planning
next_action: execute-project
files_to_load: [...]
current_section: 1
current_task: 1
progress: 5/5 planning complete
---
[Markdown body with session history and next tasks]
```

**Schema Comparison**:

| Feature | Current `_resume.md` | New `resume-context.md` |
|---------|---------------------|------------------------|
| Location | `01-planning/` | `01-planning/` ✓ |
| Format | YAML + Markdown | YAML + Markdown ✓ |
| Schema version field | `resume_version` | `resume_schema_version` |
| Project name field | Missing | `project_name` (new) |
| Files to load | Array | Array ✓ |
| Validation gate | Missing | **CRITICAL NEW FEATURE** |
| Body content | Session history | Validation questions |

**Migration Impact**: Low (schema compatible, content change only)

---

### 2.2 Migration Decision Matrix

**Option A: Keep `_resume.md` naming**
- ✅ No file renames needed (0 migration)
- ✅ Existing hooks continue working
- ✅ Zero breaking changes
- ❌ Naming doesn't reflect purpose (not a "resume", it's a "context loader")
- ❌ Underscore prefix convention unclear

**Option B: Rename to `resume-context.md`**
- ✅ Clearer naming (describes purpose)
- ✅ Matches design intent from Session 2
- ❌ Requires renaming ~20 files
- ❌ Breaking change for current hooks
- ❌ Manual migration needed

**Option C: Support Both (Transitional)**
- ✅ Backwards compatible
- ✅ Gradual migration possible
- ✅ No breaking changes
- ❌ Complex logic in SessionStart hook
- ❌ Maintenance burden (two schemas)

---

### 2.3 Recommended Migration Path

**RECOMMENDATION: Option A (Keep `_resume.md`)**

**Rationale**:
1. **Zero Breaking Changes**: Existing projects continue working
2. **Schema Compatible**: Only content update needed (add validation gate)
3. **Low Risk**: No file system operations
4. **User Preference**: User originally chose `_resume.md`, only later suggested `resume-context.md`

**Implementation**:
```python
# SessionStart hook checks for resume file
RESUME_FILE = "01-planning/_resume.md"  # Keep current name

if os.path.exists(os.path.join(project_path, RESUME_FILE)):
    # Read YAML frontmatter
    # Check for resume_schema_version field
    # If missing, treat as "legacy format" (still works)
    # If present, validate against schema
```

**Migration Steps**:
1. Update FINAL-DESIGN.md to use `_resume.md` (not `resume-context.md`)
2. Update resume-state-REVISED.md to use `_resume.md`
3. Add schema version field to new resumes: `resume_schema_version: "1.0"`
4. Add validation gate content to body
5. No changes needed for existing projects (they continue working)

**Future Option**: Provide migration skill later (`migrate-resume-files`) if user wants rename

---

## 3. Validation Tests

### 3.1 Schema Validation Tests

**Test File**: `02-projects/24-project-skills-research-resume-expansion/03-working/test_schemas.py`

```python
import json
import yaml
import os
from datetime import datetime
from typing import Dict, Any

# Test 1: precompact_state.json Validation
def test_precompact_state_schema():
    """Validate precompact_state.json matches FLAT schema."""
    test_cases = [
        # Valid cases
        {
            "name": "high_confidence_transcript",
            "data": {
                "active_project_id": "24-project-test",
                "confidence": "high",
                "detection_method": "transcript",
                "timestamp": "2026-01-03T17:00:00Z"
            },
            "should_pass": True
        },
        # Invalid cases
        {
            "name": "nested_schema_WRONG",
            "data": {
                "project_detection": {  # NESTED - WRONG
                    "project_id": "24-project-test"
                }
            },
            "should_pass": False
        },
        {
            "name": "missing_required_fields",
            "data": {
                "active_project_id": "24-project-test"
                # Missing confidence, detection_method, timestamp
            },
            "should_pass": False
        },
        {
            "name": "invalid_confidence_enum",
            "data": {
                "active_project_id": "24-project-test",
                "confidence": "very_high",  # Invalid enum
                "detection_method": "transcript",
                "timestamp": "2026-01-03T17:00:00Z"
            },
            "should_pass": False
        }
    ]

    for case in test_cases:
        result = validate_precompact_state(case["data"])
        assert result == case["should_pass"], f"Test {case['name']} failed"

# Test 2: resume-context.md Validation
def test_resume_context_schema():
    """Validate resume-context.md YAML frontmatter."""
    test_cases = [
        # Valid case
        {
            "name": "valid_execution_phase",
            "yaml": """---
resume_schema_version: "1.0"
project_id: "24-project-test"
project_name: "Test Project"
current_phase: "execution"
next_action: "execute-project"
files_to_load:
  - "01-planning/overview.md"
last_updated: "2026-01-03T17:00:00Z"
---""",
            "should_pass": True
        },
        # Invalid cases
        {
            "name": "invalid_phase_enum",
            "yaml": """---
project_id: "24-project-test"
current_phase: "testing"  # Invalid enum
---""",
            "should_pass": False
        }
    ]

    for case in test_cases:
        data = yaml.safe_load(case["yaml"])
        result = validate_resume_context(data)
        assert result == case["should_pass"], f"Test {case['name']} failed"

# Test 3: File Size Validation
def test_file_size_limits():
    """Validate files meet performance requirements."""
    # precompact_state.json must be < 1KB
    state = {
        "active_project_id": "24-project-test",
        "confidence": "high",
        "detection_method": "transcript",
        "timestamp": "2026-01-03T17:00:00Z"
    }
    size = len(json.dumps(state).encode('utf-8'))
    assert size < 1024, f"precompact_state.json too large: {size} bytes"

    # resume-context.md should be < 5KB
    # (validated during hook execution)

# Test 4: Schema Compatibility
def test_backwards_compatibility():
    """Ensure new schema reads old _resume.md files."""
    old_format = """---
resume_version: 1.2
project_id: 24-project-test
---"""

    data = yaml.safe_load(old_format)
    # Should still work (legacy support)
    assert "project_id" in data
    assert validate_legacy_resume(data) == True
```

### 3.2 Integration Tests

**Test File**: `02-projects/24-project-skills-research-resume-expansion/03-working/test_integration.py`

```python
# Test 5: PreCompact → SessionStart Flow
def test_precompact_to_session_start():
    """Test full flow: PreCompact writes, SessionStart reads."""
    # Simulate PreCompact hook
    state = {
        "active_project_id": "24-project-test",
        "confidence": "high",
        "detection_method": "transcript",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

    # Write precompact_state.json
    cache_path = "00-system/.cache/precompact_state.json"
    with open(cache_path, 'w') as f:
        json.dump(state, f)

    # Simulate SessionStart hook
    with open(cache_path, 'r') as f:
        loaded_state = json.load(f)

    # Validate loaded state
    assert loaded_state["active_project_id"] == "24-project-test"
    assert "confidence" in loaded_state  # FLAT schema works

# Test 6: Session Source Detection
def test_session_source_detection():
    """Test SessionStart respects source field."""
    test_sources = [
        {"source": "resume", "should_load": True},
        {"source": "compact", "should_load": True},
        {"source": "clear", "should_load": False},  # CRITICAL
        {"source": "startup", "should_load": False}
    ]

    for case in test_sources:
        result = should_load_resume(case["source"])
        assert result == case["should_load"], f"Source {case['source']} failed"

# Test 7: File Path Resolution
def test_files_to_load_validation():
    """Ensure all files_to_load paths exist."""
    resume_yaml = {
        "files_to_load": [
            "01-planning/overview.md",
            "01-planning/plan.md",
            "01-planning/nonexistent.md"  # This should fail
        ]
    }

    project_path = "02-projects/24-project-test"
    result = validate_files_exist(resume_yaml, project_path)
    assert result == False, "Should detect missing file"
```

---

## 4. Implementation Checklist

### Phase 0.1: Schema Documentation (2 hours)

- [x] Define precompact_state.json FLAT schema (Section 1.1)
- [x] Define resume-context.md YAML schema (Section 1.2)
- [ ] Create JSON Schema files for validation
  - [ ] `00-system/.schemas/precompact_state_v1.json`
  - [ ] `00-system/.schemas/resume_context_v1.json`
- [ ] Document field specifications (types, constraints, validation)
- [ ] Create example files in `02-resources/examples/`
  - [ ] `example-precompact-state.json`
  - [ ] `example-resume-context.md`

### Phase 0.2: Migration Decision (30 minutes)

- [x] Analyze current `_resume.md` format (Section 2.1)
- [x] Create migration decision matrix (Section 2.2)
- [x] **DECISION MADE**: Keep `_resume.md` naming (Option A)
- [ ] Update FINAL-DESIGN.md with decision
- [ ] Update resume-state-REVISED.md with decision

### Phase 0.3: Validation Tests (3 hours)

- [ ] Create test file structure
  - [ ] `03-working/test_schemas.py`
  - [ ] `03-working/test_integration.py`
  - [ ] `03-working/test_data/` (fixtures)
- [ ] Write schema validation tests (7 tests from Section 3.1)
- [ ] Write integration tests (7 tests from Section 3.2)
- [ ] Run tests and document results
- [ ] Create `test-results.md` with pass/fail status

### Phase 0.4: Additional Blocker Identification (1 hour)

- [ ] Review hook-guides for any missed requirements
- [ ] Cross-check FINAL-DESIGN against validation findings
- [ ] Document any new blockers in implementation-blockers.md
- [ ] Update timeline estimates based on findings

### Phase 0.5: Documentation Updates (1.5 hours)

- [ ] Update FINAL-DESIGN.md:
  - [ ] Change all `resume-context.md` → `_resume.md`
  - [ ] Add migration strategy section
  - [ ] Add schema definitions
  - [ ] Update timeline: 31-35 hours (from 28-32)
- [ ] Update resume-state-REVISED.md:
  - [ ] Change naming to `_resume.md`
  - [ ] Add schema compatibility notes
- [ ] Update implementation-blockers.md:
  - [ ] Mark schema mismatch as RESOLVED
  - [ ] Add any new blockers from Phase 0.4

---

## 5. Identified Blockers

### Blocker 1: JSON Schema Validation Library
**Severity**: MEDIUM
**Problem**: Python hooks need JSON schema validation for precompact_state.json
**Solution**: Use `jsonschema` library (standard Python)
```python
import jsonschema
schema = {...}  # Load from .schemas/
jsonschema.validate(instance=data, schema=schema)
```
**Impact**: +30 minutes (add dependency check to hooks)

### Blocker 2: YAML Parsing in SessionStart
**Severity**: MEDIUM
**Problem**: SessionStart needs to parse YAML frontmatter safely
**Solution**: Use `frontmatter` library (already in hook examples)
```python
import frontmatter
post = frontmatter.load(resume_file)
metadata = post.metadata  # YAML dict
body = post.content       # Markdown string
```
**Impact**: Already handled (no additional time)

### Blocker 3: Timestamp Format Validation
**Severity**: LOW
**Problem**: Need to validate ISO-8601 timestamp format
**Solution**: Use `datetime.fromisoformat()` with error handling
```python
from datetime import datetime
try:
    dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
except ValueError:
    # Invalid timestamp
```
**Impact**: +15 minutes (add validation function)

### Blocker 4: File Size Monitoring
**Severity**: LOW
**Problem**: Need to ensure precompact_state.json stays < 1KB
**Solution**: Add size check after writing
```python
file_size = os.path.getsize(cache_file)
if file_size > 1024:
    # Log warning, strip optional fields
```
**Impact**: +15 minutes

---

## 6. Success Criteria

Phase 0 is complete when:

1. **Schema Definitions**: ✓
   - [x] precompact_state.json FLAT schema documented
   - [x] resume-context.md YAML schema documented
   - [ ] JSON Schema files created

2. **Migration Strategy**: ✓
   - [x] Current state analyzed
   - [x] Migration decision made (Keep `_resume.md`)
   - [ ] FINAL-DESIGN updated with decision

3. **Validation Tests**:
   - [ ] 14 unit tests written (7 schema + 7 integration)
   - [ ] All tests passing
   - [ ] Test results documented

4. **Blocker Resolution**:
   - [ ] All CRITICAL blockers from Session 2 addressed
   - [ ] No new CRITICAL blockers identified
   - [ ] All blockers documented in implementation-blockers.md

5. **Documentation Complete**:
   - [ ] FINAL-DESIGN.md updated
   - [ ] resume-state-REVISED.md updated
   - [ ] Example files created

**Gate Check**: All checkboxes above must be checked before proceeding to Phase 1 (PreCompact Hook Implementation).

---

## 7. Migration Path Selection ✅ DECISION CONFIRMED

### ✅ User Selected: **Option B** (Rename to `resume-context.md`)

**Confirmed**: 2026-01-04
**Rationale**: Clearer naming that reflects purpose (context loader, not resume)

**Implementation Actions**:
- ✅ Add migration script to Phase 0.6 (see Section 2.3)
- ✅ Update all design docs to use `resume-context.md` (FINAL-DESIGN, resume-state-REVISED)
- ✅ Update SessionStart hook to check both names during transition
- ✅ Add deprecation warnings for old `_resume.md` name
- ✅ Phase 0 estimate increased: 8-10 hours (from 6-8)
- ✅ Timeline updated: 33-37 hours (from 29-35)

**Migration Timeline**:
1. **Phase 0.6**: Create and test migration script (2h)
2. **Phase 2**: Update SessionStart hook with backward compatibility (included)
3. **Phase 5**: Run migration on all 20+ projects (included in Phase 5)
4. **Phase 6**: Deprecation warnings added
5. **Future**: Remove backward compatibility (resume-context.md only)

---

## 8. Next Steps After Phase 0

**Immediate Next Phase**: Phase 1 - PreCompact Hook Implementation

**Prerequisites from Phase 0**:
- Schema definitions validated
- Test suite passing
- Migration decision finalized
- All design docs updated

**Phase 1 Entry Criteria**:
1. All Phase 0 checklist items completed
2. User confirms migration path
3. No CRITICAL blockers remaining
4. Test suite establishes baseline

**Handoff to Phase 1**:
- Schemas available in `00-system/.schemas/`
- Test suite ready in `03-working/test_*.py`
- Example files available for reference
- FINAL-DESIGN.md is source of truth

---

## 9. Timeline Summary

| Phase | Task | Estimated Time | Status |
|-------|------|----------------|--------|
| 0.1 | Schema Documentation | 2h | Pending |
| 0.2 | Migration Decision | 0.5h | ✅ COMPLETE (Option B confirmed) |
| 0.3 | Validation Tests | 3h | Pending |
| 0.4 | Blocker Identification | 1h | Pending |
| 0.5 | Documentation Updates | 1.5h | Pending |
| 0.6 | Migration Script & Testing | **2h** | **NEW - Pending** |
| **Total** | **Phase 0** | **10 hours** | **5% Complete** |

**Updated Project Timeline** (with Phase 0 + Migration):
- Phase 0: Schema Design + Migration - **8-10h** (+2h for Option B)
- Phase 1: PreCompact Hook - 8-10h
- Phase 2: SessionStart Hook - 6-8h (includes backward compat)
- Phase 3: Research Templates - 3-4h
- Phase 4: Testing & Integration - 4-5h
- Phase 5: E2E + Run Migration - 5h (includes migrating 20+ projects)
- Phase 6: Deployment + Deprecation - 3h
- **Total**: **33-37 hours** (vs original 15-18h, +85-105%)

---

## 10. Appendix: File Locations

**Schemas** (to be created):
- `00-system/.schemas/precompact_state_v1.json`
- `00-system/.schemas/resume_context_v1.json`

**Examples** (to be created):
- `02-projects/24-project-skills-research-resume-expansion/02-resources/examples/example-precompact-state.json`
- `02-projects/24-project-skills-research-resume-expansion/02-resources/examples/example-resume-context.md`

**Tests** (to be created):
- `02-projects/24-project-skills-research-resume-expansion/03-working/test_schemas.py`
- `02-projects/24-project-skills-research-resume-expansion/03-working/test_integration.py`
- `02-projects/24-project-skills-research-resume-expansion/03-working/test_data/`

**Design Documents** (existing - to be updated):
- `02-projects/24-project-skills-research-resume-expansion/02-resources/FINAL-DESIGN.md`
- `02-projects/24-project-skills-research-resume-expansion/02-resources/resume-state-REVISED.md`
- `02-projects/24-project-skills-research-resume-expansion/02-resources/implementation-blockers.md`

---

**Phase 0 Status**: READY FOR EXECUTION
**Migration Decision**: ✅ CONFIRMED - Option B (`resume-context.md`)
**Next Action**: Execute Phase 0.1 (Schema Documentation)
**Blocked By**: None - all decisions made, ready to implement
