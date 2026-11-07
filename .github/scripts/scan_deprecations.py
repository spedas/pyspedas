#!/usr/bin/env python3
"""List deprecated routines and parameters in the PySPEDAS package, and what each
one still lacks under the breaking-change rules in RULES.md.

A routine is listed when its docstring mentions "deprecat" (any case) or its
code emits a deprecation message. For each one the scan reports:

  docstring   the docstring lines that mention "deprecat"
  warnings    calls that emit a deprecation message: logging calls whose message
              mentions "deprecat", and warnings.warn() calls whose message
              mentions it or whose category is a deprecation warning
  tests       test functions that name the routine, mention "deprecat" in code
              (comments don't count) and check a log or warning (assertLogs,
              assertWarns, warnings.catch_warnings)
  callers     package code outside the routine's own file that still calls a
              routine whose docstring's first line says it is deprecated
  migration   the docs/source/*migration*.rst pages that name the routine (a
              mention is a lead to read, not proof the deprecation is covered)

and flags these problems:

  no-warning           the docstring marks something deprecated, but no
                       deprecation message is emitted
  low-level            a deprecation message is logged below WARNING
  python-warning-only  warnings.warn() is used and nothing is logged at WARNING
  no-test              no test function matches as described above
  internal-caller      package code still calls a deprecated routine

The scan reads the source with ast and never imports pyspedas. Its matching is
heuristic; check every finding by hand (.agents/skills/deprecation-scan/SKILL.md).

Usage: python .github/scripts/scan_deprecations.py [--root DIR] [--json]
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path

DEPRECAT = re.compile(r"deprecat", re.I)
LOG_LEVELS = {"debug": 10, "info": 20, "warning": 30, "warn": 30,
              "error": 40, "exception": 40, "critical": 50}
LOGGER_NAMES = {"logging", "logger", "log", "_logger", "LOGGER"}
DEPRECATION_CATEGORIES = {"DeprecationWarning", "PendingDeprecationWarning", "FutureWarning"}
CHECKS_A_WARNING = ("assertLogs", "assertWarns", "catch_warnings")
DEFS = (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)


@dataclass
class Emission:
    line: int
    kind: str          # "logging" or "warnings"
    level: str         # logging level name, or the warning category
    level_ok: bool     # logged at WARNING or above


@dataclass
class Finding:
    file: str
    line: int
    name: str
    docstring: list[str] = field(default_factory=list)
    routine_deprecated: bool = False
    warnings: list[Emission] = field(default_factory=list)
    tests: list[str] = field(default_factory=list)
    callers: list[str] = field(default_factory=list)
    migration: list[str] = field(default_factory=list)
    problems: list[str] = field(default_factory=list)


def is_test(path: Path, package: Path) -> bool:
    parts = path.relative_to(package).parts
    return (path.name.startswith("test_")
            or any(part == "tests" or part.endswith("_tests") for part in parts[:-1]))


def own_nodes(node: ast.AST):
    """Walk a definition's body without descending into nested definitions."""
    stack = list(ast.iter_child_nodes(node))
    while stack:
        child = stack.pop()
        yield child
        if not isinstance(child, DEFS):
            stack.extend(ast.iter_child_nodes(child))


def string_text(node: ast.AST) -> str:
    return " ".join(sub.value for sub in ast.walk(node)
                    if isinstance(sub, ast.Constant) and isinstance(sub.value, str))


def emission(call: ast.Call) -> Emission | None:
    func = call.func
    if isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name):
        base, attr = func.value.id, func.attr
    elif isinstance(func, ast.Name):
        base, attr = None, func.id
    else:
        return None
    message = string_text(call)
    if attr == "warn" and base in ("warnings", None):
        category = call.args[1] if len(call.args) > 1 else next(
            (k.value for k in call.keywords if k.arg == "category"), None)
        category_name = category.id if isinstance(category, ast.Name) else (
            category.attr if isinstance(category, ast.Attribute) else "UserWarning")
        if DEPRECAT.search(message) or category_name in DEPRECATION_CATEGORIES:
            return Emission(call.lineno, "warnings", category_name, False)
        return None
    if base in LOGGER_NAMES and attr in LOG_LEVELS and DEPRECAT.search(message):
        return Emission(call.lineno, "logging", attr, LOG_LEVELS[attr] >= 30)
    return None


def test_functions(root: Path, package: Path):
    for path in sorted(package.rglob("*.py")):
        if not is_test(path, package):
            continue
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except (SyntaxError, UnicodeDecodeError):
            continue
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                code = ast.unparse(node)
                if DEPRECAT.search(code) and any(c in code for c in CHECKS_A_WARNING):
                    yield f"{path.relative_to(root).as_posix()}::{node.name}", code


def scan(root: Path) -> list[Finding]:
    package = root / "pyspedas"
    findings: list[Finding] = []
    calls_by_name: dict[str, list[str]] = {}
    for path in sorted(package.rglob("*.py")):
        rel = path.relative_to(root).as_posix()
        if is_test(path, package):
            continue
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except (SyntaxError, UnicodeDecodeError) as exc:
            print(f"skipped {rel}: {exc}", file=sys.stderr)
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                func = node.func
                called = func.id if isinstance(func, ast.Name) else (
                    func.attr if isinstance(func, ast.Attribute) else None)
                if called:
                    calls_by_name.setdefault(called, []).append(f"{rel}:{node.lineno}")
            if not isinstance(node, DEFS):
                continue
            doc = ast.get_docstring(node) or ""
            doc_lines = [line.strip() for line in doc.splitlines() if DEPRECAT.search(line)]
            emitted = [e for e in (emission(n) for n in own_nodes(node) if isinstance(n, ast.Call)) if e]
            if not doc_lines and not emitted:
                continue
            first_line = doc.strip().splitlines()[0] if doc.strip() else ""
            findings.append(Finding(rel, node.lineno, node.name, doc_lines,
                                    bool(DEPRECAT.search(first_line)), emitted))

    tests = list(test_functions(root, package))
    guides = {p.relative_to(root).as_posix(): p.read_text(encoding="utf-8")
              for p in sorted((root / "docs" / "source").glob("*migration*.rst"))}
    for f in findings:
        word = re.compile(rf"\b{re.escape(f.name)}\b")
        f.tests = [test_id for test_id, code in tests if word.search(code)]
        if f.routine_deprecated:
            f.callers = [c for c in calls_by_name.get(f.name, []) if not c.startswith(f.file + ":")]
        f.migration = [guide for guide, text in guides.items() if word.search(text)]
        if f.docstring and not f.warnings:
            f.problems.append("no-warning")
        if any(e.kind == "logging" and not e.level_ok for e in f.warnings):
            f.problems.append("low-level")
        if f.warnings and not any(e.kind == "logging" and e.level_ok for e in f.warnings) \
                and any(e.kind == "warnings" for e in f.warnings):
            f.problems.append("python-warning-only")
        if not f.tests:
            f.problems.append("no-test")
        if f.callers:
            f.problems.append("internal-caller")
    return findings


def report(findings: list[Finding]) -> None:
    for f in findings:
        print(f"{f.file}:{f.line} {f.name}")
        for line in f.docstring:
            print(f"  docstring  {line[:100]}")
        for e in f.warnings:
            print(f"  warning    line {e.line}: {e.kind} {e.level}")
        for t in f.tests:
            print(f"  test       {t}")
        for c in f.callers:
            print(f"  caller     {c}")
        for guide in f.migration:
            print(f"  migration  {guide} names it")
        print(f"  problems   {', '.join(f.problems) or 'none found'}")
        print()
    flagged = sum(1 for f in findings if f.problems)
    print(f"{len(findings)} deprecated routine(s), {flagged} with problems")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2],
                        help="repository root (default: this script's repository)")
    parser.add_argument("--json", action="store_true", help="print JSON instead of text")
    args = parser.parse_args(argv)
    findings = scan(args.root.resolve())
    if args.json:
        print(json.dumps([asdict(f) for f in findings], indent=2))
    else:
        report(findings)
    return 0


if __name__ == "__main__":
    sys.exit(main())
