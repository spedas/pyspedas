"""Persistent, per-user overrides for PySPEDAS configuration dictionaries.

Defaults stay in their existing config modules. Mission preferences are applied
before those modules process environment variables, preserving the precedence
default < preferences < environment < explicit arguments.
"""

from __future__ import annotations

import importlib
import os
from pathlib import Path
import tempfile
from collections.abc import Mapping
from functools import lru_cache

from platformdirs import user_config_path
import tomlkit


_SUBCONFIGS = {"maven": {"spdf"}}


def preferences_path() -> Path:
    """Return the preferences path, honoring ``PYSPEDAS_CONFIG_FILE``."""
    override = os.environ.get("PYSPEDAS_CONFIG_FILE")
    if override:
        return Path(override).expanduser()
    return user_config_path("pyspedas") / "preferences.toml"


@lru_cache(maxsize=4)
def _read_file(path: Path) -> dict:
    if not path.is_file():
        return {}
    try:
        with path.open("r", encoding="utf-8") as stream:
            parsed = tomlkit.parse(stream.read())
    except (OSError, ValueError) as exc:
        raise ValueError(f"Could not read PySPEDAS preferences at {path}: {exc}") from exc
    data = parsed.unwrap()
    if not isinstance(data, dict):
        raise ValueError(f"PySPEDAS preferences at {path} must be a TOML table")
    return data


def read_preferences() -> dict:
    """Read a copy of the user preferences (without applying defaults)."""
    from copy import deepcopy

    return deepcopy(_read_file(preferences_path()))


def reload_preferences() -> dict:
    """Re-read the file; already-imported mission CONFIGs are not modified.

    Restart Python to apply hand-edited preferences to mission modules already
    imported, because their loaders retain references to the CONFIG dictionaries.
    """
    _read_file.cache_clear()
    return read_preferences()


def _mission_values(mission: str) -> dict:
    projects = _read_file(preferences_path()).get("projects", {})
    if not isinstance(projects, dict):
        raise ValueError("[projects] in PySPEDAS preferences must be a table")
    values = projects
    for part in mission.split("."):
        values = values.get(part, {})
        if not isinstance(values, dict):
            raise ValueError(f"[projects.{mission}] must be a table")
    # A nested config section is not itself a key in the parent mission CONFIG.
    return {key: value for key, value in values.items()
            if key not in _SUBCONFIGS.get(mission, ())}


def _apply_values(config: dict, values: dict, section: str) -> None:
    unknown = set(values) - set(config)
    if unknown:
        names = ", ".join(sorted(unknown))
        raise ValueError(f"Unknown preference(s) for {section}: {names}")
    for key, value in values.items():
        default = config[key]
        if default is not None and type(value) is not type(default):
            raise TypeError(
                f"Preference {section}.{key} must be "
                f"{type(default).__name__}, not {type(value).__name__}"
            )
        config[key] = value


def apply_mission_preferences(config: dict, mission: str) -> dict:
    """Overlay a mission's stored values on its existing CONFIG dictionary.

    Call immediately after defining CONFIG, before existing environment-variable
    overrides.  The dictionary is updated in place to preserve imported aliases.
    """
    _apply_values(config, _mission_values(mission), f"projects.{mission}")
    return config


def apply_pyspedas_preferences(config: dict) -> dict:
    """Overlay ``[pyspedas.*]`` tables on the top-level PySPEDAS CONFIG."""
    sections = _read_file(preferences_path()).get("pyspedas", {})
    if not isinstance(sections, dict):
        raise ValueError("[pyspedas] in PySPEDAS preferences must be a table")
    unknown = set(sections) - set(config)
    if unknown:
        raise ValueError(f"Unknown PySPEDAS preference section(s): {', '.join(sorted(unknown))}")
    for section, values in sections.items():
        if not isinstance(values, dict):
            raise ValueError(f"[pyspedas.{section}] must be a table")
        _apply_values(config[section], values, f"pyspedas.{section}")
    return config


def _config_for(section: str) -> dict:
    if not section or not all(part.isidentifier() for part in section.split(".")):
        raise ValueError(f"Invalid preference section: {section!r}")
    if section.startswith("pyspedas."):
        parts = section.split(".")[1:]
        config = importlib.import_module("pyspedas.config").CONFIG
        for part in parts:
            if part not in config or not isinstance(config[part], dict):
                raise ValueError(f"Unknown PySPEDAS preference section: {section}")
            config = config[part]
        return config
    try:
        module = importlib.import_module(f"pyspedas.projects.{section}.config")
    except ModuleNotFoundError as exc:
        raise ValueError(f"Unknown mission: {section}") from exc
    return module.CONFIG


def _set_nested(table, section_name: str, values: Mapping) -> None:
    parts = section_name.split(".")
    if section_name.startswith("pyspedas."):
        section = table
    else:
        section = table.setdefault("projects", tomlkit.table())
    for part in parts:
        section = section.setdefault(part, tomlkit.table())
    for key, value in values.items():
        if value is None:
            section.pop(key, None)  # TOML has no null value.
        else:
            section[key] = value


def save_preferences(mission: str, values: Mapping) -> Path:
    """Save selected CONFIG keys for a mission or ``pyspedas.*`` section.

    ``mission`` is a project name such as ``"themis"`` or a package section
    such as ``"pyspedas.plotting"``. ``values`` may be the section's complete
    CONFIG dictionary or a smaller patch. A ``None`` value removes the TOML
    override.
    """
    if not isinstance(values, Mapping):
        raise TypeError("values must be a mapping of CONFIG keys to values")
    config = _config_for(mission)
    unknown = set(values) - set(config)
    if unknown:
        raise ValueError(f"Unknown preference(s) for {mission}: {', '.join(sorted(unknown))}")
    for key, value in values.items():
        default = config[key]
        if value is not None and default is not None and type(value) is not type(default):
            section = mission if mission.startswith("pyspedas.") else f"projects.{mission}"
            raise TypeError(f"Preference {section}.{key} must be {type(default).__name__}")

    path = preferences_path()
    if path.exists():
        try:
            table = tomlkit.parse(path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            raise ValueError(f"Could not read PySPEDAS preferences at {path}: {exc}") from exc
    else:
        table = tomlkit.document()
    _set_nested(table, mission, values)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=path.parent,
            prefix=f".{path.name}.", suffix=".tmp", delete=False,
        ) as stream:
            temp_path = Path(stream.name)
            stream.write(tomlkit.dumps(table))
        os.replace(temp_path, path)
    finally:
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)
    _read_file.cache_clear()
    return path


def set_preference(mission: str, key: str, value) -> Path:
    """Set one mission or ``pyspedas.*`` preference (``None`` removes it)."""
    return save_preferences(mission, {key: value})


def unset_preference(mission: str, key: str) -> Path:
    """Remove one preference, restoring lower-priority sources."""
    return set_preference(mission, key, None)
