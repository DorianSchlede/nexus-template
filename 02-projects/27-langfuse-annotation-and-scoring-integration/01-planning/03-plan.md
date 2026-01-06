# Langfuse Trace Analysis Research - Plan

**Last Updated**: 2026-01-05

---

## Research Approach

**Phase 1: Trace Structure Discovery**
- Explore session → trace → observation hierarchy
- Understand: 1 session = 1 Claude Code chat (confirmed)
- Understand: 1 trace = 1 user message + full response (confirmed from docs)
- Map observation types: Span, Generation, Tool, Event
- Document metadata available per trace

**Phase 2: Size & Complexity Analysis**
- Sample sessions of varying sizes
- Measure: traces per session, observations per trace, tokens per observation
- Determine: Can 1 agent handle a session in 200k context?
- Design intelligent compression/splitting strategy if needed

**Phase 3: Langfuse API Validation**
- Test scoring API (create configs, attach scores)
- Test annotation queues (create, add items, update)
- Test datasets API (ground truth storage)
- Validate all 76 existing skills work correctly

**Phase 4: Pattern Identification**
- Manually review 5-10 sessions
- Identify: What makes a "good" vs "bad" session?
- Define scoring dimensions with examples

**Phase 5: Architecture Design**
- Design multi-agent scoring system
- Define ground truth bootstrapping strategy
- Document human-in-the-loop calibration workflow
- Document the improvement loop algorithm

---

## Key Decisions

| Decision | Choice | Why |
|----------|--------|-----|
| Project type | Research | Need to understand before building |
| Data source | localhost:3002 | Claude Code traces are there (2,917+) |
| Analysis unit | Session-level | Traces are parts of sessions, need full context |
| Storage location | This project (`02-resources/`, `03-working/`) | Outputs stay here, spawn new projects |

---

## Dependencies & Links

*From 02-discovery.md*

**External Systems**:
- Langfuse API (localhost:3002) - trace storage and scoring
- Claude Code - source of traces via OTEL

**Skills Available (76 total)**:

| Category | Skills | Relevance |
|----------|--------|-----------|
| Core Read | 11 | Trace/session enumeration |
| Scoring & Evaluation | 8 | **HIGH** - score configs, create/list scores |
| Annotation Queues | 10 | **HIGH** - human-in-the-loop workflow |
| Datasets | 12 | **HIGH** - ground truth storage |
| Comments | 3 | Medium - trace annotations |
| Admin/Utility | 27 | Low - ingestion, models, projects |
| Prompts | 5 | Not relevant |

**Key Skills for This Project**:
- `langfuse-list-sessions`, `langfuse-get-session` - enumerate sessions
- `langfuse-list-traces`, `langfuse-get-trace` - trace details
- `langfuse-list-observations` - observation details
- `langfuse-create-score-config` - define scoring dimensions (NUMERIC/CATEGORICAL/BOOLEAN)
- `langfuse-create-score` - attach scores to traces/observations
- `langfuse-create-annotation-queue` - human review queues
- `langfuse-create-queue-item` - add traces to review queue
- `langfuse-create-dataset` - ground truth storage
- `langfuse-create-dataset-item` - add labeled examples

**Related Projects**:
- Project 08: langfuse-integration (archived) - 11 read-only endpoints
- Project 22: langfuse-integration-expansion (archived) - 59 additional endpoints
- Project 23: langfuse-self-hosted-setup (archived) - localhost:3002 infrastructure

---

## Research Questions

### Q1: Trace Structure
- What is 1 trace? → **Confirmed**: 1 user message + full response cycle
- How do observations relate to traces? → Observations are nested within traces (Span, Generation, Tool, Event types)
- What metadata is available? → sessionId, project, conversationId, gitBranch, cwd, name
- **NEW**: What defines a "complete" session? (has closing message? reached goal?)

### Q2: Session Size
- How many traces per session? (min/max/avg)
- How many tokens per session?
- Can we fit a session in 200k context? 100k?

### Q3: Langfuse Scoring API
- How do score configs work? (numeric vs categorical vs boolean)
- Can we score at trace level AND observation level?
- How to attach scores programmatically?
- What's the schema for score configs?

### Q4: Langfuse Annotation Queues
- How do annotation queues work?
- Can we create custom annotation workflows?
- How to assign traces to reviewers?
- What UI does Langfuse provide for human annotation?

### Q5: Scoring Dimensions
Candidates to evaluate:
- **Context Loading Quality**: Right files loaded? Unnecessary bloat?
- **Instruction Following**: Did it follow SKILL.md steps? CLAUDE.md rules?
- **Tool Usage**: Right tool for job? Unnecessary calls?
- **Error Handling**: How were errors recovered?
- **Efficiency**: Tokens used vs task complexity
- **Cost Efficiency**: $ spent relative to outcome value
- **Meta-Learning**: Did it discover patterns? Suggest improvements?

**Score Config Types Available**:
- NUMERIC (0-1 range, e.g., accuracy)
- CATEGORICAL (good/bad/neutral)
- BOOLEAN (true/false)

### Q6: Multi-Agent Architecture
- How to split traces for parallel analysis?
- Specialized critics vs general analyzer?
- How to aggregate scores?

### Q7: Human Annotation Workflow
- How will humans review AI-generated scores?
- How to flag disagreements between AI and human?
- How to use human labels to calibrate AI scorers?
- What's the feedback loop from human → AI improvement?

### Q8: Improvement Loop
- How often to run analysis? (weekly)
- How to surface improvement suggestions?
- How to track improvements over time?

### Q9: Session Identification & Filtering (NEW)
- How to identify "interesting" sessions for analysis?
- Filter by: project? duration? error rate? cost?
- How to avoid analyzing incomplete/abandoned sessions?
- Sampling strategy for large volumes (2,917+ traces)?

### Q10: Ground Truth Bootstrapping (NEW)
- How many labeled examples needed to calibrate AI scorers?
- Use Datasets API to store input/expected output pairs
- Human annotation queue → export as ground truth
- Inter-annotator agreement threshold?

---

## Output Location

All research outputs stay in this project:
```
27-langfuse-annotation-and-scoring-integration/
├── 02-resources/         # Sample session exports, API response examples
├── 03-working/           # Analysis documents, findings, design drafts
└── 04-outputs/           # Final: spawned project specs, architecture decisions
```

**Primary Goal**: Understand WHAT projects to create next and HOW to slice up the work.

---

## Improvement Loop Algorithm (Draft)

```
WEEKLY CYCLE:
1. COLLECT
   - Pull new sessions since last analysis
   - Filter: completed sessions only
   - Sample: N sessions (stratified by project, user, duration)

2. ANALYZE
   - For each session:
     - Split into analyzable chunks
     - Run scoring agents (context, instruction, tool, meta)
     - Aggregate scores
     - Store to Langfuse

3. SYNTHESIZE
   - Aggregate patterns across sessions
   - Identify recurring issues
   - Generate improvement suggestions

4. IMPROVE
   - Review suggestions (human approval)
   - Update system files:
     - core-learnings.md (patterns)
     - Skills (if needed)
     - Hooks (if needed)
     - CLAUDE.md (if needed)

5. TRACK
   - Log changes made
   - Compare scores week-over-week
   - Report on improvement trajectory
```

---

## Open Questions

- [x] What exactly is a "trace" in Claude Code's OTEL export? → 1 user message + full response cycle
- [ ] How to handle very long sessions (1000+ messages)?
- [ ] Should we score individual traces or only sessions?
- [x] How to bootstrap scoring agents? → Use Datasets API + human annotation queues
- [ ] What's the right cadence for improvement cycles?
- [ ] What defines a "complete" vs "abandoned" session?

---

## Key Insights from Discovery

1. **76 skills already exist** - Full Langfuse API coverage, no new skills needed
2. **Datasets API is perfect for ground truth** - Store input/expected output pairs, run evaluations, track over time
3. **Annotation queues enable human-in-the-loop** - Add traces to queue → assign reviewers → collect labels → export as ground truth
4. **Session = conversation, Trace = turn** - Claude Code maps cleanly to Langfuse model
5. **Self-hosted = no limits** - Can query/score at scale without rate limiting
6. **Three evaluation patterns available**:
   - Batch scoring pipeline (iterate, evaluate, store)
   - Dataset-based evaluation (benchmark runs)
   - Human annotation queue (calibration)

---

*Next: Break down research tasks in 04-steps.md*
