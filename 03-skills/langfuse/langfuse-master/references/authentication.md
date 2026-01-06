# Langfuse Authentication

## Method: Basic Auth

Langfuse uses HTTP Basic Authentication:
- **Username**: Public Key (`pk-lf-...`)
- **Password**: Secret Key (`sk-lf-...`)

## How It Works

```
Authorization: Basic base64(public_key:secret_key)
```

The client automatically handles this:

```python
from langfuse_client import get_client

client = get_client()  # Reads from env vars
```

## Key Types

### Public Key (`pk-lf-...`)
- Safe to expose in logs (limited permissions)
- Used as username in Basic Auth
- Identifies the project

### Secret Key (`sk-lf-...`)
- **NEVER expose** - treat like a password
- Used as password in Basic Auth
- Full API access

## Environment Variables

```bash
LANGFUSE_PUBLIC_KEY=pk-lf-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
LANGFUSE_SECRET_KEY=sk-lf-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
LANGFUSE_HOST=https://tracing.beamstudio.ai
```

## Security Best Practices

1. **Never commit keys** - Use `.env` files (gitignored)
2. **Rotate regularly** - Create new keys periodically
3. **Limit scope** - Use project-level keys, not org-level
4. **Monitor usage** - Check for unexpected API calls

## Troubleshooting

### 401 Unauthorized
- Keys may be swapped (public vs secret)
- Keys may be expired
- Wrong project

### 403 Forbidden
- Key lacks permissions for operation
- Organization-level restriction

### Connection Refused
- Wrong LANGFUSE_HOST
- Network/firewall issue
