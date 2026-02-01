#!/usr/bin/env python3
"""
Add sources to a NotebookLM notebook.

Supports: Google Drive, Web URLs, YouTube videos, and raw text.

Usage:
    # Add web URL
    python add_sources.py --notebook-id "abc123" --type web --url "https://example.com"

    # Add YouTube video
    python add_sources.py --notebook-id "abc123" --type youtube --url "https://youtube.com/watch?v=xxx"

    # Add text content
    python add_sources.py --notebook-id "abc123" --type text --content "Your text here..."

    # Add Google Drive file
    python add_sources.py --notebook-id "abc123" --type drive --resource-id "DRIVE_FILE_ID"

    # Add multiple URLs
    python add_sources.py --notebook-id "abc123" --type web --urls "url1,url2,url3"
"""

import argparse
import json
import sys
from pathlib import Path

# Add parent paths for imports
SCRIPT_DIR = Path(__file__).parent
MASTER_SCRIPTS = SCRIPT_DIR.parent.parent / "notebooklm-master" / "scripts"
sys.path.insert(0, str(MASTER_SCRIPTS))

from notebooklm_client import get_client


def add_sources(notebook_id: str, sources: list) -> dict:
    """
    Add sources to a notebook.

    Args:
        notebook_id: The notebook ID
        sources: List of source dicts with type-specific content

    Returns:
        dict with created source details
    """
    client = get_client()

    requests = []
    for source in sources:
        source_type = source.get("type")

        if source_type == "web":
            requests.append({
                "userContent": {
                    "webContent": {
                        "url": source.get("url")
                    }
                }
            })
        elif source_type == "youtube":
            requests.append({
                "userContent": {
                    "videoContent": {
                        "url": source.get("url")
                    }
                }
            })
        elif source_type == "text":
            requests.append({
                "userContent": {
                    "textContent": {
                        "text": source.get("content")
                    }
                }
            })
        elif source_type == "drive":
            requests.append({
                "userContent": {
                    "googleDriveContent": {
                        "resourceId": source.get("resource_id")
                    }
                }
            })

    return client.post(f"/notebooks/{notebook_id}/sources:batchCreate", {"requests": requests})


def main():
    parser = argparse.ArgumentParser(description="Add sources to NotebookLM notebook")
    parser.add_argument("--notebook-id", required=True, help="Notebook ID")
    parser.add_argument("--type", required=True, choices=["web", "youtube", "text", "drive"],
                        help="Source type")
    parser.add_argument("--url", help="URL for web/youtube sources")
    parser.add_argument("--urls", help="Comma-separated URLs for batch add")
    parser.add_argument("--content", help="Text content for text sources")
    parser.add_argument("--resource-id", help="Google Drive resource ID")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    # Build sources list
    sources = []
    source_type = args.type

    if args.urls:
        # Multiple URLs
        for url in args.urls.split(","):
            sources.append({"type": source_type, "url": url.strip()})
    elif args.url:
        sources.append({"type": source_type, "url": args.url})
    elif args.content:
        sources.append({"type": source_type, "content": args.content})
    elif args.resource_id:
        sources.append({"type": source_type, "resource_id": args.resource_id})
    else:
        print("Error: Must provide --url, --urls, --content, or --resource-id")
        sys.exit(1)

    try:
        result = add_sources(args.notebook_id, sources)

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"Successfully added {len(sources)} source(s)!")
            if "sources" in result:
                for source in result.get("sources", []):
                    print(f"  - {source.get('title', 'Untitled')} (ID: {source.get('sourceId')})")

    except Exception as e:
        if args.json:
            print(json.dumps({"error": str(e)}, indent=2))
        else:
            print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
