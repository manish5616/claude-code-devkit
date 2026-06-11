# claude-code-devkit

> A Claude Code plugin for **codebase archaeology** — explore and document any
> Python repository through a custom MCP server, a sub-agent, a slash command,
> a skill, and safety hooks.

![tests](https://github.com/YOUR_GITHUB_USERNAME/claude-code-devkit/actions/workflows/tests.yml/badge.svg)
![license](https://img.shields.io/badge/license-MIT-green)

The centerpiece is **Repo Archaeologist**, a standalone Python **MCP server** that
exposes deterministic code-analysis tools. Claude (or any MCP client) calls them
to answer factual questions about a codebase — then turns those facts into
architecture overviews and onboarding guides.

---

## What it does

Installing this plugin gives Claude Code five new capabilities:

| Capability | Type | What it does |
|---|---|---|
| `/map-repo` | Slash command | Produces an architecture overview of the current repo |
| `onboarding-guide` | Sub-agent | A read-only worker that writes a new-developer onboarding guide |
| `module-summary` | Skill | Auto-summarizes a Python module (bundles an `ast` helper script) |
| **`repo-archaeologist`** | **MCP server** | **5 code-analysis tools (below) — built from scratch in Python** |
| secret-guard / auto-format | Hooks | Blocks edits to secrets; auto-formats Python after edits |

### The Repo Archaeologist MCP tools

| Tool | Returns |
|---|---|
| `find_symbol(name, path)` | Every definition of a function/class/method by name |
| `list_symbols(path)` | All top-level functions/classes (and methods) under a path |
| `summarize_module(path)` | A module's structure: docstring, imports, classes, functions |
| `git_blame_story(repo, file)` | A file's history: commit count, authors, first/last touch |
| `explain_commit_range(repo, base, head)` | Commits and files changed between two refs |

## Design principle

**The server returns deterministic facts; the LLM writes the prose.**

No LLM or network calls live inside the server — every tool is a pure function
over `ast` and `git`. That keeps it fast, fully unit-tested, and usable by any
MCP client (Claude Desktop, Cursor, the MCP Inspector, your own scripts).

## Installation

**Prerequisites:** Python 3.11+, and the `mcp` package on the Python that Claude
Code will use to launch the server:

```bash
python -m pip install mcp
```

Then add the marketplace and install the plugin:

```bash
claude plugin marketplace add YOUR_GITHUB_USERNAME/claude-code-devkit
claude plugin install devkit@devkit-marketplace
```

Restart Claude Code. Verify with `claude mcp list` (look for
`repo-archaeologist ✔ connected`) and `/map-repo`.

## Usage examples

```
/map-repo                       # architecture overview of the current repo
"Summarize the module app.py"   # triggers the module-summary skill
"Use repo-archaeologist to find the symbol Calculator"
"Onboard me to this repository" # delegates to the onboarding-guide sub-agent
```

## Development

```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/claude-code-devkit
cd claude-code-devkit
python -m venv .venv
./.venv/Scripts/python.exe -m pip install -e ".[dev]"   # Windows
# source .venv/bin/activate && pip install -e ".[dev]"  # macOS/Linux
pytest                          # runs the 9 analyzer tests
ruff check .                    # lint
```

> Note: `.venv/` and caches are **excluded** from the published plugin — a plugin
> should ship only what users need, not your local toolchain.

## Limitations (honest)

- **Python-only.** Analysis uses Python's `ast`; other languages aren't parsed.
- **`find_symbol` is name-based** — it won't disambiguate same-named symbols by scope.
- The git tools require `git` on `PATH`.

## Roadmap

- `trace_callers` and `detect_dead_code` (heuristic, best-effort)
- Multi-language support via tree-sitter
- `explain_pr` backed by the GitHub API

See [`ROADMAP.md`](./ROADMAP.md) for the full learning roadmap this project was
built from.

## License

[MIT](./LICENSE) © Manish Kumar
