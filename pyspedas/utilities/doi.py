"""Access PySPEDAS DOI metadata from an installed package or source checkout."""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, metadata
from pathlib import Path
from typing import Literal

import tomli

DOIKind = Literal["concept", "versioned"]


def _installed_project_urls() -> dict[str, str]:
    try:
        lines = metadata("pyspedas").get_all("Project-URL") or []
    except PackageNotFoundError:
        return {}
    return dict(line.split(", ", 1) for line in lines if ", " in line)


def _source_project_urls() -> dict[str, str]:
    for parent in Path(__file__).resolve().parents:
        pyproject = parent / "pyproject.toml"
        if pyproject.is_file():
            with pyproject.open("rb") as stream:
                return tomli.load(stream)["project"]["urls"]
    return {}


def get_doi(kind: DOIKind = "versioned") -> str:
    """Return the concept or version-specific PySPEDAS DOI URL.

    A source checkout reads ``pyproject.toml``, the canonical location updated at
    release time.  An installed wheel reads its distribution metadata.
    """

    if kind not in ("concept", "versioned"):
        raise ValueError("kind must be 'concept' or 'versioned'")
    key = "Concept_DOI" if kind == "concept" else "Versioned_DOI"
    urls = _source_project_urls()
    if key not in urls:
        urls = _installed_project_urls()
    try:
        return urls[key]
    except KeyError as error:
        raise RuntimeError(f"PySPEDAS {kind} DOI metadata is unavailable") from error
