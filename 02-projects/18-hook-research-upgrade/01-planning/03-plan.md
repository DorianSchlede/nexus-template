# Hook Research Upgrade - Plan

**Last Updated**: 2026-01-01
**Status**: P0-P1 COMPLETE, P2-P5 Pending

---

## Executive Summary

This project upgraded the Nexus hook system based on research from 9 community repositories and 150+ patterns. The critical MVC fix ensures Claude receives context directly without needing to "read a file".

**Resources Index**: See [02-resources/INDEX.md](../02-resources/INDEX.md) for all research documents.

---

## COMPLETED: P0 - MVC Fix (CRITICAL)

**Problem**: `session_start.py` outputted text telling Claude to "read cache file" but Claude didn't follow this instruction. Cache was 26K+ tokens - too large for direct injection.

**Solution**: Implemented Option B from research - Essential Orchestrator + Slim Metadata (~6K tokens).

### Implementation Details

**Files Modified:**
| File | Changes |
|------|---------|
| `00-system/core/nexus/loaders.py` | +5 MVC generator functions (~250 lines) |
| `.claude/hooks/session_start.py` | Rewrote to use `hookSpecificOutput.additionalContext` |

**New Functions in loaders.py:**
```python
extract_essential_orchestrator(base_path)    # Orchestrator with minimal banner
generate_project_index_slim(base_path)       # Ultra-slim project list
generate_skill_categories(base_path)         # Categories instead of full list
generate_slim_startup(base_path)             # Complete startup context <8K
generate_slim_resume(base_path)              # Resume context <4K
```

**Token Impact:**
| Mode | Before | After |
|------|--------|-------|
| Startup | 26K (in file) | ~6K (injected) |
| Resume | 26K (in file) | ~2K (injected) |

---

## COMPLETED: P1 - Safety Patterns (HIGH)

**File Modified**: `.claude/hooks/pre_tool_use.py`

**Patterns Added:**
| Pattern | Count | Purpose |
|---------|-------|---------|
| Git dangerous operations | 8 | Block reset --hard, push --force, branch -D, etc. |
| TRASH guidance | 1 | Suggest safe alternative to rm |

**Implementation:**
```python
GIT_DANGEROUS_PATTERNS = [
    (r"git\s+reset\s+--hard", "loses uncommitted changes"),
    (r"git\s+push\s+.*--force(?!-with-lease)", "use --force-with-lease"),
    # ... 6 more patterns
]

TRASH_GUIDANCE = """
SAFE ALTERNATIVE: Instead of rm, use the TRASH pattern:
1. Create TRASH/ directory: mkdir -p TRASH
2. Move files: mv <files> TRASH/
3. Add entry in TRASH-FILES.md
"""
```

---

## REMAINING: P2-P5

### P2: Context Enhancement (MEDIUM)
- Add skill-aware context in `user_prompt_submit.py`
- Match user message against skill keywords for proactive loading
- See: [research-context-loading.md](../02-resources/research-context-loading.md)

### P3: Observability (MEDIUM)
- Add block event streaming to `/api/v2/sessions/{id}/blocks`
- Requires server-side schema check first
- See: [research-observability.md](../02-resources/research-observability.md)

### P4: Quality Chain (LOW)
- Auto-formatter chain in `post_tool_use.py`
- Two-phase notification pattern
- See: [research-tdd-quality.md](../02-resources/research-tdd-quality.md)

### P5: Tool Redirection (LOW)
- Parameter enhancement via `updatedInput`
- See: [research-tool-redirection.md](../02-resources/research-tool-redirection.md)

---

## Database Constraints (MUST PRESERVE)

From [research-current-system.md](../02-resources/research-current-system.md):

```
/api/v2/sessions/{id}/start      (session_start.py)
/api/v2/sessions/{id}/end        (session_end.py)
/api/v2/sessions/{id}/executable (pre_tool_use.py)
/api/v2/sessions/{id}/transcript (session_end.py)
/api/v2/session/{id}/meta        (session_summary.py)
/events                          (send_event.py, stream_claude_message.py)
```

All implementations preserved these endpoints with fire-and-forget pattern.

---

## Key Decisions Made

| Decision | Choice | Rationale |
|----------|--------|-----------|
| MVC Option | Option B (~6K tokens) | Best balance of completeness and size |
| Orchestrator handling | Keep full with minimal banner | All sections needed for behavior |
| Git blocking | Block all dangerous patterns | Safety > convenience |
| rm blocking | Block + TRASH guidance | Recoverable is always better |
| Context injection | `hookSpecificOutput.additionalContext` | Guaranteed delivery |

---

## Architecture Reference

```
User Action
    │
    ▼
┌─────────────────────────────────────────────────────┐
│              SESSION_START.PY                        │
│  ┌──────────────────────────────────────────────┐   │
│  │      generate_slim_startup() / _resume()      │   │
│  │  - orchestrator (~3.5K tokens)                │   │
│  │  - project index (slim)                       │   │
│  │  - skill categories                           │   │
│  │  - user context                               │   │
│  └──────────────────────────────────────────────┘   │
│                      │                               │
│                      ▼                               │
│  OUTPUT: hookSpecificOutput.additionalContext        │
│  (Claude receives context DIRECTLY - no "read file") │
└─────────────────────────────────────────────────────┘
```

```
Tool Call
    │
    ▼
┌─────────────────────────────────────────────────────┐
│                 PRE_TOOL_USE.PY                      │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────┐│
│  │ .env Block  │─▶│ rm -rf Block │─▶│ git Block   ││
│  │ (existing)  │  │ + TRASH tip  │  │ (8 patterns)││
│  └─────────────┘  └──────────────┘  └─────────────┘│
│         │                                           │
│  Exit 0 = ALLOW    Exit 2 = BLOCK with reason       │
└─────────────────────────────────────────────────────┘
```

---

## Related Projects

| Project | Relationship |
|---------|--------------|
| Project 14 | Previous hook work - foundation |
| Project 17 | Source of hook patterns - research input |

---

## Resources

- **Research Index**: [02-resources/INDEX.md](../02-resources/INDEX.md)
- **Synthesis Document**: [02-resources/SYNTHESIS.md](../02-resources/SYNTHESIS.md)
- **Implementation Resume**: [_resume.md](../_resume.md)
