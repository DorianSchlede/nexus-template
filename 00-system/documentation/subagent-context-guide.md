# Subagent Context Injection Guide

**Problem**: Subagents (Task tool) do NOT receive SessionStart hook context. They only get the prompt you provide.

**Solution**: When spawning subagents, the main agent must inject the necessary Nexus context into their prompt.

---

## Why This Happens

The SessionStart hook fires ONLY for the main session:
- Main session → SessionStart fires → `<nexus-context>` injected
- Subagent spawned → NO hook fires → blank slate

Subagents receive:
- ✅ The prompt you provide
- ✅ CLAUDE.md files (via standard injection)
- ❌ NO `<nexus-context>` XML
- ❌ NO user goals, active projects, skills catalog
- ❌ NO orchestrator instructions

---

## Required Context for Subagents

When using the Task tool, ALWAYS include in the prompt:

### 1. File Reading Instructions (ALWAYS)

```
FIRST: Read these files for context:
- 00-system/core/orchestrator.md (Nexus rules)
- {relevant project/skill files}
```

### 2. Project Context (if working on a project)

```
You are working inside NEXUS on project: {project_id}
Project path: 02-projects/{project_id}/
Current task: {current_task}
```

### 3. Nexus Identity (for complex tasks)

```
You are operating inside the NEXUS system. Follow these rules:
- Use existing patterns from the codebase
- Don't create README/CHANGELOG files
- Update progress in 04-steps.md when completing tasks
```

---

## Subagent Prompt Templates

### For Project Work

```
You are a NEXUS subagent working on project {project_id}.

FIRST: Read these files for full context:
- 02-projects/{project_id}/01-planning/01-overview.md
- 02-projects/{project_id}/01-planning/04-steps.md
- {any other relevant files}

YOUR TASK: {specific task description}

RULES:
- Follow patterns from existing code
- Update 04-steps.md checkbox when done
- Don't create documentation unless asked
```

### For Exploration/Research

```
You are a NEXUS subagent exploring the codebase.

CONTEXT: {what we're looking for and why}

FIRST: Read 00-system/core/orchestrator.md to understand Nexus patterns.

YOUR TASK: {exploration task}

RETURN: {what information to report back}
```

---

## When to Include What

| Subagent Type | Include |
|---------------|---------|
| `Explore` | Orchestrator path, search scope |
| `general-purpose` | Full project context, file list, rules |
| `Plan` | Orchestrator, project files, constraints |

---

## Examples

### BAD (subagent has no Nexus context)

```
Task prompt: "Find all TypeScript files that handle authentication"
```

### GOOD (subagent knows the system)

```
Task prompt: "You are inside NEXUS. First read 00-system/core/orchestrator.md.
Then find all TypeScript files handling authentication in this codebase.
Report: file paths, key functions, and how they relate to the auth flow."
```

---

## KEY INSIGHT

The SessionStart hook only fires for the MAIN session. Subagents are blank slates - you must tell them everything they need to know.
