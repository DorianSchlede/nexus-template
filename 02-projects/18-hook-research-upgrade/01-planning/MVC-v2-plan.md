# MVC v2 - Complete Rethink

**Created**: 2026-01-01
**Status**: PLANNING (requires approval)

---

## Mental Models Applied

### 1. **First Principles Thinking** (Cognitive)
*Strip assumptions, find fundamental truths*

**Question**: What does Claude ACTUALLY need at session start?

Breaking down to fundamentals:
- Claude needs to know **what to do** (routing rules)
- Claude needs to know **what NOT to do** (constraints)
- Claude needs to know **how to respond** (language, action)

Everything else (projects, skills, user context) can be **discovered on demand**.

**Insight**: We were solving the wrong problem. We tried to front-load everything when Claude can read files itself.

---

### 2. **Inversion** (Cognitive)
*Solve problems by considering the opposite*

Instead of asking "What do we include?", ask **"What can we EXCLUDE?"**

| Remove | Why Safe |
|--------|----------|
| Full orchestrator | Claude can Read() the file |
| Project list | Claude can scan 02-projects/ |
| Skill list | Claude can scan 03-skills/ |
| User goals | Claude can Read() goals.md |
| Navigation hints | Claude knows the folder structure |

**What remains**: Pure routing logic (~500 tokens)

---

### 3. **Pareto Analysis (80/20)** (Analytical)
*Prioritization by impact concentration*

20% of the context delivers 80% of the value:
- Routing priority table → **Critical** (prevents wrong behavior)
- Core skill matching → **Critical** (prevents wrong skill loads)
- Never do list → **Critical** (prevents dangerous actions)
- Language setting → **Important** (user experience)

Everything else → **Nice to have** (can be loaded on demand)

---

### 4. **Theory of Constraints** (Operational)
*Find and elevate the bottleneck*

The constraint is: `hookSpecificOutput.additionalContext` has practical limits.

**Before**: Tried to fit 6K+ tokens into constrained channel
**After**: Minimize to ~500 tokens, eliminate the constraint entirely

---

### 5. **Fault Tree Analysis** (Diagnostic)
*Work backward from failures to root causes*

```
FAILURE: Zero context injected
    └── Exception caught, fallback empty
        └── ImportError: No module named 'yaml'
            └── loaders.py imports utils.py
                └── utils.py: import yaml (line 16)
                    └── pyyaml not in subprocess environment
```

**Root cause**: Dependency chain too deep for subprocess execution.

---

### 6. **Second-Order Thinking** (Cognitive)
*Consider consequences of consequences*

**v1 First-Order**: "Let's dynamically generate context"
**v1 Second-Order**: Dependencies → subprocess isolation → import failures → zero context

**v2 First-Order**: "Let's hardcode minimal routing"
**v2 Second-Order**: No imports → always works → Claude reads files on demand → full capability retained

---

### 7. **Margin of Safety** (Risk)
*Build in buffer for errors*

v1 had a **single point of failure**: `import yaml`
- If pyyaml missing → entire system crashes → zero context

v2 has **multiple fallback layers**:
1. Try to read user-config.yaml with regex → works without yaml parser
2. If read fails → use "English" default
3. If entire build fails → output minimal routing context
4. Hardcoded routing rules → always available

**Margin of safety**: 4 layers deep.

---

### 8. **MECE Principle** (Collaborative)
*Mutually Exclusive, Collectively Exhaustive breakdown*

Context breakdown for MVC v2:

| Category | Content | Tokens | MECE Check |
|----------|---------|--------|------------|
| **Routing** | Priority table | 100 | ✓ Exclusive: only routing logic |
| **Skills** | Core 3 skills | 50 | ✓ Exclusive: only skill matching |
| **Constraints** | Never do list | 50 | ✓ Exclusive: only prohibitions |
| **Action** | display_menu or continue | 20 | ✓ Exclusive: only action directive |
| **Metadata** | Session, language | 30 | ✓ Exclusive: only session info |
| **TOTAL** | | ~250 | ✓ Collectively exhaustive |

Nothing overlaps. Everything Claude needs is covered.

---

### 9. **Opportunity Cost** (Time & Resource)
*What you give up by choosing this option*

| Choice | Opportunity Cost |
|--------|------------------|
| Include full orchestrator (8K) | Fast startup, small context |
| Include project list (500) | Dynamic discovery, user sees current state |
| Include skill list (500) | Claude can route without scanning |

**Decision**: The opportunity cost of including more is higher than excluding.
- Excluding = Claude reads on demand (minor delay)
- Including = Larger context, dependency risk, slower startup

---

### 10. **Constraint Removal** (Creative)
*Ask "what if X limitation didn't exist?"*

**What if we had no token limit?**
→ We'd still not inject 26K tokens (Claude drowns in noise)

**What if we had no dependency limit?**
→ We'd still not chain 5 imports (fragile architecture)

**Insight**: Even without constraints, v2 is better design. Constraints just forced the right answer.

---

## Context Reduction Analysis

### Orchestrator.md Breakdown (~8K tokens → target ~1K)

| Section | Lines | Est. Tokens | Verdict | Reason |
|---------|-------|-------------|---------|--------|
| ASCII Banner | 1-12 | 200 | **REMOVE** | Decorative, zero behavioral value |
| Philosophy | 14-18 | 80 | **REDUCE** | Keep 1 sentence: "Every .md is executable code" |
| Startup (MANDATORY) | 22-29 | 100 | **REMOVE** | Obsolete - we inject directly now |
| Core Concepts: Projects | 35-40 | 120 | **KEEP** | Critical for project understanding |
| Core Concepts: Skills | 42-52 | 180 | **KEEP** | Critical for skill understanding |
| Smart Routing table | 56-76 | 300 | **ESSENTIAL** | Core routing logic |
| Core Skill Matching | 79-98 | 350 | **ESSENTIAL** | Prevents wrong skill loads |
| Learning Skills table | 101-114 | 200 | **REDUCE** | Summary: "suggest onboarding contextually" |
| NEVER Do | 118-123 | 80 | **ESSENTIAL** | 3 critical constraints |
| Menu Display | 126-217 | 1,500 | **REMOVE** | Claude can Read() when needed |
| Actions Reference | 221-228 | 100 | **REDUCE** | Only 3 actions, can inline |
| Language Preference | 231-235 | 60 | **INJECT** | Single value in context |
| Proactive Onboarding | 239-293 | 800 | **REMOVE** | Nice-to-have, not critical |
| Session End Behavior | 296-314 | 300 | **REMOVE** | Nice-to-have, not critical |

### What's TRULY Essential (~1K tokens)

```markdown
## Smart Routing (First Match Wins)

| Priority | Trigger | Action |
|----------|---------|--------|
| 0 | "add/integrate [name]" + integration exists | → {name}-connect skill |
| 1 | Message matches skill description | → Load skill |
| 2 | User mentions project by name/ID | → execute-project skill |
| 3 | No match | → Respond naturally |

## Core Skill Matching

| Skill | Intent |
|-------|--------|
| create-project | User wants NEW work with deliverable |
| execute-project | User references EXISTING project |
| create-skill | User wants to AUTOMATE patterns |

## Core Concepts (Quick Reference)

- **Project**: Temporal work with beginning/end. Location: 02-projects/
- **Skill**: Reusable workflow. Location: 03-skills/ (user) > 00-system/skills/ (system)
- Will do ONCE? → Project. Will do AGAIN? → Skill.

## NEVER Do

- ❌ Read project files directly → use execute-project
- ❌ Create folders directly → use create skills
- ❌ Auto-load learning skills → suggest, user decides

## Actions

| Action | Behavior |
|--------|----------|
| display_menu | Read orchestrator.md for template |
| load_and_execute_project | Load execute-project skill |
| continue_working | Skip menu, resume previous task |
```

### What We Can REMOVE (7K tokens saved!)

| Section | Tokens | Why Safe to Remove |
|---------|--------|-------------------|
| ASCII Banner | 200 | Decorative |
| Startup (MANDATORY) | 100 | Obsolete - hook injects context |
| Menu Display Template | 1,500 | Claude reads file when display_menu |
| Proactive Onboarding | 800 | Nice-to-have, complex logic |
| Session End Behavior | 300 | Nice-to-have |
| Example Suggestions | 300 | Claude can reason |
| display_hints logic | 200 | Complex, optional |
| Learning Skills detail | 200 | Summary sufficient |
| **TOTAL REMOVED** | **~3,600** | |

### Reduction Strategies

#### Strategy 1: Table Compression

**Before** (350 tokens):
```markdown
| Priority | Trigger | Action |
|----------|---------|--------|
| **0. Integration Exists** | "add/integrate [name]" where name is in `stats.configured_integrations` | Redirect to `{name}-connect` skill, explain it's already built |
| **1. Skill Match** | Message matches any skill description in `metadata.skills` | Load skill → Execute workflow |
| **2. Project Reference** | User mentions ANY project by name, ID, or number | **ALWAYS** load `execute-project` skill first |
| **3. General** | No match | Respond naturally. For Nexus questions → `00-system/documentation/product-overview.md` |
```

**After** (100 tokens):
```markdown
| # | Match | Action |
|---|-------|--------|
| 0 | integration name | {name}-connect |
| 1 | skill match | load skill |
| 2 | project ref | execute-project |
| 3 | none | respond naturally |
```

#### Strategy 2: Prose to List

**Before** (180 tokens):
```markdown
### Skills
**Reusable workflows** for repetitive tasks.
- Location: `03-skills/{skill-name}/` (user) or `00-system/skills/` (system)
- **User skills beat system skills** (03-skills/ has priority)
- Triggered by matching description keywords
- Example: "Weekly Status Report" (repeatable process)
```

**After** (50 tokens):
```markdown
**Skill** = Reusable workflow (03-skills/ > 00-system/skills/)
```

#### Strategy 3: Remove Examples

All "Example:", "For example:", example code blocks → REMOVE
- Claude can reason from principles
- Examples are ~30% of token usage

#### Strategy 4: Inline Actions

**Before** (separate Actions Reference section)
**After**: Inline in routing table or context JSON

---

## Why v1 Failed

| Problem | Root Cause |
|---------|------------|
| `PyYAML is required but not installed` | session_start.py → loaders.py → utils.py → `import yaml` |
| Zero context injected | Exception caught, fallback bundle has no data |
| Complex dependency chain | 5 generator functions, 250+ lines of code |
| Still too large | Tried to fit 6K+ tokens, orchestrator alone is 8K |

**Core insight**: The MVC v1 was **over-engineered**. It tried to dynamically generate everything when a simpler static approach would work.

---

## New Philosophy

| Principle | Implementation |
|-----------|----------------|
| **Zero dependencies** | No YAML, no loaders.py imports |
| **Static over dynamic** | Pre-computed where possible |
| **Small injection** | ~1.5K tokens max |
| **Two-phase loading** | Inject rules, Claude reads details |
| **Fail-safe** | If extraction fails, inject minimal routing |

---

## Architecture: Hybrid Extract-on-Read

### Data Flow

```
session_start.py (REWRITTEN - standalone)
       ↓
Read orchestrator.md directly (raw file read)
       ↓
Extract with regex: routing table, NEVER do, core skills
       ↓
Build slim context (~1.5K tokens)
       ↓
Output via hookSpecificOutput.additionalContext
       ↓
Claude receives rules immediately
       ↓
Claude reads orchestrator.md for full menu template (if needed)
```

### What Gets Injected

```json
{
  "nexus_version": "v4",
  "routing": {
    "priority": [
      {"order": 0, "match": "integration name in message", "action": "redirect to {name}-connect skill"},
      {"order": 1, "match": "skill description matches", "action": "load matching skill"},
      {"order": 2, "match": "project name/ID mentioned", "action": "load execute-project skill"},
      {"order": 3, "match": "no match", "action": "respond naturally"}
    ]
  },
  "core_skills": {
    "create-project": "User wants to START something NEW with deliverable",
    "execute-project": "User references EXISTING project by name/ID",
    "create-skill": "User wants to AUTOMATE repeating work"
  },
  "never_do": [
    "Read project files directly - use execute-project",
    "Create project/skill folders directly - use create skills",
    "Auto-load learning skills - suggest, user decides"
  ],
  "language": "English",
  "action": "display_menu",
  "instruction": "For menu template, read: 00-system/core/orchestrator.md"
}
```

**Token estimate**: ~400 tokens (vs 6K+ in v1)

---

## Implementation Steps

### Step 1: Rewrite session_start.py (COMPLETE REPLACEMENT)

```python
#!/usr/bin/env python3
"""
SessionStart Hook - MVC v2 (Minimal Viable Context)

Design principles:
- Zero external dependencies (no yaml, no loaders.py)
- Small injection (~1.5K tokens max)
- Two-phase: inject rules, Claude reads orchestrator for details
- Fail-safe: minimal routing always works
"""

import json
import sys
import os
import re
from pathlib import Path
from datetime import datetime

# Constants (hardcoded, no imports)
ORCHESTRATOR_PATH = "00-system/core/orchestrator.md"
USER_CONFIG_PATH = "01-memory/user-config.yaml"

def extract_language(project_dir: str) -> str:
    """Extract language from user-config.yaml using simple regex."""
    config_path = Path(project_dir) / USER_CONFIG_PATH
    if config_path.exists():
        try:
            content = config_path.read_text(encoding="utf-8")
            match = re.search(r'language:\s*["\']?([^"\'\n]+)', content, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        except Exception:
            pass
    return "English"

def build_slim_context(project_dir: str, source: str) -> dict:
    """Build minimal routing context without external dependencies."""

    # Core routing rules (static, from orchestrator.md)
    routing = {
        "priority": [
            {"order": 0, "match": "integration name in message", "action": "redirect to {name}-connect skill"},
            {"order": 1, "match": "skill description matches", "action": "load matching skill"},
            {"order": 2, "match": "project name/ID mentioned", "action": "load execute-project skill"},
            {"order": 3, "match": "no match", "action": "respond naturally"}
        ]
    }

    # Core skills (static)
    core_skills = {
        "create-project": "User wants to START something NEW with deliverable",
        "execute-project": "User references EXISTING project by name/ID",
        "create-skill": "User wants to AUTOMATE repeating work"
    }

    # Never do (static)
    never_do = [
        "Read project files directly - use execute-project",
        "Create project/skill folders directly - use create skills",
        "Auto-load learning skills - suggest, user decides"
    ]

    # Detect resume mode
    resume_mode = source in ("resume", "compact")

    # Build context
    context = {
        "nexus_version": "v4",
        "mode": "resume" if resume_mode else "startup",
        "routing": routing,
        "core_skills": core_skills,
        "never_do": never_do,
        "language": extract_language(project_dir),
    }

    # Action depends on mode
    if resume_mode:
        context["action"] = "continue_working"
        context["instruction"] = "Continue from where you left off. Check _resume.md in active project."
    else:
        context["action"] = "display_menu"
        context["instruction"] = "For menu template, read: 00-system/core/orchestrator.md"

    return context

def main():
    try:
        input_data = json.load(sys.stdin)
        session_id = input_data.get("session_id", "unknown")
        source = input_data.get("source", "startup")
        project_dir = os.environ.get("CLAUDE_PROJECT_DIR", "")

        # Build slim context
        context = build_slim_context(project_dir, source)
        context["session"] = {
            "id": session_id,
            "source": source,
            "timestamp": datetime.now().isoformat()
        }

        # Output as hook response
        hook_output = {
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": json.dumps(context, ensure_ascii=False)
            }
        }

        print(json.dumps(hook_output), flush=True)
        sys.exit(0)

    except Exception as e:
        # Fail-safe: output minimal context
        fallback = {
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": json.dumps({
                    "nexus_version": "v4",
                    "action": "display_menu",
                    "instruction": "Read 00-system/core/orchestrator.md for instructions",
                    "error": str(e)
                })
            }
        }
        print(json.dumps(fallback), flush=True)
        sys.exit(0)

if __name__ == "__main__":
    main()
```

### Step 2: Keep database calls (add back later)

The above is the minimal working version. After testing, add back:
- `send_to_server()` call for session start event
- `ensure_server_running()` check
- Session file tracking

### Step 3: Remove loaders.py dependency

The MVC v2 code in session_start.py:
- Does NOT import from loaders.py
- Does NOT import from utils.py
- Uses only stdlib: json, sys, os, re, pathlib, datetime

---

## Testing Plan

### Test 1: Fresh Session Start
```
Expected:
- Hook outputs valid JSON with hookSpecificOutput
- additionalContext contains routing rules
- Claude receives context and displays menu
```

### Test 2: Resume/Compact Session
```
Expected:
- mode: "resume"
- action: "continue_working"
- instruction points to _resume.md
```

### Test 3: Fallback on Error
```
Expected:
- Even if project_dir is empty/invalid
- Hook outputs minimal routing context
- Never crashes, never blocks Claude
```

---

## Token Analysis

| Component | v1 Tokens | v2 Tokens |
|-----------|-----------|-----------|
| Orchestrator (full) | 8,000 | 0 (Claude reads if needed) |
| Routing rules | 800 | 300 |
| Core skills | 500 | 150 |
| Never do | 100 | 100 |
| Project index | 500 | 0 (not included) |
| Skill categories | 500 | 0 (not included) |
| User context | 300 | 50 |
| JSON overhead | 500 | 100 |
| **Total** | **~6,000** | **~700** |

v2 is **8.5x smaller** than v1!

---

## Trade-offs

### What We Lose
- Project list in initial context (Claude must scan 02-projects/)
- Skill list in initial context (Claude must scan 03-skills/)
- Full orchestrator in context (Claude reads file when needed)

### What We Gain
- **Zero dependencies** - no pyyaml, no loaders.py
- **Fast startup** - ~700 tokens vs 6K+
- **Always works** - hardcoded fallback
- **Simple code** - ~100 lines vs 250+

---

## Future Enhancements (Optional)

### Phase 2: Add Project Index
```python
def scan_projects_simple(project_dir: str) -> list:
    """Scan projects using only pathlib, no YAML."""
    projects = []
    projects_path = Path(project_dir) / "02-projects"
    if projects_path.exists():
        for folder in sorted(projects_path.iterdir()):
            if folder.is_dir() and not folder.name.startswith("."):
                # Extract ID and name from folder name
                match = re.match(r'(\d+)-(.+)', folder.name)
                if match:
                    projects.append({
                        "id": match.group(1),
                        "name": match.group(2).replace("-", " ").title(),
                        "folder": folder.name
                    })
    return projects[:10]  # Limit to 10 for token budget
```

### Phase 3: Add Active Project Detection
```python
def detect_active_project(project_dir: str) -> dict | None:
    """Find project with IN_PROGRESS status using simple text search."""
    # Read overview.md files, look for "status: IN_PROGRESS"
    ...
```

---

## Decision Required

**Option A**: Implement v2 as described (minimal, ~700 tokens)
**Option B**: Implement v2 + simple project scanner (~1K tokens)
**Option C**: Different approach entirely

Which option should we proceed with?

---

## Files to Modify

| File | Action | Lines |
|------|--------|-------|
| `.claude/hooks/session_start.py` | REPLACE | ~100 |
| `00-system/core/nexus/loaders.py` | KEEP (for CLI use, not hooks) | 0 |

---

## Success Metrics

| Metric | v1 (Failed) | v2 (Target) |
|--------|-------------|-------------|
| Dependencies | pyyaml (missing) | None |
| Injection size | 6K (blocked) | ~700 |
| Claude follows routing | 0% | 100% |
| Fallback on error | Yes (empty) | Yes (minimal routing) |
| Startup latency | N/A (crashed) | <50ms |

---

## Implementation Options (DECISION REQUIRED)

### Option A: Ultra-Minimal (~400 tokens)

**Inject ONLY routing rules, nothing else.**

```json
{
  "nexus": "v4",
  "routing": [
    {"match": "integration", "action": "{name}-connect"},
    {"match": "skill", "action": "load skill"},
    {"match": "project", "action": "execute-project"},
    {"match": "none", "action": "natural response"}
  ],
  "never": ["read project directly", "create folders directly", "auto-load learning"],
  "action": "display_menu",
  "read": "00-system/core/orchestrator.md"
}
```

**Pros**: Smallest possible, zero complexity
**Cons**: Claude must read orchestrator.md for any nuance

---

### Option B: Essential Context (~800 tokens)

**Inject routing + core concepts + NEVER do.**

Same as "What's TRULY Essential" section above.

**Pros**: Claude has enough to route correctly without reading file
**Cons**: Slightly larger, but still small

---

### Option C: Static File Approach

**Pre-create a slim orchestrator file that hook reads directly.**

Create: `00-system/core/orchestrator-slim.md` (~800 tokens)
Hook reads this file instead of generating context.

**Pros**: Easy to maintain, no code changes needed
**Cons**: Must sync when orchestrator.md changes

---

### Option D: Tiered Approach

**Different context based on source type.**

| Source | Context Size | What's Included |
|--------|--------------|-----------------|
| startup | ~800 | Full routing + concepts |
| resume | ~200 | Just action + instruction |
| compact | ~200 | Just action + instruction |
| clear | ~800 | Full routing + concepts |

**Pros**: Optimized for each scenario
**Cons**: More code paths to test

---

## Recommendation

**Option B: Essential Context (~800 tokens)** with **Option D tiering**.

- Startup/clear: inject ~800 tokens (routing + concepts)
- Resume/compact: inject ~200 tokens (just "continue working")

This gives us:
- Small enough to always work (< 1K tokens)
- Enough for correct routing without file reads
- Fast resume (200 tokens)
- Zero dependencies

---

## Next Steps After Approval

1. **Backup current session_start.py**
2. **Write new session_start.py** (Option B + D implementation)
3. **Test with fresh session**
4. **Test with resume/compact**
5. **Verify routing works correctly**
6. **Update project docs**
