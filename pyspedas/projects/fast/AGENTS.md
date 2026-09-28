---
related_files:
  - pyspedas/projects/AGENTS.md
  - pyspedas/projects/fast/__init__.py
  - pyspedas/projects/fast/config.py
  - pyspedas/projects/fast/load.py
  - pyspedas/projects/fast/README.md
  - pyspedas/projects/fast/tests/test_fast.py
  - pyspedas/utilities/pyspedas_functools.py
  - pyspedas/utilities/datasets.py
  - .github/workflows/full_coverage.yml
maintenance: |
  Update when load.py gains or changes an instrument, level or datatype branch,
  or when __init__.py adds a loader or edits the per-loader docstrings.
---

# FAST

Loaders for the FAST auroral satellite: DC and AC fields, ESA electron and ion
spectrometers, and TEAMS ion composition. All data are CDF files from SPDF.

## Layout

- `load.py`: `load()`, the only loading code.
- `__init__.py`: defines `dcf`, `acf`, `esa`, `teams` as
  `better_partial(load, instrument=...)` (`pyspedas/utilities/pyspedas_functools.py`)
  and `datasets` as a partial of `find_datasets()` (`pyspedas/utilities/datasets.py`).
  Each loader's docstring is written out in full here, so a change to
  `load()`'s keywords must be copied four times.
- `config.py`, `tests/test_fast.py`, `README.md` (user guide).

## How `load()` works

`load()` checks that `trange` is a two-element list in order (else it logs an
error and returns `[]`), accepts one instrument, a list, or `'all'` (all four),
and for each picks a template under `CONFIG['remote_data_dir']`
(`https://spdf.gsfc.nasa.gov/pub/data/fast/`):

- `dcf`: `level='l2'` (default) reads hourly high-resolution files
  `dcf/l2/dcb/%Y/%m/fast_hr_dcb_%Y%m%d%H????_?????_v??.cdf`, expanded by
  `dailynames()` at one-hour resolution; `level='k0'` reads daily key parameters.
- `acf`: k0 only.
- `esa`: L2, `datatype` one of `eeb`, `ees`, `ieb`, `ies`; anything else becomes
  `eeb`.
- `teams`: `level='l2'` reads pitch-angle (`pa`) files, `level='k0'` key parameters.

Files go through `download()` and `cdf_to_tplot()` one instrument at a time.

## Things to know

- Every variable gets the prefix `fast_<instrument>_` (`fast_dcf_DeltaB_GEI`,
  `fast_esa_eflux`); a user `prefix` goes before it.
- `datatype` matters only for `esa` and `level` only for `dcf` and `teams`.
- With `notplot=True`, `load()` returns the data dictionary of the first
  instrument only.
- `time_clip` defaults to False; when set, variables are clipped in place.
- The local data folder is `FAST_DATA_DIR`, else `SPEDAS_DATA_DIR/fast`, else
  `fast_data/` (`config.py`). Setting `FAST_NO_DOWNLOAD` turns downloads off.

## Tests

`python -m pyspedas.projects.fast.tests.test_fast`, including invalid `trange`
and instrument cases. CI runs it in `.github/workflows/full_coverage.yml`.
