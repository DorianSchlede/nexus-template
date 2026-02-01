#!/usr/bin/env python3
"""
NotebookLM Enterprise API Client

Shared client for NotebookLM Enterprise API authentication and requests.
Uses OAuth 2.0 via gcloud CLI for authentication.
"""

import os
import subprocess
import json
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent.parent.parent.parent
ENV_FILE = PROJECT_ROOT / ".env"


def load_env():
    """Load environment variables from .env"""
    env_vars = {}
    if ENV_FILE.exists():
        with open(ENV_FILE, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, _, value = line.partition('=')
                    env_vars[key.strip()] = value.strip().strip('"\'')
    return env_vars


class NotebookLMClient:
    """NotebookLM Enterprise API client with gcloud OAuth authentication"""

    def __init__(self):
        self.project_number = None
        self.location = None
        self.endpoint_location = None
        self.access_token = None
        self._load_config()

    def _load_config(self):
        """Load configuration from .env"""
        env_vars = load_env()

        self.project_number = env_vars.get('GOOGLE_CLOUD_PROJECT_NUMBER') or os.getenv('GOOGLE_CLOUD_PROJECT_NUMBER')
        self.location = env_vars.get('NOTEBOOKLM_LOCATION') or os.getenv('NOTEBOOKLM_LOCATION') or 'global'
        self.endpoint_location = env_vars.get('NOTEBOOKLM_ENDPOINT_LOCATION') or os.getenv('NOTEBOOKLM_ENDPOINT_LOCATION') or 'global'

        if not self.project_number:
            raise ValueError("GOOGLE_CLOUD_PROJECT_NUMBER not found in .env or environment")

    def _get_access_token(self):
        """Get access token from gcloud CLI"""
        try:
            result = subprocess.run(
                ['gcloud', 'auth', 'print-access-token'],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            raise Exception(f"Failed to get gcloud access token: {e.stderr}")
        except FileNotFoundError:
            raise Exception("gcloud CLI not found. Install Google Cloud SDK: https://cloud.google.com/sdk/docs/install")

    def get_base_url(self):
        """Get the base URL for API requests"""
        prefix = f"{self.endpoint_location}-" if self.endpoint_location != 'global' else 'global-'
        return f"https://{prefix}discoveryengine.googleapis.com/v1alpha/projects/{self.project_number}/locations/{self.location}"

    def get_headers(self):
        """Get headers for API request"""
        if not self.access_token:
            self.access_token = self._get_access_token()

        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

    def get(self, endpoint, params=None):
        """Make GET request"""
        import requests

        url = f"{self.get_base_url()}{endpoint}"
        response = requests.get(
            url,
            headers=self.get_headers(),
            params=params,
            timeout=60
        )
        return self._handle_response(response)

    def post(self, endpoint, data=None, headers_override=None):
        """Make POST request"""
        import requests

        url = f"{self.get_base_url()}{endpoint}"
        headers = headers_override if headers_override else self.get_headers()

        if headers_override:
            # Add auth header if not present
            if "Authorization" not in headers:
                headers["Authorization"] = f"Bearer {self._get_access_token()}"

        response = requests.post(
            url,
            headers=headers,
            json=data if not headers_override else None,
            data=data if headers_override else None,
            timeout=120
        )
        return self._handle_response(response)

    def post_file(self, endpoint, file_path, content_type):
        """Upload a file via POST"""
        import requests

        url = f"{self.get_base_url()}{endpoint}"
        file_name = Path(file_path).name

        with open(file_path, 'rb') as f:
            file_data = f.read()

        headers = {
            "Authorization": f"Bearer {self._get_access_token()}",
            "Content-Type": content_type,
            "X-Goog-Upload-File-Name": file_name,
            "X-Goog-Upload-Protocol": "raw"
        }

        response = requests.post(
            url,
            headers=headers,
            data=file_data,
            timeout=300
        )
        return self._handle_response(response)

    def delete(self, endpoint):
        """Make DELETE request"""
        import requests

        url = f"{self.get_base_url()}{endpoint}"
        response = requests.delete(
            url,
            headers=self.get_headers(),
            timeout=60
        )
        return self._handle_response(response)

    def _handle_response(self, response):
        """Handle API response"""
        if response.status_code in [200, 201, 204]:
            try:
                return response.json()
            except:
                return {"status": "success"}
        elif response.status_code == 401:
            # Token expired, refresh and raise for retry
            self.access_token = None
            raise Exception("Token expired - please retry")
        elif response.status_code == 403:
            raise Exception(f"Permission denied. Check that NotebookLM Enterprise API is enabled and you have required roles. Details: {response.text}")
        elif response.status_code == 404:
            raise Exception(f"Resource not found: {response.text}")
        else:
            raise Exception(f"API error: {response.status_code} - {response.text}")


def get_client():
    """Get a configured NotebookLM client"""
    return NotebookLMClient()
