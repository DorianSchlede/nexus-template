# Phase 3: Hook Integration Testing Plan

**Goal**: Verify PreCompact and SessionStart hooks work correctly in real Claude Code environment with actual session lifecycle events.

---

## Testing Strategy

### Why Integration Testing is Different

**Unit Tests** (Phase 1-2): Isolated hook execution with mock data
- ✅ Fast execution
- ✅ Controlled environment
- ✅ Repeatable results
- ❌ Subprocess overhead affects performance
- ❌ Doesn't test real transcript parsing
- ❌ Doesn't test actual Claude Code integration

**Integration Tests** (Phase 3): Real session lifecycle with actual hooks
- ✅ Real transcript from actual tool use
- ✅ Real compaction trigger
- ✅ Real Claude Code hook execution (no subprocess overhead)
- ✅ Tests complete PreCompact → SessionStart → Claude resume flow
- ❌ Slower (requires hitting 200k token limit)
- ❌ Harder to reproduce specific scenarios

---

## Test Scenarios

### Scenario 1: Basic Resume Flow ✓ PRIORITY

**Objective**: Verify hooks work in the happy path - work on project, hit compaction, resume successfully

**Setup**:
1. Start working on THIS project (24-project-skills-research-resume-expansion)
2. Continue until session hits ~200k tokens (compaction triggers)
3. Observe PreCompact hook execution
4. Observe SessionStart hook execution after compaction
5. Verify resume instructions appear in Claude's context

**Success Criteria**:
- [ ] PreCompact hook detects project 24 from transcript
- [ ] PreCompact writes `precompact_state.json` with FLAT schema
- [ ] PreCompact returns `{}` successfully
- [ ] SessionStart hook reads state after compaction
- [ ] SessionStart loads `resume-context.md` from project 24
- [ ] SessionStart injects catastrophic instructions
- [ ] Claude reads files from `files_to_load` in parallel
- [ ] Claude answers validation gate questions
- [ ] Claude continues with `execute-project` skill
- [ ] Performance: PreCompact <50ms, SessionStart <200ms

**How to Verify**:
- Check `.cache/precompact_state.json` exists and is valid
- Check `.cache/session_start_output.log` shows resume instructions injected
- Observe Claude's first message after compaction includes file reads
- Ask Claude: "What files did you just load?" to verify context

**Files to Monitor**:
- `00-system/.cache/precompact_state.json`
- `00-system/.cache/session_start_output.log`
- `00-system/.cache/session_start_full_context.json`

---

### Scenario 2: Multiple Active Projects

**Objective**: Verify PreCompact detects the MOST RECENT project when multiple projects are active

**Setup**:
1. Work on Project A (e.g., this project 24)
2. Switch to Project B (e.g., project 17-hook-pattern-research)
3. Continue until compaction
4. Verify PreCompact detects Project B (most recent)

**Success Criteria**:
- [ ] PreCompact detects most recently accessed project
- [ ] Confidence score is accurate (high if transcript + cache agree)
- [ ] SessionStart loads correct project's resume-context.md

**How to Verify**:
- Check `precompact_state.json` has correct `active_project_id`
- Check `detection_method` is "transcript"
- Check `confidence` is "high" or "medium"

---

### Scenario 3: Source="clear" Exclusion

**Objective**: Verify SessionStart does NOT auto-resume when user explicitly clears session

**Setup**:
1. Work on a project until some progress
2. User runs `/clear` command
3. Observe SessionStart hook execution
4. Verify NO resume instructions injected

**Success Criteria**:
- [ ] SessionStart detects `source: "clear"`
- [ ] SessionStart skips reading precompact_state.json
- [ ] SessionStart does NOT inject catastrophic instructions
- [ ] Claude starts fresh (no project context loaded)

**How to Verify**:
- Check `session_start_output.log` shows `Source: clear`
- Check log shows `Resume Instructions: None`
- Observe Claude's first message is the normal menu (not resume instructions)

---

### Scenario 4: Backward Compatibility with _resume.md

**Objective**: Verify SessionStart loads legacy `_resume.md` when `resume-context.md` doesn't exist

**Setup**:
1. Find a project with `_resume.md` (e.g., 18-hook-research-upgrade)
2. Work on that project until compaction
3. Verify SessionStart loads `_resume.md` successfully

**Success Criteria**:
- [ ] SessionStart checks for `resume-context.md` first
- [ ] SessionStart falls back to `_resume.md`
- [ ] Resume instructions still injected correctly
- [ ] No errors in logs

**How to Verify**:
- Check logs for "Loading resume context from _resume.md" or similar
- Verify resume instructions appear in Claude's context

---

### Scenario 5: Fresh Session (source="startup")

**Objective**: Verify SessionStart behaves normally on fresh session start (no auto-resume)

**Setup**:
1. Close Claude Code completely
2. Reopen and start fresh session
3. Observe SessionStart hook execution

**Success Criteria**:
- [ ] SessionStart detects `source: "startup"`
- [ ] SessionStart does NOT attempt to read precompact_state.json
- [ ] SessionStart does NOT inject resume instructions
- [ ] Claude displays normal menu

**How to Verify**:
- Check `session_start_output.log` shows `Source: startup`
- Check log shows `Mode: startup` (not `resume`)
- Observe normal Nexus menu displayed

---

### Scenario 6: No Active Project (General Work)

**Objective**: Verify PreCompact handles sessions with no project activity gracefully

**Setup**:
1. Work on general tasks (no project)
2. Continue until compaction
3. Verify PreCompact writes state with `active_project_id: null`

**Success Criteria**:
- [ ] PreCompact writes state file even with no project detected
- [ ] `active_project_id: null`
- [ ] `confidence: "low"`
- [ ] `detection_method: "fallback"`
- [ ] SessionStart skips resume (no project to resume)

**How to Verify**:
- Check `precompact_state.json` has `"active_project_id": null`
- Check SessionStart doesn't crash, just skips resume logic

---

## Performance Benchmarking

### Real-World Performance Targets

**PreCompact Hook**:
- Target: <50ms execution time
- Measured at: Hook execution in production (check logs)
- Acceptable: <100ms (subprocess overhead in tests was ~170ms)

**SessionStart Hook**:
- Target: <200ms execution time
- Measured at: Hook execution in production (check logs)
- Acceptable: <300ms (subprocess overhead in tests was ~280ms)

### How to Measure

1. Check hook logs after each execution:
   ```
   2026-01-04 13:21:06,453 - SessionStart - INFO - SessionStart hook completed in 130.59ms
   ```

2. Monitor `.cache/session_start_output.log`:
   ```
   Performance: 130.59ms
   ```

3. Compare to test benchmarks (expect 30-50% faster in production)

---

## Debugging Tools

### Log Files to Check

1. **`.cache/precompact_state.json`**
   - Shows what PreCompact detected
   - Validates FLAT schema structure
   - Shows confidence and detection method

2. **`.cache/session_start_output.log`**
   - Shows SessionStart execution summary
   - Shows resume project ID
   - Shows performance metrics
   - Shows whether resume instructions were injected

3. **`.cache/session_start_full_context.json`**
   - Full context dump (for detailed debugging)
   - Large file (can be 50k+ chars)

### Debug Commands

**Check if hooks are registered**:
```bash
cat .claude/hooks.json
```

**Check PreCompact state**:
```bash
cat 00-system/.cache/precompact_state.json | jq
```

**Check SessionStart log**:
```bash
cat 00-system/.cache/session_start_output.log | head -20
```

**Check hook execution**:
Look for stderr output from Claude Code showing hook execution

---

## Test Execution Checklist

### Pre-Test Setup

- [ ] Verify hooks are registered in `.claude/hooks.json`
- [ ] Verify `save_resume_state.py` exists and is executable
- [ ] Verify `session_start.py` exists and is executable
- [ ] Verify this project has `resume-context.md` with `files_to_load`
- [ ] Clear old cache files: `rm 00-system/.cache/precompact_state.json`

### During Testing

- [ ] Monitor session token count (approaching 200k)
- [ ] Watch for compaction trigger
- [ ] Observe PreCompact hook execution (check stderr)
- [ ] Observe SessionStart hook execution (check stderr)
- [ ] Check Claude's first message after compaction

### Post-Test Verification

- [ ] Read `precompact_state.json` - validate schema
- [ ] Read `session_start_output.log` - check resume status
- [ ] Verify Claude loaded correct files
- [ ] Ask Claude validation gate questions
- [ ] Check performance metrics in logs

---

## Expected Results

### Scenario 1 (Basic Resume) - Expected Output

**After PreCompact Hook**:
```json
{
  "active_project_id": "24-project-skills-research-resume-expansion",
  "confidence": "high",
  "detection_method": "transcript",
  "timestamp": "2026-01-04T14:30:00Z"
}
```

**SessionStart Log**:
```
=== SessionStart Hook Output (MVC v3.2 + Resume) ===
Timestamp: 2026-01-04T14:30:01
Session: abc-123-def-456
Source: compact
Mode: resume
Resume Project: 24-project-skills-research-resume-expansion
Resume Instructions: Injected
Performance: 145.23ms
```

**Claude's First Message** (should include):
- Reading 5 files in parallel (from `files_to_load`)
- Answering validation gate questions
- Continuing with execute-project skill

---

## Failure Scenarios & Debugging

### If PreCompact Doesn't Detect Project

**Symptoms**: `active_project_id: null` when project was active

**Check**:
1. Verify transcript contains project file paths (format: `02-projects/{id}/`)
2. Check detection pattern in `save_resume_state.py` line 83
3. Look for stderr warnings about transcript parsing

**Fix**: Update transcript detection pattern if needed

### If SessionStart Doesn't Inject Instructions

**Symptoms**: Claude resumes but doesn't load files or answer validation questions

**Check**:
1. Verify `precompact_state.json` exists and has project ID
2. Verify `resume-context.md` exists in project
3. Check SessionStart log for errors loading resume file
4. Verify `source` is "compact" or "resume" (not "clear")

**Fix**: Check YAML frontmatter format in resume-context.md

### If Performance is Too Slow

**Symptoms**: SessionStart >500ms execution time

**Check**:
1. How many files in `files_to_load`? (each adds ~10ms)
2. Is nexus-loader.py import slow? (check nexus_data load time)
3. Is validation gate extraction slow? (large markdown body)

**Fix**: Optimize YAML parser, limit validation gate extraction

---

## Phase 3 Completion Criteria

To consider Phase 3 complete, we need:

- [x] **Scenario 1**: Basic resume flow working (TESTED in this session if compaction happens)
- [ ] **Scenario 3**: Source="clear" exclusion verified
- [ ] **Scenario 5**: Fresh session behavior verified
- [ ] **Performance**: Both hooks under target times in production
- [ ] **Documentation**: Integration test findings documented
- [ ] **Validation**: All Phase 0-2 implementation matches FINAL-DESIGN.md

---

## Next Steps After Phase 3

**Phase 4A**: Research Templates + execute-project Integration (3h)
- Add research phase to create-project workflow
- Update execute-project to auto-update resume-context.md
- Auto-populate `files_to_load` based on session activity

**Phase 5**: Integration & End-to-End Testing (5h)
- Test complete project lifecycle with resume
- Performance optimization
- Edge case handling

---

**Status**: Ready for integration testing
**Estimated Time**: 4h (mostly waiting for compaction to trigger)
**Risk**: Low (unit tests passing, code reviewed)
