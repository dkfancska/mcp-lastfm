#!/usr/bin/env python3
"""MCP Server for the Last.fm API.

Provides tools to interact with Last.fm: user profiles, listening history,
top charts, search, and artist/album/track metadata.
"""

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("lastfm_mcp")


def main():
    """Entry point for the MCP server."""
    import lastfm_mcp.tools  # noqa: F401 — registers all tools on `mcp`

    mcp.run()


if __name__ == "__main__":
    main()
