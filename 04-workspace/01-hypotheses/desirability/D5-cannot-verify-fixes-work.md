# D5: Cannot Verify Fixes Work

**Type**: Desirability
**Importance**: 9/10 (HIGH - Core workflow pain)
**Evidence**: Assumption
**Status**: Updated for v2.0
**Version**: 2.0

---

## Hypothesis

**We believe** AI agent developers make changes to prompts/configurations but have no reliable way to confirm improvements actually work or that they didn't break something else, leading to "shots in the dark" optimization.

**We'll know when** 15+ out of 20 interviewed developers report:
- Changed prompt/config without systematic validation in last 2 weeks
- Do not have an existing agent performance benchmark solution
- Uncertainty whether "fix" actually improved things (6+/10 uncertainty)
- Specific example of fix that seemed to work but later regressed
- Rank "fix validation" as must-have feature (not nice-to-have)
- Use eval frameworks (Composo, DeepEval, Athina.ai) but inconsistently

**Why it matters**: If true, automated fix validation + A/B testing is a killer feature for optimization workflow. If false, developers may have sufficient testing processes already.

---

## Links to Business Model

**Linked to:**
- **VPC v2.0**: Pain "Cannot verify fixes actually work (HIGH)"
- **VPC v2.0**: Gain Creator "Fix validation"
- **BMC v3.0**: Value Proposition #2 "Automated fix validation"
- **BMC v3.0**: Key Resources "Dataset Execution & Evaluation Engine"

---

## Current Evidence

**Evidence Level**: Assumption

Volkswagen Project, they paid for this.

---

## Test Cards

**Related Tests**:
- [[1-customer-discovery-interviews-TEST-CARD]] (Multi-hypothesis customer interviews)
- [[3-evaluation-engine-TEST]] (F5 - Technical validation)

---

**Generated**: 2025-10-26 (v2.0 Strategic Refinement)
**Framework**: Testing Business Ideas - Desirability Hypothesis
