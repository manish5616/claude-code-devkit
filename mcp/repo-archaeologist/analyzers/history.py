"""Git history analysis. Shells out to `git` and parses output into plain facts.

Takes a repo directory + arguments, returns dicts/lists. No LLM, no network.
Requires `git` on PATH. Raises GitError on any git failure so callers (the MCP
server) can surface a clean message instead of a stack trace.
"""
from __future__ import annotations

import subprocess
from collections import Counter
from pathlib import Path


class GitError(RuntimeError):
    """Raised when a git command fails or git is unavailable."""


def _run_git(repo: str | Path, *args: str) -> str:
    try:
        result = subprocess.run(
            ["git", "-C", str(repo), *args],
            capture_output=True,
            text=True,
            check=True,
        )
    except FileNotFoundError as e:  # git not installed
        raise GitError("git executable not found on PATH") from e
    except subprocess.CalledProcessError as e:
        raise GitError(e.stderr.strip() or f"git {' '.join(args)} failed") from e
    return result.stdout


def git_blame_story(repo: str | Path, file: str) -> dict:
    """Summarize a single file's history: commit count, authors, first/last touch."""
    out = _run_git(
        repo, "log", "--follow", "--format=%H|%an|%ad", "--date=short", "--", file
    )
    commits: list[dict] = []
    authors: Counter[str] = Counter()
    for line in out.splitlines():
        if not line.strip():
            continue
        sha, author, date = line.split("|", 2)
        commits.append({"sha": sha[:10], "author": author, "date": date})
        authors[author] += 1

    return {
        "file": file,
        "commit_count": len(commits),
        "authors": [{"name": a, "commits": n} for a, n in authors.most_common()],
        "first_commit": commits[-1] if commits else None,
        "last_commit": commits[0] if commits else None,
    }


def explain_commit_range(repo: str | Path, base: str, head: str) -> dict:
    """Summarize the commits and files changed between two refs (base..head)."""
    rng = f"{base}..{head}"
    log_out = _run_git(repo, "log", rng, "--format=%H|%an|%s")
    commits = []
    for line in log_out.splitlines():
        if not line.strip():
            continue
        sha, author, subject = line.split("|", 2)
        commits.append({"sha": sha[:10], "author": author, "subject": subject})

    files_out = _run_git(repo, "diff", "--name-only", rng)
    files_changed = [f for f in files_out.splitlines() if f.strip()]

    return {
        "range": rng,
        "commit_count": len(commits),
        "commits": commits,
        "files_changed": files_changed,
    }
