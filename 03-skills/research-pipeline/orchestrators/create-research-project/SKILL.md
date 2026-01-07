---
name: create-research-project
description: "Create research projects with paper selection, download, and preprocessing (Phase 1). Load when user says 'create research project', 'new research', 'start research on [topic]'. Delivers analysis-ready chunks. For EXECUTING analysis, use 'execute-research-project' skill."
---

## DEPRECATION NOTICE

**This skill is being deprecated for direct invocation.** For new research projects, use:

```
plan project for [topic] research
```

The router will detect "research" type and invoke this skill's discovery workflow automatically.

**Why?** The plan-project router ensures all projects get proper discovery, mental models, and planning structure.

---

resume_instructions: |
  ## Context Checkpoint: _resume.md

  This skill requires maintaining a `_resume.md` file for context recovery.

  **Location**: `{project_path}/_resume.md`

  **Maintenance Rules**:
  1. UPDATE `_resume.md` when context usage reaches ~60% (before compaction risk)
  2. UPDATE after completing each major step (Steps 2, 5, 6, 9, 13)
  3. UPDATE after user approval gates
  4. RELOAD `_resume.md` immediately after any context summary/compaction

  **_resume.md Format**:

  updated: "{timestamp}"
  phase: "definition|selection|acquisition|readiness"
  project_id: "{project_id}"
  step: {current_step_number}
  ---

  # Resume Context

  ## Current State
  - Phase: {A|B|C|D}
  - Step: {step_number} - {step_name}
  - User gate pending: {true|false}

  ## Key Decisions Made
  - Research question: "{RQ}"
  - Papers approved: {N}
  - Papers downloaded: {N}

  ## Pending Work
  - Current step incomplete: {true|false}
  - Papers pending download: [list]
  - Papers pending preprocess: [list]

  ## Files Created
  - _briefing.md: {exists|missing}
  - _analysis_kit.md: {exists|missing}
  - _extraction_guide.md: {exists|missing}

  ## Next Actions
  1. {immediate next step}
  2. {following step}
  ```

  **On Resume After Compaction**:
  1. Read `{project_path}/_resume.md` first
  2. Read `01-planning/steps.md` for checkbox progress
  3. Continue from `## Next Actions`
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
            ├─ Step 10: Generate _analysis_kit.md + validate
            ├─ Step 11: Generate _extraction_guide.md + validate
            ├─ Step 12: Generate orchestrator instructions + validate
            └─ Step 13: Confirm ready for execution
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
- [ ] Generate _analysis_kit.md + validate (Step 10)
- [ ] Generate _extraction_guide.md + validate (Step 11)
- [ ] Generate orchestrator instructions in plan.md + validate (Step 12)
- [ ] Readiness gate → handoff (Step 13)
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

## Step 2: Define Research Question (with AI Field Generation)

**Gap G5 Fix: AI-Generated Field Suggestions**
**Gap G22a Fix: Add research_purpose field**

Interactive session to create `02-resources/_briefing.md`:

### 2.1 Research Question

```
AI: What is your main research question?

User: "What are foundational ontologies for digital work?"
```

### 2.2 Research Purpose (G22a - NEW)

```
AI: Why does this research matter? What will you use the insights for?
    (This helps subagents understand context and make better extraction decisions)

User: "Validate the 8-entity hypothesis for our UDWO metamodel"

AI: Got it. I'll include this as research_purpose in the briefing.
```

### 2.3 AI Field Generation (G5)

```
AI: Based on your research question, I'll suggest extraction fields.

   ANALYZING RESEARCH QUESTION...
   Domain detected: {detected_domain}
   Key concepts: {extracted_concepts}

   SUGGESTED FIELDS:
   ┌─────────────────────────────────────────────────────────────┐
   │ 1. {field_1}        - {description_1}                       │
   │ 2. {field_2}        - {description_2}                       │
   │ 3. {field_3}        - {description_3}                       │
   │ 4. {field_4}        - {description_4}                       │
   │ 5. {field_5}        - {description_5}                       │
   │ 6. {field_6}        - {description_6}                       │
   │ 7. {field_7}        - {description_7}                       │
   │ 8. {field_8}        - {description_8}                       │
   └─────────────────────────────────────────────────────────────┘

   FIELD QUALITY CHECK:
   ⚠ "{generic_field}" is generic - consider removing if not research-focused
   ✓ All other fields are domain-specific

   Commands:
   - 'ok' → Accept all fields
   - 'remove N' → Remove field N (e.g., 'remove 6')
   - 'add FIELD_NAME: description' → Add custom field
   - 'edit N: new description' → Edit description

User: remove 6, add ai_integration: How ontology enables AI agents

AI: Updated fields (8 total). Confirm? [Y/N]

User: Y

AI: Creating _briefing.md with research_purpose and 8 extraction fields...
```

### FIELD GENERATION PROMPT TEMPLATE (for AI)

When generating field suggestions, follow this template:

```
Given research question: "{RQ}"
Given domain hints: "{domain}"

1. Identify 6-10 extraction fields that would capture key insights
2. For each field provide:
   - field_key (snake_case, specific to domain)
   - description (what it captures, 10-15 words)
   - priority (high/medium based on RQ relevance)
3. Flag any generic fields that might match too much content (sparsity risk)
4. Ensure fields are MECE (mutually exclusive, collectively exhaustive)

AVOID generic fields like: "key_findings", "main_points", "summary"
PREFER specific fields like: "entity_types", "algorithm_complexity", "security_mechanisms"
```

**Output: `02-resources/_briefing.md`**

```yaml
---
research_question: "{RQ}"

# G22a: WHY this research matters (provides context to subagents)
research_purpose: "{purpose statement - what will you use insights for}"

domain: "{field/domain}"

extraction_schema:
  - field: {field_1}
    description: "{description_1}"
    priority: high
  - field: {field_2}
    description: "{description_2}"
    priority: high
  - field: {field_3}
    description: "{description_3}"
    priority: medium
  # ... AI-generated fields confirmed by user

focus_areas: [...]
skip_sections: ["Acknowledgments", "Author Contributions", "Funding"]
---
```

**Token Impact**: +30-50 tokens for research_purpose (validated as acceptable)

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
python 03-skills/research-pipeline/skills/paper-search/scripts/paper_download.py \
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
python 03-skills/research-pipeline/skills/paper-search/scripts/paper_download.py \
  --arxiv "2506.23998" \
  --output "02-projects/NN-{slug}/02-resources/"

# By DOI
python 03-skills/research-pipeline/skills/paper-search/scripts/paper_download.py \
  --doi "10.1177/08944393231220483" \
  --output "02-projects/NN-{slug}/02-resources/"

# By title search
python 03-skills/research-pipeline/skills/paper-search/scripts/paper_download.py \
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
python 03-skills/research-pipeline/skills/pdf-preprocess/scripts/pdf_to_markdown.py \
  "02-projects/NN-{slug}/02-resources/" \
  --batch \
  --recursive
```

### Custom Chunk Settings (Optional)

```bash
# Smaller chunks with more overlap
python 03-skills/research-pipeline/skills/pdf-preprocess/scripts/pdf_to_markdown.py \
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

## Step 10: Generate Analysis Kit

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

### Step 10 Validation

**After creating `_analysis_kit.md`, verify:**

```python
kit = read("02-resources/_analysis_kit.md")
assert kit.frontmatter.project_id == project_id, "Wrong project_id"
assert kit.frontmatter.generated is not None, "Missing timestamp"
assert "## Research Question" in kit, "Missing research question section"
assert "## Extraction Schema" in kit, "Missing extraction schema"
assert "## Validation Contract" in kit, "Missing validation contract"
```

**If validation fails:** Regenerate the file before proceeding.

---

## Step 11: Generate Extraction Guide

**Create `_extraction_guide.md` with project-specific extraction examples:**

**Use template from:** `03-skills/research-pipeline/shared/paper-analyze-core/references/extraction_guide_template.md`

**Populate with:**
- Field-specific examples for EACH field in `_briefing.md`
- Controlled vocabulary for this domain
- Good/bad extraction examples

**Output:** `02-resources/_extraction_guide.md`

```markdown
# Extraction Guide: {project_name}

## Field Definitions

### Field: {field_1_name}
**Definition**: {from briefing}
**Format**: Array of strings | Array of objects | String
**Priority**: high | medium

**Example GOOD extraction**:
{domain-specific example}

**Example BAD extraction**:
{what to avoid}

### Field: {field_2_name}
...

## Controlled Vocabulary

| Term | Use When |
|------|----------|
| {standard_term_1} | {when paper uses synonyms} |
| {standard_term_2} | {when paper uses synonyms} |
```

### Step 11 Validation

**After creating `_extraction_guide.md`, verify:**

```python
guide = read("02-resources/_extraction_guide.md")
briefing = read("02-resources/_briefing.md")

# Count fields in guide
guide_fields = count_sections_matching("### Field:")
briefing_fields = len(briefing.extraction_schema)

assert guide_fields == briefing_fields, \
    f"Field count mismatch: guide has {guide_fields}, briefing has {briefing_fields}"
assert "## Controlled Vocabulary" in guide, "Missing controlled vocabulary section"
```

**If validation fails:** Add missing field definitions before proceeding.

---

## Step 12: Generate Orchestrator Instructions + Subagent Allocation Plan

**Add orchestrator instructions to `plan.md`:**

**Use template from:** `references/orchestrator_template.md`

### 12.1: Calculate Subagent Allocation (CRITICAL)

**Read each paper's `_metadata.json` and calculate subagent allocation:**

```python
# Token estimation: Each chunk ≈ 10-15k tokens (1000 lines × ~50 chars/line)
# Usable budget: 74k tokens per subagent (after 26k methodology overhead)

allocation = []
for paper in papers_with_chunks:
    metadata = read(f"02-resources/papers/{paper}/_metadata.json")
    chunks = metadata.total_chunks
    chars = metadata.total_chars
    tokens_est = (chars / 5) * 1.3

    # Allocation rules
    if chunks <= 6:
        subagents = 1
        splits = [f"1-{chunks}"]
    elif chunks <= 12:
        subagents = 2
        splits = ["1-6", f"7-{chunks}"]
    elif chunks <= 18:
        subagents = 3
        splits = ["1-6", "7-12", f"13-{chunks}"]
    else:
        # Split into 5-6 chunk segments
        subagents = ceil(chunks / 6)
        splits = [f"{i*6+1}-{min((i+1)*6, chunks)}" for i in range(subagents)]

    allocation.append({
        "paper_id": paper,
        "chunks": chunks,
        "tokens_est": tokens_est,
        "subagents": subagents,
        "splits": splits
    })
```

### 12.2: Write Allocation Table to plan.md

**The allocation table MUST be written to plan.md so execute-research-project can read it:**

```markdown
## Subagent Allocation Plan

| Paper ID | Chunks | Est. Tokens | Subagents | Splits |
|----------|--------|-------------|-----------|--------|
| Small_Paper | 3 | ~35,000 | 1 | 1-3 |
| Medium_Paper | 6 | ~70,000 | 1 | 1-6 |
| Large_Paper | 10 | ~120,000 | 2 | 1-6, 7-10 |
| Survey_Paper | 16 | ~190,000 | 3 | 1-6, 7-12, 13-16 |

**Total subagents**: 7
**Max concurrent**: 15
**Estimated batches**: 1
```

### 12.3: Generate Subagent Prompts

**Populate with:**
- Project path constants
- **Pre-calculated allocation from 12.1** (NOT dynamic calculation)
- Subagent prompt template with `{paper_id}` and `{chunks}` variables
- Split prompts for large papers (with specific chunk ranges)
- Merge prompts for multi-part papers
- Validation checks (Phase 4.5)
- Synthesis instructions

**Key sections to add:**
1. **Constants** - PROJECT, PAPERS, KIT, METHODOLOGY paths
2. **Subagent Allocation Plan** - Pre-calculated table from 12.1
3. **Phase 4** - Subagent prompts (standard + split + merge)
4. **Phase 4.5** - Validation checks (hallucination prevention)
5. **Phase 5** - Synthesis prompt

### Step 12 Validation

**After updating `plan.md`, verify:**

```python
plan = read("01-planning/plan.md")

assert "## Orchestrator Instructions" in plan, "Missing orchestrator section"
assert "## Subagent Allocation Plan" in plan, "Missing allocation plan"
assert "| Paper ID | Chunks |" in plan, "Missing allocation table"
assert "**Total subagents**:" in plan, "Missing subagent count"
assert "### Constants" in plan, "Missing constants"
assert "### Phase 4: Paper Analysis" in plan, "Missing Phase 4"
assert "### Phase 4.5: Validation" in plan, "Missing Phase 4.5"
assert "{paper_id}" in plan, "Missing paper_id variable in template"

# Verify allocation count matches paper count
paper_count = count_papers_with_metadata_json()
allocation_rows = count_table_rows("## Subagent Allocation Plan")
assert allocation_rows == paper_count, f"Allocation mismatch: {allocation_rows} vs {paper_count} papers"
```

**If validation fails:** Add missing sections or regenerate allocation table.

---

## Step 13: Confirm Ready for Execution

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

# 3. Verify analysis kit exists
if not exists("02-resources/_analysis_kit.md"):
    fail("Missing _analysis_kit.md - run Step 10")

# 4. Verify extraction guide exists
if not exists("02-resources/_extraction_guide.md"):
    fail("Missing _extraction_guide.md - run Step 11")

# 5. Verify orchestrator instructions in plan.md
if "## Orchestrator Instructions" not in read("01-planning/plan.md"):
    fail("Missing orchestrator instructions - run Step 12")

# 6. Update overview.md
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
- `02-resources/_analysis_kit.md` (subagent context)
- `02-resources/_extraction_guide.md` (field examples + vocabulary)
- `01-planning/plan.md` with `## Orchestrator Instructions` section
- `01-planning/steps.md` (batch tracking)
- `overview.md` with `status: READY_FOR_EXECUTION`

**execute-research-project will:**
1. Validate all prerequisites exist (fail fast if missing)
2. Read orchestrator instructions from plan.md
3. Spawn analysis subagents in batches (max 10 parallel)
4. Validate each batch (Phase 4.5 - hallucination check)
5. Retry failed papers
6. Generate synthesis
7. Mark project COMPLETE

---

## Files Created by This Skill

| File | Location | Purpose |
|------|----------|---------|
| `_briefing.md` | 02-resources/ | Extraction schema |
| `_analysis_kit.md` | 02-resources/ | Subagent context (Step 10) |
| `_extraction_guide.md` | 02-resources/ | Field examples + vocabulary (Step 11) |
| `_search_results.md` | 02-resources/ | API results |
| `_abstract_reviews.md` | 02-resources/ | AI assessments |
| `_selection_log.md` | 03-working/ | Approved papers + acquisition status |
| `*.pdf` | 02-resources/papers/{paper}/ | Downloaded papers |
| `*_N.md` | 02-resources/papers/{paper}/ | Markdown chunks |
| `_metadata.json` | 02-resources/papers/{paper}/ | Chunk index |
| `plan.md` | 01-planning/ | Orchestrator instructions (Step 12) |
| `steps.md` | 01-planning/ | Batch tracking |

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
| Step 10 | Missing _briefing.md | Go back to Step 2 |
| Step 10 | Validation fails | Regenerate _analysis_kit.md |
| Step 11 | Field count mismatch | Add missing field definitions |
| Step 12 | Missing sections | Add missing orchestrator sections |
| Step 13 | 0 papers ready | Block handoff, must retry acquisition |

---

## References

- [Abstract Review Process](references/abstract_review.md)
- [Phase 1 Planning Details](references/phase1_planning.md)
- [Analysis Kit Template](references/analysis_kit_template.md)
- [Orchestrator Template](references/orchestrator_template.md)
- [Extraction Guide Template](../../shared/paper-analyze-core/references/extraction_guide_template.md)
- [paper-search skill](../../skills/paper-search/SKILL.md)
- [pdf-preprocess skill](../../skills/pdf-preprocess/SKILL.md)

---

**Version**: 5.0 (2025-12-28)
**Changes**:
- v4.0: Added Step 9.5/9.6 for analysis kit and orchestrator instructions
- v5.0: Renumbered steps to full numbers (9.5→10, 9.6→12, 10→13)
- v5.0: Added Step 11: Generate _extraction_guide.md
- v5.0: Added inline validation after Steps 10, 11, 12
- v5.0: Updated readiness gate to check all new files
**Handles**: Phase 1 (Planning + Acquisition) - delivers analysis-ready chunks + orchestrator plan
**Handoff to**: `execute-research-project` (expects chunks + plan, does analysis only)
