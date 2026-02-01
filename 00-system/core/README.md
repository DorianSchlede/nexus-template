# Core Infrastructure

**Location**: `00-system/core/`

---

## Purpose

Contains fundamental infrastructure for Nexus system operation. Loaded every session.

---

## Structure

```
core/
├── nexus-loader.py      # CLI entry point (thin wrapper)
├── nexus/               # Python package
│   ├── __init__.py      # Public API
│   ├── config.py        # Constants and paths
│   ├── models.py        # Dataclasses (Build, Skill, State)
│   ├── loaders.py       # File scanning and loading
│   ├── state.py         # State detection and instructions
│   ├── service.py       # NexusService orchestration
│   ├── sync.py          # Git sync and updates
│   ├── utils.py         # Helpers (YAML, tokens, etc.)
│   └── templates/       # Default file templates
├── orchestrator.md      # AI routing logic
└── test_nexus_loader.py # Test suite
```

---

## Usage

```bash
# Startup (loads memory, detects state, returns instructions)
nexus-load --startup

# Load build metadata + file paths
nexus-load --build {id}

# Load skill content
nexus-load --skill {name}

# List all builds/skills
nexus-load --list-builds
nexus-load --list-skills

# Check for updates
nexus-load --check-update
```

---

## Related

- [orchestrator.md](orchestrator.md) - AI decision logic
- [system-map.md](../system-map.md) - System overview
- [CLAUDE.md](../../CLAUDE.md) - Entry point
