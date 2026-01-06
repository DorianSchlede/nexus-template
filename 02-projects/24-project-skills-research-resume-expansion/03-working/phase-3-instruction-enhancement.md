# Phase 3: Resume Instructions Enhancement

**Date**: 2026-01-04
**Session**: Post-Compaction (bcd0ba35-5a6a-4199-a817-9225db396404)
**Issue**: AI ignored resume instructions and responded to user question immediately

---

## Problem

After the compaction/resume event, the SessionStart hook successfully injected resume instructions into context:

```markdown
# MANDATORY: Resume Project After Compaction

## STEP 1: Load Required Files
You MUST read these files IN PARALLEL...

## STEP 2: Validation Gate
Before continuing, you MUST verify you understand...

## STEP 3: Execute Skill
After loading files and answering validation questions, execute...
```

**However**: The AI completely ignored these instructions and jumped straight to responding to the user's question about the compaction error.

**Why This Happened**: The instructions used polite language ("MUST", "MANDATORY") which the AI interpreted as strong suggestions rather than absolute requirements. The AI's helpful instinct to answer user questions immediately overrode the loading instructions.

---

## Root Cause Analysis

### AI Behavior Pattern

The AI received:
1. ✅ Resume instructions via `additionalContext` (SessionStart hook)
2. ❌ User question: "this was whats in precompact state... is that correct based on..."
3. ❌ AI decision: Answer user question FIRST, ignore loading instructions

**Why the AI chose wrong**:
- Instructions were too polite ("MUST read" vs "DO NOT RESPOND UNTIL")
- No explicit consequences stated
- No visual emphasis (warnings, symbols)
- Helpful instinct prioritized immediate user assistance over context loading

### Expected Behavior

The AI should have:
1. ✅ Recognized post-compaction resume scenario
2. ✅ Read all 5 files in parallel FIRST
3. ✅ Answered 4 validation questions
4. ✅ THEN responded to user question with full context

---

## The Fix

### Before (Too Polite)

```markdown
# MANDATORY: Resume Project After Compaction

## STEP 1: Load Required Files

You MUST read these files IN PARALLEL (use multiple Read tool calls in one message):

## STEP 2: Validation Gate

Before continuing, you MUST verify you understand:

## STEP 3: Execute Skill

After loading files and answering validation questions, execute:

**CRITICAL**: Do NOT skip Steps 1-2. Loading context is MANDATORY for project continuation.
```

**Problems**:
- ❌ Starts with "MANDATORY" (suggestion-level language)
- ❌ Uses "MUST" (AI interprets as strong preference, not requirement)
- ❌ Warning at END (AI already started responding)
- ❌ No visual emphasis (no symbols, all looks like regular text)
- ❌ No explicit "DO NOT RESPOND" directive

---

### After (IMPOSSIBLE TO IGNORE)

```markdown
# ⚠️ CRITICAL: STOP AND READ THIS FIRST ⚠️

## THIS IS A POST-COMPACTION RESUME - YOU MUST RELOAD CONTEXT

**DO NOT RESPOND TO THE USER UNTIL YOU COMPLETE ALL 3 STEPS BELOW**

---

**Project Detected**: {project_name} ({project_id})
**Phase**: {current_phase}
**Progress**: {progress}

## ⚠️ STEP 1: LOAD REQUIRED FILES IMMEDIATELY ⚠️

**BEFORE doing ANYTHING else**, you MUST read these files IN PARALLEL (use multiple Read tool calls in one message):

- `{files}`

## ⚠️ STEP 2: ANSWER VALIDATION QUESTIONS ⚠️

{validation_gate}

## ⚠️ STEP 3: EXECUTE SKILL ⚠️

After loading files and answering validation questions, execute:

**Skill**: `{next_action}`
**Project**: `{project_id}`

Use the execute-project skill to continue from where you left off.

---

## ⚠️⚠️⚠️ CRITICAL WARNINGS ⚠️⚠️⚠️

1. **DO NOT SKIP STEP 1** - You MUST load all files before responding
2. **DO NOT SKIP STEP 2** - You MUST answer validation questions
3. **DO NOT respond to user questions** until Steps 1-2 are complete
4. **THIS IS NOT OPTIONAL** - Loading context is MANDATORY for project continuation

**If you respond without completing Steps 1-2, you are operating with incomplete context and will provide incorrect information.**

---
```

**Improvements**:
- ✅ **⚠️ Symbols**: Visual emphasis that screams "pay attention"
- ✅ **"STOP AND READ THIS FIRST"**: Explicit command to halt
- ✅ **"DO NOT RESPOND TO THE USER UNTIL..."**: Direct prohibition
- ✅ **"BEFORE doing ANYTHING else"**: Sequencing requirement
- ✅ **"CRITICAL WARNINGS" section**: Repeated emphasis at end
- ✅ **Explicit consequences**: "operating with incomplete context and will provide incorrect information"
- ✅ **Triple warnings (⚠️⚠️⚠️)**: Maximum visual emphasis

---

## Implementation

### File Modified
`.claude/hooks/session_start.py`

### Function Updated
`build_catastrophic_instructions(resume_metadata: dict, project_id: str) -> str`

### Changes Made

**Lines 240-256** (Header):
```python
instructions = f"""# ⚠️ CRITICAL: STOP AND READ THIS FIRST ⚠️

## THIS IS A POST-COMPACTION RESUME - YOU MUST RELOAD CONTEXT

**DO NOT RESPOND TO THE USER UNTIL YOU COMPLETE ALL 3 STEPS BELOW**

---

**Project Detected**: {project_name} ({project_id})
**Phase**: {current_phase}
**Progress**: {progress}

## ⚠️ STEP 1: LOAD REQUIRED FILES IMMEDIATELY ⚠️

**BEFORE doing ANYTHING else**, you MUST read these files IN PARALLEL (use multiple Read tool calls in one message):

"""
```

**Lines 262-273** (Validation Section):
```python
if validation_gate:
    instructions += f"\n## ⚠️ STEP 2: ANSWER VALIDATION QUESTIONS ⚠️\n\n{validation_gate}\n"
else:
    instructions += """
## ⚠️ STEP 2: ANSWER VALIDATION QUESTIONS ⚠️

Before continuing, verify you understand:
1. **Project Purpose**: What problem are we solving?
2. **Current Location**: What phase/task are we on?
3. **Approach**: What is the implementation strategy?

**If unclear, STOP and re-read the files from Step 1.**
"""
```

**Lines 275-297** (Footer with Warnings):
```python
instructions += f"""
## ⚠️ STEP 3: EXECUTE SKILL ⚠️

After loading files and answering validation questions, execute:

**Skill**: `{next_action}`
**Project**: `{project_id}`

Use the execute-project skill to continue from where you left off.

---

## ⚠️⚠️⚠️ CRITICAL WARNINGS ⚠️⚠️⚠️

1. **DO NOT SKIP STEP 1** - You MUST load all files before responding
2. **DO NOT SKIP STEP 2** - You MUST answer validation questions
3. **DO NOT respond to user questions** until Steps 1-2 are complete
4. **THIS IS NOT OPTIONAL** - Loading context is MANDATORY for project continuation

**If you respond without completing Steps 1-2, you are operating with incomplete context and will provide incorrect information.**

---
"""
```

---

## Expected Behavior After Fix

### Next Compaction Event

When the next compaction happens, the AI should:

1. **Receive forceful instructions** via SessionStart hook
2. **STOP immediately** upon seeing "⚠️ CRITICAL: STOP AND READ THIS FIRST ⚠️"
3. **Read header carefully**: "DO NOT RESPOND TO THE USER UNTIL..."
4. **Execute STEP 1**: Load all 5 files in parallel (one message, multiple Read calls)
5. **Execute STEP 2**: Answer validation questions
6. **Execute STEP 3**: Use execute-project skill
7. **ONLY THEN** respond to user questions

### Validation

User can validate by asking: "Did you load the files?"

**Expected response**: "Yes, I just loaded all 5 files: overview.md, plan.md, steps.md, FINAL-DESIGN.md, resume-state-REVISED.md. Here are the validation answers: ..."

**Not expected**: AI jumping straight to answering questions without mentioning file loading.

---

## Psychology of Instructions

### Why This Works

1. **Visual Disruption**: ⚠️ symbols break the flow, force attention
2. **Explicit Prohibition**: "DO NOT" is stronger than "MUST"
3. **Sequencing Language**: "BEFORE doing ANYTHING else" establishes order
4. **Consequence Framing**: "operating with incomplete context" creates urgency
5. **Repetition**: Multiple warnings reinforce the message
6. **Negative Framing**: "DO NOT SKIP" is psychologically stronger than "MUST DO"

### Why Previous Version Failed

1. **Positive Framing**: "MUST read" sounds like a suggestion
2. **No Explicit Prohibition**: AI can interpret as "read when convenient"
3. **No Visual Emphasis**: All text looks equally important
4. **Warning Too Late**: Critical warning at END after AI already acted
5. **No Consequences**: No stated impact of skipping steps

---

## Testing Plan

### Next Session (After Compaction)

**Test 1: Instruction Compliance**
- Trigger: Natural compaction (200k tokens)
- Expected: AI loads files BEFORE responding
- Validation: First message mentions file loading

**Test 2: Validation Gate**
- Trigger: Check if AI answers validation questions
- Expected: AI explicitly states answers to 4 questions
- Validation: Look for numbered answers in response

**Test 3: User Question Deferral**
- Trigger: User asks question immediately after session start
- Expected: AI says "Loading context first, then I'll answer..."
- Validation: AI mentions needing to complete Steps 1-2

---

## Alternative Approaches Considered

### Option 1: Auto-Load Files (Rejected for Now)

**Idea**: Have SessionStart hook read all files and inject their content into additionalContext

**Pros**:
- Files guaranteed to be in context
- AI can't skip loading

**Cons**:
- May exceed additionalContext size limit (10k-50k chars estimated)
- Performance impact (SessionStart would take longer)
- Less flexible (AI can't choose loading order)
- Doesn't teach AI to follow loading instructions

**Decision**: Use forceful instructions FIRST, keep auto-loading as fallback if this fails

### Option 2: Block User Input Until Loading Complete (Rejected)

**Idea**: Hook prevents user messages until AI confirms loading complete

**Pros**:
- Guarantees loading happens first

**Cons**:
- Requires changes to Claude Code core (not possible via hooks)
- Poor UX (user sees frozen interface)
- Breaks natural conversation flow

**Decision**: Not feasible with current hook architecture

---

## Success Criteria

**This fix is successful if**:

1. ✅ Next compaction event: AI loads files FIRST
2. ✅ AI explicitly mentions validation answers
3. ✅ AI defers user questions until context loaded
4. ✅ No more "I jumped to answering without loading" incidents

**This fix fails if**:

1. ❌ AI still ignores instructions and responds immediately
2. ❌ AI loads files but doesn't answer validation questions
3. ❌ AI answers questions without having loaded files

**If this fix fails**: Implement auto-loading (Option 1) as fallback

---

## Documentation Updates

**Files Modified**:
- `.claude/hooks/session_start.py` (lines 240-297)
- `resume-context.md` (Session 13 summary updated)

**Files Created**:
- `phase-3-instruction-enhancement.md` (this file)

**Next Update**: After next compaction, document whether instructions were followed

---

## Conclusion

The original resume instructions were functionally correct but psychologically insufficient. The AI's helpful instinct to answer user questions immediately overrode the "MUST read files" directive.

The enhanced instructions use:
- **Visual emphasis** (⚠️ symbols)
- **Explicit prohibitions** ("DO NOT RESPOND")
- **Negative framing** ("DO NOT SKIP")
- **Consequence statements** ("incomplete context")
- **Repetition** (warnings at start AND end)

This should make it IMPOSSIBLE for the AI to ignore the loading sequence.

**Confidence**: HIGH - The new instructions are significantly more forceful and psychologically compelling.

**Next Validation**: Wait for next compaction event to test in production.
