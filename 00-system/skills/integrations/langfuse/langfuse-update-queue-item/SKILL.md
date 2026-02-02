---
name: langfuse-update-queue-item
description: "Update a queue item. Load when user says 'update queue item', 'complete review'."
---

# Update Queue Item

Update a queue item status.

## Usage

```bash
uv run python scripts/update_queue_item.py --queue "queue-abc" --item "item-xyz" --status COMPLETED
```

## API Reference

```
PATCH /api/public/annotation-queues/{id}/items/{itemId}
```
