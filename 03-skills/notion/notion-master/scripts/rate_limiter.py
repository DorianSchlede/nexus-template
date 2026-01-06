#!/usr/bin/env python3
"""
Rate Limiter - Exponential backoff for Notion API

Usage:
    from rate_limiter import with_retry, RateLimiter

    # Simple decorator usage
    @with_retry(max_retries=3, base_delay=1.0)
    def my_api_call():
        return requests.get(...)

    # Or use RateLimiter class directly
    limiter = RateLimiter(max_retries=3, base_delay=1.0)
    response = limiter.execute(lambda: requests.get(...))

Notion API Rate Limits:
    - 3 requests per second (average)
    - 429 Too Many Requests returned when exceeded
    - Retry-After header may be present
"""

import time
import random
import sys
from functools import wraps

try:
    import requests
except ImportError:
    requests = None


class RateLimitError(Exception):
    """Raised when rate limit is exceeded after all retries"""
    pass


class RateLimiter:
    """
    Handles Notion API rate limiting with exponential backoff.

    Args:
        max_retries: Maximum number of retry attempts (default: 3)
        base_delay: Initial delay in seconds (default: 1.0)
        max_delay: Maximum delay in seconds (default: 60.0)
        jitter: Random jitter factor 0-1 (default: 0.1)
    """

    def __init__(self, max_retries=3, base_delay=1.0, max_delay=60.0, jitter=0.1):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.jitter = jitter
        self.last_request_time = 0
        self.min_request_interval = 0.35  # ~3 requests per second

    def _calculate_delay(self, attempt, retry_after=None):
        """
        Calculate delay with exponential backoff and jitter.

        Args:
            attempt: Current retry attempt (0-indexed)
            retry_after: Optional Retry-After header value

        Returns:
            Delay in seconds
        """
        if retry_after:
            try:
                return float(retry_after)
            except (ValueError, TypeError):
                pass

        # Exponential backoff: base_delay * 2^attempt
        delay = self.base_delay * (2 ** attempt)

        # Add jitter to prevent thundering herd
        jitter_range = delay * self.jitter
        delay += random.uniform(-jitter_range, jitter_range)

        # Cap at max_delay
        return min(delay, self.max_delay)

    def _respect_rate_limit(self):
        """Ensure minimum time between requests"""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.min_request_interval:
            time.sleep(self.min_request_interval - elapsed)
        self.last_request_time = time.time()

    def execute(self, func, *args, **kwargs):
        """
        Execute a function with retry logic.

        Args:
            func: Function to execute (should return a response with status_code)
            *args, **kwargs: Arguments to pass to func

        Returns:
            The function result

        Raises:
            RateLimitError: If rate limit exceeded after all retries
            Exception: Any other exception from func
        """
        last_error = None

        for attempt in range(self.max_retries + 1):
            try:
                self._respect_rate_limit()
                result = func(*args, **kwargs)

                # Check if result is a response object with status_code
                if hasattr(result, 'status_code'):
                    if result.status_code == 429:
                        retry_after = result.headers.get('Retry-After')
                        delay = self._calculate_delay(attempt, retry_after)

                        if attempt < self.max_retries:
                            print(f"[WARN] Rate limited. Retrying in {delay:.1f}s (attempt {attempt + 1}/{self.max_retries})",
                                  file=sys.stderr)
                            time.sleep(delay)
                            continue
                        else:
                            raise RateLimitError(
                                f"Rate limit exceeded after {self.max_retries} retries"
                            )

                return result

            except Exception as e:
                last_error = e

                # Only retry on rate limit, network errors, or 5xx
                should_retry = (
                    isinstance(e, RateLimitError) or
                    (requests and isinstance(e, requests.exceptions.RequestException)) or
                    (hasattr(e, 'response') and getattr(e.response, 'status_code', 0) >= 500)
                )

                if should_retry and attempt < self.max_retries:
                    delay = self._calculate_delay(attempt)
                    print(f"[WARN] Request failed: {e}. Retrying in {delay:.1f}s",
                          file=sys.stderr)
                    time.sleep(delay)
                    continue

                raise

        if last_error:
            raise last_error


def with_retry(max_retries=3, base_delay=1.0, max_delay=60.0, jitter=0.1):
    """
    Decorator for adding retry logic to functions.

    Usage:
        @with_retry(max_retries=3)
        def my_api_call():
            return requests.get(...)
    """
    limiter = RateLimiter(max_retries, base_delay, max_delay, jitter)

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return limiter.execute(lambda: func(*args, **kwargs))
        return wrapper

    return decorator


def make_request_with_retry(method, url, headers, max_retries=3, **kwargs):
    """
    Convenience function for making HTTP requests with retry.

    Args:
        method: HTTP method ('get', 'post', 'patch', 'delete')
        url: Request URL
        headers: Request headers
        max_retries: Maximum retries
        **kwargs: Additional requests arguments (json, params, timeout, etc.)

    Returns:
        Response object

    Raises:
        RateLimitError: If rate limit exceeded after all retries
        requests.exceptions.RequestException: On network errors after retries
    """
    if not requests:
        raise ImportError("requests library required")

    limiter = RateLimiter(max_retries=max_retries)
    method_func = getattr(requests, method.lower())

    return limiter.execute(lambda: method_func(url, headers=headers, **kwargs))


# Example usage
if __name__ == "__main__":
    print("Rate Limiter Module")
    print("=" * 40)
    print()
    print("Usage in scripts:")
    print()
    print("  from rate_limiter import make_request_with_retry")
    print()
    print("  response = make_request_with_retry(")
    print("      'get',")
    print("      'https://api.notion.com/v1/databases',")
    print("      headers={'Authorization': 'Bearer ...'},")
    print("      max_retries=3")
    print("  )")
    print()
    print("Features:")
    print("  - Exponential backoff (1s, 2s, 4s, ...)")
    print("  - Respects Retry-After header")
    print("  - Adds jitter to prevent thundering herd")
    print("  - Rate limits to ~3 requests/second")
    print("  - Retries on 429, 5xx, and network errors")
