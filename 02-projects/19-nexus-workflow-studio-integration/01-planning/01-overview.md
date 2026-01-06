---
id: 19-nexus-workflow-studio-integration
name: Nexus Workflow Studio Integration
status: PLANNING
description: "Load when user mentions 'workflow studio', 'cc-wf-studio', 'visual workflow', 'nexus visualization', 'skill visualizer', 'workflow editor'"
created: 2026-01-01
---

# Nexus Workflow Studio Integration

## Purpose

Integrate cc-wf-studio (Claude Code Workflow Studio) with the Nexus system to enable:

1. **Visual Design**: Design skill-chains and workflows using drag-and-drop interface
2. **Bidirectional Sync**: Import existing Nexus SKILL.md files into visual editor, export back
3. **Nexus-Native Nodes**: Custom node types for Orchestrator, Phase, SubSkill, and Project
4. **Skill Discovery**: Browse and use 03-skills/ directly from the workflow editor

This bridges the gap between Nexus's text-based skill system and visual workflow design.

---

## Success Criteria

**Must achieve**:
- [ ] Fork and customize cc-wf-studio for Nexus integration
- [ ] Add 4 Nexus-specific node types (Orchestrator, Phase, SubSkill, Project)
- [ ] Implement SKILL.md import parser
- [ ] Implement Nexus skill discovery (03-skills/ scanning)
- [ ] Export workflows to Nexus-compatible format
- [ ] Full bidirectional workflow editing

**Nice to have**:
- [ ] Visualize existing skill-chains (research-pipeline, etc.)
- [ ] Project visualization from 02-projects/
- [ ] Integration with nexus-loader.py for live metadata

---

## Context

**Background**:
- cc-wf-studio is an open-source VSCode extension for visual Claude Code workflow design
- Currently exports to `.claude/agents/*.md` and `.claude/commands/*.md` format
- Nexus uses a different structure: `03-skills/` with SKILL.md files and nested orchestrators

**Stakeholders**:
- Nexus users who want visual workflow design
- Non-technical users building skill-chains
- Team collaboration on complex workflows

**Constraints**:
- Must maintain compatibility with existing Nexus SKILL.md format
- Should not require changes to nexus-loader.py core
- Extension must work in VSCode environment

---

## Scope

**In Scope**:
- Custom node types for Nexus taxonomy
- Skill discovery from 03-skills/
- SKILL.md import/export
- Property panels for Nexus nodes
- Nexus metadata in workflow JSON

**Out of Scope**:
- Modifying nexus-loader.py
- Changes to existing SKILL.md structure
- Mobile or web editor (VSCode only)
- Real-time collaboration

---

*Next: Complete plan.md to define your approach*
