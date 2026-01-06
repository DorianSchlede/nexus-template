# Handover Test Suite - Plan

**Last Updated**: 2026-01-05

---

## Context

**Load Before Reading**:
- `01-planning/01-overview.md` - Purpose and success criteria
- `01-planning/02-discovery.md` - Dependencies discovered

---

## Approach

**Test-First, Layered Architecture**:
1. Start with utility functions (no external deps) → `xml.py`, `transcript.py`
2. Then test core logic functions → `session_start.py` functions
3. Finally integration tests → full handover flow

**Mocking Strategy**:
- Use `tempfile.TemporaryDirectory()` for file system isolation
- Mock `nexus.loaders` imports to avoid external dependencies
- Create fixture factories for common test data (projects, transcripts)

---

## Key Decisions

| Decision | Choice | Why |
|----------|--------|-----|
| Test framework | pytest | Better fixtures, parameterized tests, cleaner assertions |
| File isolation | tempfile | Cross-platform, auto-cleanup, no side effects |
| Nexus imports | Mock/patch | Avoid coupling tests to nexus core changes |
| Test location | `.claude/hooks/tests/` | Co-located with code under test |

---

## Dependencies & Links

*Auto-populated from 02-discovery.md*

**Files Under Test**:
- `.claude/hooks/session_start.py` - Main handover logic
- `.claude/hooks/save_resume_state.py` - PreCompact hook
- `.claude/hooks/utils/transcript.py` - Transcript parsing
- `.claude/hooks/utils/xml.py` - XML utilities

**Files to Create**:
- `.claude/hooks/tests/test_session_start.py`
- `.claude/hooks/tests/test_transcript_utils.py`
- `.claude/hooks/tests/test_xml_utils.py`
- `.claude/hooks/tests/test_handover_integration.py`
- `.claude/hooks/tests/conftest.py`

---

## Technical Architecture

**Test Structure**:
```
.claude/hooks/tests/
├── conftest.py              # Shared fixtures
├── test_xml_utils.py        # XML escaping, building
├── test_transcript_utils.py # Transcript parsing
├── test_session_start.py    # Core handover logic
├── test_save_resume.py      # PreCompact hook
└── test_integration.py      # End-to-end flows
```

**Fixture Factories**:
- `create_project_structure(project_id, status, phase)` - Mock project dirs
- `create_transcript(entries)` - Mock JSONL transcript
- `create_resume_context(session_id, files_to_load)` - Mock resume file

---

## Implementation Strategy

**Phase 1: Foundation** (utility tests)
- `test_xml_utils.py` - escape functions, load_file_to_xml
- `test_transcript_utils.py` - project detection, skill switch

**Phase 2: Core Logic** (session_start tests)
- `test_session_start.py::TestDetermineContextMode` - All 10 cases
- `test_session_start.py::TestProjectPhaseDetection` - Planning vs execution
- `test_session_start.py::TestResumeContextLoading` - YAML parsing

**Phase 3: Integration**
- `test_integration.py` - Full flow: compact → detect → build XML

**Testing Approach**:
- Parameterized tests for the 10 context mode cases
- Edge case coverage (empty dirs, missing files, invalid YAML)
- Cross-platform path handling validation

---

## Test Case Matrix

### `determine_context_mode()` - 10 Cases

| Case | Source | Project | Skill Switch | Expected Mode | Expected Action |
|------|--------|---------|--------------|---------------|-----------------|
| 1 | new | - | - | startup | display_menu |
| 2 | compact | yes | no | compact | continue_working |
| 3 | compact | yes | no | compact | continue_working |
| 4 | compact | yes | yes | startup | continue_working |
| 5 | compact | no | - | startup | continue_working |
| 6 | compact | no | - | startup | continue_working |
| 7 | compact | yes (chat) | no | compact | continue_working |
| 8 | resume | yes | - | compact | continue_working |
| 9 | resume | yes | - | compact | continue_working |
| 10 | resume | no | - | startup | display_menu |

---

## Open Questions

- [x] Mock nexus.loaders or run with real imports? → **Mock** (isolation)
- [ ] Delete outdated test_save_resume_state.py after new tests pass?

---

*Next: Break down execution in 04-steps.md*
