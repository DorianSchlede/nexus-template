---
name: langfuse-create-dataset-run-item
description: "Create a dataset run item. Load when user says 'create run item', 'log evaluation', 'add run result'."
---

# Create Dataset Run Item

Link a trace/observation to a dataset item as part of an evaluation run.

## Usage

### CLI
```bash
# Link trace to dataset item
python scripts/create_dataset_run_item.py --run "run-2024-01" --dataset-item "item-123" --trace "trace-abc"

# With observation
python scripts/create_dataset_run_item.py --run "run-2024-01" --dataset-item "item-123" --observation "obs-xyz"
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| --run | string | **Required**. Run name |
| --dataset-item | string | **Required**. Dataset item ID |
| --trace | string | Trace ID to link |
| --observation | string | Observation ID to link |

## API Reference

```
POST /api/public/dataset-run-items
```
