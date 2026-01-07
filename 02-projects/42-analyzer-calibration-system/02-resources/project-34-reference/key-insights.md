# Key Insights - Subagent Validation System

**Project 34** | Last Updated: 2026-01-07

---

## 1. Subagent Context Injection

**Problem**: Subagents do NOT receive SessionStart hook context automatically.

**Solution**: Tell subagents to read the cached context file:
```
FIRST: Read 00-system/.cache/session_start_context.xml
```

**Validation**: 10/10 subagents successfully loaded context.

---

## 2. Langfuse Trace Identification

**How agent_id maps to Langfuse**:
- `agentId` from Task tool → `metadata.conversationId = "agent-{agentId}"`
- Each subagent gets unique `sessionId` in Langfuse
- **Use composite key**: `{sessionId}:{agentId}` for guaranteed uniqueness

**Query pattern**:
```python
for trace in traces:
    if trace.metadata.get('conversationId') == f"agent-{agent_id}":
        session_id = trace.sessionId
        break
```

**Timing**: Traces appear in Langfuse ~5-10 seconds after subagent completion.

---

## 3. Subagent Resume Pattern (CRITICAL)

**Discovery**: Task tool `resume` parameter enables interactive validation flows.

**Pattern**:
1. Spawn subagent with real user request (NOT test-aware)
2. Subagent follows orchestrator rules, hits decision points
3. Subagent stops and reports questions
4. Orchestrator provides answers via `resume` parameter
5. Repeat until complete
6. Fetch traces from Langfuse
7. Analyzer evaluates against criteria

**Example**:
```python
# Initial spawn
result = Task(prompt="User wants to create Notion integration", ...)
agent_id = result.agent_id  # e.g., "a01d45d"

# Resume with answer
result = Task(prompt="User answered: I want read/query and create/update",
              resume="a01d45d", ...)
```

**Why this matters**: Subagents behave authentically (like real users) because they don't know they're being tested.

---

## 4. Natural Orchestrator Behavior (test-orchestrator)

**Key insight**: Don't tell subagents they're running tests.

**Implementation**: `.claude/agents/test-orchestrator.md`
- Just a normal Nexus orchestrator
- Reads `session_start_context.xml` on startup
- Follows orchestrator rules naturally
- **Doesn't know it's being tested**

**Instead of**:
```markdown
You are a TEST RUNNER. Execute this test scenario...
```

**Use**:
```markdown
You are Claude Code operating inside NEXUS.
FIRST: Read 00-system/.cache/session_start_context.xml
```

**Benefit**: Validates actual user experience, not test-aware behavior. Claude automatically invokes `test-orchestrator` when spawning validation tasks.

---

## 5. Meta Skill Design

**Decision**: validate-feature is a META skill, not a routed skill.

**Why**:
- Not for automatic routing/triggers
- Manually invoked when validating specific features
- Added to projects on case-by-case basis
- Developer tool, not user-facing

**Usage**: Copy scenario templates to project's `02-resources/validation-scenarios.yaml` when needed.

---

## 6. Windows Encoding Issue

**Problem**: Unicode characters (→) in trace output cause `cp1252` encoding errors on Windows.

**Solution**: Use `--output file.json` instead of printing to console.

---

## 7. Git Worktree Isolation (Destructive Tests)

**Problem**: Testing skills like `plan-project` that create files causes conflicts when running parallel subagents.

**Solution**: Use git worktrees for full file isolation.

```bash
# Setup
python scripts/worktree-manager.py setup --count 3 --prefix test-validation

# Each subagent works in its own worktree
# ../test-validation-0/
# ../test-validation-1/
# ../test-validation-2/

# Cleanup
python scripts/worktree-manager.py cleanup --prefix test-validation
```

**When to use**: Testing any skill that creates/modifies files (plan-project, execute-project, etc.)

**Key benefits**:
- Full file isolation between parallel subagents
- No race conditions on file creation
- Each worktree is a complete copy of the repo
- Shared git history, separate working directories

---

## Architecture Summary

```
┌─────────────────────────────────────────────────────────────┐
│                 validate-feature WORKFLOW                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  AUTOMATED MODE:                                             │
│  1. Load scenario from project's validation-scenarios.yaml   │
│  2. Spawn N test subagents in parallel                       │
│  3. Wait for Langfuse ingestion (~10s)                       │
│  4. Fetch traces by agent_id → session_id                    │
│  5. Spawn analyzer to evaluate against pass_criteria         │
│  6. Generate validation report                               │
│                                                              │
│  MANUAL MODE:                                                │
│  1. User provides session IDs from previous runs             │
│  2. Fetch traces directly by session_id                      │
│  3. Spawn analyzer to evaluate                               │
│  4. Generate validation report                               │
│                                                              │
│  INTERACTIVE MODE (via resume):                              │
│  1. Spawn subagent with real user request                    │
│  2. Subagent hits decision point, reports question           │
│  3. Resume with user's answer                                │
│  4. Repeat until complete                                    │
│  5. Analyze full conversation trace                          │
│                                                              │
│  WORKTREE MODE (destructive tests):                          │
│  1. Create N git worktrees (one per subagent)                │
│  2. Spawn subagents, each in isolated worktree               │
│  3. No file conflicts between parallel runs                  │
│  4. Analyze results across worktrees                         │
│  5. Cleanup worktrees after testing                          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

*These insights should be preserved for future reference and onboarding.*
