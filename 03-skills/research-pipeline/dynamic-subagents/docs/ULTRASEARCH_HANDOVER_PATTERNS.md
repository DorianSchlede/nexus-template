# ULTRASEARCH: Subagent Handover Patterns

> **Zero-Loss Data Transfer zwischen Orchestrator und Subagents**

---

## Das Handover-Problem

```
ORCHESTRATOR                    SUBAGENT                    PROBLEM
────────────────────────────────────────────────────────────────────
"Analysiere Paper X"    →→→    "Hier ist mein Output"      VAGE
"Lies diese 5 Dateien"  →→→    "Hab ich gemacht"           NICHT VERIFIZIERBAR
"Extrahiere Patterns"   →→→    "Patterns: A, B, C"         OHNE KONTEXT
"Fasse zusammen"        →→→    "Summary: ..."              CITATIONS VERLOREN
```

**ULTRASEARCH LÖSUNG**: Strukturierte Handover-Protokolle mit vollständiger Traceability

---

## Pattern 1: TICKET-BASED HANDOVER

```
┌─────────────────────────────────────────────────────────────────────┐
│                        TICKET STRUCTURE                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ticket_id: "TASK-2025-12-28-001"                                  │
│  created_at: "2025-12-28T15:30:00"                                 │
│  orchestrator: "synthesize-research-project"                        │
│  subagent_type: "general-purpose"                                   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ INPUT MANIFEST                                               │   │
│  ├─────────────────────────────────────────────────────────────┤   │
│  │ files:                                                       │   │
│  │   - path: "02-resources/_briefing.md"                       │   │
│  │     hash: "a7b8c9d4..."                                     │   │
│  │     required: true                                           │   │
│  │     purpose: "Research question"                             │   │
│  │                                                              │   │
│  │   - path: "02-resources/papers/02-KG/02-KG_1.md"           │   │
│  │     hash: "e5f6g7h8..."                                     │   │
│  │     required: true                                           │   │
│  │     purpose: "Chunk 1 content"                               │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ OUTPUT CONTRACT                                              │   │
│  ├─────────────────────────────────────────────────────────────┤   │
│  │ file: "03-working/_batch_entity_types_1.yaml"               │   │
│  │ format: "yaml"                                               │   │
│  │ schema_version: "2.3"                                        │   │
│  │ required_fields: [batch_id, field, patterns]                │   │
│  │ validation_script: "verify_batch.py"                         │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ COMPLETION RECEIPT (filled by subagent)                     │   │
│  ├─────────────────────────────────────────────────────────────┤   │
│  │ completed_at: "2025-12-28T15:35:00"                         │   │
│  │ files_read:                                                  │   │
│  │   - path: "02-resources/_briefing.md"                       │   │
│  │     hash_verified: true                                      │   │
│  │   - path: "02-resources/papers/02-KG/02-KG_1.md"           │   │
│  │     hash_verified: true                                      │   │
│  │ output_written: "03-working/_batch_entity_types_1.yaml"     │   │
│  │ output_hash: "i9j0k1l2..."                                  │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**Key Insight**: Jeder Handover hat ein TICKET mit:
- Input Manifest (was gelesen werden MUSS)
- Output Contract (was produziert werden MUSS)
- Completion Receipt (Beweis dass es getan wurde)

---

## Pattern 2: HASH-CHAIN VERIFICATION

```
ORCHESTRATOR                     SUBAGENT                      VERIFICATION
─────────────────────────────────────────────────────────────────────────────

1. PRE-COMPUTE HASHES
   ┌──────────────────┐
   │ Compute hash of  │
   │ each input file  │
   │ BEFORE handover  │
   └────────┬─────────┘
            │
            ▼
   input_hashes:
     briefing: "a7b8c9d4"
     chunk_1: "e5f6g7h8"
     chunk_2: "i9j0k1l2"

2. INCLUDE IN PROMPT              3. VERIFY DURING READ           4. VALIDATE AFTER
   ┌──────────────────┐           ┌──────────────────┐           ┌──────────────────┐
   │ "Expected hash   │    →→→    │ Read file,       │    →→→    │ Compare hashes   │
   │  for chunk_1:    │           │ compute hash,    │           │ in receipt vs    │
   │  e5f6g7h8"       │           │ verify match     │           │ expected         │
   └──────────────────┘           └──────────────────┘           └──────────────────┘

MISMATCH = File was modified OR subagent read wrong file OR incomplete read
```

**Implementation**:

```yaml
# In prompt
input_manifest:
  files:
    - path: "chunk_1.md"
      expected_hash: "e5f6g7h8..."  # First 16 chars

# Subagent must report
files_read:
  - path: "chunk_1.md"
    computed_hash: "e5f6g7h8..."  # Must match
    match: true
```

---

## Pattern 3: CITATION CHAIN PRESERVATION

```
PROBLEM: Citations get lost or corrupted through pipeline stages

SOLUTION: Citation Chain with validation at each step

Stage 1: EXTRACTION
─────────────────────
Pattern: "Endurant Definition"
Source: 02-KG (Chunk 2:128-133)
Quote: "An endurant is wholly present..."
Hash: "q1w2e3r4"  ← Hash of this extraction record
         │
         ▼
Stage 2: AGGREGATION
─────────────────────
Pattern: "Endurant Definition"
Sources:
  - ref: 02-KG (Chunk 2:128-133)
    extraction_hash: "q1w2e3r4"  ← Chain link
  - ref: 05-DOLCE (Chunk 1:89-95)
    extraction_hash: "t5y6u7i8"  ← Chain link
         │
         ▼
Stage 3: SYNTHESIS
─────────────────────
Finding: "Foundational ontologies share endurant concept"
Citations:
  - 02-KG (2:128) via extraction "q1w2e3r4"
  - 05-DOLCE (1:89) via extraction "t5y6u7i8"
         │
         ▼
VALIDATION: Trace any citation back to original source
```

**Rule**: Every citation carries its chain hash for traceability.

---

## Pattern 4: STRUCTURED HANDOVER PROTOCOL (SHP)

```yaml
# _handover_{task_id}.yaml

handover:
  version: "1.0"
  task_id: "batch_extraction_entity_types_1"

  # PHASE 1: Orchestrator prepares
  preparation:
    timestamp: "2025-12-28T15:30:00"
    context:
      research_question: "What entity types exist in foundational ontologies?"
      research_purpose: "Build taxonomy for AI agent framework"
      field: "entity_types"

    input_files:
      - path: "02-resources/_briefing.md"
        hash: "a7b8c9d4e5f6g7h8i9j0k1l2m3n4o5p6"
        lines: 127
        purpose: "Research context and schema"

      - path: "02-resources/papers/02-KG/02-KG_2.md"
        hash: "q1w2e3r4t5y6u7i8o9p0a1s2d3f4g5h6"
        lines: 487
        token_estimate: 12175
        purpose: "Primary extraction source"

    output_spec:
      file: "03-working/_batch_entity_types_1.yaml"
      format: "yaml"
      schema:
        required: [batch_id, field, extracted_at, patterns]
        patterns_each: [name, chunk_ref, quote, description]
      validation:
        - "patterns[].chunk_ref matches ^[\\w-]+ \\(Chunk \\d+:\\d+-\\d+\\)$"
        - "patterns[].quote length between 50-200 chars"
        - "all chunk_refs point to files in input_files"

  # PHASE 2: Subagent executes
  execution:
    started_at: "2025-12-28T15:30:05"
    completed_at: "2025-12-28T15:35:42"

    files_read:
      - path: "02-resources/_briefing.md"
        hash_verified: true
        lines_counted: 127

      - path: "02-resources/papers/02-KG/02-KG_2.md"
        hash_verified: true
        lines_counted: 487
        reading_evidence:
          start: "Knowledge graphs represent structured..."
          mid: "entity types can be classified into..."
          end: "comprehensive taxonomy framework."

    output_produced:
      file: "03-working/_batch_entity_types_1.yaml"
      hash: "z9x8c7v6b5n4m3l2k1j0h9g8f7d6s5a4"
      patterns_count: 12

  # PHASE 3: Orchestrator validates
  validation:
    timestamp: "2025-12-28T15:35:45"

    input_hashes_match: true
    output_schema_valid: true

    spot_checks:
      - pattern: "Endurant"
        chunk_ref: "02-KG (Chunk 2:128-133)"
        quote_found_at_line: true

      - pattern: "Perdurant"
        chunk_ref: "02-KG (Chunk 2:131-135)"
        quote_found_at_line: true

    verdict: "PASS"
    confidence: 0.95
```

---

## Pattern 5: MULTI-STAGE HANDOVER CHAIN

Für komplexe Pipelines mit mehreren Subagents:

```
ORCHESTRATOR
     │
     ├──► SUBAGENT 1 (Extraction Batch 1)
     │         │
     │         ▼
     │    _batch_1.yaml ──────────────────────────┐
     │                                            │
     ├──► SUBAGENT 2 (Extraction Batch 2)        │
     │         │                                  │
     │         ▼                                  │
     │    _batch_2.yaml ──────────────────────────┤
     │                                            │
     │    ┌───────────────────────────────────────┤
     │    │ AGGREGATION SCRIPT                    │
     │    │ (deterministic, no subagent)          │
     │    │                                       │
     │    │ Inputs:                               │
     │    │   - _batch_1.yaml (hash: "...")       │
     │    │   - _batch_2.yaml (hash: "...")       │
     │    │                                       │
     │    │ Output:                               │
     │    │   - _synthesis_field.yaml             │
     │    └───────────────────────────────────────┘
     │                                            │
     │                                            ▼
     │    ┌───────────────────────────────────────┐
     │    │ CHAIN MANIFEST                        │
     │    │                                       │
     │    │ stage_1:                              │
     │    │   type: extraction                    │
     │    │   subagents: [batch_1, batch_2]       │
     │    │   outputs:                            │
     │    │     - file: _batch_1.yaml             │
     │    │       hash: "..."                     │
     │    │     - file: _batch_2.yaml             │
     │    │       hash: "..."                     │
     │    │                                       │
     │    │ stage_2:                              │
     │    │   type: aggregation                   │
     │    │   processor: script                   │
     │    │   inputs_from: stage_1                │
     │    │   output:                             │
     │    │     file: _synthesis_field.yaml       │
     │    │     hash: "..."                       │
     │    └───────────────────────────────────────┘
     │
     └──► SUBAGENT FINAL (Report Generation)
               │
               ▼
          Uses chain manifest to trace all data
```

---

## Pattern 6: ERROR-RECOVERY HANDOVER

```yaml
# When subagent fails or times out

handover:
  task_id: "paper_analysis_02-KG"
  status: "PARTIAL"

  completed:
    chunks_read: [1, 2, 3]
    chunks_evidence:
      1: {start: "...", end: "...", hash: "..."}
      2: {start: "...", end: "...", hash: "..."}
      3: {start: "...", end: "...", hash: "..."}
    extractions_so_far:
      entity_types: [{name: "Endurant", ...}, ...]

  incomplete:
    chunks_remaining: [4, 5, 6]
    reason: "timeout"

  recovery:
    resume_from: 4
    preserve_work: true
    output_partial: "03-working/_partial_02-KG.yaml"

# Orchestrator can spawn new subagent with:
resume_task:
  base_on: "_partial_02-KG.yaml"
  start_chunk: 4
  append_to_existing: true
```

---

## Pattern 7: CONTEXT INJECTION PROTOCOL (CIP)

Wie übergeben wir KONTEXT ohne Token zu verschwenden?

```
┌─────────────────────────────────────────────────────────────────────┐
│                    CONTEXT INJECTION LEVELS                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ LEVEL 1: ESSENTIAL (always include)                                 │
│ ├─ research_question: "What entity types..."                       │
│ ├─ field_to_extract: "entity_types"                                │
│ └─ citation_format: "Paper-ID (Chunk N:Line-Line)"                 │
│                                                 ~200 tokens         │
│                                                                     │
│ LEVEL 2: DOMAIN (include for domain-specific tasks)                │
│ ├─ domain: "ontology"                                              │
│ ├─ key_vocabulary: {Endurant: "...", Perdurant: "..."}            │
│ └─ extraction_examples: [...]                                       │
│                                                 ~500 tokens         │
│                                                                     │
│ LEVEL 3: METHODOLOGY (include for complex tasks)                   │
│ ├─ step_by_step_instructions: [...]                                │
│ ├─ quality_criteria: [...]                                         │
│ └─ anti_hallucination_rules: [...]                                 │
│                                                 ~1500 tokens        │
│                                                                     │
│ LEVEL 4: FULL (for first-time tasks)                               │
│ ├─ complete_schema: {...}                                          │
│ ├─ all_examples: [...]                                             │
│ └─ complete_validation_rules: [...]                                │
│                                                 ~3000 tokens        │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

SELECTION RULE:
- First task in batch: LEVEL 4
- Subsequent tasks same type: LEVEL 2
- Recovery tasks: LEVEL 3
- Simple extraction: LEVEL 1
```

---

## Implementation: Handover Manager

```python
# handover_manager.py

class HandoverManager:
    """Manages structured handovers between orchestrator and subagents."""

    def create_ticket(
        self,
        task_type: str,
        input_files: List[Path],
        output_spec: dict
    ) -> HandoverTicket:
        """Create handover ticket with pre-computed hashes."""

        ticket = HandoverTicket(
            task_id=generate_task_id(),
            created_at=datetime.now(),
            input_manifest=self._build_input_manifest(input_files),
            output_contract=output_spec
        )

        # Save ticket for later verification
        self._save_ticket(ticket)
        return ticket

    def generate_prompt_with_ticket(
        self,
        ticket: HandoverTicket,
        context_level: int = 2
    ) -> str:
        """Generate subagent prompt that includes ticket requirements."""

        prompt = f"""
# Task: {ticket.task_id}

## HANDOVER TICKET

You are receiving a structured task. Follow this exactly.

### INPUT MANIFEST

{self._format_input_manifest(ticket.input_manifest)}

### OUTPUT CONTRACT

{self._format_output_contract(ticket.output_contract)}

### COMPLETION RECEIPT

After completing the task, you MUST fill out this receipt:

```yaml
completion_receipt:
  task_id: "{ticket.task_id}"
  completed_at: "<timestamp>"
  files_read:
    # For each file in INPUT MANIFEST:
    - path: "<path>"
      hash_verified: true/false  # Did hash match expected?
      lines_counted: <N>
  output_written:
    file: "<output path>"
    hash: "<computed hash of your output>"
```

Write this receipt to: `03-working/_receipt_{ticket.task_id}.yaml`

---

{self._get_context_for_level(context_level)}
"""
        return prompt

    def verify_completion(
        self,
        ticket: HandoverTicket,
        receipt_path: Path
    ) -> VerificationResult:
        """Verify subagent completed task correctly."""

        receipt = yaml.safe_load(receipt_path.read_text())

        # Verify input hashes
        for input_file in ticket.input_manifest.files:
            reported = next(
                (f for f in receipt['files_read'] if f['path'] == input_file.path),
                None
            )
            if not reported or not reported['hash_verified']:
                return VerificationResult(
                    passed=False,
                    reason=f"Hash mismatch for {input_file.path}"
                )

        # Verify output exists and matches schema
        output_path = Path(receipt['output_written']['file'])
        if not output_path.exists():
            return VerificationResult(
                passed=False,
                reason="Output file not found"
            )

        # Validate output schema
        if not self._validate_output_schema(output_path, ticket.output_contract):
            return VerificationResult(
                passed=False,
                reason="Output schema validation failed"
            )

        return VerificationResult(passed=True)
```

---

## Quick Reference: Handover Checklist

### Orchestrator → Subagent

- [ ] Compute hashes of ALL input files
- [ ] Include hashes in INPUT MANIFEST
- [ ] Specify EXACT output format
- [ ] Define validation rules
- [ ] Request COMPLETION RECEIPT

### Subagent → Orchestrator

- [ ] Verify input file hashes while reading
- [ ] Report any hash mismatches
- [ ] Follow OUTPUT CONTRACT exactly
- [ ] Include all required fields
- [ ] Write COMPLETION RECEIPT

### Post-Handover Verification

- [ ] Check receipt exists
- [ ] Verify input hashes match
- [ ] Validate output schema
- [ ] Spot-check citations
- [ ] Compute output hash for chain

---

## Summary: ULTRASEARCH Handover Principles

1. **TICKET-BASED**: Every handover has a structured ticket
2. **HASH-VERIFIED**: Input and output hashes for integrity
3. **CHAIN-PRESERVED**: Citations traceable through all stages
4. **RECEIPT-CONFIRMED**: Subagent proves completion
5. **CONTEXT-OPTIMIZED**: Right level of context injection
6. **RECOVERY-ENABLED**: Partial work preserved for retry

**Result**: Zero-loss data transfer with full traceability.

---

**Version**: 1.0 (2025-12-28)
**Pattern Source**: Research Pipeline optimization
**Goal**: HIGH QUALITY DATA TRANSFER through structured handover protocols
