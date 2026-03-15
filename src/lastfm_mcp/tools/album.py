"""Album-related Last.fm tools."""

from lastfm_mcp.client import api_request, format_number, format_tags, handle_error
from lastfm_mcp.models import AlbumInput
from lastfm_mcp.server import mcp


@mcp.tool(
    name="lastfm_get_album_info",
    annotations={
        "title": "Get Album Info",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def lastfm_get_album_info(params: AlbumInput) -> str:
    """Get detailed information about an album.

    Returns tracklist, tags, listener stats, and wiki summary.
    """
    try:
        data = await api_request("album.getinfo", artist=params.artist, album=params.album)
        a = data.get("album", {})

        tags = format_tags(a.get("tags", {}))
        wiki = a.get("wiki", {})
        summary = wiki.get("summary", "").split("<a href")[0].strip()

        tracks = a.get("tracks", {}).get("track", [])
        if isinstance(tracks, dict):
            tracks = [tracks]

        lines = [
            f"# {a.get('name', params.album)}",
            f"**by {a.get('artist', params.artist)}**",
            "",
            f"- **Listeners**: {format_number(a.get('listeners', 0))}",
            f"- **Scrobbles**: {format_number(a.get('playcount', 0))}",
            f"- **Tags**: {tags or 'N/A'}",
            f"- **URL**: {a.get('url', 'N/A')}",
        ]

        if tracks:
            lines.extend(["", "## Tracklist", ""])
            for t in tracks:
                rank = t.get("@attr", {}).get("rank", "?")
                duration = int(t.get("duration", 0))
                dur_str = f" ({duration // 60}:{duration % 60:02d})" if duration else ""
                lines.append(f"{rank}. {t.get('name', 'Unknown')}{dur_str}")

        if summary:
            lines.extend(["", "## About", "", summary])

        return "\n".join(lines)
    except Exception as e:
        return handle_error(e)
