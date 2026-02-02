# Langfuse Setup Guide

## Prerequisites

1. Langfuse account (cloud or self-hosted)
2. API keys from Langfuse project settings

## Getting API Keys

1. Go to your Langfuse instance (e.g., https://tracing.beamstudio.ai)
2. Navigate to **Settings** → **API Keys**
3. Create new API key pair
4. Copy both Public Key and Secret Key

## Configuration

Add to your `.env` file:

```bash
# Langfuse Integration (LLM Observability)
LANGFUSE_SECRET_KEY=sk-lf-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
LANGFUSE_PUBLIC_KEY=pk-lf-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
LANGFUSE_HOST=https://tracing.beamstudio.ai
```

### Host Options

| Instance | Host URL |
|----------|----------|
| Cloud EU | https://cloud.langfuse.com |
| Cloud US | https://us.cloud.langfuse.com |
| Self-hosted | Your instance URL |

## Verify Configuration

```bash
uv run python 00-system/skills/langfuse/langfuse-master/scripts/check_langfuse_config.py --test
```

Expected output:
```
[OK] Langfuse configuration valid
     Host: https://tracing.beamstudio.ai
     [OK] Connection test passed - Project: YourProjectName
```

## Python SDK (Optional)

For direct SDK usage:

```bash
pip install langfuse
```

```python
from langfuse import Langfuse

langfuse = Langfuse()  # Auto-reads from env vars
```

## Troubleshooting

### "Missing credentials" error
- Verify `.env` file exists in project root
- Check variable names match exactly
- Ensure no extra spaces around values

### "Connection failed" error
- Verify LANGFUSE_HOST is correct
- Check network/firewall settings
- Ensure API keys have correct permissions

### "401 Unauthorized" error
- Public and Secret keys may be swapped
- Keys may be expired or revoked
- Wrong project/organization
