# claude-code-devkit — project memory

## What this is
A Claude Code plugin centered on the "Repo Archaeologist" MCP server (Python).
See ROADMAP.md for the phased build plan.

## Core design rule (do not violate)
The MCP server returns DETERMINISTIC FACTS. The LLM writes the PROSE.
Never put LLM/network calls inside the server — it must stay pure and testable.

## Language & tooling
- Python 3.11+, standard library first (ast, subprocess for git).
- No tree-sitter in v1 — Python-only analysis via the stdlib `ast` module.
- Format/lint with ruff. Tests with pytest.

## Commands
- Run tests:    pytest -q
- Format:       ruff format .
- Lint:         ruff check .

## Conventions
- Each analyzer is pure: input paths/strings in, plain dict/list out.
- Every analyzer function gets a unit test against a fixture repo.
- Document limitations honestly (e.g. trace_callers can't resolve dynamic dispatch).
