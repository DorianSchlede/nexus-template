# Google Integration Setup Guide

Complete setup instructions for Google services (Gmail, Docs, Sheets, Calendar, Drive, Tasks, Slides).

---

## Prerequisites

- Google account
- Python 3.8+
- Internet access

---

## Step 1: Install Dependencies

```bash
pip install google-auth google-auth-oauthlib google-api-python-client
```

---

## Step 2: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click **Select a project** > **New Project**
3. Name it (e.g., "Nexus Integration")
4. Click **Create**

---

## Step 3: Enable APIs

In Google Cloud Console:

1. Go to **APIs & Services** > **Library**
2. Search and enable each:
   - **Gmail API**
   - **Google Docs API**
   - **Google Sheets API**
   - **Google Calendar API**
   - **Google Drive API**
   - **Google Tasks API**
   - **Google Slides API**

Click **Enable** for each one.

---

## Step 4: Configure OAuth Consent Screen

1. Go to **APIs & Services** > **OAuth consent screen**
2. Select **External** (unless you have Google Workspace)
3. Click **Create**
4. Fill in:
   - App name: "Nexus"
   - User support email: your email
   - Developer contact: your email
5. Click **Save and Continue**
6. On **Scopes** page, click **Add or Remove Scopes**
7. Add these scopes:
   ```
   https://www.googleapis.com/auth/gmail.readonly
   https://www.googleapis.com/auth/gmail.send
   https://www.googleapis.com/auth/gmail.compose
   https://www.googleapis.com/auth/gmail.modify
   https://www.googleapis.com/auth/gmail.labels
   https://www.googleapis.com/auth/documents
   https://www.googleapis.com/auth/drive
   https://www.googleapis.com/auth/drive.file
   https://www.googleapis.com/auth/drive.metadata.readonly
   https://www.googleapis.com/auth/spreadsheets
   https://www.googleapis.com/auth/calendar
   https://www.googleapis.com/auth/calendar.events
   https://www.googleapis.com/auth/tasks
   https://www.googleapis.com/auth/tasks.readonly
   https://www.googleapis.com/auth/presentations
   ```
8. Click **Save and Continue**
9. On **Test users** page, click **Add Users**
10. Add your Google email address
11. Click **Save and Continue**

---

## Step 5: Create OAuth Credentials

1. Go to **APIs & Services** > **Credentials**
2. Click **Create Credentials** > **OAuth client ID**
3. Application type: **Desktop app**
4. Name: "Nexus Desktop"
5. Click **Create**
6. Copy the **Client ID** and **Client Secret**

---

## Step 6: Add Credentials to .env

Add these lines to your `.env` file (at Nexus root):

```
# Google Integration
GOOGLE_CLIENT_ID=your-client-id-here.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret-here
GOOGLE_PROJECT_ID=your-project-id
```

Replace with your actual values from Step 5.

---

## Step 7: Authenticate

Run the authentication script:

```bash
uv run python 00-system/skills/google/google-master/scripts/google_auth.py --login
```

This will:
1. Open your browser
2. Ask you to sign in with Google
3. Request permissions for all services
4. Save the token to `01-memory/integrations/google-token.json`

---

## Step 8: Verify Setup

```bash
uv run python 00-system/skills/google/google-master/scripts/check_google_config.py
```

Should output:
```
ALL CHECKS PASSED
Ready to use Google services (credentials from .env)
```

---

## Troubleshooting

### "Access blocked: This app's request is invalid"

Your OAuth consent screen may not be configured correctly:
1. Go to OAuth consent screen
2. Ensure you added yourself as a test user
3. Make sure the app is in "Testing" mode

### "Error 403: access_denied"

You're not listed as a test user:
1. Go to OAuth consent screen > Test users
2. Add your email
3. Wait a few minutes
4. Try again

### "Error 400: redirect_uri_mismatch"

The credentials were created for a different app type:
1. Delete the existing OAuth client
2. Create new credentials as "Desktop app"

### Token keeps expiring

Google tokens expire after 7 days in test mode. To avoid:
1. Publish your app (requires Google verification)
2. Or re-run `--login` when tokens expire

### "ModuleNotFoundError: No module named 'google'"

Dependencies not installed:
```bash
pip install google-auth google-auth-oauthlib google-api-python-client
```

---

## Security Notes

### Credentials in .env

The `.env` file contains your OAuth client ID and secret. This identifies your app, not your personal data.

- **Already in `.gitignore`** - will not be committed
- **Do NOT share** publicly (attackers could impersonate your app)

### Token File

The `google-token.json` file contains your authenticated session. This grants access to your Google account.

- **NEVER commit** to version control
- **NEVER share** with anyone
- Already in `.gitignore` (inside `01-memory/`)

### Revoking Access

To revoke Nexus's access to your Google account:
1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Third-party apps with account access
3. Find "Nexus" and click **Remove Access**

Or locally:
```bash
uv run python google_auth.py --logout
```

---

## File Locations Summary

| File | Path | Purpose |
|------|------|---------|
| OAuth credentials | `.env` (GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET) | App identity |
| Access token | `01-memory/integrations/google-token.json` | Your authenticated session |

Both files are in `.gitignore` and will not be committed.

---

**Version**: 1.1
**Updated**: 2025-12-18
