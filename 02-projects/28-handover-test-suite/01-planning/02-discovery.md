# Discovery

**Time**: 15 min | **Purpose**: Surface dependencies before planning

---

## Dependencies

*Files, systems, APIs this project will touch*

**Files to Test (Primary)**:
- `.claude/hooks/session_start.py` - Main handover logic (912 lines)
- `.claude/hooks/save_resume_state.py` - PreCompact hook for saving state (176 lines)
- `.claude/hooks/utils/transcript.py` - Transcript parsing utilities (213 lines)
- `.claude/hooks/utils/xml.py` - XML building utilities (156 lines)

**Files to Create**:
- `.claude/hooks/tests/test_session_start.py` - Core session start tests
- `.claude/hooks/tests/test_transcript_utils.py` - Transcript parsing tests
- `.claude/hooks/tests/test_xml_utils.py` - XML utility tests
- `.claude/hooks/tests/test_handover_integration.py` - End-to-end integration tests
- `.claude/hooks/tests/conftest.py` - Shared fixtures (projects, transcripts, mock fs)

**External Systems**:
- File system (temp directories for mock projects)
- JSON/JSONL transcript files (mock)

---

## Existing Patterns

*Skills, templates, code to reuse*

**Related Tests (Existing)**:
- `test_save_resume_state.py` - 250 lines, good patterns for mocking
  - Uses `tempfile.TemporaryDirectory()` for isolated file operations
  - Uses `unittest.mock.patch` for env var overrides
  - Has integration test class pattern

**Code Patterns to Reuse**:
- `test_save_resume_state.py:TestIntegration` - Full flow test pattern
- Transcript fixture pattern with mock JSONL data
- Project directory structure creation

**Key Functions to Test**:
1. `determine_context_mode()` - 10 cases documented in docstring
2. `find_project_by_session_id()` - session_id matching
3. `find_most_recent_project()` - timestamp-based detection
4. `detect_project_phase()` - Phase 1 completion check
5. `load_resume_context()` - YAML frontmatter parsing
6. `build_startup_xml()` - Full startup context
7. `build_compact_xml()` - Compact continuation context
8. From `utils/transcript.py`:
   - `parse_transcript_for_project()` - tool_use extraction
   - `check_skill_switch_after_project()` - skill switch detection
9. From `utils/xml.py`:
   - `escape_xml_content()` / `escape_xml_attribute()`
   - `load_file_to_xml()`

---

## Risks & Unknowns

*What could derail? What don't we know?*

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Import dependencies (nexus.loaders etc.) | High | Mock or skip full XML build tests |
| Windows path handling | Medium | Use pathlib consistently |
| Performance tests (200ms budget) | Low | Use time.perf_counter() |
| Mock complexity for nested XML | Medium | Test components separately first |

**Open Questions**:
- [x] Does existing test_save_resume_state.py match current implementation? → NO, outdated
- [ ] Do we need to mock external imports (nexus.loaders)?

---

*→ Auto-populate plan.md Dependencies section from findings above*
