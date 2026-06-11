# What I built and learned

A plain-language summary of this project.

## What this is
**devkit** is an add-on (plugin) for Claude Code, themed around "codebase
archaeology" — tools that help understand and explain any Python codebase. Install
it once, and Claude gains five new abilities in any project.

## The five pieces, in everyday terms

1. **A shortcut (`/map-repo` command).** Type one word; Claude runs a whole
   pre-written task ("map this codebase").
2. **A specialist helper (`onboarding-guide` sub-agent).** A focused, read-only
   worker that only writes onboarding docs and can't touch files.
3. **An auto-skill (`module-summary`).** A talent Claude reaches for on its own
   when you ask to summarize a file; it runs a small bundled script first.
4. **A real engine I built (the MCP server).** A standalone Python program that
   answers factual questions about code (where is this function? who edited this
   file?). Any AI tool can use it, not just Claude.
5. **Automatic safety rules (hooks).** Guardrails that fire by themselves —
   auto-tidy code after edits, and block edits to secret files.

All five are packaged into one installable bundle with its own marketplace.

## The core idea
**The engine gives facts; the AI writes the words.** The server only returns hard
facts; Claude turns them into readable explanations. Keeping those jobs separate
made the code testable and reliable.

## Lessons that stuck
- Commands run from the folder where you launch Claude.
- Hooks are reliable because the *system* runs them, not because Claude remembers.
- Test the failure paths, not just the happy path (9 tests, including a bad-git case).
- Don't ship your toolbox — excluding `.venv` from the plugin fixed a real install bug.
- Windows + antivirus can lock files mid-rename (the cause of several errors).

## Résumé line this supports
> Designed and published an open-source Claude Code plugin with a custom Python
> MCP server, automated hooks, a sub-agent, and a distributable marketplace.
