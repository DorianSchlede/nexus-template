# MCP Server Setup Guide

**Complete installation and configuration instructions**

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation Process](#installation-process)
- [Configuration Format](#configuration-format)
- [Tool-Specific Credentials](#tool-specific-credentials)
  - [GitHub](#github)
  - [Slack](#slack)
  - [Google Drive](#google-drive)
  - [Notion](#notion)
  - [Linear](#linear)
  - [PostgreSQL](#postgresql)
  - [Obsidian](#obsidian)
  - [File System](#file-system)
- [Security Best Practices](#security-best-practices)
- [Testing Your Setup](#testing-your-setup)
- [Common Configuration Mistakes](#common-configuration-mistakes)
- [Validation Tools](#validation-tools)
- [Updating Integrations](#updating-integrations)
- [Resources](#resources)

---

## Prerequisites

### Node.js and npm

**Required**: MCP servers run via npx, which requires Node.js

**Check if installed**:
```bash
node --version
npm --version
```

**If not installed**:
1. Visit: https://nodejs.org/
2. Download LTS version (recommended)
3. Run installer
4. Restart terminal/command prompt
5. Verify installation with commands above

**Versions**:
- Node.js: 16.x or higher
- npm: Comes automatically with Node.js

---

## Installation Process

### Step 1: Install MCP Server

MCP servers are installed via npx (no permanent installation needed).

**Generic command**:
```bash
npx -y @modelcontextprotocol/server-{tool-name}
```

**What npx does**:
- Downloads the MCP server package
- Installs dependencies temporarily
- Runs the server when Claude needs it
- Auto-updates to latest version each time

**No manual updates needed!**

### Step 2: Get API Credentials

Each tool requires API credentials (keys, tokens, etc.).

**Common credential types**:
- **API Keys**: Single token (simple)
- **OAuth Tokens**: Access + refresh tokens (complex)
- **App Credentials**: Client ID + Secret (enterprise)
- **Personal Access Tokens**: User-specific (GitHub, GitLab)

See [Tool-Specific Credentials](#tool-specific-credentials) below for details.

### Step 3: Configure Claude

Add MCP server to Claude's configuration file.

**Configuration file location**:

| Platform | Path |
|----------|------|
| macOS | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Windows | `%APPDATA%\Claude\claude_desktop_config.json` |
| Linux | `~/.config/Claude/claude_desktop_config.json` |

**For Claude Code (VS Code)**:
- Configure via VS Code settings
- Search for "MCP" in settings
- Or edit settings.json directly

### Step 4: Restart Claude

**CRITICAL**: MCP servers only load on Claude startup.

After editing config:
1. Save the file
2. Quit Claude completely
3. Restart Claude
4. MCP servers will load automatically

**No restart = No connection!**

---

## Configuration Format

### Basic Template

```json
{
  "mcpServers": {
    "{tool-name}": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-{tool-name}"],
      "env": {
        "{TOKEN_VARIABLE}": "your_actual_token_here"
      }
    }
  }
}
```

**Replace**:
- `{tool-name}`: Lowercase tool name (github, slack, etc.)
- `{TOKEN_VARIABLE}`: Environment variable name (see tool-specific)
- `your_actual_token_here`: Your actual API key/token

### Multiple Integrations

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_abc123..."
      }
    },
    "slack": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-slack"],
      "env": {
        "SLACK_BOT_TOKEN": "xoxb-123...",
        "SLACK_APP_TOKEN": "xapp-456..."
      }
    },
    "gdrive": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-gdrive"],
      "env": {
        "GDRIVE_CLIENT_ID": "abc.apps.googleusercontent.com",
        "GDRIVE_CLIENT_SECRET": "secret123"
      }
    }
  }
}
```

**Important**:
- Commas between entries (but NOT after last entry)
- Quotes around all strings
- Braces properly matched
- Use JSON validator if unsure: https://jsonlint.com/

---

## Tool-Specific Credentials

### GitHub

**Get Token**:
1. Go to: https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Name: "Nexus MCP Integration"
4. Scopes needed:
   - ✓ `repo` (full repository access)
   - ✓ `workflow` (optional, for CI/CD)
   - ✓ `read:org` (optional, for org access)
5. Click "Generate token"
6. **Copy immediately** (won't see again!)

**Configuration**:
```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_your_token_here"
      }
    }
  }
}
```

**Environment Variable**: `GITHUB_PERSONAL_ACCESS_TOKEN`

---

### Slack

**Get Tokens**:
1. Create Slack App: https://api.slack.com/apps
2. Enable "Socket Mode"
3. Add OAuth scopes:
   - `chat:write` (send messages)
   - `channels:read` (list channels)
   - `channels:history` (read messages)
4. Install app to workspace
5. Copy tokens:
   - Bot Token: Starts with `xoxb-`
   - App Token: Starts with `xapp-`

**Configuration**:
```json
{
  "mcpServers": {
    "slack": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-slack"],
      "env": {
        "SLACK_BOT_TOKEN": "xoxb-your-bot-token",
        "SLACK_APP_TOKEN": "xapp-your-app-token"
      }
    }
  }
}
```

**Environment Variables**:
- `SLACK_BOT_TOKEN`
- `SLACK_APP_TOKEN`

---

### Google Drive

**Get Credentials**:
1. Go to: https://console.cloud.google.com/
2. Create build (or use existing)
3. Enable Google Drive API
4. Create OAuth 2.0 credentials
5. Download client_id and client_secret

**Configuration**:
```json
{
  "mcpServers": {
    "gdrive": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-gdrive"],
      "env": {
        "GDRIVE_CLIENT_ID": "123456.apps.googleusercontent.com",
        "GDRIVE_CLIENT_SECRET": "your_client_secret"
      }
    }
  }
}
```

**Environment Variables**:
- `GDRIVE_CLIENT_ID`
- `GDRIVE_CLIENT_SECRET`

**First use**: Will prompt for OAuth authorization in browser

---

### Notion

**Get Token**:
1. Go to: https://www.notion.so/my-integrations
2. Create new integration
3. Name: "Nexus MCP"
4. Copy "Internal Integration Token"
5. Share pages with integration (important!)

**Configuration**:
```json
{
  "mcpServers": {
    "notion": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-notion"],
      "env": {
        "NOTION_API_KEY": "secret_your_api_key"
      }
    }
  }
}
```

**Environment Variable**: `NOTION_API_KEY`

**Remember**: Must share pages with integration!

---

### Linear

**Get Token**:
1. Go to: Linear → Settings → API
2. Create Personal API Key
3. Name: "Nexus MCP"
4. Copy token

**Configuration**:
```json
{
  "mcpServers": {
    "linear": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-linear"],
      "env": {
        "LINEAR_API_KEY": "lin_api_your_key"
      }
    }
  }
}
```

**Environment Variable**: `LINEAR_API_KEY`

---

### PostgreSQL

**Setup**:
1. Have PostgreSQL database running
2. Get connection string
3. Format: `postgresql://user:password@host:port/database`

**Configuration**:
```json
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "POSTGRES_CONNECTION_STRING": "postgresql://user:pass@localhost:5432/mydb"
      }
    }
  }
}
```

**Environment Variable**: `POSTGRES_CONNECTION_STRING`

**Security**: Use read-only user when possible!

---

### Obsidian

**Setup**:
1. Ensure Obsidian vault exists on your machine
2. Get vault path

**Configuration**:
```json
{
  "mcpServers": {
    "obsidian": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-obsidian"],
      "env": {
        "OBSIDIAN_VAULT_PATH": "/path/to/your/vault"
      }
    }
  }
}
```

**Environment Variable**: `OBSIDIAN_VAULT_PATH`

**Path format**:
- macOS/Linux: `/Users/name/Documents/MyVault`
- Windows: `C:\\Users\\name\\Documents\\MyVault`

---

### File System

**Setup**:
1. Choose allowed directories
2. Configure paths (for security)

**Configuration**:
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem"],
      "env": {
        "ALLOWED_DIRECTORIES": "/path/to/allowed/dir1:/path/to/allowed/dir2"
      }
    }
  }
}
```

**Environment Variable**: `ALLOWED_DIRECTORIES`

**Multiple paths**: Separate with `:` (colon)

---

## Security Best Practices

### API Key Management

1. **Never commit to git**
   - Add config file to `.gitignore`
   - Never paste in public channels
   - Don't screenshot with keys visible

2. **Use minimal permissions**
   - Grant only necessary scopes
   - Start with read-only when possible
   - Increase permissions as needed

3. **Rotate regularly**
   - Change keys every 3-6 months
   - Rotate immediately if compromised
   - Document rotation schedule

4. **Store securely**
   - Config file has restricted permissions
   - Use password managers for backup
   - Never email or share keys

### Configuration File Security

**macOS/Linux - Set permissions**:
```bash
chmod 600 ~/Library/Application Support/Claude/claude_desktop_config.json
```

This ensures only you can read the file.

**Windows - Check file permissions**:
- Right-click config file → Properties → Security
- Ensure only your user has access

### What to Do if Key Compromised

1. **Revoke immediately** in the tool's settings
2. **Generate new key** with same permissions
3. **Update config** with new key
4. **Restart Claude**
5. **Review usage logs** for unauthorized access
6. **Document incident** in 01-memory/core-learnings.md

---

## Testing Your Setup

### After Configuration

**Test each integration**:

| Tool | Test Command |
|------|--------------|
| GitHub | "List my GitHub repositories" |
| Slack | "List Slack channels" |
| Google Drive | "Show files in my Google Drive" |
| Notion | "List my Notion pages" |
| Linear | "Show my Linear issues" |
| PostgreSQL | "Show database tables" |
| Obsidian | "List notes in my Obsidian vault" |
| File System | "List files in [allowed directory]" |

**Expected result**: Claude successfully connects and returns data

**If fails**: See [Troubleshooting Guide](troubleshooting-guide.md)

---

## Common Configuration Mistakes

### 1. Syntax Errors

**Wrong** (no comma between entries):
```json
{
  "mcpServers": {
    "github": {...}
    "slack": {...}  ← Missing comma!
  }
}
```

**Right**:
```json
{
  "mcpServers": {
    "github": {...},
    "slack": {...}
  }
}
```

### 2. Trailing Comma

**Wrong** (comma after last entry):
```json
{
  "mcpServers": {
    "github": {...},  ← Extra comma!
  }
}
```

**Right**:
```json
{
  "mcpServers": {
    "github": {...}
  }
}
```

### 3. Missing Quotes

**Wrong**:
```json
{
  "mcpServers": {
    github: {...}  ← Missing quotes!
  }
}
```

**Right**:
```json
{
  "mcpServers": {
    "github": {...}
  }
}
```

### 4. Wrong Token Variable Name

Each tool expects specific environment variable names. Check tool-specific sections above for correct names.

### 5. File Path Escaping (Windows)

**Wrong**:
```json
"OBSIDIAN_VAULT_PATH": "C:\Users\name\vault"  ← Single backslashes fail!
```

**Right**:
```json
"OBSIDIAN_VAULT_PATH": "C:\\Users\\name\\vault"  ← Double backslashes or forward slashes
```

---

## Validation Tools

### JSON Validator

Before saving config, validate JSON syntax:

**Online**: https://jsonlint.com/
1. Paste your config
2. Click "Validate JSON"
3. Fix any errors shown

**Command line** (if you have jq):
```bash
cat claude_desktop_config.json | jq .
```

### MCP Server Test

Test if npx can run the server:
```bash
npx -y @modelcontextprotocol/server-{tool-name} --version
```

Should download and show version number.

---

## Updating Integrations

### Changing Credentials

1. Edit config file
2. Update token value
3. Save file
4. **Restart Claude** (required!)

### Adding New Integration

1. Follow setup for new tool
2. Add entry to `mcpServers` object
3. Remember comma after previous entry
4. Save and restart Claude

### Removing Integration

1. Delete entry from `mcpServers`
2. Fix commas (no trailing commas!)
3. Save and restart Claude

Or just comment out with `// ` (but remember JSON doesn't officially support comments, so some parsers may fail)

---

## Resources

- **MCP Server Directory**: https://github.com/modelcontextprotocol/servers
- **MCP Documentation**: https://modelcontextprotocol.io/
- **JSON Validator**: https://jsonlint.com/
- **Node.js Download**: https://nodejs.org/
- **Troubleshooting Guide**: [troubleshooting-guide.md](troubleshooting-guide.md)
