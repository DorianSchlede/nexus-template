# Phase 2: Execution Workflow

Detailed workflow for the Execution phase of a research project.

---

## Overview

Phase 2 transforms approved papers into analyzed, validated, and synthesized research outputs.

**Inputs**: `_selection_log.md` with approved papers
**Outputs**: `index.md` for each paper, `_synthesis.md`, `_validation_report.md`

---

## Prerequisites

Before starting Phase 2:
- [x] Phase 1 complete (Planning Gate passed)
- [x] `_selection_log.md` exists with `approved_by_user: true`
- [x] `_briefing.md` exists with extraction schema
- [x] At least 1 paper approved

---

## Step-by-Step Workflow

### 1. Download Approved Papers

**Action**: Fetch PDFs for all approved papers

**For each paper in `_selection_log.md`**:

```python
for paper in approved_papers:
    # Create paper folder
    paper_folder = f"02-resources/{sanitize_name(paper.title)}"
    mkdir(paper_folder)

    # Download PDF
    if paper.open_access and paper.pdf_url:
        download(paper.pdf_url, f"{paper_folder}/{paper_name}.pdf")
    elif paper.doi:
        # Try Unpaywall, then other sources
        pdf_url = find_open_access(paper.doi)
        if pdf_url:
            download(pdf_url, f"{paper_folder}/{paper_name}.pdf")
        else:
            log_warning(f"No open access for: {paper.title}")
```

**Progress Tracking**:
```
Downloading papers...
  [1/20] Using LLMs for TA... OK
  [2/20] GPT-4 Qualitative... OK
  [3/20] Multi-Agent QDA... WARN: No open access, skipped
  ...
Downloaded: 18/20 papers
Skipped: 2 (no open access)
```

**Update `_selection_log.md`**:
```yaml
download_status:
  downloaded: 18
  skipped: 2
  skipped_papers:
    - title: "Paper Title"
      reason: "No open access available"
```

---

### 2. Preprocess PDFs

**Action**: Convert PDFs to markdown chunks

**Use `pdf-preprocess` skill** for each downloaded paper:

```
[Load pdf-preprocess skill]

For each paper folder:
  1. Read PDF
  2. Extract text (preserve structure)
  3. Split into chunks (~1000 lines each)
  4. Create: {paper}_1.md, {paper}_2.md, ...
  5. Create: _metadata.json
```

**Result per paper**:
```
02-resources/{paper}/
├── {paper}.pdf           # Original PDF
├── {paper}_1.md          # Chunk 1
├── {paper}_2.md          # Chunk 2
├── ...
└── _metadata.json        # Chunk metadata
```

**Metadata format**:
```json
{
  "title": "Paper Title",
  "source_pdf": "paper.pdf",
  "chunks": 3,
  "total_chars": 45000,
  "total_words": 9000,
  "preprocessed_at": "2025-12-18T14:30:00"
}
```

**Progress Tracking**:
```
Preprocessing PDFs...
  [1/18] Using LLMs for TA... 4 chunks, OK
  [2/18] GPT-4 Qualitative... 3 chunks, OK
  ...
Preprocessed: 18 papers, 52 chunks total
```

---

### 3. Analyze Papers

**Action**: Run paper-analyze with subagents

**Load `paper-analyze` skill**:

```
[Load paper-analyze skill]

Collection path: 02-projects/NN-{slug}/02-resources/
Briefing path: 02-resources/_briefing.md

For each paper:
  1. Estimate tokens
  2. Spawn subagent with paper-analyze-core methodology
  3. Subagent creates:
     - _analysis_log.md (Schema v2.0)
     - index.md (analysis output)
```

**Subagent outputs per paper**:
```
02-resources/{paper}/
├── {paper}.pdf
├── {paper}_1.md, {paper}_2.md, ...
├── _metadata.json
├── _analysis_log.md      # NEW: Schema v2.0 log
└── index.md              # NEW: Analysis output
```

**Concurrency**: Max 3 subagents at once (avoid rate limits)

**Progress Tracking**:
```
Analyzing papers...
  [1/18] Using LLMs for TA... analyzing 4 chunks
  [2/18] GPT-4 Qualitative... analyzing 3 chunks
  [3/18] Multi-Agent QDA... analyzing 5 chunks
  ...
  [1/18] Using LLMs for TA... COMPLETE
  [2/18] GPT-4 Qualitative... COMPLETE
  ...
Analyzed: 18/18 papers
```

---

### 4. Validate Results

**Action**: Run validation script on all analysis logs

**Command**:
```bash
python 03-skills/research-pipeline/skills/paper-analyze/scripts/validate_analysis.py \
  02-projects/NN-{slug}/02-resources/ \
  --output 04-outputs/_validation_report.md
```

**Validation Checks**:
1. Schema version = 2.0
2. All steps completed
3. All chunks read
4. Multi-point evidence matches actual chunks
5. index.md created and valid

**Results Display**:
```
Validation Results
══════════════════════════════════════════════════════
✓ PASSED: 16 papers (logs valid, evidence matches)
⚠ WARNING: 1 paper (minor issues, usable)
✗ FAILED: 1 paper (evidence mismatch, needs re-analysis)
══════════════════════════════════════════════════════

Failed Papers:
  - Paper_XYZ: Chunk 3 evidence mismatch (may not have read full content)

Action Required:
  - Re-analyze Paper_XYZ? [Y/N]
```

**Handle Failures**:
- **Re-analyze**: Spawn new subagent for failed papers
- **Skip**: Exclude from synthesis, note in report
- **Manual**: User reviews index.md manually

**Output**: `04-outputs/_validation_report.md`

---

### 5. Generate Synthesis

**Action**: Cross-paper analysis using paper-synthesize

**Use `paper-synthesize` skill**:

```
[Load paper-synthesize skill]

Collection path: 02-projects/NN-{slug}/02-resources/
Research question: {from _briefing.md}
Extraction fields: {from _briefing.md}

Read all index.md files
Aggregate by field
Generate synthesis
```

**Synthesis Structure**:
```markdown
---
synthesized_at: "2025-12-18T16:00:00"
papers_included: 17
papers_excluded: 1
research_question: "{RQ}"
---

# Research Synthesis: {Project Name}

## Executive Summary
{2-3 paragraph summary of key findings}

## Methodology Overview
{Summary of methods used across papers}

## Key Themes

### Theme 1: {Name}
- **Papers**: [Paper1, Paper2, Paper3]
- **Summary**: {Cross-paper synthesis}
- **Key Quotes**:
  - "Quote" (Paper1, Chunk 2)
  - "Quote" (Paper2, Chunk 4)

### Theme 2: {Name}
...

## Gaps and Limitations
{What the literature doesn't cover}

## Future Research Directions
{Opportunities identified}

## Paper-by-Paper Summary
| Paper | Key Contribution | Relevance |
|-------|-----------------|-----------|
| Paper1 | {contribution} | High |
| Paper2 | {contribution} | High |
...

## References
{Formatted citations}
```

**Output**: `04-outputs/_synthesis.md`

---

### 6. Generate Quality Metrics

**Action**: Aggregate analysis quality metrics

**Collect from `_analysis_log.md` files**:
- Relevance scores
- Extraction confidence
- Domain match rates
- Validation status

**Create**: `04-outputs/_quality_metrics.md`

```yaml
---
generated_at: "2025-12-18T16:05:00"
total_papers: 18
---

# Quality Metrics

## Overall Statistics
- Papers analyzed: 18
- Validation pass rate: 94% (17/18)
- Average relevance score: 4.2/5
- High confidence extractions: 78%

## By Paper
| Paper | Relevance | Confidence | Validated |
|-------|-----------|------------|-----------|
| Paper1 | 5/5 | High | ✓ |
| Paper2 | 4/5 | Medium | ✓ |
| Paper3 | 3/5 | Low | ⚠ |
...

## Distribution
- Score 5: 8 papers (44%)
- Score 4: 6 papers (33%)
- Score 3: 3 papers (17%)
- Score 2: 1 paper (6%)

## Recommendations
- Consider re-analyzing low-confidence papers
- Paper3 may need manual review
```

---

### 7. Project Completion

**Action**: Finalize project and mark complete

**Final Project Structure**:
```
02-projects/NN-{slug}/
├── 01-planning/
│   ├── overview.md          # status: COMPLETE
│   ├── plan.md
│   └── steps.md             # All tasks checked
├── 02-resources/
│   ├── _briefing.md
│   ├── _search_results.md
│   ├── _abstract_reviews.md
│   └── {paper}/             # 18 paper folders
│       ├── *.pdf
│       ├── *_N.md
│       ├── _metadata.json
│       ├── _analysis_log.md
│       └── index.md
├── 03-working/
│   └── _selection_log.md
└── 04-outputs/
    ├── _validation_report.md
    ├── _quality_metrics.md
    └── _synthesis.md
```

**Update `overview.md`**:
```yaml
status: COMPLETE
completed_at: "2025-12-18T16:10:00"
```

**Completion Summary**:
```
══════════════════════════════════════════════════════
RESEARCH PROJECT COMPLETE
══════════════════════════════════════════════════════

Project: {Name}
Research Question: {RQ}

Results:
- Papers analyzed: 17/18
- Validation rate: 94%
- Synthesis generated: Yes

Outputs:
- 04-outputs/_synthesis.md - Cross-paper synthesis
- 04-outputs/_validation_report.md - Quality report
- 04-outputs/_quality_metrics.md - Metrics dashboard

Next Steps:
- Review synthesis for research insights
- Export to desired format (PDF, Word, etc.)
- Archive project: 'archive project {name}'

══════════════════════════════════════════════════════
```

---

## Error Handling

### Download Failures
- Skip papers without open access
- Log in `_selection_log.md`
- Continue with available papers

### Preprocessing Failures
- Retry once
- If still fails, skip paper
- Log error with reason

### Analysis Failures
- Check validation results
- Re-analyze failed papers once
- If still fails, exclude from synthesis

### Synthesis Failures
- Ensure at least 3 papers available
- Fall back to simpler aggregation
- Manual synthesis if automated fails

---

## Phase 2 Checklist

Before marking complete:

- [ ] All approved papers downloaded (or logged as unavailable)
- [ ] All PDFs preprocessed into chunks
- [ ] All papers analyzed with subagents
- [ ] Validation script run, results reviewed
- [ ] Failed papers re-analyzed or excluded
- [ ] Synthesis generated
- [ ] Quality metrics generated
- [ ] Project status updated to COMPLETE

---

**Previous**: [Phase 1: Planning Workflow](phase1_planning.md)
