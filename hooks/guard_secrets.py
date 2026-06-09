#!/usr/bin/env python3
"""PreToolUse hook: block edits to secret paths before they happen.

The harness runs this BEFORE an Edit/Write tool call and pipes a JSON event to
stdin. If the target path is a secret (.env or anything under secrets/), we exit
with code 2, which tells Claude Code to BLOCK the tool call; whatever we print to
stderr is fed back to the model as the reason.

This intentionally overlaps the `deny` rule in .claude/settings.json — it's
defense-in-depth, and the clearest way to demonstrate the PreToolUse blocking
contract (exit code 2 + stderr reason).
"""
import json
import os
import sys


def is_secret(path: str) -> bool:
    norm = path.replace("\\", "/").lower()
    base = os.path.basename(norm)
    if base == ".env" or norm.endswith("/.env"):
        return True
    if norm.startswith("secrets/") or "/secrets/" in norm:
        return True
    return False


def main() -> int:
    try:
        event = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0

    path = (event.get("tool_input") or {}).get("file_path") or ""
    if path and is_secret(path):
        print(
            f"Blocked by project hook: edits to secret paths are not allowed ({path}).",
            file=sys.stderr,
        )
        return 2  # exit 2 => block the tool call
    return 0


if __name__ == "__main__":
    sys.exit(main())
