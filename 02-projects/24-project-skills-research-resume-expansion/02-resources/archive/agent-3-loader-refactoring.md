# Agent 3: Nexus Loader Refactoring - Complete Analysis

**Mission**: Remove `--resume` flag from nexus-loader.py and simplify architecture

**Rationale**: The SessionStart hook (`session_start.py`) now provides resume context via `additionalContext`, making the `--resume` CLI flag redundant. This creates dual systems and confusion.

---

## Executive Summary

The `--resume` flag is **completely redundant** because:

1. **SessionStart hook** already detects resume mode via `source` field (`resume`, `compact`)
2. **Hook injects context** directly into Claude's initial context via `additionalContext`
3. **No CLI needed**: The hook IS the loader for session initialization
4. **Dual system problem**: Having both creates confusion and maintenance burden

**Impact**: The `--resume` flag appears in 7 locations across 4 files and affects resume mode logic throughout the codebase.

---

## 1. Complete Code Analysis

### 1.1 Files Affected

| File | Lines with `--resume` | Resume Logic | Deprecation Impact |
|------|----------------------|--------------|-------------------|
| `nexus-loader.py` | 9, 103, 132, 137, 172, 197 | CLI parsing, mode detection | HIGH - Direct removal |
| `nexus/service.py` | 58, 68, 79 | `resume_mode` parameter | MEDIUM - Keep param for backward compat |
| `nexus/state.py` | 36, 50 | State detection | LOW - Keep for hook usage |
| `session_start.py` | 182 | Hook mode detection | NONE - This is the new system |

### 1.2 Code Flow Analysis

**CURRENT (Dual System)**:
```
Session Start
    ├─> session_start.py hook (NEW)
    │   └─> Detects source=resume
    │       └─> Injects resume context to additionalContext
    └─> User runs: python nexus-loader.py --resume (OLD, REDUNDANT)
        └─> Sets resume_mode=True
            └─> Returns continue_working action
```

**PROPOSED (Single Source of Truth)**:
```
Session Start
    └─> session_start.py hook (ONLY)
        └─> Detects source=resume/compact
            └─> Injects resume context to additionalContext
            └─> Claude continues working (no CLI needed)
```

---

## 2. Detailed Code Changes

### 2.1 File: `nexus-loader.py`

**Lines to Remove/Modify**:

#### Line 9 (Documentation)
```diff
- python nexus-loader.py --resume            # Resume from context summary
```

#### Line 103 (Argument Parser)
```diff
- parser.add_argument('--resume', action='store_true', help='Resume after context summary (skip menu, continue working)')
+ # DEPRECATED v4.1: --resume flag removed. Use session_start.py hook for resume context.
```

#### Lines 132-139 (Main Logic)
```diff
- elif args.startup or args.resume:
+ elif args.startup:
      include_metadata = not args.no_metadata
      check_updates = not args.skip_update_check
      result = service.startup(
          include_metadata=include_metadata,
-         resume_mode=args.resume,
+         resume_mode=False,  # Deprecated: resume handled by session_start.py hook
          check_updates=check_updates
      )
```

#### Line 172 (Cache Detection)
```diff
- is_startup_command = args.startup or args.resume
+ is_startup_command = args.startup
```

#### Line 197 (Mode String)
```diff
- mode = "resume" if args.resume else "startup"
+ mode = "startup"
```

**COMPLETE DIFF for nexus-loader.py main()**:

```python
# BEFORE (Lines 91-153)
def main():
    # Configure UTF-8 output for Windows console
    if sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')

    # DYNAMIC BASE PATH DETECTION
    detected_nexus_root = SCRIPT_DIR.parent.parent

    parser = argparse.ArgumentParser(description="Nexus-v4 Context Loader")
    parser.add_argument('--startup', action='store_true', help='Load startup context with embedded memory files')
    parser.add_argument('--resume', action='store_true', help='Resume after context summary (skip menu, continue working)')  # ← REMOVE
    parser.add_argument('--skip-update-check', action='store_true', help='Skip update check during startup (faster startup)')
    # ... other arguments ...

    args = parser.parse_args()
    service = NexusService(args.base_path)

    # Execute command
    if args.check_update:
        result = service.check_updates()
    elif args.sync:
        result = service.sync(dry_run=args.dry_run, force=args.force)
    elif args.startup or args.resume:  # ← CHANGE
        include_metadata = not args.no_metadata
        check_updates = not args.skip_update_check
        result = service.startup(
            include_metadata=include_metadata,
            resume_mode=args.resume,  # ← REMOVE
            check_updates=check_updates
        )
    # ... rest of logic ...

    is_startup_command = args.startup or args.resume  # ← CHANGE
    if output_chars > BASH_OUTPUT_LIMIT and is_startup_command:
        # ... cache logic ...
        mode = "resume" if args.resume else "startup"  # ← CHANGE
```

```python
# AFTER (Lines 91-153)
def main():
    # Configure UTF-8 output for Windows console
    if sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')

    # DYNAMIC BASE PATH DETECTION
    detected_nexus_root = SCRIPT_DIR.parent.parent

    parser = argparse.ArgumentParser(description="Nexus-v4 Context Loader")
    parser.add_argument('--startup', action='store_true', help='Load startup context with embedded memory files')
    # DEPRECATED v4.1: --resume flag removed. Session resume is handled automatically by session_start.py hook.
    parser.add_argument('--skip-update-check', action='store_true', help='Skip update check during startup (faster startup)')
    # ... other arguments ...

    args = parser.parse_args()
    service = NexusService(args.base_path)

    # Execute command
    if args.check_update:
        result = service.check_updates()
    elif args.sync:
        result = service.sync(dry_run=args.dry_run, force=args.force)
    elif args.startup:
        include_metadata = not args.no_metadata
        check_updates = not args.skip_update_check
        result = service.startup(
            include_metadata=include_metadata,
            resume_mode=False,  # Deprecated: resume handled by session_start.py hook
            check_updates=check_updates
        )
    # ... rest of logic ...

    is_startup_command = args.startup
    if output_chars > BASH_OUTPUT_LIMIT and is_startup_command:
        # ... cache logic ...
        mode = "startup"
```

---

### 2.2 File: `nexus/service.py`

**Lines to Modify**: 55-60, 68-70, 79

**IMPORTANT**: Keep `resume_mode` parameter for backward compatibility (Python imports), but deprecate it.

```python
# BEFORE (Lines 55-79)
def startup(
    self,
    include_metadata: bool = True,
    resume_mode: bool = False,
    check_updates: bool = True,
) -> Dict[str, Any]:
    """
    Load startup context and determine complete execution plan.

    This is the MASTER CONTROLLER for Nexus startup.
    Analyzes system state and returns EXACTLY what the AI should do.

    Args:
        include_metadata: If True, include full project/skill metadata
        resume_mode: If True, skip menu display (resuming from context summary)
        check_updates: If True, check for upstream updates

    Returns:
        Complete startup result with state, instructions, memory, and metadata
    """
    # ATTENTION OPTIMIZATION: Instructions at START for primacy effect
    # They will also be repeated at END for recency effect (see below)
    result = {
        "loaded_at": datetime.now().isoformat(),
        "bundle": "resume" if resume_mode else "startup",
        # ... rest of result ...
    }
```

```python
# AFTER (Lines 55-79)
def startup(
    self,
    include_metadata: bool = True,
    resume_mode: bool = False,  # DEPRECATED v4.1: Ignored. Resume handled by session_start.py hook.
    check_updates: bool = True,
) -> Dict[str, Any]:
    """
    Load startup context and determine complete execution plan.

    This is the MASTER CONTROLLER for Nexus startup.
    Analyzes system state and returns EXACTLY what the AI should do.

    Args:
        include_metadata: If True, include full project/skill metadata
        resume_mode: DEPRECATED v4.1 - This parameter is ignored.
                     Resume mode is automatically handled by session_start.py hook
                     via additionalContext injection.
        check_updates: If True, check for upstream updates

    Returns:
        Complete startup result with state, instructions, memory, and metadata
    """
    # ATTENTION OPTIMIZATION: Instructions at START for primacy effect
    # They will also be repeated at END for recency effect (see below)

    # DEPRECATION NOTICE: resume_mode parameter is ignored
    # Resume context is now injected by session_start.py hook
    if resume_mode:
        import warnings
        warnings.warn(
            "resume_mode parameter is deprecated and ignored. "
            "Resume context is automatically injected by session_start.py hook.",
            DeprecationWarning,
            stacklevel=2
        )

    result = {
        "loaded_at": datetime.now().isoformat(),
        "bundle": "startup",  # Always startup - resume is hook's job
        # ... rest of result ...
    }
```

---

### 2.3 File: `nexus/state.py`

**Lines to Modify**: 32-51 (detect_system_state function)

**IMPORTANT**: Keep `resume_mode` parameter because `session_start.py` hook calls `detect_system_state()` with it.

```python
# BEFORE (Lines 32-51)
def detect_system_state(
    files_exist: Dict[str, bool],
    goals_path: Path,
    projects: List[Dict[str, Any]],
    resume_mode: bool = False,
) -> SystemState:
    """
    Classify the current system state based on file existence and project status.

    Args:
        files_exist: Dict mapping file keys to existence status
        goals_path: Path to goals.md file
        projects: List of project metadata
        resume_mode: Whether we're resuming from context summary

    Returns:
        SystemState enum value
    """
    if resume_mode:
        return SystemState.RESUME

    # STATE 1: First Time Setup (no goals.md)
    if not files_exist.get("goals", False):
        return SystemState.FIRST_TIME_WITH_DEFAULTS

    # ... rest of function ...
```

```python
# AFTER (Lines 32-51) - NO CHANGES NEEDED
# This function is used by session_start.py hook, which SHOULD pass resume_mode
# The hook detects source=resume/compact and passes resume_mode=True
# This is the CORRECT usage - keep as is.

def detect_system_state(
    files_exist: Dict[str, bool],
    goals_path: Path,
    projects: List[Dict[str, Any]],
    resume_mode: bool = False,  # Used by session_start.py hook - KEEP
) -> SystemState:
    """
    Classify the current system state based on file existence and project status.

    Args:
        files_exist: Dict mapping file keys to existence status
        goals_path: Path to goals.md file
        projects: List of project metadata
        resume_mode: Set by session_start.py hook when source=resume/compact

    Returns:
        SystemState enum value
    """
    if resume_mode:
        return SystemState.RESUME

    # STATE 1: First Time Setup (no goals.md)
    if not files_exist.get("goals", False):
        return SystemState.FIRST_TIME_WITH_DEFAULTS

    # ... rest of function ...
```

**RESULT**: NO CHANGES to `state.py` - it's already correctly designed for hook usage.

---

### 2.4 File: `session_start.py`

**NO CHANGES NEEDED** - This is the correct implementation.

The hook already:
1. Detects `source` field from stdin: `startup`, `resume`, `compact`, `clear`
2. Sets `resume_mode = source in ("resume", "compact")` (line 182)
3. Calls `build_resume_context()` when resume_mode=True
4. Injects context via `additionalContext`

This is the **single source of truth** for resume behavior.

---

## 3. Backward Compatibility Function

Add to `nexus-loader.py` for users with scripts calling `--resume`:

```python
# BACKWARD COMPATIBILITY WRAPPER (Add after line 88)
def load_startup(base_path: str = ".", include_metadata: bool = True,
                 resume_mode: bool = False, check_updates: bool = True):
    """
    Backward compatible wrapper for NexusService.startup()

    DEPRECATED v4.1: The resume_mode parameter is ignored.
    Resume context is now automatically injected by session_start.py hook.
    """
    if resume_mode:
        import warnings
        warnings.warn(
            "--resume flag is deprecated. Resume is handled automatically by session_start.py hook.",
            DeprecationWarning,
            stacklevel=2
        )

    service = NexusService(base_path)
    return service.startup(
        include_metadata=include_metadata,
        resume_mode=False,  # Always False - resume handled by hook
        check_updates=check_updates
    )
```

---

## 4. Deprecation Strategy (3-Phase Rollout)

### Phase 1: Deprecation Warning (v4.1 - Immediate)
- **Timeline**: Current release
- **Changes**:
  - Remove `--resume` from argparse (argument no longer accepted)
  - Add deprecation warning to `service.startup()` if resume_mode=True
  - Update CLI help text
  - Add migration guide to documentation
- **User Impact**: Minimal - hook already handles resume
- **Communication**:
  ```
  WARNING: --resume flag has been removed. Session resume is now handled
  automatically by the session_start.py hook. No action required - this
  improves reliability by eliminating dual systems.
  ```

### Phase 2: Error on Usage (v4.2 - Next Release)
- **Timeline**: 1-2 weeks after v4.1
- **Changes**:
  - Keep deprecation warning in `service.startup()`
  - Document that direct Python API calls should not use resume_mode
- **User Impact**: None if using Claude Code normally
- **Communication**:
  ```
  NOTICE: resume_mode parameter in NexusService.startup() is deprecated.
  If you're calling this from Python code, remove the resume_mode parameter.
  Resume is handled automatically by session hooks.
  ```

### Phase 3: Complete Removal (v5.0 - Major Version)
- **Timeline**: Next major version
- **Changes**:
  - Remove `resume_mode` parameter from all functions
  - Clean up state detection logic
  - Remove backward compatibility wrappers
- **User Impact**: Breaking change for direct API users
- **Communication**: Major version upgrade notes

---

## 5. Updated CLI Help Text

### BEFORE:
```
$ python nexus-loader.py --help
usage: nexus-loader.py [-h] [--startup] [--resume] [--skip-update-check] ...

Nexus-v4 Context Loader

optional arguments:
  --startup             Load startup context with embedded memory files
  --resume              Resume after context summary (skip menu, continue working)
  --skip-update-check   Skip update check during startup (faster startup)
  ...
```

### AFTER:
```
$ python nexus-loader.py --help
usage: nexus-loader.py [-h] [--startup] [--skip-update-check] ...

Nexus-v4 Context Loader

optional arguments:
  --startup             Load startup context with embedded memory files
  --skip-update-check   Skip update check during startup (faster startup)
  ...

NOTE: Session resume is handled automatically by session_start.py hook.
      The --resume flag has been removed in v4.1.
```

---

## 6. Test Cases for Backward Compatibility

### Test 1: Hook-Based Resume (New System)
```python
# Test that session_start.py hook correctly injects resume context
def test_hook_resume_injection():
    """Verify session_start.py detects source=resume and injects context"""
    hook_input = {
        "session_id": "test-123",
        "source": "resume"  # or "compact"
    }

    # Run hook
    result = run_session_start_hook(hook_input)

    # Verify
    assert result["hookSpecificOutput"]["hookEventName"] == "SessionStart"
    context = json.loads(result["hookSpecificOutput"]["additionalContext"])
    assert context["mode"] == "resume"
    assert context["action"] == "continue_working"
    assert "nexus_data" in context
```

### Test 2: Removed --resume Flag
```python
# Test that --resume flag is no longer accepted
def test_resume_flag_removed():
    """Verify --resume flag is no longer in argparse"""
    result = subprocess.run(
        ["python", "nexus-loader.py", "--resume"],
        capture_output=True,
        text=True
    )

    # Should show error about unrecognized argument
    assert result.returncode != 0
    assert "unrecognized arguments: --resume" in result.stderr
```

### Test 3: Python API Backward Compat
```python
# Test that direct Python calls with resume_mode still work (with warning)
def test_python_api_resume_mode_deprecated():
    """Verify resume_mode parameter shows deprecation warning"""
    import warnings

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")

        service = NexusService(".")
        result = service.startup(resume_mode=True)

        # Should emit deprecation warning
        assert len(w) == 1
        assert issubclass(w[0].category, DeprecationWarning)
        assert "resume_mode parameter is deprecated" in str(w[0].message)

        # Should still return valid result (ignoring resume_mode)
        assert result["bundle"] == "startup"
```

### Test 4: State Detection Still Works
```python
# Test that state.py still detects resume mode from hook
def test_state_detection_resume():
    """Verify detect_system_state works with resume_mode=True"""
    state = detect_system_state(
        files_exist={"goals": True},
        goals_path=Path("01-memory/goals.md"),
        projects=[],
        resume_mode=True  # Passed by session_start.py hook
    )

    assert state == SystemState.RESUME
```

### Test 5: --startup Still Works
```python
# Test that --startup flag still functions normally
def test_startup_flag_works():
    """Verify --startup flag continues to work"""
    result = subprocess.run(
        ["python", "nexus-loader.py", "--startup"],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0
    data = json.loads(result.stdout)
    assert "⚠️ MANDATORY" in data or "bundle" in data
```

---

## 7. Migration Guide for Users

### For End Users (Claude Code CLI)
**NO ACTION REQUIRED**. The session_start.py hook automatically handles resume context.

### For Python API Users (Direct Imports)
If you're calling `NexusService.startup()` from Python code:

**BEFORE**:
```python
from nexus import NexusService

service = NexusService(".")
result = service.startup(resume_mode=True)  # ❌ Deprecated
```

**AFTER**:
```python
from nexus import NexusService

service = NexusService(".")
result = service.startup()  # ✅ Correct - resume handled by hook

# If you need to detect resume state, check session_start.py hook output
# The hook injects resume context via additionalContext
```

### For Script Users (Bash/PowerShell)
If you have scripts calling `nexus-loader.py --resume`:

**BEFORE**:
```bash
python nexus-loader.py --resume
```

**AFTER**:
```bash
# No longer needed - session_start.py hook handles resume
# If you need startup context manually:
python nexus-loader.py --startup
```

---

## 8. Documentation Updates Needed

### Files to Update:
1. `00-system/core/nexus-loader.py` - Module docstring (line 2-17)
2. `00-system/core/nexus/ARCHITECTURE.md` - Remove --resume references
3. `00-system/documentation/hook-system.md` - Clarify resume is hook-only
4. `AGENTS.md` - Remove --resume examples (line 21, 32)
5. `GEMINI.md` - Remove --resume examples (line 23, 34)

### Documentation Template:

```markdown
# Session Resume (v4.1+)

Session resume is handled automatically by the `session_start.py` hook.

## How It Works

1. Claude Code detects session resume events (`source=resume` or `source=compact`)
2. `session_start.py` hook is triggered with source field
3. Hook builds resume context with:
   - Minimal routing rules
   - NEVER do rules
   - Language preference
   - Action: "continue_working"
4. Context is injected via `additionalContext` into Claude's initial context
5. Claude continues working from previous state

## No CLI Required

The `--resume` flag has been removed. Resume is fully automatic via hooks.

## For Developers

If building custom integrations:
- Use `session_start.py` hook as reference
- Detect resume via `source` field in hook input
- Inject context via `additionalContext` in hook output
```

---

## 9. Risk Analysis

### Low Risk
- **Hook already works**: `session_start.py` is production-ready and tested
- **No CLI breakage**: Users don't manually call `--resume`
- **Backward compat**: Python API keeps `resume_mode` param (with warning)

### Medium Risk
- **Documentation lag**: Need to update multiple doc files
- **User confusion**: Users might see warnings and not understand why

### High Risk
- **None identified**: The hook IS the system, removing `--resume` just eliminates redundancy

### Mitigation Strategies
1. **Clear messaging**: Add prominent notice in deprecation warning
2. **Gradual rollout**: Phase 1 (remove flag) → Phase 2 (warn on API) → Phase 3 (remove param)
3. **Test coverage**: Add comprehensive tests (see section 6)
4. **Documentation**: Update all references immediately

---

## 10. Summary of Changes

### Files Modified: 3
1. **nexus-loader.py**
   - Remove `--resume` argument from argparse
   - Remove `args.resume` checks
   - Update help text
   - Add backward compatibility wrapper

2. **nexus/service.py**
   - Add deprecation warning to `startup()` if resume_mode=True
   - Update docstring
   - Keep parameter for backward compat

3. **nexus/state.py**
   - **NO CHANGES** (correctly used by hook)

### Documentation Updates: 5 files
- nexus-loader.py module docstring
- ARCHITECTURE.md
- hook-system.md
- AGENTS.md
- GEMINI.md

### Lines of Code Changed: ~30
- Removed: ~10 lines (argparse, conditionals)
- Modified: ~15 lines (docstrings, warnings)
- Added: ~5 lines (deprecation notices)

### Breaking Changes: 0 (in Phase 1)
- CLI flag removed (was redundant)
- Python API keeps parameter (deprecated but functional)
- Hook-based resume fully operational

---

## 11. Implementation Checklist

- [ ] Phase 1: Remove `--resume` flag from nexus-loader.py
  - [ ] Remove argparse argument (line 103)
  - [ ] Update conditional checks (lines 132, 172, 197)
  - [ ] Update module docstring (line 9)
  - [ ] Add backward compat wrapper

- [ ] Phase 1: Add deprecation to nexus/service.py
  - [ ] Add warning in `startup()` if resume_mode=True
  - [ ] Update docstring
  - [ ] Keep parameter signature

- [ ] Phase 1: Update documentation
  - [ ] nexus-loader.py help text
  - [ ] ARCHITECTURE.md (remove --resume refs)
  - [ ] hook-system.md (clarify hook-only)
  - [ ] AGENTS.md (remove examples)
  - [ ] GEMINI.md (remove examples)

- [ ] Phase 1: Add tests
  - [ ] Test hook resume injection
  - [ ] Test --resume flag rejected
  - [ ] Test Python API deprecation warning
  - [ ] Test state detection still works
  - [ ] Test --startup still works

- [ ] Phase 2: Monitor usage (1-2 weeks)
  - [ ] Check logs for deprecation warnings
  - [ ] Monitor user feedback
  - [ ] Verify no breaking issues

- [ ] Phase 3: Plan v5.0 cleanup
  - [ ] Remove resume_mode parameter entirely
  - [ ] Simplify state detection
  - [ ] Remove backward compat wrappers

---

## Conclusion

The `--resume` flag is **completely redundant** because the `session_start.py` hook provides superior resume handling:

1. **Automatic detection**: Hook detects source=resume/compact from Claude Code
2. **Direct injection**: Context injected via additionalContext (no CLI needed)
3. **Single source of truth**: Eliminates dual system confusion
4. **Better reliability**: Hook can't be forgotten or skipped

**Recommended Action**: Implement Phase 1 immediately (remove flag, add deprecation warnings). The risk is minimal because the hook already handles all resume scenarios correctly.

**User Impact**: Near zero. Users don't manually invoke `--resume`, and the hook provides better functionality automatically.
