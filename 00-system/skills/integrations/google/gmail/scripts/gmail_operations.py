#!/usr/bin/env python3
"""
Gmail Operations

All operations for Gmail:
- list: List emails with filters
- read: Read email content
- send: Send new email
- reply: Reply to an email
- forward: Forward an email
- search: Search emails
- labels: Manage labels
- draft: Create/manage drafts
- trash: Move to trash
- archive: Archive emails
"""

import os
import sys
import json
import argparse
import base64
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# Find Nexus root
def find_nexus_root():
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / "CLAUDE.md").exists():
            return parent
    return Path.cwd()

NEXUS_ROOT = find_nexus_root()

# Import from google-master shared auth
# Try both possible locations for google-master
for path in [
    NEXUS_ROOT / "03-skills" / "google" / "google-master" / "scripts",
    NEXUS_ROOT / "00-system" / "skills" / "google" / "google-master" / "scripts",
]:
    if path.exists():
        sys.path.insert(0, str(path))
        break
from google_auth import get_credentials, get_service as _get_service, check_dependencies

def get_service():
    """Get authenticated Gmail service."""
    return _get_service('gmail')

# =============================================================================
# LIST/SEARCH OPERATIONS
# =============================================================================

def list_emails(query: str = None, max_results: int = 10, label_ids: list = None):
    """
    List emails matching criteria.

    Args:
        query: Gmail search query (e.g., "from:user@example.com", "is:unread")
        max_results: Maximum number of emails to return
        label_ids: Filter by label IDs (e.g., ["INBOX", "UNREAD"])

    Returns:
        List of email summaries
    """
    service = get_service()

    params = {
        'userId': 'me',
        'maxResults': max_results
    }

    if query:
        params['q'] = query
    if label_ids:
        params['labelIds'] = label_ids

    results = service.users().messages().list(**params).execute()
    messages = results.get('messages', [])

    emails = []
    for msg in messages:
        # Get message details
        message = service.users().messages().get(
            userId='me',
            id=msg['id'],
            format='metadata',
            metadataHeaders=['From', 'To', 'Subject', 'Date']
        ).execute()

        headers = {h['name']: h['value'] for h in message.get('payload', {}).get('headers', [])}

        emails.append({
            'id': msg['id'],
            'thread_id': message.get('threadId'),
            'snippet': message.get('snippet', '')[:100],
            'from': headers.get('From', ''),
            'to': headers.get('To', ''),
            'subject': headers.get('Subject', ''),
            'date': headers.get('Date', ''),
            'labels': message.get('labelIds', [])
        })

    return emails

def search_emails(query: str, max_results: int = 10):
    """
    Search emails using Gmail search syntax.

    Args:
        query: Gmail search query
        max_results: Maximum results

    Common search operators:
        - from:email@example.com
        - to:email@example.com
        - subject:keyword
        - is:unread / is:read
        - is:starred
        - has:attachment
        - after:2024/01/01
        - before:2024/12/31
        - label:labelname
        - in:inbox / in:sent / in:trash
    """
    return list_emails(query=query, max_results=max_results)

# =============================================================================
# READ OPERATIONS
# =============================================================================

def read_email(message_id: str, format: str = 'full'):
    """
    Read full email content.

    Args:
        message_id: The email message ID
        format: 'full', 'minimal', 'raw', or 'metadata'

    Returns:
        Email content with headers and body
    """
    service = get_service()

    message = service.users().messages().get(
        userId='me',
        id=message_id,
        format=format
    ).execute()

    headers = {h['name']: h['value'] for h in message.get('payload', {}).get('headers', [])}

    # Extract body
    body = ''
    payload = message.get('payload', {})

    if 'body' in payload and payload['body'].get('data'):
        body = base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8')
    elif 'parts' in payload:
        for part in payload['parts']:
            if part['mimeType'] == 'text/plain' and part['body'].get('data'):
                body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                break
            elif part['mimeType'] == 'text/html' and part['body'].get('data') and not body:
                body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')

    # Get attachments info
    attachments = []
    if 'parts' in payload:
        for part in payload['parts']:
            if part.get('filename'):
                attachments.append({
                    'filename': part['filename'],
                    'mimeType': part['mimeType'],
                    'size': part['body'].get('size', 0),
                    'attachmentId': part['body'].get('attachmentId')
                })

    return {
        'id': message_id,
        'thread_id': message.get('threadId'),
        'from': headers.get('From', ''),
        'to': headers.get('To', ''),
        'cc': headers.get('Cc', ''),
        'bcc': headers.get('Bcc', ''),
        'subject': headers.get('Subject', ''),
        'date': headers.get('Date', ''),
        'body': body,
        'snippet': message.get('snippet', ''),
        'labels': message.get('labelIds', []),
        'attachments': attachments
    }

def get_attachment(message_id: str, attachment_id: str, output_path: str = None):
    """
    Download an email attachment.

    Args:
        message_id: The email message ID
        attachment_id: The attachment ID
        output_path: Path to save the file

    Returns:
        Attachment data or file path
    """
    service = get_service()

    attachment = service.users().messages().attachments().get(
        userId='me',
        messageId=message_id,
        id=attachment_id
    ).execute()

    data = base64.urlsafe_b64decode(attachment['data'])

    if output_path:
        with open(output_path, 'wb') as f:
            f.write(data)
        return {'saved_to': output_path, 'size': len(data)}

    return {'data': data, 'size': len(data)}

# =============================================================================
# SEND OPERATIONS
# =============================================================================

def send_email(to: str, subject: str, body: str, cc: str = None, bcc: str = None,
               html: bool = False, attachments: list = None):
    """
    Send a new email.

    Args:
        to: Recipient email (comma-separated for multiple)
        subject: Email subject
        body: Email body (plain text or HTML)
        cc: CC recipients (comma-separated)
        bcc: BCC recipients (comma-separated)
        html: If True, body is HTML
        attachments: List of file paths to attach

    Returns:
        Sent message info
    """
    service = get_service()

    if attachments:
        message = MIMEMultipart()
        message.attach(MIMEText(body, 'html' if html else 'plain'))

        for file_path in attachments:
            with open(file_path, 'rb') as f:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename="{Path(file_path).name}"')
            message.attach(part)
    else:
        message = MIMEText(body, 'html' if html else 'plain')

    message['to'] = to
    message['subject'] = subject
    if cc:
        message['cc'] = cc
    if bcc:
        message['bcc'] = bcc

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')

    result = service.users().messages().send(
        userId='me',
        body={'raw': raw}
    ).execute()

    return {
        'id': result['id'],
        'thread_id': result.get('threadId'),
        'to': to,
        'subject': subject,
        'status': 'sent'
    }

def reply_to_email(message_id: str, body: str, reply_all: bool = False, html: bool = False):
    """
    Reply to an email.

    Args:
        message_id: Original message ID to reply to
        body: Reply body
        reply_all: If True, reply to all recipients
        html: If True, body is HTML

    Returns:
        Sent reply info
    """
    service = get_service()

    # Get original message
    original = read_email(message_id)

    # Build recipients
    to = original['from']
    cc = None
    if reply_all and original.get('cc'):
        cc = original['cc']

    # Build subject
    subject = original['subject']
    if not subject.lower().startswith('re:'):
        subject = f"Re: {subject}"

    # Create message
    message = MIMEText(body, 'html' if html else 'plain')
    message['to'] = to
    message['subject'] = subject
    message['In-Reply-To'] = message_id
    message['References'] = message_id
    if cc:
        message['cc'] = cc

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')

    result = service.users().messages().send(
        userId='me',
        body={
            'raw': raw,
            'threadId': original['thread_id']
        }
    ).execute()

    return {
        'id': result['id'],
        'thread_id': result.get('threadId'),
        'to': to,
        'subject': subject,
        'status': 'sent',
        'reply_to': message_id
    }

def forward_email(message_id: str, to: str, additional_text: str = None):
    """
    Forward an email.

    Args:
        message_id: Message ID to forward
        to: Forward recipient
        additional_text: Optional text to add before forwarded content

    Returns:
        Sent forward info
    """
    service = get_service()

    # Get original message
    original = read_email(message_id)

    # Build subject
    subject = original['subject']
    if not subject.lower().startswith('fwd:'):
        subject = f"Fwd: {subject}"

    # Build body with forward header
    forward_header = f"\n\n---------- Forwarded message ----------\n"
    forward_header += f"From: {original['from']}\n"
    forward_header += f"Date: {original['date']}\n"
    forward_header += f"Subject: {original['subject']}\n"
    forward_header += f"To: {original['to']}\n\n"

    body = ""
    if additional_text:
        body = additional_text
    body += forward_header + original['body']

    return send_email(to=to, subject=subject, body=body)

# =============================================================================
# DRAFT OPERATIONS
# =============================================================================

def create_draft(to: str, subject: str, body: str, cc: str = None, html: bool = False):
    """
    Create a draft email.

    Args:
        to: Recipient email
        subject: Email subject
        body: Email body
        cc: CC recipients
        html: If True, body is HTML

    Returns:
        Draft info
    """
    service = get_service()

    message = MIMEText(body, 'html' if html else 'plain')
    message['to'] = to
    message['subject'] = subject
    if cc:
        message['cc'] = cc

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')

    result = service.users().drafts().create(
        userId='me',
        body={'message': {'raw': raw}}
    ).execute()

    return {
        'draft_id': result['id'],
        'message_id': result['message']['id'],
        'to': to,
        'subject': subject,
        'status': 'draft'
    }

def list_drafts(max_results: int = 10):
    """List all drafts."""
    service = get_service()

    results = service.users().drafts().list(
        userId='me',
        maxResults=max_results
    ).execute()

    drafts = []
    for draft in results.get('drafts', []):
        draft_detail = service.users().drafts().get(
            userId='me',
            id=draft['id']
        ).execute()

        message = draft_detail.get('message', {})
        headers = {h['name']: h['value'] for h in message.get('payload', {}).get('headers', [])}

        drafts.append({
            'draft_id': draft['id'],
            'message_id': message.get('id'),
            'to': headers.get('To', ''),
            'subject': headers.get('Subject', ''),
            'snippet': message.get('snippet', '')[:100]
        })

    return drafts

def send_draft(draft_id: str):
    """Send an existing draft."""
    service = get_service()

    result = service.users().drafts().send(
        userId='me',
        body={'id': draft_id}
    ).execute()

    return {
        'id': result['id'],
        'thread_id': result.get('threadId'),
        'status': 'sent'
    }

def delete_draft(draft_id: str):
    """Delete a draft."""
    service = get_service()

    service.users().drafts().delete(
        userId='me',
        id=draft_id
    ).execute()

    return {'deleted': draft_id}

# =============================================================================
# LABEL OPERATIONS
# =============================================================================

def list_labels():
    """List all labels."""
    service = get_service()

    results = service.users().labels().list(userId='me').execute()

    return [
        {
            'id': label['id'],
            'name': label['name'],
            'type': label['type']
        }
        for label in results.get('labels', [])
    ]

def create_label(name: str):
    """Create a new label."""
    service = get_service()

    result = service.users().labels().create(
        userId='me',
        body={'name': name}
    ).execute()

    return {
        'id': result['id'],
        'name': result['name']
    }

def add_label(message_id: str, label_ids: list):
    """Add labels to an email."""
    service = get_service()

    service.users().messages().modify(
        userId='me',
        id=message_id,
        body={'addLabelIds': label_ids}
    ).execute()

    return {'message_id': message_id, 'labels_added': label_ids}

def remove_label(message_id: str, label_ids: list):
    """Remove labels from an email."""
    service = get_service()

    service.users().messages().modify(
        userId='me',
        id=message_id,
        body={'removeLabelIds': label_ids}
    ).execute()

    return {'message_id': message_id, 'labels_removed': label_ids}

# =============================================================================
# MANAGE OPERATIONS
# =============================================================================

def trash_email(message_id: str):
    """Move email to trash."""
    service = get_service()

    service.users().messages().trash(
        userId='me',
        id=message_id
    ).execute()

    return {'message_id': message_id, 'status': 'trashed'}

def untrash_email(message_id: str):
    """Remove email from trash."""
    service = get_service()

    service.users().messages().untrash(
        userId='me',
        id=message_id
    ).execute()

    return {'message_id': message_id, 'status': 'restored'}

def archive_email(message_id: str):
    """Archive email (remove from inbox)."""
    return remove_label(message_id, ['INBOX'])

def mark_read(message_id: str):
    """Mark email as read."""
    return remove_label(message_id, ['UNREAD'])

def mark_unread(message_id: str):
    """Mark email as unread."""
    return add_label(message_id, ['UNREAD'])

def star_email(message_id: str):
    """Star an email."""
    return add_label(message_id, ['STARRED'])

def unstar_email(message_id: str):
    """Remove star from email."""
    return remove_label(message_id, ['STARRED'])

# =============================================================================
# CLI INTERFACE
# =============================================================================

def main():
    # Fix Windows encoding for emoji output
    if sys.platform == 'win32':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
            sys.stderr.reconfigure(encoding='utf-8')
        except AttributeError:
            pass

    parser = argparse.ArgumentParser(description="Gmail Operations")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # List
    list_parser = subparsers.add_parser("list", help="List emails")
    list_parser.add_argument("--query", "-q", help="Search query")
    list_parser.add_argument("--max", type=int, default=10, help="Max results")
    list_parser.add_argument("--label", help="Filter by label")
    list_parser.add_argument("--json", action="store_true", help="Output as JSON")

    # Search
    search_parser = subparsers.add_parser("search", help="Search emails")
    search_parser.add_argument("query", help="Search query")
    search_parser.add_argument("--max", type=int, default=10, help="Max results")
    search_parser.add_argument("--json", action="store_true", help="Output as JSON")

    # Read
    read_parser = subparsers.add_parser("read", help="Read email content")
    read_parser.add_argument("message_id", help="Message ID")
    read_parser.add_argument("--json", action="store_true", help="Output as JSON")

    # Send
    send_parser = subparsers.add_parser("send", help="Send email")
    send_parser.add_argument("--to", required=True, help="Recipient")
    send_parser.add_argument("--subject", required=True, help="Subject")
    send_parser.add_argument("--body", required=True, help="Body text")
    send_parser.add_argument("--cc", help="CC recipients")
    send_parser.add_argument("--html", action="store_true", help="Body is HTML")
    send_parser.add_argument("--yes", "-y", action="store_true", help="Skip confirmation (use with caution)")
    send_parser.add_argument("--json", action="store_true", help="Output as JSON")

    # Reply
    reply_parser = subparsers.add_parser("reply", help="Reply to email")
    reply_parser.add_argument("message_id", help="Message ID to reply to")
    reply_parser.add_argument("--body", required=True, help="Reply body")
    reply_parser.add_argument("--all", action="store_true", help="Reply all")
    reply_parser.add_argument("--yes", "-y", action="store_true", help="Skip confirmation (use with caution)")
    reply_parser.add_argument("--json", action="store_true", help="Output as JSON")

    # Forward
    forward_parser = subparsers.add_parser("forward", help="Forward email")
    forward_parser.add_argument("message_id", help="Message ID to forward")
    forward_parser.add_argument("--to", required=True, help="Forward to")
    forward_parser.add_argument("--text", help="Additional text")
    forward_parser.add_argument("--yes", "-y", action="store_true", help="Skip confirmation (use with caution)")
    forward_parser.add_argument("--json", action="store_true", help="Output as JSON")

    # Draft
    draft_parser = subparsers.add_parser("draft", help="Create draft")
    draft_parser.add_argument("--to", required=True, help="Recipient")
    draft_parser.add_argument("--subject", required=True, help="Subject")
    draft_parser.add_argument("--body", required=True, help="Body text")
    draft_parser.add_argument("--json", action="store_true", help="Output as JSON")

    # Drafts list
    drafts_parser = subparsers.add_parser("drafts", help="List drafts")
    drafts_parser.add_argument("--json", action="store_true", help="Output as JSON")

    # Labels
    labels_parser = subparsers.add_parser("labels", help="List labels")
    labels_parser.add_argument("--json", action="store_true", help="Output as JSON")

    # Trash
    trash_parser = subparsers.add_parser("trash", help="Move to trash")
    trash_parser.add_argument("message_id", help="Message ID")

    # Archive
    archive_parser = subparsers.add_parser("archive", help="Archive email")
    archive_parser.add_argument("message_id", help="Message ID")

    # Mark read
    markread_parser = subparsers.add_parser("mark-read", help="Mark as read")
    markread_parser.add_argument("message_id", help="Message ID")

    # Mark unread
    markunread_parser = subparsers.add_parser("mark-unread", help="Mark as unread")
    markunread_parser.add_argument("message_id", help="Message ID")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if not check_dependencies():
        print("[ERROR] Missing dependencies. Run:")
        print("  pip install google-auth google-auth-oauthlib google-api-python-client")
        sys.exit(1)

    try:
        if args.command == "list":
            label_ids = [args.label] if args.label else None
            result = list_emails(query=args.query, max_results=args.max, label_ids=label_ids)
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                for email in result:
                    print(f"* {email['subject']}")
                    print(f"  From: {email['from']}")
                    print(f"  Date: {email['date']}")
                    print(f"  ID: {email['id']}")
                    print()

        elif args.command == "search":
            result = search_emails(args.query, args.max)
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                for email in result:
                    print(f"* {email['subject']}")
                    print(f"  From: {email['from']}")
                    print(f"  ID: {email['id']}")
                    print()

        elif args.command == "read":
            result = read_email(args.message_id)
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                print(f"From: {result['from']}")
                print(f"To: {result['to']}")
                print(f"Subject: {result['subject']}")
                print(f"Date: {result['date']}")
                print("-" * 50)
                print(result['body'])

        elif args.command == "send":
            # DRAFT-FIRST WORKFLOW (default)
            # Step 1: Create draft
            draft_result = create_draft(
                to=args.to,
                subject=args.subject,
                body=args.body,
                cc=args.cc,
                html=args.html
            )

            print("\n" + "=" * 50)
            print("[>] DRAFT CREATED - REVIEW BEFORE SENDING")
            print("=" * 50)
            print(f"TO: {args.to}")
            if args.cc:
                print(f"CC: {args.cc}")
            print(f"SUBJECT: {args.subject}")
            print("-" * 50)
            print(args.body)
            print("=" * 50)
            print(f"\n[LIST] Draft ID: {draft_result['draft_id']}")
            print("[EMAIL] You can review this draft in Gmail before sending.")

            # Step 2: Ask for confirmation to send
            if args.yes:
                # --yes flag: send immediately (use with caution)
                result = send_draft(draft_result['draft_id'])
                if args.json:
                    print(json.dumps(result, indent=2))
                else:
                    print(f"\n[OK] Email sent to {args.to}")
                    print(f"Subject: {args.subject}")
                    print(f"ID: {result['id']}")
            else:
                confirm = input("\n[!]  Send this email now? (yes/no/keep-draft): ").strip().lower()
                if confirm in ['yes', 'y']:
                    result = send_draft(draft_result['draft_id'])
                    if args.json:
                        print(json.dumps(result, indent=2))
                    else:
                        print(f"\n[OK] Email sent to {args.to}")
                        print(f"Subject: {args.subject}")
                        print(f"ID: {result['id']}")
                elif confirm in ['keep-draft', 'keep', 'draft', 'k', 'd']:
                    print(f"\n[>] Draft kept. Review and send from Gmail when ready.")
                    print(f"Draft ID: {draft_result['draft_id']}")
                else:
                    # Delete the draft if user cancels
                    delete_draft(draft_result['draft_id'])
                    print("[ERROR] Email cancelled and draft deleted.")

        elif args.command == "reply":
            # Get original email for preview
            original = read_email(args.message_id)

            # Build reply subject
            reply_subject = original['subject']
            if not reply_subject.lower().startswith('re:'):
                reply_subject = f"Re: {reply_subject}"

            # DRAFT-FIRST WORKFLOW
            # Step 1: Create draft reply
            draft_result = create_draft(
                to=original['from'],
                subject=reply_subject,
                body=args.body
            )

            print("\n" + "=" * 50)
            print("[>] REPLY DRAFT CREATED - REVIEW BEFORE SENDING")
            print("=" * 50)
            print(f"REPLYING TO: {original['from']}")
            print(f"SUBJECT: {reply_subject}")
            print("-" * 50)
            print("YOUR REPLY:")
            print(args.body)
            print("=" * 50)
            print(f"\n[LIST] Draft ID: {draft_result['draft_id']}")
            print("[EMAIL] You can review this draft in Gmail before sending.")

            # Step 2: Ask for confirmation to send
            if args.yes:
                result = send_draft(draft_result['draft_id'])
                if args.json:
                    print(json.dumps(result, indent=2))
                else:
                    print(f"\n[OK] Reply sent to {original['from']}")
            else:
                confirm = input("\n[!]  Send this reply now? (yes/no/keep-draft): ").strip().lower()
                if confirm in ['yes', 'y']:
                    result = send_draft(draft_result['draft_id'])
                    if args.json:
                        print(json.dumps(result, indent=2))
                    else:
                        print(f"\n[OK] Reply sent to {original['from']}")
                elif confirm in ['keep-draft', 'keep', 'draft', 'k', 'd']:
                    print(f"\n[>] Draft kept. Review and send from Gmail when ready.")
                    print(f"Draft ID: {draft_result['draft_id']}")
                else:
                    delete_draft(draft_result['draft_id'])
                    print("[ERROR] Reply cancelled and draft deleted.")

        elif args.command == "forward":
            # Get original email for preview
            original = read_email(args.message_id)

            # Build forward subject and body
            fwd_subject = original['subject']
            if not fwd_subject.lower().startswith('fwd:'):
                fwd_subject = f"Fwd: {fwd_subject}"

            forward_header = f"\n\n---------- Forwarded message ----------\n"
            forward_header += f"From: {original['from']}\n"
            forward_header += f"Date: {original['date']}\n"
            forward_header += f"Subject: {original['subject']}\n"
            forward_header += f"To: {original['to']}\n\n"

            fwd_body = ""
            if args.text:
                fwd_body = args.text
            fwd_body += forward_header + original['body']

            # DRAFT-FIRST WORKFLOW
            # Step 1: Create draft forward
            draft_result = create_draft(
                to=args.to,
                subject=fwd_subject,
                body=fwd_body
            )

            print("\n" + "=" * 50)
            print("[>] FORWARD DRAFT CREATED - REVIEW BEFORE SENDING")
            print("=" * 50)
            print(f"FORWARDING TO: {args.to}")
            print(f"ORIGINAL FROM: {original['from']}")
            print(f"SUBJECT: {fwd_subject}")
            if args.text:
                print("-" * 50)
                print("YOUR NOTE:")
                print(args.text)
            print("=" * 50)
            print(f"\n[LIST] Draft ID: {draft_result['draft_id']}")
            print("[EMAIL] You can review this draft in Gmail before sending.")

            # Step 2: Ask for confirmation to send
            if args.yes:
                result = send_draft(draft_result['draft_id'])
                if args.json:
                    print(json.dumps(result, indent=2))
                else:
                    print(f"\n[OK] Email forwarded to {args.to}")
            else:
                confirm = input("\n[!]  Send this forward now? (yes/no/keep-draft): ").strip().lower()
                if confirm in ['yes', 'y']:
                    result = send_draft(draft_result['draft_id'])
                    if args.json:
                        print(json.dumps(result, indent=2))
                    else:
                        print(f"\n[OK] Email forwarded to {args.to}")
                elif confirm in ['keep-draft', 'keep', 'draft', 'k', 'd']:
                    print(f"\n[>] Draft kept. Review and send from Gmail when ready.")
                    print(f"Draft ID: {draft_result['draft_id']}")
                else:
                    delete_draft(draft_result['draft_id'])
                    print("[ERROR] Forward cancelled and draft deleted.")

        elif args.command == "draft":
            result = create_draft(
                to=args.to,
                subject=args.subject,
                body=args.body
            )
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                print(f"[OK] Draft created")
                print(f"Draft ID: {result['draft_id']}")

        elif args.command == "drafts":
            result = list_drafts()
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                for draft in result:
                    print(f"* {draft['subject']}")
                    print(f"  To: {draft['to']}")
                    print(f"  Draft ID: {draft['draft_id']}")
                    print()

        elif args.command == "labels":
            result = list_labels()
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                for label in result:
                    print(f"* {label['name']} ({label['id']})")

        elif args.command == "trash":
            result = trash_email(args.message_id)
            print(f"[OK] Email moved to trash")

        elif args.command == "archive":
            result = archive_email(args.message_id)
            print(f"[OK] Email archived")

        elif args.command == "mark-read":
            result = mark_read(args.message_id)
            print(f"[OK] Email marked as read")

        elif args.command == "mark-unread":
            result = mark_unread(args.message_id)
            print(f"[OK] Email marked as unread")

    except Exception as e:
        print(f"[ERROR] {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
