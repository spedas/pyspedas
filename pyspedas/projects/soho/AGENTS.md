---
related_files:
  - pyspedas/projects/AGENTS.md
  - pyspedas/projects/soho/__init__.py
  - pyspedas/projects/soho/config.py
  - pyspedas/projects/soho/load.py
  - pyspedas/projects/soho/celias.py
  - pyspedas/projects/soho/costep.py
  - pyspedas/projects/soho/erne.py
  - pyspedas/projects/soho/orbit.py
  - pyspedas/projects/soho/celias_postprocessing.py
  - pyspedas/projects/soho/costep_postprocessing.py
  - pyspedas/projects/soho/erne_postprocessing.py
  - pyspedas/projects/soho/orbit_postprocessing.py
  - pyspedas/projects/soho/README.md
  - pyspedas/projects/soho/tests/test_soho.py
  - .github/workflows/full_coverage.yml
maintenance: |
  Update when load.py gains or changes an instrument branch or file resolution,
  or when a *_postprocessing.py module starts doing real work.
---

# SOHO

Loaders for SOHO in-situ data: CELIAS solar wind, COSTEP/EPHIN and ERNE
energetic particles, and orbit/attitude. All data are CDF files from SPDF.

## Layout

- `celias.py`, `costep.py`, `erne.py`, `orbit.py`: one wrapper per instrument,
  each calling `load()` and then its `*_postprocessing.py` module.
- `celias_postprocessing.py`, `costep_postprocessing.py`,
  `erne_postprocessing.py`, `orbit_postprocessing.py`: placeholders that return
  the variable list unchanged.
- `load.py`: `load()`, the file-path chain and loading for all instruments.
- `config.py`, `tests/test_soho.py`, `README.md` (user guide). There is no
  `datasets()`. `__init__.py` imports only the four wrappers, so
  `pyspedas.projects.soho.load` is the module, not the function.

## How it works

Each wrapper calls `load(instrument=..., datatype=...)`, which picks a template
under `CONFIG['remote_data_dir']` (`https://spdf.gsfc.nasa.gov/pub/data/soho/`)
and runs the usual `dailynames()`, `download()`, `cdf_to_tplot()` pipeline:

- `celias`, `erne`: daily files
  `<instrument>/<datatype>/%Y/soho_<instrument>-<datatype>_%Y%m%d_v??.cdf`
  (defaults `pm_5min` and `hed_l2-1min`).
- `costep`: yearly files `..._%Y0101_v??.??.cdf` (note the two-part version),
  so `dailynames()` runs at 366-day resolution. Default `ephin_l3i-1day`.
- `orbit`: `datatype` must be `pre_or` (default), `def_or` or `def_at`; the file
  name reverses it (`orbit/pre_or/cdf/%Y/so_or_pre_...`). Other values log an
  error and return None.

## Things to know

- Variable names come straight from the CDF with no instrument prefix.
- The wrappers do not expose `force_download`; `load()` has it.
- `time_clip` defaults to False; with a yearly COSTEP file, set it to get only
  the requested range.
- The local data folder is `SOHO_DATA_DIR`, else `SPEDAS_DATA_DIR/soho`, else
  `soho_data/` (`config.py`). Setting `SOHO_NO_DOWNLOAD` turns downloads off.

## Tests

`python -m pyspedas.projects.soho.tests.test_soho`. CI runs it in
`.github/workflows/full_coverage.yml`.
