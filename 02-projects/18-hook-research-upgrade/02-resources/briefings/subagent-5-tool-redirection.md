# Subagent Briefing: Tool Redirection Patterns Research

**Priority**: MEDIUM
**Output Path**: `02-projects/18-hook-research-upgrade/02-resources/research-tool-redirection.md`

---

## Mission

Research tool redirection patterns: how to silently modify tool inputs, redirect tools to alternatives, and use updatedInput to improve tool behavior. Focus on patterns that enhance Claude's capabilities without changing visible behavior.

---

## Required Reading (IN ORDER - READ EVERYTHING)

### Step 1: Understand Research Structure
```
READ: 04-workspace/00-ai-native-org/hook-research/_index.md
```
Navigation hub.

### Step 2: Context Loading (updatedInput)
```
READ: 04-workspace/00-ai-native-org/hook-research/hook-guides/CONTEXT_LOADING.md
```
The updatedInput mechanism - silent input modification.

### Step 3: PreToolUse Guide (Redirection patterns)
```
READ: 04-workspace/00-ai-native-org/hook-research/hook-guides/PRE_TOOL_USE.md
```
Tool interception and modification patterns.

### Step 4: MCP Tool Patterns
```
READ: 04-workspace/00-ai-native-org/hook-research/patterns/mcp-tools.yaml
```
MCP tool redirection patterns (if exists).

---

## Current Nexus System (FOR COMPARISON)

### Current PreToolUse
```
READ: .claude/hooks/pre_tool_use.py
```
Does it currently redirect any tools?

### Shortcut Resolver
```
READ: .claude/hooks/shortcut_resolver.py
```
This is a form of "redirection" - understand how it works.

---

## Output Format

Create file at:
```
02-projects/18-hook-research-upgrade/02-resources/research-tool-redirection.md
```

Structure:

```markdown
# Tool Redirection Patterns Research Results

## Executive Summary
[2-3 sentences: What tool redirection patterns exist?]

---

## 1. The updatedInput Mechanism

### Concept
Silently modify tool input before execution. Claude doesn't see the modification.

### How It Works
\`\`\`python
# Hook outputs JSON with updatedInput
output = {
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "allow"
    },
    "updatedInput": {
        # Modified tool_input goes here
        "command": "modified_command",
        "file_path": "modified_path"
    }
}
print(json.dumps(output))
sys.exit(0)
\`\`\`

### Security Implications
- Claude doesn't see the modification
- Use carefully - can be confusing if overused
- Good for: path normalization, command sanitization
- Bad for: major behavior changes

---

## 2. Common Redirection Patterns

### 2.1 WebFetch to MCP Redirect
**Scenario**: Redirect WebFetch to a more capable MCP tool
**Implementation**:
\`\`\`python
def redirect_webfetch_to_mcp(tool_input: dict) -> dict | None:
    """
    If WebFetch is called, suggest using MCP browser tool instead.
    Returns modified input or None if no redirect needed.
    """
    url = tool_input.get("url", "")

    # Could redirect to playwright-mcp or similar
    # But better to use systemMessage to guide Claude
    return None  # Use guidance instead of silent redirect
\`\`\`

### 2.2 Path Normalization
**Scenario**: Normalize relative paths to absolute
**Implementation**:
\`\`\`python
def normalize_file_path(tool_input: dict, cwd: str) -> dict:
    """Normalize file_path to absolute path."""
    file_path = tool_input.get("file_path", "")
    if file_path and not os.path.isabs(file_path):
        tool_input["file_path"] = os.path.join(cwd, file_path)
    return tool_input
\`\`\`

### 2.3 Command Sanitization
**Scenario**: Add safety flags to commands
**Implementation**:
\`\`\`python
def add_safety_flags(command: str) -> str:
    """Add -i (interactive) flag to rm commands."""
    if re.match(r"^\s*rm\s+", command):
        # Add -i flag for interactive confirmation
        return re.sub(r"^(\s*rm)\s+", r"\1 -i ", command)
    return command
\`\`\`

### 2.4 Shortcut Resolution (Existing in Nexus)
**Pattern from shortcut_resolver.py**:
[Document how shortcut_resolver.py works]

---

## 3. Guidance vs Silent Redirect

### When to Use updatedInput (Silent Redirect)
- Path normalization (no semantic change)
- Adding safety flags (defensive)
- Fixing typos in known patterns

### When to Use systemMessage (Guidance)
- Tool choice suggestions
- Alternative approaches
- Anything that changes Claude's behavior significantly

### Example: Prefer Guidance
\`\`\`python
# Instead of silent redirect, guide Claude
output = {
    "systemMessage": (
        "Consider using the mcp_browser tool instead of WebFetch "
        "for this URL - it handles JavaScript rendering."
    ),
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "allow"
    }
}
\`\`\`

---

## 4. MCP Tool Integration

### Pattern: Detect MCP Availability
\`\`\`python
def check_mcp_tools_available() -> list[str]:
    """Check which MCP tools are available."""
    # Could read from settings or probe
    return []  # Implementation TBD
\`\`\`

### Pattern: Suggest MCP Alternative
\`\`\`python
def suggest_mcp_alternative(tool_name: str, tool_input: dict) -> str | None:
    """Return systemMessage suggesting MCP alternative."""
    MCP_ALTERNATIVES = {
        "WebFetch": "Consider mcp_browser for JavaScript-heavy pages",
        "Bash:git": "Consider mcp_github for GitHub operations",
    }
    return MCP_ALTERNATIVES.get(tool_name)
\`\`\`

---

## 5. Integration Notes

### Existing Redirection in Nexus
- shortcut_resolver.py handles shortcut expansion
- [Other existing redirections]

### Safe to Add
- Path normalization (updatedInput)
- Safety flag additions (updatedInput)
- MCP suggestions (systemMessage)

### Must Preserve
- Existing shortcut resolution behavior
- Database event calls

### Caution
- Don't silently change major behavior
- Prefer guidance over silent modification
- Document all redirections
```

---

## Success Criteria

- [ ] updatedInput mechanism fully documented
- [ ] At least 4 redirection patterns documented
- [ ] Guidance vs silent redirect decision matrix
- [ ] MCP integration patterns
- [ ] Existing shortcut_resolver.py analyzed
- [ ] Copy-paste-ready code templates

---

## DO NOT

- ❌ Implement anything - research only
- ❌ Suggest breaking existing shortcut resolution
- ❌ Suggest silent redirects for major changes
- ❌ Skip the shortcut_resolver.py analysis
