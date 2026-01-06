"""
Langfuse API Client

Handles authentication and HTTP requests to Langfuse API.
Uses Basic Auth with Public Key as username and Secret Key as password.
"""

import os
import requests
from typing import Optional, Any
from dotenv import load_dotenv

load_dotenv()


class LangfuseClient:
    """Client for Langfuse REST API."""

    def __init__(
        self,
        public_key: Optional[str] = None,
        secret_key: Optional[str] = None,
        host: Optional[str] = None
    ):
        self.public_key = public_key or os.getenv("LANGFUSE_PUBLIC_KEY")
        self.secret_key = secret_key or os.getenv("LANGFUSE_SECRET_KEY")
        self.host = (host or os.getenv("LANGFUSE_HOST", "")).rstrip("/")

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

    def get(self, endpoint: str, params: Optional[dict] = None) -> dict:
        """Make GET request to Langfuse API."""
        url = f"{self.base_url}{endpoint}"
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def post(self, endpoint: str, data: Optional[dict] = None) -> dict:
        """Make POST request to Langfuse API."""
        url = f"{self.base_url}{endpoint}"
        response = self.session.post(url, json=data)
        response.raise_for_status()
        return response.json()

    def delete(self, endpoint: str, params: Optional[dict] = None) -> dict:
        """Make DELETE request to Langfuse API."""
        url = f"{self.base_url}{endpoint}"
        response = self.session.delete(url, params=params)
        response.raise_for_status()
        return response.json()

    def patch(self, endpoint: str, data: Optional[dict] = None) -> dict:
        """Make PATCH request to Langfuse API (partial update)."""
        url = f"{self.base_url}{endpoint}"
        response = self.session.patch(url, json=data)
        response.raise_for_status()
        return response.json()

    def put(self, endpoint: str, data: Optional[dict] = None) -> dict:
        """Make PUT request to Langfuse API (full update)."""
        url = f"{self.base_url}{endpoint}"
        response = self.session.put(url, json=data)
        response.raise_for_status()
        return response.json()


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
