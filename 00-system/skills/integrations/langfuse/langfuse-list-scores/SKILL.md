---
name: langfuse-list-scores
description: "List Langfuse scores. Load when user says 'list scores', 'show scores', 'get evaluations'."
---

# List Scores

Get list of evaluation scores from Langfuse.

## Usage

### CLI
```bash
python scripts/list_scores.py --limit 20
python scripts/list_scores.py --trace-id trace123
python scripts/list_scores.py --name "accuracy"
```

### Python
```python
from list_scores import list_scores

scores = list_scores(limit=20)
scores = list_scores(trace_id="trace123")
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| --limit | int | Max results (default 50) |
| --cursor | string | Pagination cursor |
| --trace-id | string | Filter by trace |
| --observation-id | string | Filter by observation |
| --name | string | Filter by score name |
| --source | string | API, EVAL, or ANNOTATION |

## API Reference

```
GET /api/public/v2/scores
```

See: `langfuse-master/references/api-reference.md`
