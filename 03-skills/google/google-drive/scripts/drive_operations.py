#!/usr/bin/env python3
"""
Google Drive Operations

All operations for Google Drive:
- list: List files and folders
- search: Search for files
- info: Get file/folder metadata
- download: Download files
- upload: Upload files
- create-folder: Create folders
- move: Move files/folders
- copy: Copy files
- rename: Rename files/folders
- delete: Delete files/folders (to trash)
- share: Share files/folders
"""

import os
import sys
import json
import argparse
import io
from pathlib import Path

# Find Nexus root
def find_nexus_root():
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / "CLAUDE.md").exists():
            return parent
    return Path.cwd()

NEXUS_ROOT = find_nexus_root()

# Import from google-master shared auth
sys.path.insert(0, str(NEXUS_ROOT / "00-system" / "skills" / "google" / "google-master" / "scripts"))
from google_auth import get_credentials, get_service as _get_service, check_dependencies

def get_service():
    """Get authenticated Drive service."""
    return _get_service('drive')

# =============================================================================
# MIME TYPE HELPERS
# =============================================================================

GOOGLE_MIME_TYPES = {
    'folder': 'application/vnd.google-apps.folder',
    'document': 'application/vnd.google-apps.document',
    'spreadsheet': 'application/vnd.google-apps.spreadsheet',
    'presentation': 'application/vnd.google-apps.presentation',
    'form': 'application/vnd.google-apps.form',
    'drawing': 'application/vnd.google-apps.drawing',
}

EXPORT_MIME_TYPES = {
    'application/vnd.google-apps.document': {
        'pdf': 'application/pdf',
        'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'txt': 'text/plain',
        'html': 'text/html',
    },
    'application/vnd.google-apps.spreadsheet': {
        'pdf': 'application/pdf',
        'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'csv': 'text/csv',
    },
    'application/vnd.google-apps.presentation': {
        'pdf': 'application/pdf',
        'pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
    },
}

# =============================================================================
# LIST/SEARCH OPERATIONS
# =============================================================================

def list_files(folder_id: str = None, max_results: int = 20, file_type: str = None,
               include_trashed: bool = False):
    """
    List files and folders.

    Args:
        folder_id: Parent folder ID (None for root)
        max_results: Maximum number of results
        file_type: Filter by type (folder, document, spreadsheet, presentation)
        include_trashed: Include trashed files

    Returns:
        List of file metadata
    """
    service = get_service()

    query_parts = []

    if folder_id:
        query_parts.append(f"'{folder_id}' in parents")
    else:
        query_parts.append("'root' in parents")

    if not include_trashed:
        query_parts.append("trashed = false")

    if file_type and file_type in GOOGLE_MIME_TYPES:
        query_parts.append(f"mimeType = '{GOOGLE_MIME_TYPES[file_type]}'")

    query = " and ".join(query_parts)

    results = service.files().list(
        q=query,
        pageSize=max_results,
        fields="files(id, name, mimeType, size, createdTime, modifiedTime, parents, webViewLink)"
    ).execute()

    files = results.get('files', [])

    return [{
        'id': f['id'],
        'name': f['name'],
        'type': 'folder' if f['mimeType'] == GOOGLE_MIME_TYPES['folder'] else 'file',
        'mime_type': f['mimeType'],
        'size': f.get('size', 'N/A'),
        'created': f.get('createdTime', ''),
        'modified': f.get('modifiedTime', ''),
        'url': f.get('webViewLink', '')
    } for f in files]


def search_files(query: str, max_results: int = 20, file_type: str = None):
    """
    Search for files by name or content.

    Args:
        query: Search query (file name)
        max_results: Maximum number of results
        file_type: Filter by type

    Returns:
        List of matching files
    """
    service = get_service()

    query_parts = [f"name contains '{query}'", "trashed = false"]

    if file_type and file_type in GOOGLE_MIME_TYPES:
        query_parts.append(f"mimeType = '{GOOGLE_MIME_TYPES[file_type]}'")

    q = " and ".join(query_parts)

    results = service.files().list(
        q=q,
        pageSize=max_results,
        fields="files(id, name, mimeType, size, modifiedTime, webViewLink)"
    ).execute()

    files = results.get('files', [])

    return [{
        'id': f['id'],
        'name': f['name'],
        'type': 'folder' if f['mimeType'] == GOOGLE_MIME_TYPES['folder'] else 'file',
        'mime_type': f['mimeType'],
        'size': f.get('size', 'N/A'),
        'modified': f.get('modifiedTime', ''),
        'url': f.get('webViewLink', '')
    } for f in files]


def get_file_info(file_id: str):
    """
    Get detailed file metadata.

    Args:
        file_id: The file ID

    Returns:
        File metadata dict
    """
    service = get_service()

    file = service.files().get(
        fileId=file_id,
        fields="id, name, mimeType, size, createdTime, modifiedTime, parents, webViewLink, owners, shared, permissions"
    ).execute()

    return {
        'id': file['id'],
        'name': file['name'],
        'mime_type': file['mimeType'],
        'size': file.get('size', 'N/A'),
        'created': file.get('createdTime', ''),
        'modified': file.get('modifiedTime', ''),
        'url': file.get('webViewLink', ''),
        'owners': [o.get('emailAddress', '') for o in file.get('owners', [])],
        'shared': file.get('shared', False),
        'parents': file.get('parents', [])
    }

# =============================================================================
# DOWNLOAD/UPLOAD OPERATIONS
# =============================================================================

def download_file(file_id: str, output_path: str = None, export_format: str = None):
    """
    Download a file from Drive.

    Args:
        file_id: The file ID
        output_path: Local path to save (optional, uses file name if not specified)
        export_format: For Google Docs/Sheets/Slides, export format (pdf, docx, xlsx, etc.)

    Returns:
        Path to downloaded file
    """
    from googleapiclient.http import MediaIoBaseDownload

    service = get_service()

    # Get file metadata first
    file = service.files().get(fileId=file_id, fields="name, mimeType").execute()
    file_name = file['name']
    mime_type = file['mimeType']

    # Determine if we need to export (Google Docs format)
    is_google_doc = mime_type in EXPORT_MIME_TYPES

    if is_google_doc:
        if not export_format:
            export_format = 'pdf'  # Default export format

        export_mime = EXPORT_MIME_TYPES.get(mime_type, {}).get(export_format)
        if not export_mime:
            raise ValueError(f"Cannot export {mime_type} to {export_format}")

        request = service.files().export_media(fileId=file_id, mimeType=export_mime)

        if not output_path:
            output_path = f"{file_name}.{export_format}"
    else:
        request = service.files().get_media(fileId=file_id)

        if not output_path:
            output_path = file_name

    # Download
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)

    done = False
    while not done:
        status, done = downloader.next_chunk()

    # Write to file
    with open(output_path, 'wb') as f:
        f.write(fh.getvalue())

    return {
        'file_id': file_id,
        'name': file_name,
        'output_path': output_path,
        'size': len(fh.getvalue())
    }


def upload_file(local_path: str, folder_id: str = None, name: str = None):
    """
    Upload a file to Drive.

    Args:
        local_path: Path to local file
        folder_id: Parent folder ID (None for root)
        name: Name in Drive (optional, uses local filename)

    Returns:
        Uploaded file metadata
    """
    from googleapiclient.http import MediaFileUpload
    import mimetypes

    service = get_service()

    local_path = Path(local_path)
    if not local_path.exists():
        raise FileNotFoundError(f"File not found: {local_path}")

    file_name = name or local_path.name
    mime_type = mimetypes.guess_type(str(local_path))[0] or 'application/octet-stream'

    file_metadata = {'name': file_name}
    if folder_id:
        file_metadata['parents'] = [folder_id]

    media = MediaFileUpload(str(local_path), mimetype=mime_type, resumable=True)

    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id, name, webViewLink'
    ).execute()

    return {
        'id': file['id'],
        'name': file['name'],
        'url': file.get('webViewLink', ''),
        'uploaded_from': str(local_path)
    }

# =============================================================================
# FOLDER OPERATIONS
# =============================================================================

def create_folder(name: str, parent_id: str = None):
    """
    Create a new folder.

    Args:
        name: Folder name
        parent_id: Parent folder ID (None for root)

    Returns:
        Created folder metadata
    """
    service = get_service()

    file_metadata = {
        'name': name,
        'mimeType': GOOGLE_MIME_TYPES['folder']
    }

    if parent_id:
        file_metadata['parents'] = [parent_id]

    folder = service.files().create(
        body=file_metadata,
        fields='id, name, webViewLink'
    ).execute()

    return {
        'id': folder['id'],
        'name': folder['name'],
        'url': folder.get('webViewLink', '')
    }

# =============================================================================
# FILE MANAGEMENT OPERATIONS
# =============================================================================

def move_file(file_id: str, new_parent_id: str):
    """
    Move a file to a different folder.

    Args:
        file_id: The file ID
        new_parent_id: New parent folder ID

    Returns:
        Updated file metadata
    """
    service = get_service()

    # Get current parents
    file = service.files().get(fileId=file_id, fields='parents').execute()
    previous_parents = ",".join(file.get('parents', []))

    # Move to new parent
    file = service.files().update(
        fileId=file_id,
        addParents=new_parent_id,
        removeParents=previous_parents,
        fields='id, name, parents'
    ).execute()

    return {
        'id': file['id'],
        'name': file['name'],
        'new_parent': new_parent_id
    }


def copy_file(file_id: str, new_name: str = None, parent_id: str = None):
    """
    Copy a file.

    Args:
        file_id: The file ID to copy
        new_name: Name for the copy (optional)
        parent_id: Parent folder for copy (optional)

    Returns:
        Copied file metadata
    """
    service = get_service()

    body = {}
    if new_name:
        body['name'] = new_name
    if parent_id:
        body['parents'] = [parent_id]

    file = service.files().copy(
        fileId=file_id,
        body=body,
        fields='id, name, webViewLink'
    ).execute()

    return {
        'id': file['id'],
        'name': file['name'],
        'url': file.get('webViewLink', ''),
        'copied_from': file_id
    }


def rename_file(file_id: str, new_name: str):
    """
    Rename a file or folder.

    Args:
        file_id: The file ID
        new_name: New name

    Returns:
        Updated file metadata
    """
    service = get_service()

    file = service.files().update(
        fileId=file_id,
        body={'name': new_name},
        fields='id, name'
    ).execute()

    return {
        'id': file['id'],
        'name': file['name']
    }


def delete_file(file_id: str, permanent: bool = False):
    """
    Delete a file (move to trash or permanently delete).

    Args:
        file_id: The file ID
        permanent: If True, permanently delete. If False, move to trash.

    Returns:
        Deletion status
    """
    service = get_service()

    if permanent:
        service.files().delete(fileId=file_id).execute()
        return {'id': file_id, 'status': 'permanently_deleted'}
    else:
        service.files().update(
            fileId=file_id,
            body={'trashed': True}
        ).execute()
        return {'id': file_id, 'status': 'trashed'}

# =============================================================================
# SHARING OPERATIONS
# =============================================================================

def share_file(file_id: str, email: str, role: str = 'reader', notify: bool = True):
    """
    Share a file with someone.

    Args:
        file_id: The file ID
        email: Email address to share with
        role: Permission role (reader, writer, commenter)
        notify: Send notification email

    Returns:
        Permission details
    """
    service = get_service()

    permission = {
        'type': 'user',
        'role': role,
        'emailAddress': email
    }

    result = service.permissions().create(
        fileId=file_id,
        body=permission,
        sendNotificationEmail=notify,
        fields='id, role, emailAddress'
    ).execute()

    return {
        'file_id': file_id,
        'shared_with': email,
        'role': role,
        'permission_id': result['id']
    }


def get_sharing_info(file_id: str):
    """
    Get sharing/permissions info for a file.

    Args:
        file_id: The file ID

    Returns:
        List of permissions
    """
    service = get_service()

    permissions = service.permissions().list(
        fileId=file_id,
        fields='permissions(id, type, role, emailAddress, displayName)'
    ).execute()

    return [{
        'id': p['id'],
        'type': p['type'],
        'role': p['role'],
        'email': p.get('emailAddress', ''),
        'name': p.get('displayName', '')
    } for p in permissions.get('permissions', [])]

# =============================================================================
# CLI
# =============================================================================

def main():
    # Windows UTF-8 encoding fix
    if sys.platform == 'win32':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
            sys.stderr.reconfigure(encoding='utf-8')
        except AttributeError:
            pass

    parser = argparse.ArgumentParser(
        description="Google Drive Operations",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # List command
    list_parser = subparsers.add_parser('list', help='List files in a folder')
    list_parser.add_argument('--folder', help='Folder ID (root if not specified)')
    list_parser.add_argument('--max', type=int, default=20, help='Max results')
    list_parser.add_argument('--type', choices=['folder', 'document', 'spreadsheet', 'presentation'])

    # Search command
    search_parser = subparsers.add_parser('search', help='Search for files')
    search_parser.add_argument('query', help='Search query')
    search_parser.add_argument('--max', type=int, default=20, help='Max results')
    search_parser.add_argument('--type', choices=['folder', 'document', 'spreadsheet', 'presentation'])

    # Info command
    info_parser = subparsers.add_parser('info', help='Get file info')
    info_parser.add_argument('file_id', help='File ID')

    # Download command
    dl_parser = subparsers.add_parser('download', help='Download a file')
    dl_parser.add_argument('file_id', help='File ID')
    dl_parser.add_argument('--output', help='Output path')
    dl_parser.add_argument('--format', help='Export format for Google Docs (pdf, docx, xlsx, etc.)')

    # Upload command
    up_parser = subparsers.add_parser('upload', help='Upload a file')
    up_parser.add_argument('path', help='Local file path')
    up_parser.add_argument('--folder', help='Parent folder ID')
    up_parser.add_argument('--name', help='Name in Drive')

    # Create folder command
    mkdir_parser = subparsers.add_parser('create-folder', help='Create a folder')
    mkdir_parser.add_argument('name', help='Folder name')
    mkdir_parser.add_argument('--parent', help='Parent folder ID')

    # Move command
    move_parser = subparsers.add_parser('move', help='Move a file')
    move_parser.add_argument('file_id', help='File ID')
    move_parser.add_argument('folder_id', help='Destination folder ID')

    # Copy command
    copy_parser = subparsers.add_parser('copy', help='Copy a file')
    copy_parser.add_argument('file_id', help='File ID')
    copy_parser.add_argument('--name', help='New name')
    copy_parser.add_argument('--folder', help='Destination folder ID')

    # Rename command
    rename_parser = subparsers.add_parser('rename', help='Rename a file')
    rename_parser.add_argument('file_id', help='File ID')
    rename_parser.add_argument('new_name', help='New name')

    # Delete command
    del_parser = subparsers.add_parser('delete', help='Delete a file')
    del_parser.add_argument('file_id', help='File ID')
    del_parser.add_argument('--permanent', action='store_true', help='Permanently delete')

    # Share command
    share_parser = subparsers.add_parser('share', help='Share a file')
    share_parser.add_argument('file_id', help='File ID')
    share_parser.add_argument('email', help='Email to share with')
    share_parser.add_argument('--role', choices=['reader', 'writer', 'commenter'], default='reader')
    share_parser.add_argument('--no-notify', action='store_true', help='Skip notification email')

    # Sharing info command
    sharing_parser = subparsers.add_parser('sharing', help='Get sharing info')
    sharing_parser.add_argument('file_id', help='File ID')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    try:
        if args.command == 'list':
            result = list_files(args.folder, args.max, args.type)
        elif args.command == 'search':
            result = search_files(args.query, args.max, args.type)
        elif args.command == 'info':
            result = get_file_info(args.file_id)
        elif args.command == 'download':
            result = download_file(args.file_id, args.output, args.format)
        elif args.command == 'upload':
            result = upload_file(args.path, args.folder, args.name)
        elif args.command == 'create-folder':
            result = create_folder(args.name, args.parent)
        elif args.command == 'move':
            result = move_file(args.file_id, args.folder_id)
        elif args.command == 'copy':
            result = copy_file(args.file_id, args.name, args.folder)
        elif args.command == 'rename':
            result = rename_file(args.file_id, args.new_name)
        elif args.command == 'delete':
            result = delete_file(args.file_id, args.permanent)
        elif args.command == 'share':
            result = share_file(args.file_id, args.email, args.role, not args.no_notify)
        elif args.command == 'sharing':
            result = get_sharing_info(args.file_id)
        else:
            parser.print_help()
            return

        print(json.dumps(result, indent=2, default=str))

    except Exception as e:
        print(json.dumps({'error': str(e)}, indent=2))
        sys.exit(1)

if __name__ == "__main__":
    main()
