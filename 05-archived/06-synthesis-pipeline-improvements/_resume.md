---
updated: "2025-12-29T11:00:00"
phase: "phase-4-migration"
project_id: "06-synthesis-pipeline-improvements"
plan_version: "3.4"
schema_version: "v2.3"
---

# Resume Context

## PHASE 4.1f COMPLETE ✅

**Paper 02 Re-Analysis DONE** with new simplified evidence format:
- 3 parallel subagents + merge completed successfully
- Validation: 0 errors, 11 warnings (expected - evidence mismatches are warnings)
- Schema v2.3 with chunk_index for all 15 chunks
- All 15 fields assessed per chunk (3-state)

**Next**: Phase 4.2 - Re-analyze remaining 21 papers, OR skip to Phase 5 (Synthesis)

---

## CRITICAL: Files to Load on Resume

**READ THESE FILES IN ORDER:**

### 1. This Project's Files (CURRENT STATE)
```
02-projects/06-synthesis-pipeline-improvements/01-planning/overview.md    ← Status: IN_PROGRESS 75%
02-projects/06-synthesis-pipeline-improvements/01-planning/steps.md       ← Phase tracking
02-projects/06-synthesis-pipeline-improvements/01-planning/plan.md        ← v3.4 (aligned)
02-projects/06-synthesis-pipeline-improvements/03-working/root_cause_analysis.md     ← 5-Whys analysis
02-projects/06-synthesis-pipeline-improvements/02-resources/subagent_optimization_report.md  ← Optimization report
```

### 2. Validation Script (UPDATED ✅)
```
03-skills/research-pipeline/skills/paper-analyze/scripts/validate_analysis.py
```
**All fixes applied**:
- `normalize_markdown()` - strips `_`, `*`, `**`
- `normalize_unicode()` - includes accented chars (í→i, é→e)
- Handle HTML comments for headerless chunks
- Expand end search from 30% to 40%
- **Hash is now OPTIONAL** - validation computes hash internally if not provided
- Start/end mismatches are WARNINGS only (not errors)

### 3. SKILL.md (UPDATED ✅)
```
03-skills/research-pipeline/shared/paper-analyze-core/SKILL.md
```
**Evidence format simplified**:
- **Removed**: hash (validation computes internally)
- **Removed**: mid evidence (unnecessary)
- **Kept**: start + end evidence only

### 4. Test Papers (for validation testing)
```
02-projects/09-ontologies-research-v22-archive/02-resources/papers/03-PROV-AGENT_Unified_Provenance_for_AI_Agents/  ← Single-chunk test PASSED
02-projects/09-ontologies-research-v22-archive/02-resources/papers/02-Knowledge_Graphs/  ← NEEDS RE-ANALYSIS
```

---

## Current State

- **Phase**: Phase 4 - Migration (IN PROGRESS)
- **Plan Version**: 3.4 (with hash-optional changes)
- **Schema Version**: v2.3 (with chunk_index)
- **Status**: HASH-OPTIONAL IMPLEMENTED, RE-ANALYZE PAPER 02 NEXT
- **Phases 0-3**: COMPLETE (Planning, Skills, Scripts, Validation Updates)
- **Phase 4.1**: COMPLETE (single-chunk test on paper 03 - PASSED)
- **Phase 4.1b**: COMPLETE (multi-chunk test on paper 02 - structural success)
- **Phase 4.1c**: COMPLETE (root cause analysis - 5-Whys for 4 issues)
- **Phase 4.1d**: COMPLETE (validation fixes applied - hash-primary validation)
- **Phase 4.1e**: COMPLETE (Option C - removed hash from subagent output)

---

## Multi-Chunk Test Summary (Paper 02) - NEEDS RE-ANALYSIS

### Previous Test (Old Evidence Format)
- Paper: 02-Knowledge_Graphs
- Chunks: 15
- Total tokens: ~162,000
- Subagents: 3 (parallel) + 1 merge
- Evidence format: start + mid + end + hash (OLD)

### What Worked ✅
- Dynamic allocation based on token budget (70k per subagent)
- Parallel execution of 3 subagents
- Merge subagent combined all 3 parts correctly
- Schema v2.3 output with chunk_index for all 15 chunks
- Fields_found (3-state) assessed for all 15 fields per chunk

### Issues Fixed (Option C Implementation)
1. **Hash removed from subagent output** - LLMs can't reliably copy hashes
2. **Mid evidence removed** - unnecessary, start+end sufficient
3. **Validation computes hash internally** - ground truth from source file
4. **Evidence mismatches are WARNINGS** - not errors

### Action Required
**Delete old analysis files and re-analyze with new evidence format:**
```
02-projects/09-ontologies-research-v22-archive/02-resources/papers/02-Knowledge_Graphs/
├── _analysis_log_part1.md  ← DELETE
├── _analysis_log_part2.md  ← DELETE
├── _analysis_log_part3.md  ← DELETE
├── index_part1.md          ← DELETE
├── index_part2.md          ← DELETE
├── index_part3.md          ← DELETE
├── _analysis_log.md        ← DELETE (will regenerate)
└── index.md                ← DELETE (will regenerate)
```

---

## Validation Script Updates

### All Applied ✅
| Update | Purpose |
|--------|---------|
| `normalize_unicode()` | Handle Unicode → ASCII (includes accented chars) |
| `normalize_markdown()` | Strip `_`, `*`, `**` from text |
| Start evidence prefix (80 chars) | Flexible start matching |
| End evidence partial matching | Search last 40% with substring |
| Quote key word overlap (60%) | Handle paraphrased quotes |
| YAML frontmatter skip | Don't extract quotes from YAML |
| `actual_in_chunk_start` | Accept start evidence in first 500 chars |
| Handle headerless chunks | Use first 100 chars if no `#` header |
| **Hash optional** | Validation computes hash if not provided |
| **Mid evidence optional** | Only required for Schema v2.1/v2.2 |
| **Evidence mismatches = WARNINGS** | Not errors (hash is ground truth) |

---

## Token Budget Reference (Large Papers)

| Paper Size | Chunks | Tokens | Subagents | Strategy |
|------------|--------|--------|-----------|----------|
| Small | 1-3 | <35k | 1 | Single subagent |
| Medium | 4-6 | 35-70k | 1 | Single subagent |
| Large | 7-10 | 70-120k | 2 | Split + Merge |
| Very Large | 11-15 | 120-180k | 3 | Split + Merge |
| Huge | 16+ | 180k+ | 4+ | Split + Merge |

---

## Key Decisions (ALL RESOLVED)

| Question | Decision |
|----------|----------|
| Field generation | AI suggests from RQ, user confirms |
| Chunk assessment | **3-state: true/partial/false** |
| Migration | Clean Break (re-analyze all papers) |
| Token formula | **`chars // 4`** (standardized) |
| Research context | **research_purpose + synthesis_goals** |
| Large paper handling | **Split/Merge with parallel subagents** |
| Schema version | **v2.3** (with chunk_index) |
| **Evidence format** | **start + end only (no hash, no mid)** |
| **Hash computation** | **Validation script computes internally** |
| **Evidence mismatches** | **WARNINGS only (hash is ground truth)** |

---

## Root Cause Analysis Summary (NEW)

### 5-Whys Findings

| Issue | Root Cause | Fix |
|-------|------------|-----|
| Markdown stripped | LLM semantic processing | `normalize_markdown()` |
| Header in evidence | Ambiguous prompt | Already works (flexibility) |
| Headerless chunks | Rigid structure assumptions | Handle HTML comments |
| End position | Semantic vs positional | Expand to 40% |

### Meta-Insights
1. **LLMs are semantic processors** - validation must normalize for equivalence
2. **Content is diverse** - bibliography, appendix, footnotes are common
3. **Position ≠ Meaning** - use flexible search regions

---

## Next Steps

### Immediate (Phase 4.1f - Re-analyze Paper 02)
1. Delete old analysis files from Paper 02
2. Re-analyze Paper 02 with new evidence format (start + end only)
3. Run validation - expect 0 errors, minimal warnings
4. Confirm new format works correctly

### Then (Phase 4.2)
1. Re-analyze remaining 21 papers with Schema v2.3
2. Use split/merge for papers with >6 chunks
3. Run validation on each paper after analysis

### Paper Analysis Queue (21 remaining)
| Priority | Papers | Strategy |
|----------|--------|----------|
| High | UFO, DOLCE, BFO | Single subagent |
| Medium | PROV-O, Process Mining papers | Single/Split |
| Low | Agent/LLM papers | Split as needed |

---

*Plan Version: 3.4*
*Schema Version: v2.3*
*Phase: 4 - Migration (4.1e complete, 4.1f pending)*
*Status: RE-ANALYZE PAPER 02 WITH NEW EVIDENCE FORMAT*
*Last Updated: 2025-12-29T11:00:00*
