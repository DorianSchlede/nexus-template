# Research Algorithm Documentation

> Comprehensive documentation of the Nexus Research Pipeline for academic paper analysis and synthesis.

---

## Overview

The Nexus Research Algorithm is a sophisticated **3-phase pipeline** that automates the discovery, acquisition, analysis, and synthesis of academic papers. It consists of **11 components** (3 orchestrators, 6 skills, 1 master router, 1 shared methodology) that work together to transform a research question into actionable insights with comprehensive cross-paper synthesis.

---

## System Architecture

```mermaid
graph TB
    subgraph "Phase 1: Planning & Acquisition"
        CRP[create-research-project] --> PS[paper-search]
        PS --> PP[pdf-preprocess]
    end

    subgraph "Phase 2: Analysis"
        ARP[analyze-research-project] --> PA[paper-analyze]
        PA --> PAC[paper-analyze-core]
    end

    subgraph "Phase 3: Synthesis (7-Level)"
        SRP[synthesize-research-project]
        L1[L1: Routing Script]
        L2[L2: Allocation Script]
        L3[L3: Prompts Script]
        L4[L4: Extraction Subagents]
        L5[L5: Verification Script]
        L6[L6: Aggregation Script]
        L7[L7: Report Subagent]

        SRP --> L1 --> L2 --> L3 --> L4 --> L5 --> L6 --> L7
    end

    subgraph "Utility Skills"
        PQ[paper-query]
        PM[paper-manage]
    end

    CRP --> ARP
    PP --> PA
    ARP --> SRP
    SRP --> PQ
    PM --> CRP
    PM --> ARP

    style CRP fill:#4CAF50,color:white
    style ARP fill:#2196F3,color:white
    style SRP fill:#9C27B0,color:white
    style PAC fill:#FF9800,color:white
```

---

## Complete Process Flow

```mermaid
flowchart TD
    Start([User: Research Question]) --> Init[Initialize Project]

    subgraph Phase1["Phase 1: Planning & Acquisition (Steps 0-13)"]
        Init --> Define[Step 2: Define Research Question]
        Define --> Brief[Create _briefing.md]
        Brief --> Search[Step 3: Search Academic APIs]
        Search --> Results[_search_results.md]
        Results --> Review[Step 4: AI Abstract Review]
        Review --> Abstract[_abstract_reviews.md]
        Abstract --> Select[Step 5: User Paper Selection]
        Select --> Gate1{Step 6: Selection Gate}
        Gate1 -->|Approved| Download[Step 7: Download Papers]
        Gate1 -->|Modify| Select
        Download --> Preprocess[Step 8: PDF to Markdown Chunks]
        Preprocess --> Kit[Step 10: Generate Analysis Kit]
        Kit --> Guide[Step 11: Generate Extraction Guide]
        Guide --> Orch[Step 12: Generate Orchestrator Instructions]
        Orch --> Ready1{Step 13: Readiness Gate}
    end

    subgraph Phase2["Phase 2: Analysis (Steps 0-4)"]
        Ready1 -->|Ready| Validate1[Step 1: Validate Readiness]
        Validate1 --> Plan[Step 1.5: Read Pre-Calculated Allocation]
        Plan --> Analyze[Step 2: Spawn Subagents per Allocation]
        Analyze --> Index[index.md per Paper]
        Index --> Validate2[Step 3: Validate Analysis Logs]
        Validate2 --> Ready2[Step 4: Mark READY_FOR_SYNTHESIS]
    end

    subgraph Phase3["Phase 3: Synthesis (Steps 0-9, 7 Levels)"]
        Ready2 --> ValidateP3[Step 1: Validate Readiness]
        ValidateP3 --> L1[Step 2: L1 Routing Script]
        L1 --> L2[Step 3: L2 Allocation Script]
        L2 --> L4Prompts[Step 4: L3 Generate Prompts]
        L4Prompts --> L4[Step 5: L4 Extract Patterns]
        L4 --> L5[Step 6: L5 Verify Quotes]
        L5 --> L6[Step 7: L6 Aggregate Patterns]
        L6 --> L7[Step 8: L7 Generate Report]
        L7 --> Complete[Step 9: Mark Complete]
    end

    Complete --> End([_synthesis_report.md])

    style Phase1 fill:#E8F5E9
    style Phase2 fill:#E3F2FD
    style Phase3 fill:#F3E5F5
```

---

## Skills Overview

### Orchestrators (3)

| Orchestrator | Phase | Steps | Purpose |
|--------------|-------|-------|---------|
| `create-research-project` | Phase 1 | 0-13 | Planning & Acquisition |
| `analyze-research-project` | Phase 2 | 0-4 | Per-paper analysis |
| `synthesize-research-project` | Phase 3 | 0-9 | Cross-paper synthesis (7-level) |

### Core Skills (6)

| Skill | Purpose | Trigger Keywords |
|-------|---------|------------------|
| `paper-search` | Search 9 academic APIs | "find paper", "search paper" |
| `pdf-preprocess` | Convert PDFs to markdown | "preprocess pdf", "chunk pdf" |
| `paper-analyze` | Orchestrate paper analysis | "analyze papers", "process papers" |
| `paper-synthesize` | Cross-paper synthesis | "synthesize collection" |
| `paper-query` | Query analyzed papers | "query papers", "find papers about" |
| `paper-manage` | Manage collections | "list collections", "paper stats" |

### Shared Components (2)

| Component | Type | Purpose |
|-----------|------|---------|
| `paper-analyze-core` | Shared methodology | Analysis methodology (internal use) |
| `SKILL.md` | Master router | Skill-chain router |

---

## Phase 1: Planning & Acquisition

### Workflow Diagram

```mermaid
sequenceDiagram
    participant U as User
    participant CRP as create-research-project
    participant PS as paper-search
    participant PP as pdf-preprocess

    U->>CRP: "Start research on [topic]"
    CRP->>CRP: Create project structure
    CRP->>U: Request research question
    U->>CRP: Define RQ + extraction schema
    CRP->>CRP: Create _briefing.md

    CRP->>PS: Search academic APIs
    PS->>PS: Query 9 APIs (S2, OpenAlex, arXiv...)
    PS->>CRP: Return _search_results.md

    CRP->>CRP: AI Abstract Review
    CRP->>U: Present paper recommendations
    U->>CRP: Approve/modify selection
    CRP->>CRP: Create _selection_log.md

    CRP->>PS: Download approved papers
    PS->>PS: Multi-source fallback resolution
    PS->>CRP: Return PDFs

    CRP->>PP: Preprocess PDFs
    PP->>PP: Convert to markdown chunks
    PP->>CRP: Return chunks + _metadata.json

    CRP->>CRP: Generate _analysis_kit.md
    CRP->>U: Readiness Gate
```

### Step Details

#### Steps 0-3: Research Definition
- **Step 0**: Initialize TodoWrite task tracking
- **Step 1**: Create Nexus project structure
- **Step 2**: Interactive research question definition → `_briefing.md`
- **Step 3**: Search academic APIs → `_search_results.md`

#### Steps 4-6: Paper Selection
- **Step 4**: AI reviews abstracts with scoring (1-5) → `_abstract_reviews.md`
- **Step 5**: User selection interface → `_selection_log.md`
- **Step 6**: Selection Gate (user approves papers)

#### Steps 7-9: Acquisition
- **Step 7**: Batch download with multi-source fallback
- **Step 8**: PDF preprocessing to markdown chunks (max 1000 lines/chunk)
- **Step 9**: Acquisition Report + User Gate

#### Steps 10-13: Readiness Gate (NEW in v5.0)
- **Step 10**: Generate `_analysis_kit.md` (subagent context) + validate
- **Step 11**: Generate `_extraction_guide.md` (field examples + vocabulary) + validate
- **Step 12**: Calculate subagent allocation + Generate orchestrator instructions in `plan.md`
  - 12.1: Calculate allocation based on chunk counts (see Subagent Planning table)
  - 12.2: Write allocation table to plan.md
  - 12.3: Generate subagent prompts with pre-calculated splits
- **Step 13**: Confirm ready for execution → Handoff to Phase 2

---

## Phase 2: Analysis

### Workflow Diagram

```mermaid
sequenceDiagram
    participant U as User
    participant ARP as analyze-research-project
    participant PA as paper-analyze
    participant PAC as paper-analyze-core

    U->>ARP: "Analyze research project"
    ARP->>ARP: Validate readiness
    ARP->>ARP: Read pre-calculated allocation from plan.md

    loop For each paper (max 15 concurrent)
        ARP->>PA: Spawn subagent
        PA->>PAC: Load methodology
        PAC->>PAC: 7-step analysis
        PAC->>PA: Return index.md + _analysis_log.md
    end

    PA->>ARP: All analyses complete
    ARP->>ARP: Validate analysis logs (schema v2.3)
    ARP->>ARP: Mark READY_FOR_SYNTHESIS
    ARP->>U: Analysis Complete
```

### Analysis Methodology (7 Steps)

```mermaid
graph LR
    S0[Step 0: Init Log] --> S1[Step 1: Read Briefing]
    S1 --> S2[Step 2: Read Metadata]
    S2 --> S3[Step 3: Analyze Chunks]
    S3 --> S4[Step 4: Compile index.md]
    S4 --> S5[Step 5: Validate]
    S5 --> S6[Step 6: Complete Log]

    style S0 fill:#FFF3E0
    style S3 fill:#E8F5E9
    style S6 fill:#E3F2FD
```

#### Anti-Hallucination Measures
- **3-Point Evidence Recording**: Start (100 chars), Mid (100 chars), End (100 chars)
- **SHA256 Hash**: Full chunk content verification
- **Chunk:Line References**: Every extraction must cite source location

---

## Phase 3: Cross-Paper Synthesis

### 7-Level Hierarchical Architecture

Phase 3 implements a sophisticated **7-level synthesis architecture** where Levels 1-3, 5-6 are deterministic Python scripts, and only Levels 4 & 7 use LLM subagents.

```mermaid
graph TD
    Input[All index.md files] --> L1[Level 1: Routing Script]
    L1 -->|_synthesis_routing.yaml| L2[Level 2: Allocation Script]
    L2 -->|_subagent_plan.yaml| L3[Level 3: Prompts Script]
    L3 -->|45× _prompt_*.md| L4[Level 4: Extraction Subagents]
    L4 -->|_batch_*.yaml| L5[Level 5: Verification Script]
    L5 -->|_verification_report.yaml| L6[Level 6: Aggregation Script]
    L6 -->|_synthesis_{field}.yaml| L7[Level 7: Report Subagent]
    L7 --> Output[_synthesis_report.md]

    style L1 fill:#FFF3E0
    style L2 fill:#FFF3E0
    style L3 fill:#FFF3E0
    style L4 fill:#E3F2FD
    style L5 fill:#FFF3E0
    style L6 fill:#FFF3E0
    style L7 fill:#E3F2FD
```

### Level Breakdown

| Level | Type | Purpose | Output |
|-------|------|---------|--------|
| **L1: Routing** | Script | Boolean chunk lookup by field | `_synthesis_routing.yaml` |
| **L2: Allocation** | Script | Greedy bin-packing (70k tokens/batch) + L7 budget | `_subagent_plan.yaml` |
| **L3: Prompts** | Script | Generate INPUT CONTRACT per batch | `_prompt_{batch_id}.md` |
| **L4: Extraction** | 15 Subagents | Parallel pattern extraction with citations | `_batch_{field}_{N}.yaml` |
| **L5: Verification** | Script | 10% sample quote-line checking (±5 line tolerance) | `_verification_report.yaml` |
| **L6: Aggregation** | Script | Fuzzy deduplication (90% similarity threshold) | `_synthesis_{field}.yaml` |
| **L7: Report** | Subagent | Narrative synthesis with cross-field insights | `_synthesis_report.md` |

### Why 7 Levels?

**Determinism**: 6/7 levels are Python scripts (reproducible)
- L1-3: Routing, allocation, prompt generation are 100% deterministic
- L5-6: Verification and aggregation are algorithmic
- Only L4 & L7 require LLM intelligence

**Verifiability**: Level 5 catches hallucinations
- 10% sample verification with ±5 line tolerance
- 90% threshold to pass
- Re-extracts failed batches automatically

**Scalability**: Parallel extraction
- 15 concurrent subagents at Level 4
- ~10 minutes for 23 papers (45 batches ÷ 15 = 3 rounds)

**Cost-Effective**: Scripts are free
- Only L4 extraction and L7 report use LLM
- Saves ~70% on token costs vs. single-pass synthesis

**Safe**: Token budget calculated upfront
- Level 2 calculates Level 7 budget
- Splits into priority passes if needed
- INPUT CONTRACT prevents scope drift

### Gap Fixes in Phase 3

| Gap | Issue | Solution |
|-----|-------|----------|
| **G2** | No token budget for L7 | L2 calculates budget, splits if >75k synthesis tokens |
| **G13** | No input scope control | L3 generates INPUT CONTRACT per prompt |
| **G15** | Can't verify citations | L5 quote-line verification (10% sample, 90% threshold) |
| **G19** | Too-generic fields | L1 sparsity check (>80% match = warning) |
| **G22a** | Missing research context | L3 includes research_purpose in prompts |
| **G22b** | Missing synthesis goals | L3 includes synthesis_goals in prompts |

---

## Data Flow Architecture

```mermaid
graph TB
    subgraph Input
        RQ[Research Question]
        APIs[9 Academic APIs]
        PDFs[PDF Papers]
    end

    subgraph Processing
        Brief[_briefing.md]
        Search[_search_results.md]
        Reviews[_abstract_reviews.md]
        Select[_selection_log.md]
        Kit[_analysis_kit.md]
    end

    subgraph Analysis
        Meta[_metadata.json]
        Chunks[Paper Chunks]
        Log[_analysis_log.md]
        Index[index.md]
    end

    subgraph Output
        Synth[_synthesis.md]
        Valid[_validation_report.md]
        Quality[_quality_metrics.md]
    end

    RQ --> Brief
    APIs --> Search
    Search --> Reviews
    Reviews --> Select
    Select --> Kit
    PDFs --> Meta
    PDFs --> Chunks
    Chunks --> Log
    Log --> Index
    Index --> Synth
    Index --> Valid
    Valid --> Quality
```

---

## Project Structure

```
02-projects/NN-{slug}/
├── 01-planning/
│   ├── overview.md          # Project metadata
│   ├── plan.md              # Orchestrator instructions + subagent prompts
│   └── steps.md             # Progress checkboxes
├── 02-resources/
│   ├── _briefing.md         # Research question + schema
│   ├── _analysis_kit.md     # Subagent context (consolidated)
│   ├── _extraction_guide.md # Field examples + controlled vocabulary
│   ├── _search_results.md   # API search results
│   ├── _abstract_reviews.md # AI assessments
│   └── papers/
│       └── {paper}/
│           ├── {paper}.pdf
│           ├── {paper}_1.md, _2.md, ...
│           ├── _metadata.json
│           ├── _analysis_log.md
│           └── index.md
├── 03-working/
│   ├── _selection_log.md    # Approved papers + acquisition status
│   └── _resume.md           # Context recovery checkpoint
└── 04-outputs/
    ├── _synthesis.md        # Cross-paper synthesis
    ├── _synthesis_validation.md  # Synthesis spot-check results
    ├── _validation_report.md
    └── _quality_metrics.md
```

---

## Validation System

### Three-Level Validation

```mermaid
graph TD
    subgraph Level1["Level 1: Analysis Validation"]
        A1[Schema Version Check]
        A2[Step Completion Check]
        A3[Chunk Evidence Verification]
        A4[Hash Validation]
    end

    subgraph Level2["Level 2: Log Validation"]
        B1[All Chunks Read?]
        B2[Evidence Matches Content?]
        B3[index.md Created?]
    end

    subgraph Level3["Level 3: Synthesis Validation"]
        C1[Frontmatter Complete?]
        C2[Paper References Exist?]
        C3[Spot-Check Claims]
        C4[Coverage >= 70%?]
    end

    A1 --> A2 --> A3 --> A4
    B1 --> B2 --> B3
    C1 --> C2 --> C3 --> C4

    Level1 --> Level2 --> Level3
```

### Validation Thresholds

| Metric | Pass | Warn | Fail |
|--------|------|------|------|
| Frontmatter completeness | 100% | <100% | Missing required |
| Paper reference accuracy | 100% | >90% | <90% |
| Spot-check verification | >90% | 70-90% | <70% |
| Coverage | >80% | 60-80% | <60% |

---

## Paper Query System

### 3-Level Progressive Disclosure

```mermaid
graph TD
    Query[User Query] --> L1[Level 1: Frontmatter Scan]
    L1 --> |Python Script| Results1[Ranked Paper List]
    Results1 --> L2[Level 2: Full Index Reading]
    L2 --> |AI| Results2[Relevant Chunks Identified]
    Results2 --> L3[Level 3: Chunk Loading]
    L3 --> |AI| Answer[Answer with Citations]

    style L1 fill:#E8F5E9
    style L2 fill:#FFF3E0
    style L3 fill:#E3F2FD
```

### Ranking Factors

| Factor | Weight | Source |
|--------|--------|--------|
| relevance_triggers match | 3x | index.md YAML |
| topics match | 2x | index.md YAML |
| methods match | 2x | index.md YAML |
| key_findings match | 1x | index.md YAML |
| year (newer preferred) | 0.5x | index.md YAML |

---

## Academic API Coverage

```mermaid
pie title "API Coverage (1B+ Documents)"
    "OpenAlex" : 250
    "CORE" : 300
    "BASE" : 300
    "Semantic Scholar" : 200
    "CrossRef" : 130
    "PubMed" : 35
    "arXiv" : 2
    "DOAJ" : 9
```

| API | Documents | Best For |
|-----|-----------|----------|
| Semantic Scholar | 200M+ | CS/AI, citations |
| OpenAlex | 250M+ | Broad academic |
| arXiv | 2M+ | CS/Physics/Math preprints |
| CrossRef | 130M+ | DOI metadata |
| PubMed | 35M+ | Biomedical |
| CORE | 300M+ | UK/EU research |
| BASE | 300M+ | German aggregator |
| DOAJ | 9M+ | Verified OA journals |
| Unpaywall | - | OA PDF lookup via DOI |

---

## Token Budget Management

```mermaid
graph LR
    subgraph "100k Context Window"
        A[Methodology: 3k]
        B[Briefing: 2k]
        C[Metadata: 0.5k]
        D[Log Overhead: 3.5k]
        E[Paper Content: 74k]
        F[Output Buffer: 17k]
    end

    style E fill:#4CAF50,color:white
```

### Large Paper Handling (Phase 2)

- Papers > 8 chunks are split into parts (calculated in Phase 1 Step 12)
- Each part analyzed by separate subagent
- Merge subagent combines partial indexes
- Final unified index.md generated

### Large Synthesis Handling (Phase 3)

- If synthesis files > 75k tokens, Level 2 sets `requires_split: true`
- Level 7 processes high-priority fields first
- Level 7 processes medium/low-priority fields second
- Final merge pass combines all outputs

---

## Error Handling

### By Phase

| Phase | Error | Action |
|-------|-------|--------|
| Search | API rate limit | Wait and retry |
| Download | All paywalled | Suggest arXiv alternatives |
| Preprocess | PDF corrupted | Skip, log error |
| Analysis | Subagent fails | Retry once, then log failure |
| Validation | Evidence mismatch | Re-analyze or exclude |
| Synthesis | <3 papers | Warn about limited synthesis |

---

## Concurrency & Performance

| Setting | Value | Notes |
|---------|-------|-------|
| Max concurrent subagents | 15 | Parallel analysis for speed |
| Timeout per paper | 5 min | Generous for large papers |
| Retry on failure | 1 | Single retry before exclusion |
| Min papers for synthesis | 3 | Warn if fewer |

### Subagent Planning (Phase 1 Step 12)

**Allocation is calculated ONCE in Phase 1 Step 12 and written to plan.md.**
Phase 2 reads the pre-calculated allocation - it does NOT recalculate.

**Token estimation**: Each chunk ≈ 10-15k tokens (1000 lines × ~50 chars/line)
**Usable budget**: 74k tokens per subagent (after 26k methodology overhead)

| Chunk Count | Est. Tokens | Subagents | Strategy |
|-------------|-------------|-----------|----------|
| 1-3 chunks | <45k | 1 | Single subagent analyzes all |
| 4-6 chunks | 45k-74k | 1 | Single subagent (near limit) |
| 7-12 chunks | 74k-150k | 2 | Split at chunk 6, merge after |
| 13-18 chunks | 150k-220k | 3 | Split into 6-chunk segments |
| 19+ chunks | >220k | 4+ | Split into 5-6 chunk segments |

**Allocation table in plan.md** (written by Phase 1 Step 12):
```markdown
## Subagent Allocation Plan

| Paper ID | Chunks | Est. Tokens | Subagents | Splits |
|----------|--------|-------------|-----------|--------|
| Paper_A  | 4      | ~47,000     | 1         | 1-4    |
| Paper_B  | 10     | ~120,000    | 2         | 1-6, 7-10 |

**Total subagents**: 3
```

---

## Context Recovery

The pipeline maintains `_resume.md` for context recovery after compaction:

```yaml
---
updated: "{timestamp}"
phase: "definition|selection|acquisition|readiness|analysis|synthesis"
project_id: "{project_id}"
step: {current_step_number}
---

# Resume Context

## Current State
- Phase: {current phase}
- Step: {step_number} - {step_name}
- Papers analyzed: {N}/{total}

## Next Actions
1. {immediate next step}
2. {following step}
```

**Update triggers**:
- Context usage reaches ~60%
- After completing each major step
- After user approval gates

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 6.0 | 2026-01-01 | **MAJOR ARCHITECTURE UPDATE**: Documented 3-phase pipeline (was 2-phase), added complete Phase 3 (synthesize-research-project) with 7-level architecture, fixed orchestrator names, updated skill count to 11 components |
| 5.0 | 2025-12-28 | Added Steps 10-13 (analysis kit, extraction guide, orchestrator), 15 concurrent subagents, _resume.md context recovery, subagent planning |
| 4.0 | 2025-12-19 | Added analysis kit, orchestrator templates, Phase 4.5 validation |
| 2.2 | 2025-12-19 | Added chunk:line extraction tracking, two-tier detail strategy |
| 2.1 | 2025-12-19 | Added 3-point anti-hallucination sampling |
| 2.0 | 2025-12-19 | Separated planning/acquisition from analysis/synthesis |

---

**Last Updated**: 2026-01-01
