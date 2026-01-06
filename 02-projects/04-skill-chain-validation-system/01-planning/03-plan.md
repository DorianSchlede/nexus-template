# Skill-Chain Validation System - Plan

**Last Updated**: 2025-12-27

---

## Approach

Build a generic validation framework that:
1. Defines skill-chains as YAML contracts (inputs, outputs, gates)
2. Validates project state against contracts
3. Reports what's missing/broken with actionable recommendations
4. Tracks validation history over time
5. Enables 3-step fix workflow (research → plan → execute)

**First test case**: Research pipeline (create-research-project → execute-research-project)

---

## Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Contract format | YAML | Human-readable, easy to edit, Python-friendly |
| Contract location | Central skill library | Reusable across projects, version controlled |
| Validation output | Markdown reports | Readable, can include tables, integrates with Nexus |
| Fix workflow | 3-step (research/plan/execute) | Matches user preference, prevents blind auto-fixes |
| History storage | JSON per run | Easy to parse, compare, aggregate |

---

## Resources Needed

**Tools/Access**:
- Python 3.x (available)
- PyYAML for contract parsing
- pathlib for file operations

**Information/Data**:
- Complete mapping of research pipeline outputs
- Existing validation scripts to understand patterns

---

## Dependencies & Links

**Files Impacted**:
- `03-skills/validate-skill-chain/` - New skill to create
- `02-projects/02-ontologies-research/` - Test target

**Related Skills**:
- `create-research-project` - Phase 1 of research pipeline
- `execute-research-project` - Phase 2 of research pipeline
- `paper-analyze`, `paper-synthesize` - Sub-skills in pipeline

**Existing Validation Scripts** (to learn from):
- `03-skills/paper-analyze/scripts/validate_analysis.py`
- `03-skills/paper-synthesize/scripts/validate_synthesis.py`

---

## Technical Architecture

**System Components**:

```
validate-skill-chain/
├── SKILL.md                    # Skill definition + workflow
├── contracts/
│   └── research-pipeline.yaml  # Chain contract definition
├── scripts/
│   ├── contract_loader.py      # Parse YAML contracts
│   ├── validate_chain.py       # Main validation runner
│   ├── report_generator.py     # Markdown report builder
│   └── fix_planner.py          # 3-step fix workflow
└── references/
    ├── contract-schema.md      # Contract format documentation
    └── validation-rules.md     # Standard validation rules
```

**Data Flow**:
```
Contract (YAML) + Project Path
         ↓
   contract_loader.py
         ↓
   validate_chain.py
    ├── Check each skill's outputs
    ├── Validate against rules
    └── Check gates
         ↓
   report_generator.py
         ↓
   Validation Report (MD) + History (JSON)
```

**Technology Stack**:
- Python for scripts
- YAML for contracts
- Markdown for reports
- JSON for history

---

## Implementation Strategy

**Development Phases**:

1. **Contract Schema** - Define YAML format, document it
2. **Research Pipeline Contract** - Map actual outputs to contract
3. **Validation Scripts** - Core logic (loader, validator, reporter)
4. **History Tracking** - Store and view past runs
5. **Test on Real Project** - Validate 02-ontologies-research
6. **Fix Workflow** - 3-step fix planner
7. **Package as Skill** - Final SKILL.md and structure

**Testing Approach**:
- Test against 02-ontologies-research (real incomplete project)
- Verify reports match actual state
- Test fix workflow on identified issues

---

## Mental Models Applied

### First Principles

**Core problem**: Need to know if a skill-chain executed correctly.

**Fundamental truths**:
1. Skills produce files as outputs
2. Files have expected locations and formats
3. Some files have required fields/values
4. Skills have dependencies on previous skill outputs
5. Gates are boolean checks that must pass

**Stripped assumptions**:
- ~~Need complex validation logic~~ → Simple file existence + YAML field checks cover 80%
- ~~Need to understand skill internals~~ → Only care about outputs, not how they're made
- ~~Need real-time monitoring~~ → Post-hoc validation is sufficient

### Systems Thinking

**Components**:
```
┌─────────────────┐     ┌─────────────────┐
│ create-research │────▶│execute-research │
│    -project     │     │    -project     │
└────────┬────────┘     └────────┬────────┘
         │                       │
         ▼                       ▼
   [Phase 1 Outputs]       [Phase 2 Outputs]
   - _briefing.md          - */index.md
   - _selection_log.md     - _synthesis.md
   - _analysis_kit.md      - _validation_report.md
   - papers/*/_metadata    - papers/*/_analysis_log
```

**Feedback Loops**:
- Validation failure → Fix workflow → Re-validate (reinforcing quality)
- History tracking → Trend detection → Preventive improvements

**Leverage Points**:
- Contract definitions (small change in contract = large change in what's validated)
- Gate conditions (block bad state from propagating)

### Pre-Mortem Analysis

**Imagining failure**: "It's 3 months from now and the validation system is unused/broken..."

| Failure Mode | Likelihood | Prevention |
|--------------|------------|------------|
| Contracts too rigid | High | Start simple, add complexity only when needed |
| Reports not actionable | Medium | Include specific fix recommendations |
| Doesn't match real outputs | High | Test against actual project first |
| Too slow to run | Low | Python is fast enough for file checks |
| No one uses it | Medium | Integrate into close-session or make it easy to run |

**Biggest risk**: Contracts don't match reality → Mitigation: Build contract BY READING actual skill outputs, not from documentation.

---

## Open Questions

- [x] Fix mode: 3-step (research/plan/execute) - **Decided**
- [x] History tracking: Yes - **Decided**
- [x] Contract location: Central in skill - **Decided**
- [ ] Should validation run automatically on close-session?
- [ ] What's the minimum viable contract for v1?

---

*Next: Complete steps.md to break down execution*
