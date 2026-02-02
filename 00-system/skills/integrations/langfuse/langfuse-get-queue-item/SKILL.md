---
name: langfuse-get-queue-item
description: "Get a queue item. Load when user says 'get queue item', 'item details'."
---

# Get Queue Item

Get a specific queue item.

## Usage

```bash
uv run python scripts/get_queue_item.py --queue "queue-abc" --item "item-xyz"
```

## API Reference

```
GET /api/public/annotation-queues/{id}/items/{itemId}
```
