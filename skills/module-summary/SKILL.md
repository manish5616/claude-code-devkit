---
name: module-summary
description: >
  Summarize what a Python module does — its purpose, public API, classes,
  functions, and dependencies. Use when the user asks to summarize, explain, or
  document a specific .py file or Python module.
---

# Module Summary

When the user asks you to summarize or explain a Python module/file, do NOT guess
its structure from a quick skim. Extract the facts deterministically, then write
the prose.

## Steps

1. Run the bundled helper to get the module's structure as JSON:

   ```
   python "${CLAUDE_PLUGIN_ROOT}/skills/module-summary/scripts/extract_structure.py" <path-to-file.py>
   ```

   (`${CLAUDE_PLUGIN_ROOT}` is set by Claude Code to this plugin's install
   directory, so the path resolves wherever the plugin is installed.)

2. The helper returns: `module_docstring`, `imports`, `classes` (with methods and
   docstrings), and `functions` (with args and docstrings). Treat this as ground
   truth about the module's shape.

3. Write a clear summary with these sections:
   - **Purpose** — what the module is for (from the docstring + names).
   - **Public API** — the functions/classes a caller would use, with one line each.
   - **Dependencies** — notable imports and what they imply.
   - **Notable patterns** — anything worth flagging (e.g. pure functions, side effects).

Keep it concise and accurate. If the helper returns an `error` field, report it
plainly instead of inventing structure.
