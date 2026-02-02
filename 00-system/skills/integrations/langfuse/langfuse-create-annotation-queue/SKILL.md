---
name: langfuse-create-annotation-queue
description: "Create an annotation queue. Load when user says 'create queue', 'new annotation queue'."
---

# Create Annotation Queue

Create a new annotation queue for human review.

## Usage

```bash
uv run python scripts/create_annotation_queue.py --name "review-queue" --description "Production review"
```

## API Reference

```
POST /api/public/annotation-queues
```
