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

**roadmap.md** - How you'll get there
- Goal breakdown into milestones
- Timeline and sequencing
- Key activities per milestone

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

**Strategic Discussion**:
- roadmap.md (when talking about milestones, timeline, planning)

**Pattern Recognition**:
- core-learnings.md (when similar situations arise)

**Historical Context**:
- session-reports/ (only when user explicitly asks about past sessions)

---

## How Memory Evolves

**Onboarding** (Projects 00-03):
- goals.md → Created in Project 00
- roadmap.md → Created in Project 00
- user-config.yaml → Created in Project 00
- core-learnings.md → Starts empty, grows over time

**Operational** (After onboarding):
- close-session updates core-learnings.md automatically
- close-session creates session reports
- User updates goals.md and roadmap.md as needed

---

**This map helps the AI understand your memory system structure.**
