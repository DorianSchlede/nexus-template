#!/usr/bin/env python3
"""
Beam API Client

Shared client for Beam API authentication and requests.
Used by all Beam API scripts.
"""

import os
import time
from pathlib import Path


SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent.parent.parent.parent
ENV_FILE = PROJECT_ROOT / ".env"
BASE_URL = "https://api.beamstudio.ai"


class BeamClient:
    """Beam API client with automatic token management"""

    def __init__(self):
        self.api_key = None
        self.workspace_id = None
        self.access_token = None
        self.refresh_token = None
        self.token_expiry = 0
        self._load_config()

    def _load_config(self):
        """Load configuration from .env"""
        env_vars = {}
        if ENV_FILE.exists():
            with open(ENV_FILE, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, _, value = line.partition('=')
                        env_vars[key.strip()] = value.strip().strip('"\'')

        self.api_key = env_vars.get('BEAM_API_KEY') or os.getenv('BEAM_API_KEY')
        self.workspace_id = env_vars.get('BEAM_WORKSPACE_ID') or os.getenv('BEAM_WORKSPACE_ID')

        if not self.api_key:
            raise ValueError("BEAM_API_KEY not found in .env or environment")
        if not self.workspace_id:
            raise ValueError("BEAM_WORKSPACE_ID not found in .env or environment")

    def _authenticate(self):
        """Get access token from API key"""
        import requests

        response = requests.post(
            f"{BASE_URL}/auth/access-token",
            json={"apiKey": self.api_key},
            timeout=30
        )

        if response.status_code != 201:
            raise Exception(f"Authentication failed: {response.status_code} - {response.text}")

        tokens = response.json()
        self.access_token = tokens['idToken']
        self.refresh_token = tokens['refreshToken']
        self.token_expiry = time.time() + 3500  # ~58 minutes

    def _refresh_access_token(self):
        """Refresh access token"""
        import requests

        response = requests.post(
            f"{BASE_URL}/auth/refresh-token",
            json={"refreshToken": self.refresh_token},
            timeout=30
        )

        if response.status_code != 201:
            # Refresh failed, re-authenticate
            self._authenticate()
            return

        tokens = response.json()
        self.access_token = tokens['idToken']
        self.refresh_token = tokens['refreshToken']
        self.token_expiry = time.time() + 3500

    def _ensure_token(self):
        """Ensure we have a valid access token"""
        if time.time() > self.token_expiry:
            if self.refresh_token:
                self._refresh_access_token()
            else:
                self._authenticate()

    def get_headers(self):
        """Get headers for API request"""
        self._ensure_token()
        return {
            'Authorization': f'Bearer {self.access_token}',
            'current-workspace-id': self.workspace_id,
            'Content-Type': 'application/json'
        }

    def get(self, endpoint, params=None):
        """Make GET request"""
        import requests

        url = f"{BASE_URL}{endpoint}"
        response = requests.get(
            url,
            headers=self.get_headers(),
            params=params,
            timeout=60
        )
        return self._handle_response(response)

    def post(self, endpoint, data=None):
        """Make POST request"""
        import requests

        url = f"{BASE_URL}{endpoint}"
        response = requests.post(
            url,
            headers=self.get_headers(),
            json=data,
            timeout=60
        )
        return self._handle_response(response)

    def patch(self, endpoint, data=None):
        """Make PATCH request"""
        import requests

        url = f"{BASE_URL}{endpoint}"
        response = requests.patch(
            url,
            headers=self.get_headers(),
            json=data,
            timeout=60
        )
        return self._handle_response(response)

    def _handle_response(self, response):
        """Handle API response"""
        if response.status_code in [200, 201]:
            try:
                return response.json()
            except:
                return {"status": "success"}
        elif response.status_code == 401:
            # Token expired, retry once
            self._authenticate()
            raise Exception("Token expired - please retry")
        else:
            raise Exception(f"API error: {response.status_code} - {response.text}")


def get_client():
    """Get a configured Beam client"""
    return BeamClient()
