---
id: 27-langfuse-annotation-and-scoring-integration
name: langfuse-annotation-and-scoring-integration
status: COMPLETE
type: research
description: "Load when user mentions 'analyze traces', 'score sessions', 'self-improvement', 'langfuse scoring', 'trace research'"
created: 2026-01-05
completed: 2026-01-05
---

# Langfuse Trace Analysis Research

## Purpose

**Research project** to understand Claude Code traces in Langfuse and design a scoring/analysis system for recursive self-improvement.

This project answers:
1. What does a full session look like in Langfuse?
2. How are traces structured (sessions vs traces vs observations)?
3. What can we realistically measure and score?
4. How do we handle trace size for multi-agent analysis?
5. What scoring dimensions make sense?

**Deliverables**: Research findings + design spec for implementation projects.

---

## Success Criteria

**Must achieve**:
- [x] Full understanding of trace/session/observation structure
- [x] Sample sessions analyzed manually to identify patterns
- [x] Scoring dimensions defined with rationale
- [x] Multi-agent architecture designed (how to split traces)
- [x] Design doc for implementation phase

**Outputs spawn new projects**:
- Project: Score config implementation
- Project: Multi-agent scoring system
- Project: Weekly analysis workflow

---

## Context

**Background**:
- Claude Code sessions traced to Langfuse (localhost:3002)
- 2,917+ traces exist
- Trace type: `claude_code_user`
- Structure partially known (user messages, observations)
- Need deeper exploration before building

**Research Questions**:
1. How do sessions group traces? (sessionId)
2. What's in observations? (tool calls, responses, costs)
3. How large are typical sessions? (token count, message count)
4. What patterns indicate good vs bad sessions?
5. Can we score at trace level or need session level?

**Constraints**:
- Local Langfuse must be running (localhost:3002)
- Research, not implementation - stay exploratory

---

## End Vision (Post-Research)

```
RUNTIME (continuous)
├── Claude Code sessions → OTEL → Langfuse
└── Human labels interesting traces (ground truth)

BATCH ANALYSIS (weekly)
├── Pull traces from Langfuse
├── Multi-agent scoring system (design TBD)
├── Store scores/comments to Langfuse
└── Generate improvement suggestions

IMPROVEMENT CYCLE
├── Review suggestions
├── Update system files
└── Better sessions → repeat
```

---

## Storage Location

Research outputs go to:
`04-workspace/00-ai-native-org/self-improvement/`

---

*Next: Fill in 03-plan.md with research approach*
