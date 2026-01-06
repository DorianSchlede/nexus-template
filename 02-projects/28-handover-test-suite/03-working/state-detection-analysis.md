# State Detection Analysis - session_start.py

**Created**: 2026-01-06
**Purpose**: Analyze current state detection mechanisms and identify improvement opportunities using init_project.py metadata patterns

---

## Current State Detection Mechanisms

### 1. Project Detection (Priority Order)

**Primary: Session ID Match** (`find_project_by_session_id()`)
- Scans `02-projects/*/01-planning/resume-context.md`
- Looks for exact `session_id: "{uuid}"` match in YAML frontmatter
- **Most reliable** - bulletproof cross-session resume

**Fallback: Transcript Parsing** (`parse_transcript_for_project()`)
- Parses `.claude/sessions/{id}/transcript.jsonl`
- Looks for `tool_use` entries calling project scripts
- **Less reliable** - depends on transcript format

**Resume Mode: Most Recent Project** (`find_most_recent_project()`)
- Scans all `resume-context.md` files
- Extracts `last_updated: "{timestamp}"` from YAML
- Returns project with most recent timestamp
- **Useful for resume without explicit project context**

### 2. Phase Detection (`detect_project_phase()`)

**Current Logic:**
```python
# Reads 04-steps.md
# Extracts Phase 1 section using regex
# Counts checkboxes: total vs completed
# If ALL Phase 1 tasks [x] → execution
# Otherwise → planning
```

**Limitations:**
- Only looks at Phase 1 checkboxes
- Doesn't use resume-context.md metadata
- Can't detect mid-execution pauses
- No awareness of actual project state beyond checkboxes

### 3. Resume Context Loading (`load_resume_context()`)

**Current Extraction:**
- Reads `resume-context.md` (or legacy `_resume.md`)
- Extracts `files_to_load: [...]` array from YAML
- Returns list of files to inject into XML context

**Metadata Available But Not Used:**
- `current_phase: planning | execution`
- `next_action: plan-project | execute-project`
- `current_section: N` (which section of steps.md)
- `tasks_completed: N`
- `last_updated: "{timestamp}"`
- `session_id: "{uuid}"`

---

## init_project.py Metadata Patterns

### Files Created by init_project.py

```
02-projects/{ID}-{name}/
├── 01-planning/
│   ├── 01-overview.md        # YAML frontmatter with status
│   ├── 02-discovery.md        # Empty template
│   ├── 03-plan.md             # Empty template
│   ├── 04-steps.md            # Checkbox tracking
│   └── resume-context.md      # Rich state metadata
├── 02-resources/
├── 03-working/
└── 04-outputs/
```

### Key Metadata Sources

#### 1. `01-overview.md` YAML Frontmatter
```yaml
---
id: 28-handover-test-suite
name: handover-test-suite
status: PLANNING | IN_PROGRESS | COMPLETE
description: "Full test suite for session handover functionality"
created: 2026-01-05
project_path: 02-projects/28-handover-test-suite/
---
```

**State Indicators:**
- `status` field - explicit project lifecycle state
- `created` date - project age
- `description` - keyword-based project matching

#### 2. `resume-context.md` YAML Frontmatter
```yaml
---
session_id: "ae83144f-a87c-42c2-bb21-3eb589ca04d7"
last_updated: "2026-01-06T01:13:09.213621"
current_phase: planning | execution
next_action: plan-project | execute-project
current_section: 7
tasks_completed: 49
files_to_load:
  - 01-planning/01-overview.md
  - 01-planning/04-steps.md
---
```

**State Indicators:**
- `session_id` - cross-session continuity
- `last_updated` - recency for most-recent detection
- `current_phase` - explicit phase (better than checkbox inference)
- `next_action` - which skill to load
- `current_section` - granular progress within steps.md
- `tasks_completed` - absolute progress counter

#### 3. `04-steps.md` Checkbox Tracking
```markdown
## Phase 1: Foundation (Utility Tests) ✅
- [x] Create test directory
- [x] Create conftest.py

## Phase 2: Core Logic Tests ✅
- [x] Test determine_context_mode()

## Phase 7: State Understanding ⚠️
- [ ] Review init_project.py
- [ ] Identify patterns
```

**State Indicators:**
- Phase completion symbols (✅ ⚠️)
- Checkbox completion ratio per section
- Section headers for current work area

---

## Improvement Opportunities

### 1. Enhanced Phase Detection

**Current Problem:**
`detect_project_phase()` only checks Phase 1 checkboxes, which doesn't reflect actual state during execution.

**Solution:**
Use `resume-context.md` metadata as primary source:
```python
def detect_project_phase_enhanced(project_dir: str, project_id: str) -> str:
    """Enhanced phase detection using resume-context.md metadata."""

    # Try resume-context.md first (explicit, authoritative)
    resume = load_resume_context(project_dir, project_id)
    if resume and "current_phase" in resume:
        phase = resume["current_phase"]
        skill = resume.get("next_action", "execute-project")
        logging.info(f"Using explicit phase from resume-context: {phase} → {skill}")
        return skill

    # Fallback to checkbox logic
    return detect_project_phase_legacy(project_dir, project_id)
```

**Benefits:**
- Accurate mid-execution state
- Respects manual phase overrides
- Faster (no regex parsing)

### 2. Status-Aware Project Detection

**Current Problem:**
`find_most_recent_project()` returns projects in any state, including COMPLETE.

**Solution:**
Filter by `status` field from overview.md:
```python
def find_most_recent_project_enhanced(project_dir: str,
                                     exclude_complete: bool = True) -> str | None:
    """Find most recent project, optionally excluding COMPLETE."""

    for project_path in projects_dir.iterdir():
        # Read overview.md YAML frontmatter
        overview = project_path / "01-planning" / "01-overview.md"
        if overview.exists():
            status = extract_yaml_field(overview, "status")

            # Skip COMPLETE projects if requested
            if exclude_complete and status == "COMPLETE":
                logging.info(f"Skipping COMPLETE project: {project_path.name}")
                continue

            # Check resume-context.md timestamp...
```

**Benefits:**
- Don't auto-resume finished projects
- Respect project lifecycle
- Better user experience

### 3. Progress-Aware Context Loading

**Current Problem:**
Execution phase always loads same 2 files (`01-overview.md`, `04-steps.md`), regardless of progress.

**Solution:**
Use `current_section` to load relevant working files:
```python
def get_context_files_for_section(project_path: Path,
                                  current_section: int) -> list[str]:
    """Get relevant files based on current section."""

    base_files = [
        "01-planning/01-overview.md",
        "01-planning/04-steps.md"
    ]

    # Section-specific files
    if current_section >= 7:  # State understanding phase
        base_files.append("00-system/skills/projects/plan-project/scripts/init_project.py")

    # Check for section-specific working files
    working_dir = project_path / "03-working"
    if working_dir.exists():
        section_files = list(working_dir.glob(f"section-{current_section}-*.md"))
        base_files.extend([str(f.relative_to(project_path)) for f in section_files])

    return base_files
```

**Benefits:**
- Focused context for current work
- Reduced token usage
- More relevant file loading

### 4. Multi-Project Detection Enhancement

**Current Problem:**
Transcript parsing can detect multiple projects but returns first match.

**Solution:**
Use overview.md `description` field for semantic matching:
```python
def find_project_by_intent(project_dir: str,
                          user_message: str) -> str | None:
    """Match project based on user message and project descriptions."""

    projects = []
    for project_path in (Path(project_dir) / "02-projects").iterdir():
        overview = project_path / "01-planning" / "01-overview.md"
        if overview.exists():
            description = extract_yaml_field(overview, "description")
            name = extract_yaml_field(overview, "name")

            # Semantic matching against user message
            if matches_intent(user_message, name, description):
                projects.append((project_path.name, confidence_score))

    # Return highest confidence match
    return projects[0][0] if projects else None
```

**Benefits:**
- Better project selection from ambiguous input
- Use rich metadata instead of just filenames
- Keyword-based matching from description field

---

## Recommended Changes Priority

### High Priority (Immediate Value)

1. **Use resume-context.md for phase detection**
   - Replace checkbox logic with explicit `current_phase` field
   - Fallback to checkbox if metadata missing
   - File: `session_start.py:208-249`

2. **Filter COMPLETE projects in find_most_recent_project()**
   - Read overview.md status field
   - Skip COMPLETE unless explicitly requested
   - File: `session_start.py:151-206`

### Medium Priority (Quality of Life)

3. **Extract more metadata from resume-context.md**
   - Return full YAML dict, not just `files_to_load`
   - Make `current_section`, `tasks_completed` available
   - File: `session_start.py:252-306`

4. **Section-aware file loading**
   - Use `current_section` to load relevant working files
   - Reduce token waste on irrelevant files
   - File: `session_start.py:495-599` (build_compact_xml)

### Low Priority (Future Enhancement)

5. **Semantic project matching**
   - Use description field for intent-based selection
   - Better multi-project session handling
   - New utility function

6. **Status-based routing**
   - PLANNING → always use plan-project
   - IN_PROGRESS → check phase for skill selection
   - COMPLETE → never auto-load
   - File: `session_start.py:53-148`

---

## Implementation Notes

### Backward Compatibility

All enhancements should gracefully degrade:
- If resume-context.md missing → fallback to checkbox logic
- If overview.md missing status → assume IN_PROGRESS
- If current_section not in resume → use first unchecked task

### Testing Requirements

Each enhancement needs:
- Unit test for happy path
- Test for missing metadata (fallback behavior)
- Test for malformed YAML
- Integration test with real projects

### Performance Impact

Current target: <200ms for session_start.py execution
- Reading overview.md YAML: ~5ms per project
- Parsing resume-context.md: already done
- Minimal impact if we cache parsed YAML

---

## Next Steps

1. **Mark current task complete** - State indicators identified ✓
2. **Document patterns** - Create state detection design doc
3. **Build utility** - Implement enhanced functions
4. **Test** - Validate against test suite projects
5. **Integrate** - Update session_start.py with enhancements

---

**Status**: Analysis complete, ready for documentation phase
