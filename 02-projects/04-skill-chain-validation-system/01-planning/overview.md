---
id: 04-skill-chain-validation-system
name: Skill-Chain Validation System
status: ARCHIVED
description: "ARCHIVED - Validation kann manuell erfolgen. Over-Engineering für das Problem."
created: 2025-12-27
archived: 2025-12-28
type: build
archive_reason: "First Principles Analysis: Validation braucht kein eigenes System. Manuelles Prüfen (ls, grep) reicht. Fokus auf create-skill-algorithm stattdessen."
---

# Skill-Chain Validation System

## Purpose

Create a generic system to validate algorithm execution via skill-chains. A skill-chain is a sequence of skills that must execute in order, with each skill producing outputs that the next skill consumes.

**Problem**: Currently no way to systematically verify that:
- All expected outputs from a skill exist
- Outputs meet quality contracts (valid YAML, required fields present)
- Gates between skills pass before proceeding
- Failed steps can be identified and fixed

**Solution**: A validation framework with:
- YAML-defined contracts for skill-chains
- Automated validation of outputs against contracts
- 3-step fix workflow (research → plan → execute)
- Historical tracking of validation runs

---

## Success Criteria

**Must achieve**:
- [ ] Can validate any skill-chain defined in YAML format
- [ ] Provides actionable feedback on what's missing/broken
- [ ] Works with existing research pipeline without modifications
- [ ] Generates clear reports for human review
- [ ] Successfully validates 02-ontologies-research project

**Nice to have**:
- [ ] Trend detection for recurring failures
- [ ] Auto-fix for common issues
- [ ] Extensible to other skill-chains (content creation, interview analysis)

---

## Context

**Background**: The research pipeline (create-research-project → execute-research-project) has 9 skills with complex handoffs. Currently validation is scattered across individual scripts. Need a unified approach.

**Stakeholders**:
- User (me) - wants confidence that pipelines work correctly
- Future skill authors - need clear contracts to follow

**Constraints**:
- Must work with existing skill structure (no breaking changes)
- Python scripts for automation
- YAML for human-readable contracts
- Markdown reports for output

---

## Timeline

**Target**: Build incrementally, test against Ontologies project

**Milestones**:
- Contract schema designed
- Research pipeline contract created
- Validation scripts working
- Tested against real project
- Packaged as reusable skill

---

*Next: Complete plan.md to define approach*
