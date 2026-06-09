---
description: Generate an architecture overview of the current repository
argument-hint: "[subdirectory to focus on, optional]"
allowed-tools: Bash(git ls-files:*), Bash(git rev-parse:*), Bash(find:*), Read
---

You are mapping a codebase to produce a concise **architecture overview**.

Working directory: !`pwd`

Repository file list (git-tracked files, or a fallback listing if not a git repo):
!`git ls-files 2>/dev/null || find . -type f -not -path '*/.*' | head -200`

Focus area (optional): $ARGUMENTS

If the file list above is empty or shows an error, tell the user this command must
be run from inside the project directory and stop.

Using the file list above (and reading key files as needed), produce:

1. **Purpose** — what this project is, in 2-3 sentences.
2. **Structure** — the main directories and what each is responsible for.
3. **Entry points** — where execution / the main flow starts.
4. **Key modules** — the 3-5 most important files and their roles.
5. **How to run / test** — inferred from config files.

Keep it tight and skimmable. Prefer a new reader's perspective (onboarding).
