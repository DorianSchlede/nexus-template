# Architech Hook System Deep Dive

## Executive Summary

Architech's hook system is a **multi-layered, event-driven architecture** combining shortcut resolution, context bundling, agent activation, and observability into a cohesive framework. Its core innovation is **progressive disclosure** - loading only what's needed when it's needed - achieving 60-85% token reduction compared to monolithic context loading. The system uses frontmatter metadata as the single source of truth for entity behavior, enabling dynamic behavioral injection without code changes.

---

## 1. System Architecture

### Overall Design

```
                         USER INPUT: "~meta-architect"
                                    |
                                    v
+-----------------------------------------------------------------------+
|                          PRE_TOOL_USE.PY                              |
|  +------------------+  +------------------+  +------------------+     |
|  | Safety Guards    |  | Exec Detection   |  | Stream Event     |     |
|  | rm -rf, .env     |  | Registry Lookup  |  | Fire & Forget    |     |
|  +--------+---------+  +--------+---------+  +--------+---------+     |
|           |                     |                     |               |
|      Exit 2 = BLOCK        Registry Hit          HTTP POST            |
+-----------------------------------------------------------------------+
                                  |
                                  v
+-----------------------------------------------------------------------+
|                     SHORTCUT_RESOLVER.PY                              |
|  +------------------+  +------------------+  +------------------+     |
|  | Root Detection   |  | Registry Build   |  | Content Load     |     |
|  | 4 Strategies     |  | 2-Tier Cascade   |  | + Dependencies   |     |
|  +------------------+  +------------------+  +------------------+     |
+-----------------------------------------------------------------------+
                                  |
                                  v
+-----------------------------------------------------------------------+
|                      CONTEXT_LOADER.PY                                |
|  +------------------+  +------------------+  +------------------+     |
|  | Flag Extraction  |  | Context Inject   |  | Format AI-Ready  |     |
|  | interactive/cog  |  | ULTRATHINK etc   |  | Output           |     |
|  +------------------+  +------------------+  +------------------+     |
+-----------------------------------------------------------------------+
```

### Key Concepts

| Concept | Definition | Architech | Nexus |
|---------|------------|-----------|-------|
| **Executables** | Runnable entities | agent, skill, task, workflow | Same |
| **Shortcuts** | Quick references | `~agent:name`, `~task:name` | `~meta-architect`, simpler |
| **Context Bundles** | Pre-packaged context | Behavioral flags + content | context_startup.json |
| **Mode System** | Context filtering | plan/exec/discover | Not implemented |
| **Layer System** | Hierarchical access | meta/system/domain/cross-domain | Flat structure |

### File Structure Comparison

| Component | Architech Lines | Nexus Lines | Gap Analysis |
|-----------|-----------------|-------------|--------------|
| Registry Builder | 1162 | 0 | **MISSING** - Nexus uses static YAML |
| Shortcut Resolver | 827 | 341 | Nexus is simpler, lacks dynamic registry |
| Context Loader | 302 | 0 | **MISSING** - Nexus has no behavioral flags |
| Agent Activation | 263 | 0 | **MISSING** - Nexus doesn't switch agents |
| Pre-Tool-Use Hook | 327 | 328 | **PARITY** |
| Platform Compat | 227 | 0 | **PARTIAL** - UTF-8 handled inline |

---

## 2. Shortcut/Executable System

### Shortcut Types

| Prefix | Type | Example | Architech | Nexus |
|--------|------|---------|-----------|-------|
| `~` | Any executable | `~meta-architect` | Yes | Yes |
| `~agent:` | Agent | `~agent:developer` | Yes | Partial |
| `~task:` | Task | `~task:create-project` | Yes | Partial |
| `~skill:` | Skill | `~skill:hubspot` | Yes | No |
| `~workflow:` | Workflow | `~workflow:deploy` | Yes | No |
| `~layer:cat:file` | Qualified | `~meta:agent:architect` | Yes | No |

### Architech Detection Logic

```python
# From build_shortcut_registry.py, Lines 245-265
def _process_file(self, item):
    # REQUIRED: description field
    if 'description' not in post.metadata:
        return  # Skip files without description

    # OPTIONAL: behavioral flags
    flag_fields = ['interactive', 'cognitive_mode', 'progressive', 'reasoning']
    for flag in flag_fields:
        if flag in post.metadata:
            behavioral_flags[flag] = post.metadata[flag]
```

### Nexus Detection Logic

```python
# From pre_tool_use.py, Lines 115-146
def parse_shortcut_for_type(shortcut):
    # Explicit type prefix: ~type:id
    match = re.match(r"~(agent|skill|task|workflow):([a-zA-Z0-9_-]+)", shortcut)
    if match:
        return {"type": match.group(1), "id": match.group(2)}

    # Known agent shortcuts (hardcoded list)
    known_agents = {
        "~meta-architect", "~master", "~architect", "~developer",
        "~product-manager", "~analyst", ...
    }
    if shortcut in known_agents:
        return {"type": "agent", "id": shortcut.lstrip("~")}
```

### Comparison with Nexus

**Differences:**
1. Architech builds registry dynamically from frontmatter; Nexus uses static YAML
2. Architech has 5-layer filtering (layer, domain, agent scope, mode, archive); Nexus has none
3. Architech generates collision-free aliases; Nexus relies on hardcoded lists
4. Architech has 3 alias levels (short, medium, full); Nexus has only direct shortcuts

**Recommendation: ADOPT (Medium Priority)**

Nexus should adopt dynamic registry building for new skills, but keep static YAML for stability:
- Add frontmatter scanning for `03-skills/` directory
- Generate compact registry at session start
- Retain hardcoded known_agents for backward compatibility

---

## 3. Context Bundle System

### What Are Context Bundles?

Architech's context bundles are **packages of behavioral instructions** extracted from entity frontmatter and injected into Claude's context when an executable is loaded. They control:

1. **Interactive Mode** - Force user engagement before proceeding
2. **Cognitive Mode** - ULTRATHINK, systems-thinking, first-principles
3. **Progressive Disclosure** - Load context incrementally
4. **Reasoning** - Explain why interactive mode is required

### Bundle Loading Pattern

```python
# From context_loader.py, Lines 82-127
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

### Context Injection Output

```python
# From context_loader.py, Lines 129-187
def _build_context_injection(self, shortcut: str, flags: Dict) -> str:
    injections = []
    injections.append(f"=== DYNAMIC CONTEXT FOR {shortcut} ===\n")

    # Interactive Mode
    if flags.get('interactive'):
        reasoning = flags.get('reasoning', 'User guidance required')
        injections.append("[!] INTERACTIVE MODE REQUIRED")
        injections.append(f"   Reasoning: {reasoning}")
        injections.append("   - Engage user with questions before proceeding")
        injections.append("   - Validate each step before moving forward")

    # Cognitive Mode
    cognitive_guidance = {
        'ULTRATHINK': 'Deep analysis with step-by-step reasoning',
        'systems-thinking': 'Holistic view, identify relationships',
        'first-principles': 'Break down to fundamental truths',
    }
    if flags.get('cognitive_mode'):
        mode = flags['cognitive_mode']
        guidance = cognitive_guidance.get(mode, 'Apply specialized thinking')
        injections.append(f"[COGNITIVE MODE: {mode}]")
        injections.append(f"   Guidance: {guidance}")
```

### Application to Nexus

**Current State:**
- Nexus uses `context_startup.json` as a monolithic bundle
- No per-skill or per-project behavioral flags
- No dynamic injection based on what's being loaded

**Recommendation: ADOPT (High Priority)**

Add frontmatter flags to skill SKILL.md files:

```yaml
---
name: hubspot-master
description: HubSpot CRM integration skill
interactive: true
reasoning: "API keys and permissions must be verified first"
cognitive_mode: first-principles
---
```

Then inject when skill is loaded:
```python
# In nexus-loader.py load_skill()
if skill_flags.get('interactive'):
    result['behavioral_context'] = build_skill_injection(skill_flags)
```

---

## 4. Pre-Tool-Use Hook Patterns

### Executable Detection

```python
# From Architech pre_tool_use.py, Lines 59-112
EXECUTABLE_TYPES = {"agent", "skill", "task", "workflow"}

def detect_executable(tool_name, tool_input):
    if tool_name == "Bash":
        command = tool_input.get("command", "")
        # Extract shortcut from shortcut_resolver.py command
        match = re.search(r"shortcut_resolver\.py\s+(~[a-zA-Z0-9_:-]+)", command)
        if match:
            shortcut = match.group(1)
            # Registry lookup (single source of truth)
            resolved = lookup_shortcut(shortcut)
            if resolved and resolved["type"] in EXECUTABLE_TYPES:
                return {
                    "type": resolved["type"],
                    "id": resolved["id"],
                    "target": resolved["path"],
                    "shortcut": shortcut,
                    "detection_method": "bash"
                }

    elif tool_name == "Read":
        file_path = tool_input.get("file_path", "")
        # Path pattern matching (fallback)
        detected = detect_from_path_patterns(file_path)
        if detected:
            return {..., "detection_method": "read"}

    return None
```

### Safety Checks (Identical in Both Systems)

```python
# rm -rf Detection (Both systems have this)
patterns = [
    r"\brm\s+.*-[a-z]*r[a-z]*f",      # rm -rf, rm -fr, rm -Rf
    r"\brm\s+.*-[a-z]*f[a-z]*r",      # rm -fr variants
    r"\brm\s+--recursive\s+--force",  # Long form
    r"\brm\s+-r\s+.*-f",              # Separated flags
]

# Dangerous paths with recursive flag
dangerous_paths = [
    r"/",       # Root directory
    r"~",       # Home directory
    r"\$HOME",  # Home environment variable
    r"\.\.",    # Parent directory references
    r"\*",      # Wildcards
]

# .env File Protection (Both systems have this)
env_patterns = [
    r"\b\.env\b(?!\.sample)",         # .env (not .env.sample)
    r"cat\s+.*\.env\b(?!\.sample)",   # cat .env
]
```

### Exit Codes

| Code | Meaning | Claude Behavior | Both Systems |
|------|---------|-----------------|--------------|
| `0` | Success/safe | Tool call proceeds | Yes |
| `2` | Security violation | **BLOCK** tool call | Yes |

**Recommendation: NO CHANGES NEEDED**

Nexus pre_tool_use.py is at parity with Architech. Both systems:
- Detect executables via regex patterns
- Block rm -rf and .env access
- Stream to observability server
- Use identical exit code conventions

---

## 5. Post-Tool-Use Hook Patterns

### Architech Patterns

Architech's post_tool_use hook is minimal - primarily for:
1. Logging tool outputs
2. Quality enforcement (checking for errors)
3. Chaining actions (rarely used)

### Nexus Patterns

```python
# From post_tool_use.py (Nexus has more features)
# - Voice notification on long operations
# - Session logging
# - Quality checks (error detection)
```

**Recommendation: NO CHANGES NEEDED**

Nexus post_tool_use is **MORE ADVANCED** than Architech in this area.

---

## 6. Session Hook Patterns

### Architech Session Start

Architech's session start is simpler - it just builds the shortcut registry and makes it available.

### Nexus Session Start

```python
# From session_start.py, Lines 33-63
def run_nexus_loader(session_id: str, resume_mode: bool) -> str:
    """Execute nexus-loader and return its output."""
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", "")
    loader_path = Path(project_dir) / "00-system" / "core" / "nexus-loader.py"

    # Build command
    cmd = ["python", str(loader_path)]
    if resume_mode:
        cmd.append("--resume")
    else:
        cmd.append("--startup")
    cmd.extend(["--session", session_id])

    # Execute loader
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
    return result.stdout.strip()
```

**KEY INSIGHT**: Nexus has a more advanced pattern - it **runs the loader directly** instead of telling Claude to run it. This is documented as:

```python
# KEY INSIGHT: Don't tell Claude to run the loader - RUN IT FOR CLAUDE
# and inject the result directly as additionalContext.
```

### Resume Handling Comparison

| Feature | Architech | Nexus |
|---------|-----------|-------|
| Resume detection | source=resume | source=resume or compact |
| Cache per session | No | Yes (session hash) |
| Direct execution | No | Yes (subprocess) |
| Slim pointer | No | Yes (summary + path) |

**Recommendation: ARCHITECH SHOULD ADOPT NEXUS PATTERN**

Nexus is **more advanced** here. The direct execution pattern is better.

---

## 7. Event Streaming System

### Event Types

| Event | Payload | When | Architech | Nexus |
|-------|---------|------|-----------|-------|
| session_start | source, timestamp | Session begins | Yes | Yes |
| executable | type, id, target, shortcut | Entity loaded | Yes | Yes |
| tool_use | tool_name, input | Every tool call | Yes | Partial |
| session_end | reason, transcript | Session ends | Yes | Yes |

### Fire-and-Forget Implementation (Identical)

```python
# Both systems use this pattern (http.py)
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

**Design Decisions (Both Systems):**
- **5 second timeout**: Prevents blocking if server down
- **Never raises**: Observability shouldn't cause failures
- **Fire-and-forget**: Return value often ignored

**Recommendation: NO CHANGES NEEDED**

Both systems have identical event streaming. This is a mature pattern.

---

## 8. Mode System & Filtering

### Architech Mode Definitions

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
```

### Context Reduction Results

| Mode | Entity Count | Reduction | Use Case |
|------|--------------|-----------|----------|
| **plan** | 11 types | ~40-60% | Design, architecture |
| **exec** | 4 types | ~65% | Implementation |
| **discover** | 5 types | ~55% | Learning, exploration |

Combined with Agent Scoping: **60-85% total reduction**

### Application to Nexus

**Current State:** Nexus loads ALL skills/projects at startup (no filtering)

**Recommendation: ADOPT (High Priority)**

Implement mode-based filtering in nexus-loader.py:

```python
# In scan_skills() and scan_projects()
def scan_skills(base_path: str, mode: str = "exec"):
    """Scan skills with mode-based filtering."""
    MODE_SKILL_TYPES = {
        'exec': {'integration', 'orchestrator', 'analysis'},
        'discover': {'documentation', 'reference'},
        'plan': {'all'}  # Full access
    }
    allowed_types = MODE_SKILL_TYPES.get(mode, MODE_SKILL_TYPES['exec'])
    # Filter skills by type...
```

---

## 9. Patterns to Adopt in Nexus

### High Priority

1. **Context Bundle System**
   - Why: Enables per-skill behavioral control without code changes
   - Effort: Medium (2-3 hours)
   - Code: Add frontmatter parsing to skill loader
   ```python
   # In load_skill():
   if skill_flags.get('interactive'):
       result['behavioral_context'] = build_injection(skill_flags)
   ```

2. **Mode-Based Filtering**
   - Why: 40-65% token reduction, faster startup
   - Effort: Medium (2-3 hours)
   - Code: Add `--mode` flag to nexus-loader.py

3. **Dynamic Registry Building**
   - Why: Auto-discover new skills without manual YAML updates
   - Effort: High (4-6 hours)
   - Code: Port build_shortcut_registry.py logic

### Medium Priority

1. **Collision Handling**
   - Why: Prevents shortcut conflicts as skills grow
   - Effort: Low (1 hour)
   - Code: Add layer prefix when collision detected

2. **Qualified Shortcuts**
   - Why: Explicit type:name format reduces ambiguity
   - Effort: Low (1 hour)
   - Code: Extend parse_shortcut_for_type()

3. **Agent Scope Filtering**
   - Why: Only show skills relevant to current context
   - Effort: Medium (2 hours)
   - Code: Add agent_scope frontmatter field

### Low Priority / Future

1. **Cognitive Mode Injection**
   - Why: Nice-to-have for complex skills
   - Effort: Low (1 hour)
   - Defer: Only if user requests specific thinking patterns

2. **Two-Tier Registry Cascade**
   - Why: Architech's domain loading is over-engineered for Nexus
   - Defer: Nexus is flatter, doesn't need this complexity

3. **Agent Activation Menu**
   - Why: Nexus doesn't have multi-agent personas
   - Defer: Not applicable to current architecture

---

## 10. Patterns NOT to Adopt

### Already Implemented Better in Nexus

| Pattern | Why Nexus is Better |
|---------|---------------------|
| Session Start | Direct subprocess execution vs. instruction output |
| Cache per Session | Hash-based session isolation prevents collisions |
| Resume State | save_resume_state.py is more comprehensive |
| Slim Pointer | Nexus injects summary + Read instruction |

### Not Applicable

| Pattern | Why Not Applicable |
|---------|---------------------|
| Agent Activation | Nexus has single orchestrator, no agent switching |
| Layer System | Nexus is flat (00-system, 01-memory, etc.), not hierarchical |
| Domain Filtering | No domain separation in Nexus structure |
| Cross-Domain Registry | Single project structure |

### Too Complex for Current Scope

| Pattern | Why Defer |
|---------|-----------|
| Two-Tier Cascade | Architech's base + domain registry is over-engineered |
| 5-Layer Filtering | Nexus doesn't have layers to filter |
| Entity Semantic Aliases | ~entity:agent adds complexity without benefit |

---

## 11. Integration Recommendations

### Quick Wins (1-2 hours each)

1. **Add `--mode exec` to nexus-loader.py**
   - Filter skills to only executables
   - Immediate token savings

2. **Parse `interactive` flag from SKILL.md frontmatter**
   - Simple regex extraction
   - Enables "stop and ask" behavior

3. **Add shortcut validation to pre_tool_use**
   - Log unknown shortcuts for debugging
   - No user-facing changes

### Requires Planning (4+ hours)

1. **Dynamic Registry Generation**
   - Scan 03-skills/ at startup
   - Build JSON registry
   - Replace static YAML approach

2. **Behavioral Context Injection**
   - Full frontmatter flag support
   - Context formatting for Claude
   - Integration with skill loader

### Database Considerations

**CAREFUL - These patterns affect database events:**

| Pattern | Database Impact | Risk Level |
|---------|-----------------|------------|
| Executable streaming | Already implemented | Low |
| Session events | Already implemented | Low |
| Mode filtering | May reduce events | Medium |
| New event types | Requires schema | High |

**Recommendation:** Do NOT add new event types without database schema review.

---

## 12. Summary Matrix

| Pattern | Adopt? | Priority | Effort | Token Savings |
|---------|--------|----------|--------|---------------|
| Context Bundles | YES | High | Medium | 10-20% |
| Mode Filtering | YES | High | Medium | 40-65% |
| Dynamic Registry | YES | Medium | High | N/A |
| Collision Handling | YES | Medium | Low | N/A |
| Qualified Shortcuts | YES | Medium | Low | N/A |
| Agent Scope | MAYBE | Low | Medium | 20-30% |
| Cognitive Modes | MAYBE | Low | Low | N/A |
| Two-Tier Cascade | NO | - | - | - |
| Layer System | NO | - | - | - |
| Agent Activation | NO | - | - | - |

---

**Document Version**: 1.0.0
**Generated**: 2026-01-01
**Source**: Architech hook-system-reference.system.doc.md analysis
**Analyst**: Subagent 6 - Architech Patterns Deep Dive
