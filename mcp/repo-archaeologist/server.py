"""Repo Archaeologist — an MCP server exposing deterministic code-analysis tools.

This is a thin protocol adapter: every tool just delegates to a pure, tested
analyzer in analyzers/. No logic lives here, which is exactly the point — the
facts layer is already built and tested; the server only speaks MCP.

Run as a stdio MCP server:  python server.py
"""
from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from analyzers import history, modules, symbols

mcp = FastMCP("repo-archaeologist")


@mcp.tool()
def find_symbol(name: str, path: str = ".") -> list[dict]:
    """Find every definition of a function/class/method named `name` under `path`.

    Returns a list of {name, kind, file, lineno, parent}. `path` may be a file or
    a directory (scanned recursively, skipping venvs and caches).
    """
    return symbols.find_symbol(name, path)


@mcp.tool()
def list_symbols(path: str = ".") -> list[dict]:
    """List all top-level functions/classes (and their methods) under `path`."""
    return symbols.list_symbols(path)


@mcp.tool()
def summarize_module(path: str) -> dict:
    """Summarize one Python module's structure: docstring, imports, classes, functions."""
    return modules.summarize_module(path)


@mcp.tool()
def git_blame_story(file: str, repo: str = ".") -> dict:
    """Summarize a file's git history: commit count, authors, first/last touch.

    `file` is relative to `repo` (the git repository root).
    """
    return history.git_blame_story(repo, file)


@mcp.tool()
def explain_commit_range(base: str, head: str, repo: str = ".") -> dict:
    """Summarize commits and changed files between two git refs (base..head)."""
    return history.explain_commit_range(repo, base, head)


def main() -> None:
    mcp.run()  # stdio transport by default


if __name__ == "__main__":
    main()
