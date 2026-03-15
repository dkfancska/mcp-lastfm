"""Track-related Last.fm tools."""

from lastfm_mcp.client import api_request, format_number, format_tags, handle_error
from lastfm_mcp.models import TrackInput
from lastfm_mcp.server import mcp


@mcp.tool(
    name="lastfm_get_track_info",
    annotations={
        "title": "Get Track Info",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def lastfm_get_track_info(params: TrackInput) -> str:
    """Get detailed information about a track.

    Returns listener stats, tags, album info, and wiki summary.
    """
    try:
        data = await api_request("track.getinfo", artist=params.artist, track=params.track)
        t = data.get("track", {})

        tags = format_tags(t.get("toptags", {}))
        wiki = t.get("wiki", {})
        summary = wiki.get("summary", "").split("<a href")[0].strip()

        album = t.get("album", {})
        album_name = album.get("title", "") if isinstance(album, dict) else ""

        duration_ms = int(t.get("duration", 0))
        duration_s = duration_ms // 1000 if duration_ms > 1000 else duration_ms
        dur_str = f"{duration_s // 60}:{duration_s % 60:02d}" if duration_s else "N/A"

        artist = t.get("artist", {})
        artist_name = artist.get("name", params.artist) if isinstance(artist, dict) else str(artist)

        lines = [
            f"# {t.get('name', params.track)}",
            f"**by {artist_name}**",
            "",
            f"- **Album**: {album_name or 'N/A'}",
            f"- **Duration**: {dur_str}",
            f"- **Listeners**: {format_number(t.get('listeners', 0))}",
            f"- **Scrobbles**: {format_number(t.get('playcount', 0))}",
            f"- **Tags**: {tags or 'N/A'}",
            f"- **URL**: {t.get('url', 'N/A')}",
        ]

        if summary:
            lines.extend(["", "## About", "", summary])

        return "\n".join(lines)
    except Exception as e:
        return handle_error(e)


@mcp.tool(
    name="lastfm_get_similar_tracks",
    annotations={
        "title": "Get Similar Tracks",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def lastfm_get_similar_tracks(params: TrackInput) -> str:
    """Get tracks similar to the specified track."""
    try:
        data = await api_request(
            "track.getsimilar", artist=params.artist, track=params.track, limit=20
        )
        tracks = data.get("similartracks", {}).get("track", [])
        if not tracks:
            return f"No similar tracks found for '{params.artist} — {params.track}'."

        lines = [f"# Tracks Similar to {params.artist} — {params.track}", ""]
        for t in tracks:
            artist = t.get("artist", {})
            artist_name = (
                artist.get("name", "Unknown") if isinstance(artist, dict) else str(artist)
            )
            match = float(t.get("match", 0)) * 100
            lines.append(
                f"- **{artist_name}** — {t.get('name', 'Unknown')} ({match:.0f}% match)"
            )

        return "\n".join(lines)
    except Exception as e:
        return handle_error(e)
