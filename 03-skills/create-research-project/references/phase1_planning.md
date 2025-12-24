# Phase 1: Planning Workflow

Detailed workflow for the Planning phase of a research project.

---

## Overview

Phase 1 ends with a **Planning Gate** - user must approve paper selection before Phase 2 begins.

**Inputs**: Research question/topic from user
**Outputs**: `_selection_log.md` with approved papers

---

## Step-by-Step Workflow

### 1. Project Initialization

**Action**: Create standard Nexus project structure

```bash
# Use create-project skill internally
python 00-system/skills/projects/create-project/scripts/init_project.py \
  "{Project Name}" \
  --path 02-projects \
  --type research
```

**Result**:
```
02-projects/NN-{slug}/
├── 01-planning/
│   ├── overview.md          # type: research
│   ├── plan.md
│   └── steps.md
├── 02-resources/
├── 03-working/
└── 04-outputs/
```

**Validation**: Verify all folders created, overview.md has `type: research`

---

### 2. Research Question Definition

**Action**: Interactive session to define research scope

**Questions to Ask**:
1. "What is your main research question?"
2. "What specific information do you need from each paper?"
3. "What domain/field is this research in?"
4. "How many papers do you expect to analyze? (5-10, 10-25, 25+)"
5. "Any specific authors or papers you want included?"

**Create**: `02-resources/_briefing.md`

```yaml
---
research_question: "{User's research question}"
domain: "{Field/domain for relevance filtering}"
scope: "{small|medium|large}"
expected_papers: {number}
extraction_schema:
  - field: topics
    description: "Main topics/themes discussed"
    required: true
  - field: methods
    description: "Research methods used"
    required: true
  - field: findings
    description: "Key findings/results"
    required: true
  - field: limitations
    description: "Stated limitations"
    required: false
  # Add custom fields based on user needs
focus_areas:
  - "{Priority topic 1}"
  - "{Priority topic 2}"
skip_sections:
  - "Acknowledgments"
  - "Author biographies"
  - "Funding statements"
must_include_papers:
  - "{Specific paper DOI or title}"
exclude_keywords:
  - "{Wrong-domain terms}"
---

# Research Briefing

## Research Question
{Detailed elaboration of research question}

## What to Extract
{Description of extraction requirements}

## Domain Context
{Background on the field to help filter relevance}
```

---

### 3. Paper Search

**Action**: Use `paper-search` skill to find relevant papers

**Search Strategy**:
1. Primary search: Research question as query
2. Secondary search: Key terms from focus areas
3. Author search: Known relevant authors
4. Citation search: Papers citing foundational works

**Commands**:
```
# Search using paper-search skill
[Load paper-search skill]
Search: "{research_question}"
Filters:
  - Year: 2020-2025 (or user-specified)
  - Type: peer-reviewed
  - Open access preferred
```

**Store Results**: `02-resources/_search_results.md`

```yaml
---
search_query: "{query used}"
search_date: "{ISO date}"
apis_used:
  - semantic_scholar
  - openalex
  - arxiv
total_results: {N}
filters_applied:
  year_range: "2020-2025"
  open_access: true
---

# Search Results

## Paper 1: {Title}
- **Authors**: {Authors}
- **Year**: {Year}
- **Abstract**: "{Abstract text}"
- **DOI**: {DOI}
- **Open Access**: {Yes/No}
- **Source**: {API that found it}
- **Status**: PENDING_REVIEW

## Paper 2: ...
```

---

### 4. Abstract Review

**Action**: AI reads each abstract and assesses relevance

**Review Criteria**:

| Criterion | Weight | Description |
|-----------|--------|-------------|
| Domain Match | 40% | Is this the right field? |
| Research Question Fit | 35% | Does it address our RQ? |
| Methodology Relevance | 15% | Methods applicable to our needs? |
| Recency | 10% | How current is the research? |

**Scoring**:
- **5/5**: Highly relevant, must include
- **4/5**: Relevant, recommend include
- **3/5**: Marginal, user should decide
- **2/5**: Likely irrelevant, recommend skip
- **1/5**: Wrong domain, reject

**Flags**:
- `DOMAIN_MISMATCH`: Terms suggest wrong field
- `OUTDATED`: Published >5 years ago
- `NO_ABSTRACT`: Cannot assess without abstract
- `DUPLICATE`: Same paper from different source

**Create**: `02-resources/_abstract_reviews.md`

```yaml
---
reviewed_date: "{ISO date}"
total_papers: {N}
by_recommendation:
  approve: {count}
  review: {count}
  reject: {count}
---

# Abstract Reviews

## APPROVED (Score >= 4)

### Paper 1: {Title}
- **Score**: 5/5
- **Domain Match**: Yes
- **Recommendation**: APPROVE
- **Rationale**: "{Why this paper is relevant}"
- **Key Terms**: [term1, term2, term3]

### Paper 2: ...

## NEEDS REVIEW (Score = 3)

### Paper N: {Title}
- **Score**: 3/5
- **Domain Match**: Partial
- **Recommendation**: USER_REVIEW
- **Rationale**: "{Why flagged for review}"
- **Concerns**: "{What's unclear}"

## REJECTED (Score <= 2)

### Paper M: {Title}
- **Score**: 1/5
- **Domain Match**: No
- **Recommendation**: REJECT
- **Rationale**: "{Why rejected}"
- **Flag**: DOMAIN_MISMATCH
```

---

### 5. User Selection

**Action**: Present recommendations and get user approval

**Display Format**:
```
══════════════════════════════════════════════════════
PAPER SELECTION - {Project Name}
══════════════════════════════════════════════════════

APPROVED ({N} papers) - AI recommends including:
  1. [x] Paper Title (5/5) - {brief rationale}
  2. [x] Paper Title (4/5) - {brief rationale}
  ...

NEEDS REVIEW ({N} papers) - Please decide:
  3. [ ] Paper Title (3/5) - {concern}
  4. [ ] Paper Title (3/5) - {concern}
  ...

REJECTED ({N} papers) - AI recommends excluding:
  [SKIP] Paper Title (1/5) - Wrong domain
  [SKIP] Paper Title (2/5) - Not relevant
  ...

──────────────────────────────────────────────────────
Commands:
  'approve all'     - Accept AI recommendations
  'add N'           - Include paper N from NEEDS REVIEW
  'remove N'        - Exclude paper N from APPROVED
  'show N'          - View full abstract for paper N
  'custom'          - Make all selections manually
  'search more'     - Find additional papers
──────────────────────────────────────────────────────
```

**User Actions**:
- `approve all`: Accept all AI-approved papers
- `add 3`: Add paper #3 from NEEDS REVIEW to approved
- `remove 2`: Remove paper #2 from approved
- `show 5`: Display full abstract for paper #5
- `custom`: Manual selection mode

**Create**: `03-working/_selection_log.md`

```yaml
---
selection_date: "{ISO date}"
selection_method: "{auto|user_modified|manual}"
total_searched: {N}
total_approved: {N}
total_rejected: {N}
user_modifications:
  added:
    - "{Paper title}"
  removed:
    - "{Paper title}"
approved_by_user: true
---

# Paper Selection Log

## Selection Summary
- Search returned: {N} papers
- AI recommended: {N} papers
- User approved: {N} papers
- Final selection: {N} papers

## Approved Papers

| # | Title | Score | DOI | Status |
|---|-------|-------|-----|--------|
| 1 | {Title} | 5/5 | {DOI} | APPROVED |
| 2 | {Title} | 4/5 | {DOI} | APPROVED |
| 3 | {Title} | 3/5 | {DOI} | USER_ADDED |

## Rejected Papers

| # | Title | Score | Reason |
|---|-------|-------|--------|
| 1 | {Title} | 1/5 | Domain mismatch |
| 2 | {Title} | 2/5 | Not relevant |

## Modification History
- {timestamp}: User added "{Paper}" (was NEEDS_REVIEW)
- {timestamp}: User removed "{Paper}" (was APPROVED)
```

---

### 6. Planning Gate

**Action**: Confirm selection before Phase 2

**Gate Conditions**:
- [x] `_selection_log.md` exists
- [x] `approved_by_user: true` in frontmatter
- [x] At least 1 paper approved
- [x] `_briefing.md` exists with extraction schema

**Display**:
```
══════════════════════════════════════════════════════
PLANNING GATE - Ready for Phase 2?
══════════════════════════════════════════════════════

Research Question: "{RQ}"
Papers Selected: {N}
Extraction Fields: {N} fields defined

Estimated Phase 2:
- Download time: ~{N} minutes
- Analysis time: ~{N} minutes (with subagents)
- Total: ~{N} minutes

──────────────────────────────────────────────────────
[Y] Yes, proceed to Phase 2 (Download + Analyze)
[N] No, modify selection
[S] Save and continue later
──────────────────────────────────────────────────────
```

**On 'Y'**: Mark Phase 1 complete, start Phase 2
**On 'N'**: Return to Step 5 (User Selection)
**On 'S'**: Save state, update steps.md with progress

---

## Phase 1 Checklist

Before proceeding to Phase 2, verify:

- [ ] Project structure created (`02-projects/NN-{slug}/`)
- [ ] `overview.md` has `type: research`
- [ ] `02-resources/_briefing.md` exists with schema
- [ ] `02-resources/_search_results.md` exists
- [ ] `02-resources/_abstract_reviews.md` exists
- [ ] `03-working/_selection_log.md` exists
- [ ] `approved_by_user: true` in selection log
- [ ] At least 1 paper approved

---

**Next**: [Phase 2: Execution Workflow](phase2_execution.md)
