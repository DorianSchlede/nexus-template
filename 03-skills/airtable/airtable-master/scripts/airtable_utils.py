#!/usr/bin/env python3
"""
Airtable Shared Utilities

Shared functions for all Airtable scripts:
- Multi-token API key management
- Rate-limited request handling
- Context file management

Usage:
    from airtable_utils import get_api_key, get_headers, make_request_with_retry
"""

import os
import sys
import time
from pathlib import Path
from datetime import datetime

try:
    import requests
except ImportError:
    print("[ERROR] requests library not installed", file=sys.stderr)
    print("Install with: pip install requests", file=sys.stderr)
    sys.exit(1)

try:
    import yaml
except ImportError:
    print("[ERROR] PyYAML library not installed", file=sys.stderr)
    print("Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(1)


# Constants
API_BASE_URL = 'https://api.airtable.com/v0'


def find_nexus_root():
    """Find Nexus root directory (contains CLAUDE.md)"""
    current = Path(__file__).resolve().parent
    for path in [current] + list(current.parents):
        if (path / 'CLAUDE.md').exists():
            return path
    # Fallback to cwd
    current = Path.cwd()
    for path in [current] + list(current.parents):
        if (path / 'CLAUDE.md').exists():
            return path
    return None


def load_env(nexus_root=None):
    """Load .env file into environment variables."""
    if nexus_root is None:
        nexus_root = find_nexus_root()
    if nexus_root is None:
        return

    env_path = nexus_root / '.env' if isinstance(nexus_root, Path) else Path(nexus_root) / '.env'
    if not env_path.exists():
        return

    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip().strip('"').strip("'")


def get_api_key(token_name: str = None) -> str:
    """
    Get Airtable API key, supporting multiple tokens.

    Args:
        token_name: Optional token name suffix (e.g., "MUTAGENT" -> AIRTABLE_API_KEY_MUTAGENT)
                   If None, uses default AIRTABLE_API_KEY

    Returns:
        API key string

    Raises:
        ValueError: If API key not found

    Examples:
        get_api_key()           # Uses AIRTABLE_API_KEY
        get_api_key("MUTAGENT") # Uses AIRTABLE_API_KEY_MUTAGENT
    """
    # Ensure env is loaded
    load_env()

    if token_name:
        key_name = f"AIRTABLE_API_KEY_{token_name.upper()}"
    else:
        key_name = "AIRTABLE_API_KEY"

    api_key = os.environ.get(key_name)
    if not api_key:
        raise ValueError(f"{key_name} not set in .env")

    return api_key


def get_headers(token_name: str = None) -> dict:
    """
    Get API headers with optional token selection.

    Args:
        token_name: Optional token name for multi-workspace support

    Returns:
        Dict with Authorization and Content-Type headers
    """
    api_key = get_api_key(token_name)
    return {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }


def make_request_with_retry(method: str, url: str, headers: dict = None,
                            json_data: dict = None, max_retries: int = 3,
                            base_delay: float = 1.0, timeout: int = 30) -> requests.Response:
    """
    Make HTTP request with exponential backoff for rate limits.

    Args:
        method: HTTP method (GET, POST, PATCH, DELETE)
        url: Request URL
        headers: Request headers
        json_data: JSON body for POST/PATCH
        max_retries: Maximum retry attempts (default 3)
        base_delay: Initial delay in seconds (default 1.0)
        timeout: Request timeout in seconds (default 30)

    Returns:
        Response object

    Rate Limit Handling:
        - Retries on 429 (rate limited) with exponential backoff
        - Respects Retry-After header if present
        - Max delay capped at 60 seconds
    """
    last_response = None

    for attempt in range(max_retries + 1):
        try:
            response = requests.request(
                method,
                url,
                headers=headers,
                json=json_data,
                timeout=timeout
            )
            last_response = response

            if response.status_code == 429:
                # Rate limited
                retry_after = response.headers.get('Retry-After')
                if retry_after:
                    wait = min(60, int(retry_after))
                else:
                    wait = min(60, base_delay * (2 ** attempt))

                print(f"[WARN] Rate limited, waiting {wait:.1f}s (attempt {attempt + 1}/{max_retries + 1})", file=sys.stderr)
                time.sleep(wait)
                continue

            # Success or non-retryable error
            return response

        except requests.exceptions.Timeout:
            print(f"[WARN] Request timed out (attempt {attempt + 1}/{max_retries + 1})", file=sys.stderr)
            if attempt < max_retries:
                time.sleep(base_delay * (2 ** attempt))
                continue
            raise

        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Network error: {e}", file=sys.stderr)
            if attempt < max_retries:
                time.sleep(base_delay * (2 ** attempt))
                continue
            raise

    # Return last response if all retries exhausted
    return last_response


def get_cache_file_path(nexus_root=None) -> Path:
    """Get path to airtable-bases.yaml cache file."""
    if nexus_root is None:
        nexus_root = find_nexus_root()
    if nexus_root is None:
        raise ValueError("Could not find Nexus root")

    return Path(nexus_root) / '01-memory' / 'integrations' / 'airtable-bases.yaml'


def load_base_cache(nexus_root=None) -> dict:
    """Load cached base info from YAML file."""
    cache_file = get_cache_file_path(nexus_root)
    if cache_file.exists():
        with open(cache_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or {}
    return {}


def update_context_file(nexus_root=None, bases=None, base_update=None):
    """
    Update airtable-bases.yaml context file.

    Args:
        nexus_root: Path to Nexus root
        bases: Full list of bases to write (overwrites)
        base_update: Single base to update/add (merges)
    """
    if nexus_root is None:
        nexus_root = find_nexus_root()
    if nexus_root is None:
        print("[WARN] Could not find Nexus root, skipping context update", file=sys.stderr)
        return

    cache_file = get_cache_file_path(nexus_root)

    # Ensure directory exists
    cache_file.parent.mkdir(parents=True, exist_ok=True)

    # Load existing or start fresh
    if cache_file.exists():
        with open(cache_file, 'r', encoding='utf-8') as f:
            context = yaml.safe_load(f) or {}
    else:
        context = {}

    # Update bases
    if bases is not None:
        context['bases'] = bases
        context['total_bases'] = len(bases)
    elif base_update is not None:
        existing_bases = context.get('bases', [])
        base_id = base_update.get('id')

        # Find and update or append
        found = False
        for i, b in enumerate(existing_bases):
            if b.get('id') == base_id:
                existing_bases[i] = base_update
                found = True
                break
        if not found:
            existing_bases.append(base_update)

        context['bases'] = existing_bases
        context['total_bases'] = len(existing_bases)

    context['discovered_at'] = datetime.now().isoformat()

    # Write back
    with open(cache_file, 'w', encoding='utf-8') as f:
        yaml.dump(context, f, default_flow_style=False, allow_unicode=True)

    print(f"[INFO] Updated context file: {cache_file}", file=sys.stderr)


def resolve_base_id(base_ref: str, token_name: str = None, verbose: bool = False) -> str:
    """
    Resolve base name to ID.

    Args:
        base_ref: Base ID (appXXX) or name
        token_name: Optional token name for API calls
        verbose: Print debug info

    Returns:
        Base ID string
    """
    # Already an ID
    if base_ref.startswith('app'):
        return base_ref

    # Try cache first
    cache = load_base_cache()
    for base in cache.get('bases', []):
        if base.get('name', '').lower() == base_ref.lower():
            if verbose:
                print(f"[INFO] Resolved '{base_ref}' → {base['id']} (from cache)", file=sys.stderr)
            return base['id']

    # Try API
    try:
        headers = get_headers(token_name)
        response = requests.get(f"{API_BASE_URL}/meta/bases", headers=headers, timeout=10)
        if response.status_code == 200:
            for base in response.json().get('bases', []):
                if base.get('name', '').lower() == base_ref.lower():
                    if verbose:
                        print(f"[INFO] Resolved '{base_ref}' → {base['id']} (from API)", file=sys.stderr)
                    return base['id']
    except Exception as e:
        if verbose:
            print(f"[WARN] API lookup failed: {e}", file=sys.stderr)

    raise ValueError(f"Could not resolve base: {base_ref}")


# Module-level initialization
_nexus_root = find_nexus_root()
if _nexus_root:
    NEXUS_ROOT = _nexus_root
    CACHE_FILE = get_cache_file_path(_nexus_root)
else:
    NEXUS_ROOT = None
    CACHE_FILE = None
