---
related_files:
  - pyspedas/projects/AGENTS.md
  - pyspedas/projects/wind/__init__.py
  - pyspedas/projects/wind/config.py
  - pyspedas/projects/wind/load.py
  - pyspedas/projects/wind/mfi.py
  - pyspedas/projects/wind/swe.py
  - pyspedas/projects/wind/sms.py
  - pyspedas/projects/wind/waves.py
  - pyspedas/projects/wind/threedp.py
  - pyspedas/projects/wind/orbit.py
  - pyspedas/projects/wind/datasets.py
  - pyspedas/projects/wind/README.md
  - pyspedas/projects/wind/tests/test_wind.py
  - pyspedas/utilities/datasets.py
  - pyspedas/utilities/download.py
  - .github/workflows/full_coverage.yml
maintenance: |
  Update when load.py changes an instrument branch, the automatic prefixes, the
  master-CDF handling or the Berkeley server option, or when __init__.py adds a loader.
---

# Wind

Loaders for the Wind solar wind mission: magnetic field, plasma, composition,
3DP particles, WAVES radio and orbit/attitude. All data are CDF files, from SPDF
by default.

## Layout

- `mfi.py`, `swe.py`, `sms.py`, `waves.py`, `threedp.py`, `orbit.py`: one wrapper
  per instrument, each calling `load()`.
- `load.py`: `load()`, the file-path chain and loading for all instruments.
- `datasets.py`: `datasets()`, lists Wind datasets on CDAWeb through
  `find_datasets()` (`pyspedas/utilities/datasets.py`).
- `config.py`, `tests/test_wind.py`, `README.md` (user guide).

## How it works

Each wrapper calls `load()` with an instrument string; two differ from the
wrapper name: `mfi()` passes `instrument='fgm'` and `threedp()` passes `'3dp'`.
`load()` picks a path template in an if/elif chain, e.g.
`mfi/mfi_<datatype>/%Y/wi_<datatype>_mfi_%Y%m%d_v??.cdf`, and runs the usual
`dailynames()`, `download()`, `cdf_to_tplot()` pipeline. For `orbit` and most
`3dp` types the datatype is `<name>_<level>` (`pre_or`, `3dp_pm`) and the file
name reverses it (`wi_or_pre_...`, `wi_pm_3dp_...`).

Two steps are specific to Wind:

- `addmaster=True` (the default) also downloads the CDAWeb master CDF
  (`https://cdaweb.gsfc.nasa.gov/pub/software/cdawlib/0MASTERS/`) into
  `<local_data_dir>wind_masters/` and passes it to `cdf_to_tplot()` as
  `mastercdf`, so variable metadata come from the master. It is turned off for
  WAVES `tnr`, `qtnfit` and `qtnfit-filtered`.
- Both downloads pass `last_version=True` to `download()`
  (`pyspedas/utilities/download.py`), so only the highest `v??` version of each
  file is kept.

## Things to know

- Automatic prefixes: WAVES `rad1`, `rad2`, `tnr`, `qtnfit`, `qtnfit-filtered`
  get `wi_l2_wav_<datatype>_` and 3DP types other than `3dp_emfits_e0` get
  `wi_<datatype>_`, with a user `prefix` placed before them. Everything else uses
  the bare CDF names (`BGSE`, `N_elec`, `GSM_POS`).
- `threedp(berkeley=True)` switches the server to
  `http://themis.ssl.berkeley.edu/data/wind/` and to Berkeley's
  `3dp/<datatype>/%Y/wi_<datatype>_3dp_...` file names. Only `threedp()` exposes
  `berkeley`.
- `time_clip` defaults to False in all wrappers.
- The local data folder is `WIND_DATA_DIR`, else `SPEDAS_DATA_DIR/wind`, else
  `wind_data/` (`config.py`). Setting `WIND_NO_DOWNLOAD` turns downloads off.

## Tests

`python -m pyspedas.projects.wind.tests.test_wind`. CI runs it in
`.github/workflows/full_coverage.yml`.
