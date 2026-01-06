# State Detection Integration Plan

**Created**: 2026-01-06
**Status**: Implementation Ready

---

## Summary

Integration plan for connecting the new `project_state.py` utility to `session_start.py` for smarter context mode detection using resume-context.md metadata.

---

## Current vs Enhanced Functions

### 1. `detect_project_phase()`

**Current Implementation:**
- Parses `04-steps.md` Phase 1 section
- Counts checkboxes: all complete = execution, otherwise = planning
- **Limitation**: Doesn't respect resume-context.md explicit phase
- **Limitation**: Regex parsing every time (slower)

**Enhanced Implementation:**
```python
# session_start.py (lines 208-249)

def detect_project_phase(project_dir: str, project_id: str) -> str:
    """
    Detect phase with metadata priority:
    1. resume-context.md current_phase + next_action (explicit)
    2. 04-steps.md checkbox analysis (fallback)

    Returns: "plan-project" or "execute-project"
    """
    from utils.project_state import detect_phase_from_metadata

    project_path = Path(project_dir) / "02-projects" / project_id

    # Use enhanced detection (tries resume-context first)
    phase, skill = detect_phase_from_metadata(project_path)

    logging.info(f"Detected phase for {project_id}: {phase} → {skill}")
    return skill
```

**Benefits:**
- Respects explicit phase from resume-context.md
- Falls back to checkbox logic if metadata missing
- Reuses tested utility code
- Faster (no regex when metadata available)

---

### 2. `find_most_recent_project()`

**Current Implementation:**
- Scans all `resume-context.md` files
- Returns project with most recent `last_updated` timestamp
- **Limitation**: Returns COMPLETE projects
- **Limitation**: Doesn't use overview.md status field

**Enhanced Implementation:**
```python
# session_start.py (lines 151-205)

def find_most_recent_project(project_dir: str) -> str | None:
    """
    Find most recent non-COMPLETE project for RESUME source.

    Uses project_state utility to filter by status.
    """
    from utils.project_state import find_most_recent_project_enhanced

    projects_dir = Path(project_dir) / "02-projects"

    # Use enhanced detection (excludes COMPLETE by default)
    state = find_most_recent_project_enhanced(
        projects_dir,
        exclude_complete=True,
        exclude_archived=True
    )

    if state:
        logging.info(f"Most recent project: {state.project_id} - {state.name} ({state.progress_percent}%)")
        return state.project_id + "-" + state.name.lower().replace(' ', '-')
    else:
        logging.info("No active projects found")
        return None
```

**Benefits:**
- Skips COMPLETE projects automatically
- Uses tested utility code
- Returns full ProjectState (could use more metadata)
- Consistent with project_state logic

---

### 3. `load_resume_context()`

**Current Implementation:**
- Reads `resume-context.md` or legacy `_resume.md`
- Extracts `files_to_load` array from YAML
- **Returns**: List of file paths

**Enhanced Implementation:**
```python
# session_start.py (lines 252-306)

def load_resume_context(project_dir: str, project_id: str) -> dict:
    """
    Load complete resume metadata (not just files_to_load).

    Returns full metadata dict for richer context mode detection.
    """
    from utils.project_state import get_project_metadata_from_resume

    project_path = Path(project_dir) / "02-projects" / project_id

    # Get full metadata dict
    metadata = get_project_metadata_from_resume(project_path)

    if metadata:
        logging.info(f"Loaded resume context: phase={metadata.get('current_phase')}, section={metadata.get('current_section')}")
        # Return full dict, not just files_to_load
        return metadata
    else:
        logging.warning(f"No resume context found for {project_id}")
        return {}
```

**Breaking Change**: This changes the return type from `list[str]` to `dict`.

**Callers to Update:**
```python
# session_start.py - determine_context_mode() (lines 53-148)

# OLD:
files_to_load = load_resume_context(nexus_root, detected_project)

# NEW:
resume_metadata = load_resume_context(nexus_root, detected_project)
files_to_load = resume_metadata.get('files_to_load', [])
current_section = resume_metadata.get('current_section', 1)
tasks_completed = resume_metadata.get('tasks_completed', 0)
```

**Benefits:**
- Access to current_section for section-aware file loading
- Access to tasks_completed for progress tracking
- Access to current_phase for better routing
- Single source of truth (project_state utility)

---

## Implementation Phases

### Phase 1: Non-Breaking Enhancements ✅ SAFE
1. Update `detect_project_phase()` to use `detect_phase_from_metadata()`
   - No signature change, drop-in replacement
   - File: `session_start.py:208-249`

2. Update `find_most_recent_project()` to filter COMPLETE projects
   - No signature change, drop-in replacement
   - File: `session_start.py:151-205`

**Risk**: Very low - both maintain same return types
**Testing**: Run existing session_start tests

---

### Phase 2: Breaking Change (load_resume_context) ⚠️ REQUIRES TESTING
1. Change `load_resume_context()` return type to `dict`
   - File: `session_start.py:252-306`

2. Update `determine_context_mode()` to use dict return
   - Extract `files_to_load` from metadata
   - Use `current_section`, `tasks_completed` for enhanced routing
   - File: `session_start.py:53-148`

3. Update `build_compact_xml()` to use dict
   - Extract files_to_load from dict
   - File: `session_start.py:495-599`

**Risk**: Medium - changes function signature
**Testing**: Integration tests required

---

### Phase 3: Advanced Features (FUTURE)
1. Section-aware file loading
   - Use `current_section` to load working files
   - Reduce token waste on irrelevant files

2. Status-based routing
   - PLANNING → always plan-project
   - IN_PROGRESS → check phase
   - COMPLETE → never auto-load

3. Multi-session tracking
   - Use `session_ids` list for enhanced detection
   - Track all sessions that touched project

---

## Testing Strategy

### Unit Tests
- [x] Test `project_state.py` utility (33 tests passing)
- [ ] Test enhanced `detect_project_phase()` fallback
- [ ] Test `find_most_recent_project()` filtering

### Integration Tests
- [ ] Test session_start with enhanced phase detection
- [ ] Test resume mode with COMPLETE project filtering
- [ ] Test load_resume_context dict return

### Regression Tests
- [ ] Verify existing handover tests still pass (128 tests)
- [ ] Test with real project 28
- [ ] Test backward compatibility (projects without resume-context.md)

---

## Recommended Next Steps

1. **Implement Phase 1 (SAFE)** - low risk, immediate value
   - Update detect_project_phase()
   - Update find_most_recent_project()
   - Run tests: `pytest .claude/hooks/tests/ -v`

2. **Create PR/checkpoint** - save working state

3. **Implement Phase 2 (BREAKING)** - requires careful testing
   - Update load_resume_context()
   - Update callers
   - Add integration tests

4. **Validate end-to-end** - test real session flows
   - new → compact → resume cycle
   - Multiple projects active
   - COMPLETE project filtering

---

## Code Diff Preview

### Phase 1 Changes

```python
# session_start.py

# BEFORE:
def detect_project_phase(project_dir: str, project_id: str) -> str:
    steps_file = Path(project_dir) / "02-projects" / project_id / "01-planning" / "04-steps.md"
    # ... 40 lines of regex parsing ...
    return "plan-project"

# AFTER:
def detect_project_phase(project_dir: str, project_id: str) -> str:
    """Detect phase using metadata-first approach."""
    from utils.project_state import detect_phase_from_metadata

    project_path = Path(project_dir) / "02-projects" / project_id
    phase, skill = detect_phase_from_metadata(project_path)

    logging.info(f"Detected phase for {project_id}: {phase} → {skill}")
    return skill
```

```python
# BEFORE:
def find_most_recent_project(project_dir: str) -> str | None:
    # ... manual timestamp parsing ...
    return most_recent_project  # might be COMPLETE

# AFTER:
def find_most_recent_project(project_dir: str) -> str | None:
    """Find most recent non-COMPLETE project."""
    from utils.project_state import find_most_recent_project_enhanced

    projects_dir = Path(project_dir) / "02-projects"
    state = find_most_recent_project_enhanced(projects_dir, exclude_complete=True)

    if state:
        return f"{state.project_id}-{state.name.lower().replace(' ', '-')}"
    return None
```

---

**Status**: Ready for Phase 1 implementation
**Risk**: Low (backward compatible)
**Value**: Immediate improvement to handover accuracy
