---
description: Generate an architecture overview of the current repository
argument-hint: "[subdirectory to focus on, optional]"
allowed-tools: Glob, Read, mcp__repo-archaeologist__list_symbols, mcp__repo-archaeologist__summarize_module
---

Produce a concise **architecture overview** of the repository in the current
working directory.

Focus area (optional): $ARGUMENTS

How to gather the facts (do this quietly — do not narrate these steps):

1. Use `Glob` (e.g. `**/*.py`, plus top-level config files) to see the layout.
2. For Python repos, call the `repo-archaeologist` MCP tools as ground truth:
   - `list_symbols` with `path` set to the repository's absolute root, to inventory
     functions/classes.
   - `summarize_module` on the 3-5 most important files.
3. Read key config files (pyproject.toml, package.json, README) only as needed.

Then write the overview from those facts:

1. **Purpose** — what this project is, in 2-3 sentences.
2. **Structure** — the main directories and what each is responsible for.
3. **Entry points** — where execution / the main flow starts.
4. **Key modules** — the 3-5 most important files and their roles.
5. **How to run / test** — inferred from config files.

Keep it tight and skimmable, written for a new reader. Output **only** the overview —
do not describe your tool calls or working directory.
