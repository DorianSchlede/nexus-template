# Tool Redirection Patterns Research Results

## Executive Summary

Tool redirection patterns allow hooks to intercept, modify, or reroute tool calls before execution. The key mechanisms are: (1) **updatedInput** for silent parameter modification, (2) **deny + permissionDecisionReason** for blocking with guidance to alternatives, and (3) **systemMessage** for invisible behavioral steering. The decision between silent redirect vs guidance depends on semantic impact - use silent modification for parameter enhancements, but guidance for tool substitutions that change behavior.

---

## 1. The updatedInput Mechanism

### Concept

The `updatedInput` field in PreToolUse hook responses allows silent modification of tool inputs before execution. Claude does not see the modification - it receives the original tool call response as if no change occurred. This enables transparent parameter normalization, enhancement, and safety additions.

### How It Works

```python
#!/usr/bin/env python3
import json
import sys

def main():
    data = json.load(sys.stdin)
    tool_name = data.get("tool_name", "")
    tool_input = data.get("tool_input", {})

    # Modify the input silently
    modified_input = tool_input.copy()
    modified_input["extract_depth"] = "advanced"  # Upgrade parameter

    # Return JSON with updatedInput
    output = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "allow"
        },
        "updatedInput": modified_input  # Silent modification
    }
    print(json.dumps(output))
    sys.exit(0)

if __name__ == "__main__":
    main()
```

### Key Properties

| Property | Value |
|----------|-------|
| Visibility to Claude | Invisible - Claude sees original call succeeded |
| Visibility to User | Invisible - no indication of modification |
| When to Use | Parameter enhancement, normalization, safety flags |
| When to Avoid | Major behavioral changes, tool substitution |

### Security Implications

- **Silent operation**: Changes happen without audit trail unless explicitly logged
- **Potential confusion**: If overused, debugging becomes difficult
- **Trust boundary**: Should only modify in well-understood, predictable ways
- **Logging recommended**: Consider logging original vs modified inputs for audit

### Real-World Example: Tavily Extract Depth Upgrader

From `claude-codex-settings`:

```python
# Always upgrade extract_depth to "advanced" for better results
tool_input = data["tool_input"]
tool_input["extract_depth"] = "advanced"

# Optional: Add systemMessage tip for GitHub URLs
github_urls = [url for url in urls if "github.com" in url]

if github_urls:
    print(json.dumps({
        "systemMessage": "Tip: For GitHub URLs, consider gh CLI instead",
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "allow",
            "updatedInput": tool_input,
        },
    }))
else:
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "allow",
            "updatedInput": tool_input,
        }
    }))
```

---

## 2. Common Redirection Patterns

### 2.1 WebFetch to MCP Tool Redirect

**Scenario**: Redirect built-in WebFetch to a more capable MCP tool (e.g., Tavily)

**Strategy**: Block with guidance (NOT silent redirect) - because this changes which tool executes

**Implementation** (from claude-codex-settings):

```python
#!/usr/bin/env python3
import json
import sys

def main():
    try:
        data = json.load(sys.stdin)
        url = data["tool_input"]["url"]
    except (KeyError, json.JSONDecodeError) as err:
        sys.exit(1)

    print(json.dumps({
        "systemMessage": "WebFetch detected. AI is directed to use Tavily extract instead.",
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": f"Please use mcp__tavily__tavily-extract with urls: ['{url}'] and extract_depth: 'advanced'"
        }
    }))
    sys.exit(0)

if __name__ == "__main__":
    main()
```

**Why Guidance over Silent Redirect**: Tool substitution changes behavior semantically - Claude should be aware it's using a different tool so it can handle the response correctly.

### 2.2 Path Normalization (Silent)

**Scenario**: Normalize relative paths to absolute paths

**Strategy**: Silent redirect via updatedInput - no semantic change, just normalization

**Implementation**:

```python
import os

def normalize_file_path(tool_input: dict, cwd: str) -> dict:
    """Normalize file_path to absolute path."""
    modified = tool_input.copy()
    file_path = modified.get("file_path", "")

    if file_path and not os.path.isabs(file_path):
        modified["file_path"] = os.path.join(cwd, file_path)

    return modified

# In hook:
output = {
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "allow",
        "updatedInput": normalize_file_path(tool_input, os.getcwd())
    }
}
```

### 2.3 Command Sanitization (Silent)

**Scenario**: Add safety flags to commands automatically

**Strategy**: Silent redirect - defensive enhancement without semantic change

**Implementation**:

```python
import re

def add_safety_flags(command: str) -> str:
    """Add safety flags to potentially dangerous commands."""
    # Add -i (interactive) flag to rm commands for confirmation
    if re.match(r"^\s*rm\s+", command):
        # Check if already has -i or --interactive
        if not re.search(r"\s-[a-z]*i|--interactive", command):
            return re.sub(r"^(\s*rm)\s+", r"\1 -i ", command)
    return command

# In hook:
modified_input = tool_input.copy()
if "command" in modified_input:
    modified_input["command"] = add_safety_flags(modified_input["command"])

output = {
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "allow",
        "updatedInput": modified_input
    }
}
```

### 2.4 Default Timeout Injection (Silent)

**Scenario**: Ensure all Bash commands have a timeout

**Strategy**: Silent redirect - adds missing parameter

**Implementation**:

```python
def ensure_timeout(tool_input: dict, default_ms: int = 30000) -> dict:
    """Ensure Bash command has timeout."""
    modified = tool_input.copy()
    if "timeout" not in modified or modified["timeout"] is None:
        modified["timeout"] = default_ms
    return modified
```

### 2.5 Shortcut Resolution (Existing in Nexus)

**Pattern from shortcut_resolver.py**:

The existing Nexus shortcut resolver is a form of path redirection that:
1. Takes a shortcut like `~architect`
2. Resolves it via registry lookup to actual file path
3. Returns the resolved path for Claude to read

**Key characteristics**:
- **Visible transformation**: Claude sees the resolved path, not the shortcut
- **Registry-based**: Single source of truth in YAML
- **Caching**: Results cached for performance
- **Fallback**: Returns original if not found

```python
# From shortcut_resolver.py
def resolve(self, shortcut: str, feature: Optional[str] = None) -> str:
    """Resolve a shortcut to actual file path."""
    # Return non-shortcuts as-is
    if not shortcut.startswith('~'):
        return shortcut

    # Check cache first
    cache_key = f"{shortcut}:{self.repo_context}:{feature}"
    if cache_key in self.cache:
        return self.cache[cache_key]

    resolved_path = self._resolve_shortcut(shortcut, feature)
    self.cache[cache_key] = resolved_path
    return resolved_path
```

This is NOT silent redirection - Claude receives the resolved path and knows what file it's reading.

---

## 3. Guidance vs Silent Redirect Decision Matrix

### Decision Framework

| Factor | Silent Redirect (updatedInput) | Guidance (deny + reason) |
|--------|-------------------------------|--------------------------|
| **Semantic change** | No | Yes |
| **Tool substitution** | Never | Always |
| **Parameter enhancement** | Yes | No |
| **Path normalization** | Yes | No |
| **Safety additions** | Yes (defensive) | No |
| **Claude awareness needed** | No | Yes |
| **Response format changes** | No | Yes |
| **Audit importance** | Low | High |

### When to Use Silent Redirect (updatedInput)

1. **Path normalization** - Converting relative to absolute paths
2. **Parameter enhancement** - Adding better defaults (`extract_depth: advanced`)
3. **Safety flag injection** - Adding `-i` to rm commands
4. **Default value injection** - Adding timeout when not specified
5. **Format normalization** - Standardizing input formats
6. **Typo correction** - Fixing known typos in patterns

### When to Use Guidance (systemMessage + deny)

1. **Tool substitution** - WebFetch to Tavily, grep to rg
2. **Workflow changes** - Suggesting different approaches
3. **Major behavioral changes** - Anything that changes what Claude expects
4. **Response format changes** - When the tool returns different structure
5. **Learning opportunities** - Teaching Claude about better patterns
6. **Audit requirements** - When changes must be visible

### Example: The Right Choice

```python
# WRONG: Silent redirect for tool substitution
output = {
    "updatedToolName": "mcp__tavily__tavily_search",  # BAD - silent tool change
    "updatedInput": {"query": original_query}
}

# RIGHT: Guidance for tool substitution
output = {
    "systemMessage": "WebSearch is available, but Tavily provides better results",
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": "Please use mcp__tavily__tavily_search instead"
    }
}

# RIGHT: Silent redirect for parameter enhancement
output = {
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "allow",
        "updatedInput": {**tool_input, "extract_depth": "advanced"}
    }
}
```

---

## 4. MCP Tool Integration Patterns

### Pattern: Detect MCP Availability

```python
import subprocess
import json

def check_mcp_tools_available() -> list[str]:
    """Check which MCP tools are available by querying settings."""
    try:
        # Read from .claude/settings.json or similar
        with open(".claude/settings.json") as f:
            settings = json.load(f)

        mcp_servers = settings.get("mcpServers", {})
        available_tools = []

        for server_name, config in mcp_servers.items():
            # Each server may provide multiple tools
            tools = config.get("tools", [])
            available_tools.extend([f"mcp__{server_name}__{t}" for t in tools])

        return available_tools
    except Exception:
        return []
```

### Pattern: Suggest MCP Alternative with Fallback

```python
MCP_ALTERNATIVES = {
    "WebFetch": {
        "mcp_tool": "mcp__tavily__tavily-extract",
        "reason": "Tavily provides better structured extraction",
        "fallback_allowed": True  # Allow WebFetch if Tavily unavailable
    },
    "WebSearch": {
        "mcp_tool": "mcp__tavily__tavily_search",
        "reason": "Tavily search provides more relevant results",
        "fallback_allowed": True
    }
}

def suggest_mcp_alternative(tool_name: str, tool_input: dict) -> dict | None:
    """Return hook output suggesting MCP alternative, with fallback."""
    if tool_name not in MCP_ALTERNATIVES:
        return None

    alt = MCP_ALTERNATIVES[tool_name]
    available = check_mcp_tools_available()

    if alt["mcp_tool"] in available:
        # MCP tool available - suggest it
        return {
            "systemMessage": alt["reason"],
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": f"Please use {alt['mcp_tool']} instead"
            }
        }
    elif alt["fallback_allowed"]:
        # MCP not available, allow original
        return None  # Allow through
    else:
        # MCP required but not available
        return {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": f"{alt['mcp_tool']} is required but not configured"
            }
        }
```

### Pattern: MCP Tool Parameter Enhancement

```python
def enhance_mcp_parameters(tool_name: str, tool_input: dict) -> dict:
    """Enhance MCP tool parameters for better results."""

    MCP_ENHANCEMENTS = {
        "mcp__tavily__tavily-extract": {
            "extract_depth": "advanced",
            "include_images": False
        },
        "mcp__context7__query-docs": {
            "max_tokens": 10000  # Ensure enough context
        }
    }

    enhancements = MCP_ENHANCEMENTS.get(tool_name, {})
    if not enhancements:
        return tool_input

    modified = tool_input.copy()
    for key, value in enhancements.items():
        if key not in modified:  # Only add if not already set
            modified[key] = value

    return modified
```

---

## 5. Integration Notes

### Existing Redirection in Nexus

From analysis of `.claude/hooks/pre_tool_use.py`:

1. **Executable Detection & Streaming** (lines 59-113, 163-177)
   - Detects when Claude loads executables (agents, skills, tasks, workflows)
   - Streams events to observability server
   - NOT a redirection - purely observational

2. **Safety Blocking** (lines 179-282)
   - `is_dangerous_rm_command()` - blocks dangerous rm patterns
   - `is_env_file_access()` - blocks .env file access
   - Uses exit code 2 to block - NOT updatedInput

3. **Shortcut Resolution** (separate file)
   - Resolves `~shortcuts` to file paths
   - Returns resolved path to Claude
   - Visible transformation, not silent

### Safe to Add (Low Risk)

| Pattern | Mechanism | Risk Level |
|---------|-----------|------------|
| Path normalization | updatedInput | Low |
| Default timeout injection | updatedInput | Low |
| Safety flag addition | updatedInput | Low |
| MCP parameter enhancement | updatedInput | Low |
| Tool preference suggestions | systemMessage | Low |

### Moderate Risk (Needs Testing)

| Pattern | Mechanism | Risk Level |
|---------|-----------|------------|
| Tool redirection guidance | deny + reason | Medium |
| MCP tool substitution | deny + reason | Medium |
| Command sanitization | updatedInput | Medium |

### Must Preserve

1. **Existing executable detection** - Observability depends on it
2. **Safety blocking for rm/env** - Security critical
3. **Shortcut resolution behavior** - Core navigation system
4. **Database event streaming** - Observability infrastructure

### Caution Areas

1. **Never silently change tool_name** - Use guidance instead
2. **Log all updatedInput modifications** - Audit trail essential
3. **Test MCP availability before suggesting** - Graceful fallback
4. **Prefer guidance over silent modification** - When in doubt, be visible
5. **Document all redirections** - Team must understand behavior

---

## 6. Copy-Paste Ready Templates

### Template: Parameter Enhancement Hook

```python
#!/usr/bin/env python3
"""PreToolUse hook: Enhance tool parameters silently."""
import json
import sys

ENHANCEMENTS = {
    "mcp__tavily__tavily-extract": {
        "extract_depth": "advanced"
    },
    "Bash": {
        "timeout": 30000  # Default 30s timeout
    }
}

def main():
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)  # Fail open

    tool_name = data.get("tool_name", "")
    tool_input = data.get("tool_input", {})

    enhancements = ENHANCEMENTS.get(tool_name, {})
    if not enhancements:
        sys.exit(0)  # No enhancements, allow through

    # Apply enhancements
    modified = tool_input.copy()
    for key, value in enhancements.items():
        if key not in modified:
            modified[key] = value

    output = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "allow",
            "updatedInput": modified
        }
    }
    print(json.dumps(output))
    sys.exit(0)

if __name__ == "__main__":
    main()
```

### Template: Tool Redirect with Guidance

```python
#!/usr/bin/env python3
"""PreToolUse hook: Redirect tool with guidance."""
import json
import sys

REDIRECTS = {
    "WebFetch": {
        "target": "mcp__tavily__tavily-extract",
        "reason": "Tavily provides better web content extraction",
        "param_mapping": lambda i: {"urls": [i.get("url", "")], "extract_depth": "advanced"}
    },
    "WebSearch": {
        "target": "mcp__tavily__tavily_search",
        "reason": "Tavily search provides more structured results",
        "param_mapping": lambda i: {"query": i.get("query", "")}
    }
}

def main():
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    tool_name = data.get("tool_name", "")
    tool_input = data.get("tool_input", {})

    if tool_name not in REDIRECTS:
        sys.exit(0)

    redirect = REDIRECTS[tool_name]
    suggested_params = redirect["param_mapping"](tool_input)

    output = {
        "systemMessage": f"{redirect['reason']}. Use {redirect['target']} instead.",
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": (
                f"Please use {redirect['target']} with parameters: "
                f"{json.dumps(suggested_params)}"
            )
        }
    }
    print(json.dumps(output))
    sys.exit(0)

if __name__ == "__main__":
    main()
```

### Template: Path Normalization Hook

```python
#!/usr/bin/env python3
"""PreToolUse hook: Normalize file paths to absolute."""
import json
import sys
import os

PATH_TOOLS = {"Read", "Write", "Edit", "MultiEdit"}

def main():
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    tool_name = data.get("tool_name", "")
    tool_input = data.get("tool_input", {})

    if tool_name not in PATH_TOOLS:
        sys.exit(0)

    file_path = tool_input.get("file_path", "")
    if not file_path or os.path.isabs(file_path):
        sys.exit(0)  # Already absolute or empty

    # Normalize to absolute path
    modified = tool_input.copy()
    modified["file_path"] = os.path.abspath(file_path)

    output = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "allow",
            "updatedInput": modified
        }
    }
    print(json.dumps(output))
    sys.exit(0)

if __name__ == "__main__":
    main()
```

---

## 7. Success Criteria Checklist

- [x] updatedInput mechanism fully documented
- [x] At least 4 redirection patterns documented (6 covered)
- [x] Guidance vs silent redirect decision matrix
- [x] MCP integration patterns
- [x] Existing shortcut_resolver.py analyzed
- [x] Copy-paste-ready code templates (3 templates provided)

---

*Research completed by Subagent 5 | Tool Redirection Patterns*
*Source: hook-research corpus + Nexus codebase analysis*
