#!/usr/bin/env python3
"""
Upload File to Slack

Upload a file using the new Slack files API (files.getUploadURLExternal).
The old files.upload endpoint was deprecated in March 2025.

Usage:
    python upload_file.py --file /path/to/file.pdf --channel C123
    python upload_file.py --file /path/to/file.pdf --channel C123 --title "My Report"
    python upload_file.py --content "Hello world" --filename "hello.txt" --channel C123
"""

import sys
import json
import argparse
import requests
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from slack_client import get_client, SlackAPIError, explain_error


def upload_file(file_path=None, content=None, channel=None, filename=None,
                title=None, initial_comment=None, filetype=None):
    """
    Upload a file to Slack using the new API flow:
    1. Get upload URL from files.getUploadURLExternal
    2. POST file to the upload URL
    3. Complete upload with files.completeUploadExternal
    """
    client = get_client()

    # Determine file content and metadata
    if file_path:
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        filename = filename or file_path.name
        file_content = file_path.read_bytes()
        file_size = len(file_content)

    elif content:
        filename = filename or 'untitled.txt'
        file_content = content.encode('utf-8')
        file_size = len(file_content)

    else:
        raise ValueError("Must provide either --file or --content")

    # Step 1: Get upload URL
    upload_params = {
        'filename': filename,
        'length': file_size
    }

    upload_url_response = client.get('files.getUploadURLExternal', upload_params)
    upload_url = upload_url_response.get('upload_url')
    file_id = upload_url_response.get('file_id')

    if not upload_url or not file_id:
        raise SlackAPIError("Failed to get upload URL", method='files.getUploadURLExternal')

    # Step 2: Upload file content to the URL
    upload_response = requests.post(
        upload_url,
        data=file_content,
        headers={'Content-Type': 'application/octet-stream'},
        timeout=60
    )

    if upload_response.status_code != 200:
        raise SlackAPIError(
            f"Upload failed with status {upload_response.status_code}",
            method='upload_to_url',
            status_code=upload_response.status_code
        )

    # Step 3: Complete the upload
    complete_params = {
        'files': [{'id': file_id, 'title': title or filename}]
    }

    if channel:
        complete_params['channel_id'] = channel

    if initial_comment:
        complete_params['initial_comment'] = initial_comment

    complete_response = client.post('files.completeUploadExternal', complete_params)

    # Return file info
    files = complete_response.get('files', [])
    if files:
        return {'file': files[0], 'ok': True}
    else:
        return {'file': {'id': file_id, 'name': filename}, 'ok': True}


def main():
    parser = argparse.ArgumentParser(description='Upload file to Slack')
    parser.add_argument('--file', '-f',
                        help='Path to file to upload')
    parser.add_argument('--content', '-c',
                        help='Text content to upload as file')
    parser.add_argument('--channel',
                        help='Channel ID to share to')
    parser.add_argument('--filename',
                        help='Filename (default: original filename)')
    parser.add_argument('--title', '-t',
                        help='Title for the file')
    parser.add_argument('--initial-comment',
                        help='Message to post with the file')
    parser.add_argument('--filetype',
                        help='File type (e.g., txt, pdf, png)')
    parser.add_argument('--dry-run', action='store_true',
                        help='Preview upload without uploading')
    parser.add_argument('--json', action='store_true',
                        help='Output as JSON')
    args = parser.parse_args()

    if not args.file and not args.content:
        parser.error("Must provide either --file or --content")

    try:
        # Dry-run mode
        if args.dry_run:
            file_info = {}
            if args.file:
                file_path = Path(args.file)
                file_info['path'] = str(file_path)
                file_info['exists'] = file_path.exists()
                file_info['size'] = file_path.stat().st_size if file_path.exists() else None
                file_info['name'] = args.filename or file_path.name
            else:
                file_info['content_length'] = len(args.content) if args.content else 0
                file_info['name'] = args.filename or 'untitled.txt'

            if args.json:
                output = {
                    'dry_run': True,
                    'would_upload': {
                        'file': file_info,
                        'channel': args.channel,
                        'title': args.title
                    }
                }
                print(json.dumps(output, indent=2))
            else:
                print(f"\n[DRY-RUN] File would be uploaded (not actually uploaded):")
                print(f"    File: {file_info.get('name')}")
                if 'size' in file_info and file_info['size']:
                    print(f"    Size: {file_info['size']} bytes")
                print(f"    Channel: {args.channel or 'None specified'}")
                if args.title:
                    print(f"    Title: {args.title}")
                print()
            sys.exit(0)

        result = upload_file(
            file_path=args.file,
            content=args.content,
            channel=args.channel,
            filename=args.filename,
            title=args.title,
            initial_comment=args.initial_comment,
            filetype=args.filetype
        )

        file_info = result.get('file', {})

        if args.json:
            output = {
                'success': True,
                'file': {
                    'id': file_info.get('id'),
                    'name': file_info.get('name'),
                    'title': file_info.get('title'),
                    'filetype': file_info.get('filetype'),
                    'size': file_info.get('size'),
                    'permalink': file_info.get('permalink'),
                    'url_private': file_info.get('url_private')
                }
            }
            print(json.dumps(output, indent=2))
        else:
            print(f"\n[OK] File uploaded!")
            print(f"    Name: {file_info.get('name')}")
            print(f"    ID: {file_info.get('id')}")
            if file_info.get('filetype'):
                print(f"    Type: {file_info.get('filetype')}")
            if file_info.get('permalink'):
                print(f"    Link: {file_info['permalink']}")
            print()

    except FileNotFoundError as e:
        if args.json:
            print(json.dumps({
                'success': False,
                'error': {'message': str(e)}
            }, indent=2))
        else:
            print(f"\n[X] {e}")
        sys.exit(1)
    except SlackAPIError as e:
        if args.json:
            print(json.dumps({
                'success': False,
                'error': e.to_dict()
            }, indent=2))
        else:
            print(f"\n[X] Upload failed: {e}")
            print(f"    {explain_error(e.error_code)}")
        sys.exit(1)
    except Exception as e:
        if args.json:
            print(json.dumps({
                'success': False,
                'error': {'message': str(e)}
            }, indent=2))
        else:
            print(f"\n[X] Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
