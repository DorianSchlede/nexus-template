# Integration Architecture Comparison

**Created**: 2026-01-07
**Source**: Deep audit of add-integration vs create-master-skill

---

## Executive Summary

Two skills exist for creating integrations. After comprehensive audit, **add-integration** is the better choice but has a critical bug.

| Criteria | add-integration | create-master-skill | Winner |
|----------|:---------------:|:-------------------:|:------:|
| Creates complete structure | ✅ master + connect + ops | ❌ master only | add-integration |
| Templates | 11 production-ready | 6 partial | add-integration |
| Auth support | 3 types | Generic placeholders | add-integration |
| Post-scaffold work | LOW | HIGH (100+ placeholders) | add-integration |
| Research depth | 2-3 searches | 10 searches | create-master-skill |
| Test templates | ❌ None | ✅ Yes | create-master-skill |
| **Critical Bug** | Scaffold never runs | Workflow violation | Both broken |

---

## The 3-Tier Integration Architecture

Both skills aim to create this structure:

```
{service}/
├── {service}-master/           # Tier 1: Shared resources
│   ├── SKILL.md                # "DO NOT LOAD DIRECTLY"
│   ├── scripts/
│   │   ├── {service}_client.py # API client
│   │   ├── check_{service}_config.py  # Pre-flight validation
│   │   └── setup_{service}.py  # Interactive setup
│   └── references/
│       ├── setup-guide.md
│       ├── api-reference.md
│       ├── error-handling.md
│       └── authentication.md
│
├── {service}-connect/          # Tier 2: User entry point
│   └── SKILL.md                # Routes to operations
│
└── {service}-{operation}/      # Tier 3: Per-endpoint skills
    ├── SKILL.md
    └── scripts/
        └── {operation}.py
```

**Why this pattern?**
- **DRY**: Shared docs in master, not duplicated
- **Progressive disclosure**: Users start at connect, drill into operations
- **AI-friendly**: Config check returns `ai_action` field

---

## add-integration: What It Does

### Workflow (8 Steps)

1. Initialize TodoList
2. Ask service name
3. WebSearch for API docs
4. Create integration project
5. Parse and present endpoints
6. User selects endpoints
7. Gather auth details, write `integration-config.json`
8. **BROKEN**: Says "execute-project will scaffold" but doesn't

### What It Creates

**During Planning**:
```
02-projects/{id}-{service}-integration/
├── 01-planning/
│   ├── 01-overview.md
│   ├── 03-plan.md
│   └── 04-steps.md
└── 02-resources/
    └── integration-config.json  ← KEY OUTPUT
```

**Should Create (but doesn't)**:
```
00-system/skills/{service}/
├── {service}-master/
├── {service}-connect/
└── {service}-{operation}/ × N
```

### Templates (11 total)

| Template | Lines | Purpose |
|----------|-------|---------|
| master-skill.md | 130 | Master SKILL.md |
| connect-skill.md | 127 | Connect SKILL.md |
| operation-skill.md | 74 | Per-operation SKILL.md |
| api-client.py | 124 | Shared API client |
| config-check.py | 164 | Pre-flight validation |
| setup-wizard.py | 153 | Interactive setup |
| operation-script.py | 85 | Per-operation Python |
| setup-guide.md | 95 | Setup documentation |
| api-reference.md | 60 | API endpoint docs |
| error-handling.md | 123 | Troubleshooting |
| authentication.md | 81 | Auth documentation |

### Scaffold Script

**Location**: `scripts/scaffold_integration.py` (859 lines)

**Input**: `integration-config.json`
```json
{
  "service_name": "HubSpot",
  "service_slug": "hubspot",
  "base_url": "https://api.hubapi.com",
  "auth_type": "oauth2|api_key|bearer",
  "env_key": "HUBSPOT_API_KEY",
  "endpoints": [...]
}
```

**Auth Types Supported**:
- `oauth2` - Token refresh, client credentials
- `bearer` - API key as Bearer token
- `api_key` - X-API-Key header

---

## create-master-skill: What It Does

### Workflow (5 Phases)

0. Ask integration name
1. Web research (8 comprehensive searches)
2. Architecture design (identify child skills)
3. Build from templates
4. Validate

### What It Creates

```
{integration}-master/
├── SKILL.md
├── references/ (3 files)
├── scripts/ (2 files)
└── tests/ (2 files)
```

**Missing**: connect skill, operation skills

### Templates (6 total)

| Template | Purpose |
|----------|---------|
| SKILL.md.template | Master SKILL.md |
| setup-guide.md.template | Setup docs |
| api-reference.md.template | API docs |
| error-handling.md.template | Troubleshooting |
| check_config.py.template | Config validation |
| discover_resources.py.template | Resource discovery |

### Scaffold Script

**Location**: `scripts/init_master_skill.py` (390 lines)

**Input**: Just integration name
**Output**: 100+ placeholders to fill manually

---

## Critical Bugs

### add-integration Bug

```
SKILL.md Step 8:
"When the user returns and says 'work on {service} integration',
the execute-project skill will run scaffold_integration.py"

REALITY:
- execute-project doesn't know about scaffold_integration.py
- No detection of integration projects
- Users get plans, ZERO skills generated
```

**Fix Options**:
1. Minimal: Add scaffold command to steps.md output
2. Better: Auto-execute scaffold after config finalization
3. Complete: Integrate with execute-project detection

### create-master-skill Bug

```
SKILL.md:
"RUN create-project skill to create planning project"

REALITY:
- init_master_skill.py doesn't create project
- Directly creates skill structure
- Violates "project FIRST" principle
```

---

## What to Merge from create-master-skill

### HIGH VALUE

1. **tests/ folder**
   - `run_tests.py.template` - Test runner
   - `README.md.template` - Test docs
   - add-integration has NO tests

2. **research-checklist.md** (353 lines)
   - 10 comprehensive search areas
   - add-integration only does 2-3 searches

3. **master-skill-patterns.md** (278 lines)
   - DRY architecture documentation
   - Context reduction metrics
   - Anti-patterns

4. **discover_resources.py.template**
   - Helps users discover account resources
   - add-integration doesn't have this

### MEDIUM VALUE

5. **Workflow enforcement**
   - Project-first pattern
   - Validation before scaffold

---

## Production Integration Analysis

All 9 production integrations in `03-skills/` use the master pattern:

| Integration | Scripts | Pattern | Notes |
|-------------|---------|---------|-------|
| Airtable | 14 (5.5K LOC) | Master | Multi-token |
| Beam | 28 | Master | Token auto-refresh |
| Google | 9 per service | Master | Unified OAuth |
| HubSpot | 25 | Master | CRUD per object |
| Langfuse | 71+ | Master | One per endpoint |
| Notion | 13 (6.3K LOC) | Master | 60% context reduction |
| Slack | 46 | Master | User OAuth |
| NotebookLM | 15 | Master | gcloud CLI |
| HeyReach | 12 | Master | LinkedIn automation |

**Key Finding**: All use master pattern, none were created by add-integration (scaffold never ran).

---

## Recommendation

1. **Fix add-integration** (this project)
   - Execute scaffold during workflow
   - Merge high-value components from create-master-skill

2. **Keep create-master-skill** for edge cases
   - Complex integrations needing deep research
   - Non-standard auth patterns
   - Add deprecation notice pointing to add-integration

3. **Route integration type** to add-integration
   - Already done in `_type.yaml`
   - See Project 30 decision

---

## References

- Full add-integration audit: `02-resources/audit-add-integration.md`
- Full create-master-skill audit: `02-resources/audit-create-master-skill.md`
- Production integrations: `03-skills/*/`
- Decision record: `30-improve-plan-project-skill/01-planning/resume-context.md`
