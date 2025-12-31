# Implementation Steps

## Phase 1: Session Management (HIGH PRIORITY) ✅ MOSTLY COMPLETE
- [x] Create `session_start.py` hook
- [x] Detect `source`: startup | resume | clear | compact
- [x] Write session ID to `.claude/sessions/{hash}.session`
- [x] Output nexus-loader command via stdout (additionalContext) ← **GAME CHANGER**
- [x] Add to settings.json SessionStart config
- [ ] Test fresh session and resume scenarios
- [ ] Test /clear and /compact triggers

**Research Notes** (from ULTRATHINK):
- Bug #13650: Wrap additionalContext in XML tags `<NexusStartup>...</NexusStartup>` for reliability
- Use `print(json.dumps(result), flush=True)` to ensure output is captured
- Fixed in v2.0.76+

## Phase 2: Safety Hooks ✅ MOSTLY COMPLETE
- [x] Create `pre_tool_use.py` hook (already exists, 11KB)
- [x] Implement `rm -rf` detection patterns
- [x] Implement `.env` file protection
- [x] Add to settings.json PreToolUse config
- [ ] Test with dangerous commands (exit code 2 = BLOCK)
- [ ] Add git safety (--force, --hard reset, --global config)
- [ ] Add credential blocking (*.pem, *.key, client_secret.json)

**Recommended Regex Patterns** (from claude-code-safety-net):
```python
# rm -rf variants (6 patterns)
r'\brm\s+.*-[a-z]*r[a-z]*f'      # rm -rf, rm -fr, rm -Rf
r'\brm\s+--recursive\s+--force'  # long form
r'\brm\s+-r\s+.*-f'              # separated flags

# .env protection (allow .env.sample, .env.example)
r'\.env(?!\.sample|\.example)'

# git dangerous operations
r'git\s+push\s+.*--force'
r'git\s+reset\s+--hard'
r'git\s+config\s+--global'

# credential files
r'client_secret\.json|\.credentials\.json|token\.pickle'
r'\.(pem|key)$'
```

## Phase 3: Utilities
- [x] `utils/` folder exists with http.py, server.py, registry.py
- [ ] Create `utils/safety.py` module (shared detection patterns)
- [ ] Create `utils/platform.py` for Windows UTF-8 encoding
- [ ] Unit tests for safety patterns (test all 6 rm variants)
- [ ] Unit tests for credential detection

## Phase 4: Integration & Multi-Session ✅ MOSTLY COMPLETE
- [x] Update nexus-loader.py to support `--session` flag
- [x] Implement session-isolated cache: `context_startup_{hash}.json`
- [x] Test 5 parallel sessions with isolated caches
- [x] session_end.py cleanup (session cache + stale caches >60min)
- [x] Attention Sandwich in service.py (instructions at START and END)
- [ ] Full hook chain test (SessionStart → PreToolUse → PreCompact → SessionEnd)
- [x] CLAUDE.md updated (session ID now via hook stdout!)

## Remaining Tasks Summary

| Priority | Task | Status |
|----------|------|--------|
| HIGH | Test session scenarios (startup/resume/clear/compact) | Pending |
| HIGH | Test dangerous command blocking | Pending |
| MEDIUM | Add git safety patterns | Pending |
| MEDIUM | Add credential file blocking | Pending |
| LOW | Create utils/safety.py shared module | Pending |
| LOW | Create utils/platform.py UTF-8 fix | Pending |
| LOW | Full hook chain integration test | Pending |

## References

- [Claude Code Hooks Docs](https://code.claude.com/docs/en/hooks)
- [claude-code-safety-net](https://github.com/kenryu42/claude-code-safety-net)
- [Taming YOLO Mode](https://www.agentic-engineer.com/blog/2025-10-13-taming-claude-yolo-mode)
- [SessionStart bug #13650](https://github.com/anthropics/claude-code/issues/13650)
- [GitButler Parallel Sessions](https://blog.gitbutler.com/parallel-claude-code)
