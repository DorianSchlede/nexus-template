# Nexus Loader Architecture

> Auto-generated documentation for the nexus package.

## Package Structure

```
00-system/core/
├── nexus-loader.py          # CLI wrapper (thin, ~230 lines)
└── nexus/                   # Core package
    ├── __init__.py          # Public API exports, version
    ├── config.py            # Constants, paths, limits
    ├── models.py            # Data classes & enums
    ├── utils.py             # Helper functions
    ├── loaders.py           # Scan/load builds, skills, memory
    ├── state.py             # State detection & instruction building
    ├── service.py           # NexusService (main API)
    ├── sync.py              # Git sync operations
    └── templates/           # Smart default templates
```

---

## Module Dependency Flow

```mermaid
graph TD
    CLI["nexus-loader.py<br/>(CLI Entry Point)"]

    subgraph "nexus package"
        SVC["service.py<br/>NexusService"]
        LDR["loaders.py<br/>scan/load functions"]
        STA["state.py<br/>detect state, build instructions"]
        SYN["sync.py<br/>git operations"]
        CFG["config.py<br/>constants"]
        MDL["models.py<br/>dataclasses"]
        UTL["utils.py<br/>helpers"]
    end

    CLI --> SVC
    SVC --> LDR
    SVC --> STA
    SVC --> SYN
    SVC --> UTL
    LDR --> CFG
    LDR --> UTL
    STA --> CFG
    STA --> MDL
    SYN --> CFG
    UTL --> CFG
```

---

## CLI Commands

```mermaid
flowchart TB
    subgraph "CLI Commands"
        START["--startup"]
        RESUME["--resume"]
        SKILL["--skill NAME"]
        PROJ["--build ID"]
        LIST_P["--list-builds"]
        LIST_S["--list-skills"]
        META["--metadata"]
        SYNC["--sync"]
        CHECK["--check-update"]
    end

    subgraph "NexusService Methods"
        S_STARTUP["startup()"]
        S_SKILL["load_skill()"]
        S_PROJ["load_build()"]
        S_LIST_P["list_builds()"]
        S_LIST_S["list_skills()"]
        S_META["load_metadata()"]
        S_SYNC["sync()"]
        S_CHECK["check_updates()"]
    end

    subgraph "Output Handling"
        OUT_SMALL["Print JSON<br/>(< 30K chars)"]
        OUT_CACHE["Cache to file<br/>(> 30K chars)<br/>Print pointer"]
        OUT_LARGE["Print full JSON<br/>(skill/build)"]
    end

    START --> S_STARTUP --> OUT_CACHE
    RESUME --> S_STARTUP --> OUT_CACHE
    SKILL --> S_SKILL --> OUT_LARGE
    PROJ --> S_PROJ --> OUT_LARGE
    LIST_P --> S_LIST_P --> OUT_SMALL
    LIST_S --> S_LIST_S --> OUT_SMALL
    META --> S_META --> OUT_SMALL
    SYNC --> S_SYNC --> OUT_SMALL
    CHECK --> S_CHECK --> OUT_SMALL
```

### Command Reference

| Command | Method | Description |
|---------|--------|-------------|
| `--startup` | `startup()` | Load full context: memory, metadata, instructions |
| `--resume` | `startup(resume_mode=True)` | Resume after context summary |
| `--skill NAME` | `load_skill()` | File tree + SKILL.md (slim mode) |
| `--build ID` | `load_build()` | Build metadata + file paths |
| `--list-builds` | `list_builds()` | Scan all builds |
| `--list-skills` | `list_skills()` | Scan all skills |
| `--metadata` | `load_metadata()` | Builds + skills only |
| `--check-update` | `check_updates()` | Check upstream version |
| `--sync` | `sync()` | Sync from upstream |

---

## Startup Flow

The main entry point for session initialization.

```mermaid
sequenceDiagram
    participant CLI as nexus-loader.py
    participant SVC as NexusService
    participant LDR as loaders.py
    participant STA as state.py
    participant SYN as sync.py
    participant FS as File System
    participant CACHE as Cache File

    CLI->>SVC: startup(include_metadata, resume_mode, check_updates)

    Note over SVC: Step 1: Load mandatory maps
    SVC->>FS: Check orchestrator.md, system-map.md
    FS-->>SVC: files_to_embed[]

    Note over SVC: Step 2: Check memory files
    SVC->>FS: Check goals.md, user-config.yaml, memory-map.md
    FS-->>SVC: files_exist{}

    Note over SVC: Step 3: Scan builds & skills
    SVC->>LDR: scan_builds()
    LDR->>FS: Glob 02-builds/*/overview.md
    FS-->>LDR: build files
    LDR-->>SVC: builds[]

    SVC->>LDR: scan_skills()
    LDR->>FS: Glob 03-skills/**/SKILL.md
    FS-->>LDR: skill files
    LDR-->>SVC: skills[]

    Note over SVC: Step 4: First-time setup
    alt No goals.md
        SVC->>LDR: create_smart_defaults()
        LDR->>FS: Create template files
    end

    Note over SVC: Step 5: Detect system state
    SVC->>STA: detect_system_state()
    STA-->>SVC: SystemState enum

    Note over SVC: Step 6: Check updates
    alt check_updates=true
        SVC->>SYN: check_for_updates()
        SYN->>FS: git fetch upstream
        SYN-->>SVC: update_info{}
    end

    Note over SVC: Step 7-8: Build stats & instructions
    SVC->>STA: build_stats()
    STA-->>SVC: stats{}
    SVC->>STA: build_instructions()
    STA-->>SVC: instructions{}

    Note over SVC: Step 9: Embed memory content
    SVC->>FS: Read all files_to_embed
    FS-->>SVC: memory_content{}

    SVC-->>CLI: result{}

    Note over CLI: Output handling
    alt output > 30K chars
        CLI->>CACHE: Write full JSON
        CLI->>CLI: Print cache pointer
    else output <= 30K chars
        CLI->>CLI: Print full JSON
    end
```

### Startup Result Structure

```json
{
  "loaded_at": "2025-12-31T...",
  "bundle": "startup",
  ">>> EXECUTE_FIRST <<<": { /* instructions */ },
  "system_state": "operational_with_active_builds",
  "memory_content": {
    "orchestrator.md": "...",
    "goals.md": "...",
    "user-config.yaml": "..."
  },
  "metadata": {
    "builds": [...],
    "skills": [...]
  },
  "stats": {
    "total_builds": 14,
    "active_builds": 3,
    "total_skills": 100,
    "goals_personalized": true,
    "display_hints": [...]
  },
  ">>> EXECUTE_AFTER_READING <<<": { /* same instructions (attention sandwich) */ }
}
```

---

## Skill Loading (Slim Mode)

Skills always load in slim mode: file tree + SKILL.md only.

```mermaid
flowchart TB
    subgraph "Input"
        CMD["--skill airtable-master"]
    end

    subgraph "Search Locations"
        LOC1["03-skills/"]
        LOC2["00-system/skills/"]
    end

    subgraph "Search Strategy"
        DIRECT["Direct path<br/>skills/{name}/SKILL.md"]
        RECUR["Recursive glob<br/>skills/**/{name}/SKILL.md"]
    end

    subgraph "load_skill_slim()"
        BUILD["Build file tree with sizes"]
        READ_SKILL["Read SKILL.md content"]
        LIST_FILES["List references/scripts/assets<br/>(paths only, no content)"]
    end

    subgraph "Output"
        OUT["JSON with:<br/>- file_tree<br/>- SKILL.md content<br/>- available_files{}<br/>- hint: Use Read tool"]
    end

    CMD --> LOC1 --> DIRECT
    CMD --> LOC2 --> DIRECT
    DIRECT -->|not found| RECUR
    DIRECT -->|found| BUILD
    RECUR -->|found| BUILD
    BUILD --> READ_SKILL --> LIST_FILES --> OUT
```

### Skill Output Structure

```json
{
  "loaded_at": "2025-12-31T...",
  "bundle": "skill_slim",
  "skill_name": "airtable-master",
  "skill_path": "C:/.../03-skills/airtable/airtable-master",
  "file_tree": "airtable-master/\n├── references/\n│   ├── api-reference.md (7,755 bytes)\n...",
  "SKILL.md": "---\nname: airtable-master\n...",
  "available_files": {
    "references": ["references/api-reference.md", ...],
    "scripts": ["scripts/query_records.py", ...],
    "assets": []
  },
  "hint": "Use Read tool on any file path to load its content"
}
```

---

## System State Detection

```mermaid
stateDiagram-v2
    [*] --> CheckResumeMode

    CheckResumeMode --> RESUME: resume_mode=true
    CheckResumeMode --> CheckGoals: resume_mode=false

    CheckGoals --> FIRST_TIME_WITH_DEFAULTS: No goals.md
    CheckGoals --> CheckTemplate: goals.md exists

    CheckTemplate --> FIRST_TIME_WITH_DEFAULTS: is_template=true
    CheckTemplate --> CheckActiveBuilds: is_template=false

    CheckActiveBuilds --> OPERATIONAL_WITH_ACTIVE_BUILDS: Has IN_PROGRESS builds
    CheckActiveBuilds --> OPERATIONAL: No active builds

    RESUME: Resume Mode<br/>Load context immediately
    FIRST_TIME_WITH_DEFAULTS: First Time Setup<br/>Suggest onboarding
    OPERATIONAL_WITH_ACTIVE_BUILDS: Active Builds<br/>Highlight work in progress
    OPERATIONAL: Ready to Work<br/>Show menu
```

### State → Instructions Mapping

| State | Action | Message |
|-------|--------|---------|
| `FIRST_TIME_WITH_DEFAULTS` | `display_menu` | Welcome! Quick Start Mode active |
| `OPERATIONAL_WITH_ACTIVE_BUILDS` | `display_menu` | Welcome back! N active builds |
| `OPERATIONAL` | `display_menu` | System ready |
| `RESUME` | `EXECUTE_MANDATORY_LOADING_SEQUENCE` | Load build context first |

---

## Cache Strategy

Only startup/resume commands use caching (when output > 30K chars).

```mermaid
flowchart TB
    subgraph "Output Size Check"
        SIZE{output > 30K chars?}
        IS_STARTUP{is --startup or --resume?}
    end

    subgraph "Cache Path"
        SESSION{--session provided?}
        CACHE_DEFAULT["00-system/.cache/context_startup.json"]
        CACHE_SESSION["00-system/.cache/context_startup_{hash}.json"]
    end

    subgraph "Output Strategy"
        PRINT_FULL["Print full JSON"]
        PRINT_POINTER["Print slim pointer + cache_path"]
    end

    SIZE -->|yes| IS_STARTUP
    SIZE -->|no| PRINT_FULL

    IS_STARTUP -->|yes| SESSION
    IS_STARTUP -->|no| PRINT_FULL

    SESSION -->|yes| CACHE_SESSION --> PRINT_POINTER
    SESSION -->|no| CACHE_DEFAULT --> PRINT_POINTER
```

### Multi-Session Support

When `--session SESSION_ID` is provided:
1. Hash the session ID: `md5(session_id)[:8]`
2. Cache to: `context_startup_{hash}.json`
3. Prevents collisions between parallel Claude instances

---

## Data Models

```mermaid
classDiagram
    class SystemState {
        <<enumeration>>
        FIRST_TIME_WITH_DEFAULTS
        GOALS_NOT_PERSONALIZED
        OPERATIONAL_WITH_ACTIVE_BUILDS
        OPERATIONAL
        RESUME
    }

    class BuildStatus {
        <<enumeration>>
        PLANNING
        IN_PROGRESS
        ON_HOLD
        COMPLETE
        ARCHIVED
    }

    class Build {
        +str id
        +str name
        +BuildStatus status
        +float progress
        +int tasks_total
        +int tasks_completed
        +str current_task
        +to_dict()
    }

    class Skill {
        +str name
        +str description
        +str _file_path
        +to_dict()
    }

    class Instructions {
        +str action
        +str execution_mode
        +str message
        +str reason
        +list workflow
        +to_dict()
    }

    Build --> BuildStatus
```

---

## Configuration Constants

### Token & Output Limits

| Constant | Value | Purpose |
|----------|-------|---------|
| `CHARS_PER_TOKEN` | 4 | Rough token estimation |
| `CONTEXT_WINDOW` | 200,000 | Claude's context limit |
| `BASH_OUTPUT_LIMIT` | 30,000 | Claude Code bash truncation |
| `METADATA_BUDGET_WARNING` | 7,000 | Warn if metadata tokens exceed |

### Cache Configuration

| Constant | Value |
|----------|-------|
| `CACHE_DIR` | `00-system/.cache` |
| `CACHE_STARTUP_FILE` | `context_startup.json` |

### Mandatory Maps

Always loaded at startup (order matters):
1. `00-system/core/orchestrator.md` - AI behavior rules
2. `00-system/system-map.md` - Navigation structure

### Integration Environment Variables

| Integration | Required Env Var |
|-------------|------------------|
| airtable | `AIRTABLE_API_KEY` |
| notion | `NOTION_API_KEY` |
| beam | `BEAM_API_KEY` |
| hubspot | `HUBSPOT_ACCESS_TOKEN` |

### Sync Configuration

**Sync paths** (updated from upstream):
- `00-system/`
- `CLAUDE.md`
- `README.md`

**Protected paths** (never touched):
- `01-memory/`
- `02-builds/`
- `03-skills/`
- `04-workspace/`
- `.env`
- `.claude/`

---

## Public API

### NexusService

```python
from nexus import NexusService

service = NexusService(base_path=".")

# Session startup
result = service.startup(
    include_metadata=True,
    resume_mode=False,
    check_updates=True
)

# Load specific build
build = service.load_build("14-advanced-hook-system")

# Load skill (slim mode - file tree + SKILL.md only)
skill = service.load_skill("airtable-master")

# List all builds/skills
builds = service.list_builds(full=False)
skills = service.list_skills(full=False)

# Metadata only
metadata = service.load_metadata()

# Git sync
update_info = service.check_updates()
sync_result = service.sync(dry_run=False, force=False)
```

### Backward Compatibility

The CLI wrapper exports these functions for direct import:

```python
from nexus_loader import (
    load_startup,
    load_build,
    load_skill,
    load_metadata,
    scan_builds,
    scan_skills,
    check_for_updates,
    sync_from_upstream,
)
```

---

## Key Design Decisions

### 1. Slim Skill Loading (Default)

Skills always return file tree + SKILL.md only. References/scripts are listed as paths, not loaded.

**Why**: Prevents context bloat. AI uses `Read` tool to load specific files as needed.

### 2. Attention Sandwich

Instructions appear twice in startup result:
- `>>> EXECUTE_FIRST <<<` (at start)
- `>>> EXECUTE_AFTER_READING <<<` (at end)

**Why**: Exploits LLM primacy and recency effects for better instruction following.

### 3. Cache Only for Startup

Only `--startup` and `--resume` use cache redirection. Other commands print full JSON.

**Why**: Startup output (~84KB) exceeds bash limits. Skills/builds need full content.

### 4. Progressive Disclosure

Metadata scanning returns minimal fields by default. Use `--full` for complete data.

**Why**: Reduces token usage for routing decisions.

### 5. Single Source of Truth

Task progress (`tasks_total`, `tasks_completed`, `progress`) is calculated from actual `steps.md` checkboxes, not YAML metadata.

**Why**: Prevents drift between metadata and reality.

---

## Version

Current: `0.15.1` (see `__init__.py`)
