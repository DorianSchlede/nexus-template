---
name: create-master-skill
description: "create master skill, integration master, shared skill library."
---

-------------------------------------------------------
[!] CRITICAL EXECUTION REQUIREMENTS [!]

WORKFLOW: Build FIRST, Research SECOND, Build THIRD

MANDATORY STEPS (DO NOT SKIP):
1. [OK] Create TodoWrite with ALL phases
2. [OK] Ask integration name (e.g., "airtable", "slack", "github")
3. [OK] RUN plan-build skill to create planning build
4. [OK] PHASE 1: Web Research - comprehensive API/integration research
5. [OK] PHASE 2: Architecture Design - define master skill structure
6. [OK] PHASE 3: Build - create master skill from templates
7. [OK] PHASE 4: Validate - test and document

ANTI-PATTERN (DO NOT DO THIS):
[ERROR] Skip build creation
[ERROR] Start building without research
[ERROR] Create master skill without understanding the integration
[ERROR] Copy from notion-master without adapting
[ERROR] Skip validation phase

CORRECT PATTERN (DO THIS):
[OK] Ask integration → Create build → Research → Design → Build → Validate
-------------------------------------------------------

# Create Master Skill

Build production-ready master skills (shared resource libraries) for any integration.

## Purpose

Master skills solve the **duplication problem**: When 3+ skills share common content (setup, API docs, error handling), extract it into a master skill that all can reference.

**Key Insight from notion-master:**
- 3 Notion skills had 950 lines of duplicated content
- After extraction: 60% context reduction (950 → 370 lines)
- Single source of truth for setup, API, errors, schemas

---

## Quick Start

**User says:** "create master skill for Airtable"

**AI does:**
1. Creates planning build: `{ID}-airtable-master-skill`
2. Runs comprehensive web research on Airtable API
3. Designs architecture based on research
4. Builds master skill from templates
5. Validates and documents

---

## Workflow

### Phase 0: Initiation

```
[*] CREATE MASTER SKILL

What integration do you want to create a master skill for?
Examples: airtable, slack, github, linear, google-sheets, stripe

Integration name: ___________
```

**After user provides name:**
1. Validate name (lowercase, hyphenated)
2. Check if `{integration}-master` already exists
3. Create planning build using `plan-build` skill

---

### Phase 1: Web Research (CRITICAL)

**Purpose:** Gather comprehensive information before building anything.

**Run these searches:**

```markdown
## Research Tasks

1. **API Documentation**
   - Search: "{integration} API documentation official"
   - Capture: Base URLs, authentication, rate limits

2. **API Reference**
   - Search: "{integration} API endpoints reference"
   - Capture: Key endpoints, request/response formats

3. **Authentication Patterns**
   - Search: "{integration} API authentication OAuth API key"
   - Capture: Auth methods, token handling, refresh patterns

4. **Common Operations**
   - Search: "{integration} API CRUD operations examples"
   - Capture: Create, read, update, delete patterns

5. **Error Handling**
   - Search: "{integration} API error codes troubleshooting"
   - Capture: Error codes, messages, recovery patterns

6. **Rate Limits**
   - Search: "{integration} API rate limits throttling"
   - Capture: Limits, backoff strategies, best practices

7. **SDK/Libraries**
   - Search: "{integration} Python SDK library"
   - Capture: Official SDK, popular libraries, installation

8. **Best Practices**
   - Search: "{integration} API best practices integration"
   - Capture: Patterns, anti-patterns, optimization tips
```

**Save research to:** `02-builds/{ID}-{integration}-master-skill/02-resources/research.md`

---

### Phase 2: Architecture Design

**Based on research, design the master skill structure:**

1. **Identify Child Skills** - What specific skills will use this master?
   - Query/search operations
   - Import/export operations
   - Management operations
   - Automation/workflow operations

2. **Define Shared Resources**
   - What setup steps are common?
   - What API patterns are reused?
   - What errors occur across all operations?
   - What schemas/types need documentation?

3. **Plan Scripts**
   - Configuration validation script
   - Resource discovery script
   - Common utility functions
   - Rate limiting (if needed)

**Document architecture in:** `02-builds/{ID}-{integration}-master-skill/01-planning/plan.md`

---

### Phase 3: Build Master Skill

**Use templates from:** `create-master-skill/templates/`

1. **Create folder structure:**
   ```
   00-system/skills/{integration}-master/
   ├── SKILL.md
   ├── references/
   │   ├── setup-guide.md
   │   ├── api-reference.md
   │   ├── error-handling.md
   │   └── [domain-specific].md
   ├── scripts/
   │   ├── check_{integration}_config.py
   │   ├── discover_resources.py
   │   └── [operation scripts].py
   └── tests/
       ├── README.md
       └── run_tests.py
   ```

2. **Populate from templates** (adapting to research)

3. **Fill in integration-specific content**

---

### Phase 4: Validate

1. **Run config check:** `python scripts/check_{integration}_config.py`
2. **Test discovery:** `python scripts/discover_resources.py`
3. **Verify documentation completeness**
4. **Create at least one child skill** that uses the master

---

## Resources

### templates/

**[SKILL.md.template](templates/SKILL.md.template)** - Master skill declaration template

**[setup-guide.md.template](templates/setup-guide.md.template)** - Setup wizard template

**[api-reference.md.template](templates/api-reference.md.template)** - API documentation template

**[error-handling.md.template](templates/error-handling.md.template)** - Error handling template

**[check_config.py.template](templates/check_config.py.template)** - Config validation script template

### references/

**[master-skill-patterns.md](references/master-skill-patterns.md)** - Architecture patterns from notion-master

**[research-checklist.md](references/research-checklist.md)** - Comprehensive research checklist

---

## Example: Creating Airtable Master Skill

```
User: "create master skill for airtable"

AI: "I'll help you create an Airtable master skill. First, let me create
     a planning build to organize this work."

     → Runs plan-build skill
     → Creates: 04-airtable-master-skill build

AI: "Build created. Now I'll research the Airtable API comprehensively."

     → Runs 8 web searches
     → Saves findings to research.md

AI: "Research complete. Based on findings, I recommend these child skills:
     - airtable-connect (query any base/table)
     - airtable-sync (import/export records)
     - airtable-automate (trigger-based workflows)

     The master skill will provide:
     - Setup guide (API key, base IDs)
     - API reference (REST endpoints, field types)
     - Error handling (rate limits, validation errors)
     - Scripts (config check, base discovery)

     Shall I proceed with building?"

User: "Yes"

AI: → Creates 00-system/skills/airtable-master/
    → Populates from templates
    → Adapts content based on research
    → Validates setup
```

---

## Success Criteria

A master skill is complete when:

- [ ] **SKILL.md** clearly says "DO NOT load directly"
- [ ] **setup-guide.md** covers first-time setup end-to-end
- [ ] **api-reference.md** documents key operations
- [ ] **error-handling.md** covers common errors with solutions
- [ ] **check_config.py** validates all required configuration
- [ ] **At least one child skill** successfully references it
- [ ] **Context reduction** achieved (measure before/after)

---

## Why This Design?

**Why Build First?**
- Complex work deserves proper planning
- Research findings need a home
- Progress tracked via build tasks
- Validates the approach before building

**Why Research First?**
- Every integration is different
- API patterns vary significantly
- Prevents wrong assumptions
- Ensures comprehensive coverage

**Why Templates?**
- Consistent structure across master skills
- Proven patterns from notion-master
- Reduces cognitive load
- Accelerates development

---

**Version**: 1.0
**Created**: 2025-12-11
**Based on**: notion-master architecture analysis
