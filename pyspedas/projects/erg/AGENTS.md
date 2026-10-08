---
related_files:
  - pyspedas/projects/AGENTS.md
  - pyspedas/projects/erg/ground/AGENTS.md
  - pyspedas/projects/erg/satellite/AGENTS.md
  - pyspedas/projects/erg/__init__.py
  - pyspedas/projects/erg/config.py
  - pyspedas/projects/erg/README.md
  - pyspedas/projects/erg/satellite/erg/load.py
  - pyspedas/projects/erg/satellite/erg/get_gatt_ror.py
  - pyspedas/projects/erg/satellite/erg/mgf/mgf.py
  - pyspedas/projects/erg/ground/geomag/gmag_isee_fluxgate.py
  - pyspedas/preferences.py
  - pyspedas/utilities/dailynames.py
  - pyspedas/utilities/download.py
  - pyspedas/tplot_tools/importers/cdf_to_tplot.py
  - pyspedas/projects/erg/tests/test_erg_load.py
  - pyspedas/projects/erg/tests/test_erg_spdf.py
  - pyspedas/projects/erg/tests/test_erg.py
  - pyspedas/projects/erg/tests/test_erg_ground.py
  - pyspedas/projects/erg/tests/test_erg_cotrans.py
maintenance: |
  Update when satellite/erg/load.py changes, when config.py changes the data server or
  environment variables, or when __init__.py adds or renames a loader or tool.
---

# Arase (ERG)

Loaders for the Arase (ERG) satellite and for the ground-based networks served by the ERG
Science Center (ERG-SC, ISEE, Nagoya University), plus Arase coordinate transforms and
particle products. The code follows IDL SPEDAS's `erg` plug-in closely.

## Layout

- `satellite/`: Arase loaders, the shared `load()`, the SGA/SGI/DSI/J2000 transforms and
  the particle products. Has its own AGENTS.md.
- `ground/`: magnetometer, all-sky imager, SuperDARN, riometer and VLF loaders. Has its own
  AGENTS.md.
- `config.py`: `CONFIG` with `local_data_dir`, separate `ground_remote_data_dir` and
  `satellite_remote_data_dir`, legacy `remote_data_dir`, and `no_download`.
- `__init__.py`: imports every loader and tool under its short name
  (`pyspedas.projects.erg.mgf`, `...sd_fit`, `...erg_cotrans`).
- `tests/`: unittest modules; they download from ERG-SC.
- `README.md`: user guide with examples.

## How a loader works

Every loader, satellite or ground, builds its own file path template and calls `load()` in
`satellite/erg/load.py`. For `mgf()` (`satellite/erg/mgf/mgf.py`) the template is
`satellite/erg/mgf/l2/8sec/%Y/%m/erg_mgf_l2_8sec_%Y%m%d_v??.??.cdf`; ground templates start
with `ground/` (see `ground/geomag/gmag_isee_fluxgate.py`). `load()`:

1. expands the template with `dailynames()` using the caller's `file_res` (daily or hourly);
2. selects the ground or satellite URL, strips the corresponding template prefix for
   remote names, translates SPDF product directories and EFD filename case, and
   uses those URL-relative paths directly beneath `local_data_dir`; `download()` selects
   the last version only for wildcard paths and passes `uname`/`passwd` as credentials;
3. loads the files with `cdf_to_tplot()`, using the caller's `prefix` and `suffix`;
4. with `notplot=True`, adds each file's CDF attributes to the returned dicts under
   `['CDF']` (`VATT`, `GATT`, `FILENAME`), which several wrappers use to build variables.

The wrapper then prints the PI and rules-of-the-road text (`ror=True`, the default) from
the CDF global attributes via `satellite/erg/get_gatt_ror.py`, and post-processes the
variables (fill value clipping, plot options, renaming).

## Things to know

- Server: `https://ergsc.isee.nagoya-u.ac.jp/data/ergsc/`, overridden by
  `ERG_REMOTE_DATA_DIR` (legacy common base URL), or independently by
  `ERG_GROUND_REMOTE_DATA_DIR` and `ERG_SATELLITE_REMOTE_DATA_DIR`. SPDF satellite URL:
  `https://spdf.gsfc.nasa.gov/pub/data/arase/`. Local folder: `ERG_DATA_DIR`, else `SPEDAS_DATA_DIR/ergsc`, else
  `erg_data/`. `ERG_NO_DOWNLOAD` turns downloads off. Stored preferences
  (`pyspedas/preferences.py`) are applied first, then these variables.
- Some data sets need an ERG-SC account; pass `uname` and `passwd` to the wrapper.
- All satellite wrappers put explicit `version` strings into the path template; `None`
  uses a wildcard. The shared `load()` retains its unused `version` argument for compatibility. Wrappers also differ in which keywords they pass to
  `load()`, so check before relying on one (for example `varnames`).
- Rules of the road are printed with `print()`, not `logging`, unless `ror=False`.
- Names start with the product: `erg_mgf_l2_mag_8sec_dsi`, `erg_mepe_l2_3dflux_FEDU`,
  `isee_fluxgate_mag_ktb_1min_hdz`, `sd_<site>_vlos_<n>`.
- `README.md` examples use the pre-2.0 path `pyspedas.erg`; the package is now
  `pyspedas.projects.erg`.

## Tests

`tests/test_erg.py` covers the satellite loaders and `get_dist` routines,
`tests/test_erg_ground.py` the ground loaders, `tests/test_erg_cotrans.py` the transforms;
the other modules cover the particle products of one instrument each.
`tests/test_erg_load.py` checks routing, cache paths, URL overrides and version handling
without network access. `tests/test_erg_spdf.py` tests satellite loading from SPDF in a
fresh cache, including explicit versions; it runs in the SPDF-heavy full coverage shard,
not in quick_tests, and excludes particle get_dist tests.
