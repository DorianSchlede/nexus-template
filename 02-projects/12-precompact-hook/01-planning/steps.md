# Implementation Steps

## Phase 1: Setup
- [x] Create `.claude/hooks/` directory
- [x] Create `save-resume-state.py` script
- [x] Create `.claude/settings.json` with PreCompact hook config

## Phase 2: Script Implementation
- [x] Read stdin JSON (transcript_path, session_id, trigger)
- [x] Load `00-system/.cache/context_startup.json` for active project
- [x] Parse transcript JSONL for last skill call
- [x] Extract skill name from `--skill X` pattern
- [x] Determine phase from skill name
- [x] Write `_resume.md` with YAML frontmatter

## Phase 3: Testing
- [x] Test manual /compact trigger
- [ ] Test auto compact (fill context)
- [x] Verify _resume.md is updated correctly
- [ ] Test --resume loads correct skill

## Phase 4: Documentation
- [x] Update CLAUDE.md to remove manual update instruction
- [ ] Add hook to system documentation
