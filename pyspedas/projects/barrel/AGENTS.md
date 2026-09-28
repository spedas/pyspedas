---
related_files:
  - pyspedas/projects/AGENTS.md
  - pyspedas/projects/barrel/__init__.py
  - pyspedas/projects/barrel/config.py
  - pyspedas/projects/barrel/load.py
  - pyspedas/projects/barrel/sspc.py
  - pyspedas/projects/barrel/mspc.py
  - pyspedas/projects/barrel/fspc.py
  - pyspedas/projects/barrel/rcnt.py
  - pyspedas/projects/barrel/magn.py
  - pyspedas/projects/barrel/ephm.py
  - pyspedas/projects/barrel/hkpg.py
  - pyspedas/projects/barrel/README.md
  - pyspedas/projects/barrel/tests/test_barrel.py
  - .github/workflows/full_coverage.yml
maintenance: |
  Update when load.py changes its path template, variable prefix or keywords,
  when a wrapper is added, or when balloon flights are added to CONFIG['defaults'].
---

# BARREL

Loaders for BARREL, the balloon campaigns measuring precipitating relativistic
electrons (X-ray spectra, rate counters, magnetometer, ephemeris and
housekeeping). Data are L2 CDF files from SPDF.

## Layout

- `sspc.py`, `mspc.py`, `fspc.py` (slow, medium and fast spectra), `rcnt.py`
  (rate counters), `magn.py`, `ephm.py`, `hkpg.py`: one wrapper per data type,
  each calling `load(datatype=...)`.
- `load.py`: `load()`, the path template and loading.
- `config.py`: `CONFIG`, including `defaults`, a table of each flight's time range.
- `tests/test_barrel.py`, `README.md` (user guide). There is no `datasets()`.

## How it works

The keyword that selects a spacecraft is `probe`, the balloon flight ID such as
`'1A'` or `'2t'` (campaign number plus letter). Each wrapper passes `probe`,
`trange` and its data type to `load()`, which builds
`<level>/<probe>/<datatype>/bar_<probe>_<level>_<datatype>_%Y%m%d_<version>.cdf`
under `CONFIG['remote_data_dir']` (`https://spdf.gsfc.nasa.gov/pub/data/barrel/`),
lower-cases the file names from `dailynames()`, and downloads them. For
`ephm` the folder is `ephem`, not `ephm`. `level` (`'l2'`) and `version`
(`'v10'`) are `load()` keywords that the wrappers don't expose.

`load()` then reads the files with `cdf_to_tplot()`, adding the prefix
`brl<FLIGHT>_` taken from the file name, with the flight ID upper-cased
(`brl1A_SSPC`, `brl1D_FSPC1`). A user `prefix` goes before it.

## Things to know

- The wrappers take only `trange`, `probe`, `prefix`, `suffix`, `downloadonly`,
  `no_update`, `time_clip` and `force_download`; `get_support_data` and
  `notplot` exist only on `load()`, and there is no `varformat` or `varnames`.
- Each wrapper's default `trange` is a day in late January 2013, inside flight
  `1A`. `CONFIG['defaults']` lists every flight's time range, keyed by
  lower-case flight ID; `load()` reads it only when `trange=None`.
- `load()` returns None when no variables were created.
- The local data folder is `BARREL_DATA_DIR`, else `SPEDAS_DATA_DIR/barrel`, else
  `barrel_data/` (`config.py`). Setting `BARREL_NO_DOWNLOAD` turns downloads off.

## Tests

`python -m pyspedas.projects.barrel.tests.test_barrel`. CI runs it in
`.github/workflows/full_coverage.yml`.
