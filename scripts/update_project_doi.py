#!/usr/bin/env python3
"""Read or update the DOI URLs stored in ``pyproject.toml``.

This deliberately lives outside the PySPEDAS package so the release workflows can
also copy it into other projects.  ``tomlkit`` preserves the file's formatting.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import tomlkit


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=Path, default=Path("pyproject.toml"))
    parser.add_argument(
        "--key", choices=("Concept_DOI", "Versioned_DOI"), required=True
    )
    parser.add_argument("--value", help="DOI or https://doi.org/ URL to write")
    args = parser.parse_args()

    document = tomlkit.parse(args.file.read_text(encoding="utf-8"))
    urls = document["project"]["urls"]
    if args.value is None:
        print(urls[args.key])
        return

    value = args.value.strip()
    if not value.startswith("https://doi.org/"):
        value = f"https://doi.org/{value}"
    urls[args.key] = value
    args.file.write_text(tomlkit.dumps(document), encoding="utf-8")
    print(value)


if __name__ == "__main__":
    main()
