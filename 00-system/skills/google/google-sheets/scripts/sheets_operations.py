#!/usr/bin/env python3
"""
Google Sheets Operations

All CRUD operations for Google Sheets:
- read: Read data from a range
- write: Write data to a range
- append: Append rows to a sheet
- clear: Clear a range
- create: Create a new spreadsheet
- list: List sheets in a spreadsheet
- format: Apply formatting to cells
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
    """Get authenticated Sheets service."""
    return _get_service('sheets')

def get_drive_service():
    """Get authenticated Drive service (for listing spreadsheets)."""
    return _get_service('drive')

# =============================================================================
# READ OPERATIONS
# =============================================================================

def read_range(spreadsheet_id: str, range_name: str, value_render: str = "FORMATTED_VALUE"):
    """
    Read data from a spreadsheet range.

    Args:
        spreadsheet_id: The spreadsheet ID (from URL)
        range_name: A1 notation range (e.g., "Sheet1!A1:D10" or "A1:D10")
        value_render: How to render values (FORMATTED_VALUE, UNFORMATTED_VALUE, FORMULA)

    Returns:
        List of rows, each row is a list of cell values
    """
    service = get_service()
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=range_name,
        valueRenderOption=value_render
    ).execute()

    values = result.get('values', [])
    return values

def get_spreadsheet_info(spreadsheet_id: str):
    """Get spreadsheet metadata including all sheet names."""
    service = get_service()
    result = service.spreadsheets().get(
        spreadsheetId=spreadsheet_id,
        fields="properties.title,sheets.properties"
    ).execute()

    info = {
        "title": result["properties"]["title"],
        "spreadsheet_id": spreadsheet_id,
        "sheets": [
            {
                "name": sheet["properties"]["title"],
                "id": sheet["properties"]["sheetId"],
                "index": sheet["properties"]["index"]
            }
            for sheet in result.get("sheets", [])
        ]
    }
    return info

# =============================================================================
# WRITE OPERATIONS
# =============================================================================

def write_range(spreadsheet_id: str, range_name: str, values: list, value_input: str = "USER_ENTERED"):
    """
    Write data to a spreadsheet range.

    Args:
        spreadsheet_id: The spreadsheet ID
        range_name: A1 notation range (e.g., "Sheet1!A1:D10")
        values: 2D list of values [[row1], [row2], ...]
        value_input: How to interpret input (USER_ENTERED or RAW)

    Returns:
        Update result with updated range and cell count
    """
    service = get_service()
    body = {"values": values}

    result = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=range_name,
        valueInputOption=value_input,
        body=body
    ).execute()

    return {
        "updated_range": result.get("updatedRange"),
        "updated_rows": result.get("updatedRows"),
        "updated_columns": result.get("updatedColumns"),
        "updated_cells": result.get("updatedCells")
    }

def append_rows(spreadsheet_id: str, range_name: str, values: list, value_input: str = "USER_ENTERED"):
    """
    Append rows to the end of a table.

    Args:
        spreadsheet_id: The spreadsheet ID
        range_name: A1 notation range to append after (e.g., "Sheet1!A:D")
        values: 2D list of rows to append [[row1], [row2], ...]
        value_input: How to interpret input (USER_ENTERED or RAW)

    Returns:
        Append result with updated range
    """
    service = get_service()
    body = {"values": values}

    result = service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range=range_name,
        valueInputOption=value_input,
        insertDataOption="INSERT_ROWS",
        body=body
    ).execute()

    updates = result.get("updates", {})
    return {
        "updated_range": updates.get("updatedRange"),
        "updated_rows": updates.get("updatedRows"),
        "updated_cells": updates.get("updatedCells")
    }

def clear_range(spreadsheet_id: str, range_name: str):
    """Clear values from a range (keeps formatting)."""
    service = get_service()
    service.spreadsheets().values().clear(
        spreadsheetId=spreadsheet_id,
        range=range_name
    ).execute()
    return {"cleared": range_name}

def batch_update(spreadsheet_id: str, data: list, value_input: str = "USER_ENTERED"):
    """
    Update multiple ranges in one request.

    Args:
        spreadsheet_id: The spreadsheet ID
        data: List of {"range": "A1:B2", "values": [[...]]}
        value_input: How to interpret input

    Returns:
        Batch update results
    """
    service = get_service()
    body = {
        "valueInputOption": value_input,
        "data": data
    }

    result = service.spreadsheets().values().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body=body
    ).execute()

    return {
        "total_updated_sheets": result.get("totalUpdatedSheets"),
        "total_updated_cells": result.get("totalUpdatedCells"),
        "responses": result.get("responses", [])
    }

# =============================================================================
# CREATE OPERATIONS
# =============================================================================

def create_spreadsheet(title: str, sheets: list = None):
    """
    Create a new spreadsheet.

    Args:
        title: Spreadsheet title
        sheets: Optional list of sheet names to create

    Returns:
        New spreadsheet info with ID and URL
    """
    service = get_service()

    body = {"properties": {"title": title}}

    if sheets:
        body["sheets"] = [
            {"properties": {"title": name}}
            for name in sheets
        ]

    result = service.spreadsheets().create(body=body).execute()

    return {
        "spreadsheet_id": result["spreadsheetId"],
        "title": result["properties"]["title"],
        "url": result["spreadsheetUrl"],
        "sheets": [s["properties"]["title"] for s in result.get("sheets", [])]
    }

def add_sheet(spreadsheet_id: str, sheet_name: str):
    """Add a new sheet to an existing spreadsheet."""
    service = get_service()

    body = {
        "requests": [{
            "addSheet": {
                "properties": {"title": sheet_name}
            }
        }]
    }

    result = service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body=body
    ).execute()

    reply = result["replies"][0]["addSheet"]
    return {
        "sheet_id": reply["properties"]["sheetId"],
        "title": reply["properties"]["title"]
    }

def delete_sheet(spreadsheet_id: str, sheet_id: int):
    """Delete a sheet by its ID (not name)."""
    service = get_service()

    body = {
        "requests": [{
            "deleteSheet": {"sheetId": sheet_id}
        }]
    }

    service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body=body
    ).execute()

    return {"deleted_sheet_id": sheet_id}

# =============================================================================
# FORMAT OPERATIONS
# =============================================================================

def format_range(spreadsheet_id: str, sheet_id: int, start_row: int, end_row: int,
                 start_col: int, end_col: int, format_type: str, format_value: dict = None):
    """
    Apply formatting to a range.

    Args:
        spreadsheet_id: The spreadsheet ID
        sheet_id: The sheet ID (numeric, not name)
        start_row, end_row: Row range (0-indexed)
        start_col, end_col: Column range (0-indexed)
        format_type: Type of format (bold, italic, background, number, etc.)
        format_value: Format-specific values

    Supported format_types:
        - bold: Make text bold
        - italic: Make text italic
        - background: Set background color (format_value: {"red": 1, "green": 0.9, "blue": 0.8})
        - number: Set number format (format_value: {"type": "CURRENCY", "pattern": "$#,##0.00"})
        - align: Set alignment (format_value: {"horizontal": "CENTER", "vertical": "MIDDLE"})
    """
    service = get_service()

    cell_format = {}
    fields = ""

    if format_type == "bold":
        cell_format = {"textFormat": {"bold": True}}
        fields = "userEnteredFormat.textFormat.bold"
    elif format_type == "italic":
        cell_format = {"textFormat": {"italic": True}}
        fields = "userEnteredFormat.textFormat.italic"
    elif format_type == "background":
        cell_format = {"backgroundColor": format_value or {"red": 1, "green": 1, "blue": 0}}
        fields = "userEnteredFormat.backgroundColor"
    elif format_type == "number":
        cell_format = {"numberFormat": format_value or {"type": "NUMBER", "pattern": "#,##0.00"}}
        fields = "userEnteredFormat.numberFormat"
    elif format_type == "align":
        cell_format = {
            "horizontalAlignment": format_value.get("horizontal", "LEFT"),
            "verticalAlignment": format_value.get("vertical", "MIDDLE")
        }
        fields = "userEnteredFormat.horizontalAlignment,userEnteredFormat.verticalAlignment"

    body = {
        "requests": [{
            "repeatCell": {
                "range": {
                    "sheetId": sheet_id,
                    "startRowIndex": start_row,
                    "endRowIndex": end_row,
                    "startColumnIndex": start_col,
                    "endColumnIndex": end_col
                },
                "cell": {"userEnteredFormat": cell_format},
                "fields": fields
            }
        }]
    }

    service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body=body
    ).execute()

    return {"formatted": f"Rows {start_row}-{end_row}, Cols {start_col}-{end_col}"}

def auto_resize_columns(spreadsheet_id: str, sheet_id: int, start_col: int = 0, end_col: int = None):
    """Auto-resize columns to fit content."""
    service = get_service()

    dimension_range = {
        "sheetId": sheet_id,
        "dimension": "COLUMNS",
        "startIndex": start_col
    }
    if end_col:
        dimension_range["endIndex"] = end_col

    body = {
        "requests": [{
            "autoResizeDimensions": {
                "dimensions": dimension_range
            }
        }]
    }

    service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body=body
    ).execute()

    return {"resized": "columns"}

# =============================================================================
# LIST OPERATIONS
# =============================================================================

def list_spreadsheets(query: str = None, limit: int = 10):
    """
    List spreadsheets accessible to the user.

    Args:
        query: Optional search query
        limit: Max results to return
    """
    service = get_drive_service()

    q = "mimeType='application/vnd.google-apps.spreadsheet'"
    if query:
        q += f" and name contains '{query}'"

    result = service.files().list(
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

    parser = argparse.ArgumentParser(description="Google Sheets Operations")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Read
    read_parser = subparsers.add_parser("read", help="Read data from a range")
    read_parser.add_argument("spreadsheet_id", help="Spreadsheet ID")
    read_parser.add_argument("range", help="A1 notation range (e.g., Sheet1!A1:D10)")
    read_parser.add_argument("--json", action="store_true", help="Output as JSON")

    # Write
    write_parser = subparsers.add_parser("write", help="Write data to a range")
    write_parser.add_argument("spreadsheet_id", help="Spreadsheet ID")
    write_parser.add_argument("range", help="A1 notation range")
    write_parser.add_argument("--values", required=True, help="JSON array of values")
    write_parser.add_argument("--json", action="store_true", help="Output as JSON")

    # Append
    append_parser = subparsers.add_parser("append", help="Append rows to a sheet")
    append_parser.add_argument("spreadsheet_id", help="Spreadsheet ID")
    append_parser.add_argument("range", help="A1 notation range (e.g., Sheet1!A:D)")
    append_parser.add_argument("--values", required=True, help="JSON array of rows")
    append_parser.add_argument("--json", action="store_true", help="Output as JSON")

    # Clear
    clear_parser = subparsers.add_parser("clear", help="Clear a range")
    clear_parser.add_argument("spreadsheet_id", help="Spreadsheet ID")
    clear_parser.add_argument("range", help="A1 notation range")

    # Info
    info_parser = subparsers.add_parser("info", help="Get spreadsheet info")
    info_parser.add_argument("spreadsheet_id", help="Spreadsheet ID")
    info_parser.add_argument("--json", action="store_true", help="Output as JSON")

    # Create
    create_parser = subparsers.add_parser("create", help="Create new spreadsheet")
    create_parser.add_argument("title", help="Spreadsheet title")
    create_parser.add_argument("--sheets", nargs="+", help="Sheet names to create")
    create_parser.add_argument("--json", action="store_true", help="Output as JSON")

    # List
    list_parser = subparsers.add_parser("list", help="List spreadsheets")
    list_parser.add_argument("--query", help="Search query")
    list_parser.add_argument("--limit", type=int, default=10, help="Max results")
    list_parser.add_argument("--json", action="store_true", help="Output as JSON")

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
            result = read_range(args.spreadsheet_id, args.range)
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                for i, row in enumerate(result):
                    print(f"{i+1}: {row}")

        elif args.command == "write":
            values = json.loads(args.values)
            result = write_range(args.spreadsheet_id, args.range, values)
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                print(f"✅ Updated {result['updated_cells']} cells in {result['updated_range']}")

        elif args.command == "append":
            values = json.loads(args.values)
            result = append_rows(args.spreadsheet_id, args.range, values)
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                print(f"✅ Appended {result['updated_rows']} rows")

        elif args.command == "clear":
            result = clear_range(args.spreadsheet_id, args.range)
            print(f"✅ Cleared {result['cleared']}")

        elif args.command == "info":
            result = get_spreadsheet_info(args.spreadsheet_id)
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                print(f"Title: {result['title']}")
                print(f"ID: {result['spreadsheet_id']}")
                print("Sheets:")
                for sheet in result['sheets']:
                    print(f"  - {sheet['name']} (ID: {sheet['id']})")

        elif args.command == "create":
            result = create_spreadsheet(args.title, args.sheets)
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                print(f"✅ Created: {result['title']}")
                print(f"ID: {result['spreadsheet_id']}")
                print(f"URL: {result['url']}")

        elif args.command == "list":
            result = list_spreadsheets(args.query, args.limit)
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                for item in result:
                    print(f"• {item['name']}")
                    print(f"  ID: {item['id']}")

    except Exception as e:
        print(f"[ERROR] {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
