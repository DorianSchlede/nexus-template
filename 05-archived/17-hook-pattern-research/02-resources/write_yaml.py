#!/usr/bin/env python3
import os

content = r'''repo_id: "awesome"
repo_name: "awesome-claude-code"
repo_type: "index/collection"
language: "Markdown"
extracted_at: "2025-12-31T12:00:00Z"

patterns:
  # ===== HOOK LIBRARIES/SDKs =====
  - pattern_name: "Britfix - British English Conversion"
    hook_event: "PostToolUse"
    source_file: "README.md"
    external_link: "https://github.com/Talieisin/britfix"
    description: "Auto-converts American spellings to British English as files are written. Context-aware: only converts comments and docstrings, never identifiers or string literals."
    use_case:
      category: "Quality"
      when_to_use: "When professional credibility or compliance requires British English spelling in documentation and comments."

  - pattern_name: "CC Notify - Desktop Notifications"
    hook_event: "Stop"
    source_file: "README.md"
    external_link: "https://github.com/dazuiba/CCNotify"
    description: "Provides desktop notifications for Claude Code, alerting users to input needs or task completion with one-click jumps back to VS Code and task duration display."
    use_case:
      category: "Notification"
      when_to_use: "When working on long-running tasks and need to be alerted when Claude needs input or completes work."

  - pattern_name: "cchooks - Python SDK"
    hook_event: "Unknown"
    source_file: "README.md"
    external_link: "https://github.com/GowayLee/cchooks"
    description: "Lightweight Python SDK with clean API that simplifies writing hooks and integrating them into codebases, providing abstraction over JSON configuration files."
    use_case:
      category: "Productivity"
      when_to_use: "When building custom hooks in Python and want a cleaner API than raw JSON configuration."

  - pattern_name: "Claude Hook Comms (HCOM) - Multi-Agent Communication"
    hook_event: "SubagentStop"
    source_file: "README.md"
    external_link: "https://github.com/aannoo/claude-hook-comms"
    description: "Lightweight CLI tool for real-time communication between Claude Code sub agents using hooks. Enables multi-agent collaboration with @-mention targeting and live dashboard monitoring."
    use_case:
      category: "Coordination"
      when_to_use: "When orchestrating multiple Claude Code sub agents that need to communicate and coordinate with each other."

  - pattern_name: "claude-code-hooks-sdk - PHP SDK"
    hook_event: "Unknown"
    source_file: "README.md"
    external_link: "https://github.com/beyondcode/claude-hooks-sdk"
    description: "Laravel-inspired PHP SDK for building Claude Code hook responses with a clean, fluent API using expressive, chainable interface."
    use_case:
      category: "Productivity"
      when_to_use: "When building custom hooks in PHP/Laravel projects and want a fluent, chainable API."

  - pattern_name: "claude-hooks - TypeScript SDK"
    hook_event: "Unknown"
    source_file: "README.md"
    external_link: "https://github.com/johnlindquist/claude-hooks"
    description: "TypeScript-based system for configuring and customizing Claude Code hooks with a powerful and flexible interface."
    use_case:
      category: "Productivity"
      when_to_use: "When building custom hooks in TypeScript projects and need type-safe hook configuration."

  - pattern_name: "Claudio - Audio Feedback"
    hook_event: "Stop"
    source_file: "README.md"
    external_link: "https://github.com/ctoth/claudio"
    description: "No-frills library that adds delightful OS-native sounds to Claude Code via simple hooks for audio feedback on events."
    use_case:
      category: "Notification"
      when_to_use: "When you want audio feedback for Claude Code events without visual interruption."

  - pattern_name: "TDD Guard - Test-Driven Development Enforcement"
    hook_event: "PreToolUse"
    source_file: "README.md"
    external_link: "https://github.com/nizos/tdd-guard"
    description: "Hooks-driven system that monitors file operations in real-time and blocks changes that violate TDD principles."
    use_case:
      category: "Safety"
      when_to_use: "When enforcing test-driven development practices and want to block code changes without corresponding tests."

  - pattern_name: "TypeScript Quality Hooks"
    hook_event: "PostToolUse"
    source_file: "README.md"
    external_link: "https://github.com/bartolli/claude-code-typescript-hooks"
    description: "Quality check hook for Node.js TypeScript projects with TypeScript compilation, ESLint auto-fixing, and Prettier formatting. Uses SHA256 config caching for <5ms validation performance."
    use_case:
      category: "Quality"
      when_to_use: "When working on TypeScript projects and want automatic type checking, linting, and formatting after edits."

  # ===== HOOK-RELATED SLASH COMMANDS =====
  - pattern_name: "/create-hook - Hook Creation Wizard"
    hook_event: "Unknown"
    source_file: "resources/slash-commands/create-hook/create-hook.md"
    external_link: "https://github.com/omril321/automated-notebooklm/blob/main/.claude/commands/create-hook.md"
    description: "Slash command that intelligently prompts through hook creation with smart suggestions based on project setup (TypeScript, Prettier, ESLint detection)."
    use_case:
      category: "Productivity"
      when_to_use: "When creating new hooks and want guided assistance with project-aware suggestions."

  # ===== HOOK PATTERNS FROM TOOLING CATEGORY =====
  - pattern_name: "Code Quality Hooks (fcakyon)"
    hook_event: "PreToolUse"
    source_file: "README.md"
    external_link: "https://github.com/fcakyon/claude-codex-settings/tree/main/.claude/hooks"
    description: "Well-written hooks for code quality and tool usage regulation, including forcing Tavily over WebFetch tool."
    use_case:
      category: "Quality"
      when_to_use: "When you want to regulate which tools Claude uses and enforce code quality standards."

  # ===== PATTERNS FROM CREATE-HOOK COMMAND DOCUMENTATION =====
  - pattern_name: "TypeScript Type Checking Hook"
    hook_event: "PostToolUse"
    source_file: "resources/slash-commands/create-hook/create-hook.md"
    external_link: ""
    description: "Runs TypeScript compilation (tsc --noEmit) after file edits on .ts/.tsx files and provides error feedback via additionalContext."
    use_case:
      category: "Quality"
      when_to_use: "When working on TypeScript projects and want immediate type error feedback after edits."

  - pattern_name: "Pre-Edit Type Blocking Hook"
    hook_event: "PreToolUse"
    source_file: "resources/slash-commands/create-hook/create-hook.md"
    external_link: ""
    description: "Blocks file edits if TypeScript type errors exist, preventing further changes until types are fixed."
    use_case:
      category: "Safety"
      when_to_use: "When you want to prevent Claude from making changes to files with existing type errors."

  - pattern_name: "Auto-Format Hook"
    hook_event: "PostToolUse"
    source_file: "resources/slash-commands/create-hook/create-hook.md"
    external_link: ""
    description: "Automatically runs Prettier on edited files after changes, with suppressOutput:true for silent operation."
    use_case:
      category: "Quality"
      when_to_use: "When you want all edited files automatically formatted according to project Prettier config."

  - pattern_name: "ESLint Auto-Fix Hook"
    hook_event: "PostToolUse"
    source_file: "resources/slash-commands/create-hook/create-hook.md"
    external_link: ""
    description: "Runs ESLint with auto-fix after file edits to automatically correct linting issues."
    use_case:
      category: "Quality"
      when_to_use: "When you want automatic ESLint fixes applied after Claude edits files."

  - pattern_name: "Pre-Commit Lint Blocking"
    hook_event: "PreToolUse"
    source_file: "resources/slash-commands/create-hook/create-hook.md"
    external_link: ""
    description: "Blocks git commits if linting errors exist in staged files."
    use_case:
      category: "Safety"
      when_to_use: "When you want to prevent commits with linting errors."

  - pattern_name: "Test Validation Hook"
    hook_event: "PreToolUse"
    source_file: "resources/slash-commands/create-hook/create-hook.md"
    external_link: ""
    description: "Runs test suite before allowing commits to ensure tests pass."
    use_case:
      category: "Safety"
      when_to_use: "When you want to ensure tests pass before Claude commits changes."

  - pattern_name: "Build Validation Hook"
    hook_event: "PreToolUse"
    source_file: "resources/slash-commands/create-hook/create-hook.md"
    external_link: ""
    description: "Validates build succeeds before allowing commits."
    use_case:
      category: "Safety"
      when_to_use: "When you want to ensure the project builds successfully before committing."

  - pattern_name: "Secret Detection Hook"
    hook_event: "PreToolUse"
    source_file: "resources/slash-commands/create-hook/create-hook.md"
    external_link: ""
    description: "Scans for secrets/keys in code and blocks commits containing sensitive patterns. Exit code 2 blocks the operation."
    use_case:
      category: "Safety"
      when_to_use: "When you need to prevent accidental commits of API keys, passwords, or other secrets."

  - pattern_name: "Security Scan Hook"
    hook_event: "PostToolUse"
    source_file: "resources/slash-commands/create-hook/create-hook.md"
    external_link: ""
    description: "Runs security scanning on file changes to detect vulnerabilities."
    use_case:
      category: "Safety"
      when_to_use: "When you want security vulnerability scanning after file modifications."

external_resources:
  - name: "Britfix"
    url: "https://github.com/Talieisin/britfix"
    hook_types: ["PostToolUse"]

  - name: "CC Notify"
    url: "https://github.com/dazuiba/CCNotify"
    hook_types: ["Stop", "Notification"]

  - name: "cchooks (Python SDK)"
    url: "https://github.com/GowayLee/cchooks"
    hook_types: ["Unknown"]

  - name: "Claude Hook Comms (HCOM)"
    url: "https://github.com/aannoo/claude-hook-comms"
    hook_types: ["SubagentStop"]

  - name: "claude-code-hooks-sdk (PHP)"
    url: "https://github.com/beyondcode/claude-hooks-sdk"
    hook_types: ["Unknown"]

  - name: "claude-hooks (TypeScript)"
    url: "https://github.com/johnlindquist/claude-hooks"
    hook_types: ["Unknown"]

  - name: "Claudio (Audio)"
    url: "https://github.com/ctoth/claudio"
    hook_types: ["Stop", "Notification"]

  - name: "TDD Guard"
    url: "https://github.com/nizos/tdd-guard"
    hook_types: ["PreToolUse"]

  - name: "TypeScript Quality Hooks"
    url: "https://github.com/bartolli/claude-code-typescript-hooks"
    hook_types: ["PostToolUse"]

  - name: "fcakyon Code Quality Hooks"
    url: "https://github.com/fcakyon/claude-codex-settings/tree/main/.claude/hooks"
    hook_types: ["PreToolUse", "PostToolUse"]

  - name: "/create-hook Command"
    url: "https://github.com/omril321/automated-notebooklm/blob/main/.claude/commands/create-hook.md"
    hook_types: ["Unknown"]

  - name: "Official Claude Code Hooks Documentation"
    url: "https://docs.claude.com/en/docs/claude-code/hooks"
    hook_types: ["SessionStart", "PreToolUse", "PostToolUse", "PreCompact", "Stop", "SubagentStop", "UserPromptSubmit", "Notification"]

summary:
  total_patterns: 20
  by_hook_event:
    PostToolUse: 6
    PreToolUse: 7
    Stop: 2
    SubagentStop: 1
    Unknown: 4
  by_category:
    Quality: 7
    Safety: 6
    Productivity: 4
    Notification: 2
    Coordination: 1
  notes: |
    This is an index/collection repository (awesome list) that catalogs community hook implementations.
    The patterns extracted include both direct hook libraries and hook patterns documented in slash commands.
    Hook SDKs (cchooks, claude-hooks-sdk, claude-hooks) are marked as "Unknown" event type since they support all events.
    Many tooling resources in the broader list also mention hooks as part of their feature set.
'''

output_path = r'c:\Users\dsber\infinite\auto-company\strategy-nexus\02-projects\17-hook-pattern-research\02-resources\patterns\awesome.yaml'
os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(content)
print(f'Written to {output_path}')
