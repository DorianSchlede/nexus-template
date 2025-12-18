# Release Notes

## v0.14.0 - Memory Auto-Scaffolding & Loader Refactor (2025-12-18)

### Auto-Scaffolding for New Users

Memory files now auto-create from templates on first startup.

#### Changes

- **Templates in `00-system/core/nexus/templates/`** - Default memory files stored as templates
- **Auto-scaffold on startup** - `nexus-loader.py --startup` creates `01-memory/` files if missing
- **New nexus/ package** - Refactored loader into modular Python package:
  - `config.py` - Paths and constants
  - `models.py` - SystemState enum
  - `utils.py` - File utilities
  - `loaders.py` - Project/skill/memory loading
  - `state.py` - State detection and stats
  - `sync.py` - Git sync operations
  - `service.py` - Main NexusService class

#### Why This Matters

- New users get scaffolded files automatically on first run
- Templates provide consistent starting point
- Cleaner loader architecture with modular components

---

## v0.13.0 - Display Hints & Mental Models Expansion (2025-12-18)

### Display Hints for Menu Rendering

Added `display_hints` to nexus-loader output to ensure AI never misses critical menu items.

#### Features

- **`stats.display_hints`** - Array of actionable hints AI must check before rendering menu
- **`instructions.display_hints`** - Same hints in instructions for immediate visibility
- Hints include:
  - `SHOW_UPDATE_BANNER: vX → vY` - Display update notification
  - `ONBOARDING_INCOMPLETE: N skills pending` - Emphasize onboarding
  - `PROMPT_SETUP_GOALS` - Suggest goals setup
  - `PROMPT_SETUP_WORKSPACE` - Suggest workspace setup

#### Why This Matters

Previously, conditional menu items (like update banners) could be missed when AI parsed the loader output. Display hints make critical items impossible to overlook.

### Mental Models Expansion

Expanded mental models from 30 to **59 models** across **12 categories**.

#### New Categories (4)
- **Time & Resource** - Eisenhower Matrix, Time Boxing, Opportunity Cost, Sunk Cost, Resource Mapping
- **Communication** - Pyramid Principle, BLUF, Situation-Complication-Resolution, Steel Manning
- **Learning** - Feynman Technique, Spaced Repetition, Deliberate Practice, T-Shaped Skills
- **Probability & Risk** - Expected Value, Margin of Safety, Black Swan, Bayesian Updating, Regret Minimization

#### New Structure

Models now stored as individual files in `00-system/mental-models/models/{category}/{model}.md` for better organization and loading.

#### Updated Scanner

```bash
python 00-system/mental-models/scripts/select_mental_models.py --format brief
python 00-system/mental-models/scripts/select_mental_models.py --category cognitive
python 00-system/mental-models/scripts/select_mental_models.py --format list
```

### Other Changes

- Removed HubSpot integration project (skills remain available)
- Added 4 tests for display_hints feature (14 total loader tests)
- Updated orchestrator with display_hints documentation
- Fixed beam-connect API key format

---

## v0.10.0 - HubSpot Integration (2025-12-13)

### New Integration: HubSpot CRM

Complete HubSpot CRM integration following the master/connect/specialized pattern.

#### Features

**CRM Operations (12 endpoints)**
- **Contacts**: List, Create, Update, Search
- **Companies**: List, Create, Search
- **Deals**: List, Create, Update, Search
- **Associations**: Get linked records between objects

**Engagement Operations (8 endpoints)**
- **Emails**: List, Log
- **Calls**: List, Log
- **Notes**: List, Create
- **Meetings**: List, Create

#### Architecture

```
00-system/skills/hubspot/
├── hubspot-master/          # Shared resources
│   ├── scripts/             # 20 Python scripts
│   │   ├── hubspot_client.py
│   │   ├── check_hubspot_config.py
│   │   ├── list_contacts.py
│   │   ├── create_contact.py
│   │   └── ... (16 more)
│   └── references/
│       ├── setup-guide.md
│       ├── api-reference.md
│       ├── error-handling.md
│       └── authentication.md
└── hubspot-connect/         # User entry point
    └── SKILL.md             # Meta-skill with routing
```

#### Usage

Say any of these to trigger HubSpot operations:
- "hubspot" / "list contacts" / "show companies"
- "create contact john@example.com"
- "search deals enterprise"
- "list meetings" / "log call"

#### Setup

1. Create HubSpot Private App (Settings → Integrations → Private Apps)
2. Add required scopes (crm.objects.contacts.read/write, etc.)
3. Copy access token to `.env` as `HUBSPOT_ACCESS_TOKEN`

#### Technical Notes

- Token format: EU accounts use `pat-eu1-...`, US use `pat-na1-...`
- Rate limits: 100 requests/10 seconds, 500,000/day
- Scope changes regenerate access tokens

### Other Changes

- Added `hubspot` to integration auto-detection in nexus-loader.py
- Added `pending_onboarding` stats for proactive skill suggestions
- Minor updates to learning skills and orchestrator

---

## Previous Releases

### v0.9.0 (2025-12-11)
- Dynamic integrations menu
- Improved integration detection
- README updates
