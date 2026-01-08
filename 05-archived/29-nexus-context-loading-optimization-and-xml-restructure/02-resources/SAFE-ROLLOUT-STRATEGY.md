# Safe Rollout Strategy - Zero Risk Implementation

**Mental Models Applied**: Margin of Safety, Risk Mitigation, Incremental Validation

---

## 🎯 Core Principle: Test in Isolation, Validate Before Integration

**Rule**: Each change must be:
1. **Testable independently** (no dependencies)
2. **Reversible instantly** (git branch per change)
3. **Validated before next step** (measure, don't assume)

---

## 📦 Project Split (5 Separate Projects)

### Project 29A: Skill Description Updates (SAFE - No Code)
**Risk**: ⭐ VERY LOW (just text changes)

**What**:
- Update ~100 SKILL.md descriptions to 15-20 words
- No Python code touched
- No system files modified

**Test**:
- Search for skill descriptions in orchestrator/loader
- Verify they still load correctly
- Check routing accuracy with sample inputs

**Rollback**: `git checkout -- 03-skills/` (instant)

**Duration**: 1-2 days

**Success Criteria**:
- All skills have 15-20 word descriptions
- Routing still works (test 20 inputs)
- No errors in session_start hook

---

### Project 29B: Orchestrator Philosophy Update (SAFE - Text Only)
**Risk**: ⭐ LOW (behavior guidance, no logic)

**What**:
- Deploy orchestrator-v6.xml → 00-system/core/orchestrator.md
- Only philosophy section changes (7 principles)
- No routing logic changes yet

**Test**:
- Start new session
- Verify orchestrator loads
- Check Claude exhibits new behaviors (Complete Over Perfect, Context-Aware)
- Test 10 interactions

**Rollback**: `git checkout -- 00-system/core/orchestrator.md` (instant)

**Duration**: 1 day

**Success Criteria**:
- Orchestrator loads without errors
- Claude shows improved behavior quality
- No routing breakage

---

### Project 29C: Routing Priority Fix (MEDIUM RISK - Core Logic)
**Risk**: ⭐⭐ MEDIUM (routing is critical path)

**What**:
- Update orchestrator.md routing section only
- Change Priority 1: System → Priority 2: User
- Nothing else changes

**Test Strategy**:
1. Create test skill in 03-skills/ named "close-session" (conflict test)
2. Try to trigger it → Should load system skill instead
3. Test 50 routing scenarios (system, user, projects)
4. Verify close-session, setup-memory, validate-system still work

**Rollback**: `git checkout -- 00-system/core/orchestrator.md` (instant)

**Duration**: 1 day

**Success Criteria**:
- System skills take priority (tested with conflict)
- User skills still load when no conflict
- All core utilities work (close-session, setup-memory)
- Routing accuracy ≥95%

---

### Project 29D: State Template Functions (MEDIUM RISK - Hook Logic)
**Risk**: ⭐⭐ MEDIUM (modifies session_start hook)

**What**:
- Add state-template-functions.py to loaders.py
- Modify build_startup_xml() to use new templates
- Replace static instruction templates

**Implementation Steps** (INCREMENTAL):

**Step 1**: Add functions, don't use them yet
```python
# In loaders.py - just add the functions
def build_next_action_instruction(context):
    # ... implementation
```
**Test**: Import works, no errors

**Step 2**: Use new functions in parallel (A/B test)
```python
# Generate both old and new
old_instruction = load_instruction_template("startup_menu")
new_instruction = build_next_action_instruction(context)

# Log both for comparison (don't use new yet)
logger.debug(f"Old: {old_instruction}")
logger.debug(f"New: {new_instruction}")
```
**Test**: Compare outputs, verify new matches expected

**Step 3**: Switch to new, keep old as fallback
```python
try:
    instruction = build_next_action_instruction(context)
except Exception as e:
    logger.error(f"New template failed: {e}")
    instruction = load_instruction_template("startup_menu")  # Fallback
```
**Test**: 5 sessions in each state, verify correct template selected

**Step 4**: Remove old templates (only after validation)

**Rollback**: `git checkout -- .claude/hooks/session_start.py 00-system/core/nexus/loaders.py`

**Duration**: 2-3 days

**Success Criteria**:
- All 5 states tested (onboarding, active, workspace, fresh, ready)
- MECE compliance verified (no overlap)
- Hook execution time <200ms
- Menu displays correctly

---

### Project 29E: CLI Discovery Implementation (LOW RISK - Optional Feature)
**Risk**: ⭐ LOW (new feature, doesn't break existing)

**What**:
- Implement load-skill CLI command
- Add to loaders.py

**Implementation**:
```python
def handle_load_skill_command(category: str, args: str = "") -> str:
    """Execute load-skill {category} --help"""
    if args == "--help":
        # Scan 03-skills/{category}/
        # Read all SKILL.md files
        # Return formatted list
```

**Test**:
- Run `load-skill langfuse --help`
- Verify returns 28 skills (not auto-loaded)
- Check formatting is readable
- Test with all integration categories

**Rollback**: Remove function (feature flag it first)

**Duration**: 1 day

**Success Criteria**:
- CLI works for all categories
- Prevents auto-loading spam
- Returns clean formatted output

---

## 🔒 Safety Mechanisms

### 1. Git Branch Strategy
```bash
# Each project gets its own branch
git checkout -b project-29a-skill-descriptions
git checkout -b project-29b-orchestrator-philosophy
git checkout -b project-29c-routing-priority
git checkout -b project-29d-state-templates
git checkout -b project-29e-cli-discovery

# Merge only after validation
```

### 2. Feature Flags
```python
# In loaders.py
USE_NEW_STATE_TEMPLATES = os.getenv("NEXUS_USE_NEW_TEMPLATES", "false") == "true"

if USE_NEW_STATE_TEMPLATES:
    instruction = build_next_action_instruction(context)
else:
    instruction = load_instruction_template("startup_menu")
```

### 3. Logging & Monitoring
```python
import time

start = time.perf_counter()
# ... hook execution
duration = time.perf_counter() - start

if duration > 0.2:
    logger.warning(f"Hook took {duration:.3f}s (target <0.2s)")
```

### 4. Golden Dataset Testing
Create `test-inputs.json`:
```json
[
  {"input": "build api integration", "expected": "plan-project"},
  {"input": "continue project 29", "expected": "execute-project"},
  {"input": "send slack message", "expected": "slack-send-message"},
  {"input": "close session", "expected": "close-session"},
  ...
]
```

Run after EVERY change:
```python
def test_routing_accuracy():
    golden_dataset = load_golden_dataset()
    correct = 0
    for test in golden_dataset:
        result = route_user_input(test["input"])
        if result == test["expected"]:
            correct += 1
    accuracy = correct / len(golden_dataset)
    assert accuracy >= 0.95, f"Routing accuracy {accuracy:.1%} below 95% threshold"
```

---

## 📊 Risk Matrix

| Project | Risk | Impact if Failed | Rollback Time | Dependencies |
|---------|------|------------------|---------------|--------------|
| 29A - Skill Descriptions | ⭐ Very Low | Minor (search less accurate) | Instant | None |
| 29B - Philosophy | ⭐ Low | Minor (behavior quality) | Instant | None |
| 29C - Routing Priority | ⭐⭐ Medium | **CRITICAL** (system breaks) | Instant | None |
| 29D - State Templates | ⭐⭐ Medium | High (menu broken) | Instant | None |
| 29E - CLI Discovery | ⭐ Low | None (optional feature) | Instant | None |

---

## 📅 Recommended Sequence

**Week 1**:
- **Day 1-2**: Project 29A (Skill Descriptions) - Safe warmup
- **Day 3**: Project 29B (Philosophy) - Low risk, high value

**Week 2**:
- **Day 4**: Project 29C (Routing Priority) - **CRITICAL**, test extensively
- **Day 5**: Validation day (test routing with 50+ inputs)

**Week 3**:
- **Day 6-8**: Project 29D (State Templates) - Incremental, 4 steps
- **Day 9**: Validation day (test all 5 states)

**Week 4**:
- **Day 10**: Project 29E (CLI Discovery) - Optional, low risk
- **Day 11-12**: Final integration testing, documentation

---

## ✅ Validation Checklist (Run After Each Project)

**After 29A** (Skill Descriptions):
- [ ] All SKILL.md files have 15-20 word descriptions
- [ ] No YAML frontmatter errors
- [ ] Skills still load in session_start hook
- [ ] Routing test: 20 inputs, 100% accuracy

**After 29B** (Philosophy):
- [ ] Orchestrator loads without errors
- [ ] New session displays menu correctly
- [ ] Claude exhibits quality behaviors (test 10 interactions)
- [ ] No routing changes (same test inputs work)

**After 29C** (Routing Priority):
- [ ] Create conflict test (03-skills/close-session/)
- [ ] System skill loads (not user skill)
- [ ] Test 50 routing scenarios
- [ ] Core utilities work (close-session, setup-memory, validate-system)
- [ ] Routing accuracy ≥95%

**After 29D** (State Templates):
- [ ] All 5 states tested (onboarding, active, workspace, fresh, ready)
- [ ] MECE compliance (no overlap, all cases covered)
- [ ] Hook execution <200ms
- [ ] Menu displays correctly in all states
- [ ] Dynamic instructions make sense

**After 29E** (CLI Discovery):
- [ ] `load-skill langfuse --help` works
- [ ] Returns 28 skills (not auto-loaded)
- [ ] Test all integration categories
- [ ] Formatting is clean and readable

---

## 🚨 Stop Conditions (When to HALT)

**STOP immediately if**:
- Hook execution time >300ms
- Routing accuracy drops below 90%
- Session_start hook crashes (any error)
- Close-session stops working (critical data loss risk)
- Any error in logs during normal operation

**When stopped**:
1. Rollback to previous working state (git checkout)
2. Analyze logs to understand failure
3. Fix issue in isolated branch
4. Test fix independently
5. Re-attempt after validation

---

## 💾 Backup Strategy

**Before starting ANY project**:
```bash
# Tag current working state
git tag nexus-pre-optimization-$(date +%Y%m%d)
git push origin --tags

# Create safety branch
git checkout -b nexus-stable-backup
git push origin nexus-stable-backup

# Now safe to work on feature branches
```

**If everything breaks**:
```bash
git checkout nexus-stable-backup
# System restored to pre-optimization state
```

---

## 🎯 Success Metrics (Overall)

**Must Achieve**:
- [ ] Token reduction ≥30% in STARTUP mode
- [ ] Routing accuracy ≥95%
- [ ] Hook execution <200ms
- [ ] Zero session_start crashes (1000 sessions)
- [ ] All core utilities work (close-session, setup-memory, etc.)

**Nice to Have**:
- [ ] User feedback positive (subjective quality improvement)
- [ ] Session summaries show better planning behavior
- [ ] Mental models used more frequently

---

## 📝 Summary

**Why This Works**:
✅ **Incremental**: Each project independent, small scope
✅ **Testable**: Clear success criteria per project
✅ **Reversible**: Instant rollback via git
✅ **Safe**: Low-risk first, critical changes isolated
✅ **Validated**: Test after every step, not at the end

**Timeline**: ~2-3 weeks with validation
**Risk**: Minimized through isolation + testing
**Rollback**: Always instant (git checkout)

---

**Next**: Create 5 separate project folders OR execute sequentially with branches?
