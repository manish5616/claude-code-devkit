# claude-code-devkit

A Claude Code plugin for **codebase archaeology** — explore and document any Python
repo through a custom MCP server, a driving sub-agent, and a slash command.

> ⚠️ Work in progress — built phase by phase as a learning project.
> See [`ROADMAP.md`](./ROADMAP.md) for the full plan and progress tracker.

## What it will do

- **Repo Archaeologist MCP server** (Python, stdio) — deterministic code-analysis
  tools: `find_symbol`, `list_symbols`, `summarize_module`, `git_blame_story`,
  `explain_commit_range`.
- **`/map-repo`** slash command + **`onboarding-guide`** sub-agent — drive the
  tools to auto-generate architecture / onboarding docs.
- **Hooks** — auto-format on edit, guard secret paths.
- **Skill** — `module-summary` for on-demand module explanations.
- Packaged as an installable **plugin** with its own **marketplace**.

## Design principle

The MCP server returns **deterministic facts**; the LLM writes the **prose**.
No LLM calls live inside the server, so it stays testable and works with any MCP
client.

## Status

Early development. Not yet installable.

## License

MIT (see `LICENSE`).
