# HYPERPLAN: Multi-Agent Repository Exploration

## Objective
Systematically explore all 10 cloned hook repositories using parallel agents to extract patterns, best practices, and reusable code for the Nexus Advanced Hook System.

---

## Repository Inventory

| # | Repo | Language | Priority | Agent Focus |
|---|------|----------|----------|-------------|
| 1 | claude-code-safety-net | Python | **CRITICAL** | Safety patterns (rm, git rules) |
| 2 | claude-code-tools | Python | **CRITICAL** | Safety-hooks plugin architecture |
| 3 | claude-code-hooks-mastery | Python | **HIGH** | All 8 hook events, settings.json |
| 4 | claude-code-hooks | Python | **HIGH** | Git-specific hooks (15 hooks) |
| 5 | claude-codex-settings | Python | **MEDIUM** | Tool redirection, code quality |
| 6 | tdd-guard | TypeScript | **MEDIUM** | TDD enforcement patterns |
| 7 | cc-tools | Go | **LOW** | High-performance patterns |
| 8 | claude-hooks | TypeScript | **LOW** | TypeScript hook architecture |
| 9 | awesome-claude-code | Markdown | **REFERENCE** | Index of all resources |
| 10 | (reserved) | - | - | Future repos |

---

## Phase 1: CRITICAL Safety Repos (Parallel Agents)

### Agent 1A: claude-code-safety-net
**Path**: `04-workspace/00-ai-native-org/hook-repos/claude-code-safety-net/`

**Files to Read**:
```
scripts/safety_net_impl/rules_rm.py      # rm -rf analysis
scripts/safety_net_impl/rules_git.py     # 12+ git safety rules
scripts/safety_net_impl/shell.py         # Command parsing utilities
scripts/safety_net_impl/hook.py          # Main hook implementation
hooks/hooks.json                         # Hook configuration
tests/test_safety_net_rm.py              # Test patterns
tests/test_safety_net_git.py             # Git test patterns
```

**Extract**:
- [ ] All rm -rf detection patterns with edge cases
- [ ] Git command safety rules (checkout, restore, reset, push, clean, stash)
- [ ] Temp path detection logic (`_is_temp_path`)
- [ ] CWD protection logic (`_is_path_within_cwd`)
- [ ] Exit code patterns and blocking behavior
- [ ] Test cases to copy for our implementation

**Output**: `findings/safety-net-patterns.md`

---

### Agent 1B: claude-code-tools safety-hooks
**Path**: `04-workspace/00-ai-native-org/hook-repos/claude-code-tools/plugins/safety-hooks/`

**Files to Read**:
```
hooks/rm_block_hook.py              # TRASH folder pattern
hooks/git_checkout_safety_hook.py   # Live git status check
hooks/git_add_block_hook.py         # Git add safety
hooks/git_commit_block_hook.py      # Git commit safety
hooks/env_file_protection_hook.py   # .env protection
hooks/file_length_limit_hook.py     # File size limits
hooks/command_utils.py              # Shared utilities
```

**Extract**:
- [ ] TRASH folder pattern (alternative to rm)
- [ ] Live `git status --porcelain` checking before checkout
- [ ] Uncommitted changes warning with file list
- [ ] Compound command parsing (`extract_subcommands`)
- [ ] JSON response format for blocking (`decision: block/approve`)

**Output**: `findings/claude-code-tools-patterns.md`

---

## Phase 2: HIGH Priority Hook Systems (Parallel Agents)

### Agent 2A: claude-code-hooks-mastery
**Path**: `04-workspace/00-ai-native-org/hook-repos/claude-code-hooks-mastery/`

**Files to Read**:
```
.claude/settings.json                    # Complete 8-hook config
.claude/hooks/session_start.py           # Context loading, git status
.claude/hooks/pre_tool_use.py            # rm + .env detection
.claude/hooks/post_tool_use.py           # Post-execution hooks
.claude/hooks/pre_compact.py             # Pre-compaction hooks
.claude/hooks/stop.py                    # Stop hooks
.claude/hooks/subagent_stop.py           # Subagent stop
.claude/hooks/user_prompt_submit.py      # User prompt hooks
.claude/hooks/notification.py            # Notification hooks
.claude/hooks/utils/                     # Utility modules
```

**Extract**:
- [ ] Complete settings.json structure for all 8 hooks
- [ ] `uv run` pattern for dependency management
- [ ] Session logging to `logs/` directory
- [ ] Git branch + uncommitted changes detection at session start
- [ ] TTS announcement patterns
- [ ] Context file loading (.claude/CONTEXT.md, TODO.md)

**Output**: `findings/hooks-mastery-patterns.md`

---

### Agent 2B: claude-code-hooks (EvanL1)
**Path**: `04-workspace/00-ai-native-org/hook-repos/claude-code-hooks/`

**Files to Read**:
```
hooks/git-safety-check.py           # Protected branches, --no-verify
hooks/npm-safety-check.py           # npm safety
hooks/aws-safety-check.py           # AWS safety
hooks/docker-validator.py           # Docker validation
hooks/cargo-auto-format.py          # Auto-formatting
hooks/command-logger.py             # Command logging
hooks/dev-event-notifier.py         # Desktop notifications
hooks/file-stats.py                 # File statistics
examples/settings.json              # Example config
```

**Extract**:
- [ ] Protected branch detection (main, master, production, prod)
- [ ] `--no-verify` blocking with message context detection
- [ ] Multi-language safety patterns (npm, AWS, Docker)
- [ ] Notification patterns
- [ ] Command logging format

**Output**: `findings/claude-code-hooks-patterns.md`

---

## Phase 3: MEDIUM Priority Plugins (Parallel Agents)

### Agent 3A: claude-codex-settings (fcakyon)
**Path**: `04-workspace/00-ai-native-org/hook-repos/claude-codex-settings/`

**Files to Read**:
```
plugins/general-dev/hooks/scripts/enforce_rg_over_grep.py
plugins/github-dev/hooks/scripts/gh_pr_create_confirm.py
plugins/github-dev/hooks/scripts/git_commit_confirm.py
plugins/tavily-tools/hooks/scripts/webfetch_to_tavily_extract.py
plugins/tavily-tools/hooks/scripts/websearch_to_tavily_search.py
plugins/ultralytics-dev/hooks/scripts/python_code_quality.py
plugins/ultralytics-dev/hooks/scripts/format_python_docstrings.py
```

**Extract**:
- [ ] Tool redirection pattern (WebFetch → Tavily)
- [ ] Grep → ripgrep enforcement
- [ ] PR creation confirmation flow
- [ ] Git commit confirmation flow
- [ ] Python code quality hooks (ruff, black, isort)
- [ ] Docstring formatting hooks

**Output**: `findings/claude-codex-settings-patterns.md`

---

### Agent 3B: tdd-guard
**Path**: `04-workspace/00-ai-native-org/hook-repos/tdd-guard/`

**Files to Read**:
```
src/hooks/HookEvents.ts             # Hook event handling
src/hooks/processHookData.ts        # Data processing
src/hooks/sessionHandler.ts         # Session management
src/hooks/userPromptHandler.ts      # User prompt handling
src/hooks/postToolLint.ts           # Post-tool linting
src/guard/GuardManager.ts           # TDD guard logic
src/config/Config.ts                # Configuration
reporters/jest/src/JestReporter.ts  # Jest integration
reporters/pytest/tdd_guard_pytest/pytest_reporter.py  # Pytest integration
```

**Extract**:
- [ ] TDD enforcement logic
- [ ] Multi-framework test reporter architecture
- [ ] Hook event type definitions
- [ ] Session state management
- [ ] Guard blocking patterns

**Output**: `findings/tdd-guard-patterns.md`

---

## Phase 4: LOW Priority & Reference (Sequential)

### Agent 4A: cc-tools (Go)
**Path**: `04-workspace/00-ai-native-org/hook-repos/cc-tools/`

**Files to Read**:
```
internal/output/hook.go             # Hook output handling
internal/statusline/statusline.go   # Status line implementation
reference/hooks.md                  # Hook documentation
reference/statusline.md             # Status line docs
example-config.yaml                 # Configuration example
```

**Extract**:
- [ ] High-performance hook patterns
- [ ] Status line implementation
- [ ] Configuration patterns

**Output**: `findings/cc-tools-patterns.md`

---

### Agent 4B: claude-hooks (TypeScript)
**Path**: `04-workspace/00-ai-native-org/hook-repos/claude-hooks/`

**Extract**:
- [ ] TypeScript hook architecture
- [ ] Type definitions for hooks

**Output**: `findings/claude-hooks-patterns.md`

---

### Agent 4C: awesome-claude-code (Reference)
**Path**: `04-workspace/00-ai-native-org/hook-repos/awesome-claude-code/`

**Files to Read**:
```
THE_RESOURCES_TABLE.csv             # Full resource index
README_ALTERNATIVES/README_FLAT_HOOKS_AZ.md  # Hooks section
```

**Extract**:
- [ ] Any additional hook repos not yet cloned
- [ ] Community patterns and best practices
- [ ] Missing resources to explore

**Output**: `findings/awesome-index.md`

---

## Execution Strategy

### Wave 1 (Critical - Run in Parallel)
```
Agent 1A: claude-code-safety-net    ──┬── Run simultaneously
Agent 1B: claude-code-tools         ──┘
```

### Wave 2 (High - Run in Parallel after Wave 1)
```
Agent 2A: claude-code-hooks-mastery ──┬── Run simultaneously
Agent 2B: claude-code-hooks         ──┘
```

### Wave 3 (Medium - Run in Parallel after Wave 2)
```
Agent 3A: claude-codex-settings     ──┬── Run simultaneously
Agent 3B: tdd-guard                 ──┘
```

### Wave 4 (Low - Sequential after Wave 3)
```
Agent 4A: cc-tools
Agent 4B: claude-hooks
Agent 4C: awesome-claude-code
```

---

## Output Structure

```
02-projects/14-advanced-hook-system/02-research/
├── findings/
│   ├── safety-net-patterns.md          # Agent 1A output
│   ├── claude-code-tools-patterns.md   # Agent 1B output
│   ├── hooks-mastery-patterns.md       # Agent 2A output
│   ├── claude-code-hooks-patterns.md   # Agent 2B output
│   ├── claude-codex-settings-patterns.md  # Agent 3A output
│   ├── tdd-guard-patterns.md           # Agent 3B output
│   ├── cc-tools-patterns.md            # Agent 4A output
│   ├── claude-hooks-patterns.md        # Agent 4B output
│   └── awesome-index.md                # Agent 4C output
├── extracted-code/
│   ├── safety-patterns.py              # Consolidated safety patterns
│   ├── git-rules.py                    # All git safety rules
│   └── hook-configs/                   # Example settings.json files
└── SYNTHESIS.md                        # Final synthesis of all findings
```

---

## Agent Prompt Template

```
You are exploring a Claude Code hooks repository to extract patterns for the Nexus Advanced Hook System.

REPO: {repo_name}
PATH: 04-workspace/00-ai-native-org/hook-repos/{repo_name}/

YOUR TASK:
1. Read ALL files listed in the exploration plan
2. Extract patterns, best practices, and reusable code
3. Document findings in a structured markdown format
4. Highlight any CRITICAL safety patterns
5. Note any dependencies or setup requirements

OUTPUT FORMAT:
## {Repo Name} Findings

### Key Patterns
- Pattern 1: ...
- Pattern 2: ...

### Code to Copy
```python
# Paste reusable code here
```

### Configuration Examples
```json
// Settings.json patterns
```

### Dependencies
- Dependency 1: ...

### Notes for Implementation
- Note 1: ...
```

---

## Success Criteria

After all agents complete:
- [ ] All 10 repos explored
- [ ] 9 findings files created
- [ ] Safety patterns consolidated
- [ ] Git rules documented
- [ ] Hook configurations extracted
- [ ] SYNTHESIS.md created with implementation recommendations
