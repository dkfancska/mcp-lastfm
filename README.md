# lastfm-mcp

MCP server for the [Last.fm API](https://www.last.fm/api). Enables LLM agents to access music data: user profiles, listening history, top charts, search, and artist/album/track metadata.

## Prerequisites

- Python 3.10+
- [Last.fm API key](https://www.last.fm/api/account/create) (free)

## Installation

### Using uv (recommended)

No installation required — runs directly:

```bash
uv run --with lastfm-mcp --python 3.10 lastfm-mcp
```

### Using pip

```bash
pip install lastfm-mcp
```

Then run:

```bash
lastfm-mcp
```

## Configuration

### Claude Desktop

Add to your `claude_desktop_config.json`:

- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%/Claude/claude_desktop_config.json`

#### Using uv

```json
{
  "mcpServers": {
    "lastfm": {
      "command": "uv",
      "args": ["run", "--with", "lastfm-mcp", "--python", "3.10", "lastfm-mcp"],
      "env": {
        "LASTFM_API_KEY": "your_api_key"
      }
    }
  }
}
```

> **Note:** You may need to replace `uv` with the full path to the executable. Find it with `which uv` (macOS/Linux) or `where uv` (Windows).

#### Using pip

```json
{
  "mcpServers": {
    "lastfm": {
      "command": "lastfm-mcp",
      "env": {
        "LASTFM_API_KEY": "your_api_key"
      }
    }
  }
}
```

### Cursor

Add to `.cursor/mcp.json` in your project root:

```json
{
  "mcpServers": {
    "lastfm": {
      "command": "uv",
      "args": ["run", "--with", "lastfm-mcp", "--python", "3.10", "lastfm-mcp"],
      "env": {
        "LASTFM_API_KEY": "your_api_key"
      }
    }
  }
}
```

### Claude Code

```bash
claude mcp add lastfm -- uv run --with lastfm-mcp --python 3.10 lastfm-mcp
```

Make sure `LASTFM_API_KEY` is set in your environment.

## Tools

### User

| Tool | Description |
|---|---|
| `lastfm_get_user_info` | User profile: country, scrobble count, registration date |
| `lastfm_get_recent_tracks` | Recently played tracks (including now playing) |
| `lastfm_get_user_top_artists` | Top artists for a time period |
| `lastfm_get_user_top_albums` | Top albums for a time period |
| `lastfm_get_user_top_tracks` | Top tracks for a time period |
| `lastfm_get_user_loved_tracks` | Loved (favorited) tracks |

### Search

| Tool | Description |
|---|---|
| `lastfm_search_artist` | Search artists by name |
| `lastfm_search_album` | Search albums by name |
| `lastfm_search_track` | Search tracks by name |

### Artist

| Tool | Description |
|---|---|
| `lastfm_get_artist_info` | Artist details: bio, tags, stats |
| `lastfm_get_similar_artists` | Similar artists |
| `lastfm_get_artist_top_tracks` | Artist's top tracks |
| `lastfm_get_artist_top_albums` | Artist's top albums |

### Album

| Tool | Description |
|---|---|
| `lastfm_get_album_info` | Album details: tracklist, tags, description |

### Track

| Tool | Description |
|---|---|
| `lastfm_get_track_info` | Track details: duration, tags, stats |
| `lastfm_get_similar_tracks` | Similar tracks |

## Parameters

Top chart tools support a `period` parameter:

| Value | Period |
|---|---|
| `overall` | All time (default) |
| `7day` | Last 7 days |
| `1month` | Last month |
| `3month` | Last 3 months |
| `6month` | Last 6 months |
| `12month` | Last year |

All list tools support pagination via `limit` and `page`.

## Project Structure

```
src/lastfm_mcp/
├── server.py       # Entry point, FastMCP initialization
├── client.py       # HTTP client, error handling, formatting
├── models.py       # Pydantic models and enums
└── tools/
    ├── user.py     # User profile and listening tools
    ├── search.py   # Artist, album, track search
    ├── artist.py   # Artist info and top charts
    ├── album.py    # Album info
    └── track.py    # Track info and similar tracks
```

## License

MIT
