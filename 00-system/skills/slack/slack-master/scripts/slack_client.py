#!/usr/bin/env python3
"""
Slack API Client

Shared client for Slack API authentication and requests.
Used by all Slack API scripts.

Uses User OAuth tokens (xoxp-) for per-user authentication.
"""

import os
import json
import time
from pathlib import Path
from urllib.parse import urlencode


SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent.parent.parent.parent
ENV_FILE = PROJECT_ROOT / ".env"
BASE_URL = "https://slack.com/api"


class SlackClient:
    """Slack API client with User OAuth token support"""

    def __init__(self):
        self.user_token = None
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

        self.user_token = env_vars.get('SLACK_USER_TOKEN') or os.getenv('SLACK_USER_TOKEN')

        if not self.user_token:
            raise ValueError("SLACK_USER_TOKEN not found in .env or environment")

    def get_headers(self):
        """Get headers for API request"""
        return {
            'Authorization': f'Bearer {self.user_token}',
            'Content-Type': 'application/json; charset=utf-8'
        }

    def get(self, method, params=None):
        """Make GET request to Slack API"""
        import requests

        url = f"{BASE_URL}/{method}"
        response = requests.get(
            url,
            headers=self.get_headers(),
            params=params,
            timeout=30
        )
        return self._handle_response(response, method)

    def post(self, method, data=None):
        """Make POST request to Slack API"""
        import requests

        url = f"{BASE_URL}/{method}"
        response = requests.post(
            url,
            headers=self.get_headers(),
            json=data,
            timeout=30
        )
        return self._handle_response(response, method)

    def post_form(self, method, data=None, files=None):
        """Make POST request with form data (for file uploads)"""
        import requests

        url = f"{BASE_URL}/{method}"
        headers = {'Authorization': f'Bearer {self.user_token}'}
        response = requests.post(
            url,
            headers=headers,
            data=data,
            files=files,
            timeout=60
        )
        return self._handle_response(response, method)

    def _handle_response(self, response, method):
        """Handle Slack API response"""
        if response.status_code != 200:
            raise SlackAPIError(
                f"HTTP {response.status_code}",
                method=method,
                status_code=response.status_code,
                response_text=response.text
            )

        try:
            data = response.json()
        except json.JSONDecodeError:
            raise SlackAPIError(
                "Invalid JSON response",
                method=method,
                response_text=response.text
            )

        if not data.get('ok', False):
            error = data.get('error', 'unknown_error')
            raise SlackAPIError(
                error,
                method=method,
                error_code=error,
                response_data=data
            )

        return data

    def paginate(self, method, params=None, limit=None):
        """Paginate through results using cursor-based pagination"""
        params = params or {}
        results = []
        cursor = None

        while True:
            if cursor:
                params['cursor'] = cursor

            response = self.get(method, params)

            # Extract items based on method
            if 'channels' in response:
                results.extend(response['channels'])
            elif 'members' in response:
                results.extend(response['members'])
            elif 'messages' in response:
                results.extend(response['messages'])
            elif 'files' in response:
                results.extend(response['files'])
            elif 'items' in response:
                results.extend(response['items'])

            # Check for more pages
            metadata = response.get('response_metadata', {})
            cursor = metadata.get('next_cursor', '')

            if not cursor:
                break

            if limit and len(results) >= limit:
                results = results[:limit]
                break

            # Rate limit protection
            time.sleep(0.2)

        return results


class SlackAPIError(Exception):
    """Slack API Error with detailed information"""

    def __init__(self, message, method=None, status_code=None, error_code=None,
                 response_text=None, response_data=None):
        super().__init__(message)
        self.method = method
        self.status_code = status_code
        self.error_code = error_code
        self.response_text = response_text
        self.response_data = response_data

    def to_dict(self):
        """Convert error to dictionary for JSON output"""
        return {
            'error': str(self),
            'method': self.method,
            'status_code': self.status_code,
            'error_code': self.error_code,
            'details': self.response_data or self.response_text
        }


def get_client():
    """Get a configured Slack client"""
    return SlackClient()


# Common error code explanations
ERROR_EXPLANATIONS = {
    'not_authed': 'No authentication token provided',
    'invalid_auth': 'Invalid authentication token',
    'account_inactive': 'User account is inactive',
    'token_revoked': 'Token has been revoked',
    'no_permission': 'Token does not have required scope',
    'missing_scope': 'Token is missing a required scope',
    'channel_not_found': 'Channel does not exist or you lack access',
    'user_not_found': 'User does not exist',
    'message_not_found': 'Message does not exist',
    'cant_delete_message': 'Cannot delete this message (not yours or too old)',
    'rate_limited': 'Too many requests - wait and retry',
    'fatal_error': 'Server error - retry later',
}


def explain_error(error_code):
    """Get human-readable explanation for error code"""
    return ERROR_EXPLANATIONS.get(error_code, f'Unknown error: {error_code}')
