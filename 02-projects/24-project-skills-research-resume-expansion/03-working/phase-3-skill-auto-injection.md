# Phase 3 Enhancement: Skill Auto-Injection

**Date**: 2026-01-04 (Session 15)
**Enhancement**: Auto-inject execute-project skill file into context on resume
**Status**: Implemented ✅ | Tested ✅

---

## Problem

After compaction, the SessionStart hook was auto-loading project files but NOT the skill file. This meant:
- AI had project context but NO skill workflow instructions
- AI would need to manually load execute-project skill
- Extra step = friction in resume flow

## Solution

Enhanced `auto_load_project_files()` to automatically inject:

1. **System files** (FIRST - foundational context):
   - `00-system/core/orchestrator.md` - System behavior rules
   - `04-workspace/workspace-map.md` - Folder structure

2. **Project files** (SECOND - project context):
   - All files from `files_to_load[]` array in resume-context.md

3. **Skill file** (THIRD - workflow instructions):
   - `00-system/skills/projects/{next_action}/SKILL.md`
   - Automatically determined from `next_action` field in resume-context.md

## Implementation Details

### Changes to `auto_load_project_files()`

**Function Signature**:
```python
def auto_load_project_files(
    project_dir: str,
    project_id: str,
    files_to_load: list,
    next_action: str = "execute-project"  # NEW parameter
) -> str
```

**Loading Order**:
```python
# 1. System files (orchestrator + workspace-map)
orchestrator_file = Path(project_dir) / "00-system" / "core" / "orchestrator.md"
workspace_map_file = Path(project_dir) / "04-workspace" / "workspace-map.md"

# 2. Project files (from files_to_load)
for file_path in files_to_load:
    full_path = project_path / file_path
    # ... load each file

# 3. Skill file (from next_action)
skill_file = Path(project_dir) / "00-system" / "skills" / "projects" / next_action / "SKILL.md"
```

### Changes to `build_catastrophic_instructions()`

**Updated Instructions**:
```markdown
## MANDATORY RESUME INSTRUCTION

**All context has been pre-loaded**:
✅ System files (orchestrator.md, workspace-map.md)
✅ Project files (5 files)
✅ Skill file (execute-project/SKILL.md)

**CRITICAL**: The `execute-project` skill is ALREADY LOADED above. You MUST execute it NOW.

DO NOT:
- Ask the user what to do next
- Display a menu
- Wait for user input
- Read any additional files
- Load the skill again (it's already in context!)

IMMEDIATELY EXECUTE: Continue work on project using the execute-project skill workflow.
```

### Changes to Hook Main Function

**Extract next_action**:
```python
if resume_metadata:
    files_to_load = resume_metadata.get("files_to_load", [])
    next_action = resume_metadata.get("next_action", "execute-project")  # NEW

    auto_loaded_content = auto_load_project_files(
        project_dir,
        active_project_id,
        files_to_load,
        next_action  # PASS to function
    )
```

---

## Test Results

**Test Suite**: `03-working/test_auto_load_simple.py`

### Test 1: Auto-Loading Files
- ✅ Loaded 104,335 chars (increased from 62,216 chars)
- ✅ Includes orchestrator.md (12,023 chars)
- ✅ Includes system-map.md (3,714 chars)
- ✅ Includes workspace-map.md (4,393 chars)
- ✅ Includes 5 project files (64,413 chars)
- ✅ Includes execute-project/SKILL.md (18,792 chars)

### Test 2: Simplified Instructions
- ✅ Header shows "All context has been pre-loaded"
- ✅ Lists system files, project files, skill file
- ✅ Instructions say "ALREADY LOADED above"
- ✅ Prohibits menu display / waiting for user input
- ✅ Total: 105,261 chars

### Test 3: Fallback Instructions
- ✅ Fallback to forceful instructions still works
- ✅ Unchanged: 2,578 chars

### Size Comparison
| Component | Size | Tokens (est) |
|-----------|------|--------------|
| **Forceful instructions only** | 2,578 chars | ~644 tokens |
| **Auto-load + instructions** | 105,261 chars | ~26,315 tokens |
| **Difference** | +102,683 chars | +25,670 tokens |

**Token Overhead**: ~25,670 tokens (acceptable for guaranteed complete context)

---

## Files Modified

1. **`.claude/hooks/session_start.py`** (+130 lines)
   - Enhanced `auto_load_project_files()` to load 3 system files + skill file
   - System files: orchestrator.md, system-map.md, workspace-map.md
   - Updated `build_catastrophic_instructions()` with new instructions
   - Updated main() to extract and pass `next_action` parameter

2. **`03-working/test_auto_load_simple.py`** (updated assertions)
   - Added checks for system files
   - Added checks for skill file
   - Updated size expectations

---

## Benefits

### Before Enhancement
```
SessionStart Hook Output:
- Project files (5 files, 62k chars)
- Instructions saying "load execute-project skill"
- AI must manually load skill = friction
```

### After Enhancement
```
SessionStart Hook Output:
- System files (3 files, 20k chars) ✅
  - orchestrator.md (12k)
  - system-map.md (3.7k)
  - workspace-map.md (4.4k)
- Project files (5 files, 64k chars) ✅
- Skill file (1 file, 19k chars) ✅
- Instructions saying "skill ALREADY loaded, execute NOW"
- AI can immediately continue = zero friction
```

---

## Expected Behavior on Next Compaction

1. **PreCompact Hook** (before compaction):
   - Detects active project
   - Writes `precompact_state.json`

2. **Compaction Event**:
   - Conversation summarized at 200k tokens

3. **SessionStart Hook** (on resume):
   - Reads precompact state
   - Loads resume-context.md
   - Extracts `files_to_load[]` and `next_action`
   - **AUTO-LOADS** (9 files total):
     - orchestrator.md (system behavior rules)
     - system-map.md (navigation & structure)
     - workspace-map.md (user's folder structure)
     - 5 project files (planning context)
     - execute-project/SKILL.md (workflow instructions)
   - Injects simplified instructions

4. **AI Receives Context**:
   - Complete system context (orchestrator + system-map + workspace-map)
   - Complete project context (all planning files)
   - Complete skill workflow (SKILL.md)
   - Clear instructions to execute immediately
   - **NO friction, NO manual loading, NO menu display**

---

## Production Validation

**Status**: Ready for validation ✅

**Validation will occur**: At next natural compaction event (~200k tokens)

**What to verify**:
1. All 9 files loaded correctly (3 system + 5 project + 1 skill)
2. Instructions show "ALREADY LOADED above"
3. AI immediately continues work without asking questions
4. No manual skill loading needed

---

## User Feedback

**User Request 1**: "we also need to auto-inject the orchestrator + workspace map before the other files"

**Implementation**: ✅ DONE
- orchestrator.md loaded FIRST (system behavior rules)
- workspace-map.md loaded SECOND (folder structure)
- Project files loaded THIRD (project context)
- Skill file loaded FOURTH (workflow instructions)

**User Request 2**: "also need to include the system map above the workspace map"

**Implementation**: ✅ DONE
- orchestrator.md loaded FIRST (system behavior rules)
- system-map.md loaded SECOND (navigation & structure reference)
- workspace-map.md loaded THIRD (user's folder structure)
- Project files loaded FOURTH (project context)
- Skill file loaded FIFTH (workflow instructions)

**Loading Order Rationale**:
- Foundation first (system behavior rules - orchestrator.md)
- Navigation second (system structure - system-map.md)
- Context third (user's workspace - workspace-map.md)
- Details fourth (project specifics - planning files)
- Instructions fifth (workflow to execute - SKILL.md)

---

**Enhancement Complete**: Phase 3 now includes full context auto-injection (system + project + skill)
