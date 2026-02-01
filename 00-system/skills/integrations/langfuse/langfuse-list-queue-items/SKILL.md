---
name: langfuse-list-queue-items
description: "List queue items. Load when user says 'list queue items', 'show review items'."
---

# List Queue Items

Get items in an annotation queue.

## Usage

```bash
python scripts/list_queue_items.py --queue "queue-abc"
```

## API Reference

```
GET /api/public/annotation-queues/{id}/items
```
