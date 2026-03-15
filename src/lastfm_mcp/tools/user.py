"""User-related Last.fm tools."""

from lastfm_mcp.client import api_request, format_number, handle_error
from lastfm_mcp.models import RecentTracksInput, UserInput, UserTopInput
from lastfm_mcp.server import mcp


@mcp.tool(
    name="lastfm_get_user_info",
    annotations={
        "title": "Get Last.fm User Info",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def lastfm_get_user_info(params: UserInput) -> str:
    """Get profile information for a Last.fm user.

    Returns user profile data including playcount, registration date,
    country, and profile URL.
    """
    try:
        data = await api_request("user.getinfo", user=params.username)
        user = data["user"]
        registered = user.get("registered", {})
        reg_text = (
            registered.get("#text", "N/A") if isinstance(registered, dict) else str(registered)
        )
        lines = [
            f"# {user.get('name', params.username)}",
            "",
            f"- **Real name**: {user.get('realname', 'N/A')}",
            f"- **Country**: {user.get('country', 'N/A')}",
            f"- **Scrobbles**: {format_number(user.get('playcount', 0))}",
            f"- **Registered**: {reg_text}",
            f"- **Profile**: {user.get('url', 'N/A')}",
        ]
        return "\n".join(lines)
    except Exception as e:
        return handle_error(e)


@mcp.tool(
    name="lastfm_get_recent_tracks",
    annotations={
        "title": "Get Recent Tracks",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    },
)
async def lastfm_get_recent_tracks(params: RecentTracksInput) -> str:
    """Get a user's recently played tracks.

    Returns the most recent scrobbles, including currently playing track if any.
    """
    try:
        data = await api_request(
            "user.getrecenttracks",
            user=params.username,
            limit=params.limit,
            page=params.page,
        )
        tracks = data.get("recenttracks", {}).get("track", [])
        if not tracks:
            return f"No recent tracks found for user '{params.username}'."

        attr = data.get("recenttracks", {}).get("@attr", {})
        lines = [
            f"# Recent Tracks — {params.username}",
            f"Page {attr.get('page', params.page)} of {attr.get('totalPages', '?')} "
            f"({format_number(attr.get('total', '?'))} total scrobbles)",
            "",
        ]
        for i, t in enumerate(tracks, 1):
            now_playing = t.get("@attr", {}).get("nowplaying") == "true"
            artist = t.get("artist", {})
            artist_name = (
                artist.get("#text", artist.get("name", "Unknown"))
                if isinstance(artist, dict)
                else str(artist)
            )
            track_name = t.get("name", "Unknown")
            album = t.get("album", {})
            album_name = (
                album.get("#text", album.get("name", ""))
                if isinstance(album, dict)
                else str(album)
            )

            prefix = "🎵 NOW" if now_playing else f"{i}."
            date_str = ""
            if not now_playing:
                date_info = t.get("date", {})
                date_str = (
                    f" — {date_info.get('#text', '')}" if isinstance(date_info, dict) else ""
                )

            line = f"{prefix} **{artist_name}** — {track_name}"
            if album_name:
                line += f" ({album_name})"
            line += date_str
            lines.append(line)

        return "\n".join(lines)
    except Exception as e:
        return handle_error(e)


@mcp.tool(
    name="lastfm_get_user_top_artists",
    annotations={
        "title": "Get User Top Artists",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def lastfm_get_user_top_artists(params: UserTopInput) -> str:
    """Get a user's top artists for a given time period."""
    try:
        data = await api_request(
            "user.gettopartists",
            user=params.username,
            period=params.period.value,
            limit=params.limit,
            page=params.page,
        )
        artists = data.get("topartists", {}).get("artist", [])
        if not artists:
            return f"No top artists found for '{params.username}' (period: {params.period.value})."

        attr = data.get("topartists", {}).get("@attr", {})
        lines = [
            f"# Top Artists — {params.username} ({params.period.value})",
            f"Page {attr.get('page', params.page)} of {attr.get('totalPages', '?')}",
            "",
        ]
        for a in artists:
            rank = a.get("@attr", {}).get("rank", "?")
            lines.append(
                f"{rank}. **{a.get('name', 'Unknown')}** — "
                f"{format_number(a.get('playcount', 0))} plays"
            )

        return "\n".join(lines)
    except Exception as e:
        return handle_error(e)


@mcp.tool(
    name="lastfm_get_user_top_albums",
    annotations={
        "title": "Get User Top Albums",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def lastfm_get_user_top_albums(params: UserTopInput) -> str:
    """Get a user's top albums for a given time period."""
    try:
        data = await api_request(
            "user.gettopalbums",
            user=params.username,
            period=params.period.value,
            limit=params.limit,
            page=params.page,
        )
        albums = data.get("topalbums", {}).get("album", [])
        if not albums:
            return f"No top albums found for '{params.username}' (period: {params.period.value})."

        attr = data.get("topalbums", {}).get("@attr", {})
        lines = [
            f"# Top Albums — {params.username} ({params.period.value})",
            f"Page {attr.get('page', params.page)} of {attr.get('totalPages', '?')}",
            "",
        ]
        for a in albums:
            rank = a.get("@attr", {}).get("rank", "?")
            artist = a.get("artist", {})
            artist_name = artist.get("name", "Unknown") if isinstance(artist, dict) else str(artist)
            lines.append(
                f"{rank}. **{a.get('name', 'Unknown')}** by {artist_name} — "
                f"{format_number(a.get('playcount', 0))} plays"
            )

        return "\n".join(lines)
    except Exception as e:
        return handle_error(e)


@mcp.tool(
    name="lastfm_get_user_top_tracks",
    annotations={
        "title": "Get User Top Tracks",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def lastfm_get_user_top_tracks(params: UserTopInput) -> str:
    """Get a user's top tracks for a given time period."""
    try:
        data = await api_request(
            "user.gettoptracks",
            user=params.username,
            period=params.period.value,
            limit=params.limit,
            page=params.page,
        )
        tracks = data.get("toptracks", {}).get("track", [])
        if not tracks:
            return f"No top tracks found for '{params.username}' (period: {params.period.value})."

        attr = data.get("toptracks", {}).get("@attr", {})
        lines = [
            f"# Top Tracks — {params.username} ({params.period.value})",
            f"Page {attr.get('page', params.page)} of {attr.get('totalPages', '?')}",
            "",
        ]
        for t in tracks:
            rank = t.get("@attr", {}).get("rank", "?")
            artist = t.get("artist", {})
            artist_name = artist.get("name", "Unknown") if isinstance(artist, dict) else str(artist)
            lines.append(
                f"{rank}. **{artist_name}** — {t.get('name', 'Unknown')} "
                f"({format_number(t.get('playcount', 0))} plays)"
            )

        return "\n".join(lines)
    except Exception as e:
        return handle_error(e)


@mcp.tool(
    name="lastfm_get_user_loved_tracks",
    annotations={
        "title": "Get User Loved Tracks",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def lastfm_get_user_loved_tracks(params: RecentTracksInput) -> str:
    """Get a user's loved (favorited) tracks."""
    try:
        data = await api_request(
            "user.getlovedtracks",
            user=params.username,
            limit=params.limit,
            page=params.page,
        )
        tracks = data.get("lovedtracks", {}).get("track", [])
        if not tracks:
            return f"No loved tracks found for '{params.username}'."

        attr = data.get("lovedtracks", {}).get("@attr", {})
        lines = [
            f"# Loved Tracks — {params.username}",
            f"Page {attr.get('page', params.page)} of {attr.get('totalPages', '?')} "
            f"({format_number(attr.get('total', '?'))} total)",
            "",
        ]
        for i, t in enumerate(tracks, 1):
            artist = t.get("artist", {})
            artist_name = artist.get("name", "Unknown") if isinstance(artist, dict) else str(artist)
            date_info = t.get("date", {})
            date_str = (
                f" — loved {date_info.get('#text', '')}"
                if isinstance(date_info, dict) and date_info.get("#text")
                else ""
            )
            lines.append(f"{i}. **{artist_name}** — {t.get('name', 'Unknown')}{date_str}")

        return "\n".join(lines)
    except Exception as e:
        return handle_error(e)
