# Synthesis Pipeline Improvements - Plan

**Last Updated**: 2025-12-28
**Status**: PLANNING - Schema-Redesign v3.2 (Final Validated)
**Validated By**: 13 parallel codebase exploration agents across 2 sessions

---

## Executive Summary

### Das Problem
Die Synthesis-Phase kann Chunks nicht intelligent zu Research Questions zuordnen, weil:
1. `index.md` hat keine Chunk-Level `fields_found` Bewertung
2. User muss Research Question UND alle Fields manuell definieren
3. Subagent-Output ist inkonsistent → Aggregation braucht AI-Interpretation

### Die Lösung
**Forced Field Assessment** mit AI-generierter Field-Definition:

1. **User definiert NUR Research Question** → AI generiert Field-Vorschläge → User bestätigt
2. **Analysis-Subagent sieht _briefing.md** → bewertet jeden Chunk: `fields_found: {field: true/false/partial}`
3. **Routing-Script** liest `fields_found` → deterministisches Chunk-Matching
4. **Subagent-Output** hat strukturierte `patterns[]` → Script-basierte Aggregation

### v3.2 Changes (from v3.1)
- Added G22a: `research_purpose` field in `_briefing.md` (WHY context)
- Added G22b: `synthesis_goals` section in `_analysis_kit.md`
- Documented REJECTED proposals (G20, G21, G22c, G22d)
- Added SACRED COWS section (elements that MUST NOT change)
- Enhanced execution steps with complete file references

---

## Teil 0: Validated Gaps

### CRITICAL GAPS (Must Fix)

| Gap | Issue | File to Fix | Reference File | Line Numbers |
|-----|-------|-------------|----------------|--------------|
| **G1** | No calibration spec for `fields_found` | `paper-analyze-core/SKILL.md` | `extraction_guide_template.md` | Add after line ~100 |
| **G2** | Level 7 has no token budget | `synthesize-research-project/SKILL.md` | `paper-analyze-core/SKILL.md:464-489` | Full rewrite |
| **G3** | Inconsistent token formulas | ALL files with token calc | `config.py:15` | Search: `/ 5`, `* 1.3` |
| **G13** | No file allowlist for subagents | `analyze-research-project/SKILL.md` | `paper-analyze-core/SKILL.md:27-31` | Add to Step 2 |
| **G19** | No field sparsity check | `build_synthesis_routing.py` (NEW) | - | New script |

### HIGH PRIORITY GAPS (Should Fix)

| Gap | Issue | File to Fix | Reference File | Line Numbers |
|-----|-------|-------------|----------------|--------------|
| **G5** | No AI field generation prompt | `create-research-project/SKILL.md` | `extraction_guide_template.md` | Modify Step 2 |
| **G15** | Quote-line verification not implemented | `validate_analysis.py` | `analysis_log_template.md:243-287` | Add Rule 8 |
| **G16** | No partial save on timeout | `analyze-research-project/SKILL.md` | `_resume.md` pattern | Add to Error Handling |
| **G18** | No structured N/A format | `paper-analyze-core/SKILL.md` | - | Add template |
| **G22a** | Missing research purpose context | `_briefing.md` schema | - | Add field |
| **G22b** | Missing synthesis goals for subagents | `_analysis_kit.md` template | - | Add section |

### ALREADY HANDLED (Confirmed by Agents)

| Gap | Finding | Evidence Location |
|-----|---------|-------------------|
| ~~G4~~ | Verification protocol EXISTS | `analyze-research-project/SKILL.md:572-583` |
| ~~G17~~ | MAX_RETRIES=3 defined | `paper_download.py:51` |

### REJECTED PROPOSALS (Validated as Unnecessary/Harmful)

| Proposal | Verdict | Reason | Agent Evidence |
|----------|---------|--------|----------------|
| G20: Chunk summaries in YAML | **REDUNDANT** | Already exists in "Chunk Navigation" body section of index.md | Agent 1: +40-50% token overhead, breaks synthesis budget |
| G21: Generic index schema | **PREMATURE** | No non-paper corpus planned; renaming `fields_found` to `content_tags` breaks routing script | Agent 2: YAGNI - do it IF needed later |
| G22c: `related_papers_context` | **IMPOSSIBLE** | Papers analyzed IN PARALLEL (15 concurrent) - no cross-paper context available at analysis time | Agent 3: Architectural conflict |
| G22d: `example_extraction` per field | **REDUNDANT** | Already exists in `_extraction_guide.md` | Agent 3: Use existing file |

---

## Teil 0.5: SACRED COWS (DO NOT MODIFY)

These patterns have been proven across 25 sessions and 21 analyzed papers:

### 1. The 7-Step Methodology (paper-analyze-core/SKILL.md)
```
Step 0: Initialize Analysis Log FIRST    ← Enables partial recovery
Step 1: Read Briefing                    ← Research question drives extraction
Step 2: Read Metadata                    ← Chunk count validation
Step 3: Analyze Chunks (3-point evidence)← Anti-hallucination
Step 4: Compile index.md                 ← Output format for synthesis
Step 5: Validate                         ← Checklist catches incomplete
Step 6: Complete Log LAST                ← Duration metrics
```
**NEVER renumber these steps.**

### 2. 3-Point Anti-Hallucination Sampling
```
start (100 chars) + mid (100 chars at 50%) + end (100 chars) + SHA256 hash
```
**NEVER remove or modify this pattern.**

### 3. Chunk:Line Reference Format
```
Format: "Chunk N:Line-Line" (e.g., "Chunk 2:89-95")
```
**21 papers use this format. Changing it requires full re-analysis.**

### 4. Two-Tier Output Strategy
```
_analysis_log.md → HIGH detail (150-char quotes) → Validation & traceability
index.md frontmatter → MEDIUM detail (50-80 chars) → Synthesis optimization (40+ papers must fit)
```
**NEVER change quote lengths without proving token budget compliance.**

### 5. Schema Version Tracking
```
Current: v2.2 (with extraction tracking, chunk:line references)
```
**Always bump version on schema changes. Validation script checks version.**

---

## Teil 1: Neuer Flow

```
USER INPUT                          AI GENERATION                      USER CONFIRMATION
───────────────────────────────────────────────────────────────────────────────────────

"What are foundational            AI generates:                      User confirms:
 ontologies for digital           - entity_types                     ✓ entity_types
 work?"                           - entity_definitions               ✓ entity_definitions
                                  - framework_comparison             ✗ remove: methodology
                                  - ai_integration                   + add: agent_modeling
                                  - methodology

                                           ↓

                                    _briefing.md
                                    (fields = confirmed list)
                                    + research_purpose (G22a)
```

---

## Teil 2: Schema-Änderungen (EXAKTE FILE-REFERENZEN)

### 2.1 `_briefing.md` Schema (G22a Enhancement)

**File**: `02-projects/{project}/02-resources/_briefing.md`
**Reference**: `02-projects/02-ontologies-research/02-resources/_briefing.md`

**Current Schema**:
```yaml
research_question: "What are the foundational ontologies..."
extraction_schema:
  - field: entity_types
    description: "Core entity types defined"
    priority: high
```

**New Schema (G22a: Add research_purpose)**:
```yaml
research_question: "What are the foundational ontologies for digital work?"

# G22a: WHY this research matters (provides context to subagents)
research_purpose: "Validate the 8-entity hypothesis for UDWO metamodel grounding. Inform internal ontology design for AI agent orchestration platform."

domain: "Ontology Engineering, Knowledge Representation"

extraction_schema:
  - field: entity_types
    description: "Core entity types defined in ontology"
    priority: high
  # ... more fields
```

**Token Impact**: +30-50 tokens (validated as acceptable)

---

### 2.2 `_analysis_kit.md` Template (G22b Enhancement)

**File**: `03-skills/research-pipeline/shared/paper-analyze-core/references/analysis_kit_template.md`
**Reference**: `02-projects/02-ontologies-research/02-resources/_analysis_kit.md`

**Add Section (G22b: Synthesis Goals)**:
```markdown
## Synthesis Goals

The synthesis phase will aggregate:
- {goal_1: e.g., "Common entity types across all frameworks"}
- {goal_2: e.g., "Comparison matrix of BFO vs DOLCE vs UFO"}
- {goal_3: e.g., "Practical recommendations for AI agent modeling"}

Focus extractions toward these aggregation targets. When in doubt about extraction relevance, consider whether it contributes to these goals.
```

**Token Impact**: +50-100 tokens (validated as acceptable)

---

### 2.3 `index.md` Schema (Analysis Output)

**File**: `{paper_path}/index.md`
**Reference**: `02-projects/02-ontologies-research/02-resources/papers/05-DOLCE.../index.md`

**New Schema (with 3-state fields_found)**:
```yaml
paper_id: "05-DOLCE"
chunks_expected: 2
chunks_read: 2
analysis_complete: true

# NEU: Chunk-Level Field Assessment (3-STATE)
chunk_index:
  1:
    token_count: 12500
    hash: "a7b8c9d4e5f6..."
    # 3-STATE: true = explicitly discussed, partial = mentioned, false = absent
    fields_found:
      entity_types: true          # Explicitly defines entity types
      entity_definitions: true    # Has formal definitions
      entity_relationships: partial  # Mentioned but not detailed
      methodology: false          # Not in this chunk
      # ... ALLE Fields aus _briefing.md MÜSSEN gelistet sein
  2:
    token_count: 8200
    hash: "g7h8i9j0k1l2..."
    fields_found:
      entity_types: partial       # References types but no new ones
      framework_comparison: true
      # ... ALLE Fields

# STANDARDISIERTES Item-Schema für alle Fields
entity_types:
  - item: "Endurant (Continuant)"
    chunk: 1
    lines: "128-133"
    quote: "An entity wholly present at any time..."
  - item: "Perdurant (Occurrent)"
    chunk: 1
    lines: "131-133"
    quote: "An entity that can be partially present..."

# STRUCTURED N/A FORMAT (Gap G18)
methodology:
  - item: "NOT_FOUND"
    chunk: null
    lines: null
    quote: null
    reason: "Paper does not discuss research methodology"
```

**3-State `fields_found` Definition:**

| State | Meaning | Include in Synthesis? | Calibration Rule |
|-------|---------|----------------------|------------------|
| `true` | Field explicitly discussed with extractable content | YES (primary) | Has definitions, lists, examples |
| `partial` | Field mentioned/referenced but not detailed | YES (secondary) | Referenced but no extractable content |
| `false` | Field not present in chunk | NO | No mention at all |

---

## Teil 3: Exakte File-Änderungen

### 3.1 `create-research-project/SKILL.md` (Gap G5 + G22a)

**File**: `03-skills/research-pipeline/orchestrators/create-research-project/SKILL.md`

**MUST READ FIRST**:
- `03-skills/research-pipeline/shared/paper-analyze-core/references/extraction_guide_template.md`

**Änderung in Step 2** (currently lines ~207-234):

```markdown
## Step 2: Define Research Question (with AI Field Generation)

**Gap G5 Fix: AI-Generated Field Suggestions**
**Gap G22a Fix: Add research_purpose field**

Interactive session:

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
   Domain detected: Ontology Engineering, Knowledge Representation
   Key concepts: foundational, ontologies, digital work

   SUGGESTED FIELDS:
   ┌─────────────────────────────────────────────────────────────┐
   │ 1. entity_types        - Core entity types in ontologies    │
   │ 2. entity_definitions  - Formal definitions of entities     │
   │ 3. entity_relationships- How entities relate to each other  │
   │ 4. framework_comparison- Comparisons between frameworks     │
   │ 5. abstraction_level   - Level of ontology abstraction      │
   │ 6. methodology         - Research methodology used          │
   │ 7. limitations         - Stated limitations                 │
   │ 8. tools_standards     - Technical implementations          │
   └─────────────────────────────────────────────────────────────┘

   FIELD QUALITY CHECK:
   ⚠ "methodology" is generic - consider removing if not research-focused
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

**FIELD GENERATION PROMPT TEMPLATE** (for AI):
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
```

---

### 3.2 `paper-analyze-core/SKILL.md` (Gaps G1, G3, G18)

**File**: `03-skills/research-pipeline/shared/paper-analyze-core/SKILL.md`

**MUST READ FIRST**:
- `03-skills/research-pipeline/shared/paper-analyze-core/references/analysis_log_template.md`
- `03-skills/research-pipeline/shared/paper-analyze-core/references/extraction_guide_template.md`

**Änderung 1: Field Calibration Spec (Gap G1)** - ADD after Step 1 (around line ~100):

```markdown
### Step 1b: Record Field List and Calibration

After reading `_briefing.md`, record ALL field names:

```yaml
steps.step1_read_briefing:
  completed: true
  research_purpose: "{from _briefing.md}"  # G22a context
  fields_to_assess: ["entity_types", "entity_definitions", ...]
```

**CALIBRATION: What Counts as TRUE/PARTIAL/FALSE**

For EACH field, use this decision tree:

```
Does chunk EXPLICITLY discuss this field?
├─ YES → Does it provide extractable content (definitions, lists, examples)?
│        ├─ YES → fields_found: TRUE
│        └─ NO (just mentions) → fields_found: PARTIAL
└─ NO → fields_found: FALSE
```

**Examples by Field Type:**

| Field Type | TRUE (extract) | PARTIAL (include, lower priority) | FALSE (skip) |
|------------|----------------|-----------------------------------|--------------|
| `entity_types` | "The framework defines three entity types: Agent, Activity, Entity" | "Various entity types exist in the literature" | No mention of entities |
| `methodology` | "We conducted semi-structured interviews with 15 participants" | "Following standard qualitative methods" | No methodology section |
| `limitations` | "This approach is limited by X, Y, Z" | "Further work is needed" | No limitations mentioned |

**CRITICAL**: Read `_extraction_guide.md` for project-specific calibration examples.
```

**Änderung 2: Step 3 with 3-State Assessment** (around lines ~120-210):

```markdown
### Step 3: Analyze Chunks (with Forced Field Assessment)

For each chunk `{paper}_N.md` in order:

1. **Read FULL chunk content**
2. **ASSESS FIELDS** (REQUIRED - 3-STATE):

   For EVERY field from `_briefing.md`, determine using calibration rules:
   - `true`: Explicitly discusses with extractable content
   - `partial`: Mentions or references without detail
   - `false`: Not present in chunk

   ```yaml
   chunk_index:
     {N}:
       token_count: {calculate using STANDARD FORMULA: len(content) // 4}
       hash: "{SHA256 of chunk content}"
       fields_found:
         entity_types: true      # Has extractable entity types
         entity_definitions: true
         entity_relationships: partial  # Mentioned, not detailed
         ai_integration: false
         # ... EVERY field from _briefing.md must be listed!
   ```

3. **Extract items** for fields where `fields_found[field]` in [true, partial]
4. **Record 3-point evidence** (start/mid/end + hash - SACRED, do not modify)
5. **Write chunk summary and load triggers** (in body, NOT frontmatter)

**CRITICAL**: You MUST assess EVERY field for EVERY chunk. Missing fields = validation failure.
```

**Änderung 3: Token Estimation Formula (Gap G3)** - MODIFY Token Budget section (around line ~464):

```markdown
## Token Budget

**STANDARD TOKEN FORMULA** (use consistently EVERYWHERE):
```python
def estimate_tokens(text: str) -> int:
    """Standard token estimation for all pipeline components.

    Source: 00-system/core/nexus/config.py:15
    DO NOT use other formulas like chars/5*1.3
    """
    return len(text) // 4
```

| Component | Tokens | Notes |
|-----------|--------|-------|
| This methodology | ~3,000 | Fixed |
| _briefing.md | ~2,000 | Variable (+30-50 for research_purpose) |
| _analysis_kit.md | ~500 | Variable (+50-100 for synthesis_goals) |
| _metadata.json | ~500 | Small |
| Analysis log overhead | ~3,500 | Schema v2.2 |
| Paper chunks | ~74,000 | **Main content** |
| Output generation | ~17,000 | index.md + log |

**Usable budget**: `74,000 - (39 × chunk_count) - (150 × extraction_count)` tokens.
```

**Änderung 4: Structured N/A Format (Gap G18)** - ADD after Item Schema section:

```markdown
### Field Not Found Format (Gap G18)

When a field has NO content in the paper (all chunks are `false`), use this structured format:

```yaml
methodology:
  - item: "NOT_FOUND"
    chunk: null
    lines: null
    quote: null
    reason: "Paper does not discuss research methodology"
```

**Standard Reasons** (use exactly these phrases):
- "Paper does not discuss {field_name}"
- "Field not applicable to this paper type"
- "Content exists but is insufficient for extraction"

**DO NOT** leave field empty or omit it. Structured N/A enables validation.
```

---

### 3.3 `analyze-research-project/SKILL.md` (Gaps G13, G16)

**File**: `03-skills/research-pipeline/orchestrators/analyze-research-project/SKILL.md`

**MUST READ FIRST**:
- `03-skills/research-pipeline/shared/paper-analyze-core/SKILL.md`

**Änderung 1: Subagent INPUT CONTRACT (Gap G13)** - ADD to Step 2 (around line ~400):

```markdown
### Step 2: Analyze Papers (with INPUT CONTRACT)

**SUBAGENT INPUT CONTRACT (STRICT - Gap G13 Fix)**

Each subagent receives explicit file access rules in its prompt:

```markdown
## INPUT CONTRACT (STRICT)

### Files You MUST Read (in this order)
1. `03-skills/research-pipeline/shared/paper-analyze-core/SKILL.md`
2. `{project_path}/02-resources/_briefing.md`
3. `{project_path}/02-resources/_analysis_kit.md`
4. `{project_path}/02-resources/_extraction_guide.md`
5. `{paper_path}/_metadata.json`
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

**SUBAGENT PROMPT TEMPLATE:**
```python
Task(
  subagent_type="general-purpose",
  prompt=f"""
## Paper Analysis Task: {paper_id}

## INPUT CONTRACT (STRICT)
{INPUT_CONTRACT_TEXT}

## CONTEXT
Research Purpose: {research_purpose}  # G22a
Synthesis Goals: {synthesis_goals}    # G22b

## PROCESSING CONTRACT
1. Read files IN ORDER listed above
2. For EVERY chunk, assess EVERY field: true/partial/false (see calibration in SKILL.md)
3. Extract items only for true/partial fields
4. Compute SHA256 hash for each chunk
5. Record 3-point evidence (start/mid/end) for each chunk

## OUTPUT CONTRACT
Write these files:
1. `{paper_path}/_analysis_log.md` (Schema v2.2)
2. `{paper_path}/index.md` (with chunk_index in frontmatter)

YAML must include:
- chunk_index with fields_found for ALL fields
- Standardized item schema for extractions
- Structured N/A for missing fields (Gap G18 format)
"""
)
```
```

**Änderung 2: Partial Save on Timeout (Gap G16)** - ADD to Error Handling section:

```markdown
### Error Handling (with Partial Save - Gap G16)

| Step | Error | Action |
|------|-------|--------|
| Step 2 | Subagent timeout | **PARTIAL SAVE** (see below) |
| Step 2 | Subagent fails | Retry once, then mark failed |

**Timeout Partial Save Protocol:**

When timeout occurs, subagent MUST write partial progress:

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
```

---

### 3.4 `synthesize-research-project/SKILL.md` (Gap G2)

**File**: `03-skills/research-pipeline/orchestrators/synthesize-research-project/SKILL.md`

**MUST READ FIRST**:
- `03-skills/research-pipeline/shared/paper-analyze-core/SKILL.md:464-489` (token budget example)

**MAJOR REWRITE** - 7-Level Architecture with Token Budgets:

```markdown
## Architecture: 7-Level Hierarchical Synthesis

LEVEL 1: ROUTING (Script)
├── Input: All index.md (chunk_index.fields_found) + _briefing.md
├── Script: build_synthesis_routing.py
├── Algorithm: Boolean lookup - if chunk.fields_found[field] in [true, partial] → include
├── **Sparsity Check (Gap G19)**: Warn if field matches >80% of chunks
└── Output: 02-resources/_synthesis_routing.yaml

LEVEL 2: ALLOCATION (Script)
├── Input: _synthesis_routing.yaml
├── Script: calculate_subagent_allocation.py
├── Algorithm: Greedy bin-packing with 70k token budget per batch
├── **Level 7 Budget**: Calculate dynamically, split if >75k input
└── Output: 02-resources/_subagent_plan.yaml

LEVEL 3: PROMPT GENERATION (Script)
├── Input: _subagent_plan.yaml + _briefing.md
├── Script: generate_subagent_prompts.py
├── **Includes INPUT CONTRACT** (Gap G13)
├── **Includes research_purpose** (G22a)
├── **Includes synthesis_goals** (G22b)
└── Output: 03-working/prompts/_prompt_{batch_id}.md

LEVEL 4: EXTRACTION (Subagents - parallel, max 15 concurrent)
├── Input: _prompt_{batch_id}.md (Subagent reads ONLY this file + chunks listed in it)
├── Subagent extracts patterns from chunks
└── Output: 03-working/_batch_{field}_{N}.md (YAML patterns[])

LEVEL 5: VERIFICATION (Script)
├── Input: _batch_*.md + _subagent_plan.yaml
├── Script: verify_subagent_output.py
├── **Quote-Line Verification (Gap G15)**: Spot-check quotes exist at cited lines
└── Output: _verification_report.yaml

LEVEL 6: AGGREGATION (Script - NOT Subagent!)
├── Input: All _batch_{field}_*.md
├── Script: aggregate_patterns.py
├── Algorithm: Merge patterns[], dedupe by name, merge sources
└── Output: 04-outputs/_synthesis_{field}.yaml

LEVEL 7: FINAL REPORT (Subagent) - **WITH TOKEN BUDGET (Gap G2)**
├── Input: All _synthesis_{field}.yaml + _briefing.md
├── **Token Budget**: See calculation below
├── Subagent: Narrative synthesis, cross-field insights
└── Output: 04-outputs/_synthesis_report.md
```

**LEVEL 7 TOKEN BUDGET (Gap G2 Fix):**

```python
# In calculate_subagent_allocation.py
def calculate_level7_budget(synthesis_files: List[Path]) -> dict:
    """Calculate token budget for Level 7 final report subagent."""
    total_input_tokens = 0
    for f in synthesis_files:
        content = f.read_text()
        total_input_tokens += len(content) // 4  # Standard formula (G3)

    budget = {
        'methodology': 3000,           # Fixed
        'briefing': 2000,              # Fixed (+50 for research_purpose)
        'synthesis_files': total_input_tokens,
        'output_reservation': 20000,   # For final report
        'total_available': 100000,
        'usable': 100000 - 3000 - 2000 - 20000 - total_input_tokens
    }

    if budget['usable'] < 10000:
        # Need hierarchical aggregation
        budget['requires_split'] = True
        budget['split_strategy'] = 'group_by_priority'  # High-priority fields first

    return budget
```

**If synthesis files exceed budget:**
1. Group fields by priority (high first, from _briefing.md)
2. Generate multiple Level 7 passes (each within budget)
3. Final merge pass combines all Level 7 outputs

**Token Budget Table (Level 7):**

| Component | Tokens | Notes |
|-----------|--------|-------|
| Methodology | 3,000 | Fixed |
| _briefing.md | 2,000 | Fixed (+50 for research_purpose) |
| Synthesis files | Variable | Sum of all _synthesis_{field}.yaml |
| Output reservation | 20,000 | Final report |
| **Max synthesis input** | **75,000** | Before requiring split |
```

---

### 3.5 Neue Scripts (zu erstellen)

**Location**: `03-skills/research-pipeline/validation/`

| Script | Input | Output | Gaps | Dependencies |
|--------|-------|--------|------|--------------|
| `build_synthesis_routing.py` | index.md, _briefing.md | `_synthesis_routing.yaml` | G19 | PyYAML |
| `calculate_subagent_allocation.py` | `_synthesis_routing.yaml` | `_subagent_plan.yaml` | G2 | PyYAML |
| `generate_subagent_prompts.py` | `_subagent_plan.yaml`, `_briefing.md`, `_analysis_kit.md` | `_prompt_{batch_id}.md` | G13, G22a, G22b | PyYAML |
| `verify_subagent_output.py` | `_batch_*.md`, `_subagent_plan.yaml` | `_verification_report.yaml` | G15 | PyYAML |
| `aggregate_patterns.py` | `_batch_{field}_*.md` | `_synthesis_{field}.yaml` | - | PyYAML |

**Script Specifications** - See Teil 7 for full implementation code.

---

### 3.6 `validate_analysis.py` Updates (Gap G15)

**File**: `03-skills/research-pipeline/validation/validate_analysis.py`

**MUST READ FIRST**:
- `03-skills/research-pipeline/shared/paper-analyze-core/references/analysis_log_template.md:243-287`

**ADD Rule 8: Quote-Line Verification (Gap G15)**:

```python
def verify_quote_at_line(paper_path: Path, chunk: int, lines: str, quote: str) -> bool:
    """Verify that quote exists at specified line range in chunk file.

    Gap G15: Currently schema requires chunk:line refs but validation
    doesn't check if quotes actually exist at cited lines.

    Args:
        paper_path: Path to paper folder (e.g., .../papers/05-DOLCE_...)
        chunk: Chunk number (1-indexed)
        lines: Line range string (e.g., "128-133")
        quote: Quote text to verify (first 50 chars used for matching)

    Returns:
        True if quote found at lines, False otherwise
    """
    # Build chunk filename
    paper_id = paper_path.name
    chunk_file = paper_path / f"{paper_id}_{chunk}.md"

    if not chunk_file.exists():
        return False

    content_lines = chunk_file.read_text(encoding='utf-8').split('\n')
    start, end = map(int, lines.split('-'))

    # Extract cited lines (1-indexed to 0-indexed)
    cited_text = '\n'.join(content_lines[start-1:end])

    # Check if quote appears in cited lines (fuzzy match, first 50 chars)
    quote_start = quote[:50].strip()
    return quote_start in cited_text


# Add to validation rules (after existing Rule 7):
def validate_paper(paper_path: Path, briefing: dict) -> ValidationResult:
    # ... existing rules 1-7 ...

    # Rule 8: Quote-Line Verification (Sample) - Gap G15
    frontmatter = load_yaml_frontmatter(paper_path / 'index.md')

    for field_name, items in frontmatter.items():
        if not isinstance(items, list) or len(items) == 0:
            continue

        # Spot-check first 3 items per field (not all - performance)
        for item in items[:3]:
            if not all(k in item for k in ['chunk', 'lines', 'quote']):
                continue
            if item['chunk'] is None:  # Structured N/A format
                continue

            if not verify_quote_at_line(
                paper_path,
                item['chunk'],
                item['lines'],
                item['quote']
            ):
                result.warn(
                    f"Quote verification failed: {field_name}['{item.get('item', '?')}'] "
                    f"at Chunk {item['chunk']}:{item['lines']}"
                )

    return result
```

---

### 3.7 `_analysis_kit.md` Template Update (Gap G22b)

**File**: `03-skills/research-pipeline/orchestrators/create-research-project/references/analysis_kit_template.md`

> **Note**: Template is in `create-research-project/references/`, not `paper-analyze-core/references/`.

**ADD Synthesis Goals Section**:

```markdown
## Synthesis Goals (G22b)

The synthesis phase will aggregate findings toward these goals:

1. **{goal_1}**: {description}
   - e.g., "Common entity types across all frameworks"

2. **{goal_2}**: {description}
   - e.g., "Comparison matrix of BFO vs DOLCE vs UFO"

3. **{goal_3}**: {description}
   - e.g., "Practical recommendations for AI agent modeling"

**Extraction Guidance**: When in doubt about whether to extract something, ask: "Does this contribute to the synthesis goals above?" If yes, extract with appropriate `fields_found` state.
```

---

## Teil 4: Routing-Algorithmus (3-State Boolean Lookup)

**NO AI INTERPRETATION** - The analysis subagent has already decided.

```python
# build_synthesis_routing.py - 3-STATE Boolean Lookup
for field in briefing['extraction_schema']:
    field_name = field['field']

    for paper in papers:
        index = load_yaml_frontmatter(paper / 'index.md')
        chunk_index = index.get('chunk_index', {})

        for chunk_num, chunk_data in chunk_index.items():
            status = chunk_data['fields_found'].get(field_name, False)

            # 3-STATE: Include TRUE and PARTIAL
            if status in [True, 'true', 'partial']:
                routing[field_name].append({
                    'paper_id': paper.name,
                    'chunk': int(chunk_num),
                    'token_count': chunk_data['token_count'],
                    'hash': chunk_data['hash'],
                    'match_strength': 'full' if status in [True, 'true'] else 'partial'
                })
```

---

## Teil 5: Migration Strategy

**Decision: Option A - Clean Break**

1. Neues Schema für ALLE Projekte ab jetzt
2. Bestehende ontologies-research: **Re-analyze 21 Papers** mit neuem Schema
3. Vorteil: Sauberer Start, kein Legacy-Code

**Constraints:**
- Max chunk size: 500 Zeilen (confirmed)
- Token budget: 70k per subagent (Level 4), calculated for Level 7
- Kein Oversized-Chunk-Handling nötig (500 lines < 70k tokens)
- **Standard token formula**: `chars // 4` (Gap G3 - aligned with core config)

---

## Teil 6: Execution Phases (DETAILED STEPS)

### Phase 0: Planning (COMPLETE v3.2)
- [x] Identify query problem
- [x] Design forced field assessment
- [x] Document exact file changes
- [x] Run 8 validation agents on codebase (v3.1)
- [x] Run 5 validation agents on new proposals (v3.2)
- [x] Validate gaps (11 active, 4 rejected)
- [x] Document sacred cows
- [x] User review of v3.2

---

### Phase 1: Skill Documentation Updates

**Duration**: ~2-3 hours
**Prerequisite**: None

#### Step 1.1: Update `create-research-project/SKILL.md` (G5, G22a)

**Files to read first**:
```
03-skills/research-pipeline/orchestrators/create-research-project/SKILL.md
03-skills/research-pipeline/shared/paper-analyze-core/references/extraction_guide_template.md
```

**Changes**:
1. Find Step 2 (around line ~207)
2. Add research_purpose prompt (G22a) - see Teil 3.1
3. Add AI field generation flow (G5) - see Teil 3.1
4. Add FIELD GENERATION PROMPT TEMPLATE - see Teil 3.1

**Validation**: Read through modified Step 2, ensure flow is clear.

---

#### Step 1.2: Update `paper-analyze-core/SKILL.md` (G1, G3, G18)

**Files to read first**:
```
03-skills/research-pipeline/shared/paper-analyze-core/SKILL.md
03-skills/research-pipeline/shared/paper-analyze-core/references/analysis_log_template.md
03-skills/research-pipeline/shared/paper-analyze-core/references/extraction_guide_template.md
```

**Changes**:
1. Add Step 1b: Field Calibration Spec (G1) - after line ~100
2. Modify Step 3: Add 3-state fields_found assessment - around line ~120
3. Modify Token Budget section: Standardize to `chars // 4` (G3) - around line ~464
4. Add Structured N/A Format section (G18) - after Item Schema

**Validation**:
- Calibration decision tree is clear
- Token formula is `len(text) // 4` everywhere
- N/A format example is complete

---

#### Step 1.3: Update `analyze-research-project/SKILL.md` (G13, G16)

**Files to read first**:
```
03-skills/research-pipeline/orchestrators/analyze-research-project/SKILL.md
03-skills/research-pipeline/shared/paper-analyze-core/SKILL.md
```

**Changes**:
1. Add INPUT CONTRACT section to Step 2 (G13) - around line ~400
2. Add Partial Save Protocol to Error Handling (G16)
3. Update SUBAGENT PROMPT TEMPLATE to include research_purpose and synthesis_goals

**Validation**:
- INPUT CONTRACT has explicit allowlist AND forbidden list
- Timeout protocol saves partial chunk_index

---

#### Step 1.4: Rewrite `synthesize-research-project/SKILL.md` (G2)

**Files to read first**:
```
03-skills/research-pipeline/orchestrators/synthesize-research-project/SKILL.md
03-skills/research-pipeline/shared/paper-analyze-core/SKILL.md:464-489
```

**Changes**:
1. Replace entire Level architecture with 7-Level Hierarchical Synthesis
2. Add Level 7 Token Budget calculation (G2)
3. Add split strategy for large synthesis inputs

**Validation**:
- Each level has clear Input → Script/Subagent → Output
- Level 7 budget calculation is complete
- Split strategy is documented

---

#### Step 1.5: Update `_analysis_kit.md` Template (G22b)

**Files to read first**:
```
03-skills/research-pipeline/shared/paper-analyze-core/references/analysis_kit_template.md
02-projects/02-ontologies-research/02-resources/_analysis_kit.md
```

**Changes**:
1. Add "Synthesis Goals" section (G22b) - see Teil 3.7

**Validation**:
- Section has clear goal format
- Extraction guidance is actionable

---

### Phase 2: Scripts

**Duration**: ~3-4 hours
**Prerequisite**: Phase 1 complete (scripts reference new schema)

#### Step 2.1: Create `build_synthesis_routing.py` (G19)

**Location**: `03-skills/research-pipeline/validation/build_synthesis_routing.py`

**Implementation**: See Teil 7.1 for full code

**Test**:
```bash
python build_synthesis_routing.py 02-projects/02-ontologies-research
# Should output: routing table + any sparsity warnings
```

---

#### Step 2.2: Create `calculate_subagent_allocation.py` (G2)

**Location**: `03-skills/research-pipeline/validation/calculate_subagent_allocation.py`

**Implementation**: See Teil 7.2 for full code

**Test**:
```bash
python calculate_subagent_allocation.py 02-projects/02-ontologies-research
# Should output: _subagent_plan.yaml with batch allocations
```

---

#### Step 2.3: Create `generate_subagent_prompts.py` (G13, G22a, G22b)

**Location**: `03-skills/research-pipeline/validation/generate_subagent_prompts.py`

**Implementation**: See Teil 7.3 for full code

**Requirements**:
- Include INPUT CONTRACT in each prompt
- Include research_purpose (G22a)
- Include synthesis_goals (G22b)

**Test**:
```bash
python generate_subagent_prompts.py 02-projects/02-ontologies-research
# Should output: prompts in 03-working/prompts/
# Manually review 2-3 prompts for completeness
```

---

#### Step 2.4: Create `verify_subagent_output.py` (G15)

**Location**: `03-skills/research-pipeline/validation/verify_subagent_output.py`

**Implementation**: See Teil 7.4 for full code

**Requirements**:
- Check chunks_read matches expected
- Verify hashes
- Spot-check quote-line verification (G15)

**Test**:
```bash
python verify_subagent_output.py 02-projects/02-ontologies-research
# Should output: _verification_report.yaml
```

---

#### Step 2.5: Create `aggregate_patterns.py`

**Location**: `03-skills/research-pipeline/validation/aggregate_patterns.py`

**Implementation**: See Teil 7.5 for full code

**Test**:
```bash
python aggregate_patterns.py 02-projects/02-ontologies-research entity_types
# Should output: 04-outputs/_synthesis_entity_types.yaml
```

---

### Phase 3: Validation Script Updates

**Duration**: ~1 hour
**Prerequisite**: Phase 2 complete

#### Step 3.1: Update `validate_analysis.py` (G15)

**File**: `03-skills/research-pipeline/validation/validate_analysis.py`

**Changes**:
1. Add `verify_quote_at_line()` function
2. Add Rule 8: Quote-Line Verification (sample check)
3. Add validation for 3-state `fields_found`
4. Add validation for `chunk_index` structure

**Test**:
```bash
python validate_analysis.py 02-projects/02-ontologies-research/02-resources/papers/05-DOLCE...
# Should pass with any quote verification warnings noted
```

---

### Phase 4: Migration

**Duration**: ~4-6 hours (21 papers × 10-15 min each)
**Prerequisite**: Phases 1-3 complete

#### Step 4.1: Update `_briefing.md` (G22a)

**File**: `02-projects/02-ontologies-research/02-resources/_briefing.md`

**Add**:
```yaml
research_purpose: "Validate the 8-entity hypothesis for UDWO metamodel grounding. Inform internal ontology design for AI agent orchestration platform."
```

---

#### Step 4.2: Update `_analysis_kit.md` (G22b)

**File**: `02-projects/02-ontologies-research/02-resources/_analysis_kit.md`

**Add** Synthesis Goals section per template.

---

#### Step 4.3: Re-analyze 21 Papers

**For each paper**:
1. Spawn subagent with new INPUT CONTRACT
2. Subagent produces new `index.md` with `chunk_index` and 3-state `fields_found`
3. Subagent produces updated `_analysis_log.md`
4. Run `validate_analysis.py` on each paper

**Track progress**:
```
- [ ] 01-UFO
- [ ] 02-Knowledge_Graphs
- [ ] 03-...
... (21 papers)
```

---

### Phase 5: End-to-End Test

**Duration**: ~2-3 hours
**Prerequisite**: Phase 4 complete (all papers re-analyzed)

#### Step 5.1: Run Level 1 (Routing)
```bash
python build_synthesis_routing.py 02-projects/02-ontologies-research
```
**Check**: Sparsity warnings for any fields >80% coverage

#### Step 5.2: Run Level 2 (Allocation)
```bash
python calculate_subagent_allocation.py 02-projects/02-ontologies-research
```
**Check**: Level 7 budget calculated, split strategy if needed

#### Step 5.3: Run Level 3 (Prompt Generation)
```bash
python generate_subagent_prompts.py 02-projects/02-ontologies-research
```
**Check**: Prompts include INPUT CONTRACT, research_purpose, synthesis_goals

#### Step 5.4: Run Level 4 (Extraction)
Execute synthesis subagents (parallel, max 15)

#### Step 5.5: Run Level 5 (Verification)
```bash
python verify_subagent_output.py 02-projects/02-ontologies-research
```
**Check**: All batches pass, quote verification >80%

#### Step 5.6: Run Level 6 (Aggregation)
```bash
python aggregate_patterns.py 02-projects/02-ontologies-research
```
**Check**: All fields aggregated

#### Step 5.7: Run Level 7 (Final Report)
Execute final report subagent with calculated budget

**Check**: Report is coherent, citations valid

---

## Teil 7: Script Implementations

### 7.1 `build_synthesis_routing.py`

```python
#!/usr/bin/env python3
"""Build synthesis routing from index.md fields_found.

Gap G19: Includes field sparsity check (warn if >80% coverage).

Usage:
    python build_synthesis_routing.py <project_path>

Output:
    {project_path}/02-resources/_synthesis_routing.yaml
"""

import yaml
from pathlib import Path
from typing import Dict, List, Any
import sys


def load_yaml_frontmatter(file_path: Path) -> dict:
    """Load YAML frontmatter from markdown file."""
    content = file_path.read_text(encoding='utf-8')
    if content.startswith('---'):
        end = content.find('---', 3)
        if end > 0:
            return yaml.safe_load(content[3:end]) or {}
    return {}


def build_routing(project_path: Path) -> dict:
    """Build routing table from all index.md files.

    Args:
        project_path: Path to project (e.g., 02-projects/02-ontologies-research)

    Returns:
        Dict with routing table, total_chunks, and sparsity_warnings
    """
    briefing_path = project_path / '02-resources' / '_briefing.md'
    papers_path = project_path / '02-resources' / 'papers'

    if not briefing_path.exists():
        raise FileNotFoundError(f"Briefing not found: {briefing_path}")

    briefing = load_yaml_frontmatter(briefing_path)
    fields = [f['field'] for f in briefing.get('extraction_schema', [])]

    if not fields:
        raise ValueError("No fields found in extraction_schema")

    routing: Dict[str, List[Dict[str, Any]]] = {field: [] for field in fields}
    total_chunks = 0

    for paper_dir in sorted(papers_path.iterdir()):
        if not paper_dir.is_dir():
            continue

        index_path = paper_dir / 'index.md'
        if not index_path.exists():
            print(f"  Warning: No index.md in {paper_dir.name}")
            continue

        index = load_yaml_frontmatter(index_path)
        chunk_index = index.get('chunk_index', {})

        for chunk_num, chunk_data in chunk_index.items():
            total_chunks += 1
            fields_found = chunk_data.get('fields_found', {})

            for field in fields:
                status = fields_found.get(field, False)

                # 3-STATE: Include TRUE and PARTIAL
                if status in [True, 'true', 'partial']:
                    routing[field].append({
                        'paper_id': paper_dir.name,
                        'chunk': int(chunk_num),
                        'token_count': chunk_data.get('token_count', 0),
                        'hash': chunk_data.get('hash', ''),
                        'match_strength': 'full' if status in [True, 'true'] else 'partial'
                    })

    # GAP G19: FIELD SPARSITY CHECK
    warnings = []
    for field, chunks in routing.items():
        if total_chunks > 0:
            coverage = len(chunks) / total_chunks
            if coverage > 0.8:
                warnings.append({
                    'field': field,
                    'coverage': f"{coverage*100:.1f}%",
                    'chunks_matched': len(chunks),
                    'total_chunks': total_chunks,
                    'issue': 'Field matches >80% of chunks - may be too generic',
                    'recommendation': 'Consider splitting into more specific sub-fields'
                })

    return {
        'routing': routing,
        'total_chunks': total_chunks,
        'total_fields': len(fields),
        'sparsity_warnings': warnings
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: build_synthesis_routing.py <project_path>")
        print("Example: python build_synthesis_routing.py 02-projects/02-ontologies-research")
        sys.exit(1)

    project_path = Path(sys.argv[1])

    if not project_path.exists():
        print(f"Error: Project path not found: {project_path}")
        sys.exit(1)

    print(f"Building synthesis routing for: {project_path}")
    result = build_routing(project_path)

    # Write routing file
    output_path = project_path / '02-resources' / '_synthesis_routing.yaml'
    with open(output_path, 'w', encoding='utf-8') as f:
        yaml.dump(result, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    # Report results
    print(f"\n✓ Routing written to: {output_path}")
    print(f"  Total chunks: {result['total_chunks']}")
    print(f"  Total fields: {result['total_fields']}")
    print("\n  Chunks per field:")
    for field, chunks in result['routing'].items():
        full = sum(1 for c in chunks if c['match_strength'] == 'full')
        partial = sum(1 for c in chunks if c['match_strength'] == 'partial')
        print(f"    {field}: {len(chunks)} ({full} full, {partial} partial)")

    # Report sparsity warnings
    if result['sparsity_warnings']:
        print("\n⚠️  SPARSITY WARNINGS (Gap G19):")
        for w in result['sparsity_warnings']:
            print(f"  - {w['field']}: {w['coverage']} coverage ({w['chunks_matched']}/{w['total_chunks']})")
            print(f"    {w['issue']}")
            print(f"    → {w['recommendation']}")


if __name__ == '__main__':
    main()
```

### 7.2 `calculate_subagent_allocation.py`

```python
#!/usr/bin/env python3
"""Calculate subagent allocation from synthesis routing.

Gap G2: Implements Level 7 token budget calculation.

Usage:
    python calculate_subagent_allocation.py <project_path>

Output:
    {project_path}/02-resources/_subagent_plan.yaml
"""

import yaml
from pathlib import Path
from typing import Dict, List, Any
import sys
from dataclasses import dataclass


@dataclass
class BatchAllocation:
    """A batch of chunks for one subagent."""
    batch_id: str
    field: str
    chunks: List[Dict]
    total_tokens: int


def load_yaml_file(file_path: Path) -> dict:
    """Load YAML file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f) or {}


def calculate_allocation(project_path: Path, token_budget: int = 70000) -> dict:
    """Calculate subagent allocation using greedy bin-packing.

    Args:
        project_path: Path to project
        token_budget: Max tokens per subagent batch (default 70k)

    Returns:
        Allocation plan with batches and Level 7 budget
    """
    routing_path = project_path / '02-resources' / '_synthesis_routing.yaml'

    if not routing_path.exists():
        raise FileNotFoundError(f"Run build_synthesis_routing.py first: {routing_path}")

    routing = load_yaml_file(routing_path)

    batches: List[BatchAllocation] = []

    # Greedy bin-packing per field
    for field_name, chunks in routing.get('routing', {}).items():
        if not chunks:
            continue

        current_batch_chunks = []
        current_tokens = 0
        batch_num = 1

        for chunk in chunks:
            chunk_tokens = chunk.get('token_count', 0)

            # If adding this chunk exceeds budget, start new batch
            if current_tokens + chunk_tokens > token_budget and current_batch_chunks:
                batches.append(BatchAllocation(
                    batch_id=f"{field_name}_{batch_num}",
                    field=field_name,
                    chunks=current_batch_chunks,
                    total_tokens=current_tokens
                ))
                current_batch_chunks = []
                current_tokens = 0
                batch_num += 1

            current_batch_chunks.append(chunk)
            current_tokens += chunk_tokens

        # Don't forget last batch
        if current_batch_chunks:
            batches.append(BatchAllocation(
                batch_id=f"{field_name}_{batch_num}",
                field=field_name,
                chunks=current_batch_chunks,
                total_tokens=current_tokens
            ))

    # Calculate Level 7 budget
    level7_budget = calculate_level7_budget(project_path, batches)

    return {
        'project': str(project_path),
        'token_budget_per_batch': token_budget,
        'total_batches': len(batches),
        'batches': [
            {
                'batch_id': b.batch_id,
                'field': b.field,
                'chunks': b.chunks,
                'total_tokens': b.total_tokens
            }
            for b in batches
        ],
        'level7_budget': level7_budget
    }


def calculate_level7_budget(project_path: Path, batches: List[BatchAllocation]) -> dict:
    """Calculate token budget for Level 7 final report subagent.

    Gap G2: Level 7 needs explicit budget calculation.
    """
    # Estimate synthesis file sizes (each field produces ~2k-5k tokens)
    unique_fields = set(b.field for b in batches)
    estimated_synthesis_tokens = len(unique_fields) * 3500  # Conservative estimate

    budget = {
        'methodology': 3000,
        'briefing': 2000,
        'synthesis_files_estimated': estimated_synthesis_tokens,
        'output_reservation': 20000,
        'total_available': 100000,
        'usable': 100000 - 3000 - 2000 - 20000 - estimated_synthesis_tokens
    }

    if budget['usable'] < 10000:
        budget['requires_split'] = True
        budget['split_strategy'] = 'group_by_priority'
        budget['note'] = 'Synthesis files exceed budget. Will process high-priority fields first.'
    else:
        budget['requires_split'] = False

    return budget


def main():
    if len(sys.argv) < 2:
        print("Usage: calculate_subagent_allocation.py <project_path>")
        print("Example: python calculate_subagent_allocation.py 02-projects/02-ontologies-research")
        sys.exit(1)

    project_path = Path(sys.argv[1])

    if not project_path.exists():
        print(f"Error: Project path not found: {project_path}")
        sys.exit(1)

    print(f"Calculating subagent allocation for: {project_path}")
    result = calculate_allocation(project_path)

    # Write allocation plan
    output_path = project_path / '02-resources' / '_subagent_plan.yaml'
    with open(output_path, 'w', encoding='utf-8') as f:
        yaml.dump(result, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    # Report results
    print(f"\n✓ Allocation plan written to: {output_path}")
    print(f"  Total batches: {result['total_batches']}")
    print(f"  Token budget per batch: {result['token_budget_per_batch']:,}")

    # Group by field
    field_batches = {}
    for b in result['batches']:
        field_batches.setdefault(b['field'], []).append(b)

    print("\n  Batches per field:")
    for field, batches in field_batches.items():
        total_chunks = sum(len(b['chunks']) for b in batches)
        print(f"    {field}: {len(batches)} batch(es), {total_chunks} chunks")

    # Level 7 budget
    l7 = result['level7_budget']
    print(f"\n  Level 7 Budget:")
    print(f"    Usable tokens: {l7['usable']:,}")
    if l7.get('requires_split'):
        print(f"    ⚠️ {l7['note']}")


if __name__ == '__main__':
    main()
```

---

### 7.3 `generate_subagent_prompts.py`

```python
#!/usr/bin/env python3
"""Generate subagent prompts from allocation plan.

Gaps G13, G22a, G22b: Includes INPUT CONTRACT, research_purpose, synthesis_goals.

Usage:
    python generate_subagent_prompts.py <project_path>

Output:
    {project_path}/03-working/prompts/_prompt_{batch_id}.md
"""

import yaml
from pathlib import Path
from typing import Dict, List
import sys
from datetime import datetime


def load_yaml_file(file_path: Path) -> dict:
    """Load YAML file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f) or {}


def load_yaml_frontmatter(file_path: Path) -> dict:
    """Load YAML frontmatter from markdown file."""
    content = file_path.read_text(encoding='utf-8')
    if content.startswith('---'):
        end = content.find('---', 3)
        if end > 0:
            return yaml.safe_load(content[3:end]) or {}
    return {}


def extract_body_section(file_path: Path, section_header: str) -> str:
    """Extract a section from markdown body."""
    content = file_path.read_text(encoding='utf-8')

    # Skip frontmatter
    if content.startswith('---'):
        end = content.find('---', 3)
        if end > 0:
            content = content[end+3:]

    # Find section
    lines = content.split('\n')
    in_section = False
    section_lines = []

    for line in lines:
        if line.startswith('## ') and section_header in line:
            in_section = True
            continue
        elif line.startswith('## ') and in_section:
            break
        elif in_section:
            section_lines.append(line)

    return '\n'.join(section_lines).strip()


INPUT_CONTRACT_TEMPLATE = """
## INPUT CONTRACT (STRICT)

### Files You MUST Read (in this order)
1. `03-skills/research-pipeline/shared/paper-analyze-core/SKILL.md` (methodology)
{chunk_list}

### Files You MUST NOT Read
- ANY `.pdf` file
- ANY folder except the paper folders listed above
- ANY file in `04-outputs/`
- ANY file starting with `.` (hidden files)
- ANY file outside project directory

### Directory Traversal FORBIDDEN
- Do NOT use `../` paths
- Do NOT follow symbolic links
- Stay within `{project_path}/` boundary

VIOLATION = Synthesis fails validation.
"""

PROMPT_TEMPLATE = """---
batch_id: "{batch_id}"
field: "{field}"
generated_at: "{timestamp}"
chunks_count: {chunks_count}
total_tokens: {total_tokens}
---

# Batch Extraction: {field} (Batch {batch_num})

## Research Context

**Research Question**: {research_question}

**Research Purpose**: {research_purpose}

**Synthesis Goals**:
{synthesis_goals}

## Your Assignment

Extract patterns for field: **{field}**

Field description: {field_description}

{input_contract}

## Chunks to Read (FULL CONTENT - DO NOT SKIM)

{chunk_files}

## Output Schema

Write to: `{project_path}/03-working/_batch_{batch_id}.md`

```yaml
---
batch_id: "{batch_id}"
field: "{field}"
papers_read: [list of paper_ids actually read]
chunks_read: {chunks_count}
patterns_found: {{count}}
extracted_at: "{timestamp}"
---
```

## Pattern Format

For EACH pattern you find:

```markdown
### Pattern: {{pattern_name}}

- **Source**: Paper-ID (Chunk N:Line-Line)
- **Description**: {{full detail from chunk}}
- **Quote**: "{{exact text from chunk}}"
- **Context**: {{surrounding information}}
```

## CRITICAL REQUIREMENTS

1. Read EACH chunk file completely - do not skim
2. Include exact quotes with line numbers
3. Preserve citation format: Paper-ID (Chunk N:Line-Line)
4. Do NOT summarize - include full detail
5. Do NOT skip any relevant patterns
"""


def generate_prompts(project_path: Path) -> int:
    """Generate prompt files for all batches.

    Returns:
        Number of prompts generated
    """
    allocation_path = project_path / '02-resources' / '_subagent_plan.yaml'
    briefing_path = project_path / '02-resources' / '_briefing.md'
    kit_path = project_path / '02-resources' / '_analysis_kit.md'

    if not allocation_path.exists():
        raise FileNotFoundError(f"Run calculate_subagent_allocation.py first: {allocation_path}")

    allocation = load_yaml_file(allocation_path)
    briefing = load_yaml_frontmatter(briefing_path)

    # Extract research_purpose (G22a)
    research_purpose = briefing.get('research_purpose', 'Not specified')
    research_question = briefing.get('research_question', 'Not specified')

    # Build field descriptions
    field_descriptions = {}
    for field in briefing.get('extraction_schema', []):
        field_descriptions[field['field']] = field.get('description', '')

    # Extract synthesis_goals (G22b) from _analysis_kit.md body
    synthesis_goals = "Not specified"
    if kit_path.exists():
        synthesis_goals = extract_body_section(kit_path, "Synthesis Goals")
        if not synthesis_goals:
            synthesis_goals = "Not specified"

    # Create prompts directory
    prompts_dir = project_path / '03-working' / 'prompts'
    prompts_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().isoformat()

    for batch in allocation.get('batches', []):
        batch_id = batch['batch_id']
        field = batch['field']
        chunks = batch['chunks']

        # Build chunk file list
        chunk_files = []
        for chunk in chunks:
            paper_id = chunk['paper_id']
            chunk_num = chunk['chunk']
            chunk_files.append(f"- `{project_path}/02-resources/papers/{paper_id}/{paper_id}_{chunk_num}.md`")

        # Build INPUT CONTRACT (G13)
        chunk_list_for_contract = '\n'.join([f"2. `{c}`" for i, c in enumerate(chunk_files, 2)])
        input_contract = INPUT_CONTRACT_TEMPLATE.format(
            chunk_list=chunk_list_for_contract,
            project_path=project_path
        )

        # Extract batch number from batch_id
        batch_num = batch_id.split('_')[-1] if '_' in batch_id else '1'

        prompt = PROMPT_TEMPLATE.format(
            batch_id=batch_id,
            field=field,
            timestamp=timestamp,
            chunks_count=len(chunks),
            total_tokens=batch['total_tokens'],
            batch_num=batch_num,
            research_question=research_question,
            research_purpose=research_purpose,
            synthesis_goals=synthesis_goals,
            field_description=field_descriptions.get(field, ''),
            input_contract=input_contract,
            chunk_files='\n'.join(chunk_files),
            project_path=project_path
        )

        # Write prompt file
        prompt_path = prompts_dir / f"_prompt_{batch_id}.md"
        prompt_path.write_text(prompt, encoding='utf-8')

    return len(allocation.get('batches', []))


def main():
    if len(sys.argv) < 2:
        print("Usage: generate_subagent_prompts.py <project_path>")
        print("Example: python generate_subagent_prompts.py 02-projects/02-ontologies-research")
        sys.exit(1)

    project_path = Path(sys.argv[1])

    if not project_path.exists():
        print(f"Error: Project path not found: {project_path}")
        sys.exit(1)

    print(f"Generating subagent prompts for: {project_path}")
    count = generate_prompts(project_path)

    print(f"\n✓ Generated {count} prompt files")
    print(f"  Location: {project_path}/03-working/prompts/")
    print("\n  Review 2-3 prompts before executing synthesis.")


if __name__ == '__main__':
    main()
```

---

### 7.4 `verify_subagent_output.py`

```python
#!/usr/bin/env python3
"""Verify subagent batch outputs.

Gap G15: Implements quote-line verification.

Usage:
    python verify_subagent_output.py <project_path>

Output:
    {project_path}/02-resources/_verification_report.yaml
"""

import yaml
import hashlib
import re
from pathlib import Path
from typing import Dict, List, Tuple
import sys


def load_yaml_file(file_path: Path) -> dict:
    """Load YAML file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f) or {}


def load_yaml_frontmatter(file_path: Path) -> dict:
    """Load YAML frontmatter from markdown file."""
    content = file_path.read_text(encoding='utf-8')
    if content.startswith('---'):
        end = content.find('---', 3)
        if end > 0:
            return yaml.safe_load(content[3:end]) or {}
    return {}


def verify_quote_at_line(paper_path: Path, chunk: int, lines: str, quote: str) -> Tuple[bool, str]:
    """Verify that quote exists at specified line range.

    Gap G15: Quote-line verification.

    Returns:
        (success, message)
    """
    # Parse paper_id from path
    paper_id = paper_path.name
    chunk_file = paper_path / f"{paper_id}_{chunk}.md"

    if not chunk_file.exists():
        return False, f"Chunk file not found: {chunk_file}"

    try:
        content_lines = chunk_file.read_text(encoding='utf-8').split('\n')

        # Parse line range
        if '-' in lines:
            start, end = map(int, lines.split('-'))
        else:
            start = end = int(lines)

        # Extract cited lines (1-indexed to 0-indexed)
        if start < 1 or end > len(content_lines):
            return False, f"Line range {lines} out of bounds (file has {len(content_lines)} lines)"

        cited_text = '\n'.join(content_lines[start-1:end])

        # Check if quote appears (fuzzy match, first 50 chars)
        quote_start = quote[:50].strip() if quote else ""
        if quote_start and quote_start in cited_text:
            return True, "Quote verified"
        else:
            return False, f"Quote not found at lines {lines}"

    except Exception as e:
        return False, f"Error reading chunk: {e}"


def parse_patterns_from_batch(batch_path: Path) -> List[Dict]:
    """Parse patterns from batch markdown file."""
    content = batch_path.read_text(encoding='utf-8')
    patterns = []

    # Find all pattern sections
    pattern_regex = r'### Pattern: (.+?)\n(.*?)(?=### Pattern:|$)'
    matches = re.findall(pattern_regex, content, re.DOTALL)

    for name, body in matches:
        pattern = {'name': name.strip()}

        # Extract source
        source_match = re.search(r'\*\*Source\*\*:\s*(.+)', body)
        if source_match:
            source = source_match.group(1).strip()
            # Parse: Paper-ID (Chunk N:Line-Line)
            cite_match = re.search(r'(.+?)\s*\(Chunk\s*(\d+):(\d+-\d+)\)', source)
            if cite_match:
                pattern['paper_id'] = cite_match.group(1).strip()
                pattern['chunk'] = int(cite_match.group(2))
                pattern['lines'] = cite_match.group(3)

        # Extract quote
        quote_match = re.search(r'\*\*Quote\*\*:\s*"(.+?)"', body, re.DOTALL)
        if quote_match:
            pattern['quote'] = quote_match.group(1).strip()

        patterns.append(pattern)

    return patterns


def verify_batch(batch_path: Path, project_path: Path, allocation: dict) -> Dict:
    """Verify a single batch file."""
    frontmatter = load_yaml_frontmatter(batch_path)

    result = {
        'batch_id': frontmatter.get('batch_id', batch_path.stem),
        'field': frontmatter.get('field', 'unknown'),
        'chunks_read': frontmatter.get('chunks_read', 0),
        'patterns_found': frontmatter.get('patterns_found', 0),
        'verification_passed': True,
        'issues': [],
        'quote_checks': []
    }

    # Find expected chunks from allocation
    expected_chunks = 0
    for batch in allocation.get('batches', []):
        if batch['batch_id'] == result['batch_id']:
            expected_chunks = len(batch['chunks'])
            break

    # Check chunks_read matches expected
    if result['chunks_read'] != expected_chunks:
        result['issues'].append(f"Chunks mismatch: read {result['chunks_read']}, expected {expected_chunks}")
        result['verification_passed'] = False

    # Parse and verify patterns
    patterns = parse_patterns_from_batch(batch_path)

    # Spot-check first 3 patterns per field
    papers_path = project_path / '02-resources' / 'papers'
    for pattern in patterns[:3]:
        if 'paper_id' not in pattern or 'chunk' not in pattern:
            continue

        paper_path = papers_path / pattern['paper_id']
        if not paper_path.exists():
            # Try to find by partial match
            matches = list(papers_path.glob(f"*{pattern['paper_id']}*"))
            if matches:
                paper_path = matches[0]
            else:
                result['quote_checks'].append({
                    'pattern': pattern.get('name', 'unknown'),
                    'passed': False,
                    'message': f"Paper folder not found: {pattern['paper_id']}"
                })
                continue

        success, message = verify_quote_at_line(
            paper_path,
            pattern.get('chunk', 0),
            pattern.get('lines', '1-1'),
            pattern.get('quote', '')
        )

        result['quote_checks'].append({
            'pattern': pattern.get('name', 'unknown'),
            'passed': success,
            'message': message
        })

    # Calculate quote verification rate
    if result['quote_checks']:
        passed = sum(1 for c in result['quote_checks'] if c['passed'])
        result['quote_verification_rate'] = passed / len(result['quote_checks'])
        if result['quote_verification_rate'] < 0.7:
            result['issues'].append(f"Quote verification rate {result['quote_verification_rate']:.0%} < 70% threshold")
            result['verification_passed'] = False

    return result


def verify_all_batches(project_path: Path) -> dict:
    """Verify all batch files in project."""
    allocation_path = project_path / '02-resources' / '_subagent_plan.yaml'
    working_dir = project_path / '03-working'

    if not allocation_path.exists():
        raise FileNotFoundError(f"Allocation plan not found: {allocation_path}")

    allocation = load_yaml_file(allocation_path)

    # Find all batch files
    batch_files = list(working_dir.glob('_batch_*.md'))

    results = {
        'project': str(project_path),
        'verified_at': str(Path.cwd()),
        'total_batches_expected': len(allocation.get('batches', [])),
        'total_batches_found': len(batch_files),
        'all_passed': True,
        'batches': []
    }

    for batch_file in batch_files:
        batch_result = verify_batch(batch_file, project_path, allocation)
        results['batches'].append(batch_result)
        if not batch_result['verification_passed']:
            results['all_passed'] = False

    return results


def main():
    if len(sys.argv) < 2:
        print("Usage: verify_subagent_output.py <project_path>")
        print("Example: python verify_subagent_output.py 02-projects/02-ontologies-research")
        sys.exit(1)

    project_path = Path(sys.argv[1])

    if not project_path.exists():
        print(f"Error: Project path not found: {project_path}")
        sys.exit(1)

    print(f"Verifying subagent outputs for: {project_path}")
    results = verify_all_batches(project_path)

    # Write verification report
    output_path = project_path / '02-resources' / '_verification_report.yaml'
    with open(output_path, 'w', encoding='utf-8') as f:
        yaml.dump(results, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    # Report results
    print(f"\n{'✓' if results['all_passed'] else '✗'} Verification {'PASSED' if results['all_passed'] else 'FAILED'}")
    print(f"  Batches found: {results['total_batches_found']}/{results['total_batches_expected']}")
    print(f"  Report: {output_path}")

    if not results['all_passed']:
        print("\n  Failed batches:")
        for batch in results['batches']:
            if not batch['verification_passed']:
                print(f"    - {batch['batch_id']}: {', '.join(batch['issues'])}")
        sys.exit(1)


if __name__ == '__main__':
    main()
```

---

### 7.5 `aggregate_patterns.py`

```python
#!/usr/bin/env python3
"""Aggregate patterns from batch files into field synthesis.

Usage:
    python aggregate_patterns.py <project_path> [field]

Output:
    {project_path}/04-outputs/_synthesis_{field}.yaml (per field)
    or all fields if no field specified
"""

import yaml
import re
from pathlib import Path
from typing import Dict, List, Set
import sys
from datetime import datetime
from collections import defaultdict


def load_yaml_frontmatter(file_path: Path) -> dict:
    """Load YAML frontmatter from markdown file."""
    content = file_path.read_text(encoding='utf-8')
    if content.startswith('---'):
        end = content.find('---', 3)
        if end > 0:
            return yaml.safe_load(content[3:end]) or {}
    return {}


def parse_patterns_from_batch(batch_path: Path) -> List[Dict]:
    """Parse patterns from batch markdown file."""
    content = batch_path.read_text(encoding='utf-8')
    frontmatter = load_yaml_frontmatter(batch_path)
    patterns = []

    # Find all pattern sections
    pattern_regex = r'### Pattern: (.+?)\n(.*?)(?=### Pattern:|$)'
    matches = re.findall(pattern_regex, content, re.DOTALL)

    for name, body in matches:
        pattern = {
            'name': name.strip(),
            'sources': [],
            'description': '',
            'quotes': []
        }

        # Extract source
        source_match = re.search(r'\*\*Source\*\*:\s*(.+)', body)
        if source_match:
            source_text = source_match.group(1).strip()
            # Parse: Paper-ID (Chunk N:Line-Line)
            cite_match = re.search(r'(.+?)\s*\(Chunk\s*(\d+):(\d+-\d+)\)', source_text)
            if cite_match:
                pattern['sources'].append({
                    'paper_id': cite_match.group(1).strip(),
                    'chunk': int(cite_match.group(2)),
                    'lines': cite_match.group(3)
                })

        # Extract description
        desc_match = re.search(r'\*\*Description\*\*:\s*(.+?)(?=\*\*|$)', body, re.DOTALL)
        if desc_match:
            pattern['description'] = desc_match.group(1).strip()

        # Extract quote
        quote_match = re.search(r'\*\*Quote\*\*:\s*"(.+?)"', body, re.DOTALL)
        if quote_match:
            pattern['quotes'].append(quote_match.group(1).strip())

        patterns.append(pattern)

    return patterns


def normalize_pattern_name(name: str) -> str:
    """Normalize pattern name for deduplication (case-insensitive, strip whitespace)."""
    return name.lower().strip()


def merge_patterns(patterns: List[Dict]) -> List[Dict]:
    """Merge patterns by name, combining sources.

    Deduplication rules:
    - Case-insensitive name matching
    - Merge sources from all occurrences
    - Keep longest description
    - Combine all unique quotes
    """
    merged: Dict[str, Dict] = {}

    for pattern in patterns:
        key = normalize_pattern_name(pattern['name'])

        if key not in merged:
            merged[key] = {
                'name': pattern['name'],  # Keep original casing from first occurrence
                'sources': [],
                'description': pattern['description'],
                'quotes': []
            }

        # Merge sources
        for source in pattern.get('sources', []):
            # Check for duplicate source (same paper, chunk, lines)
            is_dup = any(
                s['paper_id'] == source['paper_id'] and
                s['chunk'] == source['chunk'] and
                s['lines'] == source['lines']
                for s in merged[key]['sources']
            )
            if not is_dup:
                merged[key]['sources'].append(source)

        # Keep longest description
        if len(pattern.get('description', '')) > len(merged[key]['description']):
            merged[key]['description'] = pattern['description']

        # Merge unique quotes
        for quote in pattern.get('quotes', []):
            if quote and quote not in merged[key]['quotes']:
                merged[key]['quotes'].append(quote)

    return list(merged.values())


def aggregate_field(project_path: Path, field: str) -> dict:
    """Aggregate all batch files for a single field."""
    working_dir = project_path / '03-working'

    # Find all batch files for this field
    batch_files = list(working_dir.glob(f'_batch_{field}_*.md'))

    if not batch_files:
        return {
            'field': field,
            'batches_found': 0,
            'patterns': [],
            'error': f"No batch files found for field: {field}"
        }

    # Collect all patterns from all batches
    all_patterns = []
    papers_seen: Set[str] = set()

    for batch_file in batch_files:
        patterns = parse_patterns_from_batch(batch_file)
        all_patterns.extend(patterns)

        # Track papers
        for p in patterns:
            for s in p.get('sources', []):
                papers_seen.add(s['paper_id'])

    # Merge patterns
    merged_patterns = merge_patterns(all_patterns)

    return {
        'field': field,
        'aggregated_at': datetime.now().isoformat(),
        'batches_merged': len(batch_files),
        'papers_included': sorted(papers_seen),
        'patterns_before_merge': len(all_patterns),
        'patterns_after_merge': len(merged_patterns),
        'patterns': merged_patterns
    }


def aggregate_all_fields(project_path: Path) -> List[str]:
    """Aggregate all fields found in batch files."""
    working_dir = project_path / '03-working'
    outputs_dir = project_path / '04-outputs'
    outputs_dir.mkdir(exist_ok=True)

    # Find all unique fields from batch files
    batch_files = list(working_dir.glob('_batch_*.md'))
    fields: Set[str] = set()

    for batch_file in batch_files:
        # Parse field from filename: _batch_{field}_{N}.md
        parts = batch_file.stem.split('_')
        if len(parts) >= 3:
            # Handle field names with underscores by taking everything except last part
            field = '_'.join(parts[2:-1]) if len(parts) > 3 else parts[2]
            fields.add(field)

    aggregated_fields = []
    for field in sorted(fields):
        result = aggregate_field(project_path, field)

        # Write synthesis file
        output_path = outputs_dir / f'_synthesis_{field}.yaml'
        with open(output_path, 'w', encoding='utf-8') as f:
            yaml.dump(result, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

        aggregated_fields.append(field)
        print(f"  {field}: {result['patterns_before_merge']} → {result['patterns_after_merge']} patterns")

    return aggregated_fields


def main():
    if len(sys.argv) < 2:
        print("Usage: aggregate_patterns.py <project_path> [field]")
        print("Example: python aggregate_patterns.py 02-projects/02-ontologies-research")
        print("Example: python aggregate_patterns.py 02-projects/02-ontologies-research entity_types")
        sys.exit(1)

    project_path = Path(sys.argv[1])
    field = sys.argv[2] if len(sys.argv) > 2 else None

    if not project_path.exists():
        print(f"Error: Project path not found: {project_path}")
        sys.exit(1)

    outputs_dir = project_path / '04-outputs'
    outputs_dir.mkdir(exist_ok=True)

    if field:
        # Aggregate single field
        print(f"Aggregating patterns for field: {field}")
        result = aggregate_field(project_path, field)

        output_path = outputs_dir / f'_synthesis_{field}.yaml'
        with open(output_path, 'w', encoding='utf-8') as f:
            yaml.dump(result, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

        print(f"\n✓ Aggregated {result['patterns_before_merge']} → {result['patterns_after_merge']} patterns")
        print(f"  Output: {output_path}")
    else:
        # Aggregate all fields
        print(f"Aggregating all fields for: {project_path}")
        fields = aggregate_all_fields(project_path)

        print(f"\n✓ Aggregated {len(fields)} fields")
        print(f"  Output: {outputs_dir}/_synthesis_*.yaml")


if __name__ == '__main__':
    main()
```

---

## Teil 8: File Change Summary

| File | Section | Type | Description | Gap |
|------|---------|------|-------------|-----|
| `create-research-project/SKILL.md` | Step 2 | MODIFY | AI field generation + research_purpose prompt | G5, G22a |
| `paper-analyze-core/SKILL.md` | Step 1b | ADD | Field calibration specification | G1 |
| `paper-analyze-core/SKILL.md` | Step 3 | MODIFY | 3-state forced field assessment | - |
| `paper-analyze-core/SKILL.md` | Token Budget | MODIFY | Standardize formula to `chars // 4` | G3 |
| `paper-analyze-core/SKILL.md` | N/A Format | ADD | Structured N/A format | G18 |
| `create-research-project/references/analysis_kit_template.md` | Synthesis Goals | ADD | Goal section for subagent context | G22b |
| `analyze-research-project/SKILL.md` | Step 2 | ADD | INPUT CONTRACT for subagents | G13 |
| `analyze-research-project/SKILL.md` | Errors | ADD | Partial save on timeout | G16 |
| `synthesize-research-project/SKILL.md` | ALL | REWRITE | 7-level architecture with budgets | G2 |
| `validation/build_synthesis_routing.py` | - | CREATE | Boolean routing + sparsity check | G19 |
| `validation/calculate_subagent_allocation.py` | - | CREATE | Token batching + L7 budget | G2 |
| `validation/generate_subagent_prompts.py` | - | CREATE | Prompt gen + INPUT CONTRACT + context | G13, G22a, G22b |
| `validation/verify_subagent_output.py` | - | CREATE | Hash + quote-line verification | G15 |
| `validation/aggregate_patterns.py` | - | CREATE | Pattern merge script | - |
| `validation/validate_analysis.py` | Rule 8 | MODIFY | Add quote-line verification | G15 |

---

## Teil 9: Reference Files

### Files to READ Before Implementation

| Purpose | File Path | Relevant Lines |
|---------|-----------|----------------|
| Token budget example | `paper-analyze-core/SKILL.md` | 464-489 |
| Analysis log schema | `paper-analyze-core/references/analysis_log_template.md` | ALL |
| Extraction guide template | `paper-analyze-core/references/extraction_guide_template.md` | ALL |
| Token config source | `00-system/core/nexus/config.py` | 15 |
| Existing validation | `validation/validate_analysis.py` | ALL |
| Existing synthesis validation | `validation/validate_synthesis.py` | ALL |
| Verification protocol | `analyze-research-project/SKILL.md` | 572-583 |
| Retry implementation | `paper-search/scripts/paper_download.py` | 51 |

### Example Projects

| Project | Path | Use For |
|---------|------|---------|
| Ontologies Research | `02-projects/02-ontologies-research/` | Migration test |
| Current _briefing.md | `02-projects/02-ontologies-research/02-resources/_briefing.md` | Schema reference |
| Current _analysis_kit.md | `02-projects/02-ontologies-research/02-resources/_analysis_kit.md` | Kit reference |
| Example index.md | `02-projects/02-ontologies-research/02-resources/papers/05-DOLCE.../index.md` | Before/after |

---

## Teil 10: Resolved Questions

| Question | Decision | Rationale |
|----------|----------|-----------|
| Field generation | AI generates, user confirms | Reduces manual work, maintains control |
| Chunk assessment | 3-state: true/partial/false | Partial enables secondary matching |
| Migration strategy | Clean Break (re-analyze) | No legacy code complexity |
| Max chunk size | 500 lines | Within token budget |
| Token budget L4 | 70k per subagent | Proven in 21 papers |
| Token budget L7 | Dynamic, split if >75k | Handles large projects |
| Level 6 | Script, not Subagent | Deterministic aggregation |
| Token formula | `chars // 4` | Aligned with core config |
| File constraints | Explicit INPUT CONTRACT | Prevents scope creep |
| Research context | research_purpose + synthesis_goals | Validated G22a/G22b |
| Chunk summaries | Use existing body format | G20 rejected as redundant |
| Generic schema | Keep `fields_found` | G21 rejected as premature |
| Schema version | v2.3 | Bump for chunk_index + fields_found additions |

---

*Plan Version: 3.3 (2025-12-28)*
*Validated by: 13 parallel codebase exploration agents + 6 final validation agents*
*Active Gaps: 11 (5 critical, 6 high)*
*Rejected Proposals: 4 (G20, G21, G22c, G22d)*
*Status: APPROVED FOR IMPLEMENTATION*
*Schema Version: v2.3 (new)*
*Scripts: 5/5 fully specified*
