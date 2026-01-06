---
name: hook-system-reference
description: Comprehensive technical reference for the Architech Hook System - shortcut resolution, context loading, agent activation, observability, and safety mechanisms
when: Understanding hook system internals, debugging shortcut resolution, implementing new hooks, extending observability
type: documentation
version: 1.0.0
created: 2025-12-31
updated: 2025-12-31
author: "Meta Architect | Multiagent Analysis"
audience: ai
tags: [hooks, shortcuts, automation, observability, security]
---

# Architech Hook System Reference

## Executive Summary

The Architech Hook System is a **multi-layered, event-driven architecture** providing:

1. **Shortcut Resolution** - Dynamic `~shortcut` to file path mapping
2. **Context Loading** - Progressive disclosure of behavioral flags
3. **Agent Activation** - Alias-based agent persona switching
4. **Observability Pipeline** - Real-time executable detection & streaming
5. **Safety Guards** - Dangerous command blocking (rm -rf, .env access)

**Token Optimization**: 60-85% context reduction via progressive disclosure
**Performance**: <10ms cached resolution, non-blocking observability

---

## Table of Contents

1. [Architecture Overview](#1-architecture-overview)
2. [Shortcut Registry Builder](#2-shortcut-registry-builder)
3. [Shortcut Resolver](#3-shortcut-resolver)
4. [Context Loader](#4-context-loader)
5. [Agent Activation](#5-agent-activation)
6. [Pre-Tool-Use Hook](#6-pre-tool-use-hook)
7. [Utility Modules](#7-utility-modules)
8. [Mode System & Filtering](#8-mode-system--filtering)
9. [CLI Reference](#9-cli-reference)
10. [Troubleshooting](#10-troubleshooting)

---

## 1. Architecture Overview

### 1.1 System Topology

```
.claude/hooks/                              # Claude SDK Integration Layer
├── pre_tool_use.py                         # Tool call interception
├── utils/
│   ├── http.py                             # Fire-and-forget HTTP
│   ├── registry.py                         # Shortcut cache & lookup
│   └── constants.py                        # Paths, configuration

architech/01-system/08-automation/hooks/    # Core Hook System
├── shortcut_system/
│   ├── build_shortcut_registry.py          # Registry builder (1162 lines)
│   ├── shortcut_resolver.py                # Resolution engine (827 lines)
│   └── context_loader.py                   # Behavioral injection (302 lines)
├── agent_system/
│   └── activate_agent.py                   # Agent activation (263 lines)
└── platform_compat.py                      # Cross-platform UTF-8 (227 lines)
```

### 1.2 Data Flow

```
User Input: "~meta-architect"
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│                     PRE_TOOL_USE.PY                         │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │ Safety Check    │──│ Exec Detection  │──│ Stream Event│ │
│  │ rm -rf/.env     │  │ Registry Lookup │  │ Fire&Forget │ │
│  └─────────────────┘  └─────────────────┘  └─────────────┘ │
│           │                                                 │
│  Exit 2 = BLOCK        Exit 0 = ALLOW                      │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                   SHORTCUT_RESOLVER.PY                      │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │ Root Detection  │──│ Registry Build  │──│ Content Load│ │
│  │ 4 Strategies    │  │ 2-Tier Cascade  │  │ + Deps      │ │
│  └─────────────────┘  └─────────────────┘  └─────────────┘ │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    CONTEXT_LOADER.PY                        │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │ Flag Extraction │──│ Context Inject  │──│ Format AI   │ │
│  │ interactive/cog │  │ ULTRATHINK etc  │  │ Ready Output│ │
│  └─────────────────┘  └─────────────────┘  └─────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### 1.3 Key Design Principles

| Principle | Implementation |
|-----------|----------------|
| **Progressive Disclosure** | Mode system loads only relevant entity types |
| **Single Source of Truth** | Frontmatter metadata is THE source |
| **Fire-and-Forget** | Observability never blocks execution |
| **Defense in Depth** | Multiple safety layers (rm -rf, .env) |
| **Platform Compatibility** | Windows UTF-8 auto-fix on import |

---

## 2. Shortcut Registry Builder

**File**: `architech/01-system/08-automation/hooks/shortcut_system/build_shortcut_registry.py`
**Lines**: 1162
**Version**: 5.2.0-agent-scoping

### 2.1 Core Class: `ShortcutRegistryBuilder`

```python
class ShortcutRegistryBuilder:
    def __init__(
        self,
        root_path: str = "context-store",
        max_depth: int = 2,
        layer_filter: str = None,      # meta|system|domains|cross-domain
        domain_filter: str = None,     # strategy|product|software|...
        agent_filter: str = None,      # agent-id for scope filtering
        mode: str = "plan",            # plan|exec|discover
        max_desc: int = None,          # Truncate descriptions
        entity_types: List[str] = None # Override mode filtering
    )
```

### 2.2 Scanning Logic

#### Directory Scanning (`_scan_directory`)
**Lines**: 205-224

```python
def _scan_directory(self, directory: Path, current_depth: int):
    if current_depth > self.max_depth:  # Default: 5 levels
        return

    for item in directory.iterdir():
        # File types: .md, .yaml, .py
        if item.is_file() and item.suffix in [".md", ".yaml", ".py"]:
            self._process_file(item)
        # Exclusions: dotfiles, underscore, evolution folders
        elif item.is_dir() and not item.name.startswith((".", "_")) and item.name != "evolution":
            self._scan_directory(item, current_depth + 1)
```

**Why Max Depth = 5?**
Entity definitions require 5 levels:
```
context-store/ (0) → architech/ (1) → 01-system/ (2) →
00-definitions/ (3) → entity-types/ (4) → 01-agent.md (5)
```

#### Root Path Resolution (`_resolve_root_path`)
**Lines**: 93-132

| Strategy | Method | Fallback |
|----------|--------|----------|
| 1 | Try provided path as-is | → Strategy 2 |
| 2 | Check current working directory | → Strategy 3 |
| 3 | Search up 5 parent directories | → Strategy 4 |
| 4 | Return original (will error later) | Terminal |

### 2.3 Frontmatter Extraction

#### Required & Optional Fields (`_process_file`)
**Lines**: 226-291

```python
# REQUIRED (line 233)
if 'description' not in post.metadata:
    return  # Skip files without description

# OPTIONAL
when = post.metadata.get('when', '')
agent_scope = post.metadata.get('agent_scope', None)
activation_aliases = post.metadata.get('activation_aliases', [])

# BEHAVIORAL FLAGS (lines 268-272)
flag_fields = ['interactive', 'cognitive_mode', 'progressive', 'reasoning']
for flag in flag_fields:
    if flag in post.metadata:
        behavioral_flags[flag] = post.metadata[flag]
```

#### Supported Frontmatter Schema

```yaml
---
name: entity-name
description: Required - What this entity does
when: Optional - When to use this entity
agent_scope: [agent1, agent2]  # Optional - Restrict to specific agents
activation_aliases: [alias1, alias2]  # Optional - Natural language triggers
interactive: true  # Optional - Require user engagement
cognitive_mode: ULTRATHINK  # Optional - Thinking pattern
progressive: true  # Optional - Incremental loading
reasoning: "Explanation"  # Optional - Why interactive
---
```

### 2.4 Five-Layer Filtering System

**Lines**: 245-265 (application order in `_process_file`)

#### Filter 1: Layer Matching (`_layer_matches_filter`)
**Lines**: 348-395

```python
# THREE-TIER PRIORITY:

# Priority 1: Agent-based (auto-derived from agent location)
if self.agent_filter:
    self.agent_allowed_layers = self._derive_agent_layers()
    # meta agent → ['meta', 'system']
    # system agent → ['system']
    # domain agent → ['system', 'domain-{name}']

# Priority 2: Explicit --layer flag
if self.layer_filter:
    if self.layer_filter == 'meta':
        return layer == 'meta'
    elif self.layer_filter == 'domains':
        return layer.startswith('domain-')

# Priority 3: No filter - allow all
return True
```

#### Filter 2: Domain Matching (`_domain_matches_filter`)
**Lines**: 397-421

Only applies when layer is `domain-*`:
```python
# --domain strategy → matches only 'domain-strategy'
domain_name = layer.replace('domain-', '', 1)
return domain_name == self.domain_filter
```

#### Filter 3: Agent Scope (`_agent_in_scope`)
**Lines**: 423-449

```python
# Frontmatter: agent_scope: [software-architect, backend-engineer]

if not self.agent_filter:
    return True  # No filter = orchestrator mode (include all)

if not agent_scope:
    return True  # No agent_scope = available to all

return self.agent_filter in agent_scope  # Check membership
```

#### Filter 4: Mode-Based Entity Types (`_mode_allows_entity_type`)
**Lines**: 451-473

```python
MODE_ENTITY_TYPES = {
    'plan': {  # 11 types - Full design context
        'definition', 'agent', 'skill', 'task', 'workflow',
        'blueprint', 'rule', 'checklist', 'navigation',
        'documentation', 'mental-model'
    },
    'exec': {  # 4 types - Pure execution
        'agent', 'skill', 'task', 'workflow'
    },
    'discover': {  # 5 types - Learning resources
        'definition', 'rule', 'navigation',
        'documentation', 'mental-model'
    }
}

# --entity-types override takes precedence over mode
if self.entity_types_filter:
    return entity_type in self.entity_types_filter

return entity_type in self.MODE_ENTITY_TYPES.get(self.mode, set())
```

#### Filter 5: Archive Exclusion
**Line**: 264

```python
if '99-archive' in file_path.parts or category == 'archive':
    return  # Always excluded, no exceptions
```

### 2.5 Collision Handling & Aliasing

#### Collision Detection (`_generate_registry_with_aliases`)
**Lines**: 561-651

**Two-Branch Strategy:**

```python
for filename, file_entries in self.filename_map.items():
    if len(file_entries) == 1:
        # UNIQUE: Simple shortcut ~filename
        shortcut = f"~{filename}"

    else:
        # COLLISION: Layer-prefixed qualification
        for entry in file_entries:
            primary_shortcut = f"~{layer}:{category}:{filename}"
```

**Aliasing Hierarchy:**

| Level | Format | Example |
|-------|--------|---------|
| Short | `~filename` | `~roadmap` |
| Medium | `~category:filename` | `~task:roadmap` |
| Full | `~layer:category:filename` | `~meta:definition:roadmap` |

**Entity Semantic Aliases:**
```python
# ~01-agent → also registers as ~entity:agent
entity_name = filename.split('-', 1)[1]  # "01-agent" → "agent"
entity_alias = f"~entity:{entity_name}"
registry[entity_alias] = shortcut  # Reference (not copy)
```

### 2.6 Output Formats

#### Token Optimization Comparison

| Format | Method | Content | Reduction |
|--------|--------|---------|-----------|
| Full JSON | `to_json()` | paths + flags + aliases | Baseline |
| Full XML | `to_xml()` | paths + flags + grouped | ~0% |
| AI JSON | `to_ai_json()` | d+w+e only | ~50% |
| AI XML | `to_ai_xml()` | d+w+e grouped | ~45% |
| Compact JSON | `to_compact_json()` | d+w+e no spaces | ~55% |
| **Compact XML** | `to_compact_xml()` | single-letter attrs | **70-80%** |

#### Compact XML Structure (`_generate_compact_xml`)
**Lines**: 787-848

```xml
<r>
  <l>r=registry s=shortcut n=name d=description</l>
  <u>Load: shortcut_resolver.py {n} --content</u>
  <agent>
    <s n="~meta-architect" d="Framework analyzer..."/>
    <s n="~trace-analyst" d="Trace aggregation..."/>
  </agent>
  <task>
    <s n="~run-tests" d="Execute test suite..."/>
  </task>
</r>
```

**Why 70-80% Reduction:**
- Single-letter attributes: `n=""` vs `<name></name>`
- Omits aliases (redundant with grouping)
- Omits `<when>` (covered by description)
- No indentation/whitespace

---

## 3. Shortcut Resolver

**File**: `architech/01-system/08-automation/hooks/shortcut_system/shortcut_resolver.py`
**Lines**: 827
**Version**: 3.0.0-agent-centric-mode-system

### 3.1 Core Class: `ShortcutResolver`

```python
class ShortcutResolver:
    def __init__(
        self,
        root_path: str = "context-store",
        registry_path: str = None  # Deprecated
    ):
        self.root_path = self._resolve_root_path(root_path)
        self.repo_context = self._detect_repository()
        self.cache = {}  # Path resolution cache
        self.loaded_domains = {}  # Domain registry cache
        self.registry = self._load_base_registry()
```

### 3.2 Two-Tier Cascade Architecture

#### Base Registry (Session Startup)
**Lines**: 104-125

```python
def _load_base_registry(self) -> Dict:
    """
    Load base registry at session start (00-architech only, depth 5).
    """
    builder = ShortcutRegistryBuilder(root_path=self.root_path, max_depth=5)
    dynamic_registry = builder.build_registry()
    return self._convert_registry_format(dynamic_registry)
```

- **Scope**: `architech/` only (not domain-specific)
- **Depth**: 5 levels (required for entity definitions)
- **Timing**: At `__init__` (session start)

#### Domain Registry (On-Demand)
**Lines**: 187-261

```python
def _load_domain_registry(self, domain: str):
    if domain in self.loaded_domains:
        return  # Already cached

    # Domain folder mapping
    domain_folder_map = {
        "strategy": "01-strategy",
        "product": "02-product",
        "software": "03-software",
        "finance": "04-finance",
        "marketing": "05-marketing",
        "operations": "06-operations",
        "sales": "07-sales"
    }

    # Merge into active registry
    static_shortcuts.update(domain_shortcuts)
    self.loaded_domains[domain] = converted  # Cache for session
```

#### Domain Detection (`_detect_domain_trigger`)
**Lines**: 155-185

```python
# Pattern 1: domain- prefix
# ~domain-sales:agent:closer → "sales"
if parts[0].startswith("domain-"):
    return parts[0].replace("domain-", "")

# Pattern 2: Known domain names
KNOWN_DOMAINS = ["strategy", "product", "software",
                 "finance", "marketing", "operations", "sales"]
# ~sales:workflow:pipeline → "sales"
if parts[0] in KNOWN_DOMAINS:
    return parts[0]
```

### 3.3 Resolution Pipeline

#### Main Resolution (`resolve`)
**Lines**: 289-323

```python
def resolve(self, shortcut: str, feature: Optional[str] = None) -> str:
    if not shortcut.startswith("~"):
        return shortcut  # Not a shortcut

    # Trigger domain cascade if needed
    domain = self._detect_domain_trigger(shortcut)
    if domain and domain not in self.loaded_domains:
        self._load_domain_registry(domain)

    # Check cache
    cache_key = f"{shortcut}:{self.repo_context}:{feature}"
    if cache_key in self.cache:
        return self.cache[cache_key]

    resolved_path = self._resolve_shortcut(shortcut, feature)
    self.cache[cache_key] = resolved_path
    return resolved_path
```

### 3.4 Dependency Loading

#### Dependency Extraction (`extract_dependencies`)
**Lines**: 419-483

**Supported Formats:**

```yaml
# Format 1: Inline array
dependencies: [~shortcut1, ~shortcut2]

# Format 2: YAML list
dependencies:
  - ~shortcut1
  - ~shortcut2
```

**Regex Patterns:**
```python
# Inline: dependencies: [~a, ~b, ~c]
inline_match = re.search(r'dependencies:\s*\[([^\]]+)\]', frontmatter)

# YAML list: dependencies:\n  - ~a\n  - ~b
list_match = re.search(r'dependencies:\s*\n((?:\s+-\s+[^\n]+\n?)+)', frontmatter)
```

#### Recursive Loading (`load_with_dependencies`)
**Lines**: 485-557

```python
def load_with_dependencies(
    self,
    shortcut: str,
    feature: Optional[str] = None,
    warn_large_files: bool = True,
    max_depth: int = 3,           # Max recursion depth
    _visited: Optional[set] = None # Circular prevention
) -> Tuple[str, Optional[str], List[Dict]]:

    # Circular dependency prevention
    if _visited is None:
        _visited = set()
    if shortcut in _visited:
        return shortcut, None, []
    _visited.add(shortcut)

    # Load primary file
    resolved_path, content = self.load_content(shortcut, feature)

    # Extract and load dependencies
    dependencies = self.extract_dependencies(content)
    for dep_shortcut in dependencies:
        if dep_shortcut in _visited:
            continue
        dep_path, dep_content, nested_deps = self.load_with_dependencies(
            dep_shortcut,
            max_depth=max_depth - 1,
            _visited=_visited
        )
        dep_docs.append({...})

    return resolved_path, content, dep_docs
```

### 3.5 Content Loading

#### File Loading (`load_content`)
**Lines**: 353-417

```python
def load_content(self, shortcut: str, feature: Optional[str] = None):
    resolved_path = self.resolve(shortcut, feature)

    # Path normalization
    file_path = Path(resolved_path)
    if not file_path.is_absolute():
        normalized = resolved_path.replace("\\", "/")
        if normalized.startswith("architech/"):
            file_path = Path(self.root_path) / resolved_path

    # Large file warnings
    file_size = file_path.stat().st_size
    if file_size > 100000:  # 100KB
        print("WARNING: Large file detected")
    if file_size > 1000000:  # 1MB
        print("VERY LARGE FILE warning")

    # Encoding: UTF-8 with latin-1 fallback
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except UnicodeDecodeError:
        with open(file_path, "r", encoding="latin-1") as f:
            content = f.read()

    return resolved_path, content
```

**Thresholds:**
- **100KB**: Warning about full file loading
- **1MB**: Critical warning ("VERY LARGE FILE")

---

## 4. Context Loader

**File**: `architech/01-system/08-automation/hooks/shortcut_system/context_loader.py`
**Lines**: 302
**Version**: 1.0.0

### 4.1 Core Class: `DynamicContextLoader`

```python
class DynamicContextLoader:
    def __init__(self, root_path: str = "context-store"):
        self.root_path = Path(root_path)
        self.registry_builder = ShortcutRegistryBuilder(root_path=root_path)
        self._registry_cache = None  # Lazy cache
```

### 4.2 Context Loading Flow

#### Main Loading (`load_context`)
**Lines**: 82-127

```python
def load_context(self, shortcut: str) -> Dict:
    # Step 1: Resolve shortcut to path
    file_path = self.resolve_path(shortcut)

    # Step 2: Load frontmatter
    with open(file_path, 'r', encoding='utf-8') as f:
        post = frontmatter.load(f)

    # Step 3: Extract metadata
    metadata = {
        "shortcut": shortcut,
        "path": str(file_path),
        "description": post.metadata.get('description', ''),
        "when": post.metadata.get('when', '')
    }

    # Step 4: Extract behavioral flags
    behavioral_flags = {}
    flag_fields = ['interactive', 'cognitive_mode', 'progressive', 'reasoning']
    for flag in flag_fields:
        if flag in post.metadata:
            behavioral_flags[flag] = post.metadata[flag]

    # Step 5: Build context injection
    behavioral_context = self._build_context_injection(shortcut, behavioral_flags)

    return {
        "metadata": metadata,
        "behavioral_flags": behavioral_flags,
        "behavioral_context": behavioral_context,
        "content": post.content
    }
```

### 4.3 Behavioral Flags

#### Flag Definitions

| Flag | Type | Effect | Example |
|------|------|--------|---------|
| `interactive` | bool | Force user engagement | `true` |
| `cognitive_mode` | string | Thinking pattern | `"ULTRATHINK"` |
| `progressive` | bool | Incremental loading | `true` |
| `reasoning` | string | Explanation for interactive | `"User guidance required"` |

#### Cognitive Mode Options
**Lines**: 160-167

```python
cognitive_guidance = {
    'ULTRATHINK': 'Deep analysis with step-by-step reasoning, show all thought processes',
    'systems-thinking': 'Holistic view, identify relationships, feedback loops, emergent properties',
    'first-principles': 'Break down to fundamental truths, build up from base assumptions',
    'analogous-reasoning': 'Draw parallels from other domains, find similar patterns',
    'lateral-thinking': 'Creative, non-linear approach, challenge assumptions'
}
```

### 4.4 Context Injection

#### Injection Builder (`_build_context_injection`)
**Lines**: 129-187

```python
def _build_context_injection(self, shortcut: str, flags: Dict) -> str:
    injections = []
    injections.append(f"=== DYNAMIC CONTEXT FOR {shortcut} ===\n")

    # Interactive Mode
    if flags.get('interactive'):
        reasoning = flags.get('reasoning', 'User guidance required')
        injections.append("⚠️  INTERACTIVE MODE REQUIRED")
        injections.append(f"   Reasoning: {reasoning}")
        injections.append("   - Engage user with questions before proceeding")
        injections.append("   - Validate each step before moving forward")
        injections.append("   - Seek confirmation on critical choices\n")

    # Cognitive Mode
    if flags.get('cognitive_mode'):
        mode = flags['cognitive_mode']
        guidance = cognitive_guidance.get(mode, 'Apply specialized thinking mode')
        injections.append(f"🧠 COGNITIVE MODE: {mode}")
        injections.append(f"   Guidance: {guidance}")
        injections.append("   - Apply this thinking pattern throughout\n")

    # Progressive Disclosure
    if flags.get('progressive'):
        injections.append("📊 PROGRESSIVE DISCLOSURE ENABLED")
        injections.append("   - Load context incrementally")
        injections.append("   - Fetch additional context only when needed\n")

    # Standard (no flags)
    if not flags:
        injections.append("ℹ️  Standard execution (no special behavioral flags)\n")

    return '\n'.join(injections)
```

#### Unicode Indicators

| Symbol | Flag | Meaning |
|--------|------|---------|
| ⚠️ | `interactive` | Warning - requires user attention |
| 🧠 | `cognitive_mode` | Brain - cognitive approach |
| 📊 | `progressive` | Chart - incremental loading |
| ℹ️ | (none) | Info - standard execution |

---

## 5. Agent Activation

**File**: `architech/01-system/08-automation/hooks/agent_system/activate_agent.py`
**Lines**: 263
**Version**: 1.0.0-simplified

### 5.1 Agent Discovery

#### Search Patterns (`find_agents`)
**Lines**: 29-56

```python
agent_paths = [
    root_path / "00-meta" / "01-agents",           # Meta layer
    root_path / "01-system" / "01-agents",         # System layer
    root_path / "02-domains" / "*" / "01-agents",  # Domain layers (glob)
    root_path / "03-cross-domain" / "*" / "01-agents",  # Cross-domain (glob)
]
```

#### Folder Convention
**Lines**: 68-72

```
agent-name/
├── current/              # Required subfolder
│   └── agent-name.md     # Agent definition file
└── evolution/            # Version history (optional)
```

Only `.md` files in `current/` are loaded.

### 5.2 Layer Derivation

#### Path-Based Derivation (`_derive_layer`)
**Lines**: 98-118

```python
def _derive_layer(file_path: Path, root_path: Path) -> str:
    rel_path = file_path.relative_to(root_path)
    parts = rel_path.parts

    if parts[0] == "00-meta":
        return "meta"
    elif parts[0] == "01-system":
        return "system"
    elif parts[0] == "02-domains":
        # "02-domains/03-product/..." → "domain-product"
        domain = parts[1].split("-", 1)[1]
        return f"domain-{domain}"
    elif parts[0] == "03-cross-domain":
        # "03-cross-domain/10-project-management/..." → "cross-domain-project-management"
        system = parts[1].split("-", 1)[1]
        return f"cross-domain-{system}"

    return "unknown"
```

### 5.3 Alias Resolution

#### Case-Insensitive Matching (`resolve_alias`)
**Lines**: 121-139

```python
def resolve_alias(alias: str, agents: List[Dict]) -> Optional[str]:
    alias_lower = alias.lower()

    for agent in agents:
        aliases = agent.get('aliases', [])  # From activation_aliases frontmatter
        if isinstance(aliases, str):
            aliases = [aliases]

        for a in aliases:
            if a.lower() == alias_lower:
                return agent['name']

    return None  # Triggers interactive menu if not found
```

### 5.4 Mode Derivation

#### Layer-Based Mode (`derive_mode`)
**Lines**: 142-148

```python
def derive_mode(layer: str) -> str:
    if layer in ['meta', 'system']:
        return 'plan'  # Design/orchestration work
    elif layer.startswith('domain-') or layer.startswith('cross-domain-'):
        return 'exec'  # Concrete execution work
    return 'plan'  # Default fallback
```

**Rationale:**
- **Meta/System agents**: Orchestrators needing full planning context
- **Domain agents**: Executors doing concrete implementation work

### 5.5 Interactive Menu

#### Agent Selection (`show_agent_menu`)
**Lines**: 151-208

```python
def show_agent_menu(agents: List[Dict]) -> str:
    # Group by layer
    by_layer = {}
    for agent in agents:
        layer = agent['layer']
        by_layer.setdefault(layer, []).append(agent)

    # Display with numbering scheme: i * 100 + j + 1
    for i, (layer, layer_agents) in enumerate(sorted(by_layer.items())):
        print(f"[{layer.upper()}]")
        for j, agent in enumerate(layer_agents):
            num = i * 100 + j + 1  # 101, 102, 201, 202...
            print(f"  {num}. {agent['name']}")

    # Default fallback
    print(f"  0. meta-architect (default)")
```

### 5.6 CLI Output Format

```bash
# Output: "agent_name|mode"
meta-architect|plan
product-manager|exec
developer|exec
```

**Pipe delimiter** enables easy shell parsing:
```bash
agent_output=$(python activate_agent.py "MA")
agent_name=$(echo "$agent_output" | cut -d'|' -f1)
mode=$(echo "$agent_output" | cut -d'|' -f2)
```

---

## 6. Pre-Tool-Use Hook

**File**: `.claude/hooks/pre_tool_use.py`
**Lines**: 327
**Purpose**: Claude SDK tool call interception for safety and observability

### 6.1 Executable Detection

#### Executable Types
**Line**: 32

```python
EXECUTABLE_TYPES = {"agent", "skill", "task", "workflow"}
```

Non-executables (excluded): definition, blueprint, rule, checklist, automation, documentation, mental-model

#### Detection Strategy (`detect_executable`)
**Lines**: 59-112

**For Bash Tool:**
```python
# Extract shortcut from shortcut_resolver.py command
match = re.search(r"shortcut_resolver\.py\s+(~[a-zA-Z0-9_:-]+)", command)
if match:
    shortcut = match.group(1)
    # Registry lookup (single source of truth)
    resolved = lookup_shortcut(shortcut)
    if resolved and resolved["type"] in EXECUTABLE_TYPES:
        return {"type", "id", "target", "shortcut", "detection_method": "bash"}
```

**For Read Tool:**
```python
# Path pattern matching (fallback)
detected = detect_from_path_patterns(file_path)
if detected:
    return {"type", "id", "target", "shortcut": None, "detection_method": "read"}
```

#### Path Patterns (`EXECUTABLE_PATH_PATTERNS`)
**Lines**: 35-56

```python
EXECUTABLE_PATH_PATTERNS = {
    "agent": [
        r"/01-agents/([^/]+)/",      # Nested: /01-agents/name/...
        r"/01-agents/([^/]+)\.md$",  # Direct: /01-agents/name.md
        r"\\01-agents\\([^\\]+)\\",  # Windows nested
        r"\\01-agents\\([^\\]+)\.md$",  # Windows direct
    ],
    "skill": [r"/02-skills/...", ...],
    "task": [r"/03-tasks/...", ...],
    "workflow": [r"/04-workflows/...", ...],
}
```

### 6.2 Safety Guards

#### rm -rf Detection (`is_dangerous_rm_command`)
**Lines**: 179-220

**Primary Patterns:**
```python
patterns = [
    r"\brm\s+.*-[a-z]*r[a-z]*f",      # rm -rf, rm -fr, rm -Rf, rm -arf
    r"\brm\s+.*-[a-z]*f[a-z]*r",      # rm -fr variants
    r"\brm\s+--recursive\s+--force",  # Long form (recursive first)
    r"\brm\s+--force\s+--recursive",  # Long form (force first)
    r"\brm\s+-r\s+.*-f",              # Separated: rm -r path -f
    r"\brm\s+-f\s+.*-r",              # Separated: rm -f path -r
]
```

**Dangerous Paths (with recursive flag):**
```python
dangerous_paths = [
    r"/",       # Root directory
    r"/\*",     # Root with wildcard
    r"~",       # Home directory
    r"~/",      # Home directory path
    r"\$HOME",  # Home environment variable
    r"\.\.",    # Parent directory references
    r"\*",      # Wildcards in rm -rf context
    r"\.",      # Current directory
    r"\.\s*$",  # Current directory at end
]
```

#### .env File Protection (`is_env_file_access`)
**Lines**: 223-251

**Protected Operations:**
```python
env_patterns = [
    r"\b\.env\b(?!\.sample)",         # .env (not .env.sample)
    r"cat\s+.*\.env\b(?!\.sample)",   # cat .env
    r"echo\s+.*>\s*\.env\b(?!\.sample)", # echo > .env
    r"touch\s+.*\.env\b(?!\.sample)", # touch .env
    r"cp\s+.*\.env\b(?!\.sample)",    # cp .env
    r"mv\s+.*\.env\b(?!\.sample)",    # mv .env
]
```

**Tools Checked:**
```python
["Read", "Edit", "MultiEdit", "Write", "Bash"]
```

**Allowed:** `.env.sample` (negative lookahead `(?!\.sample)`)

### 6.3 Observability Streaming

#### Event Payload (`stream_executable`)
**Lines**: 163-176

```python
payload = {
    "type": executable["type"],           # agent, skill, task, workflow
    "executable_id": executable["id"],    # meta-architect
    "target": target,                     # File path or shortcut
    "shortcut": executable.get("shortcut"), # ~meta-architect
    "detection_method": executable["detection_method"], # bash or read
    "timestamp": datetime.now().isoformat()
}
send_to_server(f"/api/v2/sessions/{session_id}/executable", payload)
```

### 6.4 Exit Codes

| Code | Meaning | Claude Behavior |
|------|---------|-----------------|
| `0` | Success/safe | Tool call proceeds |
| `2` | Security violation | **BLOCK** tool call, show error |

```python
# Block with error message
print("BLOCKED: Dangerous rm command detected", file=sys.stderr)
sys.exit(2)

# Allow execution
sys.exit(0)

# Graceful failure (allow on error)
except Exception:
    sys.exit(0)
```

---

## 7. Utility Modules

### 7.1 Platform Compatibility

**File**: `architech/01-system/08-automation/hooks/platform_compat.py`
**Lines**: 227

#### Windows Encoding Problem

Windows defaults to `cp1252` which cannot handle Unicode:
- Checkmarks: ✅ ❌ ✓ ✗
- Arrows: → ← ↑ ↓
- Emojis: 🚨 📝 🔍 💡

#### Fix Strategies (`fix_console_encoding`)
**Lines**: 35-131

| Strategy | Method | Status |
|----------|--------|--------|
| 1 | Check if already UTF-8 | `'already_utf8'` |
| 2 | `stream.reconfigure(encoding='utf-8')` | `'reconfigured'` |
| 3 | Wrap with `TextIOWrapper` | `'wrapped'` |
| 4 | Stream is None | `'skipped'` |
| 5 | All failed | `'failed'` |

#### Auto-Execute on Import
**Lines**: 175-184

```python
# This runs automatically when module is imported
_init_result = fix_console_encoding()
ensure_utf8_env()  # Set PYTHONIOENCODING for subprocesses
```

**Usage:**
```python
# Simply import - no function call needed
from platform_compat import *
```

### 7.2 HTTP Utilities

**File**: `.claude/hooks/utils/http.py`
**Lines**: 54

#### Fire-and-Forget Pattern (`send_to_server`)
**Lines**: 16-53

```python
SERVER_URL = os.environ.get("OBSERVABILITY_SERVER_URL", "http://localhost:7777")
TIMEOUT_SECONDS = 5

def send_to_server(endpoint: str, payload: dict) -> bool:
    """Fire-and-forget: Returns True/False, never raises, never blocks long."""
    try:
        url = f"{SERVER_URL}{endpoint}"
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "User-Agent": "Claude-Hook/1.0"
            },
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS) as response:
            return response.status in (200, 201)
    except Exception:
        return False  # Never raises
```

**Design Decisions:**
- **5 second timeout**: Prevents blocking if server down
- **Never raises**: Observability shouldn't cause failures
- **Fire-and-forget**: Return value often ignored

### 7.3 Registry Utilities

**File**: `.claude/hooks/utils/registry.py`
**Lines**: 174

#### Registry Caching (`load_registry`)
**Lines**: 40-72

```python
_registry_cache: Optional[Dict[str, Any]] = None
_registry_mtime: float = 0

def load_registry() -> Dict[str, Any]:
    global _registry_cache, _registry_mtime

    registry_path = get_registry_path()
    current_mtime = registry_path.stat().st_mtime

    # Check if we need to reload
    if _registry_cache is not None and current_mtime == _registry_mtime:
        return _registry_cache  # Return cached

    # Reload with PyYAML or fallback parser
    try:
        import yaml
        _registry_cache = yaml.safe_load(f)
    except ImportError:
        _registry_cache = _parse_yaml_simple(registry_path)

    _registry_mtime = current_mtime
    return _registry_cache
```

#### Entity Type Detection (`detect_type_from_path`)
**Lines**: 102-108

```python
ENTITY_TYPE_PATTERNS = {
    "agent": r"/01-agents/",
    "skill": r"/02-skills/",
    "task": r"/03-tasks/",
    "workflow": r"/04-workflows/",
}

def detect_type_from_path(path: str) -> Optional[str]:
    normalized = path.replace("\\", "/")  # Windows compatibility
    for entity_type, pattern in ENTITY_TYPE_PATTERNS.items():
        if re.search(pattern, normalized, re.IGNORECASE):
            return entity_type
    return None
```

#### ID Extraction (`extract_id_from_path`)
**Lines**: 111-132

```python
# Pattern 1: Folder-based /01-agents/name/...
match = re.search(r"/\d{2}-(?:agents|skills|tasks|workflows)/([^/]+)/", path)

# Pattern 2: File-based /01-agents/name.md
match = re.search(r"/\d{2}-(?:agents|skills|tasks|workflows)/([^/]+)\.md$", path)
```

---

## 8. Mode System & Filtering

### 8.1 Mode Definitions

```python
MODE_ENTITY_TYPES = {
    'plan': {
        'definition',      # What things ARE
        'agent',           # Who executes
        'skill',           # Prototyping containers
        'task',            # Atomic units
        'workflow',        # Multi-step coordination
        'blueprint',       # Template generators
        'rule',            # Behavioral constraints
        'checklist',       # Quality gates
        'navigation',      # Help menus
        'documentation',   # Guides
        'mental-model'     # Decision frameworks
    },
    'exec': {
        'agent',           # Who executes
        'skill',           # What they can prototype
        'task',            # What they can execute
        'workflow'         # How they coordinate
    },
    'discover': {
        'definition',      # What things are
        'rule',            # How things behave
        'navigation',      # Where to find things
        'documentation',   # How to use things
        'mental-model'     # How to think
    }
}
```

### 8.2 Context Reduction

| Mode | Entity Count | Reduction | Use Case |
|------|--------------|-----------|----------|
| **plan** | 11 types | ~40-60% | Design, architecture |
| **exec** | 4 types | ~65% | Implementation |
| **discover** | 5 types | ~55% | Learning, exploration |

**Combined with Agent Scoping:** 60-85% total reduction

### 8.3 Layer Access Rules

| Agent Location | Auto-Derived Layers | Mode |
|----------------|---------------------|------|
| `00-meta/` | `['meta', 'system']` | plan |
| `01-system/` | `['system']` | plan |
| `02-domains/01-strategy/` | `['system', 'domain-strategy']` | exec |
| `03-cross-domain/10-pm/` | `['system', 'cross-domain-project-management']` | exec |

---

## 9. CLI Reference

### 9.1 build_shortcut_registry.py

```bash
# Basic usage (AI-facing XML, plan mode)
python build_shortcut_registry.py

# Filter by layer
python build_shortcut_registry.py --layer meta
python build_shortcut_registry.py --layer system
python build_shortcut_registry.py --layer domains
python build_shortcut_registry.py --layer cross-domain

# Filter by domain
python build_shortcut_registry.py --domain strategy
python build_shortcut_registry.py --domain software
python build_shortcut_registry.py --domain marketing

# Filter by agent scope
python build_shortcut_registry.py --agent meta-architect
python build_shortcut_registry.py --agent backend-engineer

# Mode selection
python build_shortcut_registry.py --mode plan     # Default - all types
python build_shortcut_registry.py --mode exec     # Executables only
python build_shortcut_registry.py --mode discover # Learning resources

# Output formats
python build_shortcut_registry.py --format json
python build_shortcut_registry.py --format xml
python build_shortcut_registry.py --compact       # Token-optimized

# Full registry (with paths/flags)
python build_shortcut_registry.py --full

# Specific entity types (overrides mode)
python build_shortcut_registry.py --entity-types agent,task,skill

# Truncate descriptions
python build_shortcut_registry.py --max-desc 100

# Custom root path
python build_shortcut_registry.py --root /path/to/root

# Custom scan depth
python build_shortcut_registry.py --depth 5
```

### 9.2 shortcut_resolver.py

```bash
# Basic resolution (path only)
python shortcut_resolver.py ~meta-architect

# Load content
python shortcut_resolver.py ~meta-architect --content

# Content only (no path info)
python shortcut_resolver.py ~meta-architect --content-only

# Validate shortcut exists
python shortcut_resolver.py ~meta-architect --validate

# JSON output with metadata
python shortcut_resolver.py ~meta-architect --json

# Load with dependencies
python shortcut_resolver.py ~meta-architect --with-deps

# Show dependencies only
python shortcut_resolver.py ~meta-architect --deps-only

# Control dependency depth
python shortcut_resolver.py ~meta-architect --with-deps --max-depth 2

# Suppress warnings
python shortcut_resolver.py ~meta-architect --content --quiet

# Limit file size
python shortcut_resolver.py ~meta-architect --content --max-size 50000

# Custom root path
python shortcut_resolver.py ~meta-architect --root /path/to/root

# Feature-specific resolution
python shortcut_resolver.py ~meta-architect --feature my-feature
```

### 9.3 context_loader.py

```bash
# Load context (text format)
python context_loader.py ~analyze-framework

# JSON output
python context_loader.py ~analyze-framework --format json

# Show behavioral flags only
python context_loader.py ~analyze-framework --show-flags

# Custom root path
python context_loader.py ~analyze-framework --root /path/to/root
```

### 9.4 activate_agent.py

```bash
# Activate by alias
python activate_agent.py "MA"        # → meta-architect|plan
python activate_agent.py "architect" # → meta-architect|plan
python activate_agent.py "dev"       # → developer|exec

# Non-interactive mode (fail if not found)
python activate_agent.py "unknown" --no-menu
```

---

## 10. Troubleshooting

### 10.1 Common Issues

#### Shortcut Not Found
```
ERROR: Shortcut '~my-shortcut' not found in registry
```
**Solutions:**
1. Check frontmatter has `description` field (required)
2. Verify file is in scanned location (not in excluded folders)
3. Run registry builder with `--full` to see all shortcuts
4. Check layer/domain/mode filters aren't excluding it

#### Circular Dependency
```
WARNING: Circular dependency detected
```
**Solutions:**
1. Check frontmatter `dependencies` field for cycles
2. Use `--deps-only` to visualize dependency tree
3. Remove circular references from frontmatter

#### Windows Encoding Errors
```
UnicodeEncodeError: 'charmap' codec can't encode character
```
**Solutions:**
1. Ensure `from platform_compat import *` is first import
2. Check `_init_result` shows `'reconfigured'` or `'wrapped'`
3. Set environment variable: `PYTHONIOENCODING=utf-8`

#### Large File Warnings
```
WARNING: Large file detected (150,000 bytes)
```
**Solutions:**
1. Use `--quiet` to suppress warnings
2. Use `--max-size` to set explicit limit
3. Split large files into smaller chunks

### 10.2 Debug Commands

```bash
# Check registry contents
python build_shortcut_registry.py --full --format json | jq '.["~shortcut-name"]'

# Validate all shortcuts
for s in $(python build_shortcut_registry.py --format json | jq -r 'keys[]' | grep "^~"); do
    python shortcut_resolver.py "$s" --validate
done

# Check platform compatibility
python -c "from platform_compat import *; print(get_platform_info())"

# Test observability connection
curl -X POST http://localhost:7777/api/v2/sessions/test/executable \
    -H "Content-Type: application/json" \
    -d '{"type":"test","executable_id":"test"}'
```

### 10.3 Performance Tuning

| Issue | Solution |
|-------|----------|
| Slow registry build | Reduce `--depth` or use `--layer` filter |
| High memory usage | Use `--compact` output format |
| Repeated file reads | Ensure caching is working (check `_registry_cache`) |
| Slow dependency loading | Reduce `--max-depth` for dependencies |

---

## Appendix: Complete File Reference

| File | Location | Lines | Purpose |
|------|----------|-------|---------|
| `build_shortcut_registry.py` | `architech/01-system/08-automation/hooks/shortcut_system/` | 1162 | Registry builder |
| `shortcut_resolver.py` | `architech/01-system/08-automation/hooks/shortcut_system/` | 827 | Resolution engine |
| `context_loader.py` | `architech/01-system/08-automation/hooks/shortcut_system/` | 302 | Behavioral injection |
| `activate_agent.py` | `architech/01-system/08-automation/hooks/agent_system/` | 263 | Agent activation |
| `platform_compat.py` | `architech/01-system/08-automation/hooks/` | 227 | UTF-8 compatibility |
| `pre_tool_use.py` | `.claude/hooks/` | 327 | Claude hook |
| `http.py` | `.claude/hooks/utils/` | 54 | HTTP utilities |
| `registry.py` | `.claude/hooks/utils/` | 174 | Registry cache |
| `constants.py` | `.claude/hooks/utils/` | ~50 | Configuration |

---

**Document Version**: 1.0.0
**Generated**: 2025-12-31
**Source**: Multiagent ULTRATHINK Analysis (7 specialized agents)
