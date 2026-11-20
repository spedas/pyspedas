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
  tplot variable.
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

This package currently only requests and extracts **magnetic field** data:
`utilities.py`'s `_list_of_fdsn_channels()` hardcodes the SEED instrument
code `F` (magnetic), and `load_fdsn.py`'s extraction loop only recognizes
the `hx`/`hy`/`hz` (or `bx`/`by`/`bz`) components and requires
`channels_recorded_magnetic` to be present with exactly 3 entries, so a run
with electric-field channels (SEED instrument code `Q`, MTH5 components
`ex`/`ey`) is skipped rather than extracted. See `fdsn_data_model.md` for the
FDSN/MTH5 channel-naming, hierarchy, and filter-chain/calibration data model
that this package and any future electric-field support build on.

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
