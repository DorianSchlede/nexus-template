---
name: langfuse-get-prompt
description: "Get a Langfuse prompt by name. Load when user says 'get prompt', 'show prompt', 'prompt details'."
---

# Get Prompt

Retrieve a specific prompt from Langfuse by name, optionally with specific version or label.

## Usage

### CLI
```bash
# Get latest version
uv run python scripts/get_prompt.py --name "my-prompt"

# Get specific version
uv run python scripts/get_prompt.py --name "my-prompt" --version 2

# Get by label
uv run python scripts/get_prompt.py --name "my-prompt" --label production
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| --name | string | **Required**. Prompt name |
| --version | int | Specific version number |
| --label | string | Label to fetch (e.g., "production") |

## API Reference

```
GET /api/public/v2/prompts/{promptName}
```

Query Parameters:
- `version` (int): Specific version number
- `label` (string): Label to fetch
