# NotebookLM Enterprise Setup Guide

Complete guide for setting up NotebookLM Enterprise API access.

---

## Prerequisites

1. **Google Cloud Account** with billing enabled
2. **NotebookLM Enterprise** subscription (Workspace Business/Enterprise)
3. **Google Cloud SDK** (gcloud CLI) installed

---

## Step 1: Install Google Cloud SDK

If not already installed:

**Windows:**
```powershell
# Download and run installer from:
# https://cloud.google.com/sdk/docs/install#windows
```

**macOS:**
```bash
brew install --cask google-cloud-sdk
```

**Linux:**
```bash
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
```

---

## Step 2: Authenticate with gcloud

```bash
gcloud auth login
```

This opens a browser for Google authentication.

---

## Step 3: Configure Project

```bash
# Set your project
gcloud config set project YOUR_PROJECT_ID

# Get project number (needed for API)
gcloud projects describe YOUR_PROJECT_ID --format='value(projectNumber)'
```

---

## Step 4: Enable NotebookLM Enterprise API

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Navigate to **APIs & Services** > **Library**
3. Search for "Discovery Engine API"
4. Click **Enable**

Or via CLI:
```bash
gcloud services enable discoveryengine.googleapis.com
```

---

## Step 5: Configure Environment

Add to your `.env` file:

```env
GOOGLE_CLOUD_PROJECT_NUMBER=123456789012
NOTEBOOKLM_LOCATION=global
NOTEBOOKLM_ENDPOINT_LOCATION=global
```

**Location options:**
- `global` - Default, works worldwide
- `us` - US data residency
- `eu` - EU data residency

---

## Step 6: Verify Setup

```bash
uv run python 00-system/skills/notebooklm/notebooklm-master/scripts/check_notebooklm_config.py --test
```

Expected output:
```
NotebookLM Enterprise Configuration Status
=============================================

gcloud CLI: Installed
gcloud Auth: Authenticated
gcloud Project: your-project-id

Status: CONFIGURED

Environment variables:
  GOOGLE_CLOUD_PROJECT_NUMBER: 123456789012
  NOTEBOOKLM_LOCATION: global
  NOTEBOOKLM_ENDPOINT_LOCATION: global

Connection: OK
```

---

## Troubleshooting

### "Permission denied" error

1. Ensure NotebookLM Enterprise is enabled for your Workspace
2. Verify Discovery Engine API is enabled
3. Check you have the required IAM role: `NotebookLM Enterprise User`

### "gcloud not found"

Install Google Cloud SDK from https://cloud.google.com/sdk/docs/install

### "Not authenticated"

Run:
```bash
gcloud auth login
gcloud auth application-default login
```

### Wrong project

Check and set project:
```bash
gcloud config get-value project
gcloud config set project CORRECT_PROJECT_ID
```

---

## Required IAM Roles

For full access, users need:
- `roles/discoveryengine.notebooklmUser` - Basic notebook operations
- `roles/discoveryengine.notebooklmAdmin` - Share and manage notebooks

---

## API Quotas

Default quotas:
- 100 requests per minute per user
- 10 audio overview generations per day

Request quota increases via Google Cloud Console if needed.

---

**Last Updated**: 2025-12-27
