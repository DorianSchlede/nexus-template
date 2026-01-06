#!/usr/bin/env python3
"""
Download Context File

GET /agent/{agentId}/context/file/{fileId}/download

Usage:
    python download_context_file.py --agent-id AGENT --file-id FILE
    python download_context_file.py --agent-id AGENT --file-id FILE --output output.pdf
"""

import sys
import json
import argparse
from beam_client import get_client, BASE_URL


def main():
    parser = argparse.ArgumentParser(description='Download agent context file')
    parser.add_argument('--agent-id', required=True, help='Agent ID')
    parser.add_argument('--file-id', required=True, help='File ID')
    parser.add_argument('--output', help='Output file path')
    parser.add_argument('--json', action='store_true', help='Output metadata as JSON')
    args = parser.parse_args()

    try:
        import requests
        client = get_client()
        headers = client.get_headers()

        url = f"{BASE_URL}/agent/{args.agent_id}/context/file/{args.file_id}/download"
        response = requests.get(url, headers=headers, timeout=120)

        if response.status_code != 200:
            raise Exception(f"Download failed: {response.status_code}")

        # Get filename from headers or use default
        content_disp = response.headers.get('Content-Disposition', '')
        if 'filename=' in content_disp:
            filename = content_disp.split('filename=')[1].strip('"')
        else:
            filename = f"{args.file_id}.bin"

        output_path = args.output or filename

        with open(output_path, 'wb') as f:
            f.write(response.content)

        if args.json:
            print(json.dumps({
                "status": "success",
                "file": output_path,
                "size": len(response.content)
            }, indent=2))
        else:
            print(f"Downloaded: {output_path} ({len(response.content)} bytes)")

    except Exception as e:
        if args.json:
            print(json.dumps({"error": str(e)}))
        else:
            print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
