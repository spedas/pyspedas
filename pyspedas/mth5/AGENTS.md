---
related_files:
  - AGENTS.md
  - pyspedas/mth5/config.py
  - pyspedas/mth5/load_fdsn.py
  - pyspedas/mth5/utilities.py
  - pyspedas/mth5/__init__.py
  - pyspedas/mth5/fdsn_data_model.md
  - pyspedas/mth5/examples/dataset_example.py
  - pyspedas/mth5/examples/load_fdsn_example.py
  - pyspedas/mth5/examples/readme.md
  - pyspedas/mth5/tests/test_load_fdsn.py
  - pyspedas/mth5/tests/test_mth5_import.py
  - pyspedas/mth5/tests/tests.md
  - docs/source/mth5.rst
maintenance: |
  Update when the MTH5 dependency handling, FDSN loading and caching behavior,
  data-directory configuration, examples, or tests change.
---

# MTH5

This package integrates pySPEDAS with the external `mth5` package. Importing
`pyspedas.mth5` creates the configured local data directory and requires the
external dependency; when available, it synchronizes the MTH5 loguru handler
with the pySPEDAS logging level.

## Layout

- `load_fdsn.py`: validates an FDSN request, creates or reuses an MTH5 HDF5
  cache, reads the requested data through MTH5, and stores the result as a
  tplot variable. Runs with differing coordinate system, units, or
  measurement type are split into additional `_1`, `_2`, ... variables.
- `utilities.py`: provides FDSN channel filtering, time-string conversion, and
  dataset discovery helpers.
- `config.py`: defines the local `mth5/` data directory and supports
  `SPEDAS_DATA_DIR` as its parent directory.
- `examples/`: example scripts and usage notes.
- `tests/`: unit tests for FDSN loading, dataset discovery, and missing-
  dependency import handling. `tests/tests.md` documents each test's purpose
  and the setup/teardown behavior for both test modules, and must be updated
  in the same change whenever a test is added, renamed, or its behavior
  changes — not just periodically.

## Data and dependencies

The external dependency is installed separately with `pip install mth5`.
FDSN requests use the EarthScope client through MTH5 and require network
access unless a matching cached HDF5 file is reused. The `nodownload` option
reuses an existing cache; `noexception` suppresses an MTH5 request exception
and returns without creating a tplot variable.

`load_fdsn.py` loads the **magnetic** and/or **electric** field, selected by
the `datatype` keyword (`'mag'`, `'elec'`, `['mag', 'elec']`, or
`'legacy'`). Without `datatype`, `'legacy'` is used and a deprecation warning
is logged; the default is planned to change to `'mag'` in a future major
release (RULES.md). The module-level `_FIELDS` table in `load_fdsn.py` is the only
place that defines each field: SEED instrument code (`F` magnetic, `Q`
electric), MTH5 components (`hx`/`hy`/`hz` or `bx`/`by`/`bz`; `ex`/`ey`), the
`channels_recorded_*` run attribute, and output column labels. Missing
components of a run are NaN-filled.

- `'mag'`/`'elec'` create `fdsn_mag_<network>_<station>` /
  `fdsn_elec_<network>_<station>` and return a list of tplot names. Only the
  requested instruments are downloaded, into a cache file ending in `_F.h5`,
  `_Q.h5`, or `_FQ.h5`.
- `'legacy'` keeps the earlier behavior: magnetic only, `fdsn_<network>_<station>`,
  a single `str` return, a cache file without an instrument suffix, and the
  legend from station `channels_recorded`.
- An electric-only request can fail in mth5 0.6.9 and earlier (pydantic
  `ValidationError` in `StationGroup.update_metadata`) when a station run has
  no electric channels in the requested period; `load_fdsn` logs a warning.

`utilities.py`'s `datasets()` accepts the same `datatype` values. See
`fdsn_data_model.md` for the FDSN/MTH5 channel-naming, hierarchy, and
filter-chain/calibration data model.

## Tests

Run the package tests with:

```powershell
python -m unittest discover -s pyspedas/mth5/tests
```

Tests that exercise live FDSN requests require the external `mth5` package and
network access; mocked tests cover request construction and error handling.
`test_load_fdsn.py` encodes real ordering dependencies between tests (a cold
vs. warm service-discovery cache, a basic load that later tests rely on) as a
`test<bucket>_` number in each method name; see `tests/tests.md` for the bucket meanings.
