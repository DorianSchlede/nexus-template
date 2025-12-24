---
name: execute-research-project
description: "Execute research projects (Phase 2: analyze and synthesize). Load when user says 'execute research project', 'continue research', 'run research project', or mentions a research project by name after planning is complete. Expects analysis-ready chunks from create-research-project."
---

# Execute Research Project (Phase 2: Analysis & Synthesis)

Execute research projects by analyzing preprocessed papers and generating synthesis. **This skill expects analysis-ready chunks** - use `create-research-project` for paper selection, download, and preprocessing.

---

## When to Use

| User Says | Load This Skill |
|-----------|-----------------|
| "execute research project {name}" | Yes |
| "continue research {name}" | Yes |
| "run analysis on research project" | Yes |
| "analyze research project" | Yes |
| "create research project" | No → use `create-research-project` |
| "new research on [topic]" | No → use `create-research-project` |

---

## Prerequisites

Before using this skill, verify:
- [x] Research project exists in `02-projects/`
- [x] `overview.md` has `type: research`
- [x] `02-resources/_briefing.md` exists (extraction schema)
- [x] At least 1 paper folder has `_metadata.json` (chunks ready)

**If prerequisites not met:**
```
This research project isn't ready for execution.

Missing: Paper chunks (no _metadata.json found)

Papers must be downloaded and preprocessed first.
Run: "create research project {name}" to complete acquisition.
```

---

## Workflow Overview

```
execute-research-project (THIS SKILL)
        │
        ├─ PHASE A: VALIDATION
        │   ├─ Step 0: Initialize TodoWrite (tracking)
        │   └─ Step 1: Validate readiness (chunks exist)
        │
        ├─ PHASE B: ANALYSIS
        │   ├─ Step 2: Analyze papers → index.md + _analysis_log.md
        │   └─ Step 3: Validate analysis logs
        │
        ├─ PHASE C: SYNTHESIS
        │   ├─ Step 4: Generate synthesis
        │   └─ Step 4.5: Validate synthesis (NEW - anti-hallucination)
        │
        └─ PHASE D: COMPLETION
            └─ Step 5: Mark project COMPLETE
```

---

## Step 0: Initialize Task Tracking

**MANDATORY: Use TodoWrite at start of skill:**

```
TodoWrite with initial todos:
- [ ] Validate readiness (Step 1)
- [ ] Analyze papers → index.md + _analysis_log.md (Step 2)
- [ ] Validate analysis logs (Step 3)
- [ ] Generate synthesis (Step 4)
- [ ] Mark project COMPLETE (Step 5)
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
| Step 4 | `- [x] Generate cross-paper synthesis` |
| Step 5 | `- [x] Mark project complete` |

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

**After Step 5 (Complete)**, update plan.md:
```markdown
## Current State

| Metric | Value |
|--------|-------|
| Phase | COMPLETE |
| Papers Approved | 25 |
| Papers Downloaded | 18 |
| Papers with Chunks | 18 |
| Papers Analyzed | 17 |
| Total Chunks | 52 |
```

---

# PHASE A: VALIDATION

## Step 1: Validate Readiness

**Check that papers are preprocessed and ready:**

```python
# Load project
project_path = "02-projects/NN-{slug}/"

# Check briefing exists
briefing = project_path / "02-resources/_briefing.md"
if not briefing.exists():
    fail("Missing _briefing.md - research question not defined")

# Find papers with chunks (have _metadata.json)
papers_ready = []
for folder in (project_path / "02-resources").iterdir():
    if folder.is_dir() and (folder / "_metadata.json").exists():
        papers_ready.append(folder.name)

if len(papers_ready) == 0:
    fail("No papers preprocessed - run create-research-project first")

# Check for papers needing analysis (no index.md yet)
papers_to_analyze = []
for paper in papers_ready:
    if not (project_path / f"02-resources/{paper}/index.md").exists():
        papers_to_analyze.append(paper)
```

### Legacy Compatibility Check

If `_selection_log.md` exists but no chunks found:
```
This project was created with an older version (v2.x).
Papers need to be downloaded and preprocessed first.

Options:
  1. Run "create research project {name}" to complete acquisition
  2. Manually download papers and run preprocessing

The selection log shows {N} papers were approved.
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

# PHASE B: ANALYSIS

## Step 2: Analyze Papers

**Read plan.md "Orchestrator Instructions" section for subagent prompts.**

The plan.md contains:
- Paper Corpus table with chunk counts and subagent allocation
- Exact prompts for standard papers (1 subagent)
- Exact prompts for large papers (2 subagents + merge)
- Concurrency settings

### Subagent Spawning from plan.md

**For each paper in the Paper Corpus table with status=ready:**

1. Check chunk count in table
2. If <=12 chunks → Use "Standard Paper" prompt from plan.md
3. If >12 chunks → Use "Large Paper" (2 subagents + merge) from plan.md

**Example from plan.md:**
```
Task(
  subagent_type="general-purpose",
  prompt="""
Analyze paper: {paper_id}

Read IN ORDER:
1. 03-skills/paper-analyze-core/SKILL.md (methodology)
2. {project_path}/02-resources/_briefing.md (research question + schema)
3. {project_path}/02-resources/{paper_id}/_metadata.json (chunk info)
4. {project_path}/02-resources/{paper_id}/{paper_id}_1.md
... (all chunks listed in _metadata.json)

Follow the 7-step methodology. Write:
1. {project_path}/02-resources/{paper_id}/_analysis_log.md (Schema v2.0)
2. {project_path}/02-resources/{paper_id}/index.md (analysis output)

Do NOT read other files. Do NOT read the PDF.
"""
)
```

**Replace `{project_path}` and `{paper_id}` with actual values from the project.**

### Concurrency Settings

- **Max concurrent subagents**: 3 (avoid rate limits)
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
python 03-skills/paper-analyze/scripts/validate_analysis.py \
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

# PHASE C: SYNTHESIS

## Step 4: Generate Synthesis

**Use `paper-synthesize` skill:**

```
[Load paper-synthesize skill]

Collection: 02-projects/NN-{slug}/02-resources/
Research question: {from _briefing.md}

Read all index.md files (validated papers only)
Aggregate findings by extraction field
Generate cross-paper synthesis
```

### Synthesis Process

1. **Read all index.md YAML frontmatter** from validated papers
2. **Group findings by field** (from extraction_schema in _briefing.md)
3. **Identify themes** across papers
4. **Note gaps and conflicts** between papers
5. **Generate structured synthesis**

### Output: `04-outputs/_synthesis.md`

```markdown
---
synthesized_at: "{timestamp}"
papers_included: 17
papers_excluded: 1
research_question: "{RQ}"
---

# Research Synthesis

## Executive Summary

{2-3 paragraph summary of key findings across all papers}

## Key Themes

### Theme 1: {Name}
- **Papers**: [Auto_TA, SFT_TA, DeTAILS]
- **Summary**: {What these papers collectively say}
- **Key findings**:
  - Finding 1 (source: Auto_TA)
  - Finding 2 (source: SFT_TA)

### Theme 2: {Name}
...

## Extraction Field Summary

### {Field 1 from extraction_schema}
| Paper | Value | Notes |
|-------|-------|-------|
| Auto_TA | ... | ... |
| SFT_TA | ... | ... |

### {Field 2}
...

## Gaps and Limitations

- Gap 1: {What's missing from the literature}
- Limitation 1: {Methodological concerns}

## Recommendations

Based on this synthesis:
1. {Actionable recommendation}
2. {Actionable recommendation}

## Paper-by-Paper Summary

| Paper | Key Contribution | Relevance |
|-------|-----------------|-----------|
| Auto_TA | Full automation with RLHF | Critical |
| SFT_TA | Multi-agent + fine-tuning | Critical |
...

## Appendix: Excluded Papers

| Paper | Reason |
|-------|--------|
| Paper_XYZ | Validation failed (evidence mismatch) |
```

---

## Step 4.5: Validate Synthesis (NEW)

**After generating synthesis, validate quality:**

### Run Validation Script

```bash
python 03-skills/paper-synthesize/scripts/validate_synthesis.py \
  02-projects/NN-{slug}/ \
  --spot-check 10 \
  --output 04-outputs/_synthesis_validation.md
```

### Validation Checks

| Check | Threshold | Action |
|-------|-----------|--------|
| Frontmatter complete | 100% required | Regenerate synthesis |
| Paper references exist | >90% | Warn, continue |
| Spot-check verification | >70% | Regenerate synthesis |
| Coverage | >60% | Warn, continue |

### Validation Results Display

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SYNTHESIS VALIDATION RESULTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Frontmatter: ✓ COMPLETE
Paper References: ✓ 38/38 exist (100%)
Spot-Check: ✓ 9/10 verified (90%)
Coverage: ✓ 85% patterns documented

Overall: PASSED

Report saved to: 04-outputs/_synthesis_validation.md
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Handle Validation Failure

If spot-check verification <70% or frontmatter incomplete:

```
Synthesis validation FAILED.

Issues:
  ✗ Spot-check: 5/10 verified (50% < 70% threshold)
  ✗ Missing frontmatter: papers_read

Regenerating synthesis with validation contract...
```

Then respawn synthesis subagent with explicit validation contract:

```
VALIDATION CONTRACT (MANDATORY):
1. You MUST read ALL index.md files (I will verify)
2. You MUST include papers_read: [...] listing actual paper_ids
3. Every claim MUST cite paper_id (e.g., "MAPoRL: 91%")
4. I will spot-check 10 claims against source papers
```

### Two-Pass Synthesis (Optional - High Reliability)

For critical projects, use two-pass synthesis:

**Pass 1: Aggregation**
```
Task(
  subagent_type="general-purpose",
  prompt="Read all index.md, aggregate patterns, generate draft synthesis..."
)
```

**Pass 2: Verification**
```
Task(
  subagent_type="general-purpose",
  prompt="Cross-reference 20% of claims in synthesis against source papers.
  Update frontmatter with:
  - validation.spot_checks_passed: N
  - validation.spot_checks_total: N
  - validation.confidence: high|medium|low"
)
```

---

# PHASE D: COMPLETION

## Step 5: Mark Project COMPLETE

**Update project status and generate final outputs:**

### Update overview.md

```yaml
# overview.md
status: COMPLETE
completed_at: "{timestamp}"
```

### Generate Quality Metrics

**Output: `04-outputs/_quality_metrics.md`**

```markdown
---
generated_at: "{timestamp}"
---

# Quality Metrics

## Analysis Coverage

| Metric | Value |
|--------|-------|
| Papers selected | 25 |
| Papers downloaded | 18 |
| Papers analyzed | 17 |
| Papers validated | 16 |
| Papers in synthesis | 16 |

## Validation Summary

| Status | Count | Percentage |
|--------|-------|------------|
| Passed | 16 | 94% |
| Warnings | 1 | 6% |
| Failed | 1 | 6% |

## Analysis Time

| Metric | Value |
|--------|-------|
| Total analysis time | 32 min |
| Avg per paper | 1.9 min |
| Synthesis time | 4 min |
```

### Final Summary

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RESEARCH PROJECT COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Project: {name}
Research Question: "{RQ}"

Papers analyzed: 17/18
Validation rate: 94%

Outputs:
  📄 04-outputs/_synthesis.md (cross-paper synthesis)
  📋 04-outputs/_validation_report.md (analysis validation)
  📊 04-outputs/_quality_metrics.md (coverage stats)

Per-paper analysis:
  📁 02-resources/{paper}/index.md (17 papers)

Next steps:
  • Review synthesis for insights
  • Export findings to other projects
  • Archive or close project

Say "close session" to save learnings.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Files Created by This Skill

| File | Location | Purpose |
|------|----------|---------|
| `_analysis_log.md` | 02-resources/{paper}/ | Validation log (v2.0) |
| `index.md` | 02-resources/{paper}/ | Analysis output |
| `_validation_report.md` | 04-outputs/ | Analysis validation results |
| `_synthesis.md` | 04-outputs/ | Cross-paper synthesis |
| `_synthesis_validation.md` | 04-outputs/ | Synthesis validation report (NEW) |
| `_quality_metrics.md` | 04-outputs/ | Quality stats |

---

## Error Handling

| Step | Error | Action |
|------|-------|--------|
| Step 1 | No chunks found | Redirect to create-research-project |
| Step 1 | No _briefing.md | Fail with clear message |
| Step 2 | Subagent fails | Retry once, then mark failed |
| Step 2 | Subagent timeout | Log timeout, continue to next |
| Step 3 | Evidence mismatch | Offer re-analysis or exclusion |
| Step 3 | Schema mismatch | Re-analyze with correct schema |
| Step 4 | <3 papers validated | Warn about limited synthesis |
| Step 4 | 0 papers validated | Fail - nothing to synthesize |
| Step 4.5 | Spot-check <70% | Regenerate synthesis with contract |
| Step 4.5 | Missing frontmatter | Regenerate synthesis with contract |
| Step 4.5 | Coverage <60% | Warn, continue (may be acceptable) |

---

## Concurrency & Performance

| Setting | Value | Notes |
|---------|-------|-------|
| Max concurrent subagents | 3 | Avoid rate limits |
| Timeout per paper | 5 min | Generous for large papers |
| Retry on failure | 1 | Single retry before exclusion |
| Min papers for synthesis | 3 | Warn if fewer |

---

## References

- [paper-analyze skill](../paper-analyze/SKILL.md)
- [paper-analyze-core methodology](../paper-analyze-core/SKILL.md)
- [paper-synthesize skill](../paper-synthesize/SKILL.md)
- [Analysis Validation Script](scripts/validate_analysis.py)
- [Synthesis Validation Script](../paper-synthesize/scripts/validate_synthesis.py)
- [Synthesis Validation Contract](../paper-synthesize/references/synthesis_validation_contract.md)

---

**Version**: 2.1 (2025-12-19)
**Changes**:
- v2.0: Removed download/preprocess steps (now in create-research-project)
- v2.1: Added Step 4.5 Synthesis Validation with anti-hallucination checks
**Handles**: Phase 2 (Analysis & Synthesis) only
**Receives from**: `create-research-project` (expects chunks in 02-resources/)
