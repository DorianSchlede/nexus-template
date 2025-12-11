# Memory Map

<!-- AI CONTEXT FILE -->
<!-- Purpose: Help AI navigate the memory system -->
<!-- Updated by: System (static framework documentation) -->

> **Purpose**: Help AI navigate the memory system
>
> **Audience**: AI agent (loaded every session via --startup)
>
> **Maintenance**: Static system documentation

---

## Memory System Overview

The `01-memory/` folder contains context that persists across all sessions:

### Core Files (Always Loaded)

**goals.md** - What you want to achieve
- Current role and work context
- Short-term goal (3 months)
- Long-term vision (1-3 years)
- Success metrics

**core-learnings.md** - What you've learned
- What works well (successes)
- What to avoid (mistakes)
- Best practices (patterns)
- Insights (strategic realizations)

**memory-map.md** - This file
- System navigation for AI
- Structure explanation

**user-config.yaml** - Your preferences
- Language preference
- Timezone
- Date format

---

## Session Reports (Historical)

**session-reports/** - Generated after each session
- Dated session summaries
- Progress tracking
- Key decisions and outcomes
- Never loaded automatically (only on request)

---

## When AI Loads Memory Files

**Every Session** (via --startup):
- goals.md
- memory-map.md
- user-config.yaml

**Pattern Recognition**:
- core-learnings.md (when similar situations arise)

**Historical Context**:
- session-reports/ (only when user explicitly asks about past sessions)

---

## How Memory Evolves

**Quick Start** (Smart Defaults):
- Template files auto-created on first run
- User can work immediately
- Personalize anytime with "setup goals" skill

**Personalized** (After setup-goals skill):
- goals.md → Populated with user's actual goals
- user-config.yaml → Language and preferences set
- core-learnings.md → Grows over time via close-session

---

**This map helps the AI understand your memory system structure.**
