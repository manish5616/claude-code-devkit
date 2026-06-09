#!/usr/bin/env python3
"""Extract the structure of a Python module as JSON (deterministic, no LLM).

Usage: python extract_structure.py <path-to-.py>

Bundled helper for the `module-summary` skill. It is also a preview of the AST
work in the Repo Archaeologist MCP server (Phase 8): facts in, plain JSON out,
zero network/LLM calls.
"""
import ast
import json
import sys


def _arg_names(node: ast.FunctionDef | ast.AsyncFunctionDef) -> list[str]:
    return [a.arg for a in node.args.args]


def extract(source: str, filename: str = "<module>") -> dict:
    """Parse Python source and return its top-level structure as a plain dict."""
    tree = ast.parse(source, filename=filename)
    imports: list[str] = []
    classes: list[dict] = []
    functions: list[dict] = []

    for node in tree.body:
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            imports.extend(
                f"{mod}.{alias.name}" if mod else alias.name for alias in node.names
            )
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            functions.append(
                {
                    "name": node.name,
                    "lineno": node.lineno,
                    "args": _arg_names(node),
                    "docstring": ast.get_docstring(node),
                }
            )
        elif isinstance(node, ast.ClassDef):
            methods = [
                {
                    "name": n.name,
                    "lineno": n.lineno,
                    "args": _arg_names(n),
                    "docstring": ast.get_docstring(n),
                }
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
        "module_docstring": ast.get_docstring(tree),
        "imports": imports,
        "classes": classes,
        "functions": functions,
    }


def main() -> int:
    if len(sys.argv) != 2:
        print(json.dumps({"error": "usage: extract_structure.py <path.py>"}))
        return 2
    path = sys.argv[1]
    try:
        with open(path, encoding="utf-8") as f:
            source = f.read()
    except OSError as e:
        print(json.dumps({"error": f"cannot read {path}: {e}"}))
        return 1
    try:
        result = extract(source, path)
    except SyntaxError as e:
        print(json.dumps({"error": f"syntax error in {path}: {e}"}))
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
