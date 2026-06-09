"""Module structure analysis via the stdlib `ast` module.

Single Python file in -> one structured dict out (docstring, imports, classes
with methods, functions). This is the "promoted", analyzer-grade version of the
helper bundled with the module-summary skill: same idea, but part of the server's
tested core.
"""
from __future__ import annotations

import ast
from pathlib import Path


def _arg_names(node: ast.FunctionDef | ast.AsyncFunctionDef) -> list[str]:
    return [a.arg for a in node.args.args]


def _func_info(node: ast.FunctionDef | ast.AsyncFunctionDef) -> dict:
    return {
        "name": node.name,
        "lineno": node.lineno,
        "args": _arg_names(node),
        "docstring": ast.get_docstring(node),
    }


def summarize_module(path: str | Path) -> dict:
    """Return the top-level structure of a single Python module as a dict."""
    source = Path(path).read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(path))

    imports: list[str] = []
    classes: list[dict] = []
    functions: list[dict] = []

    for node in tree.body:
        if isinstance(node, ast.Import):
            imports.extend(a.name for a in node.names)
        elif isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            imports.extend(f"{mod}.{a.name}" if mod else a.name for a in node.names)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            functions.append(_func_info(node))
        elif isinstance(node, ast.ClassDef):
            methods = [
                _func_info(n)
                for n in node.body
                if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
            ]
            classes.append(
                {
                    "name": node.name,
                    "lineno": node.lineno,
                    "docstring": ast.get_docstring(node),
                    "methods": methods,
                }
            )

    return {
        "file": str(path),
        "module_docstring": ast.get_docstring(tree),
        "imports": imports,
        "classes": classes,
        "functions": functions,
    }
