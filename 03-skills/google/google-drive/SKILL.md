---
name: google-drive
version: 1.0
description: "Manage Google Drive files and folders. Load when user mentions 'google drive', 'drive', 'upload file', 'download file', 'share file', 'create folder', or references cloud file storage operations."
---

# Google Drive

Upload, download, and manage files and folders in Google Drive via OAuth authentication.

---

## Pre-Flight Check (ALWAYS RUN FIRST)

```bash
python3 00-system/skills/google/google-master/scripts/google_auth.py --check --service drive
```

**Exit codes:**
- **0**: Ready to use - proceed with user request
- **1**: Need to login - run `python3 00-system/skills/google/google-master/scripts/google_auth.py --login`
- **2**: Missing credentials or dependencies - see [../google-master/references/setup-guide.md](../google-master/references/setup-guide.md)

---

## Quick Reference

### List Files (Root)
```bash
python3 00-system/skills/google/google-drive/scripts/drive_operations.py list
```

### List Files in Folder
```bash
python3 00-system/skills/google/google-drive/scripts/drive_operations.py list --folder <folder_id>
```

### Search Files
```bash
python3 00-system/skills/google/google-drive/scripts/drive_operations.py search "report"
```

### Get File Info
```bash
python3 00-system/skills/google/google-drive/scripts/drive_operations.py info <file_id>
```

### Download File
```bash
python3 00-system/skills/google/google-drive/scripts/drive_operations.py download <file_id> --output ./local_file.pdf
```

### Download Google Doc as PDF
```bash
python3 00-system/skills/google/google-drive/scripts/drive_operations.py download <doc_id> --format pdf
```

### Upload File
```bash
python3 00-system/skills/google/google-drive/scripts/drive_operations.py upload ./local_file.pdf --folder <folder_id>
```

### Create Folder
```bash
python3 00-system/skills/google/google-drive/scripts/drive_operations.py create-folder "New Folder" --parent <parent_id>
```

### Move File
```bash
python3 00-system/skills/google/google-drive/scripts/drive_operations.py move <file_id> <destination_folder_id>
```

### Copy File
```bash
python3 00-system/skills/google/google-drive/scripts/drive_operations.py copy <file_id> --name "Copy of File"
```

### Rename File
```bash
python3 00-system/skills/google/google-drive/scripts/drive_operations.py rename <file_id> "New Name"
```

### Delete File (Trash)
```bash
python3 00-system/skills/google/google-drive/scripts/drive_operations.py delete <file_id>
```

### Share File
```bash
python3 00-system/skills/google/google-drive/scripts/drive_operations.py share <file_id> user@example.com --role writer
```

### Get Sharing Info
```bash
python3 00-system/skills/google/google-drive/scripts/drive_operations.py sharing <file_id>
```

---

## File/Folder ID

The ID is in the URL:
```
https://drive.google.com/file/d/[FILE_ID]/view
https://drive.google.com/drive/folders/[FOLDER_ID]
```

---

## Export Formats

For Google Docs files, use `--format` when downloading:

| File Type | Available Formats |
|-----------|-------------------|
| Google Docs | pdf, docx, txt, html |
| Google Sheets | pdf, xlsx, csv |
| Google Slides | pdf, pptx |

---

## Available Operations

| Operation | Function | Description |
|-----------|----------|-------------|
| **List** | `list_files()` | List files in a folder |
| **Search** | `search_files()` | Search by name |
| **Info** | `get_file_info()` | Get file metadata |
| **Download** | `download_file()` | Download to local |
| **Upload** | `upload_file()` | Upload from local |
| **Create Folder** | `create_folder()` | Create new folder |
| **Move** | `move_file()` | Move to different folder |
| **Copy** | `copy_file()` | Duplicate a file |
| **Rename** | `rename_file()` | Change name |
| **Delete** | `delete_file()` | Move to trash |
| **Share** | `share_file()` | Share with user |
| **Sharing** | `get_sharing_info()` | Get permissions |

---

## Sharing Roles

| Role | Permissions |
|------|-------------|
| `reader` | View only |
| `commenter` | View and comment |
| `writer` | View, comment, and edit |

---

## Error Handling

See [../google-master/references/error-handling.md](../google-master/references/error-handling.md) for common errors and solutions.

---

## Setup

First-time setup: [../google-master/references/setup-guide.md](../google-master/references/setup-guide.md)

**Quick start:**
1. `pip install google-auth google-auth-oauthlib google-api-python-client`
2. Create OAuth credentials in Google Cloud Console (enable Google Drive API, choose "Desktop app")
3. Add to `.env` file at Nexus root:
   ```
   GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
   GOOGLE_CLIENT_SECRET=your-client-secret
   GOOGLE_PROJECT_ID=your-project-id
   ```
4. Run `python3 00-system/skills/google/google-master/scripts/google_auth.py --login`
