# Discovery

**Time**: DEEP DISCOVERY | **Purpose**: Full dependency analysis for CLI implementation

---

## Context

**Load First**: `01-planning/01-overview.md` - Understand project purpose
**Output To**: `01-planning/03-plan.md` - Dependencies section auto-populated from this file

---

## Dependencies

*Files, systems, APIs this project will touch*

### Files to Modify

| File | Purpose | Line Numbers | Risk |
|------|---------|--------------|------|
| `00-system/core/nexus-loader.py` | Add --discover argument | L101-121 (argparse), L128-152 (dispatch) | LOW |
| `00-system/core/nexus/loaders.py` | Wire discover functions | L1375-1478 (functions exist) | NONE |
| `00-system/core/orchestrator.md` | Update CLI reference | L244-254 (skill discovery section) | LOW |
| `00-system/system-map.md` | Update CLI commands | L82-95 (cli section) | LOW |
| `.claude/hooks/session_start.py` | Add timing instrumentation | L36 (START_TIME exists), L858-862 (perf check) | NONE - already instrumented |

### Files to Create

- `02-projects/29-.../04-outputs/SUMMARY.md` - Project 29 final summary

### External Systems

- None (all local Python code)

---

## Complete Code Analysis

### 1. nexus-loader.py (232 lines)

**Location**: `00-system/core/nexus-loader.py`

**Current Arguments** (L101-121):
```python
parser.add_argument('--startup', action='store_true')
parser.add_argument('--resume', action='store_true')
parser.add_argument('--skip-update-check', action='store_true')
parser.add_argument('--metadata', action='store_true')
parser.add_argument('--no-metadata', action='store_true')
parser.add_argument('--project', help='Load project by ID')
parser.add_argument('--part', type=int, default=0)
parser.add_argument('--skill', help='Load skill by name')
parser.add_argument('--list-projects', action='store_true')
parser.add_argument('--list-skills', action='store_true')
parser.add_argument('--full', action='store_true')
parser.add_argument('--base-path', default=str(detected_nexus_root))
parser.add_argument('--show-tokens', action='store_true')
parser.add_argument('--check-update', action='store_true')
parser.add_argument('--sync', action='store_true')
parser.add_argument('--dry-run', action='store_true')
parser.add_argument('--force', action='store_true')
parser.add_argument('--session', help='Session ID')
```

**GAP**: Missing `--discover CATEGORY` argument

**Dispatch Logic** (L128-152):
```python
if args.check_update:
    result = service.check_updates()
elif args.sync:
    result = service.sync(...)
elif args.startup or args.resume:
    result = service.startup(...)
elif args.metadata:
    result = service.load_metadata()
elif args.project:
    result = service.load_project(...)
elif args.skill:
    result = service.load_skill(...)
elif args.list_projects:
    result = service.list_projects(...)
elif args.list_skills:
    result = service.list_skills(...)
else:
    parser.print_help()
```

**Implementation Pattern**: All arguments use `NexusService` methods or direct function calls.

---

### 2. loaders.py - Discovery Functions (Already Implemented)

**Location**: `00-system/core/nexus/loaders.py`

#### discover_skills_in_category() (L1375-1478)

```python
def discover_skills_in_category(category: str, base_path: str = ".") -> Dict[str, Any]:
    """
    Discover all skills in an integration category.

    Enables `load-skill {category} --help` pattern.

    Returns:
        {
            "category": "langfuse",
            "skills": [...],  # List of skill metadata dicts
            "count": 71,
            "formatted": "Langfuse Operations (71 skills):\n..."
        }
    """
```

**Search Paths**:
- `03-skills/{category}/` (user skills)
- `00-system/skills/{category}/` (system skills)

**Output Format** (formatted field):
```
Langfuse Operations (71 skills):

[Connector]
  - langfuse-connect: Setup tracing connection

[Operations]
  - langfuse-get-trace: Get trace details
  - langfuse-list-traces: List all traces
  ...

To load a skill: read langfuse/{skill-name}/SKILL.md
```

#### list_integration_categories() (L1480-1518)

```python
def list_integration_categories(base_path: str = ".") -> List[Dict[str, Any]]:
    """
    List all available integration categories.

    Returns:
        [
            {"name": "langfuse", "path": "...", "skill_count": 71},
            {"name": "slack", "path": "...", "skill_count": 15},
            ...
        ]
    """
```

#### build_skills_xml_compact() (L675-843)

This function generates XML with CLI hints:
```xml
<integration-skills location="03-skills/*-connect/">
  <category name="langfuse" operations="71">
    <connector name="langfuse-connect">Setup tracing connection</connector>
    <cli>load-skill langfuse --help</cli>
  </category>
</integration-skills>
```

**KEY INSIGHT**: The hint says `load-skill langfuse --help` but there's no CLI handler for this command.

---

### 3. session_start.py - Performance Instrumentation (Already Exists)

**Location**: `.claude/hooks/session_start.py` (954 lines)

**Timing Already Implemented**:
```python
# Line 36
START_TIME = time.perf_counter()

# Line 858-862
elapsed_ms = (time.perf_counter() - START_TIME) * 1000
if elapsed_ms > 200:
    logging.warning(f"SessionStart hook exceeded 200ms budget: {elapsed_ms:.2f}ms")
else:
    logging.info(f"SessionStart hook completed in {elapsed_ms:.2f}ms")
```

**Cache Files** (L869-911):
- `00-system/.cache/session_start_output.log` - Summary log
- `00-system/.cache/session_start_context.xml` - Full XML dump
- `00-system/.cache/session_start_tokens.txt` - Token analysis

**FINDING**: Hook performance is already measured and logged. No changes needed.

---

### 4. orchestrator.md - CLI References

**Location**: `00-system/core/orchestrator.md`

**Skill Discovery Section** (L244-254):
```markdown
## Skill Discovery

When you need to find a skill that's not immediately in the catalog:

### Pattern 1: Use load-skill CLI

```bash
# See all skills in category
load-skill langfuse --help

# Load specific skill
load-skill langfuse get-trace
```
```

**ISSUE**: The CLI hints reference `load-skill` which doesn't exist as a command.

---

### 5. system-map.md - CLI Commands

**Location**: `00-system/system-map.md` (98 lines)

**CLI Section** (L82-95):
```markdown
<section id="cli">
## CLI Commands

```bash
# Load project context
python 00-system/core/nexus-loader.py --project {ID}

# Load skill
python 00-system/core/nexus-loader.py --skill {name}

# Discover skills in category
load-skill {category} --help
```
</section>
```

**ISSUE**: Same problem - `load-skill` doesn't exist.

---

### 6. add-integration Skill

**Location**: `00-system/skills/system/add-integration/SKILL.md` (622 lines)

**Status**: Full implementation exists but uses `create-project` pattern (references old name).

**Has**:
- Complete scaffold_integration.py script
- Templates for all integration components
- Comprehensive workflow

**References**:
- `references/integration-architecture.md`
- `references/mcp-introduction.md`
- `references/mcp-setup-guide.md`

---

### 7. MECE State Templates

**Location**: `.claude/hooks/templates/`

**6 Templates** (already implemented):
1. `startup_first_run.md` - First time setup
2. `startup_onboarding_incomplete.md` - Pending onboarding items
3. `startup_active_projects.md` - Has active projects
4. `startup_workspace_modified.md` - Workspace needs sync
5. `startup_fresh_workspace.md` - Ready for first project
6. `startup_system_ready.md` - Fully configured

**Called by**: `build_next_action_instruction()` in loaders.py (L1235-1269)

---

## Existing Patterns to Reuse

### Pattern 1: NexusService Method Pattern

All nexus-loader.py operations use `NexusService`:
```python
service = NexusService(args.base_path)
result = service.some_method(...)
print(json.dumps(result, indent=2))
```

**For --discover**: Could add `NexusService.discover_category()` wrapper or call loaders directly.

### Pattern 2: Direct Loaders Import

Some operations import directly from loaders:
```python
from nexus.loaders import scan_projects
result = scan_projects(base_path, minimal=True)
```

**For --discover**: Can import directly:
```python
from nexus.loaders import discover_skills_in_category, list_integration_categories
```

---

## Risk Analysis

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Hook performance >200ms | LOW | Low | Already instrumented - just read logs |
| Breaking existing args | LOW | High | Test all existing args after changes |
| Category not found | MEDIUM | Low | discover_skills_in_category returns helpful message |
| Import path issues | LOW | Medium | Functions already exported from loaders.py |

---

## Open Questions

- [x] Keep `load-skill` or use `--discover`? → **Use `--discover` for consistency with nexus-loader.py pattern**
- [x] Add `--list-categories` flag? → **Yes, useful for discovery**
- [x] Should errors return JSON or text? → **Follow existing pattern: JSON with indent=2**
- [x] Is performance instrumentation needed? → **No, already exists in session_start.py**
- [x] Is add-integration skill deprecated? → **No, it exists and is comprehensive**

---

## Implementation Summary

### What Needs to Be Done

1. **Add to nexus-loader.py**:
   ```python
   parser.add_argument('--discover', help='Discover skills in category (e.g., langfuse)')
   parser.add_argument('--list-categories', action='store_true', help='List all integration categories')
   ```

2. **Add dispatch logic**:
   ```python
   elif args.discover:
       from nexus.loaders import discover_skills_in_category
       result = discover_skills_in_category(args.discover, args.base_path)
   elif args.list_categories:
       from nexus.loaders import list_integration_categories
       result = list_integration_categories(args.base_path)
   ```

3. **Update documentation**:
   - orchestrator.md: Change `load-skill langfuse --help` to `python nexus-loader.py --discover langfuse`
   - system-map.md: Same update

### What's Already Done

- `discover_skills_in_category()` - Fully implemented ✅
- `list_integration_categories()` - Fully implemented ✅
- `build_skills_xml_compact()` - Uses CLI hints ✅
- Performance instrumentation - Already in session_start.py ✅
- MECE state templates - All 6 implemented ✅

---

## File Reference Summary

| File | Status | Lines | What's There |
|------|--------|-------|--------------|
| nexus-loader.py | Needs --discover | 232 | All other CLI args |
| loaders.py | Complete | 1518 | discover functions at L1375-1518 |
| session_start.py | Complete | 954 | Timing at L36, L858-862 |
| orchestrator.md | Needs update | ~300 | CLI hint at L250 |
| system-map.md | Needs update | 98 | CLI hint at L93 |

---

*Deep discovery complete. Ready for implementation.*
