# Implementation Steps

## Phase 1: Session Management (HIGH PRIORITY) ✅ COMPLETE
- [x] Create `session_start.py` hook
- [x] Detect `source`: startup | resume | clear | compact
- [x] Write session ID to `.claude/sessions/{hash}.session`
- [x] Output nexus-loader command via stdout (additionalContext) ← **GAME CHANGER**
- [x] Add to settings.json SessionStart config
- [x] Implement SLIM POINTER pattern (hook output ~500 bytes instead of 84KB)
- [x] Add MANDATORY STOP enforcement in hook output
- [x] Update CLAUDE.md with HYPER IMPORTANT cache reading instruction
- [ ] Test fresh session and resume scenarios
- [ ] Test /clear and /compact triggers

**Research Notes** (from ULTRATHINK):
- Bug #13650: Wrap additionalContext in XML tags `<NexusStartup>...</NexusStartup>` for reliability
- Use `print(json.dumps(result), flush=True)` to ensure output is captured
- Fixed in v2.0.76+
- **Hook output limit**: ~9K chars safe for UserPromptSubmit, ~25KB safe for SessionStart
- **SLIM POINTER pattern**: Output summary + path, Claude reads full file via Read tool

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

## Phase 0: Research & Exploration ✅ CLONED (10 REPOS) - EXPLORATION PENDING

**Cloned Repositories** (local resources for reference):
```
04-workspace/00-ai-native-org/hook-repos/
├── awesome-claude-code/           # 18k+ stars, comprehensive resource list
├── cc-tools/                      # Go implementation - high performance hooks
├── claude-code-hooks/             # 15 Git-specific hooks (EvanL1)
├── claude-code-hooks-mastery/     # All 8 hook events with examples
├── claude-code-safety-net/        # Production-ready safety patterns
├── claude-code-tools/             # tmux + safety-hooks plugin (!!)
├── claude-codex-settings/         # fcakyon - code quality hooks
├── claude-hooks/                  # TypeScript hooks system (johnlindquist)
└── tdd-guard/                     # TDD enforcement system
```

### Exploration Tasks (TO DO):
- [ ] **Study hooks-mastery settings.json** - Learn complete 8-hook config pattern
- [ ] **Extract session_start.py patterns** - Context loading, git status, TTS announce
- [ ] **Extract pre_tool_use.py patterns** - rm -rf + .env detection to copy
- [ ] **Study rules_rm.py** - Advanced rm analysis (temp paths, cwd checks)
- [ ] **Study rules_git.py** - Copy 12+ git safety rules for our pre_tool_use
- [ ] **Review git-safety-check.py** - Protected branches, --no-verify blocking
- [ ] **Compare with awesome-claude-code list** - Find any missed patterns
- [ ] **Study claude-code-tools safety-hooks** - rm_block, git_checkout_safety, env_file_protection
- [ ] **Review claude-codex-settings plugins** - tool redirection (WebFetch→Tavily), code quality
- [ ] **Evaluate tdd-guard architecture** - multi-reporter system (jest, pytest, vitest)

**Key Files to Study**:
| Repo | File | What to Learn |
|------|------|---------------|
| hooks-mastery | `.claude/settings.json` | Complete 8-hook config example |
| hooks-mastery | `.claude/hooks/session_start.py` | Context loading, git status, TTS |
| hooks-mastery | `.claude/hooks/pre_tool_use.py` | rm -rf + .env detection patterns |
| safety-net | `scripts/safety_net_impl/rules_rm.py` | Advanced rm analysis (temp paths, cwd) |
| safety-net | `scripts/safety_net_impl/rules_git.py` | 12+ git safety rules |
| claude-code-hooks | `hooks/git-safety-check.py` | Protected branches, --no-verify |
| **claude-code-tools** | `plugins/safety-hooks/hooks/rm_block_hook.py` | **TRASH folder pattern** |
| **claude-code-tools** | `plugins/safety-hooks/hooks/git_checkout_safety_hook.py` | **Live git status check** |
| **claude-code-tools** | `plugins/safety-hooks/hooks/env_file_protection_hook.py` | .env protection |
| **claude-codex-settings** | `plugins/tavily-tools/hooks/scripts/*.py` | Tool redirection |
| **claude-codex-settings** | `plugins/ultralytics-dev/hooks/scripts/*.py` | Code quality hooks |
| awesome-claude-code | `README_ALTERNATIVES/README_FLAT_HOOKS_AZ.md` | 9 hook resources indexed |

**Community Hooks Discovered** (potential integrations):
| Name | Author | Purpose |
|------|--------|---------|
| Britfix | Talieisin | British English auto-conversion |
| CC Notify | dazuiba | Desktop notifications + VS Code jump |
| cchooks | GowayLee | Python SDK for hooks |
| HCOM | aannoo | Multi-agent communication |
| claude-hooks-sdk | beyondcode | PHP SDK (Laravel-style) |
| claude-hooks | johnlindquist | TypeScript hooks system |
| Claudio | ctoth | OS-native sounds |
| TDD Guard | nizos | TDD enforcement |
| TypeScript Quality | bartolli | ESLint + Prettier auto-fix |

---

## Remaining Tasks Summary

| Priority | Task | Status |
|----------|------|--------|
| **EXPLORE** | Study cloned repos (hooks-mastery, safety-net, claude-code-hooks) | Pending |
| **EXPLORE** | Extract best patterns from rules_rm.py and rules_git.py | Pending |
| **EXPLORE** | Review community hooks for adoption ideas | Pending |
| HIGH | Test session scenarios (startup/resume/clear/compact) | Pending |
| HIGH | Test dangerous command blocking | Pending |
| MEDIUM | Add git safety patterns (copy from safety-net) | Pending |
| MEDIUM | Add credential file blocking | Pending |
| LOW | Create utils/safety.py shared module | Pending |
| LOW | Create utils/platform.py UTF-8 fix | Pending |
| LOW | Full hook chain integration test | Pending |

---

## ULTRATHINK: Future Hook Opportunities

### Phase 5: Quality Gates (OPTIONAL)

**PostToolUse - Auto-Lint/Format**:
```json
{
  "matcher": "Edit:*.py",
  "hooks": [{"type": "command", "command": "ruff check --fix $CLAUDE_FILE_PATHS"}]
}
```

**Stop Hook - Prevent Early Termination**:
```json
{
  "type": "prompt",
  "prompt": "Check if all tasks complete. Block with reason if not."
}
```

### Phase 6: Notifications (OPTIONAL)

**Desktop Alerts**:
```json
{
  "Notification": [{
    "matcher": "permission_prompt|idle_prompt",
    "hooks": [{"type": "command", "command": ".claude/hooks/notify.sh"}]
  }]
}
```

### Phase 7: PermissionRequest Auto-Approve (OPTIONAL)

**Smart Permission Handler**:
```python
# deny_first.py
deny = ['rm -rf /', 'sudo', 'git reset --hard']
allow = ['ls', 'cat', 'git status', 'npm test']
# Unknown → user prompt (fail-safe)
```

### Phase 8: UserPromptSubmit (OPTIONAL)

**Context Injection**:
```json
{
  "UserPromptSubmit": [{
    "hooks": [{"type": "command", "command": "cat ./project-context.md"}]
  }]
}
```

---

## Debugging Checklist

```bash
# 1. Check hook config
/hooks

# 2. Debug mode
claude --debug

# 3. Test manually
echo '{"tool_name":"Bash","tool_input":{"command":"test"}}' | python .claude/hooks/pre_tool_use.py
echo $?  # Check exit code

# 4. Common fixes
chmod +x .claude/hooks/*.py
# Use $CLAUDE_PROJECT_DIR for paths
# Blocking = stderr + exit 2 (NOT stdout)
# Flush output: print(..., flush=True)
```

---

## References

**Official**:
- [Claude Code Hooks Docs](https://code.claude.com/docs/en/hooks)
- [How to Configure Hooks](https://claude.com/blog/how-to-configure-hooks)

**Awesome Lists & Plugin Hubs** (BEST RESOURCES):
- [awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) - 18k+ Stars, comprehensive collection
- [awesome-claude-code-plugins](https://github.com/ccplugins/awesome-claude-code-plugins) - Curated plugins list
- [awesome-claude-plugins](https://github.com/quemsah/awesome-claude-plugins) - 243 plugins indexed
- [claudeforge/marketplace](https://github.com/claudeforge/marketplace) - 161 plugins

**Hooks Repositories** (COPY-PASTE READY):
- [claude-code-hooks-mastery](https://github.com/disler/claude-code-hooks-mastery) - All 8 hook events covered
- [claude-code-hooks](https://github.com/EvanL1/claude-code-hooks) - 15 Git-specific hooks

**Safety**:
- [claude-code-safety-net](https://github.com/kenryu42/claude-code-safety-net)
- [Taming YOLO Mode](https://www.agentic-engineer.com/blog/2025-10-13-taming-claude-yolo-mode)
- [Bash Permission Hook](https://gist.github.com/cruftyoldsysadmin/84b2c66ddd0fa170a840fc0cb649612b)

**Examples**:
- [Steve Kinney Examples](https://stevekinney.com/courses/ai-development/claude-code-hook-examples)
- [Auto Quality Checks](https://www.letanure.dev/blog/2025-08-06--claude-code-part-8-hooks-automated-quality-checks)

**Notifications**:
- [Desktop Notifications](https://alexop.dev/posts/claude-code-notification-hooks/)
- [ntfy Integration](https://andrewford.co.nz/articles/claude-code-instant-notifications-ntfy/)

**Multi-Session**:
- [GitButler Parallel](https://blog.gitbutler.com/parallel-claude-code)
- [ccswarm](https://github.com/nwiizo/ccswarm)

**Bug Tracker**:
- [SessionStart stdout #13650](https://github.com/anthropics/claude-code/issues/13650)
- [Notification type #11964](https://github.com/anthropics/claude-code/issues/11964)

**Local Cloned Resources** (ready to explore):
- `04-workspace/00-ai-native-org/hook-repos/awesome-claude-code/`
- `04-workspace/00-ai-native-org/hook-repos/claude-code-hooks-mastery/`
- `04-workspace/00-ai-native-org/hook-repos/claude-code-hooks/`
- `04-workspace/00-ai-native-org/hook-repos/claude-code-safety-net/`
