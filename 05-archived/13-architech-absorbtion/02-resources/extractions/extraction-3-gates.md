# Extraction 3: Quality Gates Framework

**Source System**: Architech v2 (mutagent-obsidian)
**Extraction Date**: 2026-01-01
**Pattern ID**: GATE-001
**Spawns**: Project 18 (Quality Gate Implementation)

---

## Executive Summary

The Architech Quality Gates framework provides a comprehensive validation system that operates at multiple levels: **manual quality gates** for human-reviewed checkpoints, and **evaluation checklists** for automated trace validation. The system enforces a **3-phase execution model** (Activation, Execution, Completion), uses **evidence-based validation** with an anti-bullshitting protocol, and employs a **weighted scoring formula** to produce verdicts.

---

## Part 1: Checklist Entity Type Definition

### 1.1 Complete Frontmatter Schema

```yaml
---
# === MANUAL CHECKLIST FRONTMATTER ===
name: {checklist-id}                    # Kebab-case identifier
description: {WHAT this checklist validates}
when: {WHEN TO USE - the checkpoint/transition}
type: manual                            # manual | evaluation
checkpoint: {phase-transition|before-commit|pre-deployment|etc}
required: true|false                    # Is completion mandatory?
dependencies: [~shortcuts]              # Other entities to load first
created: YYYY-MM-DD
updated: YYYY-MM-DD
author: "Name | agent-name"
version: X.Y.Z
---

# === EVALUATION CHECKLIST FRONTMATTER ===
---
name: {executable-id}-checklist         # Pattern: {source}-checklist
description: Evaluation checklist for {executable-type} {executable-id}
when: Validating {executable-id} execution via diagnose-trace
type: evaluation                        # Marks as auto-derived
source_entity: ~{type}:{id}             # Links to source executable
source_type: agent|skill|task|workflow  # What kind of executable
checkpoint: activation|execution|completion
required: true
created: YYYY-MM-DD
updated: YYYY-MM-DD
author: "Name | agent-name"
version: X.Y.Z
derived_by: ~create-evaluation-checklist  # Creation method
---
```

### 1.2 Entity Definition Metadata

```yaml
# From 07-checklist.md entity definition
name: checklist
description: Quality gates and validation checklists for specific checkpoints or transitions
when: Need validation gates, quality checkpoints, or structured verification at transitions
folder_pattern: "07-checklists"
folder_purpose: Quality gates and validation checklists
location_pattern: "*/07-checklists/**/*.md"
scanned: false
category: validation
version: 2.1.0
```

### 1.3 Two Checklist Types

| Type | Purpose | Creation | Validation |
|------|---------|----------|------------|
| **Manual** | Human-reviewed quality gates at transitions | Human authoring | Human review |
| **Evaluation** | Trace validation against expected behavior | `~create-evaluation-checklist` skill | `~diagnose-trace` skill |

**Manual Checklist Examples**:
- `framework-change-checklist` - Pre-commit validation
- `domain-creation-validation` - Phase transition gate
- `release-checklist` - Pre-deployment validation

**Evaluation Checklist Examples**:
- `meta-architect-checklist` - Agent activation validation
- `create-agent-checklist` - Task execution validation
- `mental-models-checklist` - Skill workflow validation

---

## Part 2: Decision States Framework (PASS/CONCERNS/FAIL/WAIVED)

### 2.1 Core Decision States

The Architech framework uses a **four-state decision model**:

```markdown
**STATUS**: PASS | CONCERNS | FAIL | WAIVED
```

| State | Symbol | Meaning | When to Use |
|-------|--------|---------|-------------|
| **PASS** | ✅ | All criteria met, validation successful | Requirements clearly satisfied |
| **CONCERNS** | ⚠️ | Functional but with warnings | Some gaps, needs monitoring |
| **FAIL** | ❌ | Critical criteria not met, blocks progress | Requirements missing or violated |
| **WAIVED** | ⏭️ | Intentionally skipped with justification | N/A for context, documented reason |

### 2.2 Evidence Format Template

Every decision MUST include evidence (ASV-015 Anti-Bullshitting):

```markdown
**STATUS**: ✅ PASS / ⚠️ CONCERNS / ❌ FAIL
**CLAIM**: "Specific assertion about system state"
**EVIDENCE**: "Tool output or verification result"
**SOURCE**: "Tool:Command executed at timestamp"
**VALIDATION_METHOD**: "Direct Tool | Obsidian Vault | Git Status"
**DOMAIN_CONTEXT**: "domain-level: {domain_id} | system-level: {system_id}"
**CONFIDENCE**: "High (direct) / Medium (inferred) / Low (partial)"
```

### 2.3 Categorical Validation (Manual Checklists)

For comprehensive checklists like DoD or PO Master:

```markdown
| Category                        | Status | Issues |
| ------------------------------- | ------ | ------ |
| 1. Requirements Met             | PASS   |        |
| 2. Coding Standards & Structure | PARTIAL| Missing tests |
| 3. Testing & Quality Assurance  | FAIL   | No unit tests |
| 4. Documentation                | PASS   |        |
```

**Status Values**:
- `PASS` (90%+ complete)
- `PARTIAL` (60-89% complete)
- `FAIL` (<60% complete)
- `N/A` (Not applicable to context)

### 2.4 Final Verdicts

```markdown
**Final Assessment:**
- COMPLETE: The story meets all DoD criteria and is ready for review
- NEEDS WORK: The story requires additional work (see issues)
- BLOCKED: External dependencies prevent completion (specify what's needed)
```

For PO Checklists:
```markdown
**Final Decision:**
- READY FOR ARCHITECT: Requirements comprehensive, ready for technical design
- NEEDS REFINEMENT: Requires additional work to address deficiencies
```

---

## Part 3: Scoring Formula

### 3.1 Default Behavioral Specification Scoring

From `default-behavioral-spec.md`:

```
Overall Score = (Activation * 0.3) + (Execution * 0.4) + (Completion * 0.3)
```

**Weight Distribution**:
- **Activation Phase**: 30% weight
- **Execution Phase**: 40% weight (most important)
- **Completion Phase**: 30% weight

### 3.2 Phase-Specific Scoring

#### Activation Phase Scoring
```yaml
Scoring:
- All required steps present: 100%
- Missing context build: 75%
- Missing executable load: 0% (FAIL)
```

#### Execution Phase Scoring
```yaml
Scoring:
- All metrics meet threshold: 100%
- Each metric below threshold: -15 points
- Minimum: 40%

Context Modifiers:
- Documentation edits (.md files): Lower thresholds acceptable (30%)
- Configuration edits (.json, .yaml, .toml): Normal thresholds apply
- Code edits (.py, .js, .ts, etc.): Higher thresholds expected (70%)
```

#### Completion Phase Scoring
```yaml
Scoring:
- All checks pass: 100%
- Errors present: -20 points
- Pending todos: -10 points
- No clean exit: -5 points
```

### 3.3 Verdicts Based on Score

| Score Range | Verdict |
|-------------|---------|
| >= 95 | EXEMPLARY |
| >= 80 | COMPLIANT |
| >= 60 | MOSTLY_COMPLIANT |
| >= 40 | NEEDS_IMPROVEMENT |
| < 40 | FAILED |

### 3.4 Behavioral Metrics (Execution Phase)

| Metric | Description | Threshold | Severity |
|--------|-------------|-----------|----------|
| `read_before_edit` | Edits preceded by Read within 3 events | >= 50% | WARN if below |
| `verify_after_edit` | Edits followed by Bash/Read within 3 events | >= 50% | WARN if below |
| `todo_usage` | TodoWrite calls for multi-step tasks | >= 1 | WARN if 0 |

---

## Part 4: Evidence-Based Validation System

### 4.1 ASV-015: Claims Evidence Enforcer

**Philosophy**: "Every diagnostic claim requires verifiable evidence"

```yaml
# From agent-sequence-validator.yaml
ASV-015:
  name: "Claims Evidence Enforcer - Anti-Bullshitting System"
  phase: diagnostic-claims
  enforcement: BLOCKING
  description: "Enforces evidence collection for all diagnostic assertions"

  claim_patterns:
    - "exists"
    - "missing"
    - "loaded"
    - "active"
    - "compliant"
    - "detected"
    - "available"
    - "validated"
    - "operational"

  validation_logic: |
    claim = get_diagnostic_claim()
    FOR pattern IN claim_patterns:
      IF contains(claim, pattern):
        evidence = get_claim_evidence(claim)
        IF NOT evidence.verification_tool_executed:
          BLOCK claim
          ERROR "Evidence required for claim: {claim}"
          REQUIRE verification_tool_execution()
        IF NOT evidence.source_citation:
          BLOCK claim
          ERROR "Source citation required for: {claim}"
        IF NOT evidence.confidence_level:
          WARNING "Confidence level missing for: {claim}"
    RETURN PASS
```

### 4.2 ASV-016: Verification-On-Claim Protocol

```yaml
ASV-016:
  name: "Verification-On-Claim Protocol - Domain-Aware Evidence"
  phase: diagnostic-status
  enforcement: WARNING

  diagnostic_operations:
    - "*status"
    - "*asv-status"
    - "*validate-system"
    - "domain status check"
    - "system state assessment"

  evidence_requirements:
    domain_existence:
      primary: "ls context-store/{domain}/"
      fallback: "Read structure-map.yaml"
      confidence: "High (direct)"

    vault_integrity:
      primary: "git status in context-store/"
      fallback: "Check .obsidian/ directory"
      confidence: "High (direct)"

    domain_context:
      primary: "Read context-store/{domain}/domain-context.md"
      fallback: "Grep loaded files for {domain}/ paths"
      confidence: "Medium (file-based)"
```

### 4.3 Evidence Collection Methods

| Claim Type | Primary Tool | Fallback | Confidence |
|------------|--------------|----------|------------|
| Domain existence | `ls context-store/{domain}/` | Read structure-map.yaml | High |
| Vault integrity | `git status` | Check .obsidian/ | High |
| Domain context | Read domain-context.md | Grep loaded files | Medium |
| Wikilink resolution | Extract + verify targets | Manual checking | Medium |

### 4.4 Good vs Bad Evidence Examples

**BAD (No Evidence)**:
```markdown
CRITICAL FAILURE: Strategy domain is broken!
```

**GOOD (With Evidence)**:
```markdown
**STATUS**: ✅ PASS
**CLAIM**: "Strategy domain context is fully loaded"
**EVIDENCE**:
  - Read context-store/01-strategy/venture-context.md (successful)
  - Read context-store/01-strategy/sessions/session-1.md (successful)
  - Loaded rule: ~rule:strategy:hypothesis-validation
**SOURCE**: Read tool executed 2025-10-18 14:23:00
**VALIDATION_METHOD**: Direct Tool (Read)
**DOMAIN_CONTEXT**: domain-level: strategy
**CONFIDENCE**: High (direct verification)
```

---

## Part 5: Three-Phase Model (Activation/Execution/Completion)

### 5.1 Phase Overview

```
┌─────────────────────────────────────────────────────────────────┐
│              EVALUATION CHECKLIST PIPELINE                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  PHASE 1: ACTIVATION                                            │
│  ─────────────────────                                          │
│  - Scripts in activation instructions executed                  │
│  - Dependencies resolved and loaded                             │
│  - Context established                                          │
│  - Weight: 30%                                                  │
│                                                                 │
│  PHASE 2: EXECUTION                                             │
│  ─────────────────────                                          │
│  - Main workflow steps followed                                 │
│  - Tool operations performed correctly                          │
│  - Read-before-edit patterns followed                           │
│  - Weight: 40%                                                  │
│                                                                 │
│  PHASE 3: COMPLETION                                            │
│  ─────────────────────                                          │
│  - Expected outputs generated                                   │
│  - State changes persisted                                      │
│  - Clean exit achieved                                          │
│  - Weight: 30%                                                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 5.2 Activation Phase Details

**Purpose**: Ensure executable is properly initialized with all required context.

**Default Checks**:
| Step | Pattern | Required | Severity |
|------|---------|----------|----------|
| Load executable | `shortcut_resolver.py ~{id}` | Yes | FAIL if missing |
| Build context | `build_shortcut_registry.py` OR Read definitions | Yes | WARN if missing |

**Agent-Specific Example** (meta-architect):
```markdown
## Activation Phase
- [ ] Ran `shortcut_resolver.py ~meta-architect --content`
- [ ] Ran `build_shortcut_registry.py --agent meta-architect --mode plan`
- [ ] Ran `build_entity_definitions.py`
- [ ] Loaded `~meta-map` via shortcut resolver
```

**Task-Specific Example** (create-agent):
```markdown
## Step 0: Prerequisites
- [ ] Loaded `~entity:agent` definition
- [ ] Identified target layer (meta/system/domain)
```

### 5.3 Execution Phase Details

**Purpose**: Validate main workflow proceeds correctly.

**Default Behavioral Metrics**:
| Metric | Description | Threshold |
|--------|-------------|-----------|
| `read_before_edit` | Edits preceded by Read | >= 50% |
| `verify_after_edit` | Edits followed by verification | >= 50% |
| `todo_usage` | TodoWrite for multi-step | >= 1 |

**Agent-Specific Example**:
```markdown
## Execution Phase

### Context Loading
- [ ] Entity definitions available (12 types)
- [ ] Shortcut registry populated
- [ ] Agent capabilities loaded

### Output Display
- [ ] Displayed activation header with agent name
- [ ] Displayed `~help` menu with commands
- [ ] Ready for user interaction
```

**Task-Specific Example**:
```markdown
## Step 1: Gather Information
- [ ] Collected agent name
- [ ] Collected agent description
- [ ] Collected agent capabilities
- [ ] Identified dependencies

## Step 2: Create Agent File
- [ ] Created agent file at correct path
- [ ] Frontmatter includes all required fields
- [ ] Activation instructions present
```

### 5.4 Completion Phase Details

**Purpose**: Verify expected outcomes achieved.

**Default Checks**:
| Check | Description | Threshold | Severity |
|-------|-------------|-----------|----------|
| `no_errors` | Events with non-empty stderr | 0 | WARN if any |
| `todos_completed` | Pending items in final TodoWrite | 0 | WARN if any |
| `clean_exit` | Session ends with Stop event | Yes | INFO if missing |

**Agent-Specific Example**:
```markdown
## Completion Phase
- [ ] Agent persona active
- [ ] All dependencies resolved
- [ ] No error messages in activation
```

**Task-Specific Example**:
```markdown
## Step 3: Integration
- [ ] Updated shortcut registry (if applicable)
- [ ] Verified wikilinks resolve
- [ ] Displayed success confirmation
```

### 5.5 Derivation Rules by Entity Type

**From Agent**:
- **Activation Phase**: Scripts in activation instructions
- **Execution Phase**: Capabilities and expected tool usage
- **Completion Phase**: Expected outputs and state changes

**From Skill**:
- **Activation Phase**: Trigger conditions met
- **Execution Phase**: Workflow steps followed
- **Completion Phase**: Expected artifacts created

**From Task**:
- **Step 0**: Prerequisites and dependency loads
- **Steps 1-N**: Each step's expected actions
- **Completion**: Success criteria and outputs

**From Workflow**:
- **Phase Gates**: Quality checks between phases
- **Agent Handoffs**: Correct delegation sequence
- **Completion**: All phases completed, artifacts created

---

## Part 6: ASV Integration (Agent Sequence Validator)

### 6.1 Core Validation Rules

| Rule | Name | Phase | Enforcement |
|------|------|-------|-------------|
| ASV-001 | Fast Init | pre-activation | BLOCKING |
| ASV-002 | Operation Interceptor | pre-operation | BLOCKING |
| ASV-003 | Handoff Preservation | pre-handoff | BLOCKING |
| ASV-004 | Context Currency | during-operation | WARNING |
| ASV-005 | Memory Updates | post-completion | BLOCKING |
| ASV-006 | Domain Rules | pre-activation | BLOCKING |
| ASV-010 | Domain Switch | domain-switch | BLOCKING |
| ASV-015 | Claims Evidence | diagnostic-claims | BLOCKING |
| ASV-016 | Verification Protocol | diagnostic-status | WARNING |
| ASV-017 | Vault Integrity | during-operation | WARNING |
| ASV-018 | Git Compliance | session-start/end | WARNING |

### 6.2 Enforcement Modes

```yaml
enforcement:
  default_mode: "strict"  # strict | permissive | adaptive

  strict_mode:
    description: "All violations are blocking"
    blocking_rules: [ASV-001, ASV-002, ASV-003, ASV-005, ASV-006, ASV-010, ASV-015]
    warning_rules: [ASV-004, ASV-016, ASV-017, ASV-018]
    bypass_allowed: false

  permissive_mode:
    description: "Warnings but allow continuation - testing only"
    blocking_rules: [ASV-001, ASV-003, ASV-015]
    warning_rules: [ASV-002, ASV-004, ASV-005, ASV-006, ASV-010, ASV-016, ASV-017, ASV-018]
    bypass_allowed: true
```

### 6.3 Validation Logic Pattern

```yaml
validation_logic: |
  # INTERCEPT operation before execution
  operation = get_current_operation()
  required_files = operation_context_map[operation].must_load

  # FORCE LOAD each required file
  FOR file IN required_files:
    IF file.startswith("~"):
      resolved = resolve_shortcut(file)
      IF NOT loaded(resolved):
        LOG "Lazy loading: {file} -> {resolved}"
        BLOCK operation
        FORCE load(resolved)
        IF NOT verify_loaded(resolved):
          ERROR "Failed to load required: {file}"
          RETURN FAIL

  LOG "All context loaded - operation may proceed"
  RETURN PASS
```

---

## Part 7: Checklist Templates

### 7.1 Manual Checklist Template

```markdown
---
name: {checklist-id}
description: {WHAT this checklist validates}
when: {WHEN TO USE - checkpoint/transition}
type: manual
checkpoint: {phase-transition|before-commit|pre-deployment}
required: true
dependencies: [~shortcuts]
created: YYYY-MM-DD
updated: YYYY-MM-DD
author: "Name | agent-name"
version: 1.0.0
---

# {Checklist Name}

## Purpose
What this checklist validates and why

## When to Use
The specific checkpoint/transition where this applies

## Prerequisites
What must exist before using this checklist

## Checklist Items

### Category 1: {Category Name}
- [ ] Item 1
- [ ] Item 2
- [ ] Item 3

**Validation**: How to verify this category

### Category 2: {Category Name}
- [ ] Item 4
- [ ] Item 5

**Validation**: How to verify

## Pass Criteria
All items must be checked for this checklist to pass

## Failure Handling
What to do if checklist fails

## Related
- Links to related workflows, tasks, rules
```

### 7.2 Evaluation Checklist Template

```markdown
---
name: {executable-id}-checklist
description: Evaluation checklist for {type} {id}
when: Validating {id} execution via diagnose-trace
type: evaluation
source_entity: ~{type}:{id}
source_type: agent|skill|task|workflow
checkpoint: activation|execution|completion
required: true
created: YYYY-MM-DD
updated: YYYY-MM-DD
author: "Name | agent-name"
version: 1.0.0
derived_by: ~create-evaluation-checklist
---

# {Executable Name} Evaluation Checklist

**Source**: [[path/to/executable|~type:id]]
**Type**: {agent|skill|task|workflow}
**Purpose**: Validate expected behavior during trace analysis

---

## Activation Phase
Expected behavior when this executable is first invoked.

- [ ] {Expected action 1}
- [ ] {Expected action 2}
- [ ] {Expected action 3}

---

## Execution Phase
Expected behavior during main execution.

### {Step/Phase Name}
- [ ] {Expected action}
- [ ] {Expected action}

### {Next Step/Phase}
- [ ] {Expected action}

---

## Completion Phase
Expected behavior at completion.

- [ ] {Expected output}
- [ ] {Expected artifact}

---

## Validation Notes

**What diagnose-trace checks**:
- Tool calls match expected sequence
- File operations target expected paths
- Required context was loaded before use

**Common Failures**:
- Missing prerequisite load
- Wrong execution order
- Missing completion confirmation

## Related
- [[Source Executable]]
- [[~diagnose-trace]]
```

---

## Part 8: Real-World Examples

### 8.1 Framework Change Checklist (Manual)

```markdown
# Framework Change Checklist

**Type**: System Validation
**Purpose**: Prevent desynchronization when making framework-level changes
**Criticality**: HIGH
**When to Use**: ANY change to Architech Framework structure

## Pre-Change Analysis Phase

### 1. Change Classification
- [ ] Blueprint Addition/Modification
- [ ] Memory Structure Change
- [ ] Engineering Rule Change
- [ ] Agent/Workflow/Task Changes
- [ ] Cross-Repository Impact
- [ ] Meta-File Change

### 2. Impact Mapping
- [ ] Structure map checked
- [ ] Memory map checked
- [ ] Context map checked
- [ ] CLAUDE.md checked

## Validation Phase

### 6. Automated Validation Checks
- [ ] validate-structure-integrity
- [ ] validate-cross-references
- [ ] validate-dependency-chains
- [ ] validate-naming-conventions

### 7. Manual Verification
- [ ] New features findable via structure-map.yaml?
- [ ] Context-map.md accurate?
- [ ] Memory paths valid?
- [ ] Agent commands work?

## Sign-Off
- [ ] All checklist items completed
- [ ] No validation failures
- [ ] Cross-references verified
- [ ] Integration tests passed
```

### 8.2 Story DoD Checklist (Manual)

```markdown
# Story Definition of Done (DoD) Checklist

## Checklist Items

1. **Requirements Met:**
   - [ ] All functional requirements implemented
   - [ ] All acceptance criteria met

2. **Coding Standards & Structure:**
   - [ ] Follows coding standards
   - [ ] Properly organized
   - [ ] Consistent naming
   - [ ] Readable and commented

3. **Testing & Quality Assurance:**
   - [ ] Unit tests written and passing
   - [ ] Integration tests added
   - [ ] Edge cases tested
   - [ ] All existing tests pass

## VALIDATION RESULT

| Category                        | Status | Issues |
| ------------------------------- | ------ | ------ |
| 1. Requirements Met             | _TBD_  |        |
| 2. Coding Standards & Structure | _TBD_  |        |
| 3. Testing & Quality Assurance  | _TBD_  |        |

**Final Assessment:**
- COMPLETE / NEEDS WORK / BLOCKED
```

### 8.3 Meta-Architect Evaluation Checklist

```markdown
# Meta Architect Evaluation Checklist

**Source**: [[~agent:meta-architect]]
**Type**: agent
**Purpose**: Validate expected activation behavior

---

## Activation Phase
- [ ] Ran `shortcut_resolver.py ~meta-architect --content`
- [ ] Ran `build_shortcut_registry.py --agent meta-architect --mode plan`
- [ ] Ran `build_entity_definitions.py`
- [ ] Loaded `~meta-map` via shortcut resolver

---

## Execution Phase

### Context Loading
- [ ] Entity definitions available (12 types)
- [ ] Shortcut registry populated
- [ ] Agent capabilities loaded

### Output Display
- [ ] Displayed activation header with agent name
- [ ] Displayed `~help` menu with commands
- [ ] Ready for user interaction

---

## Completion Phase
- [ ] Agent persona active
- [ ] All dependencies resolved
- [ ] No error messages in activation

---

## Validation Notes

**What diagnose-trace checks**:
- Bash calls to shortcut_resolver.py and build scripts
- Read operations on meta-map.md
- Output text containing expected headers

**Common Failures**:
- Skipped entity definitions build
- Missing ~meta-map load
- Incomplete help menu display
```

---

## Part 9: Directory Structure

```
07-checklists/
├── README.md                           # Overview
├── framework-change-checklist.md       # Manual - pre-commit
├── story-definition-of-done-checklist.md  # Manual - DoD
├── story-draft-checklist.md            # Manual - story drafting
├── product-owner-master-checklist.md   # Manual - PO validation
├── architect-checklist.md              # Manual - architecture
├── product-manager-checklist.md        # Manual - PM validation
├── requirements-distribution-checklist.md
├── change-navigation-checklist.md
├── validation/
│   ├── agent-sequence-validator.yaml   # ASV rules
│   ├── ASV-COMPATIBILITY-ANALYSIS.md
│   └── ASV-V2-USAGE-GUIDE.md           # Usage documentation
└── evaluation/
    ├── README.md                       # Evaluation overview
    ├── defaults/
    │   └── default-behavioral-spec.md  # Fallback spec
    ├── agents/                         # Agent checklists
    ├── skills/                         # Skill checklists
    ├── tasks/                          # Task checklists
    └── workflows/                      # Workflow checklists
```

---

## Part 10: Implementation Recommendations for Strategy-Nexus

### 10.1 Core Adaptations Needed

1. **Simplify to Two States First**
   - Start with PASS/FAIL for MVP
   - Add CONCERNS/WAIVED in v2

2. **Implement Scoring Formula**
   ```
   Overall = (Activation * 0.3) + (Execution * 0.4) + (Completion * 0.3)
   ```

3. **Create Evidence Protocol**
   - Mandatory evidence for all claims
   - Template-based collection

4. **Build 3-Phase Model**
   - Activation checkers
   - Execution validators
   - Completion verifiers

### 10.2 Priority Implementation Order

1. **Phase 1**: Evidence framework (ASV-015/016 equivalent)
2. **Phase 2**: Basic 3-phase model for skills
3. **Phase 3**: Scoring formula implementation
4. **Phase 4**: Full checklist entity type
5. **Phase 5**: Evaluation checklist derivation

### 10.3 Key Files to Create

```
03-skills/validation/
├── quality-gate/
│   ├── SKILL.md                        # Gate orchestrator
│   └── scripts/
│       ├── validate_phase.py           # Phase validation
│       ├── collect_evidence.py         # Evidence collection
│       ├── calculate_score.py          # Scoring formula
│       └── generate_verdict.py         # Verdict generation
└── checklist-builder/
    ├── SKILL.md                        # Builds checklists
    └── scripts/
        └── derive_checklist.py         # From executable
```

---

## Appendix A: Complete ASV Rule Reference

| Rule | Phase | Enforcement | Purpose |
|------|-------|-------------|---------|
| ASV-001 | pre-activation | BLOCKING | Maps only on startup |
| ASV-002 | pre-operation | BLOCKING | Just-in-time loading |
| ASV-003 | pre-handoff | BLOCKING | Git workflow compliance |
| ASV-004 | during-operation | WARNING | Detect stale context |
| ASV-005 | post-completion | BLOCKING | Vault persistence |
| ASV-006 | pre-activation | BLOCKING | Domain/system rules |
| ASV-010 | domain-switch | BLOCKING | Context preservation |
| ASV-015 | diagnostic-claims | BLOCKING | Anti-bullshitting |
| ASV-016 | diagnostic-status | WARNING | Evidence collection |
| ASV-017 | during-operation | WARNING | Obsidian structure |
| ASV-018 | session-start/end | WARNING | Git workflow |

---

## Appendix B: Verdict Thresholds

| Score Range | Verdict | Action Required |
|-------------|---------|-----------------|
| >= 95 | EXEMPLARY | None - excellent execution |
| >= 80 | COMPLIANT | None - meets standards |
| >= 60 | MOSTLY_COMPLIANT | Review warnings |
| >= 40 | NEEDS_IMPROVEMENT | Address issues |
| < 40 | FAILED | Block progression |

---

**Document Version**: 1.0.0
**Extraction Complete**: 2026-01-01
**Next Action**: Create Project 18 for implementation
