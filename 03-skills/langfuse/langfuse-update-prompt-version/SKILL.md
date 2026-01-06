---
name: langfuse-update-prompt-version
description: "Update a Langfuse prompt version labels. Load when user says 'update prompt', 'set prompt label', 'promote prompt'."
---

# Update Prompt Version

Update labels on a specific prompt version. Use this to promote versions to production or add/remove labels.

## Usage

### CLI
```bash
# Add production label to version 3
python scripts/update_prompt_version.py --name "my-prompt" --version 3 --labels production

# Set multiple labels
python scripts/update_prompt_version.py --name "my-prompt" --version 2 --labels "staging,reviewed"
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| --name | string | **Required**. Prompt name |
| --version | int | **Required**. Version number to update |
| --labels | string | Comma-separated labels to set |

## API Reference

```
PATCH /api/public/v2/prompts/{promptName}/versions/{version}
```

Request Body:
```json
{
  "labels": ["production", "v1"]
}
```
