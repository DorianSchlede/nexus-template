# Implementation Steps

## Phase 1: Setup
- [ ] Create `.claude/hooks/` directory
- [ ] Create `save-resume-state.py` script
- [ ] Create `.claude/settings.json` with PreCompact hook config

## Phase 2: Script Implementation
- [ ] Read stdin JSON (transcript_path, session_id, trigger)
- [ ] Load `00-system/.cache/context_startup.json` for active project
- [ ] Parse transcript JSONL for last skill call
- [ ] Extract skill name from `--skill X` pattern
- [ ] Determine phase from skill name
- [ ] Write `_resume.md` with YAML frontmatter

## Phase 3: Testing
- [ ] Test manual /compact trigger
- [ ] Test auto compact (fill context)
- [ ] Verify _resume.md is updated correctly
- [ ] Test --resume loads correct skill

## Phase 4: Documentation
- [ ] Update CLAUDE.md to remove manual update instruction
- [ ] Add hook to system documentation
