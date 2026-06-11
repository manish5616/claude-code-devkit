# Claude Code — Complete Learning Roadmap

A start-to-finish course covering **every** topic in Claude Code, paired with one
hands-on project (`claude-code-devkit`, centered on the **Repo Archaeologist** MCP
server) so you learn each concept by building it.

- **Learn column** = read + understand (the syllabus).
- **Build column** = the piece of the project you create for that topic.
- A few topics are *learn-only* (you don't need to build them for a portfolio).

> How to use this file: go phase by phase. For each phase, read the concept and
> official docs, then build the matching project piece. Check the box when the
> "Done when…" condition is true. Commit after every phase.

---

## Table of contents

- [Phase 0 — Foundations](#phase-0--foundations)
- [Phase 1 — Context & Memory](#phase-1--context--memory)
- [Phase 2 — Configuration & Permissions](#phase-2--configuration--permissions)
- [Phase 3 — Slash Commands](#phase-3--slash-commands)
- [Phase 4 — Hooks](#phase-4--hooks)
- [Phase 5 — Subagents](#phase-5--subagents)
- [Phase 6 — Skills](#phase-6--skills)
- [Phase 7 — MCP: Using servers](#phase-7--mcp-using-servers)
- [Phase 8 — MCP: Building the Repo Archaeologist server](#phase-8--mcp-building-the-repo-archaeologist-server)
- [Phase 9 — Plugins & Marketplaces](#phase-9--plugins--marketplaces)
- [Phase 10 — Headless, SDK & CI (learn-only-ish)](#phase-10--headless-sdk--ci)
- [Phase 11 — Capstone & Publishing](#phase-11--capstone--publishing)
- [Reference links](#reference-links)

---

## Phase 0 — Foundations

**Concept.** The core loop: you ask → Claude reads/edits files and runs tools →
you approve. Permission modes (ask / plan / auto). Interactive shell: `!cmd` to
run a shell command, `@file` to reference a file. Essential built-ins: `/help`,
`/clear`, `/config`, `/model`, `/cost`, `/init`, plan mode (Shift+Tab).

**Build.** Decide the repo lives at `Documents/claude-code-devkit`. Run `claude`
inside it, try `/init`, make one trivial edit to confirm the loop.

**Done when…** you can explain what plan mode does and have made one approved edit.

- [ ] Read the Quickstart + CLI overview
- [ ] Made a first edit via the approve loop

---

## Phase 1 — Context & Memory

**Concept.** `CLAUDE.md` is project memory. Hierarchy: enterprise → user
(`~/.claude/CLAUDE.md`) → project (`./CLAUDE.md`) → subdirectory. The `#`
shortcut appends a memory mid-session. Put conventions, build/test commands, and
gotchas in it; keep it short and factual.

**Build.** Write the project's own `CLAUDE.md`: Python style, how to run tests
(`pytest`), the "server returns facts, the LLM writes prose" design rule.

**Done when…** the repo has a `CLAUDE.md` that would make a fresh Claude session
follow your conventions without being told.

- [ ] Understand the memory hierarchy
- [ ] `CLAUDE.md` written and committed

---

## Phase 2 — Configuration & Permissions

**Concept.** `settings.json` layers: user (`~/.claude/settings.json`), project
(`.claude/settings.json`), local (`.claude/settings.local.json`, gitignored).
`permissions` allow/deny/ask rules (e.g. allow `Bash(pytest:*)`, deny reads of
`.env`). Env vars, model selection, output styles.

**Build.** Add `.claude/settings.json` allowing `Bash(pytest:*)`,
`Bash(git status:*)`, etc., and denying reads of `.env`/`secrets/`.

**Done when…** running tests no longer prompts, but editing `.env` is blocked.

- [ ] Understand the three settings layers
- [ ] Project `settings.json` with a sane allowlist

---

## Phase 3 — Slash Commands

**Concept.** Custom commands live in `.claude/commands/*.md` (project) or
`~/.claude/commands/`. Frontmatter: `description`, `argument-hint`,
`allowed-tools`, `model`. Use `$ARGUMENTS`, `$1`, `$2`; `!cmd` embeds shell
output; `@file` embeds a file.

**Build.** First version of `/map-repo` — a command that asks Claude to produce
an architecture overview of the current repo (later it will drive the MCP tools).

**Done when…** typing `/map-repo` in any project produces a structured overview.

- [ ] Command frontmatter understood
- [ ] `/map-repo` command authored

---

## Phase 4 — Hooks

**Concept.** Hooks are shell commands the **harness** runs on events:
`PreToolUse`, `PostToolUse`, `UserPromptSubmit`, `Stop`, `SessionStart`, etc.
Each receives JSON on stdin and can allow/block via exit code or JSON output.
This is how you get *deterministic* automation (not "please remember to…").

**Build.** A `PostToolUse` hook that runs `ruff format` on any Python file Claude
edits, and a `PreToolUse` hook that blocks edits to `secrets/`.

**Done when…** editing a `.py` file auto-formats it; editing `secrets/x` is blocked.

- [ ] Understand the stdin-JSON / exit-code contract
- [ ] Format hook + guard hook working

---

## Phase 5 — Subagents

**Concept.** Subagents live in `.claude/agents/*.md` with frontmatter (`name`,
`description`, `tools`, `model`). The `description` drives automatic delegation.
Restrict `tools` for safety. Use them to isolate context and parallelize.

**Build.** The `onboarding-guide` subagent: given a repo, it calls the Repo
Archaeologist tools and assembles an onboarding doc — in its own context window.

**Done when…** the subagent can be invoked and returns an onboarding summary.

- [ ] Agent frontmatter + tool restriction understood
- [ ] `onboarding-guide` agent authored

---

## Phase 6 — Skills

**Concept.** A Skill = a folder with `SKILL.md` (name + description +
instructions) plus optional scripts/resources. **Progressive disclosure**: only
the name/description load until the skill is triggered, then the body loads.
Skills are *model-invoked* (Claude chooses them); commands are *user-invoked*.

**Build.** A `module-summary` skill: bundles a tiny Python helper that extracts a
module's structure and instructions for turning it into a readable summary.

**Done when…** asking "summarize this module" triggers the skill and its helper.

- [ ] Skills vs. commands vs. subagents clear
- [ ] `module-summary` skill authored

---

## Phase 7 — MCP: Using servers

**Concept.** MCP (Model Context Protocol) is the open standard exposing **tools**,
**resources**, and **prompts** to AI clients. Add servers with `claude mcp add`;
transports: **stdio**, **SSE**, **HTTP**; scopes: local/project/user. Share via
`.mcp.json`. Manage with `/mcp`; reference resources with `@server:resource`.

**Build.** Add an existing public MCP server (e.g. a filesystem or fetch server)
to the project and call it, so you understand the *client* side before writing a
*server*.

**Done when…** `/mcp` lists a server and Claude successfully calls one of its tools.

- [ ] Understand tools vs. resources vs. prompts
- [ ] Used a third-party MCP server from Claude Code

---

## Phase 8 — MCP: Building the Repo Archaeologist server ⭐

**The centerpiece.** A standalone **Python** MCP server (stdio) that analyzes
Python codebases. Core design rule: **the server returns deterministic facts; the
LLM writes the prose.** No LLM calls inside the server → it stays testable and
works with any MCP client.

**Stack.** Python `mcp` SDK + stdlib `ast` + `git`. No tree-sitter in v1
(multi-language is a documented "v2" item).

**v1 tools.**
- `find_symbol(name)` → locations (file + lineno) of matching `def`/`class`.
- `list_symbols(path)` → all top-level symbols in a module/package.
- `summarize_module(path)` → structured: classes, functions, docstrings, imports.
- `git_blame_story(path)` → authors, churn, age, hotspots from git history.
- `explain_commit_range(base, head)` → structured diff summary.

**v1.1 (after v1 ships, documented as best-effort).**
- `trace_callers(symbol)` → AST scan of call sites (no dynamic dispatch — say so).
- `detect_dead_code()` → heuristic unused symbols/imports (candidates, not truth).

**Build order.**
1. `analyzers/symbols.py` + pytest (pure logic, no MCP yet).
2. `analyzers/modules.py`, `analyzers/history.py` + tests.
3. `server.py` — wrap analyzers as MCP tools with JSON-schema inputs.
4. Test with the **MCP Inspector**, then register in Claude Code.

**Done when…** the server passes its tests and Claude can call all five v1 tools.

- [ ] `analyzers/` modules with passing pytest
- [ ] `server.py` exposing 5 tools over stdio
- [ ] Verified in MCP Inspector + registered in Claude Code

---

## Phase 9 — Plugins & Marketplaces

**Concept.** A plugin bundles commands, skills, agents, hooks, and MCP servers
under a `plugin.json` manifest. A `marketplace.json` (a git repo) lists
installable plugins. Users run `claude plugin marketplace add <repo>` then
`claude plugin install <name>`.

**Build.** `plugin.json` binding the commands/skill/agent/hooks/MCP server
together; `marketplace.json` so the repo is installable. Test a clean install.

**Done when…** you can install your plugin from the repo into a fresh session.

- [ ] `plugin.json` manifest complete
- [ ] `marketplace.json` published; clean install verified

---

## Phase 10 — Headless, SDK & CI

*(Mostly learn-only — optional to build, great as a README "future work" note.)*

**Concept.** Headless: `claude -p "prompt" --output-format stream-json
--allowedTools …`. The **Claude Agent SDK** (Python/TS) builds custom agents on
the same engine. CI/CD: run Claude Code in GitHub Actions for automated review.

**Build (optional).** A GitHub Action that runs `/map-repo` on push and commits
the generated architecture doc.

**Done when…** you can explain headless mode and the SDK's role (build optional).

- [ ] Understand headless flags
- [ ] (Optional) CI workflow that runs the plugin

---

## Phase 11 — Capstone & Publishing

**Goal.** Turn the repo into the resume artifact.

- Polished `README.md`: what it does, GIF/screenshots, install steps, **honest
  limitations** (Python-only, heuristic dead-code), and a v2 roadmap.
- Tests green in CI; a `LICENSE` (MIT); clean commit history.
- Publish the marketplace; write a short blog post / LinkedIn note linking it.

**Résumé line it supports:**
> Designed and shipped an open-source Claude Code plugin featuring a custom Python
> MCP server (code-analysis tools over stdio), a driving sub-agent and slash
> command, automated hooks, and a published plugin marketplace.

- [ ] README with screenshots + honest limitations
- [ ] CI green, LICENSE, tagged release
- [ ] Marketplace published + write-up

---

## Reference links

- Claude Code docs: https://docs.claude.com/en/docs/claude-code
- Subagents, Hooks, Skills, MCP, Plugins: see the corresponding pages in the docs
- Model Context Protocol (spec + Python SDK): https://modelcontextprotocol.io
- Claude Agent SDK: the "Agent SDK" section of the docs

---

## Progress tracker

| Phase | Topic | Status |
|------:|-------|:------:|
| 0 | Foundations | ✅ |
| 1 | Context & Memory | ✅ |
| 2 | Config & Permissions | ✅ |
| 3 | Slash Commands | ✅ |
| 4 | Hooks | ✅ |
| 5 | Subagents | ✅ |
| 6 | Skills | ✅ |
| 7 | MCP: Using | ✅ |
| 8 | MCP: Building ⭐ | ✅ |
| 9 | Plugins & Marketplace | ✅ |
| 10 | Headless / SDK / CI | ◐ CI built; headless & SDK are learn-only |
| 11 | Capstone & Publishing | ✅ |
