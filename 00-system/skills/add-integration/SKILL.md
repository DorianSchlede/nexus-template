---
name: add-integration
description: Guide MCP server setup to connect external tools to Nexus. Load when user mentions "add integration", "connect tool", "setup MCP", or "integrate with". Walks through installation, configuration, credential setup, testing, and documentation of integrations like GitHub, Slack, Notion, and Google Drive.
---

# Add Integration

Guide MCP server setup to connect external tools to Nexus.

## Purpose

The `add-integration` skill helps you connect external tools and services to Nexus via MCP (Model Context Protocol). It guides you through installation, configuration, testing, and documentation of integrations like GitHub, Slack, Notion, Google Drive, and more.

**Key Features:**
- **MCP Explanation**: Clear intro to what MCP is and why it's useful
- **Tool Selection**: Helps identify which MCP servers fit your needs
- **Setup Guidance**: Step-by-step installation and configuration
- **Connection Testing**: Verifies integration works
- **Documentation**: Records integration in Memory for future reference

**Time Estimate**: 10-20 minutes (depending on tool complexity)

---

## Workflow

### Step 1: Initialize TodoList

Create TodoWrite with all workflow steps:
```
- [ ] Display MCP introduction
- [ ] Ask which tool to connect
- [ ] Check MCP server availability
- [ ] Retrieve latest API documentation via Context7
- [ ] Guide through installation
- [ ] Guide through configuration
- [ ] Test connection
- [ ] Document integration
- [ ] Display success
- [ ] Close session to save progress
```

**Mark tasks complete as you finish each step.**

---

### Step 2: Display MCP Introduction

**For complete MCP overview**: See [references/mcp-introduction.md](references/mcp-introduction.md)

**Brief explanation to user:**

```
Let me help you connect external tools to Nexus! 🔌

**What is MCP (Model Context Protocol)?**

MCP is like a universal adapter that lets me (Claude) interact with
external tools and data sources. Think of it as building bridges between
Nexus and the tools you already use.

**Popular integrations:**
- GitHub (repos, issues, PRs)
- Slack (messaging, notifications)
- Google Drive (file storage)
- Notion (notes, databases)
- Linear (issue tracking)
- And many more...

**How it works:**
1. Install an MCP server (small program for the tool)
2. Configure connection (API keys, credentials)
3. I can now read/write data from that tool
4. Use it naturally in your Nexus workflows

Want to add an integration? I'll guide you through it step-by-step!
```

**Wait for user acknowledgment.**

---

### Step 3: Ask Which Tool to Connect

Display:
```
Which tool would you like to connect?

**Popular options:**
- GitHub (code repos, issues, PRs)
- Slack (messaging, notifications)
- Google Drive (file storage, sharing)
- Notion (notes, databases, pages)
- Linear (issue tracking, projects)
- Jira, Trello, PostgreSQL, Obsidian, File System

Just tell me the tool name, or say "show me more options" for the full list.
```

**Wait for user response.**

**Capture tool name:**
- Normalize input (e.g., "github", "GitHub", "GITHUB" → "github")
- Validate against known MCP servers
- Store for later steps

---

### Step 4: Check MCP Server Availability

**Check if tool has MCP server:**

**Known MCP servers**:
github, slack, gdrive, notion, linear, jira, trello, postgres, obsidian, filesystem

**Full directory**: https://github.com/modelcontextprotocol/servers

---

**IF tool has known MCP server:**

Display:
```
✅ Great choice! {Tool} has an official MCP server.

I'll guide you through:
1. Installing the MCP server
2. Getting necessary credentials (API keys, tokens)
3. Configuring the connection
4. Testing it works

Ready to start? (This will take about 10-15 minutes)
```

**Wait for confirmation.**

---

**IF tool doesn't have known MCP server:**

Display:
```
⚠️  I don't see an official MCP server for {Tool}.

Options:
1. Check the MCP directory: https://github.com/modelcontextprotocol/servers
2. Request from community: https://github.com/modelcontextprotocol/discussions
3. Build custom server: https://modelcontextprotocol.io/docs/custom-servers
4. Choose different tool: Pick one with existing support

What would you like to do?
```

**Handle user response appropriately.**

---

### Step 5: Retrieve Latest API Documentation (Context7)

🔥 **CRITICAL: Use Context7 MCP for up-to-date API documentation!**

**Before providing installation/configuration guidance:**

```python
# Use Context7 to get latest library documentation
1. Resolve library ID: resolve-library-id("{tool-name}")
2. Get documentation: get-library-docs(library_id, topic="authentication setup configuration")
```

**Why this matters:**
- API endpoints change frequently
- OAuth scopes get updated
- New authentication methods emerge
- Configuration formats evolve

**Example usage:**
```
For Gmail: resolve-library-id("gmail-api") → get-library-docs("/googleapis/google-api-python-client", topic="gmail authentication oauth")
For GitHub: resolve-library-id("github api") → get-library-docs("/octokit/rest.js", topic="authentication tokens")
For Slack: resolve-library-id("slack api") → get-library-docs("/slackapi/node-slack-sdk", topic="oauth configuration")
```

**Use retrieved documentation to:**
- ✅ Provide accurate credential setup steps
- ✅ List current required scopes/permissions
- ✅ Show latest configuration format
- ✅ Include any breaking changes or deprecations

**If Context7 unavailable:** Fall back to reference files, but note documentation may be outdated.

---

### Step 6: Guide Through Installation

**For detailed setup instructions**: See [references/mcp-setup-guide.md](references/mcp-setup-guide.md)

**Provide concise installation guidance:**

```
Step 1: Install the MCP Server

**Prerequisites:**
- Node.js installed (check: `node --version`)
- If not installed, download from: https://nodejs.org/

**Installation:**
The MCP server installs via npx (no permanent installation needed):

```bash
npx -y @modelcontextprotocol/server-{tool}
```

This downloads the {Tool} MCP server automatically.

**Ready to proceed?** Say "next" when you've verified Node.js is installed.
```

**Wait for user confirmation.**

---

### Step 7: Guide Through Configuration

**For complete configuration guide**: See [references/mcp-setup-guide.md#tool-specific-credentials](references/mcp-setup-guide.md)

**💡 Use Context7 documentation from Step 5 for accurate, up-to-date credential instructions!**

**Step 7a: Get API Credentials**

Guide user to get credentials:
```
Step 2: Get {Tool} API Credentials

[Provide tool-specific instructions]

Example for GitHub:
1. Go to https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Name: "Nexus MCP Integration"
4. Select scopes: ✓ repo, ✓ workflow
5. Generate and copy token immediately

Once you have your credentials, say "I have the credentials".
```

**Wait for user confirmation.**

---

**Step 7b: Configure MCP Server**

Provide configuration instructions:
```
Step 3: Configure Claude to Use {Tool}

**Config file location:**
- macOS: ~/Library/Application Support/Claude/claude_desktop_config.json
- Windows: %APPDATA%\Claude\claude_desktop_config.json
- Linux: ~/.config/Claude/claude_desktop_config.json

**Add this configuration:**

```json
{
  "mcpServers": {
    "{tool}": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-{tool}"],
      "env": {
        "{TOKEN_NAME}": "your_token_here"
      }
    }
  }
}
```

Replace `your_token_here` with your actual token.

**After editing:**
1. Save the file
2. **Restart Claude** (important!)
3. Say "I've configured it"

For detailed examples and troubleshooting, see:
[references/mcp-setup-guide.md](references/mcp-setup-guide.md)
```

**Wait for user confirmation.**

---

### Step 8: Test Connection

Guide user through connection test:
```
Step 4: Test the Integration

**Restarted Claude?** If not, please restart now.

**Test command for {Tool}:**

[Tool-specific test examples:]
- GitHub: "List my GitHub repositories"
- Slack: "List Slack channels"
- Google Drive: "Show files in my Google Drive"
- Notion: "List my Notion pages"

Try that command now!
```

**Wait for user to try command.**

**Attempt connection:**
- Try to execute test command via MCP
- IF succeeds → Display success, proceed to Step 8
- IF fails → Show error, refer to troubleshooting

---

**IF connection succeeds:**

```
✅ Connection successful!

I was able to connect to {Tool} and {what you did}.

Your integration is working! You can now use {Tool} features
directly in Nexus workflows.

**Example uses:**
- [Use case 1]
- [Use case 2]
- [Use case 3]

Let me document this integration in your Memory...
```

Proceed to Step 9.

---

**IF connection fails:**

```
❌ Connection failed.

Error: {error message}

**Quick troubleshooting:**
1. Verify API key is correct (no typos, no extra spaces)
2. Check token permissions/scopes
3. Verify JSON syntax in config file
4. Confirm you restarted Claude
5. Test npx: `npx -y @modelcontextprotocol/server-{tool} --version`

For detailed troubleshooting: [references/troubleshooting-guide.md](references/troubleshooting-guide.md)

Want to try troubleshooting, or pause and revisit later?
```

**Wait for user response.**

---

### Step 9: Document Integration

Update 01-memory/core-learnings.md:

Load `01-memory/core-learnings.md`

**Add integration entry** to "## Integrations" section:

```markdown
### {Tool Name}
**Connected**: {YYYY-MM-DD}
**MCP Server**: @modelcontextprotocol/server-{tool}
**Use For**: {Purpose based on tool}
**Setup Notes**:
- API Key: {masked version}
- Permissions: {what permissions granted}
- Config Location: {path to config file}

**Example Uses**:
- {Use case 1}
- {Use case 2}

**Tested**: {YYYY-MM-DD} - ✅ Working
```

Write updated file.

Confirm: `✓ Integration documented in 01-memory/core-learnings.md`

---

### Step 10: Display Success Summary

Show complete integration summary:
```
✅ Integration Complete!

🔌 {Tool} is now connected to Nexus!

---

**What you can do now:**
- {Feature 1}
- {Feature 2}
- {Feature 3}

**Documented in:**
- 01-memory/core-learnings.md (integration details)

**Configuration:**
- MCP Server: @modelcontextprotocol/server-{tool}
- Config File: {path}

---

**For more ideas**: See [references/integration-ideas.md](references/integration-ideas.md)

**Tips:**
- Test integration regularly
- Rotate API keys periodically (3-6 months)
- Check tool docs for advanced features

**Need another integration?** Just say "add integration" again!

Your integration is ready to use! 🎉
```

---

### Final Step: Close Session

Auto-trigger the `close-session` skill:

```
Auto-triggering close-session to save your integration...

[close-session workflow executes]

Session saved! ✅

Your {Tool} integration is documented and ready! 🚀
```

---

## Error Handling

**For comprehensive error scenarios**: See [references/troubleshooting-guide.md](references/troubleshooting-guide.md)

### Quick Reference

| Issue | Solution |
|-------|----------|
| Node.js Not Installed | Download from https://nodejs.org/ |
| API Key Invalid | Regenerate token, update config, restart Claude |
| Config File Syntax Error | Validate JSON at https://jsonlint.com/ |
| MCP Server Not Responding | Verify config location, check Claude restarted |
| Tool Not Supported | Check https://github.com/modelcontextprotocol/servers |
| Permissions Insufficient | Add required scopes to token |
| Multiple Integration Conflicts | Check for duplicate keys in JSON |

**For detailed troubleshooting steps**: See troubleshooting guide reference file.

---

## Notes

**Why MCP?**
- **Universal**: One protocol for many tools
- **Secure**: API keys stay on your machine
- **Flexible**: Extend Nexus without modifying core
- **Optional**: Nexus works perfectly standalone

**Security Best Practices:**
- Never share API keys publicly
- Use read-only keys when possible
- Rotate keys periodically (3-6 months)
- Review permissions granted
- Keep config file secure

**Integration Ideas:**
For creative ways to use integrations, see:
- [references/integration-ideas.md](references/integration-ideas.md)

**Examples**:
- GitHub: Create issues from tasks
- Slack: Send project updates
- Notion: Sync Memory to Notion
- Google Drive: Auto-backup outputs
- Obsidian: Sync to vault

**Resources:**
- MCP Documentation: https://modelcontextprotocol.io/
- MCP Server Directory: https://github.com/modelcontextprotocol/servers
- MCP Discussions: https://github.com/modelcontextprotocol/discussions

---

**Remember**: Integrations are powerful but optional. Add them only when they add clear value to your workflow. Nexus works perfectly standalone!
