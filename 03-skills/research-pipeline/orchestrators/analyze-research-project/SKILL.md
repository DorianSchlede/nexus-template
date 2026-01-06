---
name: analyze-research-project
description: "Analyze research papers (Phase 2: analysis only). Load when user says 'analyze research project', 'execute research project', 'continue research', 'run analysis', or mentions a research project by name after planning is complete. Expects analysis-ready chunks from create-research-project. After analysis, use synthesize-research-project for synthesis."
resume_instructions: |
  ## Context Checkpoint: _resume.md

  This skill requires maintaining a `_resume.md` file for context recovery.

  **Location**: `{project_path}/_resume.md`

  **Maintenance Rules**:
  1. UPDATE `_resume.md` when context usage reaches ~60% (before compaction risk)
  2. UPDATE after completing each batch of paper analysis
  3. UPDATE after validation steps complete
  4. RELOAD `_resume.md` immediately after any context summary/compaction

  **_resume.md Format**:
  ```yaml
  ---
  updated: "{timestamp}"
  phase: "analysis|validation|complete"
  project_id: "{project_id}"
  ---

  # Resume Context

  ## Current State
  - Phase: {current phase}
  - Papers analyzed: {N}/{total}
  - Papers validated: {N}/{total}
  - Last completed batch: {batch_number}

  ## Pending Work
  - Papers remaining: [list]
  - Next batch: {batch_number}
  - Blocked by: {any blockers}

  ## Completed Work
  - Batches complete: [1, 2, 3...]
  - Papers with index.md: [list]
  - Validation passed: [list]

  ## Next Actions
  1. {immediate next step}
  2. {following step}
  ```

  **On Resume After Compaction**:
  1. Read `{project_path}/_resume.md` first
  2. Read `01-planning/plan.md` for orchestrator instructions
  3. Continue from `## Next Actions`
---

# Analyze Research Project (Phase 2: Analysis Only)

Analyze research papers by generating index.md files with extracted data. **This skill expects analysis-ready chunks** - use `create-research-project` for paper selection, download, and preprocessing. **After analysis, use `synthesize-research-project` for cross-paper synthesis.**

---

## The 3-Skill Chain

```
create-research-project  →  analyze-research-project  →  synthesize-research-project
(Phase 1: Acquisition)      (Phase 2: Analysis)          (Phase 3: Synthesis)
        ↓                           ↓                            ↓
    _briefing.md               index.md per paper         _synthesis_report.md
    chunks ready               extracted frontmatter      FULL MARKDOWN REPORT
```

---

## When to Use

| User Says | Load This Skill |
|-----------|-----------------|
| "analyze research project {name}" | Yes |
| "execute research project {name}" | Yes |
| "continue research {name}" | Yes |
| "run analysis on research project" | Yes |
| "create research project" | No → use `create-research-project` |
| "new research on [topic]" | No → use `create-research-project` |
| "synthesize research project" | No → use `synthesize-research-project` |
| "generate synthesis" | No → use `synthesize-research-project` |

---

## Prerequisites

Before using this skill, verify:
- [x] Research project exists in `02-projects/`
- [x] `02-resources/_briefing.md` exists (extraction schema)
- [x] `02-resources/_analysis_kit.md` exists (subagent context)
- [x] `02-resources/_extraction_guide.md` exists (field examples)
- [x] `01-planning/plan.md` has `## Orchestrator Instructions` section
- [x] At least 1 paper folder has `_metadata.json` (chunks ready)

**Step 1 validates all prerequisites.** If any missing, execution stops with clear error message directing to the correct create-research-project step.

---

## Workflow Overview

```
analyze-research-project (THIS SKILL)
        │
        ├─ PHASE A: VALIDATION
        │   ├─ Step 0: Initialize TodoWrite (tracking)
        │   └─ Step 1: Validate readiness (chunks exist)
        │
        ├─ PHASE B: ANALYSIS
        │   ├─ Step 2: Analyze papers → index.md + _analysis_log.md
        │   └─ Step 3: Validate analysis logs
        │
        └─ PHASE C: COMPLETION
            └─ Step 4: Mark analysis READY_FOR_SYNTHESIS

→ HANDOFF TO: synthesize-research-project (Phase 3)
```

---

## Step 0: Initialize Task Tracking

**MANDATORY: Use TodoWrite at start of skill:**

```
TodoWrite with initial todos:
- [ ] Validate readiness (Step 1)
- [ ] Analyze papers → index.md + _analysis_log.md (Step 2)
- [ ] Validate analysis logs (Step 3)
- [ ] Mark analysis READY_FOR_SYNTHESIS (Step 4)
```

**Update todos as each step completes.**

---

## Progress Tracking: steps.md and plan.md

### Reading plan.md for Orchestrator Instructions

**At start of execution, read `01-planning/plan.md` for:**
- Paper Corpus table (which papers to analyze)
- Subagent allocation rules (how many subagents per paper)
- Orchestrator Instructions (exact prompts for subagents)
- Current State (to update as execution progresses)

**Use the prompts in plan.md "Orchestrator Instructions" section for spawning subagents.**

### Marking Checkboxes in steps.md

**After completing each step, mark the corresponding checkbox in `01-planning/steps.md`:**

| After Step | Mark Complete in steps.md |
|------------|---------------------------|
| Step 2 | `- [x] Analyze papers with subagents` |
| Step 3 | `- [x] Validate analysis logs` |
| Step 4 | `- [x] Mark analysis ready for synthesis` |

**Use Edit tool to change `- [ ]` to `- [x]` for each completed task.**

### Updating plan.md Current State

**After Step 2 (Analysis)**, update plan.md:
```markdown
## Current State

| Metric | Value |
|--------|-------|
| Phase | 4-Analysis (complete) |
| Papers Approved | 25 |
| Papers Downloaded | 18 |
| Papers with Chunks | 18 |
| Papers Analyzed | 17 |
| Total Chunks | 52 |
```

**Also update Paper Corpus table status column:**
- Change `ready` to `analyzed` for each completed paper
- Change to `failed` for papers that failed validation

**After Step 4 (Analysis Complete)**, update plan.md:
```markdown
## Current State

| Metric | Value |
|--------|-------|
| Phase | READY_FOR_SYNTHESIS |
| Papers Approved | 25 |
| Papers Downloaded | 18 |
| Papers with Chunks | 18 |
| Papers Analyzed | 17 |
| Total Chunks | 52 |
```

**Next**: Run `synthesize-research-project` for Phase 3.

---

# PHASE A: VALIDATION

## Step 1: Validate Readiness

**Check prerequisites and paper readiness:**

### 1.1 Prerequisite Checks (Fail Fast)

```python
project_path = "02-projects/NN-{slug}/"

# Check briefing exists
if not exists(project_path / "02-resources/_briefing.md"):
    fail("""
    Missing _briefing.md - research question not defined.
    Run 'create research project' Step 2 first.
    """)

# Check analysis kit exists
if not exists(project_path / "02-resources/_analysis_kit.md"):
    fail("""
    Missing _analysis_kit.md - subagent context not generated.
    Run 'create research project' Step 10 first.
    """)

# Check extraction guide exists
if not exists(project_path / "02-resources/_extraction_guide.md"):
    fail("""
    Missing _extraction_guide.md - field examples not defined.
    Run 'create research project' Step 11 first.
    """)

# Check orchestrator instructions in plan.md
plan = read(project_path / "01-planning/plan.md")
if "## Orchestrator Instructions" not in plan:
    fail("""
    Missing orchestrator instructions in plan.md.
    Run 'create research project' Step 12 first.
    """)
```

### 1.2 Paper Readiness Check

```python
# Find papers with chunks (have _metadata.json)
papers_ready = []
for folder in (project_path / "02-resources/papers").iterdir():
    if folder.is_dir() and (folder / "_metadata.json").exists():
        papers_ready.append(folder.name)

if len(papers_ready) == 0:
    fail("No papers preprocessed - run create-research-project first")

# Check for papers needing analysis (no index.md yet)
papers_to_analyze = []
for paper in papers_ready:
    if not (project_path / f"02-resources/papers/{paper}/index.md").exists():
        papers_to_analyze.append(paper)
```

### Legacy Compatibility Check

If project was created with an older version (missing _analysis_kit.md, _extraction_guide.md, or orchestrator instructions):
```
This project was created with an older version.
Missing prerequisite files must be generated first.

Run these commands to complete setup:
  1. Generate _analysis_kit.md (Step 10)
  2. Generate _extraction_guide.md (Step 11)
  3. Add orchestrator instructions to plan.md (Step 12)

Or re-run: "create research project {name}" to regenerate.
```

### Display Status

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RESEARCH PROJECT READY FOR EXECUTION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Research Project: {name}
Research Question: "{RQ}"

Papers ready:     {N} (with chunks)
Papers to analyze: {M} (no index.md yet)
Already analyzed:  {K} (have index.md)

Briefing: _briefing.md ✓

Proceeding with Phase 2 (Analysis)...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Step 1.5: Read Pre-Calculated Subagent Allocation

**The allocation was calculated in Phase 1 Step 12. READ it from plan.md - DO NOT recalculate!**

### Read Allocation Table from plan.md

```python
# Read the pre-calculated allocation from plan.md
plan = read(f"{project_path}/01-planning/plan.md")

# Parse the "## Subagent Allocation Plan" section
allocation_table = parse_markdown_table(plan, "## Subagent Allocation Plan")

# Expected format:
# | Paper ID | Chunks | Est. Tokens | Subagents | Splits |
# |----------|--------|-------------|-----------|--------|
# | Paper_A  | 4      | ~47,000     | 1         | 1-4    |
# | Paper_B  | 10     | ~120,000    | 2         | 1-6, 7-10 |

total_subagents = extract_value(plan, "**Total subagents**:")
```

### Verify Allocation Exists

```python
if "## Subagent Allocation Plan" not in plan:
    fail("""
    Missing subagent allocation plan in plan.md.
    This should have been created in Phase 1 Step 12.
    Run 'create research project' Step 12 to generate allocation.
    """)
```

### Display Pre-Calculated Plan

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SUBAGENT ALLOCATION (from plan.md)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

| Paper | Chunks | Est. Tokens | Subagents | Splits |
|-------|--------|-------------|-----------|--------|
| Small_Paper | 3 | ~35,000 | 1 | 1-3 |
| Medium_Paper | 6 | ~70,000 | 1 | 1-6 |
| Large_Paper | 10 | ~120,000 | 2 | 1-6, 7-10 |
| Survey_Paper | 16 | ~190,000 | 3 | 1-6, 7-12, 13-16 |

Total subagents: 7
Max concurrent: 15
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Proceeding with pre-planned allocation...
```

**CRITICAL**: The allocation is pre-calculated in Phase 1 Step 12. Do NOT modify or recalculate here. If allocation seems wrong, go back to Phase 1 and regenerate.

---

# PHASE B: ANALYSIS

## Step 2: Analyze Papers

**Read plan.md "Orchestrator Instructions" section for subagent prompts.**

The plan.md contains:
- Paper Corpus table with chunk counts and subagent allocation
- Exact prompts for standard papers (1 subagent)
- Exact prompts for large papers (2+ subagents + merge)
- Concurrency settings

### SUBAGENT INPUT CONTRACT (STRICT - Gap G13 Fix)

**Each subagent receives explicit file access rules in its prompt:**

```markdown
## INPUT CONTRACT (STRICT)

### Files You MUST Read (in this order)
1. `03-skills/research-pipeline/shared/paper-analyze-core/SKILL.md` (methodology)
2. `{project_path}/02-resources/_briefing.md` (research question + schema)
3. `{project_path}/02-resources/_analysis_kit.md` (subagent context)
4. `{project_path}/02-resources/_extraction_guide.md` (field examples + vocabulary)
5. `{paper_path}/_metadata.json` (chunk info)
6. `{paper_path}/{paper_id}_1.md`
7. `{paper_path}/{paper_id}_2.md`
[... exact chunk list from _metadata.json]

### Files You MUST NOT Read
- ANY `.pdf` file
- ANY folder except `{paper_path}/`
- ANY file in `04-outputs/`
- ANY other paper folder in `02-resources/papers/`
- ANY file starting with `.` (hidden files)
- ANY file outside project directory

### Directory Traversal FORBIDDEN
- Do NOT use `../` paths
- Do NOT follow symbolic links
- Stay within `{project_path}/` boundary

VIOLATION = Analysis fails validation.
```

**Include this INPUT CONTRACT in every subagent prompt.**

### Subagent Spawning from Pre-Calculated Allocation

**For each row in the Subagent Allocation Plan table:**

1. Read the `Subagents` column (pre-calculated count)
2. Read the `Splits` column (pre-calculated chunk ranges)
3. If `Subagents == 1` → Spawn single subagent for all chunks
4. If `Subagents > 1` → Spawn one subagent per split range, then spawn merge subagent

**Example: Large_Paper with Subagents=2, Splits="1-6, 7-10"**
```
Spawn Task 1: Analyze chunks 1-6 → index_part1.md
Spawn Task 2: Analyze chunks 7-10 → index_part2.md
Wait for both...
Spawn Merge Task: Combine index_part1.md + index_part2.md → index.md
```

**CRITICAL**: Follow the pre-calculated allocation EXACTLY. Do NOT recalculate or modify splits.

**SUBAGENT PROMPT TEMPLATE (with G22a, G22b context):**

```python
Task(
  subagent_type="general-purpose",
  prompt=f"""
## Paper Analysis Task: {paper_id}

## INPUT CONTRACT (STRICT)
{INPUT_CONTRACT_TEXT}  # See above

## CONTEXT
Research Purpose: {research_purpose}  # G22a - WHY this research matters
Synthesis Goals: {synthesis_goals}    # G22b - What synthesis will aggregate

## PROCESSING CONTRACT
1. Read files IN ORDER listed in INPUT CONTRACT
2. For EVERY chunk, assess EVERY field: true/partial/false (see Step 1b calibration)
3. Extract items only for true/partial fields
4. Record evidence (start + end) for each chunk
5. Use Structured N/A format for fields not found (Gap G18)

## OUTPUT CONTRACT
Write these files:
1. `{paper_path}/_analysis_log.md` (Schema v2.3)
2. `{paper_path}/index.md` (MUST use YAML frontmatter format below)

### CRITICAL: index.md MUST use this EXACT YAML frontmatter structure:

```yaml
---
paper_id: "{paper_id}"
title: "{extracted title}"
authors: []
year: null
chunks_expected: {from _metadata.json}
chunks_read: {must equal chunks_expected}
analysis_complete: true
schema_version: "2.3"

# CHUNK-LEVEL FIELD ASSESSMENT (REQUIRED for synthesis routing)
chunk_index:
  1:
    token_count: {len(chunk_content) // 4}
    fields_found:
{fields_found_template}
  2:
    token_count: {len(chunk_content) // 4}
    fields_found:
{fields_found_template}
  # ... repeat for ALL chunks

# EXTRACTION FIELDS (from _briefing.md extraction_schema)
{field_name}:
  - item: "Extracted item name"
    chunk: 1
    lines: "128-133"
    quote: "Exact quote from chunk..."

# Use Structured N/A for fields not found
{field_name_not_found}:
  - item: "NOT_FOUND"
    chunk: null
    lines: null
    quote: null
    reason: "Paper does not discuss this topic"
---
```

### fields_found template (generate from _briefing.md extraction_schema):
```yaml
      {field_1}: true|partial|false
      {field_2}: true|partial|false
      # ... ALL fields from extraction_schema MUST be listed
      # true = extractable content present
      # partial = mentioned but not detailed
      # false = not present in chunk
```

**VALIDATION**: Synthesis pipeline will FAIL if chunk_index is missing or malformed.

Do NOT read other files. Do NOT read the PDF.
"""
)
```

**Replace placeholders:**
- `{project_path}` - Absolute path to project folder
- `{paper_path}` - Absolute path to paper folder
- `{paper_id}` - Paper folder name
- `{research_purpose}` - From `_briefing.md` (G22a)
- `{synthesis_goals}` - From `_analysis_kit.md` (G22b)
- `{INPUT_CONTRACT_TEXT}` - Full INPUT CONTRACT from above

### Concurrency Settings

- **Max concurrent subagents**: 15 (parallel analysis for speed)
- **Timeout per paper**: 5 minutes
- **Retry on failure**: 1 attempt

### Subagent Outputs Per Paper

```
02-resources/{paper}/
├── {paper}.pdf           # Original (unchanged)
├── {paper}_1.md          # Chunk 1 (unchanged)
├── {paper}_2.md          # Chunk 2 (unchanged)
├── _metadata.json        # Chunk index (unchanged)
├── _analysis_log.md      # NEW: Schema v2.0 validation log
└── index.md              # NEW: Analysis output
```

### Progress Display

```
Analyzing papers...
  [1/18] Auto_TA... COMPLETE (4 chunks, 2.3 min)
  [2/18] SFT_TA... COMPLETE (3 chunks, 1.8 min)
  [3/18] De_Paoli... IN_PROGRESS...
  ...

Analyzed: 15/18 papers
In progress: 3
Failed: 0
```

---

## Step 3: Validate Analysis Logs

**Run validation on each completed analysis:**

```bash
python 03-skills/research-pipeline/skills/paper-analyze/scripts/validate_analysis.py \
  02-projects/NN-{slug}/02-resources/ \
  --output 04-outputs/_validation_report.md
```

### Validation Checks

1. Schema version = 2.0
2. All steps completed
3. All chunks read (recorded in log)
4. Multi-point evidence matches actual chunks
5. index.md created and valid YAML frontmatter

### Validation Results Display

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
VALIDATION RESULTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ PASSED:  16 papers (validation complete)
⚠ WARNING: 1 paper (minor issues, usable)
✗ FAILED:  1 paper (evidence mismatch)

Failed papers:
  • Paper_XYZ - Chunk 3 evidence mismatch

Re-analyze failed papers? [Y/N]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Handle Failures

| User Input | Action |
|------------|--------|
| **Y** | Respawn subagent for failed papers (1 retry) |
| **N** | Exclude from synthesis, note in report |

### After Retry

If still failing after retry:
```
Paper_XYZ failed validation after retry.
Excluding from synthesis. See _validation_report.md for details.

Continue with {N} validated papers? [Y/N]
```

---

# PHASE C: COMPLETION

## Step 4: Mark Analysis READY_FOR_SYNTHESIS

**Update project status to indicate readiness for synthesis:**

### Update overview.md

```yaml
# overview.md
status: READY_FOR_SYNTHESIS
analysis_completed_at: "{timestamp}"
```

### Update plan.md Current State

```markdown
## Current State

| Metric | Value |
|--------|-------|
| Phase | READY_FOR_SYNTHESIS |
| Papers Analyzed | 17 |
| Papers Validated | 16 |
| Total Chunks | 52 |
```

### Final Summary

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ANALYSIS COMPLETE - READY FOR SYNTHESIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Project: {name}
Research Question: "{RQ}"

Papers analyzed: 17/18
Validation rate: 94%

Outputs:
  📋 04-outputs/_validation_report.md (analysis validation)

Per-paper analysis:
  📁 02-resources/{paper}/index.md (17 papers)

NEXT STEP:
  Run "synthesize research project {name}" to generate synthesis report.

  This will:
  • Read all index.md files
  • Spawn batch extraction subagents
  • Aggregate patterns per field
  • Generate full _synthesis_report.md with citations

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Files Created by This Skill

| File | Location | Purpose |
|------|----------|---------|
| `_analysis_log.md` | 02-resources/papers/{paper}/ | Validation log (v2.0) |
| `index.md` | 02-resources/papers/{paper}/ | Analysis output with YAML frontmatter |
| `_validation_report.md` | 04-outputs/ | Analysis validation results |

**Note**: Synthesis files are created by `synthesize-research-project` (Phase 3).

---

## Error Handling

| Step | Error | Action |
|------|-------|--------|
| Step 1 | No chunks found | Redirect to create-research-project |
| Step 1 | No _briefing.md | Fail with clear message |
| Step 2 | Subagent fails | Retry once, then mark failed |
| Step 2 | Subagent timeout | **PARTIAL SAVE** (see below) |
| Step 3 | Evidence mismatch | Offer re-analysis or exclusion |
| Step 3 | Schema mismatch | Re-analyze with correct schema |
| Step 4 | <3 papers validated | Warn, proceed with caution |
| Step 4 | 0 papers validated | Fail - nothing to analyze |

### Timeout Partial Save Protocol (Gap G16)

**When timeout occurs, subagent MUST write partial progress:**

```yaml
# In _analysis_log.md when timeout occurs:
error_handling:
  timeout_occurred: true
  partial_success: true
  chunks_completed: [1, 2, 3]  # Which chunks were fully analyzed
  chunks_remaining: [4, 5]     # Which chunks need re-analysis
  recovery_notes: "Resume from chunk 4. Chunks 1-3 have complete extractions."

# In index.md - include partial chunk_index:
chunk_index:
  1: {token_count: ..., hash: ..., fields_found: {...}}
  2: {token_count: ..., hash: ..., fields_found: {...}}
  3: {token_count: ..., hash: ..., fields_found: {...}}
  # 4, 5 missing - will be added on resume
```

**On resume**, orchestrator:
1. Reads `chunks_remaining` from `_analysis_log.md`
2. Spawns subagent with `start_from_chunk: 4`
3. Subagent appends to existing index.md

**Resume prompt addition:**
```markdown
## RESUME MODE
Partial analysis exists. Read existing:
- `{paper_path}/_analysis_log.md` - check `chunks_completed`
- `{paper_path}/index.md` - has partial chunk_index

Start analysis from chunk {start_from_chunk}.
APPEND to existing chunk_index (don't overwrite).
```

---

## Concurrency & Performance

| Setting | Value | Notes |
|---------|-------|-------|
| Max concurrent subagents | 15 | Parallel analysis for speed |
| Timeout per paper | 5 min | Generous for large papers |
| Retry on failure | 1 | Single retry before exclusion |

---

## References

- [paper-analyze skill](../../skills/paper-analyze/SKILL.md)
- [paper-analyze-core methodology](../../shared/paper-analyze-core/SKILL.md)
- [Analysis Validation Script](../../skills/paper-analyze/scripts/validate_analysis.py)
- [synthesize-research-project](../synthesize-research-project/SKILL.md) (Phase 3)

---

**Version**: 5.0 (2025-12-28)
**Changes**:
- v2.0: Removed download/preprocess steps (now in create-research-project)
- v2.1: Added Step 4.5 Synthesis Validation with anti-hallucination checks
- v3.0: Added prerequisite checks in Step 1 for _analysis_kit.md, _extraction_guide.md, plan.md orchestrator instructions
- v4.0: Renamed from execute-research-project, removed synthesis (now in synthesize-research-project)
- v5.0: Added INPUT CONTRACT for subagents (G13), Partial Save on timeout (G16), research_purpose/synthesis_goals context (G22a, G22b), Schema v2.3 reference
**Handles**: Phase 2 (Analysis) only
**Receives from**: `create-research-project` (expects chunks + analysis kit + extraction guide + orchestrator instructions)
**Hands off to**: `synthesize-research-project` (provides papers with index.md)
