---
id: 06-synthesis-pipeline-improvements
name: Synthesis Pipeline Improvements
status: COMPLETE
progress: 100
description: "Load when user mentions 'improve synthesis', 'fix synthesis accuracy', 'subagent allocation', 'synthesis script', 'programmatic subagents', 'chunk allocation'"
created: 2025-12-28
plan_version: "3.3"
schema_version: "v2.3"
---

# Synthesis Pipeline Improvements

## Purpose

**Problem**: The research pipeline's synthesis phase (Phase 3) has critical issues:
1. **Coverage gaps** - Subagents miss patterns because they can't read enough chunks
2. **Inefficient handover** - Too much verbose text passed to subagents
3. **Token limits** - No smart allocation of chunks per subagent
4. **No pre-spawn planning** - Chunk allocation is ad-hoc, not calculated by script

**Solution**: Create a programmatic subagent spawning system that:
- Pre-calculates chunk allocation based on ~70k token budget per subagent
- Auto-generates subagent prompts from YAML routing tables
- Verifies subagent output via chunk hashes
- Standardizes output format across all synthesis levels

**Value**: Research synthesis that captures ALL patterns from ALL papers with verifiable citations.

---

## Success Criteria

**Must achieve**:
- [ ] Python script that calculates chunks-per-subagent from routing YAML
- [ ] Python script that generates subagent prompts from allocation plan
- [ ] Chunk hash verification in subagent output schema
- [ ] Run successful synthesis on ontologies-research project (21 papers)
- [ ] All subagents produce standardized markdown with citations

**Nice to have**:
- [ ] Progress tracking for long synthesis runs
- [ ] Resume capability if synthesis is interrupted
- [ ] Parallel vs sequential spawning options

---

## Context

**Background**:
- `synthesize-research-project` skill exists but relies on manual subagent spawning
- Current approach: orchestrator skill describes what to do, AI interprets loosely
- Need: Deterministic, script-driven allocation and prompt generation

**Stakeholders**:
- Research pipeline users who need accurate synthesis
- Future projects using the research-pipeline skill-chain

**Constraints**:
- Must work with existing index.md and _briefing.md formats
- Must integrate with existing routing script (prepare_synthesis_chunks.py)
- ~70k token budget per subagent for chunk reading
- Subagents split by field (entity_types, ai_integration, etc.), not by paper

---

## Scope

**In Scope**:
- calculate_subagent_allocation.py - Determines chunks per subagent per field
- generate_subagent_prompts.py - Creates ready-to-spawn prompt files
- verify_subagent_output.py - Post-spawn verification of chunk reading
- Updated synthesize-research-project skill to use scripts
- Test run on ontologies-research project

**Out of Scope** (UPDATED - some items now in scope):
- ~~Changes to Phase 1 (create-research-project)~~ → Now in scope: G5, G22a
- ~~Changes to Phase 2 (analyze-research-project)~~ → Now in scope: G13, G16
- ~~Changes to paper-analyze-core methodology~~ → Now in scope: G1, G3, G18

---

## Current Status (2025-12-28)

**Phase 0: Planning** ✅ COMPLETE
**Phase 1: Skill Documentation** ✅ COMPLETE
**Phase 2: Core Scripts** ✅ COMPLETE (5/5 scripts created)
**Phase 3: Validation Updates** ✅ COMPLETE (validate_analysis.py updated)
**Phase 4: Migration** 🔄 IN PROGRESS
- Project 02 backup created
- _briefing.md updated with research_purpose (G22a)
- _analysis_kit.md updated with synthesis_goals (G22b)
- 23 papers pending re-analysis with Schema v2.3

**Next Step**: Re-analyze papers with new schema (Phase 4.2)

**Scripts Created**:
- `build_synthesis_routing.py` - L1 routing with sparsity check
- `calculate_subagent_allocation.py` - L2 batch allocation
- `generate_subagent_prompts.py` - L3 prompt generation
- `verify_subagent_output.py` - L5 verification
- `aggregate_patterns.py` - L6 pattern aggregation
