# Core Infrastructure

**Location**: `00-system/core/`

---

## Purpose

The `core/` folder contains fundamental infrastructure files that are essential to Nexus-v3 system operation. These files are loaded every session and provide the foundation for all system functionality.

---

## Files

### orchestrator.md
**Purpose**: AI decision logic and routing system

**What it does**:
- Defines initialization sequence
- Provides smart routing logic (skills → projects → init state → general work)
- Specifies context loading rules
- Handles state detection and menu generation

**Loaded**: Every session (via CLAUDE.md)

---

### nexus-loader.py
**Purpose**: Context loading automation script

**What it does**:
- Loads core files (system-map, memory-map, project-map, goals, workspace-map)
- Scans projects and extracts YAML metadata
- Scans skills and extracts YAML metadata
- Generates structured JSON output with files + metadata + stats
- Monitors token budget

**Usage**:
```bash
# Startup (loads everything)
python 00-system/core/nexus-loader.py --startup

# Load specific project
python 00-system/core/nexus-loader.py --project {project-id}

# Load specific skill
python 00-system/core/nexus-loader.py --skill {skill-name}
```

**Loaded**: Every session initialization

---

## Why "core/"?

These files are:
- **Fundamental** - System cannot function without them
- **Always loaded** - Present in every session
- **Infrastructure** - Not user-modifiable
- **Cross-cutting** - Affect all other system components

By grouping them in `core/`, we clearly separate infrastructure from:
- `/skills/` - Reusable workflows (user-facing)
- `/documentation/` - Reference materials
- `/blueprints/` - Templates and patterns

---

## Related Documentation

- [orchestrator.md](orchestrator.md) - Complete orchestration logic
- [system-map.md](../system-map.md) - System overview
- [CLAUDE.md](../../CLAUDE.md) - Initialization entry point

---

**Last Updated**: 2025-11-03
