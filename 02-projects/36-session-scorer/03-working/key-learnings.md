# Project 36: Key Learnings

## Learning 1: Custom Subagents via `subagent_type` Don't Work (Bug)

**Date**: 2026-01-07

**Discovery**: Custom subagents defined in `.claude/agents/` are NOT discoverable via the `subagent_type` parameter in the Task tool.

**Expected Behavior** (per docs):
```python
Task(
    subagent_type="general-session-scorer",  # custom agent name
    prompt="Score session..."
)
```

**Actual Behavior**:
```
Error: Agent type 'general-session-scorer' not found.
Available agents: general-purpose, statusline-setup, Explore, Plan, claude-code-guide
```

**Root Cause**: Known bug ([GitHub Issue #11205](https://github.com/anthropics/claude-code/issues/11205)) - filesystem-based agent discovery doesn't work. Only UI-created agents via `/agents` command work.

**Workaround**: Use `general-purpose` with explicit instructions to read the prompt file.

**Impact on Architecture**:
- Removed `.claude/agents/general-session-scorer.md` (moved to TRASH)
- Created `03-skills/langfuse/langfuse-score-session/prompts/scorer-prompt.md` instead
- SKILL.md defines invocation pattern that tells subagent to read prompt file first

---

## Learning 2: Subagent Prompt Loading Pattern

**Date**: 2026-01-07

**Problem**: How do you give a `general-purpose` subagent custom instructions?

**Solution**: Two-step prompt that tells subagent to read instructions file first:

```python
Task(
    subagent_type="general-purpose",
    model="sonnet",
    prompt="""
FIRST: Read the scoring instructions from this file:
c:/Users/dsber/infinite/auto-company/strategy-nexus/03-skills/langfuse/langfuse-score-session/prompts/scorer-prompt.md

THEN: Score session {session_id} following those instructions exactly.
Return ONLY the JSON output as specified in the prompt.
"""
)
```

**Why This Works**:
- `general-purpose` has access to Read tool
- Subagent can load any file in the workspace
- Instructions are version-controlled in the skill folder
- Decouples invocation from instruction content

**Alternative (Not Chosen)**: Embed full prompt in Task call
- Pros: Guaranteed to load
- Cons: Verbose, duplicates content, harder to maintain

---

## Learning 3: Skill Structure for Subagent-Based Skills

**Date**: 2026-01-07

**Pattern Established**:

```
03-skills/{category}/{skill-name}/
├── SKILL.md                    # HOW to invoke (orchestration logic)
└── prompts/
    └── {agent}-prompt.md       # WHAT the subagent does (instructions)
```

**SKILL.md Contains**:
- Trigger phrases
- Task tool invocation pattern
- Post-processing logic (calculate aggregates)
- Score storage commands
- Dependencies list

**prompts/*.md Contains**:
- Subagent role definition
- Detailed criteria/rubrics
- Output schema (JSON format)
- Important rules

**Benefit**: Clean separation between orchestration and execution logic.

---

## Learning 4: Score Comment Field Has No Practical Limit

**Date**: 2026-01-07

**Test**: Tried storing 10,000 character comment via `langfuse-create-score`

**Result**: Works perfectly. No truncation, no errors.

**Implication**: Can store detailed root cause analysis, improvement suggestions, and session notes as score comments without worrying about length limits.

---

## Summary Table

| Learning | Impact | Action Taken |
|----------|--------|--------------|
| Custom `subagent_type` broken | Can't use named agents | Use `general-purpose` + prompt file |
| Subagent needs explicit file read | Must tell it what to read | Two-step prompt pattern |
| Skill structure pattern | Maintainable subagent skills | `SKILL.md` + `prompts/` folder |
| Score comments unlimited | Rich metadata storage | Use for detailed analysis |

---

*Updated: 2026-01-07*
