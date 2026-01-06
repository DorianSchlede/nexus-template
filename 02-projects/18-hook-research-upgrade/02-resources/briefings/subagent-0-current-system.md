# Subagent Briefing: Current Hook System Analysis

**Priority**: CRITICAL (must run first)
**Output Path**: `02-projects/18-hook-research-upgrade/02-resources/research-current-system.md`

---

## Mission

Analyze the ENTIRE current Nexus hook system. Document what each file does, how they connect, and what data flows to the database. This is critical because WE MUST NOT BREAK the existing system - it's connected to a live database.

---

## Required Reading (READ EVERY FILE COMPLETELY)

### Main Hook Files (`.claude/hooks/`)

Read in this order:

1. **session_start.py** (7.6KB)
   ```
   READ: .claude/hooks/session_start.py
   ```
   Questions to answer:
   - What triggers this hook?
   - What does it load?
   - What events does it send to the database?

2. **pre_tool_use.py** (11.8KB)
   ```
   READ: .claude/hooks/pre_tool_use.py
   ```
   Questions to answer:
   - What checks does it perform?
   - What does it block?
   - What events does it send?

3. **post_tool_use.py** (1.3KB)
   ```
   READ: .claude/hooks/post_tool_use.py
   ```

4. **user_prompt_submit.py** (3.3KB)
   ```
   READ: .claude/hooks/user_prompt_submit.py
   ```

5. **stop.py** (6.8KB)
   ```
   READ: .claude/hooks/stop.py
   ```

6. **subagent_stop.py** (4.8KB)
   ```
   READ: .claude/hooks/subagent_stop.py
   ```

7. **notification.py** (4.2KB)
   ```
   READ: .claude/hooks/notification.py
   ```

8. **send_event.py** (4.5KB) - CRITICAL for database connection
   ```
   READ: .claude/hooks/send_event.py
   ```

9. **save_resume_state.py** (6.7KB)
   ```
   READ: .claude/hooks/save_resume_state.py
   ```

10. **session_end.py** (4.9KB)
    ```
    READ: .claude/hooks/session_end.py
    ```

11. **session_summary.py** (5.9KB)
    ```
    READ: .claude/hooks/session_summary.py
    ```

12. **shortcut_resolver.py** (14.8KB)
    ```
    READ: .claude/hooks/shortcut_resolver.py
    ```

13. **stream_claude_message.py** (4.6KB)
    ```
    READ: .claude/hooks/stream_claude_message.py
    ```

### Utility Files (`.claude/hooks/utils/`)

14. **http.py** (1.4KB) - Database connection
    ```
    READ: .claude/hooks/utils/http.py
    ```

15. **server.py** (3.2KB)
    ```
    READ: .claude/hooks/utils/server.py
    ```

16. **registry.py** (5.7KB)
    ```
    READ: .claude/hooks/utils/registry.py
    ```

17. **constants.py** (0.9KB)
    ```
    READ: .claude/hooks/utils/constants.py
    ```

18. **summarizer.py** (1.9KB)
    ```
    READ: .claude/hooks/utils/summarizer.py
    ```

---

## Output Format

Create `research-current-system.md` at:
```
02-projects/18-hook-research-upgrade/02-resources/research-current-system.md
```

Structure:

```markdown
# Current Nexus Hook System Analysis

## Executive Summary
[2-3 sentences: What is this system? What does it do?]

---

## System Architecture

### Data Flow Diagram
\`\`\`
[ASCII diagram showing how hooks connect and where data flows]
\`\`\`

### Database Connection
- **Endpoint**: [URL from http.py or constants.py]
- **Events Sent**: [List all event types]
- **Protocol**: [HTTP POST? Fire-and-forget?]

---

## Hook File Analysis

### 1. session_start.py
**Trigger**: [When does this run?]
**Purpose**: [What does it do?]
**Database Events**:
- Event: `/api/v2/sessions/{id}/start`
- Payload: `{...}`
**Dependencies**: [What other files does it use?]
**Key Functions**:
- `function_name()`: [What it does]

### 2. pre_tool_use.py
**Trigger**: [When does this run?]
**Purpose**: [What does it do?]
**Current Safety Checks**:
- [x] Check 1
- [x] Check 2
**Database Events**:
- Event: [...]
**Exit Codes**:
- 0 = allow
- 2 = block

[... repeat for all 13 hook files ...]

---

## Utility Analysis

### http.py - Database Connection
**Server URL**: [From constants or env]
**Timeout**: [Value]
**Error Handling**: [What happens on failure?]

### send_event.py - Event Dispatcher
**Event Types Supported**:
1. `/api/v2/sessions/{id}/start`
2. `/api/v2/sessions/{id}/tool_use`
3. [... list all endpoints]

---

## Critical Paths (DO NOT BREAK)

### Database Event Flow
1. Hook triggers
2. Calls send_event.py
3. Uses http.py to POST to server
4. Server URL: [...]

### Files That Send to Database
- [ ] session_start.py → YES/NO
- [ ] pre_tool_use.py → YES/NO
- [ ] send_event.py → YES
- [... for each file]

---

## Integration Points

### With nexus-loader.py
- session_start.py calls nexus-loader.py to get context
- [Other connections]

### With External Server
- [What server? What data?]

---

## Recommendations for Safe Upgrades

### Safe to Modify
- [Files that don't touch database]

### Dangerous to Modify
- [Files that send to database - need careful testing]

### Must Preserve
- All `/api/v2/` endpoint calls
- Fire-and-forget pattern in http.py
- Exit code conventions (0=allow, 2=block)
```

---

## Success Criteria

- [ ] All 13 hook files documented
- [ ] All 5 utility files documented
- [ ] Database connection fully mapped
- [ ] All event types listed with payloads
- [ ] Clear "safe to modify" vs "dangerous" classification
- [ ] Data flow diagram showing database connection

---

## CRITICAL WARNINGS

- ⚠️ DO NOT suggest removing any database calls
- ⚠️ DO NOT suggest changing event payloads
- ⚠️ Document EVERYTHING that touches the database
- ⚠️ This analysis is prerequisite for all other subagents
