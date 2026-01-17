"""
Server health check and auto-start utilities.
"""

import subprocess
import time
import urllib.request
import urllib.error
import sys
import os
import shutil

SERVER_URL = os.environ.get("OBSERVABILITY_SERVER_URL", "http://localhost:7777")
STARTUP_TIMEOUT = 10


def check_server_health() -> bool:
    """Check if server is responding."""
    try:
        req = urllib.request.Request(f"{SERVER_URL}/health", method="GET")
        with urllib.request.urlopen(req, timeout=2) as response:
            return response.status == 200
    except Exception:
        return False


def start_server() -> bool:
    """
    Attempt to start server using available mechanisms.

    Tries in order:
    1. PM2 (if available)
    2. Bun (primary for claude-agent-tracer)
    3. npm start
    4. Direct node

    Returns:
        True if a start command was issued, False if all methods failed
    """
    # Default to the architech claude-agent-tracer location
    server_dir = os.environ.get(
        "OBSERVABILITY_SERVER_DIR",
        os.path.join(os.path.dirname(os.getcwd()), "architech", "claude-agent-tracer")
    )

    commands = []

    # PM2 (if available)
    if shutil.which("pm2"):
        commands.append(["pm2", "start", "observability-server", "--silent"])

    # Bun (primary for claude-agent-tracer)
    if shutil.which("bun"):
        entry = os.path.join(server_dir, "apps", "server", "src", "index.ts")
        if os.path.exists(entry):
            commands.append(["bun", "run", entry])

    # npm start
    if os.path.exists(os.path.join(server_dir, "package.json")):
        npm_cmd = "npm.cmd" if sys.platform == "win32" else "npm"
        commands.append([npm_cmd, "start", "--prefix", server_dir])

    # Direct node
    entry = os.path.join(server_dir, "dist", "index.js")
    if os.path.exists(entry) and shutil.which("node"):
        commands.append(["node", entry])

    for cmd in commands:
        try:
            # Use CREATE_NEW_PROCESS_GROUP on Windows, start_new_session on Unix
            kwargs = {
                "stdout": subprocess.DEVNULL,
                "stderr": subprocess.DEVNULL,
            }
            if sys.platform == "win32":
                kwargs["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP
            else:
                kwargs["start_new_session"] = True

            subprocess.Popen(cmd, **kwargs)
            return True
        except Exception:
            continue

    return False


def wait_for_ready(timeout: int = STARTUP_TIMEOUT) -> bool:
    """Wait for server to become healthy."""
    start = time.time()
    while time.time() - start < timeout:
        if check_server_health():
            return True
        time.sleep(0.5)
    return False


def ensure_server_running() -> bool:
    """
    Ensure server is running, starting if necessary.

    Returns:
        True if server is running, False if server is unavailable
    """
    if check_server_health():
        return True

    print("[hook] Starting observability server...", file=sys.stderr)
    if start_server() and wait_for_ready():
        print("[hook] Server ready", file=sys.stderr)
        return True

    print("[hook] Server unavailable - continuing without observability", file=sys.stderr)
    return False
