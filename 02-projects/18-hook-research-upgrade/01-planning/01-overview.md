---
id: 18-hook-research-upgrade
name: Hook Research Upgrade
status: PLANNING
description: "Load when user mentions 'hook upgrade', 'implement hooks', 'safety hooks', 'PreToolUse upgrade', 'TRASH pattern', 'context injection hooks'"
created: 2026-01-01
---

# Hook Research Upgrade

## Purpose

Upgrade the Nexus hook system with advanced patterns extracted from 9 community repositories (150+ patterns). Transform hooks from simple validators into powerful steering mechanisms with safety guards, context injection, and quality enforcement.

**Key Value**:
- Prevent dangerous operations (rm -rf, git reset --hard, .env access)
- Enable intelligent context injection (systemMessage, permissionDecisionReason)
- Improve code quality via automated formatters and TDD enforcement

---

## Success Criteria

**Must achieve**:
- [ ] PreToolUse safety gates blocking rm -rf, git force operations, .env access
- [ ] TRASH pattern implementation (move files instead of delete)
- [ ] systemMessage injection for invisible guidance on blocks
- [ ] Git protection (block force push, branch delete without confirmation)

**Nice to have**:
- [ ] Auto-formatter chain in PostToolUse (Ruff/Black for Python)
- [ ] Two-phase notification pattern (warn first, block on repeat)
- [ ] Statusline for context usage visualization
- [ ] Skill-aware context injection in UserPromptSubmit

---

## Context

**Background**:
- Existing hook system: SessionStart (context loading), basic PreToolUse, event streaming
- Research completed in Project 17: 150+ patterns from 9 repos, documented in 04-workspace/00-ai-native-org/hook-research/
- Key patterns identified: safety-net, TRASH, TDD-guard, tool redirection, systemMessage injection

**Stakeholders**:
- Nexus users (safety, quality)
- Developer (productivity, fewer mistakes)

**Constraints**:
- PreToolUse hooks must be <10ms (performance budget)
- PostToolUse hooks can be <50ms
- Must fail-open (allow on errors) except for safety blocks

---

## Timeline

**Target**: Complete Phase 1 (Safety) in current session

**Milestones**:
- Phase 1: Essential Safety (rm/git/.env protection) - Immediate
- Phase 2: Context Enhancement (systemMessage, tool redirection) - Next session
- Phase 3: Quality & Productivity (formatters, TDD) - Future

---

*Next: Complete plan.md to define your approach*
