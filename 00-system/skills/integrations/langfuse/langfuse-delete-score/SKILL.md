---
name: langfuse-delete-score
description: "Delete a score. Load when user says 'delete score', 'remove evaluation'."
---

# Delete Score

Delete a score by ID.

## Usage

```bash
uv run python scripts/delete_score.py --id "score-abc123"
```

## API Reference

```
DELETE /api/public/scores/{id}
```
