---
name: gmail
version: 1.3
description: "Read, send, and manage Gmail emails. Load when user mentions 'gmail', 'email', 'send email', 'check email', 'inbox', 'draft', or references sending/reading emails."
---

## Purpose

Automate Gmail operations including reading, sending, replying, forwarding, and managing emails. Useful for email automation, inbox management, and communication workflows.

# Gmail

Read, send, and manage Gmail via OAuth authentication.

---

## CRITICAL SAFETY RULES

**These rules are MANDATORY and must NEVER be bypassed:**

### 1. NEVER Send Without Explicit Approval
- **ALWAYS** show the user the complete email (to, subject, body) before sending
- **ALWAYS** ask for explicit confirmation: "Do you want me to send this email? (yes/no)"
- **NEVER** auto-send emails, even if user says "send an email to X"
- **NEVER** send multiple emails in a loop without per-email confirmation

### 2. Draft-First Workflow (DEFAULT BEHAVIOR)
- **ALL send/reply/forward operations create a draft FIRST**
- User sees the draft and chooses: `yes` (send now), `no` (delete draft), or `keep-draft` (review in Gmail)
- This ensures user can ALWAYS review in Gmail UI before any email is sent

### 3. Sensitive Operations Require Confirmation
| Operation | Requires Confirmation |
|-----------|----------------------|
| Send email | **YES - ALWAYS** |
| Reply to email | **YES - ALWAYS** |
| Forward email | **YES - ALWAYS** |
| Send draft | **YES - ALWAYS** |
| Delete draft | Yes |
| Trash email | Yes |

### 4. Read Operations Are Safe
These do NOT require confirmation:
- List emails, Search emails, Read email content
- List labels, List drafts, Get attachment

---

## Pre-Flight Check (ALWAYS RUN FIRST)

```bash
python3 00-system/skills/google/google-master/scripts/google_auth.py --check --service gmail
```

**Exit codes:**
- **0**: Ready to use - proceed with user request
- **1**: Need to login - run `python3 00-system/skills/google/google-master/scripts/google_auth.py --login`
- **2**: Missing credentials or dependencies - see [../google-master/references/setup-guide.md](../google-master/references/setup-guide.md)

---

## Quick Reference

### List Emails
```bash
python3 00-system/skills/google/gmail/scripts/gmail_operations.py list --max 10
```

### List Unread Emails
```bash
python3 00-system/skills/google/gmail/scripts/gmail_operations.py list --query "is:unread" --max 10
```

### Search Emails
```bash
python3 00-system/skills/google/gmail/scripts/gmail_operations.py search "from:user@example.com subject:report"
```

### Read Email
```bash
python3 00-system/skills/google/gmail/scripts/gmail_operations.py read <message_id>
```

### Send Email
```bash
python3 00-system/skills/google/gmail/scripts/gmail_operations.py send --to "user@example.com" --subject "Hello" --body "Message body"
```

### Reply to Email
```bash
python3 00-system/skills/google/gmail/scripts/gmail_operations.py reply <message_id> --body "Reply text"
```

### Forward Email
```bash
python3 00-system/skills/google/gmail/scripts/gmail_operations.py forward <message_id> --to "user@example.com"
```

### Create Draft
```bash
python3 00-system/skills/google/gmail/scripts/gmail_operations.py draft --to "user@example.com" --subject "Draft" --body "Content"
```

### List Drafts
```bash
python3 00-system/skills/google/gmail/scripts/gmail_operations.py drafts
```

### List Labels
```bash
python3 00-system/skills/google/gmail/scripts/gmail_operations.py labels
```

### Trash/Archive/Mark Read
```bash
python3 00-system/skills/google/gmail/scripts/gmail_operations.py trash <message_id>
python3 00-system/skills/google/gmail/scripts/gmail_operations.py archive <message_id>
python3 00-system/skills/google/gmail/scripts/gmail_operations.py mark-read <message_id>
```

---

## Gmail Search Syntax

| Operator | Example | Description |
|----------|---------|-------------|
| `from:` | `from:user@example.com` | Emails from sender |
| `to:` | `to:me@example.com` | Emails to recipient |
| `subject:` | `subject:meeting` | Subject contains word |
| `is:unread` | `is:unread` | Unread emails |
| `has:attachment` | `has:attachment` | Has attachments |
| `after:` | `after:2024/01/01` | After date |
| `before:` | `before:2024/12/31` | Before date |
| `label:` | `label:important` | Has label |

---

## Error Handling

See [../google-master/references/error-handling.md](../google-master/references/error-handling.md) for common errors and solutions.

---

## Setup

First-time setup: [../google-master/references/setup-guide.md](../google-master/references/setup-guide.md)

**Quick start:**
1. `pip install google-auth google-auth-oauthlib google-api-python-client`
2. Create OAuth credentials in Google Cloud Console (enable Gmail API, choose "Desktop app")
3. Add to `.env` file at Nexus root:
   ```
   GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
   GOOGLE_CLIENT_SECRET=your-client-secret
   GOOGLE_PROJECT_ID=your-project-id
   ```
4. Run `python3 00-system/skills/google/google-master/scripts/google_auth.py --login`
