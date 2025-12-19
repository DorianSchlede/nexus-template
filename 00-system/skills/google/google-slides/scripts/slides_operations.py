#!/usr/bin/env python3
"""
Google Slides Operations

All operations for Google Slides:
- list: List presentations
- info: Get presentation info
- create: Create a presentation
- read: Read slide content
- add-slide: Add a new slide
- delete-slide: Delete a slide
- add-text: Add text to a slide
- add-image: Add image to a slide
- duplicate: Duplicate a presentation
- export: Export to PDF/PPTX
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

def get_slides_service():
    """Get authenticated Slides service."""
    return _get_service('slides')

def get_drive_service():
    """Get authenticated Drive service."""
    return _get_service('drive')

# =============================================================================
# PREDEFINED LAYOUTS
# =============================================================================

LAYOUT_TYPES = {
    'blank': 'BLANK',
    'title': 'TITLE',
    'title_body': 'TITLE_AND_BODY',
    'title_two_columns': 'TITLE_AND_TWO_COLUMNS',
    'title_only': 'TITLE_ONLY',
    'section': 'SECTION_HEADER',
    'big_number': 'BIG_NUMBER',
    'caption': 'CAPTION_ONLY',
}

# =============================================================================
# PRESENTATION OPERATIONS
# =============================================================================

def list_presentations(max_results: int = 20, query: str = None):
    """
    List Google Slides presentations.

    Args:
        max_results: Maximum number of results
        query: Search query (optional)

    Returns:
        List of presentations
    """
    drive = get_drive_service()

    q = "mimeType='application/vnd.google-apps.presentation' and trashed=false"
    if query:
        q += f" and name contains '{query}'"

    results = drive.files().list(
        q=q,
        pageSize=max_results,
        fields="files(id, name, modifiedTime, webViewLink)"
    ).execute()

    files = results.get('files', [])

    return [{
        'id': f['id'],
        'name': f['name'],
        'modified': f.get('modifiedTime', ''),
        'url': f.get('webViewLink', '')
    } for f in files]


def get_presentation_info(presentation_id: str):
    """
    Get presentation metadata and structure.

    Args:
        presentation_id: The presentation ID

    Returns:
        Presentation info with slide count
    """
    slides = get_slides_service()

    presentation = slides.presentations().get(presentationId=presentation_id).execute()

    slides_list = presentation.get('slides', [])

    return {
        'id': presentation['presentationId'],
        'title': presentation.get('title', ''),
        'slide_count': len(slides_list),
        'slides': [{
            'id': s['objectId'],
            'index': i + 1
        } for i, s in enumerate(slides_list)],
        'page_size': {
            'width': presentation.get('pageSize', {}).get('width', {}).get('magnitude', 0),
            'height': presentation.get('pageSize', {}).get('height', {}).get('magnitude', 0)
        }
    }


def create_presentation(title: str):
    """
    Create a new presentation.

    Args:
        title: Presentation title

    Returns:
        Created presentation info
    """
    slides = get_slides_service()

    presentation = slides.presentations().create(body={'title': title}).execute()

    return {
        'id': presentation['presentationId'],
        'title': presentation.get('title', ''),
        'url': f"https://docs.google.com/presentation/d/{presentation['presentationId']}/edit"
    }


def read_slide(presentation_id: str, slide_index: int = None, slide_id: str = None):
    """
    Read content from a slide.

    Args:
        presentation_id: The presentation ID
        slide_index: Slide index (1-based) OR
        slide_id: Slide object ID

    Returns:
        Slide content
    """
    slides = get_slides_service()

    presentation = slides.presentations().get(presentationId=presentation_id).execute()
    slides_list = presentation.get('slides', [])

    # Find the slide
    if slide_id:
        slide = next((s for s in slides_list if s['objectId'] == slide_id), None)
    elif slide_index:
        if 1 <= slide_index <= len(slides_list):
            slide = slides_list[slide_index - 1]
        else:
            raise ValueError(f"Slide index {slide_index} out of range (1-{len(slides_list)})")
    else:
        raise ValueError("Must specify either slide_index or slide_id")

    if not slide:
        raise ValueError("Slide not found")

    # Extract text content
    texts = []
    for element in slide.get('pageElements', []):
        if 'shape' in element and 'text' in element['shape']:
            text_content = element['shape']['text']
            for text_element in text_content.get('textElements', []):
                if 'textRun' in text_element:
                    texts.append(text_element['textRun'].get('content', '').strip())

    return {
        'slide_id': slide['objectId'],
        'texts': [t for t in texts if t],
        'element_count': len(slide.get('pageElements', []))
    }

# =============================================================================
# SLIDE MANIPULATION
# =============================================================================

def add_slide(presentation_id: str, layout: str = 'blank', index: int = None):
    """
    Add a new slide to the presentation.

    Args:
        presentation_id: The presentation ID
        layout: Layout type (blank, title, title_body, section, etc.)
        index: Position to insert (optional, appends if not specified)

    Returns:
        New slide info
    """
    slides = get_slides_service()

    # Get layout ID
    layout_type = LAYOUT_TYPES.get(layout, 'BLANK')

    # Generate unique ID
    import uuid
    slide_id = f"slide_{uuid.uuid4().hex[:8]}"

    requests = [{
        'createSlide': {
            'objectId': slide_id,
            'insertionIndex': index if index else None,
            'slideLayoutReference': {
                'predefinedLayout': layout_type
            }
        }
    }]

    # Remove None values
    if index is None:
        del requests[0]['createSlide']['insertionIndex']

    slides.presentations().batchUpdate(
        presentationId=presentation_id,
        body={'requests': requests}
    ).execute()

    return {
        'slide_id': slide_id,
        'layout': layout,
        'index': index
    }


def delete_slide(presentation_id: str, slide_id: str):
    """
    Delete a slide from the presentation.

    Args:
        presentation_id: The presentation ID
        slide_id: Slide object ID

    Returns:
        Deletion status
    """
    slides = get_slides_service()

    requests = [{
        'deleteObject': {
            'objectId': slide_id
        }
    }]

    slides.presentations().batchUpdate(
        presentationId=presentation_id,
        body={'requests': requests}
    ).execute()

    return {'slide_id': slide_id, 'status': 'deleted'}


def add_text_box(presentation_id: str, slide_id: str, text: str,
                 x: float = 100, y: float = 100, width: float = 400, height: float = 50):
    """
    Add a text box to a slide.

    Args:
        presentation_id: The presentation ID
        slide_id: Slide object ID
        text: Text content
        x, y: Position in points
        width, height: Size in points

    Returns:
        Text box info
    """
    slides = get_slides_service()

    import uuid
    element_id = f"textbox_{uuid.uuid4().hex[:8]}"

    requests = [
        {
            'createShape': {
                'objectId': element_id,
                'shapeType': 'TEXT_BOX',
                'elementProperties': {
                    'pageObjectId': slide_id,
                    'size': {
                        'width': {'magnitude': width, 'unit': 'PT'},
                        'height': {'magnitude': height, 'unit': 'PT'}
                    },
                    'transform': {
                        'scaleX': 1,
                        'scaleY': 1,
                        'translateX': x,
                        'translateY': y,
                        'unit': 'PT'
                    }
                }
            }
        },
        {
            'insertText': {
                'objectId': element_id,
                'text': text,
                'insertionIndex': 0
            }
        }
    ]

    slides.presentations().batchUpdate(
        presentationId=presentation_id,
        body={'requests': requests}
    ).execute()

    return {
        'element_id': element_id,
        'slide_id': slide_id,
        'text': text
    }


def add_image(presentation_id: str, slide_id: str, image_url: str,
              x: float = 100, y: float = 100, width: float = 300, height: float = 200):
    """
    Add an image to a slide.

    Args:
        presentation_id: The presentation ID
        slide_id: Slide object ID
        image_url: URL of the image (must be publicly accessible)
        x, y: Position in points
        width, height: Size in points

    Returns:
        Image element info
    """
    slides = get_slides_service()

    import uuid
    element_id = f"image_{uuid.uuid4().hex[:8]}"

    requests = [{
        'createImage': {
            'objectId': element_id,
            'url': image_url,
            'elementProperties': {
                'pageObjectId': slide_id,
                'size': {
                    'width': {'magnitude': width, 'unit': 'PT'},
                    'height': {'magnitude': height, 'unit': 'PT'}
                },
                'transform': {
                    'scaleX': 1,
                    'scaleY': 1,
                    'translateX': x,
                    'translateY': y,
                    'unit': 'PT'
                }
            }
        }
    }]

    slides.presentations().batchUpdate(
        presentationId=presentation_id,
        body={'requests': requests}
    ).execute()

    return {
        'element_id': element_id,
        'slide_id': slide_id,
        'image_url': image_url
    }


def duplicate_presentation(presentation_id: str, new_title: str):
    """
    Duplicate a presentation.

    Args:
        presentation_id: The presentation ID to copy
        new_title: Title for the copy

    Returns:
        New presentation info
    """
    drive = get_drive_service()

    copy = drive.files().copy(
        fileId=presentation_id,
        body={'name': new_title}
    ).execute()

    return {
        'id': copy['id'],
        'name': copy['name'],
        'url': f"https://docs.google.com/presentation/d/{copy['id']}/edit"
    }


def export_presentation(presentation_id: str, output_path: str, format: str = 'pdf'):
    """
    Export presentation to PDF or PPTX.

    Args:
        presentation_id: The presentation ID
        output_path: Local path to save
        format: Export format (pdf or pptx)

    Returns:
        Export info
    """
    from googleapiclient.http import MediaIoBaseDownload

    drive = get_drive_service()

    mime_types = {
        'pdf': 'application/pdf',
        'pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation'
    }

    if format not in mime_types:
        raise ValueError(f"Unsupported format: {format}. Use 'pdf' or 'pptx'")

    request = drive.files().export_media(
        fileId=presentation_id,
        mimeType=mime_types[format]
    )

    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)

    done = False
    while not done:
        status, done = downloader.next_chunk()

    with open(output_path, 'wb') as f:
        f.write(fh.getvalue())

    return {
        'presentation_id': presentation_id,
        'output_path': output_path,
        'format': format,
        'size': len(fh.getvalue())
    }

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
        description="Google Slides Operations",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # List presentations command
    list_parser = subparsers.add_parser('list', help='List presentations')
    list_parser.add_argument('--max', type=int, default=20, help='Max results')
    list_parser.add_argument('--query', help='Search query')

    # Info command
    info_parser = subparsers.add_parser('info', help='Get presentation info')
    info_parser.add_argument('presentation_id', help='Presentation ID')

    # Create command
    create_parser = subparsers.add_parser('create', help='Create a presentation')
    create_parser.add_argument('title', help='Presentation title')

    # Read slide command
    read_parser = subparsers.add_parser('read', help='Read slide content')
    read_parser.add_argument('presentation_id', help='Presentation ID')
    read_parser.add_argument('--slide', type=int, help='Slide index (1-based)')
    read_parser.add_argument('--slide-id', help='Slide object ID')

    # Add slide command
    add_slide_parser = subparsers.add_parser('add-slide', help='Add a new slide')
    add_slide_parser.add_argument('presentation_id', help='Presentation ID')
    add_slide_parser.add_argument('--layout', default='blank',
                                  choices=list(LAYOUT_TYPES.keys()))
    add_slide_parser.add_argument('--index', type=int, help='Insert position')

    # Delete slide command
    del_slide_parser = subparsers.add_parser('delete-slide', help='Delete a slide')
    del_slide_parser.add_argument('presentation_id', help='Presentation ID')
    del_slide_parser.add_argument('slide_id', help='Slide object ID')

    # Add text command
    add_text_parser = subparsers.add_parser('add-text', help='Add text box to slide')
    add_text_parser.add_argument('presentation_id', help='Presentation ID')
    add_text_parser.add_argument('slide_id', help='Slide object ID')
    add_text_parser.add_argument('text', help='Text content')
    add_text_parser.add_argument('--x', type=float, default=100, help='X position (points)')
    add_text_parser.add_argument('--y', type=float, default=100, help='Y position (points)')
    add_text_parser.add_argument('--width', type=float, default=400, help='Width (points)')
    add_text_parser.add_argument('--height', type=float, default=50, help='Height (points)')

    # Add image command
    add_image_parser = subparsers.add_parser('add-image', help='Add image to slide')
    add_image_parser.add_argument('presentation_id', help='Presentation ID')
    add_image_parser.add_argument('slide_id', help='Slide object ID')
    add_image_parser.add_argument('image_url', help='Image URL')
    add_image_parser.add_argument('--x', type=float, default=100, help='X position (points)')
    add_image_parser.add_argument('--y', type=float, default=100, help='Y position (points)')
    add_image_parser.add_argument('--width', type=float, default=300, help='Width (points)')
    add_image_parser.add_argument('--height', type=float, default=200, help='Height (points)')

    # Duplicate command
    dup_parser = subparsers.add_parser('duplicate', help='Duplicate a presentation')
    dup_parser.add_argument('presentation_id', help='Presentation ID')
    dup_parser.add_argument('new_title', help='New title')

    # Export command
    export_parser = subparsers.add_parser('export', help='Export to PDF/PPTX')
    export_parser.add_argument('presentation_id', help='Presentation ID')
    export_parser.add_argument('output', help='Output file path')
    export_parser.add_argument('--format', choices=['pdf', 'pptx'], default='pdf')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    try:
        if args.command == 'list':
            result = list_presentations(args.max, args.query)
        elif args.command == 'info':
            result = get_presentation_info(args.presentation_id)
        elif args.command == 'create':
            result = create_presentation(args.title)
        elif args.command == 'read':
            result = read_slide(args.presentation_id, args.slide, args.slide_id)
        elif args.command == 'add-slide':
            result = add_slide(args.presentation_id, args.layout, args.index)
        elif args.command == 'delete-slide':
            result = delete_slide(args.presentation_id, args.slide_id)
        elif args.command == 'add-text':
            result = add_text_box(args.presentation_id, args.slide_id, args.text,
                                 args.x, args.y, args.width, args.height)
        elif args.command == 'add-image':
            result = add_image(args.presentation_id, args.slide_id, args.image_url,
                              args.x, args.y, args.width, args.height)
        elif args.command == 'duplicate':
            result = duplicate_presentation(args.presentation_id, args.new_title)
        elif args.command == 'export':
            result = export_presentation(args.presentation_id, args.output, args.format)
        else:
            parser.print_help()
            return

        print(json.dumps(result, indent=2, default=str))

    except Exception as e:
        print(json.dumps({'error': str(e)}, indent=2))
        sys.exit(1)

if __name__ == "__main__":
    main()
