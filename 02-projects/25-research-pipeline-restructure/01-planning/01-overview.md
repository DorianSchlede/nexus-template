---
id: 25-research-pipeline-restructure
name: Research Pipeline Restructure
status: COMPLETE
description: "Load when user mentions 'research phase', 'research template', 'improve create-project', 'add research step', or 'project research'"
created: 2026-01-04
completed: 2026-01-05
---

# Research Pipeline Restructure

## Purpose

Add a **discovery step** to the create-project workflow - a structured 5-15 minute exploration BEFORE planning to surface dependencies, risks, and existing patterns.

**Core insight**: Planning quality depends on information quality. Unknown dependencies cause the most expensive rework.

**Clarification**: This is NOT the same as `template-research.md` (which is a project TYPE for research-focused projects). This is a **workflow step** that runs before planning for ANY project type.

**Problem**: Projects skip exploration and jump straight to planning, leading to:
- Missed dependencies discovered mid-execution
- Assumptions not tested until too late
- Rework when existing patterns/skills could have been reused
- Incomplete understanding of technical landscape

**Value**: 5-15 min upfront discovery saves hours of mid-execution rework.

**Key Decisions**:
1. AI **always** proposes discovery - user can decline with simple "skip"
2. Time-boxed to 5-15 minutes max (not a lengthy research phase)
3. Output auto-populates plan.md Dependencies section (immediate value)
4. Focus is tight: dependencies, existing patterns, risks - NOT broad exploration

---

## Success Criteria

**Must achieve**:
- [x] Discovery step template created (tight, actionable sections)
- [x] Discovery workflow integrated into plan-project skill (after init, before overview)
- [x] Discovery outputs auto-populate plan.md Dependencies section
- [x] Skip path is trivially easy ("skip" or "no" proceeds immediately)
- [x] Time-boxed to 5-15 minutes max

**Nice to have**:
- [ ] Subagent integration for parallel codebase scanning
- [ ] Integration with paper-search skill for academic research projects

---

## Context

**Background**:
- Current create-project workflow: Type Selection -> Planning (overview -> plan -> steps) -> Execution
- Need: Research phase BEFORE planning to explore domain, dependencies, existing patterns
- This was originally Phase 2 in Project 24 (Project Skills Research & Resume Expansion)
- Project 24 completed the Resume/Hook system (Phases 0-3), research improvements are now separate

**Stakeholders**:
- Users working on complex projects requiring upfront research
- Users integrating with existing systems/skills
- AI agents needing comprehensive context for planning

**Constraints**:
- Must maintain backward compatibility with existing projects
- Must work within Nexus v4 framework patterns
- Research output must be consumable by planning phase
- Must integrate with existing create-project script and templates

---

## Timeline

**Target**: Complete within 1-2 work sessions

**Milestones**:
- Phase 1: Template development
- Phase 2: Workflow integration
- Phase 3: Testing & validation

---

*Next: Complete plan.md to define your approach*
