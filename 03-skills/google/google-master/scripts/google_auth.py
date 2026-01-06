#!/usr/bin/env python3
"""
Google Unified OAuth Authentication

Handles OAuth 2.0 flow for ALL Google APIs (Gmail, Docs, Sheets, Calendar).
Single authentication grants access to all Google services.

Token stored in: 01-memory/integrations/google-token.json
Credentials from: .env (GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET) or google-credentials.json
"""

import os
import sys
import json
import argparse
from pathlib import Path

# Find Nexus root (look for CLAUDE.md)
def find_nexus_root():
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / "CLAUDE.md").exists():
            return parent
    return Path.cwd()

NEXUS_ROOT = find_nexus_root()
TOKEN_PATH = NEXUS_ROOT / "01-memory" / "integrations" / "google-token.json"
CREDENTIALS_PATH = NEXUS_ROOT / "google-credentials.json"

def load_env():
    """Load .env file into environment variables."""
    env_path = NEXUS_ROOT / ".env"
    if env_path.exists():
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ.setdefault(key.strip(), value.strip())

# Load .env on import
load_env()

def get_credentials_config():
    """
    Get Google OAuth credentials from .env or JSON file.
    Priority: .env > google-credentials.json
    Returns dict in the format expected by google-auth library.
    """
    client_id = os.environ.get('GOOGLE_CLIENT_ID')
    client_secret = os.environ.get('GOOGLE_CLIENT_SECRET')
    project_id = os.environ.get('GOOGLE_PROJECT_ID', 'nexus')

    if client_id and client_secret:
        # Build credentials dict from .env
        return {
            "installed": {
                "client_id": client_id,
                "project_id": project_id,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_secret": client_secret,
                "redirect_uris": ["http://localhost"]
            }
        }
    elif CREDENTIALS_PATH.exists():
        # Fall back to JSON file
        with open(CREDENTIALS_PATH, 'r') as f:
            return json.load(f)
    else:
        return None

# All scopes for all Google services
SCOPES = {
    'gmail': [
        'https://www.googleapis.com/auth/gmail.readonly',
        'https://www.googleapis.com/auth/gmail.send',
        'https://www.googleapis.com/auth/gmail.compose',
        'https://www.googleapis.com/auth/gmail.modify',
        'https://www.googleapis.com/auth/gmail.labels'
    ],
    'docs': [
        'https://www.googleapis.com/auth/documents',
        'https://www.googleapis.com/auth/drive'
    ],
    'sheets': [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive.readonly'
    ],
    'calendar': [
        'https://www.googleapis.com/auth/calendar',
        'https://www.googleapis.com/auth/calendar.events'
    ],
    'drive': [
        'https://www.googleapis.com/auth/drive',
        'https://www.googleapis.com/auth/drive.file',
        'https://www.googleapis.com/auth/drive.metadata.readonly'
    ],
    'tasks': [
        'https://www.googleapis.com/auth/tasks',
        'https://www.googleapis.com/auth/tasks.readonly'
    ],
    'slides': [
        'https://www.googleapis.com/auth/presentations',
        'https://www.googleapis.com/auth/drive.file'
    ]
}

# Service API versions
SERVICE_VERSIONS = {
    'gmail': ('gmail', 'v1'),
    'docs': ('docs', 'v1'),
    'sheets': ('sheets', 'v4'),
    'calendar': ('calendar', 'v3'),
    'drive': ('drive', 'v3'),
    'tasks': ('tasks', 'v1'),
    'slides': ('slides', 'v1')
}

def get_all_scopes():
    """Get all scopes combined (deduplicated)."""
    all_scopes = []
    for service_scopes in SCOPES.values():
        for scope in service_scopes:
            if scope not in all_scopes:
                all_scopes.append(scope)
    return all_scopes

def get_scopes_for_service(service):
    """Get scopes for a specific service or all."""
    if service == 'all' or service is None:
        return get_all_scopes()
    return SCOPES.get(service, get_all_scopes())

def check_dependencies():
    """Check if required packages are installed."""
    try:
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
        from googleapiclient.discovery import build
        return True
    except ImportError:
        return False

def get_credentials(scopes=None):
    """
    Get valid credentials, refreshing or initiating OAuth flow as needed.

    Args:
        scopes: List of scopes to request. If None, requests all scopes.

    Returns:
        Credentials object or None if failed
    """
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request

    if scopes is None:
        scopes = get_all_scopes()

    creds = None

    # Load existing token
    if TOKEN_PATH.exists():
        try:
            creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), scopes)
        except Exception as e:
            print(f"[WARN] Could not load existing token: {e}")
            creds = None

    # Refresh or get new credentials
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"[WARN] Token refresh failed: {e}")
                creds = None

        if not creds:
            credentials_config = get_credentials_config()
            if not credentials_config:
                print("[ERROR] OAuth credentials not found")
                print("\nTo set up Google authentication, add to .env:")
                print("  GOOGLE_CLIENT_ID=your-client-id")
                print("  GOOGLE_CLIENT_SECRET=your-client-secret")
                print("  GOOGLE_PROJECT_ID=your-project-id")
                print("\nOr save credentials JSON to:")
                print(f"  {CREDENTIALS_PATH}")
                return None

            flow = InstalledAppFlow.from_client_config(credentials_config, scopes)
            creds = flow.run_local_server(port=0)

        # Save token
        TOKEN_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(TOKEN_PATH, 'w') as f:
            f.write(creds.to_json())
        print(f"[OK] Token saved to: {TOKEN_PATH}")

    return creds

def get_service(service_name, version=None):
    """
    Get an authenticated Google API service.

    Args:
        service_name: 'gmail', 'docs', 'sheets', 'calendar', or 'drive'
        version: API version (optional, uses default if not specified)

    Returns:
        Authenticated service object

    Example:
        gmail = get_service('gmail')
        docs = get_service('docs')
        sheets = get_service('sheets')
        calendar = get_service('calendar')
    """
    from googleapiclient.discovery import build

    creds = get_credentials()
    if not creds:
        raise RuntimeError("Failed to get credentials. Run: python google_auth.py --login")

    # Get service name and version
    if service_name in SERVICE_VERSIONS:
        api_name, default_version = SERVICE_VERSIONS[service_name]
        version = version or default_version
    else:
        api_name = service_name
        version = version or 'v1'

    return build(api_name, version, credentials=creds)

def check_config(service=None, json_output=False):
    """Check authentication configuration status."""
    scopes = get_scopes_for_service(service)
    credentials_config = get_credentials_config()
    has_credentials = credentials_config is not None

    # Check source of credentials
    has_env_creds = bool(os.environ.get('GOOGLE_CLIENT_ID') and os.environ.get('GOOGLE_CLIENT_SECRET'))
    credentials_source = ".env" if has_env_creds else ("JSON file" if CREDENTIALS_PATH.exists() else "none")

    status = {
        "service": service or "all",
        "credentials_configured": has_credentials,
        "credentials_source": credentials_source,
        "token_file": TOKEN_PATH.exists(),
        "token_path": str(TOKEN_PATH),
        "dependencies_installed": check_dependencies(),
        "ready": False,
        "scopes_requested": scopes
    }

    if not status["dependencies_installed"]:
        status["error"] = "Missing dependencies"
        status["ai_action"] = "install_dependencies"
        status["fix"] = "pip install google-auth google-auth-oauthlib google-api-python-client"
        status["exit_code"] = 2
    elif not has_credentials:
        status["error"] = "OAuth credentials not found"
        status["ai_action"] = "need_credentials"
        status["fix"] = "Add GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET to .env"
        status["exit_code"] = 2
    elif not status["token_file"]:
        status["message"] = "Credentials found but not authenticated yet"
        status["ai_action"] = "need_login"
        status["fix"] = "python google_auth.py --login"
        status["exit_code"] = 1
    else:
        # Try to load and validate token
        try:
            creds = get_credentials(scopes)
            if creds and creds.valid:
                status["ready"] = True
                status["ai_action"] = "proceed"
                status["message"] = "Authenticated and ready"
                status["exit_code"] = 0
            else:
                status["message"] = "Token exists but needs refresh"
                status["ai_action"] = "need_login"
                status["fix"] = "python google_auth.py --login"
                status["exit_code"] = 1
        except Exception as e:
            status["error"] = str(e)
            status["ai_action"] = "need_login"
            status["exit_code"] = 2

    if json_output:
        print(json.dumps(status, indent=2))
    else:
        service_name = service.upper() if service else "ALL GOOGLE SERVICES"
        print("=" * 60)
        print(f"GOOGLE AUTHENTICATION CHECK ({service_name})")
        print("=" * 60)
        print(f"Credentials: {'OK' if has_credentials else 'MISSING'} (source: {credentials_source})")
        print(f"Token: {'OK' if status['token_file'] else 'MISSING'}")
        print(f"  Path: {TOKEN_PATH}")
        print(f"Dependencies: {'OK' if status['dependencies_installed'] else 'MISSING'}")
        print()
        if status.get("ready"):
            print("READY - All Google services available")
        elif status.get("error"):
            print(f"ERROR: {status['error']}")
            if status.get("fix"):
                print(f"FIX: {status['fix']}")
        else:
            print(f"STATUS: {status.get('message', 'Setup incomplete')}")
            if status.get("fix"):
                print(f"FIX: {status['fix']}")
        print("=" * 60)

    sys.exit(status.get("exit_code", 1))

def login(service=None):
    """Initiate OAuth login flow."""
    if not check_dependencies():
        print("[ERROR] Missing dependencies. Run:")
        print("  pip install google-auth google-auth-oauthlib google-api-python-client")
        sys.exit(2)

    credentials_config = get_credentials_config()
    if not credentials_config:
        print("[ERROR] OAuth credentials not found")
        print("\nTo set up, add to .env:")
        print("  GOOGLE_CLIENT_ID=your-client-id")
        print("  GOOGLE_CLIENT_SECRET=your-client-secret")
        print("  GOOGLE_PROJECT_ID=your-project-id")
        print("\nOr download JSON from Google Cloud Console and save as:")
        print(f"  {CREDENTIALS_PATH}")
        sys.exit(2)

    scopes = get_scopes_for_service(service)

    print("[INFO] Starting OAuth flow for Google services...")
    print("[INFO] A browser window will open for authentication.")
    print("[INFO] You'll grant access to: Gmail, Docs, Sheets, Calendar, Drive, Tasks, Slides")
    print()

    # Remove existing token to force new auth
    if TOKEN_PATH.exists():
        TOKEN_PATH.unlink()

    creds = get_credentials(scopes)

    if creds and creds.valid:
        print("\nSuccessfully authenticated!")
        print(f"Token saved to: {TOKEN_PATH}")
        print("\nYou can now use all Google skills:")
        print("  - Gmail (email)")
        print("  - Google Docs")
        print("  - Google Sheets")
        print("  - Google Calendar")
        print("  - Google Drive")
        print("  - Google Tasks")
        print("  - Google Slides")
    else:
        print("\nAuthentication failed")
        sys.exit(1)

def logout():
    """Remove stored token."""
    if TOKEN_PATH.exists():
        TOKEN_PATH.unlink()
        print(f"[OK] Removed token: {TOKEN_PATH}")
        print("[INFO] You'll need to re-authenticate to use Google services")
    else:
        print("[INFO] No token found")

def status():
    """Show detailed authentication status."""
    print("=" * 60)
    print("GOOGLE AUTHENTICATION STATUS")
    print("=" * 60)
    print()
    print(f"Nexus Root: {NEXUS_ROOT}")
    print()
    print("FILES:")
    print(f"  Credentials: {CREDENTIALS_PATH}")
    print(f"    Exists: {'Yes' if CREDENTIALS_PATH.exists() else 'No'}")
    print(f"  Token: {TOKEN_PATH}")
    print(f"    Exists: {'Yes' if TOKEN_PATH.exists() else 'No'}")
    print()
    print("DEPENDENCIES:")
    deps_ok = check_dependencies()
    print(f"  google-auth: {'OK' if deps_ok else 'Missing'}")
    print(f"  google-auth-oauthlib: {'OK' if deps_ok else 'Missing'}")
    print(f"  google-api-python-client: {'OK' if deps_ok else 'Missing'}")
    print()
    print("SERVICES & SCOPES:")
    for service, scopes in SCOPES.items():
        print(f"  {service}:")
        for scope in scopes:
            scope_name = scope.split('/')[-1]
            print(f"    - {scope_name}")
    print()

    if TOKEN_PATH.exists() and deps_ok:
        try:
            creds = get_credentials()
            if creds and creds.valid:
                print("STATUS: Authenticated and ready")
            else:
                print("STATUS: Token needs refresh - run: python google_auth.py --login")
        except Exception as e:
            print(f"STATUS: Error - {e}")
    elif not CREDENTIALS_PATH.exists():
        print("STATUS: Need OAuth credentials from Google Cloud Console")
    elif not deps_ok:
        print("STATUS: Install dependencies first")
    else:
        print("STATUS: Need to authenticate - run: python google_auth.py --login")

    print("=" * 60)

def main():
    parser = argparse.ArgumentParser(
        description="Google Unified OAuth Authentication",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python google_auth.py --check              # Check if ready
  python google_auth.py --check --json       # Check with JSON output
  python google_auth.py --login              # Authenticate (all services)
  python google_auth.py --login --service gmail  # Auth for Gmail only
  python google_auth.py --logout             # Remove token
  python google_auth.py --status             # Detailed status
        """
    )
    parser.add_argument("--check", action="store_true", help="Check configuration status")
    parser.add_argument("--login", action="store_true", help="Initiate OAuth login")
    parser.add_argument("--logout", action="store_true", help="Remove stored token")
    parser.add_argument("--status", action="store_true", help="Show detailed status")
    parser.add_argument("--service", choices=['gmail', 'docs', 'sheets', 'calendar', 'drive', 'tasks', 'slides', 'all'],
                       default='all', help="Specific service (default: all)")
    parser.add_argument("--json", action="store_true", help="Output as JSON (for --check)")

    args = parser.parse_args()

    if args.check:
        service = None if args.service == 'all' else args.service
        check_config(service=service, json_output=args.json)
    elif args.login:
        service = None if args.service == 'all' else args.service
        login(service=service)
    elif args.logout:
        logout()
    elif args.status:
        status()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
