---
name: langfuse-create-prompt
description: "Create a new Langfuse prompt. Load when user says 'create prompt', 'new prompt', 'add prompt'."
---

# Create Prompt

Create a new prompt in Langfuse with versioning support.

## Usage

### CLI
```bash
# Create a text prompt
python scripts/create_prompt.py --name "my-prompt" --prompt "You are a helpful assistant"

# Create a chat prompt
python scripts/create_prompt.py --name "chat-prompt" --type chat --prompt '[{"role": "system", "content": "You are helpful"}]'

# With labels and config
python scripts/create_prompt.py --name "prod-prompt" --prompt "..." --labels production --config '{"temperature": 0.7}'
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| --name | string | **Required**. Prompt name (unique identifier) |
| --prompt | string | **Required**. Prompt content (text or JSON for chat) |
| --type | string | Prompt type: "text" (default) or "chat" |
| --labels | string | Comma-separated labels (e.g., "production,v1") |
| --config | JSON | Model config (temperature, max_tokens, etc.) |

## API Reference

```
POST /api/public/v2/prompts
```

Request Body:
```json
{
  "name": "my-prompt",
  "prompt": "You are a helpful assistant",
  "type": "text",
  "labels": ["production"],
  "config": {"temperature": 0.7}
}
```
