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
python 00-system/core/nexus-loader.py --startup

# Load build metadata + file paths
python 00-system/core/nexus-loader.py --build {id}

# Load skill content
python 00-system/core/nexus-loader.py --skill {name}

# List all builds/skills
python 00-system/core/nexus-loader.py --list-builds
python 00-system/core/nexus-loader.py --list-skills

# Check for updates
python 00-system/core/nexus-loader.py --check-update
```

---

## Related

- [orchestrator.md](orchestrator.md) - AI decision logic
- [system-map.md](../system-map.md) - System overview
- [CLAUDE.md](../../CLAUDE.md) - Entry point
