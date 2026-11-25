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
  - pyspedas/projects/erg/tests/test_erg_s3.py
  - pyspedas/projects/erg/tests/test_erg.py
  - pyspedas/projects/erg/tests/test_erg_ground.py
  - pyspedas/projects/erg/tests/test_erg_cotrans.py
  - RULES.md
maintenance: |
  Update when satellite/erg/load.py changes, when config.py changes the data server or
  environment variables, or when __init__.py adds or renames a loader or tool.
---

# Arase (ERG)

Every change here follows `RULES.md` at the repository root. Read it before
you change code here.

Loaders for the Arase (ERG) satellite and for the ground-based networks served by the ERG
Science Center (ERG-SC, ISEE, Nagoya University), plus Arase coordinate transforms and
particle products.

## Layout

- `satellite/`: Arase loaders, the shared `load()`, the SGA/SGI/DSI/J2000 transforms and
  the particle products. Has its own AGENTS.md.
- `ground/`: magnetometer, all-sky imager, SuperDARN, riometer and VLF loaders. Has its own
  AGENTS.md.
- `config.py`: `CONFIG` with `local_data_dir`, independent ground, satellite and att
  `*_remote_data_dir` / `*_remote_data_layout` pairs, deprecated compatibility
  `remote_data_dir`, `no_download`, and `resolve_source(family)`.
- `__init__.py`: imports every loader and the `*_part_products` and coordinate tools under
  its short name
  (`pyspedas.projects.erg.mgf`, `...sd_fit`, `...erg_cotrans`).
- `tests/`: unittest modules; `test_erg_load.py` needs no network and `test_erg_spdf.py`
  uses SPDF; `test_erg_s3.py` uses S3 satellite data with SPDF attitude,
  and the others download from ERG-SC.
- `README.md`: user guide with examples.

## How a loader works

The source-routing configuration API is experimental; its interface is being
evaluated with user feedback before it is finalized (see `config.py`).

Every loader, satellite or ground, builds its own file path template and calls `load()` in
`satellite/erg/load.py`. For `mgf()` (`satellite/erg/mgf/mgf.py`) the template is
`mgf/l2/8sec/%Y/%m/erg_mgf_l2_8sec_%Y%m%d_v??.??.cdf`; ground templates are also
family-relative (see `ground/geomag/gmag_isee_fluxgate.py`). Each wrapper passes
`**resolve_source(family)` to select satellite, att, or ground explicitly. `load()`:

1. expands the template with `dailynames()` using the caller's `file_res` (daily or hourly);
2. translates product directories and EFD filename case when the explicit layout
   is `spdf`, independently of the URL, and uses those URL-relative paths directly
   beneath `local_data_dir`; `download()` selects
   the last version only for wildcard paths and passes `uname`/`passwd` as credentials;
3. loads the files with `cdf_to_tplot()`, using the caller's `prefix` and `suffix`;
4. with `notplot=True`, adds the last file's CDF attributes to the returned dicts under
   `['CDF']` (`VATT`, `GATT`, and `FILENAME`, the full file list), which several wrappers use to build variables.

Each wrapper except `att()` then prints the PI and rules-of-the-road text (`ror=True`, the default) from
the CDF global attributes via `satellite/erg/get_gatt_ror.py`, and post-processes the
variables (fill value clipping, plot options, renaming).

## Things to know

- Server: `https://ergsc.isee.nagoya-u.ac.jp/data/ergsc/`, overridden by
  `ERG_REMOTE_DATA_DIR` (legacy common base URL), or independently by
  `ERG_GROUND_REMOTE_DATA_DIR`, `ERG_ATT_REMOTE_DATA_DIR`, and
  `ERG_SATELLITE_REMOTE_DATA_DIR`. The matching `*_REMOTE_DATA_LAYOUT` variables
  select layouts explicitly: satellite/att accept `ergsc` or `spdf`; ground accepts
  `ergsc`. No source fallback is attempted. SPDF satellite URL:
  `https://spdf.gsfc.nasa.gov/pub/data/arase/`. Local folder: `ERG_DATA_DIR`, else `SPEDAS_DATA_DIR/ergsc`, else
  `erg_data/`. `ERG_NO_DOWNLOAD` set to true turns downloads off. Stored preferences
  (`pyspedas/preferences.py`) are applied first, then these variables.
- To send credentials, pass `uname` and `passwd` to the wrapper.
- All satellite wrappers put explicit `version` strings into the path template; `None`
  uses a wildcard. The shared `load()` has a `version` argument that it does not use. Wrappers also differ in which keywords they pass to
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
