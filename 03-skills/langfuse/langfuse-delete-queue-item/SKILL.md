---
name: langfuse-delete-queue-item
description: "Delete a queue item. Load when user says 'delete queue item', 'remove from queue'."
---

# Delete Queue Item

Remove an item from annotation queue.

## Usage

```bash
python scripts/delete_queue_item.py --queue "queue-abc" --item "item-xyz"
```

## API Reference

```
DELETE /api/public/annotation-queues/{id}/items/{itemId}
```
