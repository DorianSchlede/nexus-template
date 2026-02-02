---
name: google-connect
description: "connect google, setup google, google integration."
version: "1.0"
---

# Google Connect

**Setup wizard for Google Workspace integration.**

## Purpose

Guide users through connecting their Google account to Nexus. One OAuth setup grants access to all 7 Google services: Gmail, Docs, Sheets, Calendar, Drive, Tasks, and Slides.

---

## Shared Resources

This skill uses `google-master` shared library:

| Resource | When to Load |
|----------|--------------|
| `google-master/scripts/check_google_config.py` | Always first (pre-flight) |
| `google-master/scripts/google_auth.py` | For authentication |
| `google-master/references/setup-guide.md` | Detailed setup instructions |
| `google-master/references/error-handling.md` | On any errors |

---

## Workflow 0: Config Check (ALWAYS FIRST)

Every interaction MUST start with config validation:

```bash
uv run python 00-system/skills/google/google-master/scripts/check_google_config.py --json
```

**Exit code meanings:**
- **Exit 0**: Fully configured and authenticated - ready to use
- **Exit 1**: Credentials exist but need to login (run OAuth flow)
- **Exit 2**: Missing credentials - need full setup

**Route based on exit code:**
- Exit 0 → Workflow 4 (Already Connected)
- Exit 1 → Workflow 3 (Authenticate)
- Exit 2 → Workflow 1 (Full Setup)

---

## Workflow 1: Full Setup (First-Time Users)

**Triggers**: "connect google", "setup google", config check returns exit 2

**Purpose**: Guide user through complete Google Cloud setup.

### Step 1: Introduction

Display:
```
--- GOOGLE WORKSPACE SETUP ---------------------------------

This will connect Nexus to your Google account, enabling:

  📧 Gmail      - Read, send, manage emails
  📄 Docs       - Create and edit documents
  [STATS] Sheets     - Work with spreadsheets
  [DATE] Calendar   - Manage events and schedules
  [DIR] Drive      - Upload, download, organize files
  [OK] Tasks      - Create and manage task lists
  📽️ Slides     - Create and edit presentations

Time: ~10 minutes (one-time setup)
You'll need: A Google account and browser access

------------------------------------------------------------
```

**Ask**: "Ready to set up Google integration?"

### Step 2: Create Google Cloud Project

Display:
```
--- STEP 1: CREATE GOOGLE CLOUD PROJECT -------------------

1. Go to: https://console.cloud.google.com/

2. Click the project dropdown (top-left) → "New Project"

3. Enter project name: "Nexus Integration" (or any name)

4. Click "Create"

5. Wait for project to be created, then select it

------------------------------------------------------------
```

**Ask**: "Done creating the project? (yes/no)"

### Step 3: Enable APIs

Display:
```
--- STEP 2: ENABLE GOOGLE APIS ----------------------------

Go to: APIs & Services → Library

Search for and ENABLE each of these APIs:

  ☐ Gmail API
  ☐ Google Docs API
  ☐ Google Sheets API
  ☐ Google Calendar API
  ☐ Google Drive API
  ☐ Google Tasks API
  ☐ Google Slides API

Click each one → Click "Enable"

------------------------------------------------------------
```

**Ask**: "All 7 APIs enabled? (yes/no)"

### Step 4: Configure OAuth Consent Screen

Display:
```
--- STEP 3: CONFIGURE OAUTH CONSENT -----------------------

Go to: APIs & Services → OAuth consent screen

1. Select "External" user type → Create

2. Fill in required fields:
   • App name: "Nexus"
   • User support email: (your email)
   • Developer contact: (your email)

3. Click "Save and Continue"

4. On "Scopes" page → Click "Save and Continue" (skip for now)

5. On "Test users" page:
   • Click "Add Users"
   • Add YOUR email address
   • Click "Save and Continue"

6. Review and go back to dashboard

------------------------------------------------------------
```

**Ask**: "OAuth consent screen configured? (yes/no)"

### Step 5: Create OAuth Credentials

Display:
```
--- STEP 4: CREATE OAUTH CREDENTIALS ----------------------

Go to: APIs & Services → Credentials

1. Click "Create Credentials" → "OAuth client ID"

2. Application type: "Desktop app"

3. Name: "Nexus Desktop" (or any name)

4. Click "Create"

5. A popup shows your credentials. Copy these values:
   • Client ID (ends in .apps.googleusercontent.com)
   • Client Secret

Also note your Project ID from the project dropdown.

------------------------------------------------------------
```

**Ask**: "Please paste your Client ID:"

### Step 6: Save Credentials

After user provides Client ID, Client Secret, and Project ID:

1. Check if `.env` file exists at Nexus root
2. Add or update these lines:
   ```
   GOOGLE_CLIENT_ID=<user-provided-client-id>
   GOOGLE_CLIENT_SECRET=<user-provided-client-secret>
   GOOGLE_PROJECT_ID=<user-provided-project-id>
   ```

Display:
```
[OK] Credentials saved to .env file

Your Google Cloud credentials are now stored securely.
Next: We'll authenticate with your Google account.
```

**Proceed to**: Workflow 3 (Authenticate)

---

## Workflow 2: Install Dependencies

**Run before authentication if needed:**

```bash
pip install google-auth google-auth-oauthlib google-api-python-client
```

Display:
```
Installing Google API libraries...
```

---

## Workflow 3: Authenticate

**Triggers**: Config check returns exit 1, or after Workflow 1 completes

**Purpose**: Run OAuth flow to get access token.

### Step 1: Start OAuth Flow

Display:
```
--- AUTHENTICATION ----------------------------------------

A browser window will open for Google sign-in.

1. Select your Google account
2. Click "Continue" (you may see "unverified app" warning)
3. Grant access to all requested permissions
4. Close the browser when done

------------------------------------------------------------
```

### Step 2: Run Login

```bash
uv run python 00-system/skills/google/google-master/scripts/google_auth.py --login
```

### Step 3: Verify Success

If successful:
```
[OK] Google Integration Complete!

You now have access to:
  📧 Gmail      → "list emails", "send email"
  📄 Docs       → "create doc", "read doc"
  [STATS] Sheets     → "read sheet", "append to sheet"
  [DATE] Calendar   → "list events", "create event"
  [DIR] Drive      → "list files", "upload file"
  [OK] Tasks      → "list tasks", "create task"
  📽️ Slides     → "create presentation", "add slide"

Try: "list my upcoming calendar events"
```

If failed, check error and refer to `google-master/references/error-handling.md`.

---

## Workflow 4: Already Connected

**Triggers**: Config check returns exit 0

**Purpose**: Show user they're already set up.

Display:
```
--- GOOGLE ALREADY CONNECTED ------------------------------

[OK] Your Google integration is fully configured!

Available services:
  📧 Gmail      📄 Docs       [STATS] Sheets
  [DATE] Calendar   [DIR] Drive      [OK] Tasks      📽️ Slides

Commands:
  • "list emails"           → Gmail inbox
  • "create doc [title]"    → New Google Doc
  • "list calendar events"  → Upcoming events
  • "list drive files"      → Drive contents
  • "list tasks"            → Task lists
  • "create presentation"   → New Slides

------------------------------------------------------------
```

---

## Workflow 5: Reconnect / Re-authenticate

**Triggers**: "reconnect google", "reauth google", "refresh google token"

**Purpose**: Get new OAuth token (e.g., after scope changes or token expiry).

```bash
uv run python 00-system/skills/google/google-master/scripts/google_auth.py --login
```

This removes the old token and initiates a fresh OAuth flow.

---

## Workflow 6: Disconnect

**Triggers**: "disconnect google", "remove google", "logout google"

**Purpose**: Remove stored credentials.

```bash
uv run python 00-system/skills/google/google-master/scripts/google_auth.py --logout
```

Display:
```
[OK] Google disconnected

Token removed. Your .env credentials are still saved.
To fully remove, delete these lines from .env:
  GOOGLE_CLIENT_ID
  GOOGLE_CLIENT_SECRET
  GOOGLE_PROJECT_ID
```

---

## Error Handling

| Error | Solution |
|-------|----------|
| "Missing credentials" | Run full setup (Workflow 1) |
| "Invalid client" | Check Client ID/Secret in .env |
| "Access denied" | Add your email as test user in OAuth consent |
| "Token expired" | Run reconnect (Workflow 5) |
| "API not enabled" | Enable the specific API in Google Cloud Console |

Load `google-master/references/error-handling.md` for detailed troubleshooting.

---

## Quick Reference

| Command | Action |
|---------|--------|
| `connect google` | Start setup wizard |
| `google status` | Check connection status |
| `reconnect google` | Refresh authentication |
| `disconnect google` | Remove token |

---

## File Locations

| File | Path | Purpose |
|------|------|---------|
| Credentials | `.env` | Client ID, Secret, Project ID |
| Access Token | `01-memory/integrations/google-token.json` | OAuth token |

Both files are in `.gitignore` and will not be committed.

---

*Google Connect v1.0 - Setup wizard for Google Workspace integration*
