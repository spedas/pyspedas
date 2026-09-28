#!/usr/bin/env python3
"""Check the YAML header of every AGENTS.md in this repository.

No folder has to have an AGENTS.md, but every AGENTS.md must start with a YAML
header holding exactly these two fields:

  related_files  Metadata about this AGENTS.md: every file its body describes,
                 plus the AGENTS.md files it relates to (its nearest parent,
                 its children, and any other it points to). Repo-relative
                 POSIX paths; folders are allowed too.
  maintenance    When and how to update this file.

Hard rules fail the check: the header exists and parses, it has exactly those
two fields, related_files is a non-empty list of unique repo-relative paths
other than the file itself, maintenance has at least 20 non-space characters,
and there is text after the header.

Soft rules only warn (--strict makes them fail too): every related_files path
exists; every file the body names in `inline code` or a link is listed; the
nearest parent AGENTS.md and its child list each other; the repository root
has an AGENTS.md.

Usage: python .github/scripts/check_agents_md.py [--strict] [--root DIR]
Needs PyYAML.
"""

from __future__ import annotations

import argparse
import os
import posixpath
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path, PurePosixPath

import yaml

NAME = "AGENTS.md"
FIELDS = ("related_files", "maintenance")
MIN_MAINTENANCE_CHARS = 20

FENCED_BLOCK = re.compile(r"^(```|~~~).*?^\1", re.M | re.S)
INLINE_CODE = re.compile(r"`([^`\n]+)`")
LINK_TARGET = re.compile(r"\]\(([^)\s]+)\)")
LINE_SUFFIX = re.compile(r":\d+(-\d+)?$")


def list_files(root: Path) -> list[str]:
    """Tracked plus untracked-but-not-ignored files, as repo-relative POSIX paths."""
    try:
        out = subprocess.run(
            ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
            cwd=root, capture_output=True, check=True,
        ).stdout.decode("utf-8")
        files = [p for p in out.split("\0") if p]
    except (OSError, subprocess.CalledProcessError):
        files = [p.relative_to(root).as_posix() for p in root.rglob("*")
                 if p.is_file() and ".git" not in p.relative_to(root).parts]
    return sorted(p for p in files if (root / p).is_file())


def split_header(text: str) -> tuple[dict | None, str, str | None]:
    """Return (header, body, problem) for a document that should open with '---'."""
    lines = text.replace("\r\n", "\n").split("\n")
    if lines[0].strip() != "---":
        return None, "", "must start with a '---' YAML header"
    for end in range(1, len(lines)):
        if lines[end].strip() == "---":
            break
    else:
        return None, "", "YAML header is not closed with '---'"
    try:
        header = yaml.safe_load("\n".join(lines[1:end]))
    except yaml.YAMLError as exc:
        return None, "", f"YAML header does not parse: {exc}"
    if not isinstance(header, dict):
        return None, "", "YAML header must be a mapping"
    return header, "\n".join(lines[end + 1:]), None


def path_syntax_problem(entry: object) -> str | None:
    if not isinstance(entry, str) or not entry.strip():
        return "must be a non-empty string"
    if entry != entry.strip():
        return "must not have leading or trailing spaces"
    if entry.startswith("/") or "\\" in entry or re.match(r"^[A-Za-z]:", entry):
        return "must be a repo-relative POSIX path"
    if any(part in ("", ".", "..") for part in entry.rstrip("/").split("/")):
        return "must not contain '.', '..' or empty path segments"
    return None


def mentioned_files(body: str, folder: str, files: set[str],
                    by_name: dict[str, list[str]]) -> set[str]:
    """Files the body names in inline code or links, resolved the way a reader would:
    relative to the AGENTS.md folder, then to the repo root, then (for a bare file
    name) as the only file with that name below the AGENTS.md folder."""
    body = FENCED_BLOCK.sub("", body)
    tokens = [word for span in INLINE_CODE.findall(body) for word in span.split()]
    tokens += LINK_TARGET.findall(body)
    found = set()
    for token in tokens:
        token = LINE_SUFFIX.sub("", token.strip("\"'(),;"))
        if "/" not in token and "." not in token:
            continue
        hit = next((c for c in (posixpath.normpath(posixpath.join(folder, token)), token)
                    if c in files), None)
        if hit is None and "/" not in token:
            prefix = folder + "/" if folder else ""
            matches = [p for p in by_name.get(token, []) if p.startswith(prefix)]
            hit = matches[0] if len(matches) == 1 else None
        if hit:
            found.add(hit)
    return found


def nearest_parent(path: str, present: set[str]) -> str | None:
    folder = PurePosixPath(path).parent
    while folder != PurePosixPath("."):
        folder = folder.parent
        candidate = (folder / NAME).as_posix()
        if candidate in present:
            return candidate
    return None


def check(root: Path) -> tuple[list[str], list[tuple[str, str]], list[tuple[str, str]]]:
    all_files = list_files(root)
    files = set(all_files)
    folders: set[str] = set()
    for p in all_files:
        folder = posixpath.dirname(p)
        while folder and folder not in folders:
            folders.add(folder)
            folder = posixpath.dirname(folder)
    by_name = defaultdict(list)
    for p in all_files:
        by_name[posixpath.basename(p)].append(p)
    agents = [p for p in all_files if posixpath.basename(p) == NAME]

    errors: list[tuple[str, str]] = []
    warnings: list[tuple[str, str]] = []
    related: dict[str, set[str]] = {}

    for path in agents:
        try:
            text = (root / path).read_text(encoding="utf-8")
        except UnicodeDecodeError:
            errors.append((path, "is not UTF-8 text"))
            continue
        header, body, problem = split_header(text)
        if problem:
            errors.append((path, problem))
            continue
        for key in sorted(set(header) - set(FIELDS)):
            errors.append((path, f"unknown header field '{key}' (allowed: {', '.join(FIELDS)})"))
        for key in FIELDS:
            if key not in header:
                errors.append((path, f"missing header field '{key}'"))
        if not body.strip():
            errors.append((path, "has no text after the YAML header"))

        maintenance = header.get("maintenance")
        if "maintenance" in header:
            if not isinstance(maintenance, str):
                errors.append((path, "maintenance must be a string"))
            elif len("".join(maintenance.split())) < MIN_MAINTENANCE_CHARS:
                errors.append((path, f"maintenance needs at least {MIN_MAINTENANCE_CHARS} non-space characters"))

        listed: set[str] = set()
        entries = header.get("related_files")
        if "related_files" in header and (not isinstance(entries, list) or not entries):
            errors.append((path, "related_files must be a non-empty list"))
            entries = []
        for entry in entries or []:
            problem = path_syntax_problem(entry)
            if problem:
                errors.append((path, f"related_files entry {entry!r} {problem}"))
                continue
            entry = entry.rstrip("/")
            if entry == path:
                errors.append((path, "related_files must not list the file itself"))
            elif entry in listed:
                errors.append((path, f"related_files lists {entry} twice"))
            elif entry not in files and entry not in folders:
                warnings.append((path, f"related_files entry {entry} does not exist"))
            listed.add(entry)
        related[path] = listed

        folder = posixpath.dirname(path)
        for mention in sorted(mentioned_files(body, folder, files, by_name) - listed - {path}):
            warnings.append((path, f"body mentions {mention}, which related_files does not list"))

    present = set(agents)
    if agents and NAME not in present:
        warnings.append((NAME, "missing; the repository root should have an AGENTS.md"))
    for path in agents:
        parent = nearest_parent(path, present)
        if parent is None or path not in related:
            continue
        if parent not in related[path]:
            warnings.append((path, f"related_files does not list its parent {parent}"))
        if parent in related and path not in related[parent]:
            warnings.append((parent, f"related_files does not list its child {path}"))
    return agents, errors, warnings


def report(level: str, path: str, message: str) -> None:
    if os.environ.get("GITHUB_ACTIONS") == "true":
        print(f"::{level} file={path}::{message}")
    else:
        print(f"{path}: {level}: {message}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check the YAML header of every AGENTS.md.")
    parser.add_argument("--strict", action="store_true", help="fail on warnings too")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2],
                        help="repository root (default: two levels above this script)")
    args = parser.parse_args(argv)

    agents, errors, warnings = check(args.root.resolve())
    for path, message in errors:
        report("error", path, message)
    for path, message in warnings:
        report("warning", path, message)
    print(f"{len(agents)} AGENTS.md file(s): {len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors or (args.strict and warnings) else 0


if __name__ == "__main__":
    sys.exit(main())
