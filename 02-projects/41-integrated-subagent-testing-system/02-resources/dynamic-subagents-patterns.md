# Dynamic Subagents Patterns - Research Pipeline Analysis

**Source**: Subagent analysis of `03-skills/research-pipeline/scripts/dynamic-subagents/`
**Agent ID**: a063ba9
**Date**: 2026-01-07

---

## 1. Domain-Specific Subagent Factory

**File**: `dynamic_subagent_factory.py`

### Domain Detection + Persona Assignment
```python
DOMAIN_PERSONAS = {
    "technical": {
        "name": "Technical Analyst",
        "expertise": ["architecture", "implementation", "code patterns"],
        "focus": "How things work technically"
    },
    "business": {
        "name": "Business Analyst",
        "expertise": ["strategy", "market", "operations"],
        "focus": "Why decisions matter commercially"
    },
    "research": {
        "name": "Research Synthesizer",
        "expertise": ["literature", "methodology", "evidence"],
        "focus": "What the evidence shows"
    }
}

def create_subagent(domain: str, task: dict) -> dict:
    """Factory method to create domain-specific subagent config."""
    persona = DOMAIN_PERSONAS.get(domain, DOMAIN_PERSONAS["research"])

    return {
        "persona": persona,
        "task": task,
        "context_level": determine_context_level(task),
        "output_contract": generate_output_contract(task)
    }
```

### Key Insight
Subagents get **specialized personas** based on domain, improving output quality through role-appropriate framing.

---

## 2. Handover Ticket Structure

**File**: `handover_manager.py`

### Three-Part Ticket System

#### INPUT MANIFEST
```yaml
input_manifest:
  sources:
    - path: "path/to/source"
      token_count: 15000
      hash: "abc123..."
  total_tokens: 45000
  methodology: "research-synthesis"
  constraints:
    - "Must cite line numbers"
    - "3-point evidence required"
```

#### OUTPUT CONTRACT
```yaml
output_contract:
  format: "structured-findings"
  required_sections:
    - summary
    - key_findings
    - evidence_table
    - recommendations
  verification:
    quote_rate: 0.90
    evidence_points: 3
```

#### COMPLETION RECEIPT
```yaml
completion_receipt:
  status: "complete|partial|failed"
  outputs:
    - file: "findings.md"
      hash: "def456..."
  metrics:
    quotes_verified: 45
    quotes_total: 48
    pass_rate: 0.9375
  handback_notes: "Optional context for orchestrator"
```

### Handover Flow
```
Orchestrator → INPUT MANIFEST → Subagent
                                   ↓
                              (does work)
                                   ↓
Orchestrator ← COMPLETION RECEIPT ← Subagent
```

---

## 3. Forced Reading Contract

**File**: `forced_reading_contract.py`

### 3-Point Evidence Pattern
```python
@dataclass
class ForcedReadingContract:
    """Contract ensuring subagent actually reads sources."""

    evidence_requirements: List[EvidenceRequirement] = field(default_factory=lambda: [
        EvidenceRequirement(section="start", description="Quote from first 20% of source"),
        EvidenceRequirement(section="middle", description="Quote from 40-60% of source"),
        EvidenceRequirement(section="end", description="Quote from last 20% of source")
    ])

    hash_verification: bool = True  # Require source hash in output
    spot_check_count: int = 3       # Random quotes to verify
```

### Hash Verification
```python
def verify_source_read(output: dict, sources: List[Source]) -> bool:
    """Verify subagent actually processed the sources."""

    # Check 1: Hash matches
    for source in sources:
        claimed_hash = output.get("source_hashes", {}).get(source.path)
        if claimed_hash != source.hash:
            return False

    # Check 2: Evidence points exist
    evidence = output.get("evidence", [])
    sections = {e["section"] for e in evidence}
    if sections != {"start", "middle", "end"}:
        return False

    # Check 3: Spot check quotes
    for quote in random.sample(evidence, min(3, len(evidence))):
        if not verify_quote_in_source(quote, sources):
            return False

    return True
```

---

## 4. Context Injection Levels

**File**: `dynamic_subagent_factory.py`

### 4 Levels of Context
```python
CONTEXT_LEVELS = {
    1: {
        "name": "minimal",
        "includes": ["task_only"],
        "use_when": "Simple, isolated tasks"
    },
    2: {
        "name": "standard",
        "includes": ["task", "source_summaries", "methodology"],
        "use_when": "Normal analysis tasks"
    },
    3: {
        "name": "enhanced",
        "includes": ["task", "sources", "methodology", "prior_findings"],
        "use_when": "Synthesis requiring cross-reference"
    },
    4: {
        "name": "full",
        "includes": ["task", "sources", "methodology", "prior_findings", "orchestrator_context"],
        "use_when": "Complex multi-step analysis"
    }
}

def determine_context_level(task: dict) -> int:
    """Determine appropriate context level for task."""
    if task.get("requires_synthesis"):
        return 4 if task.get("prior_findings") else 3
    elif task.get("source_count", 0) > 5:
        return 2
    else:
        return 1
```

---

## 5. Subagent Verification

**File**: `verify_subagent_reading.py`

### Verification Methods

#### Quote Spot Checks
```python
def spot_check_quotes(output: dict, sources: List[Source], count: int = 3) -> float:
    """Randomly sample quotes and verify they exist in sources."""
    quotes = output.get("quotes", [])
    sample = random.sample(quotes, min(count, len(quotes)))

    verified = sum(1 for q in sample if find_quote_in_sources(q, sources))
    return verified / len(sample) if sample else 0
```

#### Section Coverage
```python
def verify_section_coverage(output: dict, sources: List[Source]) -> bool:
    """Verify evidence covers all required sections."""
    for source in sources:
        evidence = [e for e in output.get("evidence", []) if e["source"] == source.path]
        sections = {e["section"] for e in evidence}

        if not sections >= {"start", "middle", "end"}:
            return False

    return True
```

#### Hash Chain
```python
def verify_hash_chain(output: dict, sources: List[Source]) -> bool:
    """Verify subagent's claimed source hashes match actual sources."""
    claimed_hashes = output.get("source_hashes", {})

    for source in sources:
        if claimed_hashes.get(source.path) != source.hash:
            return False

    return True
```

---

## 6. Ultrasearch Handover Patterns

**File**: `ULTRASEARCH_HANDOVER_PATTERNS.md`

### Key Patterns

1. **Explicit Boundaries**: Clear start/end markers for subagent scope
2. **No Assumptions**: Subagent must not assume prior context
3. **Atomic Tasks**: Each subagent gets complete, self-contained task
4. **Verification Built-In**: Output format includes verification fields

### Handover Template
```markdown
## SUBAGENT TASK: {task_name}

### INPUT MANIFEST
{sources with hashes and token counts}

### YOUR TASK
{specific instructions}

### OUTPUT CONTRACT
{required format and fields}

### VERIFICATION REQUIREMENTS
- Quote at least 3 evidence points per finding
- Include source hash in output
- Cite line numbers for all quotes
```

---

## Key Patterns for Project 41

1. **Domain personas** improve subagent output quality
2. **3-part handover tickets** ensure clean orchestration
3. **Hash verification** prevents source confusion
4. **4 context levels** optimize token usage
5. **Spot check verification** catches lazy/hallucinated outputs

---

*Generated by dynamic-subagents subagent analysis*
