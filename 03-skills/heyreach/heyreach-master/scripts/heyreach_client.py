#!/usr/bin/env python3
"""
HeyReach API Client

Shared client for HeyReach API authentication and requests.
Used by all HeyReach API scripts.

API Base: https://api.heyreach.io/api/public/
Auth: X-API-KEY header
Rate Limit: 300 requests/minute
"""

import os
import time
import logging
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent.parent.parent.parent
ENV_FILE = PROJECT_ROOT / ".env"
BASE_URL = "https://api.heyreach.io/api/public"


class HeyReachError(Exception):
    """Custom exception for HeyReach API errors."""

    def __init__(self, status_code, message, details=None):
        self.status_code = status_code
        self.message = message
        self.details = details or {}
        super().__init__(f"HeyReach API Error ({status_code}): {message}")


class HeyReachClient:
    """HeyReach API client with automatic error handling and retry logic."""

    def __init__(self):
        self.api_key = None
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

        self.api_key = env_vars.get('HEYREACH_API_KEY') or os.getenv('HEYREACH_API_KEY')

        if not self.api_key:
            raise ValueError("HEYREACH_API_KEY not found in .env or environment")

    def get_headers(self):
        """Get headers for API request."""
        return {
            'X-API-KEY': self.api_key,
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

            raise HeyReachError(
                status_code=response.status_code,
                message=error_data.get('message', error_data.get('error', 'Unknown error')),
                details=error_data
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

                # Rate limited - retry with backoff (300 req/min limit)
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
                raise HeyReachError(408, "Request timeout")
            except requests.exceptions.ConnectionError:
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                raise HeyReachError(503, "Cannot connect to HeyReach API")

        raise HeyReachError(500, "Max retries exceeded")

    def get(self, endpoint, params=None):
        """Make GET request."""
        return self._request_with_retry('GET', endpoint, params=params)

    def post(self, endpoint, data=None):
        """Make POST request."""
        return self._request_with_retry('POST', endpoint, data=data)

    def put(self, endpoint, data=None):
        """Make PUT request."""
        return self._request_with_retry('PUT', endpoint, data=data)

    def delete(self, endpoint):
        """Make DELETE request."""
        return self._request_with_retry('DELETE', endpoint)


def get_client():
    """Get a configured HeyReach client."""
    return HeyReachClient()


def mask_api_key(key):
    """Mask API key for safe logging."""
    if not key or len(key) < 8:
        return "***"
    return f"{key[:4]}...{key[-4:]}"
