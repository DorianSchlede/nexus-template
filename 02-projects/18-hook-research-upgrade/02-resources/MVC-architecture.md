# Minimum Viable Context (MVC) Architecture

**Purpose**: Define the smallest context needed for Claude to function at session start, with intelligent lazy loading for everything else.

**Status**: DESIGN PHASE - Options to be evaluated by subagent research

---

## Core Principle

**Load the MINIMUM needed to route, then load details on-demand.**

Current problem: 26K+ tokens at startup (orchestrator, all projects, all skills, all memory)
Goal: Reduce startup context significantly, lazy load the rest

---

## Required Components (ALWAYS LOADED)

These are non-negotiable - Claude needs them to function:

1. **orchestrator.md** - Core behavior rules, routing logic, menu display
   - Current: ~8K tokens (full)
   - Options to explore: slim version? critical sections only?

2. **user-config.yaml** - Language preference, settings
   - Small, always needed

3. **Routing capability** - Ability to say "project 5" or "hubspot"
   - Need SOME index of projects and skills

---

## Two Modes: Startup vs Resume

### STARTUP Mode (`--startup`)

**User intent**: "I'm starting fresh, orient me"

**Required Context** (research should determine exact format):
```
1. Orchestrator (behavior rules)
   - MUST include: routing rules, menu display, core concepts
   - QUESTION: Full orchestrator or extracted sections?

2. Orientation (what is this system?)
   - system-map.md (how much?)
   - workspace-map.md (if exists)

3. User context (who am I?)
   - user-config.yaml (language, preferences)
   - goals.md (how much? full or summary?)

4. Routing index (what can I do?)
   - Project index: what fields are minimum?
   - Skill index: full list or categories?
```

**Token Budget**: TBD by research - aim for smallest that works

**Lazy Loading Candidates**:
- Full skill descriptions → load on match
- Full project details → load on reference
- memory-map.md → rarely needed
- core-learnings.md → load on request

---

### RESUME Mode (`--resume`)

**User intent**: "Continue where I left off"

**Required Context** (research should determine exact format):
```
1. Orchestrator (behavior rules) - STILL NEEDED
   - Claude loses context on resume/compact
   - QUESTION: Same as startup or smaller?

2. Last active state
   - Last project ID + name + current_task
   - Last skill (if any)

3. Routing index
   - Enough to say "switch to project X"
   - QUESTION: Same as startup or smaller?

4. Resume instruction
   - "Continue working on {project} at {current_task}"
```

**Token Budget**: TBD by research

**Lazy Loading on Resume**:
- Full project details → load via --project
- Full skill content → load via --skill
- Orientation docs (maybe skip if context retained?)

---

## Skill Lazy Loading System

### Current Problem
100+ skills loaded with full descriptions = massive token waste

### Solution: Category-Based Progressive Disclosure

**Level 0 - Index Only (loaded at startup)**:
```json
{
  "skill_categories": {
    "integrations": {
      "airtable": ["airtable-connect", "airtable-master"],
      "google": ["google-connect", "gmail", "google-calendar", "google-docs", "google-drive", "google-sheets", "google-slides", "google-tasks"],
      "hubspot": ["hubspot-connect", "hubspot-master", "hubspot-create-contact", ...],
      "slack": ["slack-connect", "slack-master"],
      "notion": ["notion-connect", "notion-master"],
      "beam": ["beam-connect", "beam-master"],
      "langfuse": ["langfuse-connect", "langfuse-master"],
      "heyreach": ["heyreach-connect", "heyreach-master"]
    },
    "projects": ["create-project", "execute-project"],
    "skills": ["create-skill", "search-skill-database", "import-skill", "share-skill"],
    "onboarding": ["setup-memory", "setup-workspace", "learn-projects", "learn-skills", "learn-integrations", "learn-nexus"],
    "session": ["close-session"],
    "research": ["create-research-project", "analyze-research-project", "synthesize-research-project"]
  }
}
```

**Level 1 - Category Trigger (loaded on category match)**:
When user says "airtable" → load airtable category master skill

**Level 2 - Specific Skill (loaded on action match)**:
When user says "create contact in hubspot" → load hubspot-create-contact SKILL.md

### Matching Logic
```
User message: "add a contact to hubspot"

1. Check category keywords: "hubspot" matches integrations.hubspot
2. Load hubspot-master SKILL.md (has all action descriptions)
3. hubspot-master routes to hubspot-create-contact
4. Load hubspot-create-contact SKILL.md
```

---

## Project Minimal Index

### Current Problem
17 projects with full metadata, descriptions, file paths = token waste

### Solution: Slim Index

**Startup Index** (loaded always):
```json
{
  "projects": [
    {"id": "01", "name": "ICP Definition", "status": "PLANNING", "progress": 3},
    {"id": "02", "name": "Ontologies Research", "status": "IN_PROGRESS", "progress": 52},
    {"id": "03", "name": "NotebookLM Integration", "status": "PLANNING", "progress": 78},
    ...
  ]
}
```

**That's it.** No descriptions, no file paths, no current_task at index level.

### Routing Logic
```
User: "continue project 2"
       OR "work on ontologies"
       OR "ontologies research"

1. Match against project index (id OR name fuzzy match)
2. THEN load full project via nexus-loader.py --project 02
3. Full project includes: overview.md, plan.md, steps.md, _resume.md
```

---

## Implementation: New Startup Flow

### Step 1: Generate Slim Cache

```python
def generate_slim_startup_cache():
    return {
        "mode": "startup",
        "token_budget": 4000,

        # Orientation (slim)
        "orientation": {
            "system_type": "Nexus - AI Operating System",
            "key_concepts": ["Projects (temporal work)", "Skills (reusable workflows)"],
            "routing_rules": extract_routing_rules()  # Just the table from orchestrator
        },

        # User context (slim)
        "user": {
            "role": "...",  # From goals.md, first line only
            "goal": "...",  # From goals.md, short-term only
            "language": "English"
        },

        # Indexes (no full content)
        "project_index": [
            {"id": "01", "name": "...", "status": "...", "progress": 0}
        ],

        "skill_categories": {
            "integrations": {...},
            "projects": [...],
            ...
        },

        # Instructions
        "action": "display_menu",
        "lazy_load_hint": "Use --project ID or --skill NAME to load details"
    }
```

### Step 2: Lazy Load on Demand

```python
# When user says "work on project 2"
nexus-loader.py --project 02-ontologies-research

# When user says "hubspot"
nexus-loader.py --skill hubspot-master

# When user says "create contact in hubspot"
nexus-loader.py --skill hubspot-create-contact
```

### Step 3: Resume Flow

```python
def generate_slim_resume_cache():
    return {
        "mode": "resume",
        "token_budget": 2000,

        # Last state
        "last_active": {
            "project_id": "02-ontologies-research",
            "project_name": "Ontologies Research",
            "current_task": "Run validate_analysis.py on all papers",
            "progress": 52
        },

        # Minimal routing index
        "project_index": [...],  # Same as startup but even slimmer
        "skill_categories": {...},

        # Instructions
        "action": "continue_working",
        "instruction": "Continue 'Ontologies Research' - current task: Run validate_analysis.py"
    }
```

---

## Token Budget - OPTIONS TO EXPLORE

Research should provide multiple options with tradeoffs:

### Option A: Minimal (~5K tokens)
- Orchestrator: extracted routing rules only (~1K)
- Project index: id/name/status only
- Skill index: categories only
- **Tradeoff**: May lose important orchestrator context

### Option B: Balanced (~8K tokens)
- Orchestrator: core sections (routing, concepts, menu)
- Project index: id/name/status/progress
- Skill index: categories + descriptions
- **Tradeoff**: Larger but more complete

### Option C: Full Orchestrator (~12K tokens)
- Orchestrator: complete (~8K)
- Project index: slim
- Skill index: categories only
- **Tradeoff**: Orchestrator intact, everything else lazy

### Option D: Smart Compression
- Orchestrator: minified version (remove examples, keep rules)
- Indexes: optimized format
- **Tradeoff**: Need to create/maintain minified orchestrator

**Decision**: TBD after research - need to understand what Claude actually needs

---

## Migration Path

### Phase 1: New Cache Generator
- Create `generate_slim_cache()` in nexus-loader
- Output to new file: `context_slim.json`
- Keep old cache for fallback

### Phase 2: Update Session Start Hook
- Read slim cache instead of full cache
- Inject as additionalContext (small enough now!)
- No more "go read the file" instruction

### Phase 3: Update Routing Logic
- Match against slim indexes
- Lazy load via --project and --skill flags
- Progressive disclosure for integrations

### Phase 4: Deprecate Full Cache
- Remove full cache generation
- All context is now slim + lazy loaded

---

## Success Metrics

- [ ] Startup context < 5K tokens
- [ ] Resume context < 2K tokens
- [ ] No "read the file" instructions needed
- [ ] User can say "project 5" and it works
- [ ] User can say "hubspot" and it loads right skill
- [ ] Integration skills are grouped (not 20 separate entries)
