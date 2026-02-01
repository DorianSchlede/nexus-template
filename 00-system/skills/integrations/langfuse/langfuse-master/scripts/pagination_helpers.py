#!/usr/bin/env python3
"""Pagination helpers for fetching all items from Langfuse API.

Two pagination types:
1. Page-based: traces, sessions, datasets, prompts (use page=N)
2. Cursor-based: observations, scores (use cursor=abc...)

Usage:
    from pagination_helpers import fetch_all_pages, fetch_all_cursor

    # Page-based
    all_traces = fetch_all_pages("/traces", params={"userId": "..."})

    # Cursor-based
    all_scores = fetch_all_cursor("/v2/scores", params={"traceId": "..."})
"""

from typing import Optional, Generator
from langfuse_client import get_client, LangfuseAPIError


def fetch_all_pages(
    endpoint: str,
    params: Optional[dict] = None,
    limit: int = 100,
    max_pages: int = None
) -> list:
    """Fetch all items using page-based pagination.

    Args:
        endpoint: API endpoint (e.g., "/traces")
        params: Additional query parameters
        limit: Items per page (max 100)
        max_pages: Stop after N pages (None = fetch all)

    Returns:
        List of all items across all pages
    """
    client = get_client()
    all_items = []
    page = 1
    params = params or {}

    while True:
        params["page"] = page
        params["limit"] = min(limit, 100)

        response = client.get(endpoint, params=params)
        data = response.get("data", [])
        all_items.extend(data)

        meta = response.get("meta", {})
        total_pages = meta.get("totalPages", 1)

        print(f"Fetched page {page}/{total_pages} ({len(data)} items)")

        if page >= total_pages:
            break
        if max_pages and page >= max_pages:
            print(f"Stopped at max_pages={max_pages}")
            break

        page += 1

    print(f"Total: {len(all_items)} items")
    return all_items


def fetch_all_cursor(
    endpoint: str,
    params: Optional[dict] = None,
    limit: int = 100,
    max_iterations: int = None
) -> list:
    """Fetch all items using cursor-based pagination.

    Args:
        endpoint: API endpoint (e.g., "/v2/scores")
        params: Additional query parameters
        limit: Items per page (max 100)
        max_iterations: Stop after N fetches (None = fetch all)

    Returns:
        List of all items across all pages
    """
    client = get_client()
    all_items = []
    cursor = None
    iteration = 0
    params = params or {}

    while True:
        params["limit"] = min(limit, 100)
        if cursor:
            params["cursor"] = cursor
        elif "cursor" in params:
            del params["cursor"]

        response = client.get(endpoint, params=params)
        data = response.get("data", [])
        all_items.extend(data)

        meta = response.get("meta", {})
        has_more = meta.get("hasMore", False)
        cursor = meta.get("cursor")

        iteration += 1
        print(f"Fetched batch {iteration} ({len(data)} items, hasMore={has_more})")

        if not has_more or not cursor:
            break
        if max_iterations and iteration >= max_iterations:
            print(f"Stopped at max_iterations={max_iterations}")
            break

    print(f"Total: {len(all_items)} items")
    return all_items


def iter_pages(
    endpoint: str,
    params: Optional[dict] = None,
    limit: int = 100
) -> Generator[list, None, None]:
    """Generator that yields pages of items (page-based pagination).

    Use this for memory-efficient processing of large datasets.

    Usage:
        for page_data in iter_pages("/traces"):
            for trace in page_data:
                process(trace)
    """
    client = get_client()
    page = 1
    params = params or {}

    while True:
        params["page"] = page
        params["limit"] = min(limit, 100)

        response = client.get(endpoint, params=params)
        data = response.get("data", [])

        if data:
            yield data

        meta = response.get("meta", {})
        total_pages = meta.get("totalPages", 1)

        if page >= total_pages:
            break
        page += 1


def iter_cursor(
    endpoint: str,
    params: Optional[dict] = None,
    limit: int = 100
) -> Generator[list, None, None]:
    """Generator that yields batches of items (cursor-based pagination).

    Use this for memory-efficient processing of large datasets.

    Usage:
        for batch in iter_cursor("/v2/scores"):
            for score in batch:
                process(score)
    """
    client = get_client()
    cursor = None
    params = params or {}

    while True:
        params["limit"] = min(limit, 100)
        if cursor:
            params["cursor"] = cursor
        elif "cursor" in params:
            del params["cursor"]

        response = client.get(endpoint, params=params)
        data = response.get("data", [])

        if data:
            yield data

        meta = response.get("meta", {})
        has_more = meta.get("hasMore", False)
        cursor = meta.get("cursor")

        if not has_more or not cursor:
            break


if __name__ == "__main__":
    # Quick test
    print("Testing page-based pagination (traces)...")
    traces = fetch_all_pages("/traces", limit=10, max_pages=2)
    print(f"Got {len(traces)} traces\n")

    print("Testing cursor-based pagination (scores)...")
    scores = fetch_all_cursor("/v2/scores", limit=10, max_iterations=2)
    print(f"Got {len(scores)} scores")
