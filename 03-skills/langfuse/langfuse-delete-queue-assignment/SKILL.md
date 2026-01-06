---
name: langfuse-delete-queue-assignment
description: "Remove reviewer from queue. Load when user says 'remove assignment', 'unassign reviewer'."
---

# Delete Queue Assignment

Remove a user assignment from annotation queue.

## Usage

```bash
python scripts/delete_queue_assignment.py --queue "queue-abc" --user "user@email.com"
```

## API Reference

```
DELETE /api/public/annotation-queues/{id}/assignments
```
