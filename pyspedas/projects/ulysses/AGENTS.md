---
related_files:
  - pyspedas/projects/AGENTS.md
  - pyspedas/projects/ulysses/__init__.py
  - pyspedas/projects/ulysses/config.py
  - pyspedas/projects/ulysses/load.py
  - pyspedas/projects/ulysses/vhm.py
  - pyspedas/projects/ulysses/swoops.py
  - pyspedas/projects/ulysses/swics.py
  - pyspedas/projects/ulysses/urap.py
  - pyspedas/projects/ulysses/epac.py
  - pyspedas/projects/ulysses/hiscale.py
  - pyspedas/projects/ulysses/cospin.py
  - pyspedas/projects/ulysses/grb.py
  - pyspedas/projects/ulysses/datasets.py
  - pyspedas/projects/ulysses/README.md
  - pyspedas/projects/ulysses/tests/test_ulysses.py
  - pyspedas/utilities/datasets.py
  - .github/workflows/full_coverage.yml
maintenance: |
  Update when load.py gains or changes an instrument branch or keyword, when a
  wrapper is added to __init__.py, or when the SPDF Ulysses folder layout changes.
---

# Ulysses

Loaders for the Ulysses heliospheric mission: magnetic field, solar wind plasma
and composition, energetic particles, radio waves and gamma-ray bursts. All data
are CDF files from SPDF.

## Layout

- `vhm.py`, `swoops.py`, `swics.py`, `urap.py`, `epac.py`, `hiscale.py`,
  `cospin.py`, `grb.py`: one wrapper per instrument, each calling `load()`.
- `load.py`: `load()`, the file-path chain and loading for all instruments.
- `datasets.py`: `datasets()`, lists Ulysses datasets on CDAWeb through
  `find_datasets()` (`pyspedas/utilities/datasets.py`).
- `config.py`: `CONFIG` with the local and remote data folders.
- `tests/test_ulysses.py`: unittest module; downloads data.
- `README.md`: user guide with examples.

## How it works

Each wrapper calls `load(instrument=...)` with its own default `datatype` and
`trange`. `load()` picks a path template under `CONFIG['remote_data_dir']`
(`https://spdf.gsfc.nasa.gov/pub/data/ulysses/`) in an if/elif chain, for example
`mag_cdaweb/vhm_<datatype>/%Y/uy_<datatype>_vhm_%Y%m%d_v??.cdf`, then runs the
usual `dailynames()`, `download()`, `cdf_to_tplot()` pipeline.

Datatype strings are mostly `<name>_<level>` (`scs_m1`, `pfrp_m0`, `grb_m0`),
and the file name reverses them (`uy_m1_scs_...`); this applies to `swics`,
`urap`, `hiscale`, `grb` and the `swoops` types `bai_m0`, `bai_m1`, `bae_m0`.
Any other `swoops` datatype (the tests use `proton-moments_swoops`) is read as a
yearly file `uy_<datatype>_%Y0101_v??.cdf`. `cospin` datatypes are bare names
(`het`, `ket`, ...) mapped to `uy_m0_<datatype>`; `vhm` takes `1min`, `1sec`, `m1`.

## Things to know

- Variable names come straight from the CDF with no mission or instrument
  prefix (`B_MAG`, `Density`, `Velocity`). SWOOPS and SWICS both create
  `Velocity`, so use `prefix` or `suffix` when loading both.
- The wrappers default to `time_clip=True`; `load()` defaults to `False`.
- `prefix=None` and `suffix=None` are treated as empty strings.
- The environment variables use `ULY`, not `ULYSSES`: the local data folder is
  `ULY_DATA_DIR`, else `SPEDAS_DATA_DIR/ulysses`, else `ulysses_data/`
  (`config.py`). Setting `ULY_NO_DOWNLOAD` turns downloads off.

## Tests

`python -m pyspedas.projects.ulysses.tests.test_ulysses`. CI runs it in
`.github/workflows/full_coverage.yml`, not in the quick tests.
