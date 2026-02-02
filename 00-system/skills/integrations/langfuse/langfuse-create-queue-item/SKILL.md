---
name: langfuse-create-queue-item
description: "Add item to queue. Load when user says 'add to queue', 'queue trace for review'."
---

# Create Queue Item

Add a trace/observation to an annotation queue.

## Usage

```bash
uv run python scripts/create_queue_item.py --queue "queue-abc" --trace "trace-xyz"
```

## API Reference

```
POST /api/public/annotation-queues/{id}/items
```
