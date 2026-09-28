---
related_files:
  - pyspedas/projects/AGENTS.md
  - pyspedas/projects/solo/__init__.py
  - pyspedas/projects/solo/config.py
  - pyspedas/projects/solo/load.py
  - pyspedas/projects/solo/mag.py
  - pyspedas/projects/solo/rpw.py
  - pyspedas/projects/solo/swa.py
  - pyspedas/projects/solo/epd.py
  - pyspedas/projects/solo/datasets.py
  - pyspedas/projects/solo/README.md
  - pyspedas/projects/solo/tests/test_solo.py
  - pyspedas/utilities/datasets.py
  - .github/workflows/full_coverage.yml
maintenance: |
  Update when load.py changes a path template, the level handling or the file
  naming for an instrument, or when __init__.py adds a loader.
---

# Solar Orbiter

Loaders for Solar Orbiter in-situ instruments: MAG, RPW, SWA and EPD. All data
are CDF files from SPDF.

## Layout

- `mag.py`, `rpw.py`, `swa.py`, `epd.py`: one wrapper per instrument, each
  calling `load()`.
- `load.py`: `load()`, the file-path chain and loading for all instruments.
- `datasets.py`: `datasets()`, lists Solar Orbiter datasets on CDAWeb through
  `find_datasets()` (`pyspedas/utilities/datasets.py`).
- `config.py`, `tests/test_solo.py`, `README.md` (user guide).

## How it works

Each wrapper calls `load(instrument=..., level=..., datatype=...)`. `load()`
builds
`<instrument>/science/<level>/<datatype>/%Y/solo_<level>_<instrument>-<datatype>_%Y%m%d_v??.cdf`
under `CONFIG['remote_data_dir']` (`https://spdf.gsfc.nasa.gov/pub/data/solar-orbiter/`)
and runs the usual `dailynames()`, `download()`, `cdf_to_tplot()` pipeline.
Variations:

- `level='ll02'` selects low-latency data: folder `low_latency`, file dates
  `%Y%m%dt??????-*` and a three-digit version. For MAG there is no datatype
  folder at this level.
- `epd` adds a `mode` keyword (default `'hcad'`): `.../<datatype>/<mode>/...`
  and `solo_<level>_epd-<datatype>-<mode>_...`.
- SWA: every L2 product except `pas-eflux`, `pas-grnd-mom` and `pas-vdf`, and
  every L1 product except five listed PAS/HIS ones, is named by start and end
  time and matched with the `%Y%m%dt??????-*` wildcard.

The wildcards are resolved by `download()` from the remote directory listing.

## Things to know

- Variable names come straight from the CDF with no instrument prefix (`B_RTN`,
  `eflux`). `mag()` sets legend and title options on `B_RTN`/`B_SRF`, and
  `swa()` sets spectrogram options on `eflux`.
- The wrappers do not expose `force_download`; `load()` has it.
- `time_clip` defaults to False.
- The local data folder is `SOLO_DATA_DIR`, else `SPEDAS_DATA_DIR/solar-orbiter`
  (hyphen), else `solar_orbiter_data/` (underscore) (`config.py`). Setting
  `SOLO_NO_DOWNLOAD` turns downloads off.

## Tests

`python -m pyspedas.projects.solo.tests.test_solo`. CI runs it in
`.github/workflows/full_coverage.yml`.
