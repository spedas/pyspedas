---
related_files:
  - pyspedas/projects/themis/AGENTS.md
  - pyspedas/__init__.py
  - pyspedas/projects/themis/spacecraft/fields/fgm.py
  - pyspedas/projects/themis/load.py
  - pyspedas/utilities/dailynames.py
  - pyspedas/utilities/download.py
  - pyspedas/tplot_tools/importers/cdf_to_tplot.py
  - pyspedas/projects/mms/__init__.py
  - pyspedas/projects/mms/mms_load_data.py
  - pyspedas/tplot_tools/__init__.py
  - pyspedas/tplot_tools/store_data.py
  - pyspedas/tplot_tools/get_data.py
  - pyspedas/tplot_tools/tplot_rename.py
  - docs/source/pyspedas_2_migration.rst
  - CONTRIBUTING.md
  - pyproject.toml
  - .github/workflows/quick_tests.yml
  - .github/workflows/agents_md.yml
  - .github/scripts/check_agents_md.py
  - .github/scripts/build_agents_map.py
  - .agents/skills/agents-map/SKILL.md
  - .agents/map/MAP.md
  - .agents/map/graph.json
maintenance: |
  Update when the package layout, the loader pipeline, tplot storage or the test
  setup changes, and list any new AGENTS.md whose nearest parent is this file.
---

# pySPEDAS

Python Space Physics Environment Data Analysis Software. Mission loaders download
data files (mostly CDF) and store them as tplot variables; the rest of the package
analyzes, transforms and plots those variables. Package code is in `pyspedas/`;
dependencies are in `pyproject.toml`.

## Layout

- `pyspedas/projects/<mission>/`: one package per mission (39). Each has a
  `config.py` with `CONFIG` (`local_data_dir`, `remote_data_dir`), a `load.py`,
  one module per instrument, a README.md user guide and a `tests/` folder.
- `pyspedas/tplot_tools/`: tplot variable storage and plotting. This is the former
  PyTplot package, now part of pySPEDAS; there is no external `pytplot` dependency.
- `pyspedas/utilities/`: shared helpers, including downloading and file naming.
- `pyspedas/cotrans_tools/`, `pyspedas/geopack/`, `pyspedas/particles/`,
  `pyspedas/analysis/`: coordinate transforms, field models, particle
  distributions and general analysis.
- `pyspedas/__init__.py` re-exports the public API by name (no `import *`).

## How a loader works

Most loaders run the same pipeline. For `pyspedas.projects.themis.fgm()`:

1. The wrapper `pyspedas/projects/themis/spacecraft/fields/fgm.py` calls the
   mission's `load()` in `pyspedas/projects/themis/load.py`.
2. `load()` picks a file path template for the instrument in an if/elif chain.
3. `dailynames()` (`pyspedas/utilities/dailynames.py`) expands the template over
   the time range, and `download()` (`pyspedas/utilities/download.py`) fetches the
   files by reading the remote directory listing (S3 and fsspec also work).
4. `cdf_to_tplot()` (`pyspedas/tplot_tools/importers/cdf_to_tplot.py`) stores the
   file contents as tplot variables.

MMS is the main exception: `pyspedas/projects/mms/mms_load_data.py` queries the
LASP SDC file API instead of a directory listing.

## tplot variables

All variables live in one global `OrderedDict`, `data_quants`, defined in
`pyspedas/tplot_tools/__init__.py`. Each value is an `xarray.DataArray` with a
`time` dimension and plot options in `.attrs["plot_options"]`; non-time-varying
data is a plain dict. `store_data()` (`pyspedas/tplot_tools/store_data.py`) and
`get_data()` (`pyspedas/tplot_tools/get_data.py`) are the front doors.

Read it as `pyspedas.tplot_tools.data_quants`, never with
`from pyspedas.tplot_tools import data_quants`: `tplot_rename()`
(`pyspedas/tplot_tools/tplot_rename.py`) replaces the dict with a new object, so
a name bound at import time goes stale.

## Finding code

- Short names repeat across missions (`fgm`, `load`, `config`), so search within
  a mission: `grep -rn "^def fgm" pyspedas/projects/themis`.
- A mission's `__init__.py` imports each loader over its module name, so
  `pyspedas.projects.themis.fgm` is the function, not the module.
- MMS wrappers in `pyspedas/projects/mms/__init__.py` take `*args, **kwargs`; the
  real signature is on the `mms_load_<instrument>` function they wrap, in
  `pyspedas/projects/mms/<instrument>_tools/`.
- Version 2.0 moved missions under `pyspedas.projects` (`pyspedas.mms` is now
  `pyspedas.projects.mms`); see `docs/source/pyspedas_2_migration.rst`. Some
  READMEs still show the old paths.

## Tests and style

- Tests sit next to the code in `tests/` folders and most download real data, so
  they need network access. Run one module the way CI
  (`.github/workflows/quick_tests.yml`) does:
  `python -m pyspedas.projects.themis.tests.test_themis`.
- `SPEDAS_DATA_DIR`, or a per-mission variable such as `THM_DATA_DIR`, sets where
  data is downloaded.
- Docstrings are numpy style (`CONTRIBUTING.md`).

## AGENTS.md files

Any folder may have an AGENTS.md; none is required. Each one starts with a YAML
header with exactly two fields:

- `related_files`: metadata about that AGENTS.md. List every file its text
  describes and every related AGENTS.md (the nearest parent, the children, and
  any other it points to), as repo-relative paths.
- `maintenance`: when and how to update that AGENTS.md.

CI (`.github/workflows/agents_md.yml`) runs `.github/scripts/check_agents_md.py`
on every push and pull request. A missing or malformed header fails the build.
Listed paths that don't exist, described files that aren't listed, and one-way
parent/child links are warnings. Locally, run
`python .github/scripts/check_agents_md.py --strict` (needs PyYAML).

### The AGENTS.md map

`.agents/map/` holds a map of every AGENTS.md and its related files
(`.agents/map/MAP.md` for people, `.agents/map/graph.json` for tools), generated
by `.github/scripts/build_agents_map.py`. It is opt-in: after you add, remove or
revise an AGENTS.md, ask the human whether to rebuild the map, and rebuild it
only after an explicit yes, following `.agents/skills/agents-map/SKILL.md`.
