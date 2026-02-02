---
name: langfuse-help
description: "langfuse help, langfuse reference, langfuse --help, show langfuse operations, list langfuse skills."
---

# Langfuse Help

Quick reference for Langfuse operations. For detailed patterns, see full reference:
```bash
cat 00-system/skills/meta/langfuse-help/SKILL.md
```

---

## Available Skills (70+ operations)

### Core Operations
| Skill | Description |
|-------|-------------|
| langfuse-list-traces | List recent traces |
| langfuse-get-trace | Get trace WITH observations |
| langfuse-list-sessions | List sessions |
| langfuse-get-session | Get session (NO observations) |
| langfuse-list-observations | List spans/generations |

### Scores
| Skill | Description |
|-------|-------------|
| langfuse-list-scores | List evaluation scores |
| langfuse-create-score | Create score (with validation) |
| langfuse-delete-score | Delete score |
| langfuse-list-score-configs | List score configs |

### Datasets & Prompts
| Skill | Description |
|-------|-------------|
| langfuse-list-datasets | List datasets |
| langfuse-create-dataset-item | Add ground truth item |
| langfuse-list-prompts | List prompts |

---

## Critical Patterns

### Observations Require Individual Fetch
```python
# GET /sessions/{id} does NOT include observations
# Must call GET /traces/{id} for each trace
for trace in session["traces"]:
    full = client.get(f"/traces/{trace['id']}")
    obs = full.get("observations", [])
```

### CATEGORICAL Scores Use String Value
```python
# CORRECT
{"value": "complete", "configId": "..."}

# WRONG (400 error)
{"value": 2, "stringValue": "complete"}
```

### Use create_score.py for Validation
```bash
# Validates before sending (API accepts garbage!)
uv run python create_score.py --trace {id} --name goal_achievement \
  --string-value complete --config-id {uuid}

# List all known configs
uv run python create_score.py --list-configs

# With metadata (rich JSON, ~1MB limit)
uv run python create_score.py --trace {id} --name session_notes --value 1 \
  --metadata '{"trace_ids": ["a","b"], "findings": [...]}'
```

---

## Score Config IDs

```python
CONFIG_IDS = {
    # Quality Dimensions (NUMERIC 0-1 unless noted)
    "goal_achievement": "68cfd90c-8c9e-4907-808d-869ccd9a4c07",      # CATEGORICAL
    "tool_efficiency": "84965473-0f54-4248-999e-7b8627fc9c29",
    "process_adherence": "651fc213-4750-4d4e-8155-270235c7cad8",
    "context_efficiency": "ae22abed-bd4a-4926-af74-8d71edb1925d",
    "error_handling": "96c290b7-e3a6-4caa-bace-93cf55f70f1c",        # CATEGORICAL
    "output_quality": "d33b1fbf-d3c6-458c-90ca-0b515fe09aed",
    "overall_quality": "793f09d9-0053-4310-ad32-00dc06c69a71",
    # Meta Scores
    "root_cause_issues": "669bead7-1936-4fc4-bae8-e7814c9eab04",     # CATEGORICAL
    "session_improvements": "2e87193b-c853-4955-b2f0-9fa572531681",  # CATEGORICAL
    "session_notes": "67640329-0c03-4be6-bc9f-49765a0462b5",         # NUMERIC (value=1 + comment/metadata)
}
```

### CATEGORICAL Labels
| Score | Labels |
|-------|--------|
| goal_achievement | failed, partial, complete, exceeded |
| error_handling | poor, struggled, recovered, prevented |
| root_cause_issues | none, tool_misuse, process_violation, context_waste, error_cascade, output_quality, multiple |
| session_improvements | none, minor, moderate, significant, critical |

---

## Quick Start

```bash
# 1. Check config
uv run python 03-skills/langfuse/langfuse-master/scripts/check_langfuse_config.py --test

# 2. List recent traces
uv run python 03-skills/langfuse/langfuse-list-traces/scripts/list_traces.py --limit 10

# 3. Get trace with observations
uv run python 03-skills/langfuse/langfuse-get-trace/scripts/get_trace.py --id {trace_id}

# 4. Create score (validated)
uv run python 03-skills/langfuse/langfuse-create-score/scripts/create_score.py \
  --trace {id} --name tool_efficiency --value 0.85 \
  --config-id 84965473-0f54-4248-999e-7b8627fc9c29
```

---

## Full Reference

For comprehensive patterns (subagents, metadata, worktrees):
```bash
cat 00-system/skills/meta/langfuse-help/SKILL.md
```

Contains:
- Subagent trace finding (conversationId pattern)
- Two-step prompt pattern for custom agents
- Metadata vs comment (rich JSON storage)
- Overall quality formula
- Worktree isolation for parallel testing
