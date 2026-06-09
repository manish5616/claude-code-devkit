"""Repo Archaeologist analyzers — pure, deterministic code-analysis functions.

Each module here takes paths/strings in and returns plain dicts/lists out.
No LLM calls, no network. This keeps them unit-testable and reusable by any MCP
client. The MCP server (server.py) is only a thin wrapper around these.
"""
