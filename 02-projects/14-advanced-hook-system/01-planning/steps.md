# Implementation Steps

## Phase 1: Safety Hooks
- [ ] Create `pre_tool_use.py` hook
- [ ] Implement `rm -rf` detection patterns
- [ ] Implement `.env` file protection
- [ ] Add to settings.json PreToolUse config
- [ ] Test with dangerous commands (dry run)

## Phase 2: Session Management
- [ ] Create `session_start.py` hook
- [ ] Auto-detect startup vs resume
- [ ] Run nexus-loader.py automatically
- [ ] Add to settings.json SessionStart config
- [ ] Test fresh session and resume

## Phase 3: Utilities
- [ ] Create `utils/safety.py` module
- [ ] Create `utils/platform.py` for Windows UTF-8
- [ ] Unit tests for safety patterns

## Phase 4: Integration
- [ ] Update settings.local.json with all hooks
- [ ] Test full hook chain
- [ ] Document hook system in system docs
