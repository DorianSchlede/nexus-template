---
name: langfuse-delete-prompt
description: "Delete a Langfuse prompt. Load when user says 'delete prompt', 'remove prompt'."
---

# Delete Prompt

Delete a prompt from Langfuse by name. This deletes all versions of the prompt.

## Usage

### CLI
```bash
python scripts/delete_prompt.py --name "my-prompt"
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| --name | string | **Required**. Prompt name to delete |

## API Reference

```
DELETE /api/public/v2/prompts/{promptName}
```

**Warning**: This deletes all versions of the prompt. This action cannot be undone.
