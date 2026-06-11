"""Symbol analysis for Python source, built on the stdlib `ast` module.

Pure functions: a path (file or directory) in, plain list[dict] out. A "symbol"
is a top-level function/class, or a method defined directly inside a class.
"""
from __future__ import annotations

import ast
from collections.abc import Iterator
from dataclasses import asdict, dataclass
from pathlib import Path

# Directories we never want to walk into when scanning a tree.
_SKIP_DIRS = {".venv", "venv", "build", "dist", "__pycache__", ".git"}


@dataclass
class Symbol:
    name: str
    kind: str  # "function" | "class" | "method"
    file: str
    lineno: int
    parent: str | None = None  # enclosing class name, for methods


def _iter_python_files(path: str | Path) -> Iterator[Path]:
    """Yield .py files for a single file path or recursively under a directory."""
    p = Path(path)
    if p.is_file():
        if p.suffix == ".py":
            yield p
        return
    for file in p.rglob("*.py"):
        if _SKIP_DIRS & set(file.parts):
            continue
        yield file


def list_symbols(path: str | Path) -> list[dict]:
    """Return every top-level function/class (and method) defined under `path`.

    Files that can't be parsed (syntax/encoding errors) are skipped, not fatal —
    analysis of a large repo should never crash on one bad file.
    """
    found: list[Symbol] = []
    for file in _iter_python_files(path):
        try:
            tree = ast.parse(file.read_text(encoding="utf-8"), filename=str(file))
        except (SyntaxError, UnicodeDecodeError):
            continue
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                found.append(Symbol(node.name, "function", str(file), node.lineno))
            elif isinstance(node, ast.ClassDef):
                found.append(Symbol(node.name, "class", str(file), node.lineno))
                for sub in node.body:
                    if isinstance(sub, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        found.append(
                            Symbol(sub.name, "method", str(file), sub.lineno, parent=node.name)
                        )
    return [asdict(s) for s in found]


def find_symbol(name: str, path: str | Path) -> list[dict]:
    """Return all definitions of `name` (function/class/method) under `path`."""
    return [s for s in list_symbols(path) if s["name"] == name]
