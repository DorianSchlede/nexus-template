# Release Notes

## v0.15.1 - HeyReach Integration (2025-12-19)

### New Integration: HeyReach

Complete HeyReach LinkedIn automation integration.

#### Features

**Campaign Operations**
- List all campaigns
- Get campaign details
- Pause/resume campaigns

**Lead Operations**
- Add leads to campaigns (by LinkedIn URL)
- Get campaign leads

**Conversation Operations**
- Retrieve message threads and replies

**Account Operations**
- List connected LinkedIn accounts

**List Operations**
- List lead lists
- Create new lead lists

**Analytics Operations**
- Get overall stats
- Get campaign-specific metrics

#### Architecture

```
00-system/skills/heyreach/
├── heyreach-master/        # Shared resources
│   ├── scripts/            # Python scripts
│   │   ├── heyreach_client.py
│   │   ├── check_heyreach_config.py
│   │   ├── list_campaigns.py
│   │   ├── add_leads.py
│   │   └── ... (12 scripts total)
│   └── references/
│       ├── setup-guide.md
│       ├── api-reference.md
│       └── error-handling.md
├── heyreach-connect/       # User entry point
│   └── SKILL.md            # Meta-skill with routing
└── SKILL.md                # Main skill definition
```

#### Usage

Say any of these to trigger HeyReach operations:
- "heyreach" / "linkedin outreach" / "linkedin campaigns"
- "list campaigns" / "show campaigns"
- "add leads to campaign"
- "campaign stats" / "campaign metrics"
- "linkedin accounts"

#### Setup

1. Log into HeyReach at https://app.heyreach.io
2. Go to Settings → API
3. Copy API key to `.env` as `HEYREACH_API_KEY`

---

## v0.15.0 - Slack Integration (2025-12-19)

### New Integration: Slack

Complete Slack integration with OAuth 2.0 user authentication.

#### Features

**Messaging Operations**
- Send, update, delete messages
- Schedule messages
- Channel history retrieval

**Channel Operations**
- List channels (public/private)
- Get channel info
- Create channels

**User Operations**
- List workspace users
- Get user details

**Search Operations**
- Search messages
- Search files

**File Operations**
- Upload files to channels
- List files

#### Architecture

```
00-system/skills/slack/
├── slack-master/           # Shared resources
│   ├── scripts/            # Python scripts
│   │   ├── setup_slack.py
│   │   ├── check_slack_config.py
│   │   ├── send_message.py
│   │   ├── list_channels.py
│   │   ├── channel_history.py
│   │   ├── list_users.py
│   │   ├── search_messages.py
│   │   └── ... (more)
│   └── references/
│       ├── setup-guide.md
│       ├── api-reference.md
│       └── error-handling.md
├── slack-connect/          # User entry point
│   └── SKILL.md            # Meta-skill with routing
└── SKILL.md                # Main skill definition
```

#### Usage

Say any of these to trigger Slack operations:
- "slack" / "connect slack" / "send slack message"
- "send message to #channel"
- "list slack channels" / "slack users"
- "search slack for 'keyword'"
- "get channel history"

#### Setup

1. Create Slack App at api.slack.com/apps
2. Add User Token Scopes (channels:read, chat:write, users:read, etc.)
3. Add redirect URL: `https://localhost:8765/callback`
4. Run OAuth setup to authorize and save token

---

## v0.14.2 - Core Skill Triggering Improvements (2025-12-18)

### Skill Priority Ordering

Skills now return in priority order for better AI attention:

1. **CORE skills first**: create-project, execute-project, create-skill
2. **LEARNING skills second**: setup-memory, learn-projects, learn-skills, etc.
3. **All other skills** follow

### Renamed setup-goals → setup-memory

The `setup-goals` skill is now `setup-memory` to better reflect its purpose of configuring Nexus memory with user context.

### Orchestrator Improvements

- Added **semantic intent matching** guidance for core skills
- Clearer decision flow: check existing projects → new work → automation → skill match
- Simplified learning skill suggestion triggers using `stats.pending_onboarding`

### Simplified Skill Descriptions

Core skill descriptions now focus on intent signals rather than keyword lists:
- `create-project`: "Load when user wants to START something new with a deliverable"
- `execute-project`: "Load when user references ANY project by name, ID, or number"
- `create-skill`: "Load when user wants to automate repeating work"

### Other Changes

- Removed `_file_name` from loader output (redundant with `_file_path`)
- Updated all references from setup-goals to setup-memory across config, state, templates, and orchestrator

---

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
│   └── references/
└── hubspot-connect/         # User entry point
```

#### Setup

1. Create HubSpot Private App (Settings → Integrations → Private Apps)
2. Add required scopes (crm.objects.contacts.read/write, etc.)
3. Copy access token to `.env` as `HUBSPOT_ACCESS_TOKEN`

---

## v0.9.0 - Nexus Sync & Dynamic Integrations (2025-12-11)

### Nexus Sync Feature

Update system files from upstream while protecting user data.

- New `update-nexus` skill - say "update nexus" to pull latest changes
- `--check-update` and `--sync` commands in nexus-loader.py
- Automatic backup before sync (saved to `.sync-backup/`)
- Menu shows update notice when updates are available

### Protected Paths (Never Touched by Sync)

- `01-memory/` - Your goals, config, learnings
- `02-projects/` - Your projects
- `03-skills/` - Your custom skills
- `04-workspace/` - Your files
- `.env`, `.claude/` - Your secrets and settings

### Dynamic Integrations Menu

- Integrations detected from .env configuration
- Dynamic menu rendering based on configured integrations

---

## v0.8.0 - Quick Start Mode (2025-12-10)

### Optional Onboarding

- System now works immediately without setup
- Smart defaults for immediate use
- Onboarding skills are optional, not required
- Learning tracker in user-config.yaml

---

## v0.7.0 - Initial Release

Core features:
- Memory persistence system
- Project management
- Skill creation and execution
- Notion and Airtable integrations
- Learning skills for onboarding
