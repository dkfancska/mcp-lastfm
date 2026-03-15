"""Search tools for Last.fm."""

from lastfm_mcp.client import api_request, format_number, handle_error
from lastfm_mcp.models import SearchInput
from lastfm_mcp.server import mcp


@mcp.tool(
    name="lastfm_search_artist",
    annotations={
        "title": "Search Artists",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def lastfm_search_artist(params: SearchInput) -> str:
    """Search for artists on Last.fm by name."""
    try:
        data = await api_request(
            "artist.search", artist=params.query, limit=params.limit, page=params.page
        )
        matches = data.get("results", {}).get("artistmatches", {}).get("artist", [])
        if not matches:
            return f"No artists found for '{params.query}'."

        total = data.get("results", {}).get("opensearch:totalResults", "?")
        lines = [
            f"# Artist Search: '{params.query}'",
            f"{format_number(total)} results found",
            "",
        ]
        for a in matches:
            lines.append(
                f"- **{a.get('name', 'Unknown')}** — "
                f"{format_number(a.get('listeners', 0))} listeners"
            )

        return "\n".join(lines)
    except Exception as e:
        return handle_error(e)


@mcp.tool(
    name="lastfm_search_album",
    annotations={
        "title": "Search Albums",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def lastfm_search_album(params: SearchInput) -> str:
    """Search for albums on Last.fm by name."""
    try:
        data = await api_request(
            "album.search", album=params.query, limit=params.limit, page=params.page
        )
        matches = data.get("results", {}).get("albummatches", {}).get("album", [])
        if not matches:
            return f"No albums found for '{params.query}'."

        total = data.get("results", {}).get("opensearch:totalResults", "?")
        lines = [
            f"# Album Search: '{params.query}'",
            f"{format_number(total)} results found",
            "",
        ]
        for a in matches:
            lines.append(f"- **{a.get('name', 'Unknown')}** by {a.get('artist', 'Unknown')}")

        return "\n".join(lines)
    except Exception as e:
        return handle_error(e)


@mcp.tool(
    name="lastfm_search_track",
    annotations={
        "title": "Search Tracks",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def lastfm_search_track(params: SearchInput) -> str:
    """Search for tracks on Last.fm by name."""
    try:
        data = await api_request(
            "track.search", track=params.query, limit=params.limit, page=params.page
        )
        matches = data.get("results", {}).get("trackmatches", {}).get("track", [])
        if not matches:
            return f"No tracks found for '{params.query}'."

        total = data.get("results", {}).get("opensearch:totalResults", "?")
        lines = [
            f"# Track Search: '{params.query}'",
            f"{format_number(total)} results found",
            "",
        ]
        for t in matches:
            lines.append(
                f"- **{t.get('artist', 'Unknown')}** — {t.get('name', 'Unknown')} "
                f"({format_number(t.get('listeners', 0))} listeners)"
            )

        return "\n".join(lines)
    except Exception as e:
        return handle_error(e)
