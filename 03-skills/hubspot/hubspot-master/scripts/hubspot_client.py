#!/usr/bin/env python3
"""
HubSpot API Client

Shared client for HubSpot API authentication and requests.
Used by all HubSpot API scripts.
"""

import os
import time
import logging
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent.parent.parent.parent
ENV_FILE = PROJECT_ROOT / ".env"
BASE_URL = "https://api.hubapi.com"


class HubSpotError(Exception):
    """Custom exception for HubSpot API errors."""

    def __init__(self, status_code, message, category=None, errors=None, correlation_id=None):
        self.status_code = status_code
        self.message = message
        self.category = category
        self.errors = errors or []
        self.correlation_id = correlation_id
        super().__init__(f"HubSpot API Error ({status_code}): {message}")


class HubSpotClient:
    """HubSpot API client with automatic error handling and retry logic."""

    def __init__(self):
        self.access_token = None
        self._load_config()

    def _load_config(self):
        """Load configuration from .env file."""
        env_vars = {}
        if ENV_FILE.exists():
            with open(ENV_FILE, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, _, value = line.partition('=')
                        env_vars[key.strip()] = value.strip().strip('"\'')

        self.access_token = env_vars.get('HUBSPOT_ACCESS_TOKEN') or os.getenv('HUBSPOT_ACCESS_TOKEN')

        if not self.access_token:
            raise ValueError("HUBSPOT_ACCESS_TOKEN not found in .env or environment")

    def get_headers(self):
        """Get headers for API request."""
        return {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }

    def _handle_response(self, response):
        """Handle API response with error parsing."""
        if response.status_code in [200, 201]:
            try:
                return response.json()
            except:
                return {"status": "success"}
        elif response.status_code == 204:
            return {"status": "success", "message": "No content"}
        else:
            # Parse error response
            try:
                error_data = response.json()
            except:
                error_data = {"message": response.text}

            raise HubSpotError(
                status_code=response.status_code,
                message=error_data.get('message', 'Unknown error'),
                category=error_data.get('category'),
                errors=error_data.get('errors', []),
                correlation_id=error_data.get('correlationId')
            )

    def _request_with_retry(self, method, endpoint, params=None, data=None, max_retries=3):
        """Make request with automatic retry for rate limits and server errors."""
        import requests

        url = f"{BASE_URL}{endpoint}"

        for attempt in range(max_retries):
            try:
                response = requests.request(
                    method,
                    url,
                    headers=self.get_headers(),
                    params=params,
                    json=data,
                    timeout=60
                )

                # Rate limited - retry with backoff
                if response.status_code == 429:
                    wait = int(response.headers.get('Retry-After', 2 ** attempt))
                    logging.warning(f"Rate limited, waiting {wait}s")
                    time.sleep(wait)
                    continue

                # Server error - retry with backoff
                if response.status_code >= 500:
                    time.sleep(2 ** attempt)
                    continue

                return self._handle_response(response)

            except requests.exceptions.Timeout:
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                raise HubSpotError(408, "Request timeout")
            except requests.exceptions.ConnectionError:
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                raise HubSpotError(503, "Cannot connect to HubSpot API")

        raise HubSpotError(500, "Max retries exceeded")

    def get(self, endpoint, params=None):
        """Make GET request."""
        return self._request_with_retry('GET', endpoint, params=params)

    def post(self, endpoint, data=None):
        """Make POST request."""
        return self._request_with_retry('POST', endpoint, data=data)

    def patch(self, endpoint, data=None):
        """Make PATCH request."""
        return self._request_with_retry('PATCH', endpoint, data=data)

    def delete(self, endpoint):
        """Make DELETE request."""
        return self._request_with_retry('DELETE', endpoint)


def get_client():
    """Get a configured HubSpot client."""
    return HubSpotClient()
