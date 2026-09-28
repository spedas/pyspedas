---
related_files:
  - pyspedas/projects/AGENTS.md
  - pyspedas/projects/stereo/__init__.py
  - pyspedas/projects/stereo/config.py
  - pyspedas/projects/stereo/load.py
  - pyspedas/projects/stereo/mag.py
  - pyspedas/projects/stereo/plastic.py
  - pyspedas/projects/stereo/swea.py
  - pyspedas/projects/stereo/ste.py
  - pyspedas/projects/stereo/sept.py
  - pyspedas/projects/stereo/sit.py
  - pyspedas/projects/stereo/let.py
  - pyspedas/projects/stereo/het.py
  - pyspedas/projects/stereo/waves.py
  - pyspedas/projects/stereo/beacon.py
  - pyspedas/projects/stereo/datasets.py
  - pyspedas/projects/stereo/README.md
  - pyspedas/projects/stereo/tests/test_stereo.py
  - pyspedas/utilities/datasets.py
  - pyspedas/preferences.py
  - .github/workflows/quick_tests.yml
maintenance: |
  Update when load.py changes an instrument branch, its per-instrument server, or
  its keywords, or when __init__.py adds a loader.
---

# STEREO

Loaders for the twin STEREO-A ("ahead") and STEREO-B ("behind") spacecraft:
IMPACT (MAG, SWEA, SEP suite, beacon), PLASTIC and WAVES. All data are daily
CDF files, from three different servers.

## Layout

- `mag.py`, `plastic.py`, `swea.py`, `ste.py`, `sept.py`, `sit.py`, `let.py`,
  `het.py`, `waves.py`, `beacon.py`: one thin wrapper per instrument, each
  returning `load(instrument=...)`.
- `load.py`: `load()`, the path-template chain and server choice.
- `datasets.py`: `datasets()`, lists STEREO datasets on CDAWeb through
  `find_datasets()` (`pyspedas/utilities/datasets.py`).
- `config.py`, `tests/test_stereo.py`, `README.md` (user guide; its examples use
  the pre-2.0 path `pyspedas.stereo`).

## How it works

`load()` asserts the instrument is known, then loops over `probe` (`'a'`, `'b'`
or a list), mapping it to the `ahead`/`behind` folder. For each probe it picks a
template and a server, runs `dailynames()` and `download()`, and after the loop
loads all files with one `cdf_to_tplot()` call.

- `mag`: Berkeley, `http://sprg.ssl.berkeley.edu/data/misc/stereo/`,
  `impact/level1/<dir>/mag/RTN/%Y/%m/ST<A|B>_L1_MAG[B]_RTN_%Y%m%d_V??.cdf`.
  `datatype='32hz'` selects the burst files (`MAGB`); anything else gives 8 Hz.
- `plastic`: STEREO Science Center,
  `http://stereo-ssc.nascom.nasa.gov/data/ins_data/`, Level 2 proton
  1D-Maxwellian moments only.
- `swea`, `ste`, `sept`, `sit`, `let`, `het`, `waves`, `beacon`: SPDF,
  `https://spdf.gsfc.nasa.gov/pub/data/stereo/`, under
  `<dir>/<level>/impact/...`, `<dir>/<level>/waves/...` or `<dir>/beacon/...`.

## Things to know

- `load()` overwrites `CONFIG['remote_data_dir']` on every call to match the
  instrument, so changing that value (or its saved preference) has no effect.
- `load()` has no `force_download` keyword, and `mag()` does not expose
  `coord`, so only RTN magnetometer files are reachable through the wrapper.
- Variables keep their CDF names with no probe in them (`BFIELD`, `PSD_FLUX`),
  so loading both probes in one call merges them; load each probe with its own
  `prefix` instead.
- Default `level` differs: `l1` for `swea`, `ste`, `sept`, `sit`, `let`, `het`;
  `l2` for `plastic`; `l3` for `waves` (`datatype` `'hfr'` or `'lfr'`).
- The local data folder is `STEREO_DATA_DIR`, else `SPEDAS_DATA_DIR/stereo`,
  else `stereo_data/` (`config.py`, which first applies saved preferences from
  `pyspedas/preferences.py`). Setting `STEREO_NO_DOWNLOAD` turns downloads off.

## Tests

`python -m pyspedas.projects.stereo.tests.test_stereo` (downloads data). CI runs
it in `.github/workflows/quick_tests.yml`.
