---
name: langfuse-create-queue-assignment
description: "Assign reviewer to queue. Load when user says 'assign reviewer', 'add to queue assignment'."
---

# Create Queue Assignment

Assign a user to an annotation queue.

## Usage

```bash
uv run python scripts/create_queue_assignment.py --queue "queue-abc" --user "user@email.com"
```

## API Reference

```
POST /api/public/annotation-queues/{id}/assignments
```
