---
related_files:
  - pyspedas/projects/AGENTS.md
  - pyspedas/projects/polar/__init__.py
  - pyspedas/projects/polar/config.py
  - pyspedas/projects/polar/load.py
  - pyspedas/projects/polar/mfe.py
  - pyspedas/projects/polar/efi.py
  - pyspedas/projects/polar/pwi.py
  - pyspedas/projects/polar/hydra.py
  - pyspedas/projects/polar/tide.py
  - pyspedas/projects/polar/timas.py
  - pyspedas/projects/polar/cammice.py
  - pyspedas/projects/polar/ceppad.py
  - pyspedas/projects/polar/uvi.py
  - pyspedas/projects/polar/vis.py
  - pyspedas/projects/polar/pixie.py
  - pyspedas/projects/polar/orbit.py
  - pyspedas/projects/polar/datasets.py
  - pyspedas/projects/polar/README.md
  - pyspedas/projects/polar/tests/test_polar.py
  - pyspedas/utilities/datasets.py
  - pyspedas/preferences.py
  - .github/workflows/quick_tests.yml
maintenance: |
  Update when load.py adds an instrument branch or changes a file-name code, when
  a wrapper's instrument string changes, or when __init__.py adds a loader.
---

# Polar

Loaders for the Polar magnetospheric mission. All data are daily key-parameter
CDF files from SPDF (`https://spdf.gsfc.nasa.gov/pub/data/polar/`).

## Layout

- `mfe.py`, `efi.py`, `pwi.py`, `hydra.py`, `tide.py`, `timas.py`, `cammice.py`,
  `ceppad.py`, `uvi.py`, `vis.py`, `pixie.py`, `orbit.py`: one thin wrapper per
  instrument, each returning `load(instrument=...)`.
- `load.py`: `load()`, the path-template chain for all instruments.
- `datasets.py`: `datasets()`, lists Polar datasets on CDAWeb through
  `find_datasets()` (`pyspedas/utilities/datasets.py`).
- `config.py`, `tests/test_polar.py`, `README.md` (user guide; its examples use
  the pre-2.0 path `pyspedas.polar`).

## How it works

`load()` builds `<instrument>/<instrument>_<datatype>/%Y/po_<datatype>_<code>_%Y%m%d_v??.cdf`
and runs the usual `dailynames()`, `download()`, `cdf_to_tplot()` pipeline, then
`time_clip` if asked. `<code>` is the instrument name except for `hydra`
(`hyd`), `tide` (`tid`), `timas` (`tim`), `cammice` (`cam`), `ceppad` (`cep`) and
`pixie` (`pix`). `orbit()` passes `instrument='spha'`, which reads
`orbit/spha_<datatype>/%Y/po_<datatype>_spha_...` files.

## Things to know

- `datatype` defaults to `'k0'` in every wrapper, and the wrapper docstrings
  list no other value.
- There is no automatic prefix; variables keep their CDF names, so use `prefix`
  or `suffix` to keep instruments apart.
- `__init__.py` does not export `load`; import it from
  `pyspedas.projects.polar.load` if needed.
- The local data folder is `POLAR_DATA_DIR`, else `SPEDAS_DATA_DIR/polar`, else
  `polar_data/` (`config.py`, which first applies saved preferences from
  `pyspedas/preferences.py`). Setting `POLAR_NO_DOWNLOAD` turns downloads off.

## Tests

`python -m pyspedas.projects.polar.tests.test_polar` (downloads data). CI runs it
in `.github/workflows/quick_tests.yml`.
