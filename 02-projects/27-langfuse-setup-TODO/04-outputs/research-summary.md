# Research Summary: Langfuse Trace Analysis

**Project**: 27-langfuse-annotation-and-scoring-integration
**Status**: Research Complete + Validated
**Date**: 2026-01-05
**Updated**: 2026-01-05 (Post-Validation Revision)

---

## Executive Summary

This research project investigated how to build a quality monitoring system using Claude Code traces stored in Langfuse. The key question was: **Can we automatically score sessions, identify patterns, and generate improvement suggestions?**

**Answer**: Yes, with important clarifications from validation.

**Critical Clarification**: This is a **monitoring dashboard**, not a closed self-improvement loop. The system provides visibility and suggestions; humans close the loop by deciding what to implement.

---

## Key Findings

### 1. Trace Structure (Phase 2)

**Data hierarchy**:
```
Session (1 conversation) → Trace (1 user turn) → Observation (1 LLM response)
```

**Critical insight**: The `get-session` API returns traces WITHOUT observations. Must call `get-trace` individually to get observation details (costs, tokens).

**Observation types**: Only GENERATION observed (claude_response). No tool spans captured by current tracing.

### 2. Session Sizes (Phase 3) - VALIDATED & REVISED

| Session Type | Traces | Est. Tokens | Context Fit |
|--------------|--------|-------------|-------------|
| Small | <10 | ~25k | 50k |
| Medium | 10-50 | ~35k | 100k |
| Large | 50+ | ~75k+ | Requires chunking |

**CRITICAL FIX**: Original chunking strategy (20 traces/chunk) was INVALID. 20 traces + observations = ~115k tokens = CONTEXT OVERFLOW.

**Revised chunking strategy**: Token-based, not trace-count based.
- Target: 70,000 tokens per chunk (leave headroom)
- Overlap: 4 traces (not 2 - insufficient for multi-turn context)
- Threshold: Chunk when estimated tokens > 80,000

### 3. Langfuse API (Phase 4)

| Feature | Status | Notes |
|---------|--------|-------|
| Score Configs | Working | NUMERIC and CATEGORICAL types |
| Create Score | Working | Trace and observation level |
| Datasets | Working | Use for ground truth |
| Annotation Queues | **NOT WORKING** | 400 error on create |

**Workaround**: Use Datasets API for human labeling instead of annotation queues.

### 4. Scoring Dimensions (Phase 5) - VALIDATED & REVISED

**VALIDATION FINDINGS**: Original 6 dimensions had issues:
- Redundancy: context_efficiency + cost_efficiency highly correlated
- Missing: security_compliance (OWASP risks)
- Missing: user_satisfaction (ultimate success indicator)

**Revised 6 dimensions**:

1. **task_completion** (CATEGORICAL) - weight 0.30
   - Did it achieve the user's stated goal?
2. **execution_quality** (NUMERIC 0-1) - weight 0.25
   - Combines instruction_following + context efficiency
3. **tool_mastery** (NUMERIC 0-1) - weight 0.20
   - Combines tool_appropriateness + error_recovery
4. **resource_efficiency** (NUMERIC 0-1) - weight 0.15
   - Token usage, file operations, API calls relative to complexity
5. **security_compliance** (CATEGORICAL) - weight 0.05 (NEW)
   - OWASP risk prevention, safe practices
6. **user_satisfaction** (CATEGORICAL) - weight 0.05 (NEW)
   - User feedback signals (thanks, corrections, abandonment)

**Overall quality formula**:
```python
overall = (task * 0.30) + (exec * 0.25) + (tool * 0.20) +
          (resource * 0.15) + (security * 0.05) + (user * 0.05)
```

### 5. Architecture (Phase 6) - VALIDATED & REVISED

**Design decision**: Single general scorer using Claude Code subagents (Task tool). Not a separate API call - uses same model as Claude Code itself.

**Pipeline**: Fetch → Token-Chunk → Score (subagent) → Store → Synthesize → Report

**CRITICAL CLARIFICATION**: This is a **monitoring dashboard**, NOT self-improvement:
- System produces reports and suggestions
- Human reviews and decides what to implement
- Human manually applies approved changes
- Feedback loop is only closed through human action

**Schedule**: Weekly runs on Sunday 2am

**Human calibration**: Via Datasets API with ground truth labels

---

## Recommendations

### Immediate (Spawned Projects)

1. **Score Config Setup** (Project 28 - Small)
   - Create 7 score configs in Langfuse (revised dimensions)
   - Test on 5 sample sessions

2. **Session Scorer** (Project 29 - Medium)
   - Build skill using Claude Code subagents
   - Implement **token-based** chunking (not trace-count)
   - Extract task context from first user message

3. **Weekly Quality Monitoring** (Project 30 - Medium)
   - Create scheduled skill (NOT "self-improvement")
   - Build synthesizer and suggestion generator
   - Reports require human review before action

4. **Ground Truth Bootstrap** (Project 31 - Medium)
   - Label 50 sessions manually
   - Calculate calibration metrics

### Future Considerations

- Enrich OTEL tracing to capture tool spans
- Build specialized critic agents for dimensions
- Create Langfuse UI dashboard for scores
- **True self-improvement requires**: closing the loop with automated change application (intentionally NOT in scope)

---

## Artifacts Created

| Artifact | Purpose |
|----------|---------|
| `03-working/trace-structure-analysis.md` | Session/trace/observation hierarchy |
| `03-working/session-size-analysis.md` | Context window planning |
| `03-working/langfuse-api-validation.md` | API capability validation |
| `03-working/scoring-dimensions.md` | Quality metrics definition (REVISED) |
| `03-working/architecture-design.md` | System design with code samples (REVISED) |
| `04-outputs/validation-findings.md` | Validation agent findings (NEW) |
| `02-resources/sample-sessions/*.json` | Sample data for testing |
| `02-resources/api-responses/*.json` | API response examples |

---

## Success Metrics

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Sessions scored/week | 20+ | Langfuse score count |
| Human-AI correlation | >0.8 | Ground truth comparison |
| Improvements/month | 2+ | core-learnings.md updates |
| Quality trend | +0.05/month | Average overall_quality |

---

## Risks & Mitigations

| Risk | Severity | Mitigation |
|------|----------|------------|
| Scorer bias | Medium | Calibrate against human labels |
| High API cost | Medium | Batch scoring, efficient model |
| Context overflow | Low | Chunking strategy ready |
| Score drift | Medium | Weekly human review sample |
| Input tokens not tracked | Low | Estimate from content size |

---

## Validation Summary

Five validation subagents were spawned to test critical assumptions. Key findings:

| Area | Verdict | Action Taken |
|------|---------|--------------|
| Langfuse API | Confirmed | input_tokens=0 is known limitation |
| Scoring Dimensions | WEAK | Merged redundant, added security/satisfaction |
| Chunking Strategy | INVALID | Replaced with token-based (70k target) |
| Self-Improvement Loop | INVALID | Rebranded as "monitoring dashboard" |
| Scorer Prompt | 80% Ready | Uses subagents, added task context extraction |

See `04-outputs/validation-findings.md` for full details.

---

## Conclusion

The research confirms that a **quality monitoring system** is feasible with current Langfuse capabilities.

**Important distinctions after validation**:
1. This is monitoring, not self-improvement (loop not closed)
2. Chunking must be token-based, not trace-count based
3. Scoring dimensions were revised for clarity and completeness
4. Human review is required before any suggestions are implemented

**Recommended next step**: Create Project 28 (Score Config Setup) to establish the scoring infrastructure in Langfuse with the revised dimensions.

---

*Research complete + validated. Ready to spawn implementation projects.*
