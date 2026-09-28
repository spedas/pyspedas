---
related_files:
  - pyspedas/projects/AGENTS.md
  - pyspedas/projects/secs/__init__.py
  - pyspedas/projects/secs/config.py
  - pyspedas/projects/secs/load.py
  - pyspedas/projects/secs/read_data_files.py
  - pyspedas/projects/secs/makeplots.py
  - pyspedas/projects/secs/README.md
  - pyspedas/projects/secs/tests/test_secs.py
  - pyspedas/preferences.py
  - pyproject.toml
  - .github/workflows/full_coverage.yml
maintenance: |
  Update when load.py changes its servers, file layout or return types, when
  read_data_files.py changes the output formats, or when make_plots() changes
  its inputs or output folder.
---

# SECS / EICS

Loader and map plots for the spherical elementary currents (SECS) and
equivalent ionospheric currents (EICS) derived from ground magnetometers over
North America and Greenland. Unlike the other missions, the loader returns
arrays, not tplot variables.

## Layout

- `load.py`: `load()`, also exported as `data`, which downloads, unzips and
  reads the files.
- `read_data_files.py`: `read_data_files()`, parses the per-time-step `.dat`
  files into a numpy array, pandas DataFrame or dict.
- `makeplots.py`: `make_plots()`, vector and contour maps of one time step,
  saved as image files. Not exported by `__init__.py`.
- `config.py`, `tests/test_secs.py`, `README.md`.

## How it works

`load(dtype='EICS' or 'SECS', trange=..., resolution=10)` requires `dtype`. It
downloads one zip per day, `<dtype>/%Y/%m/<dtype>%Y%m%d.zip`, from UCLA
(`CONFIG['remote_data_dir']`, `http://vmo.igpp.ucla.edu/data1/SECS/`), plus
`.zip.gz` files for 2007. With `spdf=True` it downloads from
`CONFIG['remote_data_dir_spdf']` instead, where files sit in `<dtype>/%Y/`, and
copies them into a month folder to match the UCLA layout. Each zip is extracted
once into `<dtype>/%Y/%m/%d/<dtype>%Y%m%d_%H%M%S.dat` (skipped if the day folder
exists). `downloadonly=True` returns the zip paths. Otherwise the `.dat` names
are generated every `resolution` seconds and passed to `read_data_files()`,
whose `out_type` is `'np'` (default), `'df'` or `'dc'`.

`make_plots(dtype, dtime='YYYY-MM-DD/hh:mm:ss', ...)` reads the single `.dat`
file for `dtime` from the local data folder, so the day must already be
downloaded and unzipped by `load()`. It draws on a Lambert conformal
`mpl_toolkits.basemap` map and writes `.jpeg` files (plus an EICS grid `.pdf`)
to `CONFIG['plots_dir']`.

## Things to know

- Keywords differ from the CDF loaders: `dtype` (not `datatype`), `no_download`
  (not `no_update`; `None` means use `CONFIG['no_download']`), `out_type`,
  `save_pickle` and `spdf`. There is no `prefix`, `suffix`, `notplot` or
  `time_clip`.
- Plotting needs the optional `basemap` package (`pyproject.toml` extra
  `maps`); `makeplots.py` only logs a message at import when it is missing.
- `save_pickle=True` writes `data_dc.pkl` to the current directory, and only for
  `out_type='dc'`.
- The local data folder is `LOCAL_SECS_DATA_DIR`, else `SPEDAS_DATA_DIR/secs`,
  else `secs_data/`; plots go to `PLOTS_SECS_DIR`, else
  `SPEDAS_DATA_DIR/secs_plots`, else `secs_plots/` (`config.py`, which first
  applies saved preferences from `pyspedas/preferences.py`). Setting
  `SECS_NO_DOWNLOAD` turns downloads off. `config.py` also sets `PROJ_LIB` from
  `CONDA_PREFIX` when that is defined.

## Tests

`python -m pyspedas.projects.secs.tests.test_secs` downloads data from UCLA and,
in the two plotting tests, from SPDF. Those tests call `make_plots()` with
`matplotlib.pyplot.show` patched, so they need `basemap`. CI runs the module in
`.github/workflows/full_coverage.yml`.
