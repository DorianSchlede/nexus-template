# Phase 3 Production Validation Checklist

**Status**: Awaiting Natural Compaction Event (will occur at ~200k tokens)
**Created**: 2026-01-04
**Implementation**: Complete ✅
**Testing**: All tests passing ✅
**Documentation**: Updated ✅

---

## What Will Happen at Next Compaction

### 1. PreCompact Hook Execution (<50ms)
- [ ] Hook fires before conversation is compacted
- [ ] Parses transcript JSONL for active project detection
- [ ] Writes `00-system/.cache/precompact_state.json` with FLAT schema:
  ```json
  {
    "active_project_id": "24-project-skills-research-resume-expansion",
    "confidence": "high",
    "detection_method": "transcript",
    "timestamp": "2026-01-04T..."
  }
  ```
- [ ] Returns `{}` (empty object)
- [ ] No Windows path expansion errors (fixed in Session 13)

### 2. Compaction Event
- [ ] Conversation summarized at ~200k tokens
- [ ] Context reset
- [ ] Session resumes

### 3. SessionStart Hook Execution (<200ms)
- [ ] Hook fires on session start
- [ ] Receives `source: "compact"` from Claude Code
- [ ] Detects should_resume = True (source not "clear")
- [ ] Reads `precompact_state.json` with FLAT schema
- [ ] Extracts `active_project_id = "24-project-skills-research-resume-expansion"`
- [ ] Loads `resume-context.md` from project
- [ ] Parses YAML frontmatter for `files_to_load[]` and `next_action` fields
- [ ] **AUTO-LOADS 9 FILES** (~104,335 chars):
  - System files (3):
    - `00-system/core/orchestrator.md` (12k)
    - `00-system/system-map.md` (3.7k)
    - `04-workspace/workspace-map.md` (4.4k)
  - Project files (5):
    - `01-planning/overview.md`
    - `01-planning/plan.md`
    - `01-planning/steps.md`
    - `02-resources/FINAL-DESIGN.md`
    - `02-resources/resume-state-REVISED.md`
  - Skill file (1):
    - `00-system/skills/projects/execute-project/SKILL.md` (18.8k)
- [ ] Builds **SIMPLIFIED INSTRUCTIONS** (no STEP 1/2/3 warnings)
- [ ] Injects complete context via `additionalContext`

### 4. AI Receives Context
- [ ] All 9 files already loaded in context (3 system + 5 project + 1 skill)
- [ ] System context available (orchestrator, system-map, workspace-map)
- [ ] Project context available (all planning files)
- [ ] Skill workflow available (execute-project SKILL.md)
- [ ] Simplified resume instructions visible
- [ ] No validation questions needed
- [ ] No manual file loading ceremony
- [ ] Can immediately execute work using pre-loaded skill

---

## Success Criteria

**✅ Compaction Detected**:
- PreCompact hook wrote state file
- No execution errors or timeouts
- State file contains correct project ID

**✅ Auto-Loading Worked**:
- SessionStart hook read state file correctly
- All 9 files loaded successfully:
  - 3 system files (orchestrator, system-map, workspace-map)
  - 5 project files (from `files_to_load[]`)
  - 1 skill file (from `next_action`)
- Combined content (~105k chars) injected into additionalContext
- No file read errors or Unicode issues

**✅ Simplified Instructions**:
- Instructions contain "POST-COMPACTION RESUME - CONTEXT AUTO-LOADED"
- Instructions contain "All project files have been auto-loaded above"
- Instructions do NOT contain "STEP 1", "STEP 2", "STEP 3"
- Instructions do NOT contain forceful warnings

**✅ Seamless Continuation**:
- AI has complete system context (behavior rules, navigation, workspace)
- AI has complete project context (all planning files)
- AI has complete skill workflow (SKILL.md already loaded)
- AI can immediately continue work from exact point
- No context loss or re-explanation needed
- No manual skill loading required

---

## What to Check

1. **Hook Logs** (if accessible):
   ```
   .claude/.logs/session_start.log
   .claude/.logs/save_resume_state.log
   ```

2. **State File**:
   ```
   00-system/.cache/precompact_state.json
   ```

3. **Session Start Output** (check additionalContext):
   - Should contain ~105,261 chars of content
   - Should include all 9 files inline (3 system + 5 project + 1 skill)
   - Should have simplified header
   - Should show "All context has been pre-loaded"

4. **AI Behavior**:
   - Does AI immediately understand project context?
   - Does AI ask to read files manually?
   - Does AI continue from correct task?

---

## Potential Issues & Mitigations

| Issue | Mitigation |
|-------|-----------|
| PreCompact timeout (>50ms) | Optimize transcript parsing |
| SessionStart timeout (>200ms) | Reduce file reading overhead |
| File not found errors | Check `files_to_load[]` paths are correct |
| Unicode encoding errors | Already fixed - emojis removed |
| Windows path issues | Already fixed - relative paths |

---

## Post-Validation Actions

If validation succeeds:
- [ ] Mark production validation complete in steps.md
- [ ] Document any unexpected behavior
- [ ] Note actual execution times (PreCompact/SessionStart)
- [ ] Consider Phase 4A (Research Templates) if desired

If validation fails:
- [ ] Document failure mode in detail
- [ ] Check hook logs for errors
- [ ] Verify state file structure
- [ ] Test with simplified project (fewer files)
- [ ] Debug and fix issues

---

**Status**: Ready for Production Validation ✅

**Next Event**: Will occur naturally when conversation reaches ~200k tokens (currently at ~68k tokens, ~131k remaining)

**Estimated Time to Next Compaction**: Depends on conversation length - could be this session or several sessions from now
