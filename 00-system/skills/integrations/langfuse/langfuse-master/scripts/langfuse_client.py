"""
Langfuse API Client

Handles authentication and HTTP requests to Langfuse API.
Uses Basic Auth with Public Key as username and Secret Key as password.

Features:
- Automatic retry for transient errors (429, 503, 504)
- Parsed error messages via LangfuseAPIError
- Connection pooling via requests.Session
"""

import os
import time
import requests
from typing import Optional, Any, Callable
from dotenv import load_dotenv

load_dotenv()


# Retry configuration
RETRY_STATUS_CODES = {429, 503, 504}  # Rate limit, Service unavailable, Gateway timeout
MAX_RETRIES = 3
RETRY_DELAYS = [1, 2, 4]  # Exponential backoff in seconds


class LangfuseAPIError(Exception):
    """Exception raised for Langfuse API errors with parsed response."""

    def __init__(self, status_code: int, message: str, error_body: dict = None):
        self.status_code = status_code
        self.message = message
        self.error_body = error_body or {}
        self.is_retryable = status_code in RETRY_STATUS_CODES
        super().__init__(f"[{status_code}] {message}")


class LangfuseClient:
    """Client for Langfuse REST API with automatic retry."""

    def __init__(
        self,
        public_key: Optional[str] = None,
        secret_key: Optional[str] = None,
        host: Optional[str] = None,
        max_retries: int = MAX_RETRIES,
        retry_delays: list = None
    ):
        self.public_key = public_key or os.getenv("LANGFUSE_PUBLIC_KEY")
        self.secret_key = secret_key or os.getenv("LANGFUSE_SECRET_KEY")
        self.host = (host or os.getenv("LANGFUSE_HOST", "")).rstrip("/")
        self.max_retries = max_retries
        self.retry_delays = retry_delays or RETRY_DELAYS

        if not self.public_key or not self.secret_key:
            raise ValueError(
                "Missing Langfuse credentials. Set LANGFUSE_PUBLIC_KEY and "
                "LANGFUSE_SECRET_KEY environment variables."
            )

        if not self.host:
            raise ValueError(
                "Missing Langfuse host. Set LANGFUSE_HOST environment variable."
            )

        self.base_url = f"{self.host}/api/public"
        self.session = requests.Session()
        self.session.auth = (self.public_key, self.secret_key)
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

    def _handle_response(self, response: requests.Response) -> dict:
        """Handle API response, raising LangfuseAPIError on errors."""
        if response.ok:
            try:
                return response.json()
            except ValueError:
                return {"message": "Success", "status": response.status_code}

        # Parse error response
        try:
            error_body = response.json()
            message = error_body.get("message") or error_body.get("error") or str(error_body)
        except ValueError:
            error_body = {}
            message = response.text or response.reason

        raise LangfuseAPIError(
            status_code=response.status_code,
            message=message,
            error_body=error_body
        )

    def _request_with_retry(
        self,
        method: Callable,
        url: str,
        **kwargs
    ) -> dict:
        """Execute request with automatic retry for transient errors."""
        last_error = None

        for attempt in range(self.max_retries + 1):
            try:
                response = method(url, **kwargs)

                # Check if we should retry
                if response.status_code in RETRY_STATUS_CODES and attempt < self.max_retries:
                    delay = self.retry_delays[min(attempt, len(self.retry_delays) - 1)]

                    # Check for Retry-After header
                    retry_after = response.headers.get("Retry-After")
                    if retry_after:
                        try:
                            delay = int(retry_after)
                        except ValueError:
                            pass

                    print(f"Rate limited ({response.status_code}), retrying in {delay}s... (attempt {attempt + 1}/{self.max_retries})")
                    time.sleep(delay)
                    continue

                return self._handle_response(response)

            except requests.exceptions.ConnectionError as e:
                last_error = e
                if attempt < self.max_retries:
                    delay = self.retry_delays[min(attempt, len(self.retry_delays) - 1)]
                    print(f"Connection error, retrying in {delay}s... (attempt {attempt + 1}/{self.max_retries})")
                    time.sleep(delay)
                    continue
                raise LangfuseAPIError(
                    status_code=0,
                    message=f"Connection failed after {self.max_retries} retries: {e}"
                )

            except requests.exceptions.Timeout as e:
                last_error = e
                if attempt < self.max_retries:
                    delay = self.retry_delays[min(attempt, len(self.retry_delays) - 1)]
                    print(f"Request timeout, retrying in {delay}s... (attempt {attempt + 1}/{self.max_retries})")
                    time.sleep(delay)
                    continue
                raise LangfuseAPIError(
                    status_code=0,
                    message=f"Request timed out after {self.max_retries} retries: {e}"
                )

        # Should not reach here, but just in case
        if last_error:
            raise LangfuseAPIError(
                status_code=0,
                message=f"Request failed after {self.max_retries} retries: {last_error}"
            )

    def get(self, endpoint: str, params: Optional[dict] = None) -> dict:
        """Make GET request to Langfuse API with retry."""
        url = f"{self.base_url}{endpoint}"
        return self._request_with_retry(self.session.get, url, params=params)

    def post(self, endpoint: str, data: Optional[dict] = None) -> dict:
        """Make POST request to Langfuse API with retry."""
        url = f"{self.base_url}{endpoint}"
        return self._request_with_retry(self.session.post, url, json=data)

    def delete(self, endpoint: str, params: Optional[dict] = None) -> dict:
        """Make DELETE request to Langfuse API with retry."""
        url = f"{self.base_url}{endpoint}"
        return self._request_with_retry(self.session.delete, url, params=params)

    def patch(self, endpoint: str, data: Optional[dict] = None) -> dict:
        """Make PATCH request to Langfuse API with retry."""
        url = f"{self.base_url}{endpoint}"
        return self._request_with_retry(self.session.patch, url, json=data)

    def put(self, endpoint: str, data: Optional[dict] = None) -> dict:
        """Make PUT request to Langfuse API with retry."""
        url = f"{self.base_url}{endpoint}"
        return self._request_with_retry(self.session.put, url, json=data)


_client: Optional[LangfuseClient] = None


def get_client() -> LangfuseClient:
    """Get or create singleton Langfuse client."""
    global _client
    if _client is None:
        _client = LangfuseClient()
    return _client


if __name__ == "__main__":
    # Quick test
    client = get_client()
    print(f"Langfuse client initialized")
    print(f"Host: {client.host}")
    print(f"Base URL: {client.base_url}")
    print(f"Max retries: {client.max_retries}")
    print(f"Retry delays: {client.retry_delays}s")
