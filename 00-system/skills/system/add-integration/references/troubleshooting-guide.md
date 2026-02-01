# MCP Integration Troubleshooting Guide

**Complete guide to fixing common MCP integration issues**

## Table of Contents

- [Quick Diagnosis](#quick-diagnosis)
- [Error Scenarios](#error-scenarios)
  - [1. Node.js Not Installed](#1-nodejs-not-installed)
  - [2. API Key Invalid or Expired](#2-api-key-invalid-or-expired)
  - [3. Insufficient Permissions/Scopes](#3-insufficient-permissionsscopes)
  - [4. Config File Syntax Error](#4-config-file-syntax-error)
  - [5. MCP Server Not Responding](#5-mcp-server-not-responding)
  - [6. Tool Not Supported by MCP](#6-tool-not-supported-by-mcp)
  - [7. Connection Succeeds But Features Don't Work](#7-connection-succeeds-but-features-dont-work)
  - [8. Multiple Integration Conflicts](#8-multiple-integration-conflicts)
  - [9. Credentials in Wrong Format](#9-credentials-in-wrong-format)
  - [10. Obsidian Vault Path Issues](#10-obsidian-vault-path-issues)
- [General Troubleshooting Steps](#general-troubleshooting-steps)
- [Prevention Tips](#prevention-tips)
- [Still Need Help?](#still-need-help)

---

## Quick Diagnosis

**Integration not working?** Start here:

1. [OK] **Verify Node.js installed** → `node --version`
2. [OK] **Check Claude was restarted** → After config changes
3. [OK] **Validate JSON syntax** → Use https://jsonlint.com/
4. [OK] **Confirm API key is correct** → No typos, not expired
5. [OK] **Check token permissions** → Has necessary scopes

Still not working? Find your specific issue below.

---

## Error Scenarios

### 1. Node.js Not Installed

**Symptoms**:
- Error: "node: command not found"
- npx commands fail
- MCP servers won't start

**Diagnosis**:
```bash
node --version
npm --version
```

If commands not found → Node.js not installed

**Solution**:
1. Visit: https://nodejs.org/
2. Download **LTS version** (recommended)
3. Run installer
4. Follow installation prompts
5. Restart terminal/command prompt
6. Verify: `node --version` should show version number

**Recommended Version**: Node.js 16.x or higher

---

### 2. API Key Invalid or Expired

**Symptoms**:
- "Authentication failed" error
- "Invalid token" message
- "Unauthorized" (401) responses
- Integration worked before, now doesn't

**Diagnosis**:
- Try using token directly in tool's web interface
- Check token expiration date
- Verify no typos in config file

**Solution**:

**Step 1: Regenerate Token**
1. Go to tool's settings page
2. Revoke old token (if still exists)
3. Generate new token
4. Copy immediately (some tokens can't be viewed again)

**Step 2: Update Config**
1. Open config file
2. Replace old token with new one
3. Verify no extra spaces or line breaks
4. Save file

**Step 3: Restart Claude**
- Quit completely
- Relaunch
- Test connection

**Common Token Issues**:
- **Expiration**: Some tokens expire (check tool settings)
- **Typos**: Extra space, missing character
- **Wrong type**: Using app token instead of bot token (Slack)
- **Revoked**: Token was manually revoked

---

### 3. Insufficient Permissions/Scopes

**Symptoms**:
- Connection successful but features don't work
- "Permission denied" errors
- Can read but not write (or vice versa)
- Some APIs work, others fail

**Diagnosis**:
Check what permissions your token has vs. what's needed

**Solution**:

**For GitHub**:
Minimum scopes needed:
- [OK] `repo` (full repository access)
- [OK] `workflow` (optional, for CI/CD)
- [OK] `read:org` (optional, for organizations)

**For Slack**:
Bot token scopes:
- [OK] `chat:write` (send messages)
- [OK] `channels:read` (list channels)
- [OK] `channels:history` (read messages)

**For Notion**:
- Token works BUT pages must be **shared with integration**
- Go to page → Share → Add integration

**For Google Drive**:
OAuth scopes:
- [OK] `https://www.googleapis.com/auth/drive.file`
- [OK] `https://www.googleapis.com/auth/drive.readonly` (read-only option)

**General Steps**:
1. Go to tool's token/app settings
2. Review granted permissions
3. Add missing scopes
4. Regenerate token (some tools require this)
5. Update config with new token
6. Restart Claude

---

### 4. Config File Syntax Error

**Symptoms**:
- Claude doesn't start
- MCP servers don't load
- JSON parse error in logs
- All integrations fail

**Diagnosis**:
Use JSON validator: https://jsonlint.com/

**Common Syntax Errors**:

**Missing Comma**:
```json
{
  "mcpServers": {
    "github": {...}
    "slack": {...}  ← ERROR: Missing comma after github entry
  }
}
```

**Fix**: Add comma
```json
{
  "mcpServers": {
    "github": {...},
    "slack": {...}
  }
}
```

**Trailing Comma**:
```json
{
  "mcpServers": {
    "github": {...},  ← ERROR: Comma after last entry
  }
}
```

**Fix**: Remove trailing comma
```json
{
  "mcpServers": {
    "github": {...}
  }
}
```

**Missing Quotes**:
```json
{
  mcpServers: {  ← ERROR: Keys must be quoted
    github: {...}
  }
}
```

**Fix**: Add quotes
```json
{
  "mcpServers": {
    "github": {...}
  }
}
```

**Unescaped Backslashes (Windows paths)**:
```json
"VAULT_PATH": "C:\Users\name\vault"  ← ERROR: Single backslashes
```

**Fix**: Double backslashes or use forward slashes
```json
"VAULT_PATH": "C:\\Users\\name\\vault"
or
"VAULT_PATH": "C:/Users/name/vault"
```

**Solution**:
1. Copy entire config file
2. Paste into https://jsonlint.com/
3. Click "Validate JSON"
4. Fix errors shown
5. Save corrected file
6. Restart Claude

---

### 5. MCP Server Not Responding

**Symptoms**:
- Integration configured but doesn't respond
- Claude acts like integration doesn't exist
- No error message, just doesn't work
- Used to work, now silent

**Diagnosis**:
Test if npx can run the server:
```bash
npx -y @modelcontextprotocol/server-{tool-name} --version
```

Should download and show version.

**Solution**:

**Step 1: Verify Config File Location**

| Platform | Correct Path |
|----------|--------------|
| macOS | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Windows | `%APPDATA%\Claude\claude_desktop_config.json` |
| Linux | `~/.config/Claude/claude_desktop_config.json` |

**Check**: Are you editing the right file?

**Step 2: Verify Claude Was Restarted**
- MCP servers ONLY load on startup
- Editing config while Claude is running = no effect
- Must **quit completely** and relaunch

**Step 3: Check for Firewall/Antivirus Blocking**
- Some security software blocks npx
- Try temporarily disabling
- Add npx to allowed programs

**Step 4: Check npx PATH**
- Ensure npx is in system PATH
- Test: `npx --version` (should show version)
- If not found, reinstall Node.js

**Step 5: Review Claude Logs** (if accessible)
- Look for MCP server startup errors
- Check for connection failures
- Note specific error messages

---

### 6. Tool Not Supported by MCP

**Symptoms**:
- No MCP server exists for your tool
- Can't find `@modelcontextprotocol/server-{tool-name}`
- 404 error when trying to install

**Diagnosis**:
Check MCP server directory: https://github.com/modelcontextprotocol/servers

**Solutions**:

**Option 1: Use Alternative Tool**
- Find similar tool with MCP support
- Example: Want Asana? Use Linear instead
- Many tools have overlapping functionality

**Option 2: Request Community Server**
1. Search discussions: https://github.com/modelcontextprotocol/discussions
2. Create feature request if doesn't exist
3. Community may already be building one

**Option 3: Build Custom Server** (Advanced)
If you're technical:
1. Read guide: https://modelcontextprotocol.io/docs/custom-servers
2. Implement MCP protocol for your tool
3. Share with community!

**Option 4: Use API Directly** (Workaround)
- Some tools have simple REST APIs
- Can make HTTP requests from Nexus
- Less integrated but functional

**Document Requirement**:
Add to 01-memory/core-learnings.md:
```markdown
## Requested Integrations
- {Tool Name} - Waiting for MCP server
  - Use case: {Why you need it}
  - Requested: {YYYY-MM-DD}
  - Tracking: {Link to discussion if exists}
```

---

### 7. Connection Succeeds But Features Don't Work

**Symptoms**:
- Initial connection test passes
- Basic commands work
- Specific features fail
- Partial functionality only

**Diagnosis**:
- Which specific features fail?
- Do they require special permissions?
- Check tool's API limits

**Common Causes**:

**1. Rate Limiting**
- Too many requests in short time
- Tool API throttling responses
- Solution: Space out requests, wait and retry

**2. Missing Secondary Permissions**
- Primary connection works
- Specific APIs need extra scopes
- Solution: Add additional scopes to token

**3. Resource Not Found**
- Trying to access non-existent resource
- Wrong resource ID
- Solution: Verify resource exists and ID is correct

**4. API Version Mismatch**
- MCP server uses older API version
- Tool has deprecated that API
- Solution: Update MCP server (`npx -y` always gets latest)

**5. Free Tier Limitations**
- Tool has free tier with limited features
- Feature requires paid plan
- Solution: Upgrade plan or use alternative feature

**Solution Steps**:
1. Identify exact feature that fails
2. Check tool's API documentation
3. Verify permissions include that feature
4. Test feature directly in tool's web interface
5. Update scopes if needed
6. Contact tool support if persists

---

### 8. Multiple Integration Conflicts

**Symptoms**:
- First integration works
- Adding second breaks first
- Some integrations work, others don't
- Config seems correct

**Diagnosis**:
Check for:
- Duplicate keys in JSON
- Conflicting environment variables
- Port conflicts (rare)

**Solution**:

**Check for Duplicate Keys**:
```json
{
  "mcpServers": {
    "github": {...},
    "github": {...}  ← ERROR: Duplicate key
  }
}
```

Each tool name must be unique!

**Check Environment Variable Conflicts**:
Some tools might use same env var names (rare, but possible)

**Verify JSON Structure**:
```json
{
  "mcpServers": {
    "tool1": {...},
    "tool2": {...},
    "tool3": {...}
  }
}
```

All tools should be at same level inside `mcpServers`

**Test Individually**:
1. Comment out all but one integration
2. Test that one
3. Add next integration
4. Test both
5. Repeat until you find the conflict

---

### 9. Credentials in Wrong Format

**Symptoms**:
- Config syntax valid
- Token looks correct
- Still authentication fails

**Diagnosis**:
Check token format requirements for your tool

**Common Format Issues**:

**GitHub**:
- Must start with `ghp_` (personal access token)
- Classic token recommended
- New fine-grained tokens may have different format

**Slack**:
- Bot token starts with `xoxb-`
- App token starts with `xapp-`
- Using wrong token type = fails

**Notion**:
- Internal integration token starts with `secret_`
- Must have underscores, not hyphens
- Case-sensitive

**PostgreSQL**:
- Connection string format: `postgresql://user:pass@host:port/database`
- Must include all components
- Special characters in password may need URL encoding

**Solution**:
1. Check tool's documentation for token format
2. Verify your token matches expected format
3. Regenerate if format changed
4. Copy-paste carefully (no extra characters)

---

### 10. Obsidian Vault Path Issues

**Symptoms**:
- Obsidian integration fails
- "Vault not found" error
- Path seems correct

**Diagnosis**:
Check vault path format for your OS

**Common Issues**:

**Windows Backslashes**:
```json
"OBSIDIAN_VAULT_PATH": "C:\Users\name\MyVault"  ← ERROR
```

**Fix**: Double backslashes or forward slashes
```json
"OBSIDIAN_VAULT_PATH": "C:\\Users\\name\\MyVault"
or
"OBSIDIAN_VAULT_PATH": "C:/Users/name/MyVault"
```

**Spaces in Path**:
If vault path has spaces, ensure it's properly quoted:
```json
"OBSIDIAN_VAULT_PATH": "C:/Users/My Name/My Vault"  ← OK (already quoted)
```

**Relative vs Absolute**:
Must be absolute path, not relative:
```json
"OBSIDIAN_VAULT_PATH": "./MyVault"  ← ERROR: Relative
"OBSIDIAN_VAULT_PATH": "/Users/name/MyVault"  ← OK: Absolute
```

**Vault Folder vs Vault**:
- Point to vault root (where `.obsidian` folder is)
- Not to a subfolder inside vault

**Solution**:
1. Find vault location in Obsidian: Settings → About → Vault path
2. Copy exact path
3. Convert backslashes to forward slashes or double backslashes
4. Use in config
5. Restart Claude

---

## General Troubleshooting Steps

When in doubt, follow this sequence:

### 1. Verify Prerequisites
```bash
node --version  # Should show version
npm --version   # Should show version
```

### 2. Validate JSON
- Copy config file to https://jsonlint.com/
- Fix any syntax errors
- Save corrected version

### 3. Test npx
```bash
npx -y @modelcontextprotocol/server-{tool-name} --version
```
Should download and show version

### 4. Check Token
- Copy token to text editor
- Check for extra spaces/line breaks
- Verify matches expected format
- Test in tool's web interface

### 5. Restart Claude
- **Quit completely** (not just close window)
- Relaunch application
- Wait for full startup
- Test integration

### 6. Check Logs
- Review any error messages
- Note specific failures
- Search for error text online

### 7. Isolate Problem
- Remove all but one integration
- Test that one
- Add back one at a time
- Find which causes issue

### 8. Ask for Help
If still stuck:
- MCP Discussions: https://github.com/modelcontextprotocol/discussions
- Include: Tool name, error message, sanitized config (remove tokens!)
- Don't paste actual API keys!

---

## Prevention Tips

### Before Adding Integration

1. **Read documentation** for the tool's MCP server
2. **Check prerequisites** (Node.js version, etc.)
3. **Prepare credentials** before starting
4. **Backup config file** before editing
5. **Use JSON validator** before saving

### During Setup

1. **Add one integration at a time**
2. **Test after each addition**
3. **Keep tokens secure** (don't paste publicly)
4. **Document what you did** in Memory
5. **Note any quirks** for future reference

### After Setup

1. **Test regularly** (monthly is good)
2. **Rotate keys periodically** (3-6 months)
3. **Update MCP servers** (npx does this automatically)
4. **Monitor tool announcements** for API changes
5. **Document working config** (with tokens removed!)

---

## Still Need Help?

### Resources

- **MCP Documentation**: https://modelcontextprotocol.io/
- **MCP Discussions**: https://github.com/modelcontextprotocol/discussions
- **Tool-Specific Docs**: See each tool's official API documentation
- **JSON Validator**: https://jsonlint.com/

### When Asking for Help

Include:
- [OK] Tool name and version
- [OK] OS and Claude version
- [OK] Error message (exact text)
- [OK] What you've tried
- [OK] Sanitized config (remove actual tokens!)

Never include:
- [ERROR] Actual API keys/tokens
- [ERROR] Passwords
- [ERROR] Private data

### Document Your Solution

When you fix an issue:
1. Add to 01-memory/core-learnings.md
2. Note what caused it
3. Note how you fixed it
4. Help future you (and others!)

---

**Remember**: Most integration issues are simple fixes (typos, forgot to restart, wrong permissions). Work through the checklist systematically and you'll usually find the issue quickly!
