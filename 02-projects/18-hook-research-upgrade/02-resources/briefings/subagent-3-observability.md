# Subagent Briefing: Observability Research

**Priority**: MEDIUM
**Output Path**: `02-projects/18-hook-research-upgrade/02-resources/research-observability.md`

---

## Mission

Understand observability patterns in Claude Code hooks: event streaming, statusline, token metrics, notifications. Analyze how to extend the existing Nexus event system WITHOUT breaking database connections.

---

## Required Reading (IN ORDER - READ EVERYTHING)

### Step 1: Understand Research Structure
```
READ: 04-workspace/00-ai-native-org/hook-research/_index.md
```
Navigation hub.

### Step 2: Pattern Catalog Overview
```
READ: 04-workspace/00-ai-native-org/hook-research/HOOK_PATTERN_CATALOG.md
```
Executive summary, Top 10 patterns - good for overview.

### Step 3: Statusline (High-Performance Go)
```
READ: 04-workspace/00-ai-native-org/hook-research/patterns/cc-tools-go.yaml
```
Statusline implementation in Go. Token metrics extraction.

### Step 4: Notification Patterns
```
READ: 04-workspace/00-ai-native-org/hook-research/hook-guides/NOTIFICATION.md
```
Desktop alerts, TTS, sound patterns.

### Step 5: Architech Hook System Reference
```
READ: 04-workspace/00-ai-native-org/hook-system-reference.system.doc.md
```
**LARGE (44KB) - Focus on Section 6: Pre-Tool-Use Hook**
Contains:
- Executable detection
- Event streaming
- Fire-and-forget pattern

---

## Current Nexus System (FOR COMPARISON)

### Current Event Streaming
```
READ: .claude/hooks/send_event.py
```
What events does Nexus send? What endpoints?

### HTTP Utilities
```
READ: .claude/hooks/utils/http.py
```
Fire-and-forget pattern. Server URL.

### Server Management
```
READ: .claude/hooks/utils/server.py
```
How is the event server managed?

---

## Output Format

Create file at:
```
02-projects/18-hook-research-upgrade/02-resources/research-observability.md
```

Structure:

```markdown
# Observability Research Results

## Executive Summary
[2-3 sentences: What observability patterns exist?]

---

## 1. Event Types to Stream

### 1.1 Tool Call Events
**What**: Every tool call is logged
**Payload**:
\`\`\`json
{
    "type": "tool_call",
    "tool_name": "Bash",
    "tool_input": {...},
    "timestamp": "...",
    "session_id": "..."
}
\`\`\`
**Nexus uses this?**: [Yes/No, how?]

### 1.2 Block Events
**What**: When a tool call is blocked
**Payload**:
\`\`\`json
{
    "type": "block",
    "reason": "rm -rf detected",
    "tool_name": "Bash",
    "command": "...",
    "timestamp": "..."
}
\`\`\`
**Nexus uses this?**: [Yes/No]
**Should add?**: [Yes/No with reasoning]

### 1.3 Executable Detection Events
**What**: When agent/skill/task is activated
**Payload** (from Architech):
\`\`\`json
{
    "type": "agent|skill|task|workflow",
    "executable_id": "meta-architect",
    "target": "file_path",
    "shortcut": "~meta-architect",
    "detection_method": "bash|read"
}
\`\`\`

---

## 2. Current Nexus Event System

### Endpoints Currently Used
[List all /api/v2/... endpoints from send_event.py]

### Event Types Currently Sent
[List all event types]

### Fire-and-Forget Pattern
\`\`\`python
[Current implementation from http.py]
\`\`\`

---

## 3. Statusline Pattern

### Concept
Shows in console:
- Token usage (input/output/cached)
- Git branch + status
- Current context info

### Implementation (from cc-tools-go.yaml)
\`\`\`go
// Token metrics from transcript
func getTokenMetrics(transcriptPath string) TokenMetrics {
    // Parse JSONL transcript
    // Sum up usage.InputTokens, usage.OutputTokens
    // Return totals
}
\`\`\`

### Python Equivalent
\`\`\`python
def get_token_metrics(transcript_path: str) -> dict:
    """Extract token usage from transcript JSONL."""
    metrics = {"input": 0, "output": 0, "cached": 0}

    with open(transcript_path) as f:
        for line in f:
            msg = json.loads(line)
            usage = msg.get("message", {}).get("usage", {})
            if usage:
                metrics["input"] += usage.get("input_tokens", 0)
                metrics["output"] += usage.get("output_tokens", 0)
                metrics["cached"] += usage.get("cache_read_input_tokens", 0)

    return metrics
\`\`\`

### Display Format
\`\`\`
[main ✓] 45.2k in / 12.3k out / 8.1k cached | Project: ontologies-research
\`\`\`

---

## 4. Notification Patterns

### Desktop Notifications
\`\`\`python
# Using plyer or native OS commands
def notify(title: str, message: str):
    # macOS: osascript
    # Windows: PowerShell
    # Linux: notify-send
\`\`\`

### TTS (Text-to-Speech)
**Use Case**: "Task complete" announcement
**Providers** (from research):
1. macOS `say` command
2. Windows SAPI
3. espeak (Linux)
4. Edge TTS (online)

---

## 5. Recommended Extensions

### 5.1 Block Event Logging (NEW)
**Purpose**: Track all blocked operations
**Implementation**:
\`\`\`python
def send_block_event(reason: str, tool_name: str, details: dict):
    send_to_server("/api/v2/blocks", {
        "reason": reason,
        "tool_name": tool_name,
        "details": details,
        "timestamp": datetime.now().isoformat()
    })
\`\`\`
**Database Impact**: New endpoint, additive

### 5.2 Token Metrics (NEW)
**Purpose**: Track context usage
**Implementation**:
\`\`\`python
[Code template]
\`\`\`
**Database Impact**: [Analyze]

### 5.3 Audit Trail (NEW)
**Purpose**: Local log of all blocked commands
**Implementation**:
\`\`\`python
def write_audit_log(event: dict):
    log_path = Path.home() / ".nexus" / "audit" / f"{session_id}.jsonl"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with open(log_path, "a") as f:
        f.write(json.dumps(event) + "\n")
\`\`\`
**Database Impact**: None - local only

---

## 6. Integration Notes

### Must Preserve
- All existing send_to_server() calls
- All existing endpoints (/api/v2/sessions/...)
- Fire-and-forget pattern (never block on network)
- Error handling (silent failure)

### Safe to Add
- New event types (additive)
- Local audit logging
- Statusline (stdout only)
```

---

## Success Criteria

- [ ] All event types documented with payloads
- [ ] Statusline pattern understood with Python equivalent
- [ ] Fire-and-forget pattern documented
- [ ] Integration plan with existing send_event.py
- [ ] Copy-paste-ready code templates
- [ ] All existing database calls documented as MUST PRESERVE

---

## DO NOT

- ❌ Implement anything - research only
- ❌ Focus only on Go code - we need Python
- ❌ Skip Architech Reference - Section 6 is important!
- ❌ Suggest replacing existing event calls
- ❌ Suggest blocking on network operations
