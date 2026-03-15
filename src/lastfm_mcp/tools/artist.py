"""Artist-related Last.fm tools."""

from lastfm_mcp.client import api_request, format_number, format_tags, handle_error
from lastfm_mcp.models import ArtistInput, ArtistTopInput, SimilarInput
from lastfm_mcp.server import mcp


@mcp.tool(
    name="lastfm_get_artist_info",
    annotations={
        "title": "Get Artist Info",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def lastfm_get_artist_info(params: ArtistInput) -> str:
    """Get detailed information about an artist.

    Returns bio, stats, tags, and similar artists.
    """
    try:
        data = await api_request("artist.getinfo", artist=params.artist)
        a = data.get("artist", {})

        stats = a.get("stats", {})
        bio = a.get("bio", {})
        summary = bio.get("summary", "").split("<a href")[0].strip()
        tags = format_tags(a.get("tags", {}))

        similar = a.get("similar", {}).get("artist", [])
        similar_names = (
            ", ".join(s.get("name", "") for s in similar[:5]) if similar else "N/A"
        )

        lines = [
            f"# {a.get('name', params.artist)}",
            "",
            f"- **Listeners**: {format_number(stats.get('listeners', 0))}",
            f"- **Scrobbles**: {format_number(stats.get('playcount', 0))}",
            f"- **Tags**: {tags or 'N/A'}",
            f"- **Similar**: {similar_names}",
            f"- **URL**: {a.get('url', 'N/A')}",
        ]
        if summary:
            lines.extend(["", "## Bio", "", summary])

        return "\n".join(lines)
    except Exception as e:
        return handle_error(e)


@mcp.tool(
    name="lastfm_get_similar_artists",
    annotations={
        "title": "Get Similar Artists",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def lastfm_get_similar_artists(params: SimilarInput) -> str:
    """Get artists similar to the specified artist."""
    try:
        data = await api_request("artist.getsimilar", artist=params.artist, limit=params.limit)
        artists = data.get("similarartists", {}).get("artist", [])
        if not artists:
            return f"No similar artists found for '{params.artist}'."

        lines = [f"# Artists Similar to {params.artist}", ""]
        for a in artists:
            match = float(a.get("match", 0)) * 100
            lines.append(f"- **{a.get('name', 'Unknown')}** ({match:.0f}% match)")

        return "\n".join(lines)
    except Exception as e:
        return handle_error(e)


@mcp.tool(
    name="lastfm_get_artist_top_tracks",
    annotations={
        "title": "Get Artist Top Tracks",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def lastfm_get_artist_top_tracks(params: ArtistTopInput) -> str:
    """Get the top tracks for an artist on Last.fm."""
    try:
        data = await api_request(
            "artist.gettoptracks",
            artist=params.artist,
            limit=params.limit,
            page=params.page,
        )
        tracks = data.get("toptracks", {}).get("track", [])
        if not tracks:
            return f"No top tracks found for '{params.artist}'."

        attr = data.get("toptracks", {}).get("@attr", {})
        lines = [
            f"# Top Tracks — {attr.get('artist', params.artist)}",
            f"Page {attr.get('page', params.page)} of {attr.get('totalPages', '?')}",
            "",
        ]
        for t in tracks:
            rank = t.get("@attr", {}).get("rank", "?")
            lines.append(
                f"{rank}. **{t.get('name', 'Unknown')}** — "
                f"{format_number(t.get('playcount', 0))} plays, "
                f"{format_number(t.get('listeners', 0))} listeners"
            )

        return "\n".join(lines)
    except Exception as e:
        return handle_error(e)


@mcp.tool(
    name="lastfm_get_artist_top_albums",
    annotations={
        "title": "Get Artist Top Albums",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def lastfm_get_artist_top_albums(params: ArtistTopInput) -> str:
    """Get the top albums for an artist on Last.fm."""
    try:
        data = await api_request(
            "artist.gettopalbums",
            artist=params.artist,
            limit=params.limit,
            page=params.page,
        )
        albums = data.get("topalbums", {}).get("album", [])
        if not albums:
            return f"No top albums found for '{params.artist}'."

        attr = data.get("topalbums", {}).get("@attr", {})
        lines = [
            f"# Top Albums — {attr.get('artist', params.artist)}",
            f"Page {attr.get('page', params.page)} of {attr.get('totalPages', '?')}",
            "",
        ]
        for a in albums:
            lines.append(
                f"- **{a.get('name', 'Unknown')}** — "
                f"{format_number(a.get('playcount', 0))} plays"
            )

        return "\n".join(lines)
    except Exception as e:
        return handle_error(e)
