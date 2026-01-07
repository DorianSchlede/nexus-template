# Research-Pipeline Patterns for Project 41

**Source**: `03-skills/research-pipeline/`
**Analyzed**: 2026-01-07
**Purpose**: Extract reusable subagent orchestration patterns

---

## Executive Summary

The research-pipeline skill provides a **battle-tested orchestration framework** with:
- Domain-specific subagent factories
- Strict input/output contracts
- Anti-hallucination mechanisms (3-point evidence, hash verification)
- Zero-loss data transfer via handover tickets
- Parallel batch execution with verification

---

## 1. SUBAGENT ORCHESTRATION PATTERNS

### A. Domain-Specific Subagent Factory

**Location**: `dynamic-subagents/core/dynamic_subagent_factory.py` (Lines 37-127)

```python
DOMAIN_REGISTRY = {
    "ontology": {
        "name": "Ontologie-Ingenieur",
        "expertise": ["BFO", "DOLCE", "OWL axioms"],
        "vocabulary": {...},
        "detection_keywords": ["ontology", "BFO", "DOLCE", ...]
    },
    # Similar for: nlp, multi_agent, knowledge_graph
}
```

**P41 Adaptation**: Create TESTING_DOMAINS for unit/integration/e2e test specialization.

### B. Strict Input Contract

**Location**: `dynamic_subagent_factory.py` Lines 249-270

```python
input_contract = InputContract(
    must_read=[
        {"path": "02-resources/_briefing.md", "purpose": "Research question"},
        {"path": "02-resources/papers/{paper_id}/{paper_id}_N.md", "purpose": "Chunk content"}
    ],
    must_not_read=[
        "*.pdf",           # Forbidden file types
        "04-outputs/*",    # Forbidden directories
        "../*"             # Forbidden path traversal
    ]
)
```

**P41 Adaptation**: Control which files test-orchestrator can read during validation.

### C. Strict Output Schema

**Location**: `dynamic_subagent_factory.py` Lines 273-296

```python
output_schema = OutputSchema(
    format="yaml_frontmatter_markdown",
    required_fields=["paper_id", "chunks_read", "analysis_complete", "schema_version"],
    validation_rules=[
        "chunks_read MUST equal chunks_expected",
        "schema_version MUST be '2.3'",
        "Each extraction MUST have chunk:line reference"
    ]
)
```

**P41 Adaptation**: Define exact test report format with validation rules.

---

## 2. ANTI-HALLUCINATION MECHANISMS

### A. 3-Point Evidence (Forced Reading)

**Location**: `forced_reading_contract.py` Lines 30-42

```python
@dataclass
class ReadingProof:
    start_text: str      # First 100 chars after header
    mid_text: str        # 100 chars from 50% position
    end_text: str        # Last 100 chars
    content_hash: str    # SHA256 of full content
    line_count: int
    verification_questions: List[Dict]  # Spot check questions
```

**P41 Use**: Force test-orchestrator to prove it read the feature under test.

### B. Spot-Check Questions

**Location**: `forced_reading_contract.py` Lines 54-87

```python
def generate_verification_questions(content: str, chunk_id: str):
    """Generate questions requiring full content reading."""
    # Question from first third (line ~20%)
    # Question from middle (line ~50%)
    # Question from last third (line ~80%)
    # Subagent MUST answer correctly or output rejected
```

**P41 Use**: Verify test-case-analyzer actually read traces before scoring.

### C. Hash-Chain Verification

**Location**: `handover_manager.py` Lines 82-109

```python
# Orchestrator computes hash BEFORE handover
# Subagent verifies hash WHILE reading
# Orchestrator validates hash AFTER completion

input_manifest:
  files:
    - path: "chunk_1.md"
      expected_hash: "a7b8c9d4e5f6..."  # First 16 chars

# Subagent must report computed_hash that matches
```

**P41 Use**: Verify test scenarios weren't modified during execution.

---

## 3. HANDOVER TICKET SYSTEM

**Location**: `handover_manager.py` Lines 42-102

```python
@dataclass
class HandoverTicket:
    ticket_id: str                      # TASK-2025-12-28-a1b2c3d4
    task_type: str                      # paper_analysis, batch_extraction
    created_at: str                     # ISO timestamp
    orchestrator: str                   # synthesize-research-project

    context: Dict[str, Any]            # research_question, purpose, goals
    input_manifest: InputManifest      # Pre-computed hashes for all input files
    output_contract: OutputContract    # Exact output format
    completion_receipt: Optional[Dict] # Filled by subagent
```

**P41 Adaptation**:

```python
test_ticket = HandoverTicket(
    ticket_id="TEST-2026-01-07-plan_project_basic",
    task_type="subagent_validation",

    context={
        "feature_under_test": "plan-project skill",
        "scenario": "basic_flow",
        "pass_criteria": ["Created project folder", "Generated 4 files"]
    },

    input_manifest=InputManifest(
        files=[
            InputFile(
                path="02-resources/tests/scenarios.yaml",
                hash="a7b8c9d4...",
                purpose="Test definition"
            )
        ]
    ),

    output_contract=OutputContract(
        file="04-outputs/validation-reports/{timestamp}.md",
        format="markdown_with_yaml_frontmatter",
        validation_rules=["Pass rate per criterion calculated"]
    )
)
```

---

## 4. FILE ORGANIZATION STRATEGY

**Location**: `analyze-research-project/SKILL.md` Lines 520-531

```
02-resources/          # INPUTS (read-only for subagents)
├── tests/
│   ├── scenarios.yaml    # Test definitions
│   └── fixtures/         # Test data

03-working/            # PROCESSING (subagent workspace)
├── prompts/
│   └── _prompt_{task_id}.md
├── _batch_{scenario}_{N}.yaml
└── _verification_{task_id}.yaml

04-outputs/            # RESULTS (final artifacts)
├── validation-reports/
│   └── {timestamp}-{scenario}.md
└── _test_summary.yaml
```

**Key Pattern**: Three-phase directory structure prevents input corruption.

---

## 5. PARALLEL BATCH EXECUTION

**Location**: `synthesize-research-project/SKILL.md` Lines 158-182

```python
# Token-based batch allocation
batch_allocation = {
    "batches": [
        {
            "batch_id": "scenario_batch_1",
            "scenarios": ["basic_flow", "error_handling"],
            "tokens_estimate": 15000,
            "max_concurrent": 3  # Worktrees per batch
        }
    ],
    "budget": {
        "per_batch_tokens": 70000,
        "max_concurrent_subagents": 15
    }
}
```

**P41 Use**: Allocate test scenarios to batches, run in parallel worktrees.

---

## 6. ERROR HANDLING & RECOVERY

### A. Timeout Partial Save Protocol

**Location**: `analyze-research-project/SKILL.md` Lines 689-725

```python
# When timeout occurs, subagent MUST write partial progress:
error_handling:
  timeout_occurred: true
  partial_success: true
  scenarios_completed: ["basic_flow", "error_handling"]
  scenarios_remaining: ["edge_case"]
  recovery_notes: "Resume from edge_case scenario"
```

**P41 Use**: If test run times out, preserve completed test results.

### B. Verification Failure Handling

**Location**: `verify_subagent_reading.py` Lines 57-60

```python
# Critical failures (immediate rejection)
critical_failures = ['hash', 'evidence_start', 'evidence_end']

# Non-critical (warnings)
warnings = ['line_count']  # Within ±10% tolerance
```

**P41 Use**: Define critical vs warning-level test failures.

---

## 7. PATTERNS TO ADOPT IN PROJECT 41

| Pattern | Source | P41 Application |
|---------|--------|-----------------|
| **Domain Registry** | Lines 37-127 | Test type specialization |
| **Input Contract** | Lines 249-270 | Control test agent file access |
| **Output Schema** | Lines 273-296 | Enforce test report format |
| **3-Point Evidence** | Lines 30-42 | Prove traces were read |
| **Hash Verification** | Lines 82-109 | Verify scenario integrity |
| **Handover Tickets** | Lines 42-102 | Track reproducible test runs |
| **Batch Allocation** | Lines 158-182 | Parallelize with token budgets |
| **Partial Save** | Lines 689-725 | Resume interrupted tests |

---

## 8. IMPLEMENTATION CHECKLIST FOR P41

### Phase 1: Adopt Core Patterns
- [ ] Create TestHandoverTicket dataclass
- [ ] Define TestInputContract with must_read/must_not_read
- [ ] Define TestOutputSchema with validation_rules

### Phase 2: Add Verification
- [ ] Implement hash verification for scenario files
- [ ] Add 3-point evidence requirement to test-case-analyzer
- [ ] Define critical vs warning failures

### Phase 3: Parallel Execution
- [ ] Implement batch allocation for scenarios
- [ ] Use worktrees as batch isolation
- [ ] Track per-worktree completion status

### Phase 4: Error Recovery
- [ ] Implement partial save on timeout
- [ ] Add resume capability for interrupted tests
- [ ] Log recovery notes for debugging

---

*These patterns have been validated in production research pipelines.*
*Adapt, don't copy - testing has different constraints than research.*
