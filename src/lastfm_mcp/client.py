"""Last.fm API client and shared utilities."""

import os
from typing import Any

import httpx

API_BASE_URL = "http://ws.audioscrobbler.com/2.0/"


def _get_api_key() -> str:
    """Get Last.fm API key from environment."""
    key = os.environ.get("LASTFM_API_KEY", "")
    if not key:
        raise ValueError(
            "LASTFM_API_KEY environment variable is not set. "
            "Get a free API key at https://www.last.fm/api/account/create"
        )
    return key


async def api_request(method: str, **params: Any) -> dict:
    """Make a request to the Last.fm API."""
    api_key = _get_api_key()
    request_params = {
        "method": method,
        "api_key": api_key,
        "format": "json",
        **{k: v for k, v in params.items() if v is not None},
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(API_BASE_URL, params=request_params, timeout=30.0)
        response.raise_for_status()
        data = response.json()
        if "error" in data:
            raise ValueError(
                f"Last.fm API error {data['error']}: {data.get('message', 'Unknown error')}"
            )
        return data


def handle_error(e: Exception) -> str:
    """Format errors into actionable messages."""
    if isinstance(e, ValueError):
        return f"Error: {e}"
    if isinstance(e, httpx.HTTPStatusError):
        status: int = e.response.status_code  # type: ignore[union-attr]
        if status == 403:
            return "Error: Invalid API key. Check LASTFM_API_KEY environment variable."
        if status == 429:
            return "Error: Rate limit exceeded. Wait before making more requests."
        return f"Error: API request failed with status {status}."
    if isinstance(e, httpx.TimeoutException):
        return "Error: Request timed out. Try again."
    return f"Error: {type(e).__name__}: {e}"


def format_number(n: str | int) -> str:
    """Format a number with thousands separator."""
    try:
        return f"{int(n):,}"
    except (ValueError, TypeError):
        return str(n)


def format_tags(tags: Any) -> str:
    """Extract tag names from Last.fm tag structures."""
    if not tags:
        return ""
    tag_list = tags if isinstance(tags, list) else tags.get("tag", [])
    if isinstance(tag_list, dict):
        tag_list = [tag_list]
    return ", ".join(t.get("name", "") for t in tag_list if t.get("name"))
