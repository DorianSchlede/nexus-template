# PreCompact Hook Guide

> Comprehensive guide for the PreCompact hook event in Claude Code

---

## 1. Overview

### What This Hook Does

The **PreCompact** hook fires immediately before Claude Code performs context compaction (summarization). Context compaction occurs when the conversation grows too long and needs to be condensed to fit within the model's context window. This hook provides an opportunity to:

- Log compaction events for debugging and analytics
- Back up the full transcript before summarization
- Track whether compaction was triggered manually or automatically
- Provide verbose feedback about the compaction process

### When It Fires (Trigger Conditions)

The PreCompact hook is triggered in two scenarios:

| Trigger Type | Description |
|--------------|-------------|
| `auto` | Automatic compaction when context approaches the model's limit |
| `manual` | User-initiated compaction via `/compact` command |

### Can It Block?

**No** - PreCompact is a notification-only hook. It cannot block or prevent the compaction from occurring. The hook runs synchronously before compaction begins, but its response does not affect whether compaction proceeds.

### JSON Input Schema

```json
{
  "session_id": "string",
  "transcript_path": "string",
  "hook_event_name": "PreCompact",
  "trigger": "manual" | "auto"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `session_id` | `string` | Unique identifier for the current session |
| `transcript_path` | `string` | Absolute path to the transcript JSONL file |
| `hook_event_name` | `"PreCompact"` | Always "PreCompact" for this hook |
| `trigger` | `"manual"` \| `"auto"` | What initiated the compaction |

### JSON Output Schema (Valid Responses)

PreCompact hooks can return the following response structure:

```json
{
  "continue": true,
  "stopReason": "string (optional)",
  "suppressOutput": false,
  "decision": "approve" | "block (optional)",
  "reason": "string (optional)"
}
```

**Note**: While the schema supports `decision: "block"`, PreCompact hooks **cannot actually block** compaction. The decision field is present for API consistency but has no effect on compaction execution.

| Field | Type | Effect |
|-------|------|--------|
| `continue` | `boolean` | Whether to continue (informational only) |
| `stopReason` | `string` | Reason if stopping (no effect on compaction) |
| `suppressOutput` | `boolean` | Whether to suppress hook output display |
| `decision` | `string` | `"approve"` or `"block"` (no blocking effect) |
| `reason` | `string` | Explanation message |

---

## 2. Pattern Catalog

### Pattern: Pre-Compact Event Logging

**Sources**: hooks-mastery-session, hooks-mastery-part2, claude-hooks (TypeScript SDK)

**Description**: Logs context compaction events with trigger type differentiation, providing observability into when and why compaction occurs. This is the foundational PreCompact pattern used for debugging and session analytics.

**Decision Type**: None (observation only)

**Implementation (Bash - Simple)**:
```bash
#!/bin/bash
# pre-compact-logger.sh
# Simple PreCompact event logger

input=$(cat)
trigger=$(echo "$input" | jq -r '.trigger')
session_id=$(echo "$input" | jq -r '.session_id')
timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

echo "[$timestamp] PreCompact triggered: $trigger (session: $session_id)" >&2

# Return empty response - cannot block
echo '{}'
```

**Implementation (TypeScript - Bun)**:
```typescript
import type { PreCompactHandler, PreCompactPayload } from './lib'

const preCompact: PreCompactHandler = async (payload: PreCompactPayload) => {
  console.log(`Compact triggered: ${payload.trigger}`)

  if (payload.trigger === 'auto') {
    console.log('Allowing automatic compaction')
  } else {
    console.log('Manual compaction initiated by user')
  }

  return {} // Empty object means continue normally
}
```

**Implementation (Python)**:
```python
#!/usr/bin/env python3
import json
import sys
from datetime import datetime

def handle_pre_compact():
    input_data = json.loads(sys.stdin.read())

    trigger = input_data.get('trigger', 'unknown')
    session_id = input_data.get('session_id', 'unknown')
    timestamp = datetime.utcnow().isoformat()

    print(f"[{timestamp}] PreCompact: trigger={trigger}, session={session_id}",
          file=sys.stderr)

    # Return empty response
    print(json.dumps({}))

if __name__ == '__main__':
    handle_pre_compact()
```

**Pros**:
- Minimal overhead (<10ms execution)
- Provides visibility into compaction frequency
- Helps diagnose context pressure issues
- Simple implementation across all languages

**Cons**:
- Cannot prevent compaction
- Limited actionable intervention
- Logs may be missed in high-volume sessions

**Use When**:
- Debugging context window issues
- Building session analytics dashboards
- Tracking compaction frequency patterns
- Correlating compaction with user activities

**Avoid When**:
- You need to prevent compaction (not possible)
- Logging overhead is a concern in performance-critical environments

---

### Pattern: Transcript Backup Before Compaction

**Sources**: hooks-mastery-session, hooks-mastery-part2

**Description**: Creates a timestamped backup of the full transcript JSONL before compaction summarizes it. Preserves complete conversation history for later analysis, compliance, or recovery.

**Decision Type**: None (observation only)

**Implementation (Bash)**:
```bash
#!/bin/bash
# pre-compact-backup.sh
# Back up transcript before compaction

input=$(cat)
transcript_path=$(echo "$input" | jq -r '.transcript_path')
session_id=$(echo "$input" | jq -r '.session_id')
trigger=$(echo "$input" | jq -r '.trigger')

# Create backup directory
backup_dir="$HOME/.claude/backups/pre-compact"
mkdir -p "$backup_dir"

# Generate timestamped backup filename
timestamp=$(date +"%Y%m%d_%H%M%S")
backup_file="$backup_dir/${session_id}_${timestamp}_${trigger}.jsonl"

# Copy transcript to backup
if [ -f "$transcript_path" ]; then
    cp "$transcript_path" "$backup_file"
    echo "Transcript backed up to: $backup_file" >&2

    # Optional: Compress old backups
    find "$backup_dir" -name "*.jsonl" -mtime +7 -exec gzip {} \;
else
    echo "Warning: Transcript not found at $transcript_path" >&2
fi

echo '{}'
```

**Implementation (TypeScript)**:
```typescript
import { copyFile, mkdir } from 'fs/promises'
import { existsSync } from 'fs'
import { join } from 'path'
import { homedir } from 'os'

interface PreCompactPayload {
  session_id: string
  transcript_path: string
  trigger: 'manual' | 'auto'
}

async function backupTranscript(payload: PreCompactPayload): Promise<void> {
  const backupDir = join(homedir(), '.claude', 'backups', 'pre-compact')
  await mkdir(backupDir, { recursive: true })

  const timestamp = new Date().toISOString().replace(/[:.]/g, '-')
  const backupFile = join(
    backupDir,
    `${payload.session_id}_${timestamp}_${payload.trigger}.jsonl`
  )

  if (existsSync(payload.transcript_path)) {
    await copyFile(payload.transcript_path, backupFile)
    console.error(`Transcript backed up: ${backupFile}`)
  }
}

// Main handler
const input = await Bun.stdin.text()
const payload: PreCompactPayload = JSON.parse(input)
await backupTranscript(payload)
console.log(JSON.stringify({}))
```

**Implementation (Python)**:
```python
#!/usr/bin/env python3
import json
import sys
import shutil
import gzip
from pathlib import Path
from datetime import datetime

def backup_transcript():
    input_data = json.loads(sys.stdin.read())

    transcript_path = Path(input_data['transcript_path'])
    session_id = input_data['session_id']
    trigger = input_data['trigger']

    # Create backup directory
    backup_dir = Path.home() / '.claude' / 'backups' / 'pre-compact'
    backup_dir.mkdir(parents=True, exist_ok=True)

    # Generate backup filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = backup_dir / f"{session_id}_{timestamp}_{trigger}.jsonl"

    # Copy transcript
    if transcript_path.exists():
        shutil.copy2(transcript_path, backup_file)
        print(f"Backed up to: {backup_file}", file=sys.stderr)

        # Compress backups older than 7 days
        for old_backup in backup_dir.glob('*.jsonl'):
            age_days = (datetime.now() - datetime.fromtimestamp(old_backup.stat().st_mtime)).days
            if age_days > 7:
                with open(old_backup, 'rb') as f_in:
                    with gzip.open(f"{old_backup}.gz", 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                old_backup.unlink()

    print(json.dumps({}))

if __name__ == '__main__':
    backup_transcript()
```

**Pros**:
- Preserves complete conversation history before summarization
- Enables post-hoc analysis and debugging
- Supports compliance/audit requirements
- Automatic cleanup of old backups prevents disk bloat

**Cons**:
- Adds I/O latency to compaction process (10-50ms)
- Disk space consumption for large transcripts
- Requires periodic backup management

**Use When**:
- Compliance requires full conversation logs
- Debugging summarization quality issues
- Training data collection for model improvement
- Session recovery/replay needs

**Avoid When**:
- Disk space is severely limited
- Minimal latency is critical
- Transcripts contain sensitive data that shouldn't persist

---

### Pattern: Pre-Compact Verbose Feedback

**Sources**: hooks-mastery-session, hooks-mastery-part2

**Description**: Provides detailed statistics about the transcript before compaction, including message counts, token estimates, and context pressure metrics. Useful for understanding why compaction was triggered and what will be summarized.

**Decision Type**: None (observation only)

**Implementation (Bash)**:
```bash
#!/bin/bash
# pre-compact-stats.sh
# Provide verbose transcript statistics before compaction

input=$(cat)
transcript_path=$(echo "$input" | jq -r '.transcript_path')
trigger=$(echo "$input" | jq -r '.trigger')

if [ -f "$transcript_path" ]; then
    # Count messages by type
    total_lines=$(wc -l < "$transcript_path")
    user_msgs=$(grep -c '"type":"user"' "$transcript_path" 2>/dev/null || echo 0)
    assistant_msgs=$(grep -c '"type":"assistant"' "$transcript_path" 2>/dev/null || echo 0)
    tool_uses=$(grep -c '"tool_use"' "$transcript_path" 2>/dev/null || echo 0)

    # Estimate file size
    file_size=$(du -h "$transcript_path" | cut -f1)

    cat >&2 << EOF
=== PreCompact Statistics ===
Trigger: $trigger
Transcript: $transcript_path
File Size: $file_size
Total Lines: $total_lines
User Messages: $user_msgs
Assistant Messages: $assistant_msgs
Tool Uses: $tool_uses
=============================
EOF
fi

echo '{}'
```

**Implementation (TypeScript)**:
```typescript
import { createReadStream, statSync } from 'fs'
import { createInterface } from 'readline'

interface TranscriptStats {
  totalLines: number
  userMessages: number
  assistantMessages: number
  toolUses: number
  summaries: number
  fileSizeBytes: number
}

async function getTranscriptStats(transcriptPath: string): Promise<TranscriptStats> {
  const stats: TranscriptStats = {
    totalLines: 0,
    userMessages: 0,
    assistantMessages: 0,
    toolUses: 0,
    summaries: 0,
    fileSizeBytes: statSync(transcriptPath).size
  }

  const fileStream = createReadStream(transcriptPath)
  const rl = createInterface({ input: fileStream, crlfDelay: Infinity })

  for await (const line of rl) {
    if (!line.trim()) continue
    stats.totalLines++

    try {
      const msg = JSON.parse(line)
      if (msg.type === 'user') stats.userMessages++
      if (msg.type === 'assistant') stats.assistantMessages++
      if (msg.type === 'summary') stats.summaries++

      // Count tool uses in assistant messages
      if (msg.message?.content) {
        const content = Array.isArray(msg.message.content)
          ? msg.message.content
          : []
        stats.toolUses += content.filter(
          (c: any) => c.type === 'tool_use'
        ).length
      }
    } catch {}
  }

  return stats
}

function formatBytes(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
}

// Main
const input = await Bun.stdin.text()
const payload = JSON.parse(input)

const stats = await getTranscriptStats(payload.transcript_path)

console.error(`
=== PreCompact Statistics ===
Trigger: ${payload.trigger}
File Size: ${formatBytes(stats.fileSizeBytes)}
Total Entries: ${stats.totalLines}
User Messages: ${stats.userMessages}
Assistant Messages: ${stats.assistantMessages}
Tool Uses: ${stats.toolUses}
Previous Summaries: ${stats.summaries}
=============================
`)

console.log(JSON.stringify({}))
```

**Pros**:
- Provides visibility into what's being compacted
- Helps diagnose context pressure patterns
- Educational for understanding Claude's context management
- Useful for optimizing prompt strategies

**Cons**:
- Adds parsing overhead (50-100ms for large transcripts)
- Output may be verbose for automated pipelines
- Statistics are approximate (tool use counting heuristics)

**Use When**:
- Debugging why compaction happens frequently
- Understanding conversation patterns
- Optimizing context usage strategies
- Development and learning environments

**Avoid When**:
- Production environments where latency matters
- Automated pipelines where output should be minimal

---

### Pattern: Session State Persistence

**Sources**: claude-hooks (TypeScript SDK)

**Description**: Saves PreCompact event data to session-specific JSON files for debugging and session replay. Provides a persistent record of all hook invocations throughout a session.

**Decision Type**: None (observation only)

**Implementation (TypeScript)**:
```typescript
import { mkdir, readFile, writeFile } from 'fs/promises'
import { tmpdir } from 'os'
import { join } from 'path'

const SESSIONS_DIR = join(tmpdir(), 'claude-hooks-sessions')

interface PreCompactPayload {
  session_id: string
  transcript_path: string
  hook_event_name: 'PreCompact'
  trigger: 'manual' | 'auto'
}

interface SessionEntry {
  timestamp: string
  hookType: string
  payload: PreCompactPayload
}

async function saveSessionData(
  hookType: string,
  payload: PreCompactPayload
): Promise<void> {
  try {
    await mkdir(SESSIONS_DIR, { recursive: true })
    const sessionFile = join(SESSIONS_DIR, `${payload.session_id}.json`)

    let sessionData: SessionEntry[] = []
    try {
      const existing = await readFile(sessionFile, 'utf-8')
      sessionData = JSON.parse(existing)
    } catch {}

    sessionData.push({
      timestamp: new Date().toISOString(),
      hookType,
      payload
    })

    await writeFile(sessionFile, JSON.stringify(sessionData, null, 2))
  } catch (error) {
    console.error('Failed to save session data:', error)
  }
}

// Handler
const preCompact = async (payload: PreCompactPayload) => {
  await saveSessionData('PreCompact', payload)
  console.log(`Compact triggered: ${payload.trigger}`)
  return {}
}
```

**Pros**:
- Creates persistent audit trail of all hook events
- Enables session replay and debugging
- Correlates PreCompact with other hook events
- Session files are human-readable JSON

**Cons**:
- Additional disk I/O per hook call
- Session files grow throughout conversation
- Requires periodic cleanup of old sessions

**Use When**:
- Building hook debugging tools
- Analyzing session patterns across hook types
- Correlating compaction with other events

**Avoid When**:
- Minimal disk I/O is required
- Privacy concerns about persisting session data

---

## 3. Inspiration Ideas

Based on the patterns found, here are novel use cases and advanced applications for PreCompact hooks:

### Context Optimization Analytics

**Concept**: Track compaction frequency and correlate with conversation patterns to optimize context usage.

```typescript
// Track compaction patterns over time
interface CompactionMetrics {
  sessionId: string
  compactionCount: number
  avgMessagesBetweenCompactions: number
  toolUseHeavySessions: boolean
  timeToFirstCompaction: number
}

// Store metrics in SQLite or JSON for analysis
// Identify patterns: "Sessions with >50 tool uses compact 3x more often"
```

### Pre-Compaction Summary Injection

**Concept**: Before compaction, generate and inject a custom summary that preserves critical context that might otherwise be lost.

```typescript
// Generate structured summary before Claude's compaction
const criticalContext = await extractCriticalContext(transcriptPath)
// Write to a "preserved context" file that SessionStart hook will inject
await writePreservedContext(sessionId, criticalContext)
```

### Compaction Notification System

**Concept**: Send notifications (desktop, Slack, webhook) when compaction occurs, especially for auto-compaction indicating context pressure.

```typescript
if (payload.trigger === 'auto') {
  await sendSlackNotification({
    channel: '#claude-alerts',
    message: `Auto-compaction triggered in session ${payload.session_id}`,
    urgency: 'warning'
  })
}
```

### Context Window Pressure Dashboard

**Concept**: Real-time dashboard showing context usage across active sessions.

```typescript
// PreCompact hook emits metrics to Prometheus/Grafana
await pushMetrics({
  metric: 'claude_compaction_total',
  labels: { trigger: payload.trigger, session: payload.session_id },
  value: 1
})
```

### Conversation Milestone Markers

**Concept**: Use compaction events as natural "chapter breaks" in long conversations. Tag transcripts with milestone markers.

```typescript
// Mark the transcript with a milestone before compaction
const milestone = {
  type: 'milestone',
  reason: 'pre-compaction',
  trigger: payload.trigger,
  timestamp: new Date().toISOString(),
  summary: await generateMilestoneSummary(transcriptPath)
}
await appendToTranscript(transcriptPath, milestone)
```

### Combination with Other Hooks

| Combination | Use Case |
|-------------|----------|
| PreCompact + SessionStart | Restore critical context after compaction |
| PreCompact + PostToolUse | Track tool usage patterns that cause compaction |
| PreCompact + Stop | Generate session report including compaction stats |
| PreCompact + UserPromptSubmit | Detect prompts that rapidly consume context |

### Advanced: Compaction Quality Verification

**Concept**: After compaction completes (via SessionStart with "resume" source), compare pre-compaction context with post-compaction summary to verify nothing critical was lost.

```typescript
// PreCompact: Save critical entities
await saveCriticalEntities(sessionId, extractEntities(transcript))

// Later in SessionStart (resume after compact):
const preserved = await loadCriticalEntities(sessionId)
const postCompact = extractEntitiesFromSummary(currentContext)
const missing = preserved.filter(e => !postCompact.includes(e))
if (missing.length > 0) {
  // Inject missing entities into context
  return { hookSpecificOutput: { additionalContext: formatMissing(missing) } }
}
```

---

## 4. Implementation Recommendations

### Best Patterns to Adopt (Ranked)

| Rank | Pattern | Rationale |
|------|---------|-----------|
| 1 | **Pre-Compact Event Logging** | Essential for observability, minimal overhead |
| 2 | **Transcript Backup** | Critical for compliance and debugging |
| 3 | **Session State Persistence** | Enables cross-hook correlation |
| 4 | **Verbose Feedback** | Useful for development, disable in production |

### Patterns to Avoid

| Pattern | Reason |
|---------|--------|
| Attempting to block compaction | PreCompact cannot block; will have no effect |
| Heavy computation before compaction | Adds latency to an already expensive operation |
| Synchronous external API calls | Risk of timeout affecting compaction |
| Writing to transcript during PreCompact | May cause race conditions |

### Performance Considerations

| Concern | Recommendation |
|---------|----------------|
| Execution Time | Target <50ms; compaction is already slow |
| I/O Operations | Prefer async writes; don't block on confirmation |
| Transcript Parsing | Use streaming (readline) for large files |
| Backup Size | Compress backups >1MB, implement retention policy |

**Benchmark Targets**:
- Simple logging: <10ms
- Transcript backup: <50ms
- Full statistics: <100ms

### Testing Approach

1. **Unit Tests**: Mock the transcript file and verify output format
```typescript
describe('PreCompact Hook', () => {
  it('should log trigger type correctly', async () => {
    const payload = { trigger: 'auto', session_id: 'test', ... }
    const result = await preCompactHandler(payload)
    expect(result).toEqual({})
    expect(logOutput).toContain('auto')
  })
})
```

2. **Integration Tests**: Trigger actual compaction via `/compact`
```bash
# Manual test: Run /compact and verify hook executes
claude code /compact
# Check hook output in stderr
```

3. **Load Tests**: Verify hook doesn't add significant latency
```typescript
// Benchmark hook execution time
const start = performance.now()
await preCompactHandler(largePayload)
const duration = performance.now() - start
expect(duration).toBeLessThan(50)
```

### Configuration Example

```json
{
  "hooks": {
    "PreCompact": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "python ~/.claude/hooks/pre-compact.py"
          }
        ]
      }
    ]
  }
}
```

**Note**: The `matcher` field is typically empty for PreCompact since there's nothing to match against (unlike PreToolUse which can match tool names).

---

## Quick Reference

| Aspect | Detail |
|--------|--------|
| **Can Block?** | No |
| **Triggers** | `manual` (user /compact), `auto` (context limit) |
| **Primary Uses** | Logging, backup, analytics |
| **Performance Target** | <50ms |
| **Key Fields** | `trigger`, `transcript_path`, `session_id` |
| **Output Effect** | Informational only; cannot affect compaction |

---

*Generated from pattern analysis of: hooks-mastery-session.yaml, hooks-mastery-part2.yaml, claude-hooks-ts.yaml*
