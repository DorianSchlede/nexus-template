---
name: create-research-project
description: "Create research projects with paper selection, download, and preprocessing (Phase 1). Load when user says 'create research project', 'new research', 'start research on [topic]'. Delivers analysis-ready chunks. For EXECUTING analysis, use 'execute-research-project' skill."
---

# Create Research Project (Phase 1: Planning & Acquisition)

Create research projects with paper selection, download, and preprocessing. **This skill delivers analysis-ready chunks** - use `execute-research-project` for analysis and synthesis.

---

## Workflow Overview

```
create-research-project (THIS SKILL)
        │
        ├─ PHASE A: RESEARCH DEFINITION
        │   ├─ Step 0: Initialize TodoWrite (tracking)
        │   ├─ Step 1: Create project structure
        │   ├─ Step 2: Define research question → _briefing.md
        │   └─ Step 3: Search papers → _search_results.md
        │
        ├─ PHASE B: PAPER SELECTION
        │   ├─ Step 4: Review abstracts → _abstract_reviews.md
        │   ├─ Step 5: User selection → _selection_log.md
        │   └─ Step 6: Selection Gate (user approves papers)
        │
        ├─ PHASE C: PAPER ACQUISITION
        │   ├─ Step 7: Download approved papers
        │   ├─ Step 8: Preprocess PDFs → chunks
        │   └─ Step 9: Acquisition Report + User Gate
        │
        └─ PHASE D: READINESS GATE
            └─ Step 10: Confirm ready for execution
                    │
                    └─→ HANDOFF to execute-research-project
```

---

## Step 0: Initialize Task Tracking

**MANDATORY: Use TodoWrite at start of skill:**

```
TodoWrite with initial todos:
- [ ] Create project structure (Step 1)
- [ ] Define research question → _briefing.md (Step 2)
- [ ] Search papers → _search_results.md (Step 3)
- [ ] Review abstracts → _abstract_reviews.md (Step 4)
- [ ] User selection → _selection_log.md (Step 5)
- [ ] Selection gate approval (Step 6)
- [ ] Download approved papers (Step 7)
- [ ] Preprocess PDFs → chunks (Step 8)
- [ ] Acquisition report + user gate (Step 9)
- [ ] Readiness gate → handoff (Step 10)
```

**Update todos as each step completes.**

---

## Progress Tracking: steps.md and plan.md

### Marking Checkboxes in steps.md

**After completing each step, mark the corresponding checkbox in `01-planning/steps.md`:**

| After Step | Mark Complete in steps.md |
|------------|---------------------------|
| Step 1 | `- [x] Create project structure` |
| Step 2 | `- [x] Define research question and extraction schema` |
| Step 3 | `- [x] Search academic databases` |
| Step 4 | `- [x] Review abstracts and assess relevance` |
| Step 5-6 | `- [x] User approves paper selection` |
| Step 7 | `- [x] Download approved papers` |
| Step 8 | `- [x] Preprocess PDFs to markdown chunks` |
| Step 9 | `- [x] Verify acquisition completeness` |

**Use Edit tool to change `- [ ]` to `- [x]` for each completed task.**

### Updating plan.md

**After Step 2 (Define RQ)**, update plan.md:
```markdown
## Research Question

**Primary RQ**: {actual research question from _briefing.md}

**Focus Areas**:
- {focus area 1}
- {focus area 2}

## Extraction Schema

| Field | Description | Priority |
|-------|-------------|----------|
| {field1} | {description1} | high |
| {field2} | {description2} | medium |
```

**After Step 6 (Selection Gate)**, update plan.md Current State:
```markdown
## Current State

| Metric | Value |
|--------|-------|
| Phase | 2-Selection (complete) |
| Papers Approved | {N} |
| Papers Downloaded | 0 |
| Papers with Chunks | 0 |
| Papers Analyzed | 0 |
```

**After Step 9 (Acquisition Report)**, update plan.md:
- Current State with download/chunk counts
- Paper Corpus table with actual paper IDs, chunk counts, subagent allocation

---

# PHASE A: RESEARCH DEFINITION

## Step 1: Create Project Structure

**Use create-project skill internally:**

```bash
python 00-system/skills/projects/create-project/scripts/init_project.py \
  "{Project Name}" --type research
```

**Result:**
```
02-projects/NN-{slug}/
├── 01-planning/
│   ├── overview.md    # type: research
│   ├── plan.md
│   └── steps.md
├── 02-resources/      # Papers will go here
├── 03-working/        # Selection tracking
└── 04-outputs/        # Synthesis outputs (Phase 2)
```

---

## Step 2: Define Research Question

**Interactive session to create `02-resources/_briefing.md`:**

```
AI: Let's define your research briefing.

1. What is your main research question?
2. What fields should I extract from each paper?
   - Topics/themes? Methods? Findings? Limitations?
3. What domain is this research in?
```

**Output: `02-resources/_briefing.md`**
```yaml
---
research_question: "{RQ}"
domain: "{field/domain}"
extraction_schema:
  - field: topics
    description: "Main topics"
  - field: methods
    description: "Research methods"
  # ... custom fields
focus_areas: [...]
skip_sections: ["Acknowledgments"]
---
```

---

## Step 3: Search Papers

**Use `paper-search` skill:**

```
[Load paper-search skill]
Search: "{research question}"
Save to: 02-resources/_search_results.md
```

**Output: `02-resources/_search_results.md`**
```yaml
---
search_query: "{query}"
search_date: "{date}"
total_results: {N}
---

# Search Results

## Paper 1: {Title}
- Authors: ...
- Abstract: "..."
- DOI: ...
- PDF: {URL if available}
- Status: PENDING_REVIEW
```

---

# PHASE B: PAPER SELECTION

## Step 4: Review Abstracts

**AI reads each abstract and assesses relevance:**

See [references/abstract_review.md](references/abstract_review.md) for scoring criteria.

**Output: `02-resources/_abstract_reviews.md`**
```yaml
---
reviewed_date: "{date}"
recommended: {N}
flagged: {N}
rejected: {N}
---

## Paper 1: {Title}
- Relevance Score: 5/5
- Recommendation: APPROVE
- Rationale: "..."
```

---

## Step 5: User Selection

**Present recommendations for approval:**

```
APPROVED ({N} papers):
  1. [x] Paper Title (5/5)
  2. [x] Paper Title (4/5)

NEEDS REVIEW ({N} papers):
  3. [ ] Paper Title (3/5) - {concern}

REJECTED ({N} papers):
  [SKIP] Paper Title (1/5) - Wrong domain

Commands: 'approve all', 'add N', 'remove N', 'show N'
```

**Output: `03-working/_selection_log.md`**
```yaml
---
schema_version: "3.0"
selection_date: "{date}"
total_approved: {N}
approved_by_user: true
user_instruction: "{what user said}"

# Acquisition tracking (populated in Step 7-8)
acquisition:
  attempted_at: null
  downloaded: 0
  unavailable: 0
  preprocessed: 0
  chunks_total: 0

papers: []
unavailable_papers: []
---
```

---

## Step 6: Selection Gate

**Confirm paper selection before acquisition:**

```
Selection complete!

Research Question: "{RQ}"
Papers Selected: {N}

Ready to download and preprocess papers?

[Y] Yes → Proceed to acquisition
[N] No, modify selection
[S] Save and continue later
```

**On 'Y':** Proceed to Phase C (Acquisition)

---

# PHASE C: PAPER ACQUISITION

## Step 7: Download Approved Papers

**Download all approved papers using automated batch download:**

### Batch Download (Recommended)

```bash
# Download all papers from selection log
python 03-skills/paper-search/scripts/paper_download.py \
  --input "02-projects/NN-{slug}/03-working/_selection_log.md" \
  --output "02-projects/NN-{slug}/02-resources/" \
  --parallel 3
```

**The script automatically:**
- Resolves multiple URLs per paper (arXiv → S2 → Unpaywall → direct)
- Downloads in parallel with rate limiting
- Verifies PDFs (catches HTML error pages)
- Retries failed downloads with exponential backoff
- Generates `_download_report.md` with success/fail stats

### URL Resolution Priority

1. **arXiv ID** (if available) - Most reliable
2. **DOI via Semantic Scholar** - Often has PDF + arXiv link
3. **DOI via Unpaywall** - OA from repositories
4. **Title search on arXiv** - Fallback for paywalled papers
5. **Direct URL** - Original URL if from known OA source

### Single Paper Download (Fallback)

If batch fails for specific papers, try individual downloads:

```bash
# By arXiv ID (preferred)
python 03-skills/paper-search/scripts/paper_download.py \
  --arxiv "2506.23998" \
  --output "02-projects/NN-{slug}/02-resources/"

# By DOI
python 03-skills/paper-search/scripts/paper_download.py \
  --doi "10.1177/08944393231220483" \
  --output "02-projects/NN-{slug}/02-resources/"

# By title search
python 03-skills/paper-search/scripts/paper_download.py \
  --title "Paper Title Here" \
  --output "02-projects/NN-{slug}/02-resources/"
```

### Progress Display

```
Downloading papers...
  [1/25] Auto-TA (arxiv:2506.23998)... OK
  [2/25] SFT-TA (arxiv:2509.17167)... OK
  [3/25] Thematic-LM (ACM DOI)... UNAVAILABLE (paywall)
  [4/25] De Paoli (SAGE)... OK (via Unpaywall)
  ...

Downloaded: 18/25
Unavailable: 7 (paywalled, no OA version)
```

### Update _selection_log.md

After downloads, update the selection log with status:

```yaml
papers:
  - id: "Auto_TA"
    title: "Auto-TA: Automated Thematic Analysis"
    arxiv: "2506.23998"
    status: "downloaded"
    pdf_path: "02-resources/Auto_TA/Auto_TA.pdf"

  - id: "Thematic_LM"
    title: "Thematic-LM: Multi-agent System"
    doi: "10.1145/3696410.3714595"
    status: "unavailable"
    reason: "ACM paywall, no preprint found"

unavailable_papers:
  - title: "Thematic-LM"
    doi: "10.1145/3696410.3714595"
    reason: "ACM paywall"
```

---

## Step 8: Preprocess PDFs → Chunks

**Convert all downloaded PDFs to markdown chunks:**

### Batch Preprocessing (Recommended)

```bash
python 03-skills/pdf-preprocess/scripts/pdf_to_markdown.py \
  "02-projects/NN-{slug}/02-resources/" \
  --batch \
  --recursive
```

### Custom Chunk Settings (Optional)

```bash
# Smaller chunks with more overlap
python 03-skills/pdf-preprocess/scripts/pdf_to_markdown.py \
  "02-projects/NN-{slug}/02-resources/" \
  --batch --recursive \
  --max-lines 500 \
  --overlap 50
```

### Result Per Paper

```
02-resources/{paper}/
├── {paper}.pdf           # Original PDF
├── {paper}_1.md          # Chunk 1
├── {paper}_2.md          # Chunk 2
├── ...
└── _metadata.json        # Chunk index
```

### Progress Display

```
Preprocessing PDFs...
  [1/18] Auto_TA... 4 chunks
  [2/18] SFT_TA... 3 chunks
  [3/18] De_Paoli... 5 chunks
  ...

Preprocessed: 18 papers → 52 chunks total
```

### Update _selection_log.md

```yaml
acquisition:
  attempted_at: "2025-12-19T14:30:00"
  downloaded: 18
  unavailable: 7
  preprocessed: 18
  chunks_total: 52

papers:
  - id: "Auto_TA"
    status: "ready"        # ready = downloaded + preprocessed
    chunks: 4
```

---

## Step 9: Acquisition Report + User Gate

**Present acquisition results for user approval:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PAPER ACQUISITION COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Research Project: {name}

✓ Downloaded:    18 papers
✗ Unavailable:   7 papers (paywalled)
✓ Preprocessed:  18 papers → 52 chunks

Unavailable papers:
  • Thematic-LM (ACM paywall)
  • LLM-in-the-loop (ACL paywall)
  • CollabCoder (ACM paywall)
  • ... (+4 more)

Ready to proceed with 18 papers?

[Y] Yes, proceed to execution
[R] Retry failed downloads
[A] Add alternative papers (search again)
[S] Save and continue later
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Decision Handling

| User Input | Action |
|------------|--------|
| **Y** | Proceed to Step 10 (Readiness Gate) |
| **R** | Retry downloads (try alternative URLs) |
| **A** | Return to Step 3 (search for alternatives) |
| **S** | Save state, exit (can resume later) |

### Update plan.md with Paper Corpus

**After acquisition complete, populate the Paper Corpus table in plan.md:**

```markdown
## Paper Corpus

### Papers Ready for Analysis

| Paper ID | Chunks | Est. Tokens | Subagents | Status |
|----------|--------|-------------|-----------|--------|
| Auto_TA | 4 | ~20,000 | 1 | ready |
| SFT_TA | 3 | ~15,000 | 1 | ready |
| De_Paoli_2024 | 8 | ~40,000 | 1 | ready |
| Large_Paper | 14 | ~85,000 | 2 | ready |

### Unavailable Papers

| Paper | Reason |
|-------|--------|
| Thematic-LM | ACM paywall |
| CollabCoder | ACM paywall |
```

**Calculate subagent allocation based on chunk count:**
- <=4 chunks → 1 subagent
- 5-12 chunks → 1 subagent
- >12 chunks → 2 subagents (split at chunk 6)

**Also update Current State:**
```markdown
## Current State

| Metric | Value |
|--------|-------|
| Phase | 3-Acquisition (complete) |
| Papers Approved | 25 |
| Papers Downloaded | 18 |
| Papers with Chunks | 18 |
| Papers Analyzed | 0 |
| Total Chunks | 52 |
```

### Minimum Threshold

If <50% of papers acquired:
```
⚠️ WARNING: Only {N} of {total} papers acquired ({percent}%)

This may limit synthesis quality. Consider:
  1. Searching for arXiv preprints of paywalled papers
  2. Adding alternative papers on similar topics
  3. Proceeding with limited corpus

Continue anyway? [Y/N]
```

---

# PHASE D: READINESS GATE

## Step 9.5: Generate Analysis Kit (NEW)

**Create `_analysis_kit.md` for subagent context:**

This file consolidates everything subagents need to analyze papers, eliminating redundant reads.

**Use template from:** `references/analysis_kit_template.md`

**Populate with:**
- Research question from `_briefing.md`
- Extraction schema (fields, descriptions, priorities)
- Focus areas
- Validation contract (required frontmatter fields)

**Output:** `02-resources/_analysis_kit.md`

```markdown
---
project_id: "{project_id}"
project_path: "02-projects/{project_id}"
generated: "{date}"
---

# Analysis Kit for {project_name}

## Research Question
{from _briefing.md}

## Extraction Schema
| Field | Description | Priority |
|-------|-------------|----------|
{from _briefing.md extraction_schema}

## Validation Contract
Your output will be validated:
- chunks_read == chunks_expected
- analysis_complete == true
- high_priority_fields_found >= 1
```

---

## Step 9.6: Generate Orchestrator Instructions (NEW)

**Add orchestrator instructions to `plan.md`:**

**Use template from:** `references/orchestrator_template.md`

**Populate with:**
- Project path constants
- Batch allocation (papers grouped by 10)
- Subagent prompt template with `{paper_id}` variable
- Validation checks (Phase 4.5)
- Synthesis instructions

**Key sections to add:**
1. **Constants** - PROJECT, PAPERS, KIT, METHODOLOGY paths
2. **Phase 4** - Subagent template + batch table
3. **Phase 4.5** - Validation checks (hallucination prevention)
4. **Phase 5** - Synthesis prompt

---

## Step 10: Confirm Ready for Execution

**Final verification before handoff:**

### Readiness Checks

```python
# 1. Verify at least 1 paper has chunks
papers_with_chunks = count_papers_with_metadata_json()
if papers_with_chunks == 0:
    fail("No papers preprocessed - cannot proceed")

# 2. Verify briefing exists
if not exists("02-resources/_briefing.md"):
    fail("Missing _briefing.md - research question not defined")

# 3. Verify analysis kit exists (NEW)
if not exists("02-resources/_analysis_kit.md"):
    fail("Missing _analysis_kit.md - run Step 9.5")

# 4. Verify orchestrator instructions in plan.md (NEW)
if "Phase 4.5: Validation" not in read("01-planning/plan.md"):
    fail("Missing orchestrator instructions - run Step 9.6")

# 5. Update overview.md
update_overview(status="READY_FOR_EXECUTION")
```

### Final Summary

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PLANNING COMPLETE - READY FOR EXECUTION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Research Project: {name}
Research Question: "{RQ}"

Papers ready: {N} ({chunks} chunks)
Papers unavailable: {M}

All prerequisites met:
  ✓ _briefing.md (extraction schema)
  ✓ _analysis_kit.md (subagent context)
  ✓ _selection_log.md (user approved)
  ✓ Paper chunks ({N} papers preprocessed)
  ✓ plan.md (orchestrator instructions)
  ✓ steps.md (batch tracking)

To start analysis, say:
  "execute research project {name}"

This will:
  1. Analyze each paper (spawn subagents in batches of 10)
  2. Validate analysis logs (Phase 4.5 hallucination check)
  3. Retry failed papers
  4. Generate cross-paper synthesis
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Handoff to execute-research-project

**When Readiness Gate passes:**

The `execute-research-project` skill expects:
- Paper folders with `_metadata.json` (chunks exist)
- `02-resources/_briefing.md` (extraction schema)
- `02-resources/_analysis_kit.md` (subagent context) **NEW**
- `01-planning/plan.md` (orchestrator instructions) **NEW**
- `01-planning/steps.md` (batch tracking) **NEW**
- `overview.md` with `status: READY_FOR_EXECUTION`

**execute-research-project will:**
1. Read orchestrator instructions from plan.md
2. Spawn analysis subagents in batches (max 10 parallel)
3. **Validate each batch** (Phase 4.5 - hallucination check) **NEW**
4. Retry failed papers
5. Generate synthesis
6. Mark project COMPLETE

---

## Files Created by This Skill

| File | Location | Purpose |
|------|----------|---------|
| `_briefing.md` | 02-resources/ | Extraction schema |
| `_analysis_kit.md` | 02-resources/ | Subagent context (NEW) |
| `_search_results.md` | 02-resources/ | API results |
| `_abstract_reviews.md` | 02-resources/ | AI assessments |
| `_selection_log.md` | 03-working/ | Approved papers + acquisition status |
| `*.pdf` | 02-resources/papers/{paper}/ | Downloaded papers |
| `*_N.md` | 02-resources/papers/{paper}/ | Markdown chunks |
| `_metadata.json` | 02-resources/papers/{paper}/ | Chunk index |
| `plan.md` | 01-planning/ | Orchestrator instructions (updated) |
| `steps.md` | 01-planning/ | Batch tracking (updated) |

---

## Error Handling

| Step | Error | Action |
|------|-------|--------|
| Step 3 | API rate limit | Wait and retry, or use cached results |
| Step 7 | Download fails | Try alternative source → Mark unavailable |
| Step 7 | All papers paywalled | Warn user, suggest arXiv alternatives |
| Step 8 | PDF corrupted | Skip paper, log error |
| Step 8 | pymupdf4llm fails | Try alternative extraction, or skip |
| Step 9 | <50% acquired | Warn, offer to search alternatives |
| Step 9.5 | Missing _briefing.md | Go back to Step 2 |
| Step 10 | 0 papers ready | Block handoff, must retry acquisition |

---

## References

- [Abstract Review Process](references/abstract_review.md)
- [Phase 1 Planning Details](references/phase1_planning.md)
- [Analysis Kit Template](references/analysis_kit_template.md) **NEW**
- [Orchestrator Template](references/orchestrator_template.md) **NEW**
- [paper-search skill](../paper-search/SKILL.md)
- [pdf-preprocess skill](../pdf-preprocess/SKILL.md)

---

**Version**: 4.0 (2025-12-19)
**Changes**:
- Added Step 9.5: Generate _analysis_kit.md (subagent context)
- Added Step 9.6: Generate orchestrator instructions in plan.md
- Added Phase 4.5 validation (hallucination check) to handoff requirements
- Added batch tracking in steps.md
**Handles**: Phase 1 (Planning + Acquisition) - delivers analysis-ready chunks + orchestrator plan
**Handoff to**: `execute-research-project` (expects chunks + plan, does analysis only)
