---
project_id: "10-dynamic-subagent-research"
project_path: "02-projects/10-dynamic-subagent-research"
generated: "2025-12-28"
schema_version: "2.3"
---

# Extraction Guide: Dynamic Subagent Handover Patterns

**Purpose**: Ensure consistent extraction quality for handover patterns research.

---

## Format Rules

### Data Types

| Type | When to Use | Format |
|------|-------------|--------|
| **Array of objects** | Patterns, implementations | `[{name: "X", mechanism: "Y", source: "Chunk 2:45"}]` |
| **Array of strings** | Simple lists | `["Item 1", "Item 2"]` |
| **String** | Single value, paragraph | `"Description here"` |
| **Enum** | Controlled vocabulary | `"verification"` (not variations) |
| **null** | Not applicable | `null` |

### Empty vs N/A

| Situation | Use |
|-----------|-----|
| Paper doesn't discuss this topic | `"N/A - not discussed"` |
| Searched but nothing found | `"N/A - no relevant content found"` |
| Field not applicable | `null` |

**Never leave undefined** - always explicit about why empty.

---

## Extraction Quality

### DO

- Use exact terminology from paper
- Include chunk:line for every extraction: `(Chunk 3:127-134)`
- Quote pattern definitions verbatim
- Be specific: `"3-layer verification"` not `"multi-step"`
- Standardize to controlled vocabulary

### DON'T

- Paraphrase when exact quote is better
- Merge distinct patterns into one
- Infer what paper doesn't state
- Use generic: `"discusses various protocols"`
- Forget chunk:line references

---

## Controlled Vocabulary

### mechanism_type (ENUM)

| Value | Use When Paper Says |
|-------|---------------------|
| `verification` | validates, checks, confirms, verifies, audits |
| `enforcement` | enforces, requires, mandates, ensures, compels |
| `detection` | detects, identifies, recognizes, spots, finds |
| `prevention` | prevents, blocks, prohibits, stops, guards against |

**Rule**: Choose ONE. If mechanism does multiple things, use the PRIMARY purpose.

### integration_point (ENUM)

| Value | Use When |
|-------|----------|
| `prompt_generation` | Before/during subagent prompt creation |
| `execution` | During subagent task execution |
| `verification` | After execution, before output acceptance |
| `handover` | During transfer between components/agents |

### Protocol/Pattern Names

| Paper Uses | Standardize To |
|------------|----------------|
| "A2A", "Agent-to-Agent", "agent2agent" | `A2A` |
| "LACP", "LLM Agent Communication Protocol" | `LACP` |
| "MCP", "Model Context Protocol" | `MCP` |
| "SEMAP", "Software Engineering for Multi-Agent" | `SEMAP` |
| "TalkHier", "hierarchical communication" | `TalkHier` |
| "context window", "context budget" | `context window` |
| "hallucination", "fabrication", "confabulation" | `hallucination` |

---

## Confidence Levels

| Level | When to Use |
|-------|-------------|
| **high** | Explicit statement, direct quote available |
| **medium** | Clear implication, consistent with context |
| **low** | Inference, interpretation, ambiguous |

Flag low confidence: `[LOW CONFIDENCE: reason]`

---

## Field-Specific Instructions

### Field: `pattern_definition`

**Definition**: A complete definition of a handover/coordination pattern including name, purpose, and mechanism.

**Format**: Array of objects

**Priority**: HIGH

**Example GOOD**:
```yaml
pattern_definition:
  - name: "Structured Message Protocol"
    purpose: "Ensure inter-agent messages contain all required fields"
    mechanism: "JSON schema validation at sender/receiver endpoints"
    source: "Chunk 3:127-145"
    quote: "SMP enforces structured communication via schema validation..."
    confidence: "high"
```

**Example BAD**:
```yaml
pattern_definition:
  - "uses structured messages"  # Missing name, purpose, mechanism
  - "some protocol for communication"  # Too vague, no source
```

---

### Field: `mechanism_type`

**Definition**: The category of mechanism (verification, enforcement, detection, prevention).

**Format**: Enum string

**Priority**: HIGH

**Example GOOD**:
```yaml
mechanism_type: "verification"
# Because paper states: "validates output against schema before accepting"
```

**Example BAD**:
```yaml
mechanism_type: "checks stuff"  # Not a valid enum value
mechanism_type: "verification and detection"  # Pick ONE primary
```

---

### Field: `failure_mode`

**Definition**: What happens when the pattern is violated or fails.

**Format**: String

**Priority**: MEDIUM

**Example GOOD**:
```yaml
failure_mode: "Message rejected with error code; sender notified to retry with corrected format"
source: "Chunk 4:89-95"
```

**Example BAD**:
```yaml
failure_mode: "doesn't work"  # Not specific
failure_mode: ""  # Missing "N/A - not discussed" if not in paper
```

---

### Field: `implementation_detail`

**Definition**: Concrete code or system implementation (function, class, data structure, API).

**Format**: Array of objects

**Priority**: HIGH

**Example GOOD**:
```yaml
implementation_detail:
  - type: "function"
    name: "validate_message_schema"
    description: "Validates incoming message against protocol-specific JSON schema"
    source: "Chunk 2:201-215"
    quote: "def validate_message_schema(msg: Message) -> ValidationResult"
```

**Example BAD**:
```yaml
implementation_detail:
  - "they implemented validation"  # No specifics
  - "uses Python"  # Too generic
```

---

### Field: `integration_point`

**Definition**: Where in the agent pipeline/workflow this pattern is applied.

**Format**: Enum string

**Priority**: HIGH

**Example GOOD**:
```yaml
integration_point: "handover"
note: "Applied at agent-to-agent message boundaries (Chunk 5:67)"
```

**Example BAD**:
```yaml
integration_point: "during the process"  # Not enum value
integration_point: "everywhere"  # Be specific
```

---

### Field: `quality_metric`

**Definition**: Measurable metrics the pattern affects (accuracy, latency, success rate).

**Format**: Array of objects

**Priority**: HIGH

**Example GOOD**:
```yaml
quality_metric:
  - metric: "Message acceptance rate"
    value: "94.2%"
    baseline: "78.1% without protocol"
    source: "Chunk 6:145-152"
  - metric: "Information loss"
    value: "-35% vs baseline"
    source: "Chunk 6:160"
```

**Example BAD**:
```yaml
quality_metric:
  - "improved performance"  # No numbers
  - "better than before"  # Not measurable
```

---

### Field: `limitation`

**Definition**: Known constraints, drawbacks, or failure conditions of the pattern.

**Format**: Array of strings

**Priority**: MEDIUM

**Example GOOD**:
```yaml
limitation:
  - "Adds ~200ms latency per message due to validation overhead (Chunk 7:89)"
  - "Requires all agents to implement same schema version (Chunk 7:102)"
```

**Example BAD**:
```yaml
limitation:
  - "has some limitations"  # What are they?
```

---

### Field: `related_pattern`

**Definition**: Other patterns this one depends on, conflicts with, or complements.

**Format**: Array of objects

**Priority**: LOW

**Example GOOD**:
```yaml
related_pattern:
  - name: "Hash-Chain Verification"
    relationship: "dependency"
    note: "SMP messages include hash for chain verification (Chunk 3:178)"
  - name: "Retry Protocol"
    relationship: "complement"
    note: "Used together for fault tolerance"
```

---

## Pattern Categories to Watch For

Based on our ULTRASEARCH patterns, look for similar concepts:

| Our Pattern | Look For In Literature |
|-------------|----------------------|
| Ticket-based Handover | Structured message passing, contracts, receipts |
| Hash-chain Verification | Integrity checks, content hashing, provenance |
| Citation Chain Preservation | Source tracking, traceability, audit trails |
| 3-Point Evidence | Anti-skimming, sampling verification, read proof |
| Context Injection Protocol | Token budgets, context levels, selective loading |
| Error Recovery | Retry patterns, partial work preservation, checkpoints |

---

## Validation Checklist

Before completing analysis:

- [ ] All HIGH priority fields have extraction OR explicit N/A
- [ ] Every extraction has chunk:line reference
- [ ] mechanism_type and integration_point use exact enum values
- [ ] Quality metrics include numbers where paper provides them
- [ ] Limitations are specific, not generic
- [ ] Pattern names use standardized vocabulary
- [ ] No empty fields without N/A explanation

---

**Version**: 1.0
**Generated**: 2025-12-28
