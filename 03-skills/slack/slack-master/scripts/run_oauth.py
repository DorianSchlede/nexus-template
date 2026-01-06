#!/usr/bin/env python3
"""
Non-interactive OAuth flow for Slack.
Requires SLACK_CLIENT_ID and SLACK_CLIENT_SECRET in .env
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

SCRIPT_DIR = Path(__file__).parent

def find_project_root():
    current = SCRIPT_DIR
    for _ in range(10):
        if (current / 'CLAUDE.md').exists():
            return current
        if (current / '.env').exists():
            return current
        parent = current.parent
        if parent == current:
            break
        current = parent
    cwd = Path.cwd()
    if (cwd / '.env').exists():
        return cwd
    return SCRIPT_DIR.parent.parent.parent.parent.parent

PROJECT_ROOT = find_project_root()
ENV_FILE = PROJECT_ROOT / ".env"

OAUTH_AUTHORIZE_URL = "https://slack.com/oauth/v2/authorize"
OAUTH_TOKEN_URL = "https://slack.com/api/oauth.v2.access"
REDIRECT_PORT = 8765
REDIRECT_URI = f"https://localhost:{REDIRECT_PORT}/callback"

DEFAULT_USER_SCOPES = [
    "channels:read", "channels:write", "channels:history",
    "groups:read", "groups:write", "groups:history",
    "im:read", "im:write", "im:history",
    "mpim:read", "mpim:write", "mpim:history",
    "chat:write", "users:read", "users:read.email",
    "files:read", "files:write",
    "reactions:read", "reactions:write",
    "pins:read", "pins:write",
    "search:read",
    "reminders:read", "reminders:write",
    "team:read"
]

def load_env_file():
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
    auth_code = None
    error = None

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == '/callback':
            query = urllib.parse.parse_qs(parsed.query)
            if 'code' in query:
                OAuthCallbackHandler.auth_code = query['code'][0]
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"<html><body><h1>Success!</h1><p>You can close this window.</p></body></html>")
            elif 'error' in query:
                OAuthCallbackHandler.error = query.get('error_description', query['error'])[0]
                self.send_response(400)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(f"<html><body><h1>Error</h1><p>{OAuthCallbackHandler.error}</p></body></html>".encode())
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass

def create_self_signed_cert():
    cert_dir = tempfile.mkdtemp()
    cert_file = os.path.join(cert_dir, 'cert.pem')
    key_file = os.path.join(cert_dir, 'key.pem')
    subprocess.run([
        'openssl', 'req', '-x509', '-newkey', 'rsa:2048',
        '-keyout', key_file, '-out', cert_file,
        '-days', '1', '-nodes',
        '-subj', '/CN=localhost'
    ], capture_output=True, check=True)
    return cert_file, key_file

def exchange_code_for_token(code, client_id, client_secret):
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
    import requests
    response = requests.post(
        "https://slack.com/api/auth.test",
        headers={'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'},
        timeout=10
    )
    data = response.json()
    if not data.get('ok'):
        raise Exception(f"Token test failed: {data.get('error', 'Unknown error')}")
    return data

def main():
    import requests

    env_vars = load_env_file()
    client_id = env_vars.get('SLACK_CLIENT_ID', '')
    client_secret = env_vars.get('SLACK_CLIENT_SECRET', '')

    if not client_id or not client_secret:
        print(json.dumps({"error": "SLACK_CLIENT_ID and SLACK_CLIENT_SECRET required in .env"}))
        sys.exit(1)

    scopes = ",".join(DEFAULT_USER_SCOPES)
    auth_params = urllib.parse.urlencode({
        'client_id': client_id,
        'user_scope': scopes,
        'redirect_uri': REDIRECT_URI
    })
    auth_url = f"{OAUTH_AUTHORIZE_URL}?{auth_params}"

    print(f"Opening browser for Slack authorization...")
    print(f"\nURL: {auth_url}\n")
    print("NOTE: If you see a certificate warning, click 'Advanced' -> 'Proceed to localhost'")

    try:
        cert_file, key_file = create_self_signed_cert()
    except Exception as e:
        print(json.dumps({"error": f"Failed to create SSL certificate: {e}"}))
        sys.exit(1)

    OAuthCallbackHandler.auth_code = None
    OAuthCallbackHandler.error = None

    with socketserver.TCPServer(("", REDIRECT_PORT), OAuthCallbackHandler) as httpd:
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ssl_context.load_cert_chain(cert_file, key_file)
        httpd.socket = ssl_context.wrap_socket(httpd.socket, server_side=True)
        httpd.timeout = 120

        webbrowser.open(auth_url)
        print("Waiting for authorization (2 min timeout)...")

        import time
        start_time = time.time()
        while time.time() - start_time < 120:
            httpd.handle_request()
            if OAuthCallbackHandler.auth_code or OAuthCallbackHandler.error:
                break

    try:
        os.remove(cert_file)
        os.remove(key_file)
        os.rmdir(os.path.dirname(cert_file))
    except:
        pass

    if OAuthCallbackHandler.error:
        print(f"Authorization failed: {OAuthCallbackHandler.error}")
        sys.exit(1)

    if not OAuthCallbackHandler.auth_code:
        print("No authorization code received (timeout)")
        sys.exit(1)

    print("Authorization code received, exchanging for token...")

    try:
        token_data = exchange_code_for_token(OAuthCallbackHandler.auth_code, client_id, client_secret)
    except Exception as e:
        print(f"Token exchange failed: {e}")
        sys.exit(1)

    authed_user = token_data.get('authed_user', {})
    user_token = authed_user.get('access_token')

    if not user_token:
        print(f"No user token in response: {json.dumps(token_data, indent=2)}")
        sys.exit(1)

    save_to_env('SLACK_USER_TOKEN', user_token)
    print("Token saved to .env")

    try:
        test_result = test_token(user_token)
        print(f"\nSUCCESS! Connected as {test_result.get('user')} in {test_result.get('team')}")
    except Exception as e:
        print(f"Token test failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        import requests
    except ImportError:
        print("Error: 'requests' library required")
        sys.exit(1)
    main()
