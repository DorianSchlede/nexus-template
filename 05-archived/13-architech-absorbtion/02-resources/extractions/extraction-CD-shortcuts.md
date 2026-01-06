# Pattern C+D: Dynamic Shortcut System - Extraction

**Extracted**: 2026-01-01
**Source System**: Architech (mutagent-obsidian)
**Target System**: Nexus (strategy-nexus)
**Status**: COMPLETE - Ready to spawn Project 14

---

## Source Files

| File | Path | Lines | Purpose |
|------|------|-------|---------|
| **Registry Builder** | `mutagent-obsidian/architech/01-system/08-automation/hooks/shortcut_system/build_shortcut_registry.py` | 1162 | Builds dynamic shortcut registry from file frontmatter |
| **Shortcut Resolver** | `mutagent-obsidian/architech/01-system/08-automation/hooks/shortcut_system/shortcut_resolver.py` | 828 | Resolves shortcuts to file paths with 2-tier cascade |

**Key Classes**:
- `ShortcutRegistryBuilder` - Scans files, extracts frontmatter, builds registry
- `ShortcutResolver` - Resolves `~shortcuts` to paths, loads content, handles dependencies

---

## What It Does

The Dynamic Shortcut System provides **on-demand, self-documenting navigation** across a complex multi-layer file system. Instead of maintaining static YAML files that list every entity path, it:

1. **Scans files at runtime** looking for YAML frontmatter with `description` field
2. **Auto-derives metadata** (layer, category, entity-type) from file paths
3. **Generates shortcuts** like `~meta-architect`, `~create-agent`, `~entity:task`
4. **Filters by context** (mode, agent scope, layer, domain) for progressive disclosure
5. **Resolves on-demand** when AI needs to load a file

**Key Insight**: The system is **self-documenting** - adding a new file with proper frontmatter automatically makes it discoverable. No registry maintenance required.

---

## How It Works

### 1. Registry Builder Architecture

The `ShortcutRegistryBuilder` class is initialized with filter parameters and builds a registry in 4 steps:

```python
class ShortcutRegistryBuilder:
    def __init__(
        self,
        root_path: str = "context-store",
        max_depth: int = 2,
        layer_filter: str = None,      # 'meta', 'system', 'domains', 'cross-domain'
        domain_filter: str = None,     # 'strategy', 'product', 'software', etc.
        agent_filter: str = None,      # 'meta-architect', 'backend-engineer', etc.
        mode: str = "plan",            # 'plan', 'exec', 'discover'
        max_desc: int = None,          # Truncate descriptions
        entity_types: List[str] = None # Override mode filtering
    ):
        self.MODE_ENTITY_TYPES = {
            'plan': {
                'definition', 'agent', 'skill', 'task', 'workflow',
                'blueprint', 'rule', 'checklist', 'navigation',
                'documentation', 'mental-model'
            },
            'exec': {
                # Execution mode: Only executables
                'agent', 'skill', 'task', 'workflow'
            },
            'discover': {
                # Discovery mode: Only learning resources
                'definition', 'rule', 'navigation',
                'documentation', 'mental-model'
            }
        }
```

**Build Process**:

```python
def build_registry(self) -> Dict:
    # Step 0: Load entity metadata (folder_number -> folder_name mapping)
    self.load_entity_metadata()

    # Step 1: Scan files and collect data
    self._scan_directory(architech_path, current_depth=0)

    # Step 2: Detect collisions and generate smart shortcuts
    registry = self._generate_registry_with_aliases()

    # Step 3: Add metadata
    registry["_metadata"] = {...}

    return registry
```

---

### 2. Layer Derivation Logic (`_derive_layer`)

The layer is **auto-derived from the file path** - no frontmatter field needed:

```python
def _derive_layer(self, file_path: Path) -> str:
    """Auto-derive layer from file path."""
    parts = file_path.parts

    for i, part in enumerate(parts):
        if part == "architech":
            if i + 1 < len(parts):
                layer_folder = parts[i + 1]

                if layer_folder == "00-meta":
                    return "meta"
                elif layer_folder == "01-system":
                    return "system"
                elif layer_folder == "02-domains":
                    # Extract domain: 01-strategy -> domain-strategy
                    if i + 2 < len(parts):
                        domain_folder = parts[i + 2]
                        domain_name = domain_folder.split("-", 1)[1]
                        return f"domain-{domain_name}"
                elif layer_folder == "03-cross-domain":
                    # Extract system: 10-project-management -> cross-domain-project-management
                    if i + 2 < len(parts):
                        system_folder = parts[i + 2]
                        system_name = system_folder.split("-", 1)[1]
                        return f"cross-domain-{system_name}"

    return "unknown"
```

**Nexus Simplification**: Nexus has only 4 top-level folders (00-system, 01-memory, 02-projects, 03-skills), so layer derivation is simpler.

---

### 3. Category Derivation Logic (`_derive_category`)

The category (entity type) is derived by **walking up the path tree** looking for known folder patterns:

```python
def _derive_category(self, file_path: Path) -> str:
    """Auto-derive category from parent folders using entity metadata."""

    # Legacy map for backwards compatibility
    category_map = {
        "agents": "agent",
        "workflows": "workflow",
        "tasks": "task",
        "skills": "skill",
        "rules": "rule",
        # ... etc
    }

    # Search up the path tree (max 5 levels)
    current_path = file_path.parent
    for _ in range(5):
        folder_name = current_path.name

        # Try entity metadata first (from 00-definitions/entity-types/)
        for entity_meta in self.entity_metadata.values():
            if folder_name.endswith(entity_meta['folder_name']):
                return entity_meta['type']

        # Try legacy map
        folder_name_only = folder_name.split("-", 1)[1] if "-" in folder_name else folder_name
        if folder_name_only in category_map:
            return category_map[folder_name_only]

        current_path = current_path.parent

    return "unknown"
```

**Key Pattern**: Folders are numbered (`01-agents`, `03-tasks`) so stripping the prefix reveals the entity type.

---

### 4. Mode System (Progressive Disclosure)

The mode system filters which entity types are loaded based on work phase:

| Mode | Purpose | Entity Types Loaded | Context Reduction |
|------|---------|---------------------|-------------------|
| `plan` | Design, architect, validate | ALL 11 types | ~40-60% (via agent scope) |
| `exec` | Execute work, run tasks | agent, skill, task, workflow (4 types) | ~60% reduction |
| `discover` | Learn, explore, understand | definition, rule, navigation, docs, mental-model (5 types) | ~60% reduction |

**Implementation**:

```python
def _mode_allows_entity_type(self, entity_type: str) -> bool:
    """Check if current mode allows this entity type."""

    # If explicit entity types filter, use it instead of mode
    if self.entity_types_filter:
        return entity_type in self.entity_types_filter

    allowed_types = self.MODE_ENTITY_TYPES.get(self.mode, set())
    return entity_type in allowed_types
```

**Usage Examples**:
```bash
# Planning mode (default) - loads everything for design work
python build_shortcut_registry.py --mode plan

# Execution mode - loads only executables for implementation
python build_shortcut_registry.py --mode exec

# Discovery mode - loads only learning resources
python build_shortcut_registry.py --mode discover
```

---

### 5. Agent Scoping Mechanism

Agent scoping enables **fine-grained access control** - each file can specify which agents can access it:

**Frontmatter Field**:
```yaml
---
name: create-api-endpoint
description: Create a new REST API endpoint
agent_scope: [backend-engineer, api-developer]  # Only these agents can access
---
```

**Resolution Logic**:

```python
def _agent_in_scope(self, agent_scope: Optional[List[str]]) -> bool:
    """Check if current agent filter matches agent_scope from frontmatter."""

    if not self.agent_filter:
        return True  # No agent filter = include everything (orchestrator mode)

    if not agent_scope:
        return True  # No agent_scope = available to all agents (default)

    # Check if current agent is in the scope list
    return self.agent_filter in agent_scope
```

**Key Behaviors**:
- **No `--agent` flag**: Load ALL files (orchestrator mode)
- **`--agent backend-engineer`**: Load only files where `agent_scope` includes `backend-engineer` OR has no `agent_scope` field
- **Empty `agent_scope: []`**: Available to all agents (same as no field)

**Agent Layer Access** (auto-derived from agent's file location):

```python
def _derive_agent_layers(self) -> Optional[List[str]]:
    """Auto-derive allowed layers from agent's file location."""

    # Find agent file
    agent_path = self._find_agent_file(self.agent_filter)
    agent_layer = self._derive_layer(agent_path)

    # Apply layer access rules
    if agent_layer == 'meta':
        return ['meta', 'system']
    elif agent_layer == 'system':
        return ['system']
    elif agent_layer.startswith('domain-'):
        return ['system', agent_layer]
    elif agent_layer.startswith('cross-domain-'):
        return ['system', agent_layer]

    return None
```

---

### 6. Shortcut Resolver - 2-Tier Cascade Architecture

The resolver uses a **2-tier cascade** for progressive loading:

```
Tier 1: Base Registry (loaded at session start)
  |
  +-- All 00-meta/ shortcuts
  +-- All 01-system/ shortcuts

Tier 2: Domain Registries (loaded on-demand)
  |
  +-- Only loaded when domain shortcut detected
  +-- Cached for session duration
```

**Implementation**:

```python
class ShortcutResolver:
    def __init__(self, root_path: str = "context-store"):
        self.cache = {}           # Path resolution cache
        self.loaded_domains = {}  # Domain registry cache

        # Load base registry at initialization
        self.registry = self._load_base_registry()

    def resolve(self, shortcut: str, feature: Optional[str] = None) -> str:
        """Resolve shortcut with on-demand domain cascade."""

        if not shortcut.startswith("~"):
            return shortcut

        # Check for domain trigger (NEW CASCADE LOGIC)
        domain = self._detect_domain_trigger(shortcut)
        if domain and domain not in self.loaded_domains:
            self._load_domain_registry(domain)

        # Check cache
        cache_key = f"{shortcut}:{self.repo_context}:{feature}"
        if cache_key in self.cache:
            return self.cache[cache_key]

        # Resolve from registry
        resolved_path = self._resolve_shortcut(shortcut, feature)

        # Cache the result
        self.cache[cache_key] = resolved_path
        return resolved_path
```

**Domain Trigger Detection**:

```python
def _detect_domain_trigger(self, shortcut: str) -> Optional[str]:
    """Detect if shortcut requires domain cascade."""

    if ":" not in shortcut:
        return None

    parts = shortcut.lstrip("~").split(":")

    # Pattern 1: domain- prefix
    if parts[0].startswith("domain-"):
        return parts[0].replace("domain-", "")

    # Pattern 2: Known domain names
    KNOWN_DOMAINS = [
        "strategy", "product", "software",
        "finance", "marketing", "operations", "sales"
    ]

    if parts[0] in KNOWN_DOMAINS:
        return parts[0]

    return None
```

---

### 7. Dependency Loading Mechanism

The resolver can load a file **with all its dependencies** from frontmatter:

**Frontmatter Format**:
```yaml
---
name: create-agent
dependencies: [~entity:agent, ~git-workflow, ~naming-conventions]
---
```

**Implementation**:

```python
def load_with_dependencies(
    self,
    shortcut: str,
    feature: Optional[str] = None,
    warn_large_files: bool = True,
    max_depth: int = 3,
    _visited: Optional[set] = None
) -> Tuple[str, Optional[str], List[Dict]]:
    """Load a shortcut AND its dependencies from frontmatter."""

    if _visited is None:
        _visited = set()

    # Prevent circular dependencies
    if shortcut in _visited:
        return shortcut, None, []
    _visited.add(shortcut)

    # Load primary file
    resolved_path, content = self.load_content(shortcut, feature, warn_large_files)

    if content is None:
        return resolved_path, None, []

    # Extract dependencies from frontmatter
    dependencies = self.extract_dependencies(content)

    if not dependencies or max_depth <= 0:
        return resolved_path, content, []

    # Recursively load each dependency
    dep_docs = []
    for dep_shortcut in dependencies:
        if dep_shortcut in _visited:
            continue

        dep_path, dep_content, nested_deps = self.load_with_dependencies(
            dep_shortcut, feature, warn_large_files,
            max_depth=max_depth - 1, _visited=_visited
        )

        if dep_content:
            dep_docs.append({
                "shortcut": dep_shortcut,
                "path": dep_path,
                "content": dep_content,
                "content_length": len(dep_content)
            })
            dep_docs.extend(nested_deps)

    return resolved_path, content, dep_docs
```

**Dependency Extraction** (supports two YAML formats):

```python
def extract_dependencies(self, content: str) -> List[str]:
    """Extract dependencies from YAML frontmatter."""

    # Format 1: Inline array
    # dependencies: [~a, ~b, ~c]

    # Format 2: YAML list
    # dependencies:
    #   - ~shortcut1
    #   - ~shortcut2

    # Returns list of shortcuts starting with ~
```

**CLI Usage**:
```bash
# Load file with all dependencies (up to 3 levels deep)
python shortcut_resolver.py ~create-agent --with-deps --content

# Show dependencies without loading content
python shortcut_resolver.py ~create-agent --deps-only

# Custom depth limit
python shortcut_resolver.py ~create-agent --with-deps --max-depth 5
```

---

### 8. Session Caching Strategy

The resolver implements **multi-level caching** for performance:

```python
class ShortcutResolver:
    def __init__(self):
        self.cache = {}           # Path resolution cache (per session)
        self.loaded_domains = {}  # Domain registry cache (per session)
        self.registry = {}        # Base registry (loaded once at init)
```

**Cache Key Format**: `{shortcut}:{repo_context}:{feature}`

**Cache Invalidation**: Caches are session-scoped - cleared when process exits.

---

## Output Formats

The builder supports multiple output formats:

| Format | Command | Purpose |
|--------|---------|---------|
| AI XML | `--format xml` (default) | Token-optimized for AI consumption |
| Compact XML | `--compact --format xml` | Ultra-minimal (`<s n="~name" d="desc"/>`) |
| AI JSON | `--format json` | AI-facing with d/w/e schema |
| Full JSON | `--full --format json` | Internal use with paths |
| Full XML | `--full --format xml` | Internal use with paths |

**AI XML Output Sample**:
```xml
<timestamp>2025-01-16T10:30:45.123456</timestamp>
<shortcuts>
  <entity-type name="agent">
    <shortcut>
      <name>~meta-architect</name>
      <description>Meta-level system observer, analyzer, and domain creator</description>
      <when>Framework analysis, domain creation, pattern extraction</when>
    </shortcut>
  </entity-type>
</shortcuts>
```

---

## Collision Handling

When two files have the same filename, the builder creates **qualified shortcuts**:

```
~filename                        # Short form (first wins)
~category:filename               # Medium form
~layer:category:filename         # Full form (guaranteed unique)
```

**Entity-Type Aliases**:
```
~backend-engineer                # Primary
~agent:backend-engineer          # Entity-type prefixed alias
```

**Entity Definition Aliases**:
```
~01-agent                        # Primary (from entity-types/)
~entity:agent                    # Semantic alias
```

---

## Nexus Design (Simplified ~200 Lines)

Nexus needs a **dramatically simplified** version:

### Core Differences from Architech

| Aspect | Architech | Nexus |
|--------|-----------|-------|
| Layers | 4 (meta/system/domains/cross-domain) | 4 (00-system/01-memory/02-projects/03-skills) |
| Entity Types | 12 (agent, task, workflow, etc.) | 3 (projects, skills, memory) |
| Domain Cascade | 7 domains, on-demand loading | Not needed (no domains) |
| Agent Scoping | Per-file agent_scope field | Not needed (single orchestrator) |
| Mode System | plan/exec/discover | Maybe keep `plan`/`exec` only |
| Output Formats | 6 (JSON/XML + variations) | 2 (JSON + compact) |

### Nexus Shortcut Patterns

```
~project:ontologies-research     # Project shortcut
~skill:research-pipeline         # Skill shortcut
~memory:airtable-bases           # Memory shortcut
~system:orchestrator             # System shortcut
```

### Simplified Implementation

```python
#!/usr/bin/env python3
"""
Nexus Dynamic Shortcut Resolver - Simplified (~200 lines)
Version: 1.0.0
"""

import json
from pathlib import Path
from typing import Dict, Optional, List
import frontmatter

class NexusResolver:
    """Simplified shortcut resolver for Nexus."""

    # Nexus folder structure
    LAYERS = {
        '00-system': 'system',
        '01-memory': 'memory',
        '02-projects': 'project',
        '03-skills': 'skill'
    }

    def __init__(self, root_path: str = "."):
        self.root_path = Path(root_path)
        self.cache = {}
        self.registry = self._build_registry()

    def _build_registry(self) -> Dict:
        """Build shortcut registry from frontmatter."""
        registry = {}

        for folder, layer in self.LAYERS.items():
            folder_path = self.root_path / folder
            if not folder_path.exists():
                continue

            for md_file in folder_path.rglob("*.md"):
                shortcut = self._process_file(md_file, layer)
                if shortcut:
                    registry.update(shortcut)

        return registry

    def _process_file(self, file_path: Path, layer: str) -> Optional[Dict]:
        """Process a file and return shortcut entry."""
        try:
            post = frontmatter.load(file_path)

            if 'description' not in post.metadata:
                return None

            # Derive shortcut from filename
            name = file_path.stem
            shortcut = f"~{layer}:{name}"

            relative_path = str(file_path.relative_to(self.root_path))

            return {
                shortcut: {
                    'path': relative_path,
                    'description': post.metadata['description'],
                    'when': post.metadata.get('when', '')
                }
            }
        except Exception:
            return None

    def resolve(self, shortcut: str) -> str:
        """Resolve shortcut to file path."""
        if shortcut in self.cache:
            return self.cache[shortcut]

        if shortcut in self.registry:
            path = self.registry[shortcut]['path']
            self.cache[shortcut] = path
            return path

        return shortcut  # Return as-is if not found

    def load_content(self, shortcut: str) -> tuple[str, Optional[str]]:
        """Resolve and load file content."""
        path = self.resolve(shortcut)
        full_path = self.root_path / path

        if not full_path.exists():
            return path, None

        content = full_path.read_text(encoding='utf-8')
        return path, content

    def to_json(self) -> str:
        """Export registry as JSON."""
        return json.dumps(self.registry, indent=2)

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Nexus Shortcut Resolver")
    parser.add_argument("shortcut", nargs='?', help="Shortcut to resolve")
    parser.add_argument("--list", action="store_true", help="List all shortcuts")
    parser.add_argument("--content", action="store_true", help="Load content")
    parser.add_argument("--root", default=".", help="Root directory")

    args = parser.parse_args()
    resolver = NexusResolver(args.root)

    if args.list:
        print(resolver.to_json())
    elif args.shortcut:
        if args.content:
            path, content = resolver.load_content(args.shortcut)
            print(f"# PATH: {path}")
            if content:
                print(content)
        else:
            print(resolver.resolve(args.shortcut))

if __name__ == "__main__":
    main()
```

---

## Implementation Checklist

### Phase 1: Core Resolver (Project 14)

- [ ] Create `00-system/scripts/nexus_resolver.py` (~200 lines)
- [ ] Implement `_build_registry()` with Nexus folder structure
- [ ] Implement `resolve()` with simple caching
- [ ] Implement `load_content()` with UTF-8 handling
- [ ] Add CLI interface (`--list`, `--content`, `--root`)
- [ ] Test with existing Nexus structure

### Phase 2: Integration with nexus-loader

- [ ] Add `--shortcut` flag to nexus-loader.py
- [ ] Call resolver from nexus-loader for `~` prefixed requests
- [ ] Add shortcut resolution to context_startup.json builder
- [ ] Document shortcut patterns in CLAUDE.md

### Phase 3: Mode System (Optional)

- [ ] Add `--mode plan|exec` flag (simplified from Architech's 3 modes)
- [ ] Filter by folder type based on mode:
  - `plan`: All folders
  - `exec`: Only 02-projects and 03-skills

### Phase 4: Dependency Loading (Optional)

- [ ] Extract `dependencies:` from frontmatter
- [ ] Implement `load_with_dependencies()`
- [ ] Add `--with-deps` CLI flag

---

## Test Plan

### Unit Tests

| Test Case | Input | Expected Output |
|-----------|-------|-----------------|
| Resolve project | `~project:ontologies-research` | `02-projects/02-ontologies-research/...` |
| Resolve skill | `~skill:research-pipeline` | `03-skills/research-pipeline/...` |
| Resolve unknown | `~unknown:foo` | `~unknown:foo` (unchanged) |
| Load content | `~project:test --content` | Path + file content |
| List all | `--list` | JSON registry |

### Integration Tests

1. **Startup Integration**: Verify resolver works with nexus-loader.py
2. **Context Startup**: Verify shortcuts appear in context_startup.json
3. **Large File Warning**: Verify warnings for files >100KB
4. **UTF-8 Encoding**: Verify non-ASCII characters handled correctly
5. **Missing Files**: Verify graceful handling of deleted files

### Edge Cases

- File without frontmatter (should be skipped)
- File with empty description (should be skipped)
- Circular dependencies (should detect and break)
- Very deep nesting (should respect max_depth)

---

## Key Insights for Nexus

1. **Self-Documenting is Critical**: The main value is that adding a file with frontmatter auto-registers it. No static YAML maintenance.

2. **Mode System is Valuable**: Even a simple plan/exec split helps reduce context for different tasks.

3. **Dependency Loading is Powerful**: Loading a skill with its dependencies automatically bundles related context.

4. **Collision Handling Can Be Simpler**: Nexus has fewer files, so simple `~layer:name` patterns suffice.

5. **Caching Matters**: Session-scoped caching prevents re-scanning for repeated lookups.

6. **Output Format**: JSON is sufficient for Nexus - no need for XML variants.

---

## Open Questions for Project 14

1. Should Nexus shortcuts use `~` prefix (like Architech) or `@` (different namespace)?
2. Should mode system be included in v1 or deferred?
3. Should dependency loading be included in v1 or deferred?
4. How should resolver integrate with existing nexus-loader.py?

---

## References

- **Source Files**: `mutagent-obsidian/architech/01-system/08-automation/hooks/shortcut_system/`
- **Entity Definitions**: `mutagent-obsidian/architech/01-system/00-definitions/entity-types/`
- **Meta-Architect Agent**: `mutagent-obsidian/architech/00-meta/01-agents/meta-architect/current/`
- **Project 13 Plan**: `strategy-nexus/02-projects/13-architech-absorbtion/01-planning/`

---

**Extraction Complete** - Ready to spawn Project 14: Nexus Shortcut System
