---
related_files:
  - pyspedas/projects/AGENTS.md
  - pyspedas/projects/akebono/__init__.py
  - pyspedas/projects/akebono/config.py
  - pyspedas/projects/akebono/load.py
  - pyspedas/projects/akebono/pws.py
  - pyspedas/projects/akebono/rdm.py
  - pyspedas/projects/akebono/orb.py
  - pyspedas/projects/akebono/pws_postprocessing.py
  - pyspedas/projects/akebono/rdm_postprocessing.py
  - pyspedas/projects/akebono/orb_postprocessing.py
  - pyspedas/projects/akebono/load_csv_file.py
  - pyspedas/projects/akebono/README.md
  - pyspedas/projects/akebono/tests/test_akebono.py
  - pyspedas/cotrans_tools/xyz_to_polar.py
  - .github/workflows/full_coverage.yml
maintenance: |
  Update when load.py changes a path template or the JAXA server, or when the
  RDM or orbit text parsing in *_postprocessing.py changes its variable names.
---

# Akebono

Loaders for the Akebono (EXOS-D) auroral satellite: plasma waves (PWS),
radiation monitor (RDM) and orbit. Data come from JAXA's DARTS archive, not
SPDF, and only PWS is in CDF.

## Layout

- `pws.py`, `rdm.py`, `orb.py`: the three public loaders, each calling `load()`
  and then its `*_postprocessing.py` module.
- `load.py`: `load()`, the path templates and download.
- `rdm_postprocessing.py`, `orb_postprocessing.py`: parse the downloaded text
  files and create tplot variables with `store_data()`.
  `pws_postprocessing.py` is a placeholder that returns its input.
- `load_csv_file.py`: reads whitespace-separated text files (plain or gzip) into
  a pandas DataFrame.
- `config.py`, `tests/test_akebono.py`, `README.md` (user guide). There is no
  `datasets()`. `__init__.py` imports only `pws`, `rdm` and `orb`, so
  `pyspedas.projects.akebono.load` is the module, not the function.

## How it works

`load()` picks a template under `CONFIG['remote_data_dir']`
(`https://data.darts.isas.jaxa.jp/pub/akebono/`) and downloads the files:

- `pws`: `pws/NPW-DS/%Y/ak_h1_pws_%Y%m%d_v??.cdf`, read with `cdf_to_tplot()`
  under the prefix `akb_pws_` (`akb_pws_RX1`).
- `rdm`: `rdm/%Y/sf%y%m%d` text files. `load()` returns the file list, and
  `rdm_postprocessing()` builds `akb_rdm_FEIO` plus position variables named
  `akb_L`, `akb_MLT` and so on (no `rdm_`).
- `orb`: `orbit/daily/%Y%m/ED%y%m%d.txt`. `orb_postprocessing()` builds
  `akb_orb_geo` (Re) and footprint, MLT and geocentric variables, using
  `xyz_to_polar()` (`pyspedas/cotrans_tools/xyz_to_polar.py`).

A user `prefix` goes before `akb_`; `None` is treated as empty.

## Things to know

- For `rdm` and `orb`, `varformat`, `varnames`, `get_support_data` and
  `time_clip` have no effect, and `notplot=True` returns the downloaded file
  list without creating variables.
- `pws()` accepts `datatype` and `level`, but the file path is fixed to the
  `ak_h1_pws` files.
- The local data folder is `AKEBONO_DATA_DIR`, else `SPEDAS_DATA_DIR/akebono`,
  else `akebono_data/` (`config.py`). Setting `AKEBONO_NO_DOWNLOAD` turns
  downloads off.

## Tests

`python -m pyspedas.projects.akebono.tests.test_akebono`. CI runs it in
`.github/workflows/full_coverage.yml`.
