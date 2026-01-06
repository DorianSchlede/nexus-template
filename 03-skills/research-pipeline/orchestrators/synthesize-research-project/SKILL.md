---
name: synthesize-research-project
description: "Synthesize analyzed research papers into comprehensive reports (Phase 3). Load when user says 'synthesize research project', 'generate synthesis', 'create synthesis report', or wants cross-paper synthesis. Expects analyzed papers with index.md from analyze-research-project."
resume_instructions: |
  ## Context Checkpoint: _resume.md

  This skill requires maintaining a `_resume.md` file for context recovery.

  **Location**: `{project_path}/_resume.md`

  **Maintenance Rules**:
  1. UPDATE `_resume.md` when context usage reaches ~60% (before compaction risk)
  2. UPDATE after completing each level of synthesis
  3. UPDATE after each batch of extraction subagents completes
  4. RELOAD `_resume.md` immediately after any context summary/compaction

  **_resume.md Format**:
  ```yaml
  ---
  updated: "{timestamp}"
  phase: "routing|extraction|aggregation|report|validation|complete"
  project_id: "{project_id}"
  ---

  # Resume Context

  ## Current State
  - Level: {1|2|3|4}
  - Fields processed: {N}/{total}
  - Batches complete: {N}/{total}

  ## Pending Work
  - Fields remaining: [list]
  - Current field: {field_name}
  - Batches pending: [list]

  ## Completed Work
  - Fields synthesized: [list]
  - Batch files: [list]
  - Report sections: [list]

  ## Next Actions
  1. {immediate next step}
  2. {following step}
  ```

  **On Resume After Compaction**:
  1. Read `{project_path}/_resume.md` first
  2. Read `02-resources/_synthesis_routing.yaml` for routing
  3. Check which `03-working/_batch_*.md` files exist
  4. Check which `04-outputs/_synthesis_*.md` files exist
  5. Continue from `## Next Actions`
---

# Synthesize Research Project (Phase 3: Cross-Paper Synthesis)

Generate comprehensive cross-paper synthesis reports from analyzed papers. **This skill expects analyzed papers with index.md files** - use `analyze-research-project` first.

---

## THE 3-SKILL CHAIN

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
| "synthesize research project {name}" | Yes |
| "generate synthesis for {project}" | Yes |
| "create synthesis report" | Yes |
| "cross-paper synthesis" | Yes |
| "analyze research project" | No → use `analyze-research-project` |
| "create research project" | No → use `create-research-project` |

---

## Prerequisites

Before using this skill, verify:
- [x] Research project exists in `02-projects/`
- [x] `02-resources/_briefing.md` exists (extraction schema)
- [x] Multiple papers have `index.md` (analysis complete)
- [x] Papers have YAML frontmatter with extracted fields

**Step 1 validates all prerequisites.** If any missing, execution stops with clear error.

---

## Core Principle

**AI reads ALL chunk details. No shortcuts. Full citations preserved through every level.**

---

## Architecture: 7-Level Hierarchical Synthesis (Gap G2 Fix)

```
LEVEL 1: ROUTING (Script)
├── Input: All index.md (chunk_index.fields_found) + _briefing.md
├── Script: build_synthesis_routing.py (NEW)
├── Algorithm: Boolean lookup - if chunk.fields_found[field] in [true, partial] → include
├── **Sparsity Check (Gap G19)**: Warn if field matches >80% of chunks
└── Output: 02-resources/_synthesis_routing.yaml

LEVEL 2: ALLOCATION (Script)
├── Input: _synthesis_routing.yaml
├── Script: calculate_subagent_allocation.py (NEW)
├── Algorithm: Greedy bin-packing with 70k token budget per batch
├── **Level 7 Budget**: Calculate dynamically, split if >75k input
└── Output: 02-resources/_subagent_plan.yaml

LEVEL 3: PROMPT GENERATION (Script)
├── Input: _subagent_plan.yaml + _briefing.md
├── Script: generate_subagent_prompts.py (NEW)
├── **Includes INPUT CONTRACT** (Gap G13)
├── **Includes research_purpose** (G22a)
├── **Includes synthesis_goals** (G22b)
└── Output: 03-working/prompts/_prompt_{batch_id}.md

LEVEL 4: EXTRACTION (Subagents - parallel, max 15 concurrent)
├── Input: _prompt_{batch_id}.md (Subagent reads ONLY files listed in prompt)
├── Subagent extracts patterns from chunks with chunk:line citations
├── Includes QUOTES, context, full detail
└── Output: 03-working/_batch_{field}_{N}.md (YAML patterns[])

LEVEL 5: VERIFICATION (Script)
├── Input: _batch_*.md + _subagent_plan.yaml
├── Script: verify_subagent_output.py (NEW)
├── **Quote-Line Verification (Gap G15)**: Spot-check quotes exist at cited lines
└── Output: _verification_report.yaml

LEVEL 6: AGGREGATION (Script - NOT Subagent!)
├── Input: All _batch_{field}_*.md
├── Script: aggregate_patterns.py (NEW)
├── Algorithm: Merge patterns[], dedupe by name, merge sources
└── Output: 04-outputs/_synthesis_{field}.yaml

LEVEL 7: FINAL REPORT (Subagent) - **WITH TOKEN BUDGET (Gap G2)**
├── Input: All _synthesis_{field}.yaml + _briefing.md
├── **Token Budget**: See calculation below
├── Subagent: Narrative synthesis, cross-field insights
└── Output: 04-outputs/_synthesis_report.md
```

### LEVEL 7 TOKEN BUDGET (Gap G2 Fix)

**The final report subagent has a calculated budget, not unlimited context!**

```python
# calculate_subagent_allocation.py calculates this:
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

**Token Budget Table (Level 7):**

| Component | Tokens | Notes |
|-----------|--------|-------|
| Methodology | 3,000 | Fixed |
| _briefing.md | 2,000 | Fixed (+50 for research_purpose) |
| Synthesis files | Variable | Sum of all _synthesis_{field}.yaml |
| Output reservation | 20,000 | Final report |
| **Max synthesis input** | **75,000** | Before requiring split |

**If synthesis files exceed budget:**
1. Group fields by priority (high first, from _briefing.md)
2. Generate multiple Level 7 passes (each within budget)
3. Final merge pass combines all Level 7 outputs

---

## Citation Format (PRESERVED AT EVERY LEVEL)

```
Paper-ID (Chunk N:Line-Line)
Example: 16-KG-Agent (Chunk 1:240-259)
```

**CRITICAL**: Citations must pass through ALL 4 levels unchanged.

---

## Workflow Overview (7-Level Architecture)

```
synthesize-research-project (THIS SKILL)
        │
        ├─ PHASE A: VALIDATION
        │   ├─ Step 0: Initialize TodoWrite (tracking)
        │   └─ Step 1: Validate readiness (index.md files with chunk_index)
        │
        ├─ PHASE B: ROUTING (Script - Level 1)
        │   └─ Step 2: build_synthesis_routing.py
        │              → 02-resources/_synthesis_routing.yaml
        │
        ├─ PHASE C: ALLOCATION (Script - Level 2)
        │   └─ Step 3: calculate_subagent_allocation.py
        │              → 02-resources/_subagent_plan.yaml
        │
        ├─ PHASE D: PROMPT GENERATION (Script - Level 3)
        │   └─ Step 4: generate_subagent_prompts.py
        │              → 03-working/prompts/_prompt_{batch_id}.md
        │
        ├─ PHASE E: EXTRACTION (Subagents - Level 4)
        │   └─ Step 5: Spawn batch extraction subagents
        │              → 03-working/_batch_{field}_{N}.md
        │
        ├─ PHASE F: VERIFICATION (Script - Level 5)
        │   └─ Step 6: verify_subagent_output.py
        │              → 03-working/_verification_report.yaml
        │
        ├─ PHASE G: AGGREGATION (Script - Level 6)
        │   └─ Step 7: aggregate_patterns.py
        │              → 04-outputs/_synthesis_{field}.yaml
        │
        ├─ PHASE H: FINAL REPORT (Subagent - Level 7)
        │   └─ Step 8: Spawn final report subagent (with token budget)
        │              → 04-outputs/_synthesis_report.md
        │
        └─ PHASE I: COMPLETION
            └─ Step 9: Mark project COMPLETE
```

**Key Difference from 4-Level**: Levels 1-3, 5-6 are SCRIPTS (deterministic), only Levels 4 and 7 use subagents (LLM).

---

## Step 0: Initialize Task Tracking

**MANDATORY: Use TodoWrite at start of skill:**

```
TodoWrite with initial todos:
- [ ] Validate readiness (Step 1)
- [ ] Run build_synthesis_routing.py (Step 2 - Level 1)
- [ ] Run calculate_subagent_allocation.py (Step 3 - Level 2)
- [ ] Run generate_subagent_prompts.py (Step 4 - Level 3)
- [ ] Spawn batch extraction subagents (Step 5 - Level 4)
- [ ] Run verify_subagent_output.py (Step 6 - Level 5)
- [ ] Run aggregate_patterns.py (Step 7 - Level 6)
- [ ] Spawn final report subagent (Step 8 - Level 7)
- [ ] Mark project COMPLETE (Step 9)
```

**Update todos as each step completes.**

---

# PHASE A: VALIDATION

## Step 1: Validate Readiness

**Run interface validation script first (catches format mismatches):**

```bash
# RECOMMENDED: Run validation before synthesis
python 03-skills/research-pipeline/shared/contracts/validate_interface.py {project_path}
```

If validation fails, papers need re-analysis with the updated skill (which includes inline YAML template).

**Check prerequisites including chunk_index (required for 7-level routing):**

```python
project_path = "02-projects/NN-{slug}/"
papers_path = project_path / "02-resources/papers"

# Check briefing exists (with research_purpose - G22a)
if not exists(project_path / "02-resources/_briefing.md"):
    fail("Missing _briefing.md - research question not defined")

briefing = read(project_path / "02-resources/_briefing.md")
if 'research_purpose' not in briefing:
    warn("Missing research_purpose in _briefing.md (G22a) - subagents may lack context")

# Find papers with index.md that have chunk_index (Schema 2.3+)
papers_valid = []
papers_legacy = []
for folder in papers_path.iterdir():
    if folder.is_dir() and (folder / "index.md").exists():
        index = read(folder / "index.md")
        if 'chunk_index' in index.frontmatter:
            papers_valid.append(folder.name)
        else:
            papers_legacy.append(folder.name)

if len(papers_valid) < 3:
    if papers_legacy:
        fail(f"""
        Only {len(papers_valid)} papers have chunk_index (Schema 2.3+).
        {len(papers_legacy)} papers use legacy schema without chunk_index.

        Re-analyze legacy papers with: "analyze research project {name}"
        Legacy papers: {papers_legacy}
        """)
    else:
        fail(f"Only {len(papers_valid)} papers analyzed - need at least 3 for synthesis")

# Read briefing to get extraction fields
extraction_fields = briefing.extraction_schema
```

### Display Status

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RESEARCH PROJECT READY FOR 7-LEVEL SYNTHESIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Research Project: {name}
Research Question: "{RQ}"
Research Purpose: "{research_purpose}"

Papers with chunk_index: {N} (ready for routing)
Legacy papers:          {M} (need re-analysis)
Extraction fields:      {K} (from _briefing.md)

Proceeding with Level 1 (Routing)...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

# PHASE B: ROUTING (Script - Level 1)

## Step 2: Build Synthesis Routing Table

**Run script to build routing from chunk_index.fields_found:**

```bash
python 03-skills/research-pipeline/validation/scripts/build_synthesis_routing.py \
  {project_path} \
  --output 02-resources/_synthesis_routing.yaml
```

**What the script does (deterministic - no LLM):**
1. Reads all index.md files with chunk_index
2. For each field from _briefing.md:
   - Looks up `chunk_index[N].fields_found[field]`
   - If `true` or `partial` → add chunk to routing
3. **Sparsity Check (Gap G19)**: Warns if field matches >80% of chunks
4. Outputs routing table

**Output:** `02-resources/_synthesis_routing.yaml`

### Routing Table Structure (NEW - based on chunk_index)

```yaml
project: 02-projects/02-ontologies-research
generated_at: "2025-12-28T14:30:00"
algorithm: "boolean_lookup"  # Not full-text search

fields:
  entity_types:
    description: "Core entity types defined"
    priority: high
    sparsity_warning: false  # <80% match rate OK
    chunks:
      - paper_id: 02-Knowledge_Graphs
        chunk: 2
        fields_found_state: true  # From index.md
        token_count: 12500        # From index.md
      - paper_id: 02-Knowledge_Graphs
        chunk: 6
        fields_found_state: true
        token_count: 8200
      - paper_id: 05-DOLCE
        chunk: 1
        fields_found_state: partial  # Partial counts
        token_count: 15000

  ai_integration:
    priority: high
    sparsity_warning: true   # >80% match rate - warn user!
    chunks:
      - paper_id: 16-KG-Agent
        chunk: 1
        fields_found_state: true
        token_count: 10000

stats:
  papers_analyzed: 23
  total_chunks: 127
  chunks_per_field_avg: 34
```

### Display Routing (Level 1)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
LEVEL 1: SYNTHESIS ROUTING (from chunk_index)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Fields to synthesize: 15
Total chunks routed: 127

| Field | Chunks (true) | Chunks (partial) | Sparsity |
|-------|---------------|------------------|----------|
| entity_types | 28 | 6 | OK |
| ai_integration | 35 | 3 | ⚠️ 85% match |
| framework_comparison | 22 | 6 | OK |
...

⚠️ SPARSITY WARNING (Gap G19):
   ai_integration matches 85% of chunks.
   Consider splitting into sub-fields or removing generic field.

Proceeding with Level 2 (Allocation)...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

# PHASE C: ALLOCATION (Script - Level 2)

## Step 3: Calculate Subagent Allocation

**Run script to allocate chunks to subagent batches with token budget:**

```bash
python 03-skills/research-pipeline/validation/scripts/calculate_subagent_allocation.py \
  {project_path} \
  --input 02-resources/_synthesis_routing.yaml \
  --output 02-resources/_subagent_plan.yaml
```

**What the script does (deterministic - no LLM):**
1. Reads routing table with token counts per chunk
2. Uses greedy bin-packing to fit chunks into 70k token batches
3. Groups chunks by paper when possible (context preservation)
4. Calculates Level 7 budget (Gap G2)
5. Outputs subagent plan

**Output:** `02-resources/_subagent_plan.yaml`

### Subagent Plan Structure

```yaml
project: 02-projects/02-ontologies-research
generated_at: "2025-12-28T14:35:00"
token_budget_per_batch: 70000
standard_formula: "chars // 4"  # Gap G3

# Level 4 batches (extraction subagents)
level4_batches:
  - batch_id: "entity_types_1"
    field: entity_types
    chunks:
      - paper_id: 02-Knowledge_Graphs
        chunk: 2
        token_count: 12500
      - paper_id: 02-Knowledge_Graphs
        chunk: 6
        token_count: 8200
    total_tokens: 45700
    estimated_duration: "3 min"

  - batch_id: "entity_types_2"
    field: entity_types
    chunks:
      - paper_id: 05-DOLCE
        chunk: 1
        token_count: 15000
    total_tokens: 62000
    estimated_duration: "4 min"

# Level 7 budget calculation (Gap G2)
level7_budget:
  methodology: 3000
  briefing: 2050  # +50 for research_purpose
  synthesis_files_estimated: 45000
  output_reservation: 20000
  total_available: 100000
  usable: 29950
  requires_split: false
  split_strategy: null

stats:
  total_batches: 45
  max_concurrent: 15
  estimated_total_time: "25 min"
```

### Display Allocation (Level 2)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
LEVEL 2: SUBAGENT ALLOCATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Token budget per batch: 70,000
Batches calculated: 45

| Field | Batches | Avg Tokens/Batch |
|-------|---------|------------------|
| entity_types | 6 | 58,000 |
| ai_integration | 7 | 62,000 |
| framework_comparison | 5 | 55,000 |
...

Level 7 Budget Check:
  Synthesis files: ~45,000 tokens
  Usable: 29,950 tokens
  Status: ✓ No split required

Proceeding with Level 3 (Prompt Generation)...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

# PHASE D: PROMPT GENERATION (Script - Level 3)

## Step 4: Generate Subagent Prompts

**Run script to generate prompts with INPUT CONTRACT:**

```bash
python 03-skills/research-pipeline/validation/scripts/generate_subagent_prompts.py \
  {project_path} \
  --input 02-resources/_subagent_plan.yaml \
  --output-dir 03-working/prompts/
```

**What the script does (deterministic - no LLM):**
1. Reads subagent plan
2. Reads _briefing.md for research_purpose (G22a)
3. Reads _analysis_kit.md for synthesis_goals (G22b)
4. Generates INPUT CONTRACT per subagent (G13)
5. Outputs prompt files

**Output:** `03-working/prompts/_prompt_{batch_id}.md`

### Generated Prompt Template

```markdown
# Batch Extraction: {field_name} (Batch {N} of {total})

## INPUT CONTRACT (STRICT - Gap G13)

### Files You MUST Read (in this order)
1. `{project_path}/02-resources/_briefing.md`
2. `{paper_path}/{paper_id}_{chunk}.md`
[... exact list for this batch]

### Files You MUST NOT Read
- ANY `.pdf` file
- ANY other batch's chunks
- ANY file in 04-outputs/

VIOLATION = Extraction fails validation.

## CONTEXT (Gap G22a, G22b)
Research Purpose: {research_purpose}
Synthesis Goals: {synthesis_goals}

## EXTRACTION CONTRACT

For field "{field_name}":
1. Read EACH chunk completely
2. Extract patterns with:
   - name: Pattern name
   - chunk_ref: Paper-ID (Chunk N:Line-Line)
   - quote: "Exact text from chunk" (100-150 chars)
   - description: Full context

3. Write YAML output to: 03-working/_batch_{field}_{N}.yaml

```yaml
patterns:
  - name: "Pattern Name"
    chunk_ref: "Paper-ID (Chunk N:Line-Line)"
    quote: "Exact text proving pattern..."
    description: "Full context and detail"
```
```

### Display Prompts Generated (Level 3)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
LEVEL 3: PROMPT GENERATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Prompts generated: 45

Context included:
  ✓ INPUT CONTRACT (G13)
  ✓ research_purpose (G22a)
  ✓ synthesis_goals (G22b)

Prompts saved to: 03-working/prompts/

Proceeding with Level 4 (Extraction)...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

# PHASE E: EXTRACTION (Subagents - Level 4)

## Step 5: Spawn Batch Extraction Subagents

**Spawn subagents with prompt file path (subagent reads prompt, not orchestrator):**

```python
# Get prompt file paths
prompt_dir = project_path / "03-working/prompts/"
prompts = list(prompt_dir.glob("_prompt_*.md"))

# Spawn in parallel (max 15) - subagent reads prompt file directly
for prompt_file in prompts:
    batch_id = prompt_file.stem.replace("_prompt_", "")
    Task(
        subagent_type="general-purpose",
        prompt=f"Read and follow instructions in: {prompt_file}",
        description=f"Extract {batch_id}"
    )
```

**CRITICAL**: Do NOT read prompt content yourself. Pass the file path and let the subagent read it. This saves orchestrator context tokens.

**Subagent Output:** `03-working/_batch_{field}_{N}.yaml`

### Output Schema (YAML - for script processing)

```yaml
---
batch_id: "entity_types_1"
field: entity_types
extracted_at: "2025-12-28T14:40:00"
chunks_read: 3
patterns_found: 8
---

patterns:
  - name: "Endurant (Continuant)"
    chunk_ref: "02-Knowledge_Graphs (Chunk 2:128-133)"
    quote: "An endurant is wholly present at any time during its existence..."
    description: "Core distinction in UFO ontology between things that persist (endurants) vs events (perdurants)"

  - name: "Perdurant (Occurrent)"
    chunk_ref: "02-Knowledge_Graphs (Chunk 2:131-135)"
    quote: "A perdurant can only be partially present at any moment..."
    description: "Events, processes, activities - things that unfold over time"
```

### Concurrency Settings

| Setting | Value | Notes |
|---------|-------|-------|
| Max concurrent subagents | 15 | Parallel extraction |
| Timeout per batch | 5 min | Generous for large batches |
| Retry on failure | 1 | Single retry |

### Progress Display (Level 4)

```
Spawning extraction subagents...
  [entity_types_1] COMPLETE (3 chunks, 8 patterns)
  [entity_types_2] COMPLETE (4 chunks, 12 patterns)
  [entity_types_3] IN_PROGRESS
  [ai_integration_1] COMPLETE (5 chunks, 15 patterns)
  ...

Extracted: 38/45 batches
In progress: 7
Failed: 0
```

---

# PHASE F: VERIFICATION (Script - Level 5)

## Step 6: Verify Subagent Outputs

**Run script to verify subagent outputs with quote-line verification (Gap G15):**

```bash
python 03-skills/research-pipeline/validation/scripts/verify_subagent_output.py \
  {project_path} \
  --input-dir 03-working/ \
  --sample-rate 0.1 \
  --output 03-working/_verification_report.yaml
```

**What the script does (deterministic - no LLM):**
1. Reads all _batch_{field}_{N}.yaml files
2. For each batch, samples 10% of patterns
3. For each sampled pattern:
   - Parses chunk_ref: "Paper-ID (Chunk N:Line-Line)"
   - Reads the actual chunk file
   - Checks if quote exists at cited lines (±5 lines tolerance)
4. Reports verification pass/fail

**Output:** `03-working/_verification_report.yaml`

### Verification Report Structure

```yaml
verified_at: "2025-12-28T14:50:00"
sample_rate: 0.1
batches_checked: 45
patterns_sampled: 120
patterns_verified: 112
patterns_failed: 8

failures:
  - batch_id: "entity_types_2"
    pattern: "Perdurant Definition"
    chunk_ref: "05-DOLCE (Chunk 1:150-155)"
    expected_quote: "A perdurant can only..."
    actual_at_lines: "Different text found"
    verdict: "FAIL - quote mismatch"

stats:
  verification_rate: 93.3%
  threshold: 90%
  verdict: "PASS"
```

### Display Verification (Level 5)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
LEVEL 5: QUOTE-LINE VERIFICATION (Gap G15)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Batches verified: 45
Patterns sampled: 120 (10%)
Patterns verified: 112 (93.3%)
Patterns failed: 8

⚠️ Failed patterns:
  entity_types_2: "Perdurant Definition" - quote mismatch
  ai_integration_3: "Agent Handoff" - line drift

Verdict: PASS (93.3% > 90% threshold)

Proceeding with Level 6 (Aggregation)...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Handle Verification Failure (<90%)

If verification rate < 90%:
1. Identify worst-performing batches
2. Re-run extraction for those batches only
3. Re-verify

---

# PHASE G: AGGREGATION (Script - Level 6)

## Step 7: Aggregate Patterns

**Run script to merge patterns across batches (deterministic - no LLM):**

```bash
python 03-skills/research-pipeline/validation/scripts/aggregate_patterns.py \
  {project_path} \
  --input-dir 03-working/ \
  --output-dir 04-outputs/
```

**What the script does (deterministic - no LLM):**
1. Reads all _batch_{field}_{N}.yaml for each field
2. Merges patterns by name (fuzzy match with 90% similarity)
3. Combines sources: if Pattern X appears in 3 batches, all 3 sources merged
4. Outputs aggregated YAML per field

**Output:** `04-outputs/_synthesis_{field}.yaml`

### Aggregated Field Structure

```yaml
field: entity_types
aggregated_at: "2025-12-28T14:55:00"
batches_merged: 6
patterns_input: 45
patterns_output: 23  # After deduplication

patterns:
  - name: "Endurant (Continuant)"
    sources:
      - chunk_ref: "02-Knowledge_Graphs (Chunk 2:128-133)"
        quote: "An endurant is wholly present..."
      - chunk_ref: "05-DOLCE (Chunk 1:89-95)"
        quote: "DOLCE distinguishes endurants..."
      - chunk_ref: "23-UFO (Chunk 1:173-180)"
        quote: "In UFO, endurants are..."
    description: "Merged from 3 sources. Core distinction: entities wholly present at any time."

  - name: "Perdurant (Occurrent)"
    sources:
      - chunk_ref: "02-Knowledge_Graphs (Chunk 2:131-135)"
        quote: "A perdurant can only be partially present..."
    description: "Events and processes that unfold over time."
```

### Display Aggregation (Level 6)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
LEVEL 6: PATTERN AGGREGATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

| Field | Patterns In | Patterns Out | Dedup Rate |
|-------|-------------|--------------|------------|
| entity_types | 45 | 23 | 49% |
| ai_integration | 52 | 31 | 40% |
| framework_comparison | 38 | 22 | 42% |
...

Total patterns: 280 → 156 (44% deduplication)

Aggregated files saved to: 04-outputs/_synthesis_*.yaml

Proceeding with Level 7 (Final Report)...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

# PHASE H: FINAL REPORT (Subagent - Level 7)

## Step 8: Generate Synthesis Report

**Spawn final report subagent with token budget (Gap G2):**

### Pre-Check: Token Budget

```python
# Read Level 7 budget from _subagent_plan.yaml
plan = read(f"{project_path}/02-resources/_subagent_plan.yaml")
budget = plan['level7_budget']

if budget['requires_split']:
    # Need multiple Level 7 passes
    # Group fields by priority from _briefing.md
    high_priority = [f for f in fields if f['priority'] == 'high']
    medium_priority = [f for f in fields if f['priority'] == 'medium']

    # Pass 1: High-priority fields
    spawn_level7_subagent(high_priority, output="_synthesis_report_high.md")
    # Pass 2: Medium-priority fields
    spawn_level7_subagent(medium_priority, output="_synthesis_report_medium.md")
    # Pass 3: Merge
    spawn_level7_merge_subagent()
else:
    # Single pass - fits in budget
    spawn_level7_subagent(all_fields, output="_synthesis_report.md")
```

### Final Report Subagent Prompt (WITH BUDGET)

```markdown
# FINAL SYNTHESIS REPORT (Level 7)

## TOKEN BUDGET (Gap G2)
You have LIMITED context. Stay within budget:
- Synthesis files: {synthesis_tokens} tokens
- Methodology: 3,000 tokens
- Output reservation: 20,000 tokens
- Usable: {usable_tokens} tokens

## INPUT CONTRACT (STRICT)
Read these files ONLY:
1. `{project_path}/02-resources/_briefing.md`
2. `{project_path}/04-outputs/_synthesis_entity_types.yaml`
3. `{project_path}/04-outputs/_synthesis_ai_integration.yaml`
[... exact list from _subagent_plan.yaml]

DO NOT read chunk files directly - use citations from synthesis files.

## CONTEXT
Research Question: {research_question}
Research Purpose: {research_purpose}

## OUTPUT CONTRACT
Write to: `{project_path}/04-outputs/_synthesis_report.md`

Structure:
1. Executive Summary (3-4 paragraphs answering RQ with citations)
2. Key Findings (5-8 findings with evidence tables)
3. Cross-Field Insights (patterns spanning multiple fields)
4. Recommendations (3-5 with supporting evidence)
5. Limitations
6. Appendix A: Field Summaries
7. Appendix B: Full Reference List

CRITICAL:
- Every claim MUST have inline citation: [Paper-ID (Chunk:Line)]
- Include block quotes for key evidence
- Full reference list at end
```

### Output Structure

```markdown
---
synthesized_at: "{timestamp}"
research_question: "{RQ}"
research_purpose: "{purpose}"
papers_included: 23
fields_synthesized: ["entity_types", "ai_integration", ...]
token_budget_used: {actual}
---

# Research Synthesis: {Title}

## Executive Summary

This synthesis analyzed 23 papers across 15 fields...

Key findings:
1. Foundational ontologies share 4 core entity types [02-KG (2:128), 05-DOLCE (1:89)]
2. AI integration patterns favor hybrid approaches [16-KG-Agent (1:240)]
...

## Key Findings

### Finding 1: Core Entity Type Convergence

| Source | Evidence | Pattern |
|--------|----------|---------|
| 02-Knowledge_Graphs | 2:128-133 | Endurant definition |
| 05-DOLCE | 1:89-95 | Continuant distinction |

> "An endurant is wholly present at any time during its existence"
> — 02-Knowledge_Graphs (Chunk 2:128-133)

...

## Appendix B: Full Reference List

| Paper ID | Title | Chunks Cited |
|----------|-------|--------------|
| 02-Knowledge_Graphs | Survey of... | 2:128, 6:45 |
| 05-DOLCE | A Descriptive... | 1:89 |
```

### Progress Display (Level 7)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
LEVEL 7: FINAL REPORT GENERATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Token budget check:
  Synthesis files: 45,000 tokens
  Usable: 29,950 tokens
  Split required: No

Spawning final report subagent...

[Level 7] Generating synthesis report... COMPLETE

Output: 04-outputs/_synthesis_report.md
  - 23 papers synthesized
  - 156 patterns aggregated
  - 8 key findings
  - 12 cross-field insights

Proceeding with completion...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

# PHASE I: COMPLETION

## Step 9: Mark Project COMPLETE

**Update project status:**

### Update overview.md

```yaml
status: COMPLETE
completed_at: "{timestamp}"
synthesis_version: "7-level"
```

### Final Summary

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
7-LEVEL SYNTHESIS COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Project: {name}
Research Question: "{RQ}"
Research Purpose: "{purpose}"

Pipeline Summary:
  Level 1 (Routing):     127 chunks routed
  Level 2 (Allocation):  45 batches calculated
  Level 3 (Prompts):     45 prompts generated
  Level 4 (Extraction):  45 batches extracted
  Level 5 (Verification): 93.3% verified
  Level 6 (Aggregation): 156 unique patterns
  Level 7 (Report):      1 comprehensive report

Outputs:
  📄 04-outputs/_synthesis_report.md (FULL REPORT)
  📊 04-outputs/_synthesis_{field}.yaml ({M} field aggregations)
  📋 03-working/_verification_report.yaml

Deterministic Scripts Used:
  ✓ build_synthesis_routing.py (Level 1)
  ✓ calculate_subagent_allocation.py (Level 2)
  ✓ generate_subagent_prompts.py (Level 3)
  ✓ verify_subagent_output.py (Level 5)
  ✓ aggregate_patterns.py (Level 6)

Next steps:
  • Review synthesis report
  • Export findings
  • Archive or close project

Say "close session" to save learnings.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Files Created by This Skill

| File | Location | Purpose | Level |
|------|----------|---------|-------|
| `_synthesis_routing.yaml` | 02-resources/ | Routing table (from chunk_index) | L1 |
| `_subagent_plan.yaml` | 02-resources/ | Allocation + token budgets | L2 |
| `_prompt_{batch_id}.md` | 03-working/prompts/ | Generated subagent prompts | L3 |
| `_batch_{field}_{N}.yaml` | 03-working/ | Batch extraction outputs (YAML) | L4 |
| `_verification_report.yaml` | 03-working/ | Quote-line verification | L5 |
| `_synthesis_{field}.yaml` | 04-outputs/ | Per-field aggregation (YAML) | L6 |
| `_synthesis_report.md` | 04-outputs/ | FULL FINAL REPORT (Markdown) | L7 |

---

## Output Format by Level

| Level | Output Format | Why |
|-------|---------------|-----|
| L1-L3 | YAML | Script-generated, machine-readable |
| L4 | YAML | Structured for aggregation script |
| L5 | YAML | Verification data for retry logic |
| L6 | YAML | Structured patterns for Level 7 |
| L7 | Markdown | Human-readable final report |

**Rule**: Script levels output YAML, final subagent outputs Markdown.

---

## Error Handling (7-Level)

| Step | Level | Error | Action |
|------|-------|-------|--------|
| Step 1 | - | No chunk_index | Re-analyze with Schema 2.3 |
| Step 2 | L1 | Script fails | Check index.md format |
| Step 3 | L2 | Token budget overflow | Increase split thresholds |
| Step 4 | L3 | Missing briefing fields | Add to _briefing.md |
| Step 5 | L4 | Subagent fails | Retry once with smaller batch |
| Step 6 | L5 | Verification <90% | Re-extract worst batches |
| Step 7 | L6 | Aggregation merge conflict | Manual review |
| Step 8 | L7 | Token budget exceeded | Split into priority passes |
| Step 9 | - | Status update fails | Manual update overview.md |

---

## Concurrency & Performance

| Setting | Value | Notes |
|---------|-------|-------|
| Max concurrent extraction subagents | 15 | Level 4 parallel |
| Timeout per extraction batch | 5 min | Large chunks |
| Token budget per batch (L4) | 70,000 | Standard formula: chars // 4 |
| Token budget for Level 7 | Calculated | From _subagent_plan.yaml |
| Retry on failure | 1 | Single retry |

---

## Critical Reminders (7-Level)

1. **SCRIPTS ARE DETERMINISTIC** - Levels 1-3, 5-6 use Python scripts, NOT LLM
2. **ONLY 2 SUBAGENT LEVELS** - Level 4 (extraction) and Level 7 (report) use LLM
3. **PRESERVE CITATIONS** - Every level keeps Paper-ID (Chunk:Line)
4. **TOKEN BUDGET IS REAL** - Level 7 has calculated budget, can split
5. **VERIFICATION IS MANDATORY** - Level 5 catches hallucinated quotes
6. **YAML FOR SCRIPTS, MD FOR HUMANS** - Follow format rules

---

## References

- [analyze-research-project skill](../analyze-research-project/SKILL.md)
- [paper-query skill](../../skills/paper-query/SKILL.md)
- [paper-synthesize skill](../../skills/paper-synthesize/SKILL.md)

### Deterministic Scripts (NEW)

| Script | Level | Location |
|--------|-------|----------|
| build_synthesis_routing.py | L1 | validation/scripts/ |
| calculate_subagent_allocation.py | L2 | validation/scripts/ |
| generate_subagent_prompts.py | L3 | validation/scripts/ |
| verify_subagent_output.py | L5 | validation/scripts/ |
| aggregate_patterns.py | L6 | validation/scripts/ |

---

**Version**: 2.0 (2025-12-28)
**Major Changes**:
- v1.0: Initial 4-level architecture
- v2.0: 7-level architecture with deterministic scripts (Gap G2, G13, G15, G19)
  - Added Level 2 (Allocation) with token budget calculation
  - Added Level 3 (Prompt Generation) with INPUT CONTRACT
  - Added Level 5 (Verification) with quote-line checking
  - Moved aggregation from subagent to script (Level 6)
  - Added token budget to Level 7 with split strategy
**Handles**: Phase 3 (Synthesis) only
**Receives from**: `analyze-research-project` (expects papers with index.md + chunk_index)
**Output**: Full markdown synthesis report with citations and references
