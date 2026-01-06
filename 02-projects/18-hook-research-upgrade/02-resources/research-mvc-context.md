# MVC Context Implementation Research

## Executive Summary

The current Nexus startup system loads 26K+ tokens at session start, which is too large for direct injection via `hookSpecificOutput.additionalContext`. The fundamental problem is that the session_start.py hook tells Claude to "read the file" but Claude doesn't reliably follow this instruction. This research provides multiple implementation options for reducing context to fit within injection limits while preserving the critical orchestrator.md behavior rules.

**Key Constraint**: orchestrator.md (~8K tokens) contains Claude's behavior rules and MUST always be loaded. All options must account for this.

---

## 1. Current State Analysis

### 1.1 Current Token Usage

Based on analysis of `context_startup.json` and component files:

| Component | Est. Tokens | Characters | Needed? |
|-----------|-------------|------------|---------|
| orchestrator.md | ~8,000 | ~11,000 | **YES - Contains Claude's behavior rules** |
| system-map.md | ~1,500 | ~2,100 | SLIM - navigation only |
| memory-map.md | ~800 | ~1,100 | NO - rarely referenced |
| goals.md | ~400 | ~600 | SLIM - role + goal only |
| user-config.yaml | ~500 | ~700 | YES - language, preferences |
| projects (17) | ~5,000 | ~7,000 | SLIM - index only |
| skills (100+) | ~8,000 | ~11,000 | CATEGORY INDEX only |
| JSON overhead | ~2,000 | ~3,000 | Reducible |
| **Total** | **~26,000** | ~36,500 | **Target: <12K** |

### 1.2 Current Flow Problems

**Problem 1: Hook Output Not Injected as Context**
- Location: `session_start.py` lines 159-180
- Current: Outputs text telling Claude to "Read({cache_path})"
- Issue: This is just stdout, NOT `hookSpecificOutput.additionalContext`
- Result: Claude sees the message but doesn't reliably follow the instruction

**Problem 2: Cache Too Large for additionalContext**
- Location: `nexus-loader.py` lines 173-212
- Current: Full 26K token cache written to file
- Issue: `additionalContext` has practical limits (performance degrades >15K tokens)
- Result: Cannot simply inject full cache even if we wanted to

**Problem 3: Orchestrator.md Embedded in Full**
- Location: `service.py` lines 91-96 (MANDATORY_MAPS loading)
- Current: Full orchestrator.md (~8K tokens) embedded in every startup
- Issue: Takes majority of any reasonable token budget
- Options: Keep full? Minify? Extract critical sections?

**Problem 4: All Projects with Descriptions**
- Location: `loaders.py` `scan_projects()` lines 32-101
- Current: Returns id, name, description, status, progress, current_task, file_path
- Issue: `description` field is verbose (~100 chars each x 17 projects)

**Problem 5: All Skills with Descriptions**
- Location: `loaders.py` `scan_skills()` lines 104-165
- Current: Returns name, description, file_path for 100+ skills
- Issue: Descriptions are for semantic matching but take ~8K tokens total

---

## 2. Options Analysis

### Option A: Full Orchestrator + Slim Everything Else (~12K tokens)

**Approach**: Keep orchestrator.md intact, aggressively slim other components.

**Token Budget**:
| Component | Tokens |
|-----------|--------|
| orchestrator.md (full) | 8,000 |
| Project index (id, name, status only) | 400 |
| Skill categories (no descriptions) | 300 |
| User context (role + language) | 200 |
| Instructions/action | 200 |
| JSON overhead | 500 |
| **Total** | **~9,600** |

**Pros**:
- Orchestrator behavior rules 100% preserved
- No risk of losing critical routing/menu logic
- Simple implementation - just slim metadata

**Cons**:
- Still large for additionalContext (may cause latency)
- Orchestrator has redundant content (examples, ASCII art ~1K tokens)
- No room for growth if more projects/skills added

**Implementation**:
```python
def generate_slim_startup_full_orchestrator():
    return {
        "orchestrator": read_file("orchestrator.md"),  # Full content
        "project_index": [
            {"id": p["id"], "name": p["name"], "status": p["status"]}
            for p in scan_projects(minimal=True)
        ],
        "skill_categories": extract_skill_categories(),
        "user": {"role": goals["role"], "language": config["language"]},
        "action": "display_menu"
    }
```

---

### Option B: Essential Orchestrator Sections (~8K tokens)

**Approach**: Extract only essential sections from orchestrator.md, skip redundant/decorative content.

**What to Keep**:
- Philosophy section (100 tokens)
- Core Concepts section (300 tokens)
- Smart Routing section WITH table (500 tokens)
- Core Skill Matching section (400 tokens)
- Learning Skills table (200 tokens)
- NEVER Do section (100 tokens)
- Menu Display template (800 tokens)
- Actions Reference (100 tokens)
- Language Preference (50 tokens)
- Proactive Onboarding section (600 tokens)
- Session End Behavior (200 tokens)

**What to Skip**:
- ASCII banner (~200 tokens) - decorative
- Example suggestions (~300 tokens) - can be regenerated
- DO NOT Suggest When section - less critical

**Token Budget**:
| Component | Tokens |
|-----------|--------|
| orchestrator.md (essential) | 3,500 |
| Project index (id, name, status, progress) | 500 |
| Skill categories (with brief descriptions) | 500 |
| User context (role, goal, language) | 300 |
| system-map.md (structure only) | 500 |
| Instructions/action | 200 |
| JSON overhead | 500 |
| **Total** | **~6,000** |

**Pros**:
- Under 8K target - good for additionalContext
- All routing rules preserved
- Room for project/skill growth

**Cons**:
- Need to maintain essential orchestrator extraction logic
- Risk of accidentally omitting critical rules
- ASCII banner loss reduces "brand identity"

**Implementation**:
```python
def extract_essential_orchestrator():
    """Extract critical sections from orchestrator.md"""
    full = read_file("orchestrator.md")

    sections_to_keep = [
        "## Philosophy",
        "## Core Concepts",
        "## Smart Routing",
        "### Core Skill Matching",
        "### Learning Skills",
        "### NEVER Do",
        "## Menu Display",
        "## Actions Reference",
        "## Language Preference",
        "## Proactive Onboarding",
        "## Session End Behavior"
    ]

    # Extract sections using regex or markdown parser
    return extract_sections(full, sections_to_keep)
```

---

### Option C: Routing Table + Behavior Rules (~5K tokens)

**Approach**: Extreme minimization - just the decision tables and rules.

**What to Keep**:
- Routing priority table (as structured data)
- Skill matching rules (as structured data)
- Menu template reference (path only)
- Project/skill indexes
- User context

**Token Budget**:
| Component | Tokens |
|-----------|--------|
| Routing rules (structured) | 800 |
| Skill matching rules | 500 |
| Project index (slim) | 400 |
| Skill categories | 300 |
| User context | 300 |
| Menu template path | 50 |
| Instructions | 200 |
| JSON overhead | 400 |
| **Total** | **~2,950** |

**Pros**:
- Smallest option - fast injection
- Structured data easier to parse
- Maximum room for growth

**Cons**:
- Menu display template not in context (must be loaded separately)
- Nuanced guidance (examples, suggestions) lost
- Higher risk of incorrect behavior in edge cases

**Implementation**:
```python
def generate_minimal_routing():
    return {
        "routing_priority": [
            {"priority": 0, "trigger": "integration exists", "action": "redirect to {name}-connect"},
            {"priority": 1, "trigger": "skill match", "action": "load skill"},
            {"priority": 2, "trigger": "project reference", "action": "load execute-project"},
            {"priority": 3, "trigger": "general", "action": "respond naturally"}
        ],
        "skill_matching": {
            "create-project": "START something NEW with deliverable",
            "execute-project": "references EXISTING project by name/ID",
            "create-skill": "AUTOMATE repeating work"
        },
        "never_do": [
            "Read project files directly - use execute-project",
            "Create project/skill folders directly - use create skills",
            "Auto-load learning skills - suggest, user decides"
        ],
        "menu_template": "00-system/core/orchestrator.md#menu-display",
        "project_index": [...],
        "skill_categories": {...},
        "user": {...}
    }
```

---

### Option D: Two-Phase Loading (~4K + lazy)

**Approach**: Inject minimal context immediately, load full orchestrator.md via tool call.

**Phase 1 (Injected - 4K tokens)**:
- Routing rules (structured)
- Project index (slim)
- Skill categories
- User context
- **Mandatory instruction**: "Before responding to user, Read('00-system/core/orchestrator.md')"

**Phase 2 (Lazy Load)**:
- Full orchestrator.md loaded via Read tool
- Full skill loaded via nexus-loader --skill
- Full project loaded via nexus-loader --project

**Token Budget (Phase 1 only)**:
| Component | Tokens |
|-----------|--------|
| Routing rules | 800 |
| Mandatory load instruction | 200 |
| Project index | 400 |
| Skill categories | 300 |
| User context | 300 |
| JSON overhead | 400 |
| **Total Injected** | **~2,400** |

**Pros**:
- Smallest injection - fastest startup
- Full orchestrator available after Read
- Matches current "read the file" intent but with guaranteed execution

**Cons**:
- Adds one Read tool call to every session start
- Latency of file read before Claude can respond
- Risk: What if Claude doesn't follow "mandatory" instruction?

**Mitigation for Risk**:
```python
# Use systemMessage to make instruction unavoidable
output = {
    "systemMessage": "STOP. You MUST Read('00-system/core/orchestrator.md') before ANY response.",
    "hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": json.dumps(slim_context)
    }
}
```

---

### Option E: Hybrid Mode Detection (~4K-12K dynamic)

**Approach**: Detect context and inject appropriate amount.

**Mode Detection**:
1. **New Session** (source=startup): Full orchestrator + slim metadata (~10K)
2. **Resume** (source=resume/compact): Just routing rules + last project state (~4K)
3. **Clear** (source=clear): Full orchestrator + slim metadata (~10K)

**Token Budgets**:
| Mode | What's Included | Tokens |
|------|-----------------|--------|
| startup | Full orchestrator + all indexes | 10,000 |
| resume | Routing rules + last project + action | 4,000 |
| clear | Full orchestrator + all indexes | 10,000 |

**Pros**:
- Optimized for each use case
- Resume mode extremely fast
- Claude already has orchestrator in context on resume

**Cons**:
- More complex implementation
- Need to track "what Claude knows" vs "what Claude lost"
- Resume assumption may be wrong after long gaps

**Implementation**:
```python
def generate_context_by_mode(source: str):
    if source in ("resume", "compact"):
        # Claude likely has orchestrator in context
        return generate_slim_resume()
    else:
        # New session - need full context
        return generate_full_startup()
```

---

## 3. Skill Category System

All options benefit from converting 100+ individual skills to categories:

### 3.1 Category Structure

```python
SKILL_CATEGORIES = {
    "integrations": {
        "airtable": {"count": 2, "trigger": "airtable, base, records"},
        "google": {"count": 8, "trigger": "gmail, calendar, docs, drive, sheets, slides, tasks"},
        "hubspot": {"count": 15, "trigger": "hubspot, contacts, deals, companies"},
        "slack": {"count": 20, "trigger": "slack, channel, message"},
        "notion": {"count": 2, "trigger": "notion, database, page"},
        "beam": {"count": 15, "trigger": "beam, task, agent"},
        "langfuse": {"count": 10, "trigger": "langfuse, trace, observation"},
        "heyreach": {"count": 10, "trigger": "heyreach, campaign, leads"}
    },
    "core": {
        "projects": {"skills": ["create-project", "execute-project"], "trigger": "project, work on"},
        "skills": {"skills": ["create-skill", "search-skill-database"], "trigger": "skill, automate"},
        "session": {"skills": ["close-session"], "trigger": "done, close, wrap up"}
    },
    "onboarding": {
        "skills": ["setup-memory", "setup-workspace", "learn-projects", "learn-skills", "learn-integrations", "learn-nexus"],
        "trigger": "setup, learn, onboarding, tutorial"
    },
    "research": {
        "skills": ["create-research-project", "analyze-research-project", "synthesize-research-project"],
        "trigger": "research, papers, analysis, synthesis"
    }
}
```

### 3.2 Lazy Load Triggers

```python
def match_skill_category(user_message: str) -> str | None:
    """Match user message to skill category, return master skill."""
    msg_lower = user_message.lower()

    # Check integration keywords
    for name, info in SKILL_CATEGORIES["integrations"].items():
        triggers = info["trigger"].split(", ")
        if any(t in msg_lower for t in triggers):
            return f"{name}-master"

    # Check core skills
    for category, info in SKILL_CATEGORIES["core"].items():
        triggers = info["trigger"].split(", ")
        if any(t in msg_lower for t in triggers):
            return info["skills"][0]  # Return first skill

    return None
```

---

## 4. Project Minimal Index

### 4.1 Current vs Slim

**Current** (per project ~300 tokens):
```json
{
    "id": "02-ontologies-research",
    "name": "Ontologies Research",
    "description": "Load when user mentions 'ontology', 'foundational ontology', 'UFO', 'DOLCE', 'BFO', 'entity types', '8-entity hypothesis', 'UDWO'",
    "status": "IN_PROGRESS",
    "onboarding": false,
    "created": "2025-12-27",
    "updated": null,
    "progress": 0.517,
    "tasks_total": 29,
    "tasks_completed": 15,
    "current_task": "Run `validate_analysis.py --check-chunk-index` on all papers",
    "_file_path": "C:\\Users\\dsber\\..."
}
```

**Slim** (per project ~40 tokens):
```json
{"id": "02", "name": "Ontologies Research", "status": "IN_PROGRESS", "progress": 52}
```

### 4.2 Routing Capability

Even with slim index, routing works:
```python
def match_project(user_message: str, project_index: list) -> str | None:
    """Match user message to project."""
    msg_lower = user_message.lower()

    for p in project_index:
        # ID match: "project 2", "02", "project 02"
        if p["id"] in msg_lower or f"project {p['id']}" in msg_lower:
            return p["id"]

        # Name match: "ontologies", "ontologies research"
        name_parts = p["name"].lower().split()
        if any(part in msg_lower for part in name_parts):
            return p["id"]

    return None
```

---

## 5. Session Start Hook Changes

### 5.1 Current Implementation (Broken)

```python
# session_start.py lines 159-180
output = f"""<NexusContext source="{source}" session="{session_id}">
!!!  MANDATORY STOP - DO NOT CONTINUE WORKING !!!
...
REQUIRED FIRST ACTION:
  Read("{cache_path}")
...
</NexusContext>"""

print(output, flush=True)  # Just stdout - not additionalContext!
```

**Problem**: This prints to stdout but doesn't use `hookSpecificOutput.additionalContext`.

### 5.2 Target Implementation (Direct Injection)

```python
# session_start.py - New approach
def main():
    input_data = json.load(sys.stdin)
    session_id = input_data.get("session_id", "unknown")
    source = input_data.get("source", "startup")

    # Generate slim context based on mode
    if source in ("resume", "compact"):
        context = generate_slim_resume()
    else:
        context = generate_slim_startup()

    # Output as proper hook response with additionalContext
    output = {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": json.dumps(context, ensure_ascii=False)
        }
    }

    print(json.dumps(output))

    # Fire-and-forget server notification (preserved)
    send_to_server(f"/api/v2/sessions/{session_id}/start", {...})
```

---

## 6. Orchestrator.md Handling Options

### 6.1 Option: Keep Full (~8K tokens)

**When to use**: If additionalContext budget allows ~12K total.

```python
def get_full_orchestrator():
    path = base_path / "00-system" / "core" / "orchestrator.md"
    return path.read_text(encoding="utf-8")
```

### 6.2 Option: Extract Critical Sections (~3.5K tokens)

**When to use**: If need to stay under 8K total.

```python
def extract_critical_orchestrator():
    full = get_full_orchestrator()

    # Remove ASCII banner (decorative)
    full = re.sub(r'```\n\s*███.*?```', '', full, flags=re.DOTALL)

    # Remove example suggestion blocks
    full = re.sub(r'\*\*Before first project:\*\*.*?```', '', full, flags=re.DOTALL)
    full = re.sub(r'\*\*When user mentions.*?```', '', full, flags=re.DOTALL)

    return full.strip()
```

### 6.3 Option: Structured Rules Only (~1K tokens)

**When to use**: If need minimal injection with lazy orchestrator load.

```python
def extract_routing_rules():
    """Extract just the decision logic as structured data."""
    return {
        "routing_priority": [
            {"priority": 0, "trigger": "integration name in message", "action": "load {name}-connect"},
            {"priority": 1, "trigger": "matches skill description", "action": "load skill"},
            {"priority": 2, "trigger": "mentions project name/ID", "action": "load execute-project"},
            {"priority": 3, "trigger": "no match", "action": "respond naturally"}
        ],
        "core_skills": {
            "create-project": "User wants NEW work with deliverable",
            "execute-project": "User references EXISTING project",
            "create-skill": "User wants to AUTOMATE patterns"
        },
        "never_do": [
            "Read project files directly",
            "Create project/skill folders directly",
            "Auto-load learning skills"
        ],
        "menu_display": "render from orchestrator.md template when action=display_menu",
        "language": "Check user-config.yaml language preference"
    }
```

---

## 7. Implementation Recommendations

### 7.1 Recommended Approach: Option B + E Hybrid

Combine "Essential Orchestrator Sections" with "Mode Detection":

**Startup Mode** (~8K tokens):
- Essential orchestrator sections (routing, menu, behavior rules)
- Project slim index
- Skill categories
- User context

**Resume Mode** (~4K tokens):
- Routing rules only (structured)
- Last active project state
- Skill categories (brief)
- Continue instruction

### 7.2 Implementation Steps

**Step 1: Create Slim Generator Functions in loaders.py**
```python
def generate_slim_startup(base_path: str) -> dict:
    """Generate startup context under 8K tokens."""

def generate_slim_resume(base_path: str) -> dict:
    """Generate resume context under 4K tokens."""

def extract_essential_orchestrator(base_path: str) -> str:
    """Extract critical orchestrator sections."""

def generate_project_index(base_path: str) -> list:
    """Generate slim project index."""

def generate_skill_categories(base_path: str) -> dict:
    """Generate skill category map."""
```

**Step 2: Update NexusService in service.py**
```python
def startup_slim(self, resume_mode: bool = False) -> dict:
    """Generate slim context for hook injection."""
```

**Step 3: Update Session Start Hook**
```python
# Use hookSpecificOutput.additionalContext
# Remove "read the file" instruction pattern
# Handle both startup and resume modes
```

**Step 4: Update CLI**
```python
# Add --slim flag to nexus-loader.py
# Default to slim for session hooks
# Keep full output available for debugging
```

---

## 8. Token Calculations by Option

### Option A: Full Orchestrator + Slim Metadata
| Component | Tokens |
|-----------|--------|
| orchestrator.md (full) | 8,000 |
| Project index (17 projects x 25 tokens) | 425 |
| Skill categories | 300 |
| User context | 200 |
| Instructions | 200 |
| JSON overhead | 500 |
| **Total** | **9,625** |

### Option B: Essential Orchestrator + Slim Metadata
| Component | Tokens |
|-----------|--------|
| orchestrator.md (essential) | 3,500 |
| system-map navigation | 500 |
| Project index | 500 |
| Skill categories | 500 |
| User context | 300 |
| Instructions | 200 |
| JSON overhead | 500 |
| **Total** | **6,000** |

### Option C: Routing Table Only
| Component | Tokens |
|-----------|--------|
| Routing rules (structured) | 800 |
| Skill matching rules | 500 |
| Project index | 400 |
| Skill categories | 300 |
| User context | 300 |
| Instructions | 200 |
| JSON overhead | 400 |
| **Total** | **2,900** |

### Resume Mode (Any Option)
| Component | Tokens |
|-----------|--------|
| Routing rules (structured) | 800 |
| Last active project state | 200 |
| Skill categories (brief) | 200 |
| Continue instruction | 100 |
| JSON overhead | 300 |
| **Total** | **1,600** |

---

## 9. Database Impact

### 9.1 No Impact Expected

The slim generator changes are **additive** and don't touch database calls:
- `send_to_server()` calls in session_start.py preserved
- Event payloads unchanged
- Fire-and-forget pattern maintained

### 9.2 Must Preserve

```python
# These lines in session_start.py MUST NOT be modified:
send_to_server(
    f"/api/v2/sessions/{session_id}/start",
    {
        "source_app": "mutagent-obsidian",
        "source": source,
        "timestamp": datetime.now().isoformat()
    }
)
```

---

## 10. Risk Analysis

### 10.1 Risks by Option

| Option | Risk | Mitigation |
|--------|------|------------|
| A (Full Orchestrator) | May exceed comfortable additionalContext limit | Monitor latency, fall back to Option B |
| B (Essential Sections) | May miss critical orchestrator content | Careful section extraction, test thoroughly |
| C (Routing Only) | Menu display may break | Include menu template path, test display |
| D (Two-Phase) | Claude may not follow "mandatory" instruction | Use systemMessage + additionalContext together |
| E (Hybrid) | Mode detection may be wrong | Conservative fallback to full context |

### 10.2 Testing Recommendations

1. **Token Counting**: Verify actual token counts with tiktoken or similar
2. **Menu Display**: Test menu rendering with each option
3. **Routing**: Test project/skill matching with slim indexes
4. **Resume Flow**: Test context summary -> resume cycle
5. **Latency**: Measure session start time with each option

---

## 11. Summary: Decision Matrix

| Option | Tokens | Orchestrator Intact | Complexity | Recommended For |
|--------|--------|---------------------|------------|-----------------|
| A: Full + Slim | 9,600 | 100% | Low | Maximum safety |
| B: Essential + Slim | 6,000 | 80% | Medium | **Best balance** |
| C: Routing Only | 2,900 | 20% | Medium | Minimal latency |
| D: Two-Phase | 2,400 | 0% (lazy) | High | Experimental |
| E: Hybrid | 4K-10K | Variable | High | Advanced optimization |

**Recommendation**: Start with **Option B** (Essential Orchestrator + Slim Metadata) as it provides the best balance of:
- Preserving critical behavior rules
- Fitting within reasonable additionalContext limits
- Maintaining routing capability
- Room for growth

If Option B proves too large in practice, fall back to **Option C + lazy orchestrator load**.
