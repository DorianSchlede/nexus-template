#!/usr/bin/env python3
"""
Google Docs Operations

All CRUD operations for Google Docs:
- read: Read document content
- write: Write/replace content in a document
- insert: Insert text at a specific location
- create: Create a new document
- list: List documents
- info: Get document metadata
- export: Export document to various formats
- replace: Find and replace text
- format: Apply formatting to text
"""

import os
import sys
import json
import argparse
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
    """Get authenticated Docs service."""
    return _get_service('docs')

def get_drive_service():
    """Get authenticated Drive service (for creating/listing docs)."""
    return _get_service('drive')

# =============================================================================
# READ OPERATIONS
# =============================================================================

def read_document(document_id: str, include_formatting: bool = False):
    """
    Read the full content of a document.

    Args:
        document_id: The document ID (from URL)
        include_formatting: If True, include formatting metadata

    Returns:
        Document content as plain text, or full structure if include_formatting=True
    """
    service = get_service()
    doc = service.documents().get(documentId=document_id).execute()

    if include_formatting:
        return doc

    # Extract plain text from document body
    content = doc.get('body', {}).get('content', [])
    text_parts = []

    for element in content:
        if 'paragraph' in element:
            para = element['paragraph']
            para_text = ''
            for elem in para.get('elements', []):
                if 'textRun' in elem:
                    para_text += elem['textRun'].get('content', '')
            text_parts.append(para_text)
        elif 'table' in element:
            # Extract text from tables
            table = element['table']
            for row in table.get('tableRows', []):
                row_texts = []
                for cell in row.get('tableCells', []):
                    cell_text = ''
                    for cell_content in cell.get('content', []):
                        if 'paragraph' in cell_content:
                            for elem in cell_content['paragraph'].get('elements', []):
                                if 'textRun' in elem:
                                    cell_text += elem['textRun'].get('content', '').strip()
                    row_texts.append(cell_text)
                text_parts.append('\t'.join(row_texts) + '\n')

    return ''.join(text_parts)

def get_document_info(document_id: str):
    """Get document metadata."""
    service = get_service()
    doc = service.documents().get(documentId=document_id).execute()

    # Get document end index for positioning
    body = doc.get('body', {})
    content = body.get('content', [])
    end_index = 1
    if content:
        last_element = content[-1]
        end_index = last_element.get('endIndex', 1)

    return {
        "document_id": document_id,
        "title": doc.get('title', ''),
        "revision_id": doc.get('revisionId', ''),
        "end_index": end_index,
        "url": f"https://docs.google.com/document/d/{document_id}/edit"
    }

# =============================================================================
# WRITE OPERATIONS
# =============================================================================

def insert_text(document_id: str, text: str, index: int = 1):
    """
    Insert text at a specific index.

    Args:
        document_id: The document ID
        text: Text to insert
        index: Position to insert at (1 = start of document)

    Returns:
        Update result
    """
    service = get_service()

    requests = [{
        'insertText': {
            'location': {'index': index},
            'text': text
        }
    }]

    result = service.documents().batchUpdate(
        documentId=document_id,
        body={'requests': requests}
    ).execute()

    return {
        "document_id": document_id,
        "inserted_at": index,
        "text_length": len(text)
    }

def append_text(document_id: str, text: str):
    """
    Append text to the end of the document.

    Args:
        document_id: The document ID
        text: Text to append

    Returns:
        Update result
    """
    # Get current end index
    info = get_document_info(document_id)
    # Insert before the final newline (end_index - 1)
    insert_index = max(1, info['end_index'] - 1)

    return insert_text(document_id, text, insert_index)

def replace_all_text(document_id: str, find_text: str, replace_text: str, match_case: bool = True):
    """
    Find and replace all occurrences of text.

    Args:
        document_id: The document ID
        find_text: Text to find
        replace_text: Text to replace with
        match_case: Whether to match case

    Returns:
        Number of replacements made
    """
    service = get_service()

    requests = [{
        'replaceAllText': {
            'containsText': {
                'text': find_text,
                'matchCase': match_case
            },
            'replaceText': replace_text
        }
    }]

    result = service.documents().batchUpdate(
        documentId=document_id,
        body={'requests': requests}
    ).execute()

    replies = result.get('replies', [])
    occurrences = 0
    if replies and 'replaceAllText' in replies[0]:
        occurrences = replies[0]['replaceAllText'].get('occurrencesChanged', 0)

    return {
        "document_id": document_id,
        "find": find_text,
        "replace": replace_text,
        "occurrences_changed": occurrences
    }

def delete_content(document_id: str, start_index: int, end_index: int):
    """
    Delete content between two indices.

    Args:
        document_id: The document ID
        start_index: Start position
        end_index: End position

    Returns:
        Delete result
    """
    service = get_service()

    requests = [{
        'deleteContentRange': {
            'range': {
                'startIndex': start_index,
                'endIndex': end_index
            }
        }
    }]

    result = service.documents().batchUpdate(
        documentId=document_id,
        body={'requests': requests}
    ).execute()

    return {
        "document_id": document_id,
        "deleted_range": f"{start_index}-{end_index}"
    }

def clear_document(document_id: str):
    """
    Clear all content from a document (keeps the document).

    Args:
        document_id: The document ID

    Returns:
        Clear result
    """
    info = get_document_info(document_id)
    end_index = info['end_index']

    if end_index > 2:
        # Delete from index 1 to end-1 (preserve the final newline structure)
        return delete_content(document_id, 1, end_index - 1)

    return {"document_id": document_id, "message": "Document already empty"}

# =============================================================================
# CREATE OPERATIONS
# =============================================================================

def create_document(title: str, content: str = None):
    """
    Create a new Google Doc.

    Args:
        title: Document title
        content: Optional initial content

    Returns:
        New document info with ID and URL
    """
    service = get_service()

    doc = service.documents().create(body={'title': title}).execute()
    document_id = doc['documentId']

    result = {
        "document_id": document_id,
        "title": title,
        "url": f"https://docs.google.com/document/d/{document_id}/edit"
    }

    # Add initial content if provided
    if content:
        insert_text(document_id, content, 1)
        result["initial_content_added"] = True

    return result

def copy_document(source_id: str, new_title: str):
    """
    Create a copy of an existing document.

    Args:
        source_id: Source document ID
        new_title: Title for the copy

    Returns:
        New document info
    """
    drive_service = get_drive_service()

    result = drive_service.files().copy(
        fileId=source_id,
        body={'name': new_title}
    ).execute()

    return {
        "document_id": result['id'],
        "title": new_title,
        "url": f"https://docs.google.com/document/d/{result['id']}/edit",
        "source_id": source_id
    }

# =============================================================================
# FORMAT OPERATIONS
# =============================================================================

def format_text(document_id: str, start_index: int, end_index: int,
                bold: bool = None, italic: bool = None, underline: bool = None,
                font_size: int = None, font_family: str = None,
                foreground_color: dict = None, background_color: dict = None):
    """
    Apply formatting to a text range.

    Args:
        document_id: The document ID
        start_index: Start of range
        end_index: End of range
        bold: Make text bold
        italic: Make text italic
        underline: Underline text
        font_size: Font size in points
        font_family: Font family name
        foreground_color: Text color as {"red": 0-1, "green": 0-1, "blue": 0-1}
        background_color: Highlight color as {"red": 0-1, "green": 0-1, "blue": 0-1}

    Returns:
        Format result
    """
    service = get_service()

    text_style = {}
    fields = []

    if bold is not None:
        text_style['bold'] = bold
        fields.append('bold')
    if italic is not None:
        text_style['italic'] = italic
        fields.append('italic')
    if underline is not None:
        text_style['underline'] = underline
        fields.append('underline')
    if font_size is not None:
        text_style['fontSize'] = {'magnitude': font_size, 'unit': 'PT'}
        fields.append('fontSize')
    if font_family is not None:
        text_style['weightedFontFamily'] = {'fontFamily': font_family}
        fields.append('weightedFontFamily')
    if foreground_color is not None:
        text_style['foregroundColor'] = {'color': {'rgbColor': foreground_color}}
        fields.append('foregroundColor')
    if background_color is not None:
        text_style['backgroundColor'] = {'color': {'rgbColor': background_color}}
        fields.append('backgroundColor')

    if not text_style:
        return {"error": "No formatting options specified"}

    requests = [{
        'updateTextStyle': {
            'range': {
                'startIndex': start_index,
                'endIndex': end_index
            },
            'textStyle': text_style,
            'fields': ','.join(fields)
        }
    }]

    result = service.documents().batchUpdate(
        documentId=document_id,
        body={'requests': requests}
    ).execute()

    return {
        "document_id": document_id,
        "formatted_range": f"{start_index}-{end_index}",
        "applied_styles": fields
    }

def insert_heading(document_id: str, text: str, heading_level: int = 1, index: int = 1):
    """
    Insert a heading at a specific position.

    Args:
        document_id: The document ID
        text: Heading text
        heading_level: 1-6 for different heading sizes
        index: Position to insert at

    Returns:
        Insert result
    """
    service = get_service()

    # Map heading level to named style
    heading_styles = {
        1: 'HEADING_1',
        2: 'HEADING_2',
        3: 'HEADING_3',
        4: 'HEADING_4',
        5: 'HEADING_5',
        6: 'HEADING_6'
    }
    style = heading_styles.get(heading_level, 'HEADING_1')

    # Insert text with newline
    text_with_newline = text + '\n'

    requests = [
        {
            'insertText': {
                'location': {'index': index},
                'text': text_with_newline
            }
        },
        {
            'updateParagraphStyle': {
                'range': {
                    'startIndex': index,
                    'endIndex': index + len(text_with_newline)
                },
                'paragraphStyle': {
                    'namedStyleType': style
                },
                'fields': 'namedStyleType'
            }
        }
    ]

    result = service.documents().batchUpdate(
        documentId=document_id,
        body={'requests': requests}
    ).execute()

    return {
        "document_id": document_id,
        "heading_level": heading_level,
        "inserted_at": index
    }

def insert_bullet_list(document_id: str, items: list, index: int = 1):
    """
    Insert a bullet list.

    Args:
        document_id: The document ID
        items: List of text items
        index: Position to insert at

    Returns:
        Insert result
    """
    service = get_service()

    # Create text with newlines
    text = '\n'.join(items) + '\n'

    requests = [
        {
            'insertText': {
                'location': {'index': index},
                'text': text
            }
        },
        {
            'createParagraphBullets': {
                'range': {
                    'startIndex': index,
                    'endIndex': index + len(text)
                },
                'bulletPreset': 'BULLET_DISC_CIRCLE_SQUARE'
            }
        }
    ]

    result = service.documents().batchUpdate(
        documentId=document_id,
        body={'requests': requests}
    ).execute()

    return {
        "document_id": document_id,
        "items_added": len(items),
        "inserted_at": index
    }

def insert_table(document_id: str, rows: int, columns: int, index: int = 1, data: list = None):
    """
    Insert a table.

    Args:
        document_id: The document ID
        rows: Number of rows
        columns: Number of columns
        index: Position to insert at
        data: Optional 2D list of cell content

    Returns:
        Insert result
    """
    service = get_service()

    requests = [{
        'insertTable': {
            'rows': rows,
            'columns': columns,
            'location': {'index': index}
        }
    }]

    result = service.documents().batchUpdate(
        documentId=document_id,
        body={'requests': requests}
    ).execute()

    # If data provided, we'd need to populate cells (complex operation)
    # For now, just create the empty table

    return {
        "document_id": document_id,
        "table_size": f"{rows}x{columns}",
        "inserted_at": index,
        "note": "Table created. Populate cells manually or use insert_text with calculated indices."
    }

# =============================================================================
# EXPORT OPERATIONS
# =============================================================================

def export_document(document_id: str, format: str = "text", output_path: str = None):
    """
    Export document to various formats.

    Args:
        document_id: The document ID
        format: Export format (text, html, pdf, docx)
        output_path: Optional path to save file

    Returns:
        Content or file path
    """
    drive_service = get_drive_service()

    mime_types = {
        'text': 'text/plain',
        'html': 'text/html',
        'pdf': 'application/pdf',
        'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    }

    mime_type = mime_types.get(format, 'text/plain')

    content = drive_service.files().export(
        fileId=document_id,
        mimeType=mime_type
    ).execute()

    if output_path:
        mode = 'wb' if format in ['pdf', 'docx'] else 'w'
        with open(output_path, mode) as f:
            if isinstance(content, bytes):
                f.write(content)
            else:
                f.write(content.decode('utf-8') if isinstance(content, bytes) else content)
        return {"exported_to": output_path, "format": format}

    if format in ['pdf', 'docx']:
        return {"content_type": "binary", "size_bytes": len(content)}

    return content.decode('utf-8') if isinstance(content, bytes) else content

# =============================================================================
# RENAME OPERATIONS
# =============================================================================

def rename_document(document_id: str, new_title: str):
    """
    Rename a document.

    Args:
        document_id: The document ID
        new_title: New title for the document

    Returns:
        Updated document info
    """
    drive_service = get_drive_service()

    result = drive_service.files().update(
        fileId=document_id,
        body={'name': new_title}
    ).execute()

    return {
        "document_id": document_id,
        "title": result['name'],
        "url": f"https://docs.google.com/document/d/{document_id}/edit"
    }

# =============================================================================
# LIST OPERATIONS
# =============================================================================

def list_documents(query: str = None, limit: int = 10):
    """
    List documents accessible to the user.

    Args:
        query: Optional search query
        limit: Max results to return
    """
    drive_service = get_drive_service()

    q = "mimeType='application/vnd.google-apps.document'"
    if query:
        q += f" and name contains '{query}'"

    result = drive_service.files().list(
        q=q,
        pageSize=limit,
        fields="files(id, name, modifiedTime, webViewLink)"
    ).execute()

    return [
        {
            "id": f["id"],
            "name": f["name"],
            "modified": f.get("modifiedTime"),
            "url": f.get("webViewLink")
        }
        for f in result.get("files", [])
    ]

# =============================================================================
# BATCH OPERATIONS
# =============================================================================

def batch_update(document_id: str, requests: list):
    """
    Execute multiple operations in a single request.

    Args:
        document_id: The document ID
        requests: List of request objects

    Returns:
        Batch update result
    """
    service = get_service()

    result = service.documents().batchUpdate(
        documentId=document_id,
        body={'requests': requests}
    ).execute()

    return {
        "document_id": document_id,
        "requests_executed": len(requests),
        "replies": result.get('replies', [])
    }

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

    parser = argparse.ArgumentParser(description="Google Docs Operations")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Read
    read_parser = subparsers.add_parser("read", help="Read document content")
    read_parser.add_argument("document_id", help="Document ID")
    read_parser.add_argument("--full", action="store_true", help="Include full structure with formatting")
    read_parser.add_argument("--json", action="store_true", help="Output as JSON")

    # Info
    info_parser = subparsers.add_parser("info", help="Get document info")
    info_parser.add_argument("document_id", help="Document ID")
    info_parser.add_argument("--json", action="store_true", help="Output as JSON")

    # Create
    create_parser = subparsers.add_parser("create", help="Create new document")
    create_parser.add_argument("title", help="Document title")
    create_parser.add_argument("--content", help="Initial content")
    create_parser.add_argument("--json", action="store_true", help="Output as JSON")

    # Insert
    insert_parser = subparsers.add_parser("insert", help="Insert text at position")
    insert_parser.add_argument("document_id", help="Document ID")
    insert_parser.add_argument("text", help="Text to insert")
    insert_parser.add_argument("--index", type=int, default=1, help="Position (1=start)")
    insert_parser.add_argument("--json", action="store_true", help="Output as JSON")

    # Append
    append_parser = subparsers.add_parser("append", help="Append text to end")
    append_parser.add_argument("document_id", help="Document ID")
    append_parser.add_argument("text", help="Text to append")
    append_parser.add_argument("--json", action="store_true", help="Output as JSON")

    # Replace
    replace_parser = subparsers.add_parser("replace", help="Find and replace text")
    replace_parser.add_argument("document_id", help="Document ID")
    replace_parser.add_argument("find", help="Text to find")
    replace_parser.add_argument("replace_with", help="Replacement text")
    replace_parser.add_argument("--no-case", action="store_true", help="Case insensitive")
    replace_parser.add_argument("--json", action="store_true", help="Output as JSON")

    # Export
    export_parser = subparsers.add_parser("export", help="Export document")
    export_parser.add_argument("document_id", help="Document ID")
    export_parser.add_argument("--format", choices=['text', 'html', 'pdf', 'docx'], default='text')
    export_parser.add_argument("--output", help="Output file path")

    # List
    list_parser = subparsers.add_parser("list", help="List documents")
    list_parser.add_argument("--query", help="Search query")
    list_parser.add_argument("--limit", type=int, default=10, help="Max results")
    list_parser.add_argument("--json", action="store_true", help="Output as JSON")

    # Copy
    copy_parser = subparsers.add_parser("copy", help="Copy a document")
    copy_parser.add_argument("document_id", help="Source document ID")
    copy_parser.add_argument("title", help="New document title")
    copy_parser.add_argument("--json", action="store_true", help="Output as JSON")

    # Clear
    clear_parser = subparsers.add_parser("clear", help="Clear document content")
    clear_parser.add_argument("document_id", help="Document ID")

    # Rename
    rename_parser = subparsers.add_parser("rename", help="Rename a document")
    rename_parser.add_argument("document_id", help="Document ID")
    rename_parser.add_argument("title", help="New document title")
    rename_parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if not check_dependencies():
        print("[ERROR] Missing dependencies. Run:")
        print("  pip install google-auth google-auth-oauthlib google-api-python-client")
        sys.exit(1)

    try:
        if args.command == "read":
            result = read_document(args.document_id, include_formatting=args.full)
            if args.json or args.full:
                print(json.dumps(result, indent=2) if isinstance(result, dict) else result)
            else:
                print(result)

        elif args.command == "info":
            result = get_document_info(args.document_id)
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                print(f"Title: {result['title']}")
                print(f"ID: {result['document_id']}")
                print(f"URL: {result['url']}")
                print(f"End Index: {result['end_index']}")

        elif args.command == "create":
            result = create_document(args.title, args.content)
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                print(f"✅ Created: {result['title']}")
                print(f"ID: {result['document_id']}")
                print(f"URL: {result['url']}")

        elif args.command == "insert":
            result = insert_text(args.document_id, args.text, args.index)
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                print(f"✅ Inserted {result['text_length']} characters at index {result['inserted_at']}")

        elif args.command == "append":
            result = append_text(args.document_id, args.text)
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                print(f"✅ Appended {result['text_length']} characters")

        elif args.command == "replace":
            result = replace_all_text(args.document_id, args.find, args.replace_with,
                                      match_case=not args.no_case)
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                print(f"✅ Replaced {result['occurrences_changed']} occurrences")

        elif args.command == "export":
            result = export_document(args.document_id, args.format, args.output)
            if args.output:
                print(f"✅ Exported to: {result['exported_to']}")
            else:
                print(result)

        elif args.command == "list":
            result = list_documents(args.query, args.limit)
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                for item in result:
                    print(f"• {item['name']}")
                    print(f"  ID: {item['id']}")

        elif args.command == "copy":
            result = copy_document(args.document_id, args.title)
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                print(f"✅ Copied to: {result['title']}")
                print(f"ID: {result['document_id']}")
                print(f"URL: {result['url']}")

        elif args.command == "clear":
            result = clear_document(args.document_id)
            print(f"✅ Cleared document")

        elif args.command == "rename":
            result = rename_document(args.document_id, args.title)
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                print(f"✅ Renamed to: {result['title']}")
                print(f"URL: {result['url']}")

    except Exception as e:
        print(f"[ERROR] {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
