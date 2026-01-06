# Resume State Design - REVISED v1.3

**Purpose**: Enforce intelligent loading mechanism and validation gate after compaction
**Revision**: v1.3 - Phase 0 complete, schemas validated
**Naming**: **`resume-context.md`** (NOT `_resume.md`) - **CONFIRMED 2026-01-04**
**Migration**: 20+ existing `_resume.md` files - Migration script ready (Phase 0.6)
**Validation**: ✅ Phase 0 COMPLETE - 14/14 tests passing (100%)

---

## Core Principle

**resume-context.md is NOT a summary file. It is a LOADING MANIFEST + VALIDATION GATE.**

- ❌ NO duplication of content from other files
- ❌ NO metadata that exists elsewhere
- ✅ ONLY: What to load, in what order, validation questions
- ✅ AUTO-UPDATED: On every task completion inside execute-project

---

## Auto-Continue After Compaction Flow (CORRECTED v1.1)

### ⚠️ CRITICAL CORRECTIONS from Cross-Validation

**Original design had 3 critical architecture errors**:
1. Misunderstood hook output mechanism (hooks can't return JSON context)
2. Wrong schema structure (nested vs flat)
3. Missing session source detection

**All corrected below** ✓

---

### What Happens During Compaction (200k tokens) - CORRECTED FLOW

**CRITICAL**: Hooks drive the process, NOT nexus-loader CLI flags.

#### Step 1: PreCompact Hook Fires (BEFORE Compaction)

**Hook**: `.claude/hooks/save_resume_state.py`
**Trigger**: Claude Code fires hook before compacting conversation

**Actions**:
1. Parses transcript JSONL for active project detection
2. Identifies project from Read/Write/Edit/Bash tool calls
3. Calculates confidence score (high/medium/low)
4. Writes `00-system/.cache/precompact_state.json` with **FLAT schema**:
   ```json
   {
     "active_project_id": "24-project-...",  // FLAT (NOT nested under "project_detection")
     "confidence": "high",
     "detection_method": "transcript",
     "timestamp": "2026-01-03T14:00:00"
   }
   ```
5. **MUST return `{}`** (empty object) - PreCompact hooks CANNOT inject context via return value
6. **MUST execute in <50ms** (hook-guides requirement, NOT 500ms)
7. **MUST redact secrets** (API keys, tokens) before writing state file

**Key Architecture** (from cross-reference-agent-3):
- Hooks **RECEIVE** `source` from Claude Code (don't detect it)
- PreCompact writes state for **PROJECT detection**
- SessionStart reads state for **resume context injection**
- NO `--resume` flag needed (hooks handle everything)

#### Step 2: SessionStart Hook Fires (On Resume)

**Hook**: `.claude/hooks/session_start.py`

**Actions**:
1. Receives `source` field from Claude Code (`"resume"` or `"compact"`)
2. **Checks session source** - if `source == "clear"`, skip resume
3. Reads `precompact_state.json` with FLAT schema
4. Loads `02-projects/{active_project_id}/01-planning/resume-context.md`
5. Parses YAML frontmatter for `files_to_load[]`
6. Injects CATASTROPHIC instructions via `additionalContext`
7. **MUST execute in <200ms**

---

## resume-context.md Structure (MINIMAL - REVISED v1.1)

**Location**: `01-planning/resume-context.md` (NOT `_resume.md`)

```yaml
---
# LOADING MANIFEST
resume_schema_version: "1.0"
last_updated: "2026-01-03T15:30:00"

# PROJECT IDENTIFICATION
project_id: "24-project-skills-research-resume-expansion"
project_name: "Project Skills Research & Resume Expansion"
current_phase: execution  # research | planning | execution

# AUTO-LOAD INSTRUCTIONS
next_action: execute-project
files_to_load:
  - 01-planning/overview.md
  - 01-planning/plan.md
  - 01-planning/steps.md
  - 01-planning/research.md  # If research completed

# EXECUTION STATE (MINIMAL)
current_section: 2
current_task: 15
progress: "14/40 tasks complete"
---

# Validation Gate

Before continuing, you MUST verify you understand:

1. **Project Purpose** (from overview.md):
   - [ ] What problem are we solving?
   - [ ] What is the success criterion?

2. **Current Location** (from steps.md):
   - [ ] What phase are we in?
   - [ ] What is the next task?

3. **Approach** (from plan.md):
   - [ ] What is the implementation strategy?

**If you cannot answer these questions, STOP and re-read files_to_load.**

---

*This file is auto-updated on every task completion by execute-project skill*
```

---

## Schema Design (Phase 0 Complete ✅)

### precompact_state.json Schema (FLAT)

**✅ Validated**: Phase 0.3 - Tests 1, 2, 3, 4 passing
**Schema File**: `00-system/.schemas/precompact_state_v1.json`
**Example File**: `02-resources/examples/example-precompact-state.json`

```json
{
  "active_project_id": "string (NN-kebab-case-name)",
  "confidence": "high" | "medium" | "low",
  "detection_method": "transcript" | "cache" | "fallback",
  "timestamp": "ISO-8601 string"
}
```

**Critical Validations**:
- ✅ FLAT schema enforcement (Test 2) - `active_project_id` at top level, NOT nested
- ✅ Missing fields detection (Test 3)
- ✅ Enum validation (Test 4)
- ✅ File size < 1KB

### resume-context.md YAML Schema

**✅ Validated**: Phase 0.3 - Tests 5, 6, 7 passing
**Schema File**: `00-system/.schemas/resume_context_v1.json`
**Example File**: `02-resources/examples/example-resume-context.md`

```yaml
required: [resume_schema_version, project_id, project_name, current_phase, next_action, files_to_load, last_updated]
properties:
  resume_schema_version: string (e.g., "1.0")
  project_id: string (NN-kebab-case-name)
  project_name: string (human-readable project name)
  current_phase: "research" | "planning" | "execution" | "ready-for-implementation" | "testing" | "review"
  next_action: string (skill name)
  files_to_load: array of string (relative paths)
  current_section: integer
  current_task: integer
  progress: string (e.g., "14/40 tasks complete")
  last_updated: string (ISO-8601 timestamp)
```

**Critical Validations**:
- ✅ All 10 required fields validated (Test 5)
- ✅ Phase enum validation (Test 6)
- ✅ Backward compatibility with legacy `resume_version` (Test 7)
- ✅ Round-trip compatibility PreCompact → SessionStart (Test 1, 7)

---

## Critical Corrections Summary

| Issue | Original | Corrected | Source |
|-------|----------|-----------|--------|
| PreCompact output | Returns JSON | **MUST return `{}`** | cross-ref-agent-1 |
| Schema structure | Nested | **FLAT** | cross-ref-agent-5 |
| Performance | 500ms/2s | **<50ms/<200ms** | cross-ref-agent-5 |
| Source detection | Missing | **Check `source`, exclude "clear"** | cross-ref-agent-2 |
| Research location | 02-resources/ | **01-planning/** | Agent 4 |
| File name | _resume.md | **resume-context.md** | **User confirmed (Option B)** |
| Migration | None | **20+ projects + backward compat** | Phase 0.6 |

---

**Status**: Revised v1.2 - All critical issues + migration strategy incorporated
**Next**: Execute Phase 0.6 (Migration script), then Phase 1 (Hook implementation)
**Confidence**: HIGH (architecture validated, migration planned)
