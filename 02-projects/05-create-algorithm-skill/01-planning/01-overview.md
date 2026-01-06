---
id: 05-create-algorithm-skill
name: Create Algorithm Skill
status: IN_PROGRESS
description: "Load when user mentions 'create algorithm', 'new algorithm', 'define pipeline', 'create workflow', 'algorithm wizard'. META-SKILL for generating nested skill structures."
created: 2025-12-27
updated: 2025-12-28
type: build
linked_skill: 03-skills/create-skill-algorithm/SKILL.md
---

# Create Algorithm Skill

## Purpose

Create a META-SKILL that enables users to define new algorithms (nested skill structures) through an interactive workflow. An algorithm is a sequence of coordinated skills (like the research pipeline) that work together to accomplish complex multi-phase tasks.

**Problem**: Currently, creating an algorithm like the research pipeline requires:
- Deep understanding of Nexus skill structure
- Manual creation of orchestrator skills
- Manual creation of sub-skills
- Manual definition of contracts/validation
- No standardized pattern to follow

**Solution**: An interactive skill that:
1. Guides users through defining algorithm metadata, skills, outputs, and gates
2. Generates YAML contract files (`_chain.yaml`)
3. Generates skill folder structures with templates
4. Creates validation integration hooks
5. Produces documentation with Mermaid diagrams (`_index.md`)

---

## Success Criteria

**Must achieve**:
- [x] Interactive workflow asks right questions to define an algorithm
- [x] Generates valid YAML contract (`_chain.yaml`)
- [x] Generates complete skill folder structure
- [x] Generated skills follow Nexus conventions
- [ ] Successfully creates interview-analysis algorithm as test

**Nice to have**:
- [x] Auto-generates Mermaid diagrams (`_index.md`)
- [ ] Provides best-practice suggestions during workflow
- [ ] Detects common mistakes and warns user

---

## Context

**Background**: The research pipeline (9 skills) is a complex algorithm that took significant effort to design. We want to make creating similar pipelines much easier.

**Stakeholders**:
- Users wanting to create custom workflows
- Future Nexus developers
- AI agents needing structured algorithms

**Constraints**:
- Must follow existing Nexus skill patterns
- Python scripts for generation
- YAML for contracts
- Jinja2 for templates

**Dependencies**:
- Research pipeline as reference implementation
- Nexus skill structure conventions

**Note**: P04 (validate-skill-chain) was ARCHIVED. Validation can be done manually with `ls`, `grep`.

---

## Implementation Status

**Skill Location**: `03-skills/create-skill-algorithm/`

The skill is already implemented with:
- `SKILL.md` - Interactive 10-step workflow
- `scripts/generate_chain.py` - Main orchestrator
- `templates/*.j2` - Jinja2 templates for all generated files

**Milestones**:
1. ~~Contract schema finalized~~ ✓
2. ~~Templates designed (Jinja2)~~ ✓
3. ~~Interactive workflow implemented~~ ✓
4. ~~Generation scripts working~~ ✓
5. ~~Documentation generation~~ ✓
6. [ ] Test with interview-analysis algorithm

---

*Status: ACTIVE - Skill implemented, needs testing*
