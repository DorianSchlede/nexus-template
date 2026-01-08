---
id: 29-nexus-context-loading-optimization-and-xml-restructure
name: Nexus Context Loading Optimization and XML Restructure
status: COMPLETE
description: "Complete rethink and 10x optimization of Nexus context injection architecture"
created: 2026-01-06
completed: 2026-01-08
project_path: 02-projects/29-nexus-context-loading-optimization-and-xml-restructure/
---

# Nexus Context Loading Optimization and XML Restructure

## Project Files

| File | Purpose |
|------|---------|
| 01-overview.md | This file - purpose, success criteria |
| 02-discovery.md | Dependencies, patterns, risks |
| 03-plan.md | Approach, decisions |
| 04-steps.md | Execution tasks |
| 02-resources/ | Reference materials |
| 03-working/ | Work in progress |
| 04-outputs/ | Final deliverables |

---

## Purpose

**10x the Nexus context injection system through complete architectural optimization**

Not just restructuring - **rethinking**:
- What information Claude actually needs at startup vs mid-session vs execution
- Optimal ordering for cognitive load and decision-making
- Abstraction layers to reduce redundancy
- Pattern recognition to minimize explicit instructions
- Progressive disclosure vs upfront loading

**Core question**: What's the MINIMUM context needed to make Claude maximally effective?

---

## Success Criteria

**Must achieve**:
- [ ] All injected context is valid, well-formed XML (parseable, structured)
- [ ] Token reduction: Measure before/after startup context size
- [ ] Single source of truth for routing (orchestrator.md only)
- [ ] Consolidated state/stats data (one structured section)
- [ ] Clear cognitive ordering (what Claude reads first matters)
- [ ] Zero redundancy between sections
- [ ] Skill loading rules + skill metadata co-located
- [ ] Action-first ordering (what to do NOW at top, context/reference at bottom)

**Optimization targets**:
- [ ] Lazy-loading patterns (don't send what won't be used)
- [ ] Semantic skill matching (1-2 trigger words + intent, not exhaustive lists)
- [ ] Compressed encodings where appropriate (XML attributes vs verbose blocks)
- [ ] Abstract common patterns (DRY principle for instructions)
- [ ] Progressive disclosure design (Level 1: action → Level 2: context → Level 3: reference)

**Nice to have**:
- [ ] A/B test different orderings to find optimal cognitive flow
- [ ] Metrics on which sections Claude actually uses vs ignores
- [ ] Self-optimizing context (track what gets referenced, prune what doesn't)

---

## Context

**Background**:
Current SessionStart hook dumps ~40-50K tokens of mixed XML/markdown with:
- Routing rules scattered between orchestrator.md and system instructions
- Skill descriptions with exhaustive keyword lists
- Verbose project XML blocks
- Menu display instructions duplicated
- No clear "read this first" hierarchy
- Unknown cognitive ordering (does Claude read top-to-bottom? Does order matter?)

**Stakeholders**:
- You (Daniel) - faster startup, cleaner mental model
- Claude instance - clear hierarchy, optimal decision-making flow
- Future Nexus users - better performance, lower token costs
- The system itself - maintainability, extensibility

**Constraints**:
- Must maintain backward compatibility with existing projects/skills
- Cannot modify default Claude Code behavior (only Nexus-specific hooks)
- XML must be well-formed and parseable by standard parsers
- Changes must be testable (before/after comparison)

**Unknowns to investigate**:
- Does injection order affect Claude's decision-making?
- What sections does Claude actually reference vs ignore?
- Can we abstract patterns from orchestrator.md into reusable rules?
- What's the optimal balance between explicit instructions vs implicit patterns?
- Are there cognitive load patterns we should optimize for?

---

## The Big Questions

1. **Information Architecture**: What goes where and why?
2. **Cognitive Ordering**: What should Claude see first for optimal decision-making?
3. **Abstraction Layers**: What patterns can we extract and reference instead of repeating?
4. **Lazy Loading**: What can be loaded on-demand vs upfront?
5. **Progressive Disclosure**: Can we structure context in levels (immediate → relevant → reference)?
6. **Pattern Recognition**: Can Claude infer from structure instead of explicit instructions?
7. **Measurement**: How do we know it's better? What metrics matter?

---

*Next: Fill in 02-discovery.md - analyze current patterns, identify optimization opportunities*
