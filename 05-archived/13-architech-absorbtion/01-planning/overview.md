---
id: 13-architech-absorbtion
name: Architech Absorbtion
status: COMPLETE
description: "Extract and document patterns from Architech - implementation in separate projects"
created: 2025-12-31
completed: 2026-01-05
archived: 2026-01-05
source: mutagent-obsidian/architech/
type: extraction-and-planning
---

# Architech Absorbtion

## Project Scope

**This project is EXTRACTION + PLANNING only. No implementation.**

| Deliverable | In This Project? | Where? |
|-------------|------------------|--------|
| Pattern extraction docs | YES | This project |
| Implementation planning | YES | This project |
| Actual code changes | **NO** | Separate projects (14, 15, etc.) |

## Purpose

1. **Perfect detailed pattern extraction** from Architech (mutagent-obsidian)
2. **Granular implementation planning** that becomes specs for separate projects

**The revelation**: Architech was built to learn how to build systems. The learning is complete. Extract the value, document it perfectly, then implement in focused projects.

---

## Source of Truth

**IMPORTANT**: There are TWO Architechs. The correct one is:

| Location | Status |
|----------|--------|
| `auto-company/architech/` | LEGACY - Old software dev version, unused |
| **`mutagent-obsidian/architech/`** | **ACTIVE** - 4-layer framework, 27 Python scripts, 12 entity types |

**Reference**: See [HYPERMAP.md](../02-resources/HYPERMAP.md) for complete documentation.

---

## Success Criteria

**This project (extraction + planning)**:
- [ ] All 9 patterns fully documented with code samples
- [ ] Implementation specs ready for each pattern
- [ ] Future project stubs defined (what each implementation project needs)

**Future projects (implementation)**:
- [ ] Project 14: Nexus Shortcuts - Pattern D implementation
- [ ] Project 15: Nexus Resume Schema - Pattern 4 implementation
- [ ] Project 16: Nexus Quality Gates - Pattern 3 implementation
- [ ] etc.

**Final state**:
- [ ] Legacy Architech (auto-company) archived
- [ ] Single CLAUDE.md entry point, no system confusion

---

## Context

**Background**: Three systems exist:
- **Nexus-v4** (strategy-nexus): Operational productivity system, 100+ skills
- **Architech** (mutagent-obsidian): Active meta-framework, 27 Python scripts, 12 entity types
- **Old Architech** (auto-company): Legacy, unused since Nov 28

**Stakeholders**: Dorian (operator), Future Claude instances

**Constraints**:
- Must not break Nexus stability
- Must not add unnecessary complexity
- Incremental implementation required

---

## Patterns (REVISED Priority Order)

| # | Pattern | Source | Value | Priority |
|---|---------|--------|-------|----------|
| **C+D** | **Dynamic Shortcut System** | `build_shortcut_registry.py` + `shortcut_resolver.py` | Self-documenting shortcuts, no static YAML | **#1 - Extract first** |
| **2** | **Entity System (01-SYSTEM)** | `01-system/` (entire layer) | Full architecture extraction | **#2 - Hyperdetail** |
| **6** | **META Layer (00-META)** | `00-meta/` (entire layer) | Control plane, agent memory | **#3 - NEW** |
| 4 | Resume Schema | `00-meta/01-agents/meta-architect/memory/` | State tracking, handoff | #4 |
| 3 | Quality Gate Framework | `01-system/00-definitions/entity-types/07-checklist.md` | PASS/CONCERNS/FAIL/WAIVED | #5 |
| 5 | Self-Assessment Loop | `00-meta/01-agents/meta-architect/memory/` | Weekly synthesis | #6 |
| 1 | Mental Model Smart Selection | `01-system/08-automation/scripts/mental_models/` | Situation-aware suggestions | Optional |
| B | Context Bundler | `scripts/context_bundler.py` (300 lines) | Load multiple files | After C+D |
| A | Entity Loader | `hooks/entity_system/build_entity_definitions.py` | Frontmatter → XML | Reference only |

**Key insights**:
- **C+D combined** - Dynamic registry + resolver. Self-documenting, NO static YAML.
- **Pattern 2 expanded** - Not just entity validation, but ENTIRE 01-system layer architecture.
- **Pattern 6 NEW** - META layer controls system layer. Must understand interplay.

---

## Non-Goals

- Port the full 4-layer hierarchy (simplify for Nexus)
- Port 73 software domain entities (domain-specific)
- Port trace-aggregator (overkill for now)
- Create new navigation systems (use existing Nexus loader)

---

## Key Sources (mutagent-obsidian/architech/)

| Path | What to Extract |
|------|-----------------|
| `01-system/08-automation/scripts/mental_models/select_mental_models.py` | Smart selection algorithm |
| `01-system/00-definitions/entity-types/*.md` | Entity validation patterns |
| `01-system/08-automation/hooks/shortcut_system/build_shortcut_registry.py` | Registry builder pattern |
| `00-meta/01-agents/meta-architect/memory/` | Self-assessment patterns |
| `HYPERMAP.md` | Complete cross-reference |

---

## Architech Stats (from HYPERMAP)

| Metric | Count |
|--------|-------|
| Entity Types | 12 |
| Active Agents | 3 |
| Python Scripts | 27 |
| Test Cases | 150+ |
| Mental Models | 30+ |
| Lines of Code | 8,000+ |

---

## Output Deliverables

This project produces extraction documents in `02-resources/extractions/`:

| # | Pattern | Extraction Doc | Implementation Project |
|---|---------|----------------|----------------------|
| **C+D** | Dynamic Shortcut System | `extraction-CD-shortcuts.md` | Project 14 |
| **2** | Entity System (01-SYSTEM) | `extraction-2-entity-system.md` | Project 15 |
| **6** | META Layer (00-META) | `extraction-6-meta-layer.md` | Project 16 |
| 4 | Resume Schema | `extraction-4-resume.md` | Project 17 |
| 3 | Quality Gates | `extraction-3-gates.md` | Project 18 |
| 5 | Self-Assessment | `extraction-5-assessment.md` | Project 19 |
| 1 | Mental Models | `extraction-1-models.md` | Optional |
| B | Context Bundler | `extraction-B-bundler.md` | After C+D |

**Each extraction doc contains**:
1. Source code analysis (key functions, line counts)
2. Architecture documentation (hyperdetail)
3. Nexus integration design
4. Files to create/modify
5. Implementation checklist
6. Test plan

---

*This project extracts patterns. Implementation happens in separate projects.*
