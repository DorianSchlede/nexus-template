# Langfuse Trace Analysis Research - Execution Steps

**Last Updated**: 2026-01-05

**IMPORTANT**: This file tracks project progress. Mark tasks complete with [x] as you finish them.

**Goal**: Understand WHAT projects to create next and HOW to slice up the self-improvement system.

---

## Phase 1: Planning

- [x] Complete 01-overview.md
- [x] Complete 02-discovery.md
- [x] Complete 03-plan.md
- [x] Complete 04-steps.md (granular version)
- [x] Review with stakeholder

---

## Phase 2: Trace Structure Discovery

**Goal**: Fully understand session → trace → observation hierarchy

**Required Context**:
- `02-discovery.md` (Langfuse data model section)
- Langfuse running at localhost:3002

### 2.1 List Sessions
- [x] Run `langfuse-list-sessions` with limit=20
- [x] Save raw response to `02-resources/api-responses/list-sessions.json`
- [x] Note: 43 total sessions, all from 2026-01-05, 32-char hex IDs

### 2.2 Analyze Small Session (< 10 traces)
- [x] Pick 1 session with few traces from list (1c96db43... - 8 traces)
- [x] Run `langfuse-get-session` with full trace data
- [x] Save to `02-resources/sample-sessions/small-session.json`
- [x] Document in `03-working/trace-structure-analysis.md`:
  - Session metadata fields
  - Trace structure (what fields exist)
  - Observation types found (GENERATION only)

### 2.3 Analyze Medium Session (10-50 traces)
- [x] Pick 1 session with moderate traces (8172830f... - 14 traces)
- [x] Run `langfuse-get-session`
- [x] Save to `02-resources/sample-sessions/medium-session.json`
- [x] Add to analysis doc: Only GENERATION type, costs in observations

### 2.4 Analyze Large Session (50+ traces)
- [x] Pick 1 session with many traces (5ff25b22... - 100 traces)
- [x] Run `langfuse-get-session`
- [x] Save to `02-resources/sample-sessions/large-session.json`
- [x] Add to analysis doc: May be paginated at 100

### 2.5 Map Observation Types
- [x] List all observation types: GENERATION only (claude_response)
- [x] For each type, document: fields, typical size, relevance to scoring
- [x] Add observation type reference to `03-working/trace-structure-analysis.md`

### 2.6 Document Trace Metadata
- [x] List all metadata fields: project, conversationId, gitBranch, cwd, messageType, source
- [x] Useful for filtering: project, gitBranch
- [x] Identify sessions: sessionId, conversationId
- [x] Finalize `03-working/trace-structure-analysis.md`

---

## Phase 3: Size & Complexity Analysis

**Goal**: Determine if sessions fit in agent context windows

**Required Context**:
- `03-working/trace-structure-analysis.md` (from Phase 2)
- Sample sessions from `02-resources/sample-sessions/`

### 3.1 Measure Session Sizes
- [x] For each sample session, calculate:
  - Number of traces: 8, 14, 100
  - Number of observations per trace (avg): 1
  - Total characters in session JSON: 93k, 132k, 288k
  - Estimated tokens (chars / 4): 23k, 33k, 72k
- [x] Create table in `03-working/session-size-analysis.md`

### 3.2 Estimate Context Requirements
- [x] What's the largest session in tokens? ~72k (without observations)
- [x] Can it fit in 200k context? Yes (all sessions)
- [x] Can it fit in 100k context? Yes (most sessions)
- [x] Can it fit in 50k context? Only small/medium sessions

### 3.3 Design Chunking Strategy (if needed)
- [x] If sessions exceed context: Time-based chunking (20 traces per chunk)
- [x] Document chunking approach: Option A with smart boundaries
- [x] Define: Include 1-2 context traces for continuity

### 3.4 Finalize Size Analysis
- [x] Complete `03-working/session-size-analysis.md`
- [x] Key finding: Most sessions fit in 100k; large sessions need chunking

---

## Phase 4: Langfuse API Validation

**Goal**: Validate scoring, annotation, and datasets APIs work as expected

**Required Context**:
- `02-discovery.md` (Skills Inventory section)
- A sample trace ID from Phase 2

### 4.1 Score Configs - List Existing
- [x] Run `langfuse-list-score-configs` (empty initially)
- [x] Save to `02-resources/api-responses/score-configs.json`
- [x] Note: No configs existed

### 4.2 Score Configs - Create NUMERIC
- [x] Run `langfuse-create-score-config` test-efficiency (0-1 range)
- [x] Document response schema (id, name, minValue, maxValue, dataType)

### 4.3 Score Configs - Create CATEGORICAL
- [x] Run `langfuse-create-score-config` test-quality
- [x] Categories: poor(0), acceptable(1), good(2), excellent(3)

### 4.4 Scores - Attach to Trace
- [x] Trace ID: 954df280-faab-4823-91a8-9a31f4628f8c
- [x] Created score: test-efficiency=0.85, test-quality=good

### 4.5 Scores - Attach to Observation
- [x] Observation ID: 5a7b63e6-df31-479a-b2fb-6632f9804564
- [x] Created score: test-efficiency=0.9

### 4.6 Annotation Queues - Explore
- [x] Run `langfuse-list-annotation-queues` (empty)
- [x] Run `langfuse-create-annotation-queue` - **FAILED (400 Bad Request)**
- [x] Document: API may require UI setup or missing params

### 4.7 Datasets API - Ground Truth
- [x] Run `langfuse-list-datasets` (empty initially)
- [x] Run `langfuse-create-dataset` "test-ground-truth"
- [x] Run `langfuse-create-dataset-item` with input/expected
- [x] Works! Use datasets for ground truth storage

### 4.8 API Validation Summary
- [x] Create `03-working/langfuse-api-validation.md`
- [x] Document: Scoring works, annotation queues fail, datasets work

---

## Phase 5: Pattern Identification

**Goal**: Define what makes a good vs bad session

**Required Context**:
- Sample sessions from `02-resources/sample-sessions/`
- `03-working/trace-structure-analysis.md`

### 5.1 Manual Session Review (3 sessions)
- [x] Reviewed 3 sessions: small (8 traces), medium (14), large (100)
- [x] Analyzed trace type breakdowns:
  - Small: skill execution flow (add-integration)
  - Medium: 9 tool outputs, 5 user messages
  - Large: 40 file ops, 28 user messages, 9 todo confirmations

### 5.2 Identify Good Patterns
- [x] Context efficiency: Load only needed files, use offsets
- [x] Instruction following: Follow SKILL.md steps, use TodoWrite
- [x] Tool appropriateness: Use Read/Edit/Grep not Bash equivalents
- [x] Documented in `03-working/scoring-dimensions.md`

### 5.3 Identify Anti-Patterns
- [x] Context: Read same file multiple times, excessive startup bloat
- [x] Instructions: Skip workflow steps, ignore corrections
- [x] Tools: Use Bash for file ops, repeated failed attempts
- [x] Added to scoring dimensions doc

### 5.4 Define Scoring Dimensions
- [x] 6 dimensions defined:
  1. context_efficiency (NUMERIC 0-1)
  2. instruction_following (CATEGORICAL)
  3. tool_appropriateness (NUMERIC 0-1)
  4. task_completion (CATEGORICAL)
  5. error_recovery (CATEGORICAL)
  6. cost_efficiency (NUMERIC 0-1)
- [x] Finalized `03-working/scoring-dimensions.md`

### 5.5 Define Session Completeness
- [x] Complete = has close-session OR user confirmation OR deliverables
- [x] Exclude: <3 traces, mid-sentence endings, no user messages
- [x] Documented filtering criteria

---

## Phase 6: Architecture Design

**Goal**: Design the multi-agent scoring system

**Required Context**:
- `03-working/session-size-analysis.md`
- `03-working/scoring-dimensions.md`
- `03-working/langfuse-api-validation.md`

### 6.1 Design Session Processing Pipeline
- [x] Input: Session ID → Fetch → Chunk → Score → Store
- [x] 6-component architecture: Fetcher, Scorer, Storage, Synthesizer, Suggester, Calibrator
- [x] Document in `03-working/architecture-design.md`

### 6.2 Design Scorer Agent(s)
- [x] Decision: Single general scorer (simpler, can iterate to specialists later)
- [x] Scoring prompt template with structured JSON output
- [x] Context: session traces, metadata, instructions
- [x] Added to architecture doc

### 6.3 Design Score Aggregation
- [x] Chunking: 20 traces/chunk with 2-trace context overlap
- [x] Numeric: weighted average across chunks
- [x] Categorical: majority vote or worst-case
- [x] Overall quality: weighted formula in doc

### 6.4 Design Human Calibration Workflow
- [x] Use Datasets API for ground truth (annotation queues failed)
- [x] Human labels stored as dataset items
- [x] Calculate Cohen's kappa and correlation metrics
- [x] Added to architecture doc

### 6.5 Design Improvement Loop
- [x] Weekly schedule: Sunday 2am
- [x] Fetch → Score → Synthesize → Suggest → Report
- [x] Suggestions saved to core-learnings.md
- [x] Added to architecture doc

### 6.6 Finalize Architecture
- [x] Complete `03-working/architecture-design.md`
- [x] Includes ASCII diagrams, code samples, risk mitigation

---

## Phase 7: Research Outputs & Spawned Projects

**Goal**: Package findings and define implementation projects

**Required Context**:
- All `03-working/*.md` files from previous phases

### 7.1 Synthesize Findings
- [x] Create `04-outputs/research-summary.md`
- [x] Key findings from each phase
- [x] Recommendations

### 7.2 Define Spawned Project: Score Config Setup
- [x] Create `04-outputs/project-specs/score-config-setup.md`
- [x] Scope: Create all score configs in Langfuse
- [x] Dependencies: Scoring dimensions defined
- [x] Estimated effort: Small

### 7.3 Define Spawned Project: Session Scorer
- [x] Create `04-outputs/project-specs/session-scorer.md`
- [x] Scope: Build agent/skill to score a session
- [x] Dependencies: Architecture design, score configs
- [x] Estimated effort: Medium

### 7.4 Define Spawned Project: Weekly Analysis Workflow
- [x] Create `04-outputs/project-specs/weekly-analysis.md`
- [x] Scope: Automated weekly scoring + synthesis
- [x] Dependencies: Session scorer working
- [x] Estimated effort: Medium

### 7.5 Define Spawned Project: Ground Truth Bootstrap
- [x] Create `04-outputs/project-specs/ground-truth-bootstrap.md`
- [x] Scope: Manually label 20-50 sessions for calibration
- [x] Dependencies: Score configs, datasets API
- [x] Estimated effort: Medium (human time)

### 7.6 Final Review
- [x] Review all outputs with stakeholder
- [x] Prioritize spawned projects
- [ ] Close this research project

---

## Phase 8: Spawn Implementation Projects

**Goal**: Create actual project folders from specs

### 8.1 Create Project 35: Score Config Setup
- [x] Create project folder structure
- [x] Copy reference files from this project
- [x] Write 01-overview.md with system context
- [x] Write 02-discovery.md
- [x] Write 03-plan.md
- [x] Write 04-steps.md
- [x] Write resume-context.md

### 8.2 Create Project 36: Session Scorer
- [x] Create project folder structure
- [x] Copy reference files from this project
- [x] Write 01-overview.md with system context
- [x] Write 02-discovery.md
- [x] Write 03-plan.md
- [x] Write 04-steps.md
- [x] Write resume-context.md

### 8.3 Create Project 37: Weekly Quality Monitoring
- [ ] Create project folder structure
- [ ] Copy reference files from this project
- [ ] Write 01-overview.md with system context
- [ ] Write 02-discovery.md
- [ ] Write 03-plan.md
- [ ] Write 04-steps.md
- [ ] Write resume-context.md

### 8.4 Create Project 38: Ground Truth Bootstrap
- [ ] Create project folder structure
- [ ] Copy reference files from this project
- [ ] Write 01-overview.md with system context
- [ ] Write 02-discovery.md
- [ ] Write 03-plan.md
- [ ] Write 04-steps.md
- [ ] Write resume-context.md

### 8.5 Finalize
- [ ] Update Project 27 status to COMPLETE
- [ ] Archive Project 27

---

## Notes

**Current blockers**: None - ready to start research

**Dependencies**:
- Langfuse localhost:3002 must be running
- Claude Code traces already present (2,917+ confirmed)
- 76 Langfuse skills available (full API coverage)

**Output location**: This project (`02-resources/`, `03-working/`, `04-outputs/`)

---

*Mark tasks complete with [x] as you finish them*
