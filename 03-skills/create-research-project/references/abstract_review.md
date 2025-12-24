# Abstract Review Process

How AI reviews paper abstracts to assess relevance before download.

---

## Purpose

The abstract review prevents downloading wrong papers by:
1. Assessing domain relevance before committing resources
2. Flagging potential mismatches for user review
3. Providing rationale for each recommendation

---

## Review Criteria

### 1. Domain Match (40% weight)

**Question**: Is this paper from the right field/domain?

**Signals of MATCH**:
- Keywords align with research domain
- Methods match expected approaches
- Terminology is consistent with field
- Authors/venues are recognized in domain

**Signals of MISMATCH**:
- Same terms, different meaning (e.g., "thematic fit" in linguistics vs qualitative research)
- Wrong field entirely (e.g., music classification instead of research methods)
- Technical jargon from unrelated domain

**Examples**:
```
MATCH: "This paper presents a reflexive thematic analysis of interview data..."
  → Uses TA terminology correctly in qualitative research context

MISMATCH: "We measure thematic fit using predicate-argument structure..."
  → "Thematic fit" is linguistics term, not qualitative research
```

---

### 2. Research Question Fit (35% weight)

**Question**: Does this paper address our research question?

**Assessment**:
- Direct: Paper directly answers RQ
- Indirect: Paper provides relevant background/methods
- Tangential: Paper touches on related topics
- Unrelated: Paper doesn't connect to RQ

**Examples** (RQ: "How can LLMs be integrated into thematic analysis?"):
```
DIRECT: "We present an LLM-based pipeline for automated thematic coding..."
  → Exactly what we're looking for

INDIRECT: "This paper outlines best practices for reflexive thematic analysis..."
  → Background on TA, but no LLM content

TANGENTIAL: "We use GPT-4 for qualitative survey analysis..."
  → Related (LLM + qualitative) but not specifically TA

UNRELATED: "Deep learning for image classification..."
  → No connection to RQ
```

---

### 3. Methodology Relevance (15% weight)

**Question**: Are the methods useful for our research?

**Consider**:
- Research design applicable to our context?
- Methods transferable to our domain?
- Evaluation approaches we could use?

---

### 4. Recency (10% weight)

**Question**: How current is this research?

**Scoring**:
- Last 2 years: Full credit
- 2-5 years: Slight discount
- 5+ years: Flag as potentially outdated (unless foundational)

**Exception**: Foundational papers (e.g., Braun & Clarke 2006) get full credit regardless of age.

---

## Scoring System

### Overall Score (1-5)

| Score | Meaning | Action |
|-------|---------|--------|
| **5** | Highly relevant, must include | Auto-APPROVE |
| **4** | Relevant, recommend include | Auto-APPROVE |
| **3** | Marginal, user should decide | FLAG for review |
| **2** | Likely irrelevant, recommend skip | Auto-REJECT |
| **1** | Wrong domain, definitely skip | Auto-REJECT |

### Score Calculation

```python
def calculate_score(domain_match, rq_fit, method_relevance, recency):
    """
    Calculate overall relevance score.

    Args:
        domain_match: 0.0-1.0 (how well domain matches)
        rq_fit: 0.0-1.0 (how well addresses RQ)
        method_relevance: 0.0-1.0 (methodology usefulness)
        recency: 0.0-1.0 (how recent)

    Returns:
        score: 1-5
    """
    weighted = (
        domain_match * 0.40 +
        rq_fit * 0.35 +
        method_relevance * 0.15 +
        recency * 0.10
    )

    # Convert 0-1 to 1-5 scale
    score = round(weighted * 4 + 1)
    return max(1, min(5, score))
```

---

## Flags

### DOMAIN_MISMATCH
**When**: Terms suggest wrong field
**Example**: "Thematic fit" in linguistics context
**Action**: Auto-REJECT unless user overrides

### OUTDATED
**When**: Paper >5 years old, not foundational
**Example**: 2015 paper on general ML
**Action**: FLAG for review

### NO_ABSTRACT
**When**: Abstract not available from API
**Example**: Some older papers in databases
**Action**: FLAG, user must manually check

### DUPLICATE
**When**: Same paper from multiple sources
**Example**: Paper in both Semantic Scholar and arXiv
**Action**: Keep one, mark other as duplicate

### FOUNDATIONAL
**When**: Paper is seminal/foundational work
**Example**: Braun & Clarke 2006 for TA
**Action**: Auto-APPROVE regardless of age

### LOW_CONFIDENCE
**When**: AI unsure about relevance
**Example**: Interdisciplinary paper
**Action**: FLAG for user review

---

## Review Output Format

### For Each Paper

```yaml
paper_id: "{id}"
title: "{title}"
authors: "{authors}"
year: {year}

# Scores
domain_match_score: 0.9
rq_fit_score: 0.8
method_relevance_score: 0.7
recency_score: 1.0
overall_score: 4

# Assessment
domain_match: true
direct_rq_address: false
indirect_rq_relevance: true

# Flags
flags: []  # or [OUTDATED, LOW_CONFIDENCE, etc.]

# Recommendation
recommendation: APPROVE  # APPROVE | REVIEW | REJECT
rationale: "Paper provides comprehensive overview of reflexive TA methodology. While it doesn't specifically address LLMs, it's essential background for understanding the domain."

# Key Terms Identified
key_terms:
  - "reflexive thematic analysis"
  - "qualitative coding"
  - "inductive analysis"

# Concerns (if any)
concerns: null  # or "Methodology section is brief"
```

---

## Example Reviews

### Example 1: High Relevance (Score 5)

```yaml
title: "LLM-Assisted Thematic Analysis: A Multi-Agent Approach"
year: 2024

domain_match_score: 1.0
rq_fit_score: 1.0
method_relevance_score: 0.9
recency_score: 1.0
overall_score: 5

recommendation: APPROVE
rationale: "Directly addresses LLM integration with TA. Uses multi-agent approach similar to our research direction. Very recent (2024) and highly relevant methodology."
```

### Example 2: Wrong Domain (Score 1)

```yaml
title: "Measuring Thematic Fit: Predicate-Argument Structures in Sentence Processing"
year: 2022

domain_match_score: 0.0
rq_fit_score: 0.0
method_relevance_score: 0.1
recency_score: 0.8
overall_score: 1

flags: [DOMAIN_MISMATCH]
recommendation: REJECT
rationale: "Despite 'thematic' in title, this is computational linguistics paper about sentence parsing. 'Thematic fit' refers to predicate-argument relationships, not qualitative research themes. Wrong domain entirely."
```

### Example 3: Marginal (Score 3)

```yaml
title: "GPT-4 for Qualitative Survey Analysis"
year: 2024

domain_match_score: 0.6
rq_fit_score: 0.5
method_relevance_score: 0.7
recency_score: 1.0
overall_score: 3

flags: [LOW_CONFIDENCE]
recommendation: REVIEW
rationale: "Uses LLMs for qualitative analysis but focuses on survey data, not interview transcripts. Methods may be transferable but paper doesn't specifically address thematic analysis. User should decide if relevant."
concerns: "May be too focused on survey-specific methods"
```

### Example 4: Foundational (Score 5 despite age)

```yaml
title: "Using Thematic Analysis in Psychology"
year: 2006

domain_match_score: 1.0
rq_fit_score: 0.7
method_relevance_score: 1.0
recency_score: 0.0  # Old paper
overall_score: 5  # Override due to foundational flag

flags: [FOUNDATIONAL]
recommendation: APPROVE
rationale: "Seminal paper defining 6-phase thematic analysis methodology. Essential background despite age. All subsequent TA research builds on this foundation."
```

---

## Process Flow

```
1. Receive paper abstract
       ↓
2. Extract key terms
       ↓
3. Check domain match
   ├─ MISMATCH → Score 1-2, REJECT
   └─ MATCH → Continue
       ↓
4. Assess RQ fit
   ├─ UNRELATED → Score 2, REJECT
   ├─ TANGENTIAL → Score 3, REVIEW
   └─ DIRECT/INDIRECT → Continue
       ↓
5. Evaluate methodology
       ↓
6. Check recency
   └─ Apply FOUNDATIONAL override if applicable
       ↓
7. Calculate overall score
       ↓
8. Generate recommendation
   ├─ Score >= 4 → APPROVE
   ├─ Score == 3 → REVIEW
   └─ Score <= 2 → REJECT
       ↓
9. Write rationale
```

---

## User Override

Users can always override AI recommendations:

```
AI recommends: REJECT (Score 2)
User action: 'add 15'  # Include paper despite low score

Result: Paper included with note:
  - original_recommendation: REJECT
  - user_override: true
  - override_reason: "User included despite AI recommendation"
```

This allows:
- Including papers AI may have misjudged
- Excluding papers AI rated highly
- Manual curation of final selection

---

**Used in**: [Phase 1: Planning Workflow](phase1_planning.md)
