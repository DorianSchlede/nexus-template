"""
Shared HTTP utilities for hook scripts.
Fire-and-forget pattern with timeout.
"""

import json
import urllib.request
import urllib.error
import sys
import os

SERVER_URL = os.environ.get("OBSERVABILITY_SERVER_URL", "http://localhost:7777")
TIMEOUT_SECONDS = 5


def send_to_server(endpoint: str, payload: dict) -> bool:
    """
    Send payload to observability server.

    Fire-and-forget: Returns True/False, never raises, never blocks long.

    Args:
        endpoint: API endpoint path (e.g., "/api/v2/sessions/{id}/start")
        payload: JSON-serializable dict to send

    Returns:
        True if request succeeded, False otherwise
    """
    try:
        url = f"{SERVER_URL}{endpoint}"

        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "User-Agent": "Claude-Hook/1.0"
            },
            method="POST"
        )

        with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS) as response:
            return response.status in (200, 201)

    except urllib.error.URLError as e:
        print(f"[hook] Server connection error: {e}", file=sys.stderr)
        return False
    except urllib.error.HTTPError as e:
        print(f"[hook] Server HTTP error: {e.code}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"[hook] Server error: {e}", file=sys.stderr)
        return False
