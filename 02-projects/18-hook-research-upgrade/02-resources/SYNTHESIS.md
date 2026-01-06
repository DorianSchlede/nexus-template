# Hook Research Upgrade - Synthesis Document

**Created**: 2026-01-01
**Status**: READY FOR IMPLEMENTATION

---

## Executive Summary

This synthesis merges all 8 research outputs into an actionable implementation plan. The research uncovered 150+ patterns from 9 community repositories and identified critical improvements for the Nexus hook system.

### The Core Problem

**Session Start is Broken**: The current `session_start.py` outputs text telling Claude to "Read the cache file" but Claude doesn't reliably follow this instruction. The cache file is 26K+ tokens - too large for direct injection.

**Solution**: Implement Minimum Viable Context (MVC) - slim context that fits directly in `hookSpecificOutput.additionalContext`.

---

## Implementation Priority Matrix

| Priority | What | Why | Effort | Token Savings |
|----------|------|-----|--------|---------------|
| **P0-CRITICAL** | MVC Fix | Session start is broken | HIGH | 26K→6K |
| **P1-HIGH** | Safety Patterns | Prevent dangerous operations | LOW | - |
| **P2-HIGH** | Context Loading | Skill-aware guidance | MEDIUM | - |
| **P3-MEDIUM** | Observability | Block event logging | LOW | - |
| **P4-LOW** | Quality Chain | Auto-formatters | MEDIUM | - |
| **P5-LOW** | Tool Redirection | Parameter enhancement | LOW | - |

---

## P0: MVC Fix (CRITICAL)

### Current State
- `session_start.py` outputs text with "Read the cache file" instruction
- Claude doesn't reliably follow this instruction
- Full cache is 26K+ tokens (too large for additionalContext)
- orchestrator.md (~8K tokens) MUST always be loaded

### Solution: Option B - Essential Orchestrator + Slim Metadata (~6K tokens)

| Component | Tokens |
|-----------|--------|
| orchestrator.md (essential sections) | 3,500 |
| system-map navigation | 500 |
| Project index (slim) | 500 |
| Skill categories | 500 |
| User context | 300 |
| Instructions | 200 |
| JSON overhead | 500 |
| **Total** | **~6,000** |

### Implementation Steps

1. **Create slim generator functions in `loaders.py`**:
```python
def generate_slim_startup(base_path: str) -> dict:
    """Generate startup context under 8K tokens."""

def generate_slim_resume(base_path: str) -> dict:
    """Generate resume context under 4K tokens."""

def extract_essential_orchestrator(base_path: str) -> str:
    """Extract critical orchestrator sections."""
```

2. **Update `session_start.py`** to output proper JSON:
```python
output = {
    "hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": json.dumps(slim_context, ensure_ascii=False)
    }
}
print(json.dumps(output))
```

3. **Mode detection** for startup vs resume:
```python
if source in ("resume", "compact"):
    context = generate_slim_resume()
else:
    context = generate_slim_startup()
```

### Files to Modify
- `00-system/core/nexus/loaders.py` - Add slim generators
- `00-system/core/nexus/service.py` - Add startup_slim() method
- `.claude/hooks/session_start.py` - Use proper JSON output

### Database Impact: NONE
- Preserves all existing `send_to_server()` calls
- Only changes output format, not server communication

---

## P1: Safety Patterns (HIGH)

### Current State
- `.env` file blocking: **IMPLEMENTED**
- rm -rf blocking: **PARTIALLY IMPLEMENTED**
- git dangerous operations: **NOT IMPLEMENTED**
- TRASH pattern guidance: **NOT IMPLEMENTED**

### Patterns to Add

#### 1. Git Dangerous Operations (8 patterns)
```python
GIT_DANGEROUS_PATTERNS = [
    r"git\s+reset\s+--hard",
    r"git\s+reset\s+--merge",
    r"git\s+push\s+.*--force(?!-with-lease)",
    r"git\s+push\s+.*-f\b(?!orce-with-lease)",
    r"git\s+branch\s+-D\b",
    r"git\s+checkout\s+--\s+\.",
    r"git\s+clean\s+.*-[a-z]*f",
    r"git\s+stash\s+(drop|clear)",
]
```

#### 2. TRASH Pattern Guidance
When blocking rm commands, provide alternative:
```python
TRASH_GUIDANCE = """
Instead of 'rm':
- MOVE files using `mv` to TRASH directory
- Create TRASH/ if it doesn't exist
- Add entry in TRASH-FILES.md
"""
```

### Implementation
- Add patterns as constants in `pre_tool_use.py`
- Add `is_dangerous_git_command()` function
- Update blocking messages to include guidance

### Files to Modify
- `.claude/hooks/pre_tool_use.py` - Add new patterns and functions

### Database Impact: NONE
- Pure regex checks, no external calls

---

## P2: Context Loading (HIGH)

### 6 Context Mechanisms Available

| Mechanism | Currently Used | Nexus Opportunity |
|-----------|---------------|-------------------|
| `hookSpecificOutput.additionalContext` | YES (broken) | Fix with MVC |
| `systemMessage` | NO | Skill-aware guidance |
| `permissionDecisionReason` | NO | Better block explanations |
| `updatedInput` | NO | Parameter enhancement |
| Transcript reading | NO | Auto-detect project context |
| State files | PARTIAL | Two-phase warnings |

### New: Skill-Aware Context in UserPromptSubmit

When user message matches skill keywords, inject skill guidance:

```python
def main():
    data = json.load(sys.stdin)
    prompt = data.get("prompt", "")

    matched_skill = match_skill(prompt, skills_index)
    if matched_skill:
        skill_content = load_skill_md(matched_skill["path"])
        output = {
            "systemMessage": skill_content,
            "hookSpecificOutput": {"hookEventName": "UserPromptSubmit"}
        }
        print(json.dumps(output))
```

### Files to Modify
- `.claude/hooks/user_prompt_submit.py` - Add skill matching

### Database Impact: NONE

---

## P3: Observability (MEDIUM)

### Currently Missing: Block Event Logging

When operations are blocked, this should be logged for auditing.

```python
def send_block_event(session_id: str, reason: str, tool_name: str, details: dict):
    """Stream blocked operation event to server."""
    send_to_server(f"/api/v2/sessions/{session_id}/blocks", {
        "type": "block",
        "reason": reason,
        "tool_name": tool_name,
        "details": details,
        "timestamp": datetime.now().isoformat()
    })
```

### Statusline (Future)

Python equivalent of cc-tools-go statusline:
```
[main +] 45.2k in / 12.3k out / 8.1k cached | Project: ontologies-research
```

### Files to Modify
- `.claude/hooks/pre_tool_use.py` - Add block event streaming

### Database Impact: NEW ENDPOINT
- Adds `/api/v2/sessions/{id}/blocks` - check server schema first

---

## P4: Quality Chain (LOW)

### Two-Phase Notification Pattern

1. First occurrence: WARN (allow with message)
2. Second occurrence: BLOCK

```python
def two_phase_check(issue_key: str, message: str) -> tuple[bool, str]:
    state = load_state()
    if issue_key in state["warnings"]:
        return True, f"BLOCKED: {message}"
    else:
        state["warnings"][issue_key] = datetime.now().isoformat()
        save_state(state)
        return False, f"WARNING: {message}"
```

### Auto-Formatter Chain (PostToolUse)

After file edits, run formatters:
- Python: `ruff check --fix` + `ruff format`
- JS/TS: `prettier --write` + `eslint --fix`

### Files to Modify
- `.claude/hooks/post_tool_use.py` - Add formatter chain

### Database Impact: NONE

---

## P5: Tool Redirection (LOW)

### Parameter Enhancement via updatedInput

Silently improve tool calls:
```python
def enhance_parameters(tool_name: str, tool_input: dict) -> dict:
    ENHANCEMENTS = {
        "mcp__tavily__tavily-extract": {"extract_depth": "advanced"},
        "Bash": {"timeout": 30000}
    }
    if tool_name in ENHANCEMENTS:
        modified = {**tool_input, **ENHANCEMENTS[tool_name]}
        return modified
    return tool_input
```

### Guidance vs Silent Redirect

| Scenario | Approach |
|----------|----------|
| Parameter enhancement | Silent (updatedInput) |
| Tool substitution | Guidance (deny + reason) |
| Path normalization | Silent |
| Major behavior change | Guidance |

### Files to Modify
- `.claude/hooks/pre_tool_use.py` - Add enhancement logic

### Database Impact: NONE

---

## Critical Constraints

### MUST PRESERVE

1. **All `/api/v2/` endpoint calls** - Server contract
2. **Fire-and-forget pattern** - Never block Claude
3. **Exit code conventions** - 0=allow, 2=block
4. **Session ID propagation** - Tracking consistency

### MUST NOT BREAK

| File | Why |
|------|-----|
| `utils/http.py` | Transport layer |
| `utils/server.py` | Server auto-start |
| `send_event.py` | Event dispatcher |
| `stream_claude_message.py` | Message streaming |

### SAFE TO MODIFY

| File | Why |
|------|-----|
| `post_tool_use.py` | Local logging only |
| `user_prompt_submit.py` | Local logging only |
| `stop.py`, `subagent_stop.py` | TTS only |
| `notification.py` | TTS only |

---

## Implementation Order

### Phase 1: MVC Fix (This Session)
1. Create `generate_slim_startup()` in loaders.py
2. Create `generate_slim_resume()` in loaders.py
3. Update `session_start.py` to use proper JSON output
4. Test with real session

### Phase 2: Safety Patterns (This Session)
1. Add git dangerous patterns to pre_tool_use.py
2. Add TRASH guidance to rm blocking
3. Test with dangerous commands

### Phase 3: Context Enhancement (Next Session)
1. Add skill-aware context in user_prompt_submit.py
2. Add block event streaming in pre_tool_use.py
3. Add two-phase warning pattern

### Phase 4: Quality & Future (Later)
1. Add auto-formatter chain in post_tool_use.py
2. Add statusline visualization
3. Add TDD enforcement patterns

---

## Success Metrics

| Metric | Current | Target |
|--------|---------|--------|
| Session start tokens | 26K | <8K |
| Claude follows startup instructions | ~50% | 100% |
| Dangerous git operations blocked | 0% | 100% |
| Block events logged | No | Yes |
| Skill-aware context | No | Yes |

---

## File Change Summary

| File | Change Type | Priority |
|------|-------------|----------|
| `00-system/core/nexus/loaders.py` | MODIFY | P0 |
| `00-system/core/nexus/service.py` | MODIFY | P0 |
| `.claude/hooks/session_start.py` | MODIFY | P0 |
| `.claude/hooks/pre_tool_use.py` | MODIFY | P1 |
| `.claude/hooks/user_prompt_submit.py` | MODIFY | P2 |
| `.claude/hooks/post_tool_use.py` | MODIFY | P4 |

---

## Research Sources

All findings consolidated from:
- `research-current-system.md` - 8 API endpoints, 8 files touch database
- `research-mvc-context.md` - 5 MVC options, recommends Option B
- `research-context-loading.md` - 6 context mechanisms
- `research-safety-patterns.md` - 18+ safety patterns, TRASH pattern
- `research-observability.md` - Statusline, block events
- `research-tdd-quality.md` - Two-phase pattern, formatters
- `research-tool-redirection.md` - updatedInput mechanism
- `research-architech-patterns.md` - Mode filtering (40-65% savings)
