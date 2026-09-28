---
related_files:
  - pyspedas/projects/AGENTS.md
  - pyspedas/projects/geotail/__init__.py
  - pyspedas/projects/geotail/config.py
  - pyspedas/projects/geotail/load.py
  - pyspedas/projects/geotail/mgf.py
  - pyspedas/projects/geotail/efd.py
  - pyspedas/projects/geotail/lep.py
  - pyspedas/projects/geotail/cpi.py
  - pyspedas/projects/geotail/epic.py
  - pyspedas/projects/geotail/pwi.py
  - pyspedas/projects/geotail/datasets.py
  - pyspedas/projects/geotail/README.md
  - pyspedas/projects/geotail/tests/test_geotail.py
  - pyspedas/utilities/datasets.py
  - .github/workflows/full_coverage.yml
maintenance: |
  Update when load.py gains or changes an instrument or datatype branch, or when
  a wrapper is added to __init__.py.
---

# Geotail

Loaders for the Geotail magnetotail mission: magnetic field, electric field,
plasma, energetic particles and plasma waves. All data are CDF files from SPDF.

## Layout

- `mgf.py`, `efd.py`, `lep.py`, `cpi.py`, `epic.py`, `pwi.py`: one wrapper per
  instrument, each calling `load()`.
- `load.py`: `load()`, the file-path chain and loading for all instruments.
- `datasets.py`: `datasets()`, lists Geotail datasets on CDAWeb through
  `find_datasets()` (`pyspedas/utilities/datasets.py`).
- `config.py`, `tests/test_geotail.py`, `README.md` (user guide).

## How it works

Each wrapper calls `load(instrument=...)`; `epic()` passes `instrument='epi'`.
`load()` picks a path template under `CONFIG['remote_data_dir']`
(`https://spdf.gsfc.nasa.gov/pub/data/geotail/`), mostly
`<instrument>/<instrument>_<datatype>/%Y/ge_<datatype>_<instrument>_%Y%m%d_v??.cdf`,
and runs the usual `dailynames()`, `download()`, `cdf_to_tplot()` pipeline.
EPIC files sit under `epic/epi_<datatype>/`.

Every wrapper defaults to `datatype='k0'` (key parameters). `mgf` also takes
`eda3sec` and `edb3sec` (3-second data, under `mgf/<datatype>_mgf/`); `lep` has
a branch only for `k0`.

## Things to know

- Variable names come straight from the CDF with no instrument prefix
  (`IB_vector`, `N0`, `SW_P_Den`).
- `epic()` is the only wrapper with post-processing: it sets spectrogram and log
  options on `IDiffI_I`.
- `time_clip` defaults to False in the wrappers and in `load()`.
- The local data folder is `GEOTAIL_DATA_DIR`, else `SPEDAS_DATA_DIR/geotail`,
  else `geotail_data/` (`config.py`). Setting `GEOTAIL_NO_DOWNLOAD` turns
  downloads off.

## Tests

`python -m pyspedas.projects.geotail.tests.test_geotail`. CI runs it in
`.github/workflows/full_coverage.yml`.
