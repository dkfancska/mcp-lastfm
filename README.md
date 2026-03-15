# Last.fm MCP Server

[![PyPI - Version](https://img.shields.io/pypi/v/lastfm-mcp)](https://pypi.org/project/lastfm-mcp)

An MCP server for the [Last.fm API](https://www.last.fm/api). Enables LLM agents to access music data: user profiles, listening history, top charts, search, and artist/album/track metadata.

## Features

### User Tools

* `lastfm_get_user_info` — User profile: country, scrobble count, registration date.
* `lastfm_get_recent_tracks` — Recently played tracks (including now playing).
* `lastfm_get_user_top_artists` — Top artists for a time period.
* `lastfm_get_user_top_albums` — Top albums for a time period.
* `lastfm_get_user_top_tracks` — Top tracks for a time period.
* `lastfm_get_user_loved_tracks` — Loved (favorited) tracks.

### Search Tools

* `lastfm_search_artist` — Search artists by name.
* `lastfm_search_album` — Search albums by name.
* `lastfm_search_track` — Search tracks by name.

### Artist Tools

* `lastfm_get_artist_info` — Artist details: bio, tags, listener/scrobble stats, similar artists.
* `lastfm_get_similar_artists` — Similar artists with match scores.
* `lastfm_get_artist_top_tracks` — Artist's top tracks.
* `lastfm_get_artist_top_albums` — Artist's top albums.

### Album Tools

* `lastfm_get_album_info` — Album details: tracklist, tags, description.

### Track Tools

* `lastfm_get_track_info` — Track details: duration, tags, listener/scrobble stats.
* `lastfm_get_similar_tracks` — Similar tracks with match scores.

## Configuration

You will need a Last.fm API key. Get one for free at [last.fm/api/account/create](https://www.last.fm/api/account/create).

### Claude Desktop

1. Open the Claude Desktop configuration file located at:
   * On macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   * On Windows: `%APPDATA%/Claude/claude_desktop_config.json`

2. Add the following:

```json
{
  "mcpServers": {
    "lastfm": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "lastfm-mcp",
        "--python",
        "3.10",
        "lastfm-mcp"
      ],
      "env": {
        "LASTFM_API_KEY": "<your-api-key>"
      }
    }
  }
}
```

3. Locate the command entry for `uv` and replace it with the absolute path to the `uv` executable. This ensures that the correct version of `uv` is used when starting the server. On a Mac, you can find this path using `which uv`.

4. Restart Claude Desktop to apply the changes.

### Cursor

Add to `.cursor/mcp.json` in your project root:

```json
{
  "mcpServers": {
    "lastfm": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "lastfm-mcp",
        "--python",
        "3.10",
        "lastfm-mcp"
      ],
      "env": {
        "LASTFM_API_KEY": "<your-api-key>"
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

### Running Without uv (Using System Python)

If you prefer to use the system Python installation instead of uv, you can install the package from PyPI and run it directly:

1. Install the package using pip:
   ```bash
   pip install lastfm-mcp
   ```

2. Update your configuration to use the installed script directly:

```json
{
  "mcpServers": {
    "lastfm": {
      "command": "lastfm-mcp",
      "env": {
        "LASTFM_API_KEY": "<your-api-key>"
      }
    }
  }
}
```

Note: Make sure to use the full path to the `lastfm-mcp` script if it is not in your system PATH. You can find the path using `which lastfm-mcp`.

### Environment Variables

* `LASTFM_API_KEY` (required): Your Last.fm API key.

### Parameters

Top chart tools (`lastfm_get_user_top_artists`, `lastfm_get_user_top_albums`, `lastfm_get_user_top_tracks`) support a `period` parameter:

| Value | Period |
|---|---|
| `overall` | All time (default) |
| `7day` | Last 7 days |
| `1month` | Last month |
| `3month` | Last 3 months |
| `6month` | Last 6 months |
| `12month` | Last year |

All list tools support pagination via `limit` and `page`.

## Development

1. Clone the repository and install dependencies:
   ```bash
   git clone https://github.com/dkfancska/mcp-lastfm.git
   cd mcp-lastfm
   pip install -e .
   ```

2. Copy `.env.example` to `.env` and add your API key:
   ```bash
   cp .env.example .env
   ```

3. For testing with the MCP Inspector:
   ```bash
   npx @modelcontextprotocol/inspector lastfm-mcp
   ```

## License

MIT
