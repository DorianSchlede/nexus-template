# awesome-claude-code Index

**Source:** https://github.com/anthropics/awesome-claude-code (community curated)
**Date Indexed:** 2025-12-31
**Total Hook Resources:** 10 dedicated hook repos + numerous hook-integrated tools

---

## Hook Repositories Mentioned

### Dedicated Hook Libraries (Hooks Category)

| Repository | Author | Description | License |
|------------|--------|-------------|---------|
| **[Britfix](https://github.com/Talieisin/britfix)** | Talieisin | Claude outputs American spellings by default. Britfix converts to British English with a Claude Code hook for automatic conversion as files are written. Context-aware: handles code files intelligently by only converting comments and docstrings, never identifiers or string literals. | MIT |
| **[CC Notify](https://github.com/dazuiba/CCNotify)** | dazuiba | Desktop notifications for Claude Code, alerting you to input needs or task completion, with one-click jumps back to VS Code and task duration display. | MIT |
| **[cchooks](https://github.com/GowayLee/cchooks)** | GowayLee | A lightweight Python SDK with a clean API and good documentation; simplifies the process of writing hooks and integrating them into your codebase, providing a nice abstraction over the JSON configuration files. | MIT |
| **[Claude Code Hook Comms (HCOM)](https://github.com/aannoo/claude-hook-comms)** | aannoo | Lightweight CLI tool for real-time communication between Claude Code sub agents using hooks. Enables multi-agent collaboration with @-mention targeting, live dashboard monitoring, and zero-dependency implementation. | MIT |
| **[claude-code-hooks-sdk](https://github.com/beyondcode/claude-hooks-sdk)** | beyondcode | A Laravel-inspired PHP SDK for building Claude Code hook responses with a clean, fluent API. Makes it easy to create structured JSON responses using an expressive, chainable interface. | MIT |
| **[claude-hooks](https://github.com/johnlindquist/claude-hooks)** | John Lindquist | A TypeScript-based system for configuring and customizing Claude Code hooks with a powerful and flexible interface. | MIT |
| **[Claudio](https://github.com/ctoth/claudio)** | Christopher Toth | A no-frills little library that adds delightful OS-native sounds to Claude Code via simple hooks. | N/A |
| **[TDD Guard](https://github.com/nizos/tdd-guard)** | Nizar Selander | A hooks-driven system that monitors file operations in real-time and blocks changes that violate TDD principles. | MIT |
| **[TypeScript Quality Hooks](https://github.com/bartolli/claude-code-typescript-hooks)** | bartolli | Quality check hook for Node.js TypeScript projects with TypeScript compilation, ESLint auto-fixing, and Prettier formatting. Uses SHA256 config caching for < 5ms validation performance. | MIT |
| **[fcakyon Collection](https://github.com/fcakyon/claude-codex-settings/tree/main/.claude/hooks)** | Fatih Akyon | Very well-written set of hooks for code quality and tool usage regulation (e.g. force Tavily over WebFetch tool). | Apache-2.0 |

### Tooling with Hook Integration

| Repository | Author | Description | Hook Usage |
|------------|--------|-------------|------------|
| **[cc-tools](https://github.com/Veraticus/cc-tools)** | Josh Symonds | High-performance Go implementation of Claude Code hooks and utilities. Provides smart linting, testing, and statusline generation with minimal overhead. | Core hook implementation |
| **[claude-code-tools](https://github.com/pchalasani/claude-code-tools)** | Prasad Chalasani | A collection of awesome tools, including tmux integrations, better session management, hooks that enhance security. | Security hooks |
| **[claudekit](https://github.com/carlrannaberg/claudekit)** | Carl Rannaberg | CLI toolkit providing auto-save checkpointing, code quality hooks, specification generation and execution, and 20+ specialized subagents. | Code quality hooks |
| **[Claude Code Infrastructure Showcase](https://github.com/diet103/claude-code-infrastructure-showcase)** | diet103 | A technique that leverages hooks to ensure that Claude intelligently selects and activates the appropriate Skill given the current context. | Skill activation hooks |
| **[Claude CodePro](https://github.com/maxritter/claude-codepro)** | Max Ritter | Professional development environment with spec-driven workflow, TDD enforcement, cross-session memory, semantic search, quality hooks, and modular rules integration. | Quality hooks |

---

## Additional Repos to Consider

### NOT in our current collection:

| Repository | Why Consider | Priority |
|------------|--------------|----------|
| **[Britfix](https://github.com/Talieisin/britfix)** | Novel use case - localization hooks for British English | Medium |
| **[CC Notify](https://github.com/dazuiba/CCNotify)** | Desktop notification pattern - useful for background operations | High |
| **[cchooks](https://github.com/GowayLee/cchooks)** | Python SDK for hooks - abstraction layer pattern | High |
| **[Claude Code Hook Comms (HCOM)](https://github.com/aannoo/claude-hook-comms)** | Multi-agent communication via hooks - innovative pattern | High |
| **[claude-hooks-sdk (PHP)](https://github.com/beyondcode/claude-hooks-sdk)** | PHP SDK for hooks - different language ecosystem | Medium |
| **[Claudio](https://github.com/ctoth/claudio)** | Sound feedback hooks - UX enhancement pattern | Low |
| **[TypeScript Quality Hooks](https://github.com/bartolli/claude-code-typescript-hooks)** | TypeScript-specific quality hooks with SHA256 caching | Medium |

### Already in our collection (confirmed):
- claude-hooks (johnlindquist)
- tdd-guard (nizos)
- claude-codex-settings (fcakyon) - includes hooks
- cc-tools (Veraticus)
- claude-code-tools (pchalasani)

---

## Community Best Practices

### Patterns Identified from awesome-claude-code:

1. **SDK Abstraction Pattern**
   - cchooks (Python), claude-hooks (TypeScript), claude-hooks-sdk (PHP)
   - Provide clean APIs over JSON configuration files
   - Fluent/chainable interfaces preferred

2. **Lifecycle Hook Categories**
   - PreToolUse: Validation before tool execution
   - PostToolUse: Processing after tool completion
   - Stop hooks: Session end notifications
   - Write hooks: File operation interception

3. **Quality Gate Pattern**
   - TypeScript Quality Hooks: ESLint, Prettier, TypeScript compilation
   - TDD Guard: Test-first enforcement
   - cc-tools: Smart linting with minimal overhead

4. **Notification Pattern**
   - CC Notify: Desktop notifications for task completion
   - Claudio: Audio feedback on events
   - Integration with VS Code jumps

5. **Multi-Agent Communication Pattern**
   - HCOM: @-mention targeting between sub-agents
   - Live dashboard monitoring
   - Zero-dependency implementation

6. **Performance Optimization**
   - SHA256 config caching (< 5ms validation)
   - Go implementations for minimal overhead
   - Rust implementations for statuslines

---

## Tutorials and Guides

### Slash Command for Hook Creation
- **[/create-hook](https://github.com/omril321/automated-notebooklm/blob/main/.claude/commands/create-hook.md)** by Omri Lavi
  - Intelligently prompts through hook creation process
  - Smart suggestions based on project setup (TS, Prettier, ESLint)

### Workflow Guides with Hook Integration
- **[Claude Code Infrastructure Showcase](https://github.com/diet103/claude-code-infrastructure-showcase)**
  - Technique for hooks to activate appropriate Skills based on context
  - Well-documented and adaptable

- **[Claude Code Handbook](https://nikiforovall.blog/claude-code-rules/)**
  - Collection of best practices including hooks
  - Distributable plugins

### Documentation Resources
- **[Claude Code Documentation Mirror](https://github.com/ericbuess/claude-code-docs)**
  - Updated every few hours
  - Includes hook documentation

- **[Claude Code System Prompts](https://github.com/Piebald-AI/claude-code-system-prompts)**
  - All parts of system prompt including hook-related info
  - Updated for each Claude Code version

---

## Missing Resources to Explore

### Priority Exploration List:

1. **cchooks Python SDK** - Need to analyze abstraction patterns
2. **HCOM multi-agent communication** - Novel hook-based agent coordination
3. **CC Notify patterns** - Desktop notification implementation
4. **TypeScript Quality Hooks caching** - SHA256 config caching technique
5. **Britfix localization pattern** - Context-aware file transformation

### Research Questions:

- How does cchooks abstract the JSON configuration?
- What is HCOM's @-mention targeting implementation?
- How does cc-tools achieve minimal overhead in Go?
- What caching strategies are used for < 5ms validation?

---

## Summary Statistics

| Category | Count |
|----------|-------|
| Dedicated Hook Repos | 10 |
| Tooling with Hook Integration | 5+ |
| Hook SDKs (language-specific) | 3 (Python, TypeScript, PHP) |
| Hook Creation Tutorials | 1 |
| Workflow Guides with Hooks | 3+ |

---

## Next Steps

1. Clone and analyze cchooks, HCOM, CC Notify
2. Extract abstraction patterns from SDKs
3. Document multi-agent communication patterns
4. Study performance optimization techniques
5. Create comprehensive pattern library
