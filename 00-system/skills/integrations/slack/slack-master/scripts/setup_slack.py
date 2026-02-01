#!/usr/bin/env python3
"""
Slack OAuth Setup Wizard

Interactive setup for Slack User OAuth integration.
Guides user through authorization and saves token to .env.

Usage:
    python setup_slack.py

This script:
1. Checks for existing Slack app credentials
2. Starts a local server to receive OAuth callback
3. Opens browser for user authorization
4. Exchanges code for user token
5. Saves token to .env file
"""

import os
import sys
import json
import ssl
import webbrowser
import http.server
import socketserver
import urllib.parse
import tempfile
import subprocess
from pathlib import Path
from threading import Thread

# Find project root by looking for CLAUDE.md
SCRIPT_DIR = Path(__file__).parent

def find_project_root():
    """Find Nexus project root by looking for CLAUDE.md"""
    current = SCRIPT_DIR
    for _ in range(10):  # Max 10 levels up
        if (current / 'CLAUDE.md').exists():
            return current
        if (current / '.env').exists():
            return current
        parent = current.parent
        if parent == current:  # Reached filesystem root
            break
        current = parent
    # Fallback: use current working directory if it has .env
    cwd = Path.cwd()
    if (cwd / '.env').exists():
        return cwd
    if (cwd / 'CLAUDE.md').exists():
        return cwd
    # Last resort: assume script is in standard location
    return SCRIPT_DIR.parent.parent.parent.parent.parent

PROJECT_ROOT = find_project_root()
ENV_FILE = PROJECT_ROOT / ".env"

# OAuth configuration
OAUTH_AUTHORIZE_URL = "https://slack.com/oauth/v2/authorize"
OAUTH_TOKEN_URL = "https://slack.com/api/oauth.v2.access"
REDIRECT_PORT = 8765
REDIRECT_URI = f"https://localhost:{REDIRECT_PORT}/callback"

# Default scopes for User OAuth
DEFAULT_USER_SCOPES = [
    "channels:read",
    "channels:write",
    "channels:history",
    "groups:read",
    "groups:write",
    "groups:history",
    "im:read",
    "im:write",
    "im:history",
    "mpim:read",
    "mpim:write",
    "mpim:history",
    "chat:write",
    "users:read",
    "users:read.email",
    "files:read",
    "files:write",
    "reactions:read",
    "reactions:write",
    "pins:read",
    "pins:write",
    "search:read",
    "reminders:read",
    "reminders:write",
    "team:read"
]


def load_env_file():
    """Load environment variables from .env file"""
    env_vars = {}
    if ENV_FILE.exists():
        with open(ENV_FILE, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, _, value = line.partition('=')
                    env_vars[key.strip()] = value.strip().strip('"\'')
    return env_vars


def save_to_env(key, value):
    """Save or update a key in .env file"""
    lines = []
    key_found = False

    if ENV_FILE.exists():
        with open(ENV_FILE, 'r') as f:
            for line in f:
                if line.strip().startswith(f"{key}="):
                    lines.append(f"{key}={value}\n")
                    key_found = True
                else:
                    lines.append(line)

    if not key_found:
        if lines and not lines[-1].endswith('\n'):
            lines.append('\n')
        lines.append(f"{key}={value}\n")

    with open(ENV_FILE, 'w') as f:
        f.writelines(lines)


class OAuthCallbackHandler(http.server.BaseHTTPRequestHandler):
    """Handler for OAuth callback"""

    auth_code = None
    error = None

    def do_GET(self):
        """Handle GET request (OAuth callback)"""
        parsed = urllib.parse.urlparse(self.path)

        if parsed.path == '/callback':
            query = urllib.parse.parse_qs(parsed.query)

            if 'code' in query:
                OAuthCallbackHandler.auth_code = query['code'][0]
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"""
                    <html>
                    <head><title>Slack Authorization</title></head>
                    <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                                 display: flex; justify-content: center; align-items: center; height: 100vh;
                                 margin: 0; background: #f4f4f4;">
                        <div style="text-align: center; padding: 40px; background: white; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                            <h1 style="color: #4CAF50;">Authorization Successful!</h1>
                            <p style="color: #666;">You can close this window and return to the terminal.</p>
                        </div>
                    </body>
                    </html>
                """)
            elif 'error' in query:
                OAuthCallbackHandler.error = query.get('error_description', query['error'])[0]
                self.send_response(400)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                error_msg = OAuthCallbackHandler.error
                self.wfile.write(f"""
                    <html>
                    <head><title>Authorization Failed</title></head>
                    <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                                 display: flex; justify-content: center; align-items: center; height: 100vh;
                                 margin: 0; background: #f4f4f4;">
                        <div style="text-align: center; padding: 40px; background: white; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                            <h1 style="color: #f44336;">Authorization Failed</h1>
                            <p style="color: #666;">{error_msg}</p>
                            <p style="color: #666;">Please try again from the terminal.</p>
                        </div>
                    </body>
                    </html>
                """.encode())
            else:
                self.send_response(400)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        """Suppress logging"""
        pass


def create_self_signed_cert():
    """Create a self-signed certificate for localhost HTTPS"""
    cert_dir = tempfile.mkdtemp()
    cert_file = os.path.join(cert_dir, 'cert.pem')
    key_file = os.path.join(cert_dir, 'key.pem')

    # Generate self-signed certificate using openssl
    subprocess.run([
        'openssl', 'req', '-x509', '-newkey', 'rsa:2048',
        '-keyout', key_file, '-out', cert_file,
        '-days', '1', '-nodes',
        '-subj', '/CN=localhost'
    ], capture_output=True, check=True)

    return cert_file, key_file


def exchange_code_for_token(code, client_id, client_secret):
    """Exchange authorization code for user token"""
    import requests

    response = requests.post(
        OAUTH_TOKEN_URL,
        data={
            'client_id': client_id,
            'client_secret': client_secret,
            'code': code,
            'redirect_uri': REDIRECT_URI
        },
        timeout=30
    )

    data = response.json()

    if not data.get('ok'):
        raise Exception(f"Token exchange failed: {data.get('error', 'Unknown error')}")

    return data


def test_token(token):
    """Test that token works"""
    import requests

    response = requests.post(
        "https://slack.com/api/auth.test",
        headers={
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        },
        timeout=10
    )

    data = response.json()
    if not data.get('ok'):
        raise Exception(f"Token test failed: {data.get('error', 'Unknown error')}")

    return data


def print_banner():
    """Print setup banner"""
    print("\n" + "=" * 60)
    print("  Slack User OAuth Setup Wizard")
    print("=" * 60)
    print("\nThis will guide you through authorizing Slack access.")
    print("Your token will be saved to .env for future use.\n")


def main():
    print_banner()

    # Load existing config
    env_vars = load_env_file()
    client_id = env_vars.get('SLACK_CLIENT_ID', '') or os.getenv('SLACK_CLIENT_ID', '')
    client_secret = env_vars.get('SLACK_CLIENT_SECRET', '') or os.getenv('SLACK_CLIENT_SECRET', '')

    # Check for client credentials
    if not client_id or not client_secret:
        print("=" * 60)
        print("STEP 1: Create a Slack App")
        print("=" * 60)
        print("""
To use Slack with Nexus, you need to create a Slack App:

1. Go to: https://api.slack.com/apps
2. Click 'Create New App' -> 'From scratch'
3. Name it (e.g., 'Nexus Integration')
4. Select your workspace

After creating the app:

5. Go to 'OAuth & Permissions'
6. Under 'Redirect URLs', add:
   https://localhost:8765/callback

7. Under 'User Token Scopes', add these scopes:
   - channels:read, channels:write, channels:history
   - groups:read, groups:write, groups:history
   - im:read, im:write, im:history
   - chat:write
   - users:read
   - files:read, files:write
   - search:read
   - reactions:read, reactions:write
   - pins:read, pins:write
   - reminders:read, reminders:write

8. Go to 'Basic Information' and copy:
   - Client ID
   - Client Secret
""")

        client_id = input("Enter your Client ID: ").strip()
        if not client_id:
            print("Error: Client ID is required")
            sys.exit(1)

        client_secret = input("Enter your Client Secret: ").strip()
        if not client_secret:
            print("Error: Client Secret is required")
            sys.exit(1)

        # Save credentials
        save_to_env('SLACK_CLIENT_ID', client_id)
        save_to_env('SLACK_CLIENT_SECRET', client_secret)
        print("\n[OK] Credentials saved to .env")

    print("\n" + "=" * 60)
    print("STEP 2: Authorize Your Account")
    print("=" * 60)

    # Build authorization URL
    scopes = ",".join(DEFAULT_USER_SCOPES)
    auth_params = urllib.parse.urlencode({
        'client_id': client_id,
        'user_scope': scopes,  # Note: user_scope for user tokens
        'redirect_uri': REDIRECT_URI
    })
    auth_url = f"{OAUTH_AUTHORIZE_URL}?{auth_params}"

    print(f"\nStarting local HTTPS server on port {REDIRECT_PORT}...")
    print("(Generating self-signed certificate for localhost...)")

    # Create self-signed certificate
    try:
        cert_file, key_file = create_self_signed_cert()
    except Exception as e:
        print(f"\n[X] Failed to create SSL certificate: {e}")
        print("Make sure 'openssl' is installed on your system.")
        sys.exit(1)

    # Start local server with SSL
    OAuthCallbackHandler.auth_code = None
    OAuthCallbackHandler.error = None

    with socketserver.TCPServer(("", REDIRECT_PORT), OAuthCallbackHandler) as httpd:
        # Wrap socket with SSL
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ssl_context.load_cert_chain(cert_file, key_file)
        httpd.socket = ssl_context.wrap_socket(httpd.socket, server_side=True)
        httpd.timeout = 120  # 2 minute timeout

        print("\nOpening browser for authorization...")
        print(f"\nIf browser doesn't open, visit this URL:\n{auth_url}\n")
        print("NOTE: Your browser may warn about the self-signed certificate.")
        print("      Click 'Advanced' and 'Proceed to localhost' to continue.\n")

        webbrowser.open(auth_url)

        print("Waiting for authorization (timeout: 2 minutes)...")

        # Handle requests until we get auth code or error (or timeout)
        # Need to handle multiple requests because browser may make preflight/favicon requests
        import time
        start_time = time.time()
        while time.time() - start_time < 120:  # 2 minute timeout
            httpd.handle_request()
            if OAuthCallbackHandler.auth_code or OAuthCallbackHandler.error:
                break

    # Clean up temp cert files
    try:
        os.remove(cert_file)
        os.remove(key_file)
        os.rmdir(os.path.dirname(cert_file))
    except:
        pass

    if OAuthCallbackHandler.error:
        print(f"\n[X] Authorization failed: {OAuthCallbackHandler.error}")
        sys.exit(1)

    if not OAuthCallbackHandler.auth_code:
        print("\n[X] No authorization code received (timeout or cancelled)")
        sys.exit(1)

    print("\n[OK] Authorization code received")

    print("\n" + "=" * 60)
    print("STEP 3: Exchanging Code for Token")
    print("=" * 60)

    try:
        token_data = exchange_code_for_token(
            OAuthCallbackHandler.auth_code,
            client_id,
            client_secret
        )
    except Exception as e:
        print(f"\n[X] Token exchange failed: {e}")
        sys.exit(1)

    # Extract user token
    authed_user = token_data.get('authed_user', {})
    user_token = authed_user.get('access_token')

    if not user_token:
        print("\n[X] No user token in response")
        print(f"Response: {json.dumps(token_data, indent=2)}")
        sys.exit(1)

    # Save token
    save_to_env('SLACK_USER_TOKEN', user_token)
    print("\n[OK] User token saved to .env")

    print("\n" + "=" * 60)
    print("STEP 4: Testing Connection")
    print("=" * 60)

    try:
        test_result = test_token(user_token)
        print(f"\n[OK] Connection successful!")
        print(f"    User: {test_result.get('user')}")
        print(f"    Team: {test_result.get('team')}")
        print(f"    User ID: {test_result.get('user_id')}")
    except Exception as e:
        print(f"\n[X] Token test failed: {e}")
        sys.exit(1)

    print("\n" + "=" * 60)
    print("  Setup Complete!")
    print("=" * 60)
    print("""
Your Slack integration is now configured!

You can now use Slack skills like:
  - 'send slack message' - Send messages to channels
  - 'list slack channels' - See available channels
  - 'search slack' - Search messages and files

Your credentials are saved in .env:
  - SLACK_CLIENT_ID
  - SLACK_CLIENT_SECRET
  - SLACK_USER_TOKEN (xoxp-...)
""")


if __name__ == "__main__":
    try:
        import requests
    except ImportError:
        print("Error: 'requests' library required. Install with: pip install requests")
        sys.exit(1)

    main()
