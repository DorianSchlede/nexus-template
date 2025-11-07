# MCP Integration Guide

> Model Context Protocol (MCP) - Connect external tools to Nexus

## Table of Contents

- [What is MCP?](#what-is-mcp)
- [Common MCP Servers](#common-mcp-servers)
- [How to Get API Keys](#how-to-get-api-keys)
- [MCP Configuration File Location](#mcp-configuration-file-location)
- [Testing MCP Connection](#testing-mcp-connection)
- [Security Best Practices](#security-best-practices)
- [Custom MCP Servers](#custom-mcp-servers)
- [Troubleshooting](#troubleshooting)
- [Integration Ideas for Nexus](#integration-ideas-for-nexus)

---

## What is MCP?

**Model Context Protocol (MCP)** is an open protocol that allows Claude to connect to external tools and data sources. Think of it as a universal adapter that lets Claude interact with:

- **Project Management**: GitHub, Linear, Jira, Asana, Trello
- **Communication**: Slack, Discord, Microsoft Teams
- **Storage**: Google Drive, Dropbox, Notion, Obsidian
- **Databases**: PostgreSQL, MySQL, SQLite
- **APIs**: Custom REST APIs, GraphQL endpoints
- **And more...**

**How it works:**
1. Install an MCP server (small program that connects to a tool)
2. Configure connection (API keys, credentials)
3. Claude can now read/write data from that tool
4. Use it naturally in your workflows

**Official Resources:**
- MCP Documentation: https://modelcontextprotocol.io/
- MCP Server Directory: https://github.com/modelcontextprotocol/servers

---

## Common MCP Servers

### GitHub MCP
**What it does**: Read repos, create issues, manage PRs, review code

**Installation**:
```bash
npx -y @modelcontextprotocol/server-github
```

**Configuration**:
```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "your_token_here"
      }
    }
  }
}
```

**Use Cases**:
- Track project issues in GitHub from Nexus
- Create PRs based on project tasks
- Review code directly in conversation

---

### Google Drive MCP
**What it does**: Read/write files, manage folders, share documents

**Installation**:
```bash
npx -y @modelcontextprotocol/server-gdrive
```

**Configuration**:
```json
{
  "mcpServers": {
    "gdrive": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-gdrive"],
      "env": {
        "GOOGLE_API_KEY": "your_api_key_here",
        "GOOGLE_CLIENT_ID": "your_client_id_here",
        "GOOGLE_CLIENT_SECRET": "your_client_secret_here"
      }
    }
  }
}
```

**Use Cases**:
- Store project outputs in Google Drive
- Sync deliverables automatically
- Collaborate with team on documents

---

### Slack MCP
**What it does**: Send messages, read channels, manage notifications

**Installation**:
```bash
npx -y @modelcontextprotocol/server-slack
```

**Configuration**:
```json
{
  "mcpServers": {
    "slack": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-slack"],
      "env": {
        "SLACK_BOT_TOKEN": "xoxb-your-token-here",
        "SLACK_APP_TOKEN": "xapp-your-token-here"
      }
    }
  }
}
```

**Use Cases**:
- Send project updates to Slack channels
- Notify team when milestones complete
- Get notifications from Nexus in Slack

---

### Notion MCP
**What it does**: Read/write pages, manage databases, sync content

**Installation**:
```bash
npx -y @modelcontextprotocol/server-notion
```

**Configuration**:
```json
{
  "mcpServers": {
    "notion": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-notion"],
      "env": {
        "NOTION_API_KEY": "secret_your_key_here"
      }
    }
  }
}
```

**Use Cases**:
- Sync Nexus projects to Notion databases
- Export deliverables to Notion pages
- Mirror tasks between Nexus and Notion

---

### Linear MCP
**What it does**: Create issues, manage projects, track progress

**Installation**:
```bash
npx -y @modelcontextprotocol/server-linear
```

**Configuration**:
```json
{
  "mcpServers": {
    "linear": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-linear"],
      "env": {
        "LINEAR_API_KEY": "lin_api_your_key_here"
      }
    }
  }
}
```

**Use Cases**:
- Sync Nexus tasks to Linear issues
- Track engineering work alongside business work
- Close-loop between planning and execution

---

### PostgreSQL MCP
**What it does**: Query databases, read/write data, manage schemas

**Installation**:
```bash
npx -y @modelcontextprotocol/server-postgres
```

**Configuration**:
```json
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "POSTGRES_CONNECTION_STRING": "postgresql://user:password@localhost:5432/database"
      }
    }
  }
}
```

**Use Cases**:
- Query data for analysis in projects
- Store structured project metadata
- Generate reports from database data

---

### File System MCP (Local Files)
**What it does**: Read/write local files, manage directories

**Installation**:
```bash
npx -y @modelcontextprotocol/server-filesystem
```

**Configuration**:
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/allowed/path/here"]
    }
  }
}
```

**Use Cases**:
- Access files outside Nexus directory
- Read reference materials
- Write outputs to specific locations

---

### Obsidian MCP
**What it does**: Read/write Obsidian notes, manage vault

**Installation**:
```bash
npx -y @modelcontextprotocol/server-obsidian
```

**Configuration**:
```json
{
  "mcpServers": {
    "obsidian": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-obsidian"],
      "env": {
        "OBSIDIAN_VAULT_PATH": "/path/to/your/obsidian/vault"
      }
    }
  }
}
```

**Use Cases**:
- Sync Nexus Memory/ to Obsidian vault
- Visualize project relationships in Obsidian graph
- Dual-mode: Nexus for workflows, Obsidian for notes

---

## How to Get API Keys

### GitHub Token
1. Go to https://github.com/settings/tokens
2. Generate new token (classic)
3. Select scopes: `repo`, `workflow`
4. Copy token immediately (shown once)

### Google API Credentials
1. Go to https://console.cloud.google.com/
2. Create new project or select existing
3. Enable Google Drive API
4. Create credentials (OAuth 2.0 Client ID)
5. Download JSON credentials

### Slack Tokens
1. Go to https://api.slack.com/apps
2. Create new app or select existing
3. Install app to workspace
4. Copy Bot User OAuth Token (xoxb-...)
5. Copy App-Level Token (xapp-...)

### Notion Integration Token
1. Go to https://www.notion.so/my-integrations
2. Create new integration
3. Copy Internal Integration Token
4. Share pages with integration

### Linear API Key
1. Go to https://linear.app/settings/api
2. Create new API key
3. Copy key immediately (shown once)

---

## MCP Configuration File Location

**Claude Desktop**:
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

**Claude Code** (VS Code Extension):
- Configured via VS Code settings
- Search for "MCP" in settings
- Add servers via UI or settings.json

**Configuration Format**:
```json
{
  "mcpServers": {
    "server-name": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-name"],
      "env": {
        "API_KEY": "your_key_here"
      }
    },
    "another-server": {
      "command": "node",
      "args": ["/path/to/custom/server.js"],
      "env": {
        "CONFIG": "value"
      }
    }
  }
}
```

---

## Testing MCP Connection

After configuration, restart Claude and test:

**Test command examples:**
- GitHub: "List my GitHub repositories"
- Google Drive: "Show files in my Drive"
- Slack: "Send a test message to #general"
- Notion: "List my Notion pages"
- PostgreSQL: "Show tables in my database"

**If connection fails:**
1. Check API key is correct
2. Check token permissions/scopes
3. Verify server installed: `npx -y @modelcontextprotocol/server-name --version`
4. Check Claude config file syntax (valid JSON)
5. Restart Claude after config changes

---

## Security Best Practices

**API Keys:**
- Never share API keys publicly
- Use environment variables for sensitive data
- Rotate keys periodically
- Use read-only keys when possible

**Permissions:**
- Grant minimum necessary permissions
- Don't give full access unless required
- Review permissions regularly

**MCP Servers:**
- Only install from trusted sources
- Review server code before installing custom servers
- Keep servers updated for security patches

---

## Custom MCP Servers

You can write custom MCP servers for proprietary tools:

**Simple custom server (Node.js)**:
```javascript
// custom-server.js
const { MCPServer } = require('@modelcontextprotocol/sdk');

const server = new MCPServer({
  name: 'my-custom-server',
  version: '1.0.0',
});

server.registerTool({
  name: 'my-tool',
  description: 'Does something useful',
  inputSchema: {
    type: 'object',
    properties: {
      param: { type: 'string' }
    }
  },
  handler: async (input) => {
    // Your custom logic here
    return { result: 'success' };
  }
});

server.start();
```

**Configuration**:
```json
{
  "mcpServers": {
    "custom": {
      "command": "node",
      "args": ["/path/to/custom-server.js"]
    }
  }
}
```

**Resources:**
- MCP SDK: https://github.com/modelcontextprotocol/sdk
- Example servers: https://github.com/modelcontextprotocol/servers
- Custom server guide: https://modelcontextprotocol.io/docs/custom-servers

---

## Troubleshooting

### "MCP server not responding"
- Verify server is installed: `npx -y @modelcontextprotocol/server-name --version`
- Check config file syntax (valid JSON)
- Restart Claude
- Check server logs (if available)

### "Authentication failed"
- Verify API key is correct
- Check token hasn't expired
- Verify permissions/scopes are sufficient
- Try generating new token

### "Command not found"
- Ensure Node.js/npm installed
- Run `npx -y @modelcontextprotocol/server-name` manually to install
- Check PATH includes npm global bin directory

### "Permission denied"
- Check file system permissions
- Verify API key has necessary permissions
- Review tool access grants (GitHub, Notion, etc.)

---

## Integration Ideas for Nexus

### Project Management Integration
- Sync Nexus projects to Linear/Jira
- Auto-create issues from tasks.md
- Track progress bidirectionally

### Storage Integration
- Export project outputs to Google Drive
- Backup Memory/ to cloud storage
- Share deliverables via Notion

### Communication Integration
- Send project updates to Slack
- Notify team of milestone completions
- Create status reports via email

### Data Integration
- Query databases for project research
- Store structured project data
- Generate analytics from project history

### Knowledge Management Integration
- Sync Memory/ to Obsidian vault
- Create knowledge graph visualization
- Link projects to existing notes

---

**Remember**: MCP servers are powerful but optional. Nexus works perfectly standalone. Add integrations only when they add clear value to your workflow!
