# Subagent Briefing: MVC (Minimum Viable Context) Implementation Research

**Priority**: CRITICAL (highest priority - fixes broken session start)
**Output Path**: `02-projects/18-hook-research-upgrade/02-resources/research-mvc-context.md`

---

## Mission

Research how to implement Minimum Viable Context (MVC) for Nexus. The current system loads 26K+ tokens at startup which is too large.

**KEY CONSTRAINT**: orchestrator.md MUST always be loaded - it contains Claude's behavior rules. Research should explore OPTIONS for how to include it efficiently.

**Goal**: Provide MULTIPLE OPTIONS with tradeoffs, not a fixed decision. We want to choose the best approach after seeing all options.

---

## Required Reading (IN ORDER - READ EVERYTHING)

### Step 1: Understand the MVC Architecture
```
READ: 02-projects/18-hook-research-upgrade/02-resources/MVC-architecture.md
```
This defines the target state. Understand:
- Startup vs Resume modes
- Skill category-based lazy loading
- Project minimal index
- Token budgets (4K startup, 2K resume)

### Step 2: Current Nexus Loader Implementation
```
READ: 00-system/core/nexus-loader.py
```
Understand current implementation. Note what it outputs.

```
READ: 00-system/core/nexus/service.py
```
The NexusService class that handles startup().

```
READ: 00-system/core/nexus/loaders.py
```
Functions that scan projects and skills.

### Step 3: Current Cache Output
```
READ: 00-system/.cache/context_startup.json (first 200 lines)
```
See what's currently generated. Identify bloat.

### Step 4: Session Start Hook
```
READ: .claude/hooks/session_start.py
```
Understand how cache is consumed. The "read the file" pattern is broken.

### Step 5: Context Loading Research
```
READ: 04-workspace/00-ai-native-org/hook-research/hook-guides/CONTEXT_LOADING.md
```
Understand additionalContext injection limits and best practices.

---

## Key Problems to Solve

### Problem 1: Cache Too Large
- Current: 26K+ tokens
- Need to reduce significantly
- **KEY**: orchestrator.md (~8K) MUST be included - it's Claude's brain

### Problem 2: "Read the File" Doesn't Work
- Current: Hook outputs "go read cache file"
- Claude doesn't reliably follow this instruction
- Solution: Inject context directly as additionalContext

### Problem 3: All Skills Loaded
- Current: 100+ skills with full descriptions
- Explore: Category index only, lazy load on match?
- Explore: Skill categories with progressive disclosure?

### Problem 4: All Projects Loaded
- Current: 17 projects with full metadata
- Explore: Slim index (id, name, status, progress only)?
- Need: Ability to say "do project 5" and have it work

### Problem 5: Orchestrator is Large
- orchestrator.md is ~8K tokens
- MUST be loaded (contains behavior rules)
- Explore: Can we minify? Extract critical sections? Keep full?

---

## Output Format

Create file at:
```
02-projects/18-hook-research-upgrade/02-resources/research-mvc-context.md
```

Structure:

```markdown
# MVC Context Implementation Research

## Executive Summary
[2-3 sentences: How to implement MVC for Nexus]

---

## 1. Current State Analysis

### Current Token Usage
| Component | Tokens | Needed? |
|-----------|--------|---------|
| orchestrator.md | ~8000 | NO - extract routing rules only |
| system-map.md | ~2000 | SLIM - just structure |
| memory-map.md | ~1500 | NO - rarely used |
| goals.md | ~500 | SLIM - role + goal only |
| user-config.yaml | ~300 | YES |
| projects (17) | ~5000 | SLIM - index only |
| skills (100+) | ~8000 | CATEGORY INDEX - lazy load |
| **Total** | ~26000 | Target: <5000 |

### Current Flow Problems
1. [Problem 1 with specific code location]
2. [Problem 2 with specific code location]
...

---

## 2. Slim Cache Generator Design

### New Function: generate_slim_startup()
\`\`\`python
def generate_slim_startup(base_path: str) -> dict:
    """Generate <5K token startup context."""
    return {
        "mode": "startup",
        "token_budget": 4000,

        "orientation": {
            # Extracted from orchestrator.md - just routing table
        },

        "user": {
            # From goals.md - role + goal only
            # From user-config.yaml - language
        },

        "project_index": [
            # Slim: id, name, status, progress only
        ],

        "skill_categories": {
            # Category groups, not individual skills
        },

        "action": "display_menu"
    }
\`\`\`

### New Function: generate_slim_resume()
\`\`\`python
def generate_slim_resume(base_path: str) -> dict:
    """Generate <2K token resume context."""
    return {
        "mode": "resume",
        "token_budget": 2000,

        "last_active": {
            # From _resume.md
        },

        "project_index": [...],
        "skill_categories": {...},

        "action": "continue_working"
    }
\`\`\`

---

## 3. Routing Rules Extraction

### Current: Full orchestrator.md (~8K tokens)

### Target: Extracted routing table (~800 tokens)
\`\`\`python
def extract_routing_rules() -> dict:
    """Extract just the routing logic from orchestrator.md"""
    return {
        "priority_order": [
            {"trigger": "integration exists", "action": "redirect to {name}-connect"},
            {"trigger": "skill match", "action": "load skill"},
            {"trigger": "project reference", "action": "load execute-project"},
            {"trigger": "general", "action": "respond naturally"}
        ],
        "skill_matching": "semantic, not just keywords",
        "project_matching": "id OR name fuzzy match"
    }
\`\`\`

---

## 4. Skill Category System

### Category Structure
\`\`\`python
SKILL_CATEGORIES = {
    "integrations": {
        "airtable": ["airtable-connect", "airtable-master"],
        "google": ["google-connect", "gmail", "google-calendar", ...],
        "hubspot": ["hubspot-connect", "hubspot-master", ...],
        # ... more integrations
    },
    "projects": ["create-project", "execute-project"],
    "skills": ["create-skill", "search-skill-database", ...],
    "onboarding": ["setup-memory", "setup-workspace", ...],
    "research": ["create-research-project", "analyze-research-project", ...]
}
\`\`\`

### Lazy Load Trigger
\`\`\`python
def match_skill_category(user_message: str) -> str | None:
    """Match user message to skill category."""
    # Check integration keywords
    for integration, skills in SKILL_CATEGORIES["integrations"].items():
        if integration.lower() in user_message.lower():
            return f"{integration}-master"

    # Check other categories
    # ...
\`\`\`

---

## 5. Project Minimal Index

### Index Structure
\`\`\`python
def generate_project_index(base_path: str) -> list:
    """Generate slim project index."""
    projects = scan_projects(base_path, minimal=True)
    return [
        {
            "id": p["id"],
            "name": p["name"],
            "status": p["status"],
            "progress": int(p["progress"] * 100)
        }
        for p in projects
    ]
\`\`\`

### Routing Logic
\`\`\`python
def match_project(user_message: str, project_index: list) -> str | None:
    """Match user message to project."""
    # Check by ID: "project 2", "project 02"
    # Check by name: "ontologies", "ontologies research"
    # Fuzzy match
\`\`\`

---

## 6. Session Start Hook Changes

### Current (Broken)
\`\`\`python
# Outputs "go read cache file" - doesn't work
output = f"Read({cache_path})"
print(output)
\`\`\`

### Target (Direct Injection)
\`\`\`python
# Inject slim context directly as additionalContext
slim_context = generate_slim_startup()
output = {
    "hookSpecificOutput": {
        "additionalContext": json.dumps(slim_context)
    }
}
print(json.dumps(output))
\`\`\`

---

## 7. Implementation Plan

### Step 1: Create Slim Generator Functions
- [ ] `generate_slim_startup()` in loaders.py
- [ ] `generate_slim_resume()` in loaders.py
- [ ] `extract_routing_rules()` helper
- [ ] `generate_project_index()` helper
- [ ] `generate_skill_categories()` helper

### Step 2: Update NexusService
- [ ] Add `startup_slim()` method
- [ ] Add `resume_slim()` method
- [ ] Keep old methods for backward compatibility

### Step 3: Update Session Start Hook
- [ ] Remove "read the file" pattern
- [ ] Direct additionalContext injection
- [ ] Handle both startup and resume modes

### Step 4: Update CLI
- [ ] Add `--slim` flag to nexus-loader.py
- [ ] Default to slim for session hooks
- [ ] Full output still available for debugging

---

## 8. Token Calculations

### Startup Budget Breakdown
| Component | Est. Tokens | Calculation |
|-----------|-------------|-------------|
| Routing rules | 800 | 200 words * 4 |
| User context | 200 | 50 words * 4 |
| Project index (17) | 500 | 17 * 30 chars |
| Skill categories | 300 | 75 words * 4 |
| Orientation | 500 | 125 words * 4 |
| Instructions | 200 | 50 words * 4 |
| JSON overhead | 500 | ~20% |
| **Total** | **3000** | Under 4K budget |

### Resume Budget Breakdown
| Component | Est. Tokens | Calculation |
|-----------|-------------|-------------|
| Last active | 300 | 75 words * 4 |
| Project index | 400 | 17 * 25 chars |
| Skill categories | 300 | 75 words * 4 |
| Instructions | 200 | 50 words * 4 |
| JSON overhead | 300 | ~20% |
| **Total** | **1500** | Under 2K budget |

---

## 9. Database Impact

### No Impact Expected
- Slim generator doesn't touch database calls
- Session start hook preserves send_to_server()
- All changes are additive

### Must Preserve
- send_to_server() calls in session_start.py
- Event payloads unchanged
- Fire-and-forget pattern
```

---

## Success Criteria

- [ ] Token calculations for startup (<5K) and resume (<2K)
- [ ] Slim generator function designs
- [ ] Routing rules extraction method
- [ ] Skill category system documented
- [ ] Project index structure defined
- [ ] Session start hook changes specified
- [ ] Implementation plan with clear steps
- [ ] No database impact confirmed

---

## DO NOT

- ❌ Implement anything - research only
- ❌ Break existing nexus-loader functionality
- ❌ Remove any database calls
- ❌ Change event payloads
- ❌ Skip token calculations - they're critical
