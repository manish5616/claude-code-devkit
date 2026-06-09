#!/usr/bin/env python3
"""PostToolUse hook: auto-format a Python file after Claude edits it.

The Claude Code harness runs this after an Edit/Write tool call and pipes a JSON
event object to stdin. We pull the edited file path out of `tool_input.file_path`
and, if it's a .py file, run `ruff format` on just that file.

Contract: exit 0 always (formatting is best-effort; we never block an edit just
because formatting failed or ruff isn't installed).
"""
import json
import os
import subprocess
import sys


def main() -> int:
    try:
        event = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0  # no/invalid input -> nothing to do

    path = (event.get("tool_input") or {}).get("file_path") or ""
    if not path.endswith(".py") or not os.path.exists(path):
        return 0

    try:
        subprocess.run(["ruff", "format", path], check=False)
    except FileNotFoundError:
        # ruff not installed -> silently skip; formatting is optional.
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
