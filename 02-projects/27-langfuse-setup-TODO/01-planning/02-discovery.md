# Discovery

**Time**: Comprehensive scan | **Purpose**: Surface dependencies, patterns, and insights before planning

---

## 1. Langfuse Data Model (CRITICAL)

Understanding the hierarchy is essential for this research project.

### Hierarchy

```
Session (1 Claude Code chat session)
    └── Trace (1 user message + full response cycle)
            └── Observation (individual operations within trace)
                    ├── Span (generic operation)
                    ├── Generation (LLM call with tokens)
                    ├── Tool (tool invocation)
                    └── Event (point-in-time action)
```

### Key Definitions

| Concept | What It Is | Claude Code Mapping |
|---------|-----------|-------------------|
| **Session** | Groups related traces by sessionId | 1 Claude Code conversation |
| **Trace** | Single request/response lifecycle | 1 user message → full response |
| **Observation** | Unit of work within a trace | Tool calls, LLM generations |
| **Generation** | LLM call with input/output/tokens | Claude API calls |
| **Span** | Generic operation | File reads, searches |

### Trace Metadata Available

From Claude Code OTEL export:
- `sessionId` - Groups traces into sessions
- `project` - Nexus project context
- `conversationId` - Unique conversation identifier
- `gitBranch` - Current git branch
- `cwd` - Working directory
- `name` - Trace type (e.g., `claude_code_user`)

---

## 2. Skills Inventory (76 Total)

### Core Read Operations (11 skills - from Project 08)
- `langfuse-list-traces`, `langfuse-get-trace`
- `langfuse-list-observations`, `langfuse-get-observation`
- `langfuse-list-sessions`, `langfuse-get-session`
- `langfuse-list-scores`, `langfuse-get-score`
- `langfuse-list-models`, `langfuse-get-model`
- `langfuse-get-project`

### Scoring & Evaluation (8 skills) - **HIGH RELEVANCE**
- `langfuse-list-score-configs` - List existing score configurations
- `langfuse-create-score-config` - Create new scoring dimension
- `langfuse-get-score-config` - Get config details
- `langfuse-update-score-config` - Modify config
- `langfuse-create-score` - Score a trace/observation
- `langfuse-delete-score` - Remove score
- `langfuse-list-scores` - Query existing scores
- `langfuse-get-score` - Get score details

**Score Config Types**:
- `NUMERIC` - Min/max range (e.g., 0-1 for accuracy)
- `CATEGORICAL` - Predefined categories (e.g., good/bad/neutral)
- `BOOLEAN` - True/false

### Annotation Queues (10 skills) - **HIGH RELEVANCE**
- `langfuse-list-annotation-queues` - List queues
- `langfuse-create-annotation-queue` - Create review queue
- `langfuse-get-annotation-queue` - Get queue details
- `langfuse-list-queue-items` - List items in queue
- `langfuse-create-queue-item` - Add trace to queue
- `langfuse-get-queue-item` - Get item details
- `langfuse-update-queue-item` - Annotate/update item
- `langfuse-delete-queue-item` - Remove from queue
- `langfuse-create-queue-assignment` - Assign to reviewer
- `langfuse-delete-queue-assignment` - Remove assignment

### Datasets (12 skills) - **HIGH RELEVANCE FOR GROUND TRUTH**
- `langfuse-list-datasets` - List evaluation datasets
- `langfuse-create-dataset` - Create new dataset
- `langfuse-get-dataset` - Get dataset details
- `langfuse-list-dataset-items` - List test cases
- `langfuse-create-dataset-item` - Add test case (input + expected output)
- `langfuse-get-dataset-item` - Get item details
- `langfuse-delete-dataset-item` - Remove item
- `langfuse-list-dataset-runs` - List evaluation runs
- `langfuse-get-dataset-run` - Get run details
- `langfuse-delete-dataset-run` - Remove run
- `langfuse-list-dataset-run-items` - List run results
- `langfuse-create-dataset-run-item` - Add run result

**Dataset Use Cases**:
- Store ground truth labeled examples
- Run evaluations against benchmark
- Track performance across runs
- Compare model versions

### Comments (3 skills)
- `langfuse-list-comments`, `langfuse-create-comment`, `langfuse-get-comment`

### Prompts (5 skills)
- CRUD for prompt management (not relevant for trace analysis)

### Admin/Utility (27 skills)
- Ingestion, Media, Traces write, Models write, Projects admin, Organizations, Health/Metrics

---

## 3. Langfuse API Client

**Location**: `03-skills/langfuse/langfuse-master/scripts/langfuse_client.py`

**Methods Available**:
- `get()` - List/read operations
- `post()` - Create operations
- `delete()` - Delete operations
- `patch()` - Partial updates
- `put()` - Full updates

**Authentication**: Basic Auth via `LANGFUSE_PUBLIC_KEY` / `LANGFUSE_SECRET_KEY`

**Base URL**: `{LANGFUSE_HOST}/api/public`

---

## 4. Evaluation Workflow Patterns (from Langfuse Docs)

### Pattern 1: Batch Scoring Pipeline
```python
for trace in langfuse.api.trace.list(tags="eval", limit=100).data:
    langfuse.create_score(
        trace_id=trace.id,
        name="quality",
        value=evaluate(trace),
        comment="Auto-scored by AI"
    )
```

### Pattern 2: Dataset-Based Evaluation
```python
# Create dataset with ground truth
langfuse.create_dataset(name="claude-sessions-benchmark")
langfuse.create_dataset_item(
    dataset_name="claude-sessions-benchmark",
    input={"session_data": "..."},
    expected_output={"quality_score": 0.9, "issues": []}
)

# Run evaluation
dataset = langfuse.get_dataset("claude-sessions-benchmark")
for item in dataset.items:
    with item.run(run_name="v1-scorer") as span:
        result = score_session(item.input)
        # Automatically tracked
```

### Pattern 3: Human Annotation Queue
1. Create annotation queue with score configs
2. Add traces to queue via API or rules
3. Assign to reviewers
4. Human annotates via Langfuse UI
5. Export annotations as ground truth

---

## 5. Related Projects (Archived)

### Project 08: langfuse-integration
- **Status**: COMPLETE
- **Delivered**: 11 read-only endpoints
- **Pattern**: Skill per endpoint

### Project 22: langfuse-integration-expansion
- **Status**: COMPLETE
- **Delivered**: 59 additional endpoints (all CRUD)
- **Key Fix**: Added `patch()` and `put()` to client
- **Discovery Doc**: `05-archived/22-langfuse-integration-expansion/02-resources/discovery.md`

### Project 23: langfuse-self-hosted-setup
- **Status**: COMPLETE
- **Delivered**: Local Langfuse at localhost:3002
- **Architecture**: Docker Compose with PostgreSQL, ClickHouse, Redis, MinIO
- **Bridge**: `claude-langfuse-monitor` npm package converts Claude Code logs to traces

---

## 6. Infrastructure

### Langfuse Instances

| Instance | Host | Purpose |
|----------|------|---------|
| Claude Code | `localhost:3002` | Claude Code traces (2,917+) |
| Beam AI | `tracing.beamstudio.ai` | Beam agent traces |

**Default**: `claude_code` (localhost:3002)

### Configuration

**File**: `01-memory/integrations/langfuse.yaml`

**Environment Variables**:
```
LANGFUSE_SECRET_KEY=sk-lf-49a255c7-...
LANGFUSE_PUBLIC_KEY=pk-lf-226d37cd-...
LANGFUSE_HOST=http://localhost:3002
```

---

## 7. Risks & Unknowns

| Risk | Severity | Mitigation |
|------|----------|------------|
| Session size exceeds context window | HIGH | Design chunking/splitting strategy |
| Ground truth bootstrapping | HIGH | Use Datasets API + human annotation |
| Score calibration drift | MEDIUM | Weekly human review of AI scores |
| API rate limits | LOW | Self-hosted has no limits |
| Long sessions (1000+ messages) | MEDIUM | Sampling + summarization strategy |

---

## 8. Open Questions (To Answer in Research)

### Data Structure
- [x] What is 1 trace? → User message + full response cycle
- [ ] How many observations per trace typically?
- [ ] What observation types exist in Claude Code traces?

### Size & Complexity
- [ ] Average traces per session?
- [ ] Average tokens per session?
- [ ] Can a session fit in 200k context?

### Scoring
- [ ] Score at trace level or observation level?
- [ ] Which dimensions are measurable automatically?
- [ ] Which require human judgment?

### Ground Truth
- [ ] How many labeled examples needed to bootstrap?
- [ ] Inter-annotator agreement threshold?

---

## 9. Key Insights

1. **Datasets API is perfect for ground truth** - Store input/expected output pairs, run evaluations, track over time

2. **Annotation queues enable human-in-the-loop** - Add traces to queue → assign reviewers → collect labels

3. **76 skills already exist** - Full API coverage, no new skills needed

4. **Session = conversation, Trace = turn** - Claude Code maps cleanly to Langfuse model

5. **Self-hosted = no limits** - Can query/score at scale without rate limiting

6. **Batch scoring pattern exists** - Iterate traces, apply evaluators, store scores

---

*→ Use these findings to update 03-plan.md and 04-steps.md*
