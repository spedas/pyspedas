---
related_files:
  - pyspedas/projects/AGENTS.md
  - pyspedas/projects/psp/__init__.py
  - pyspedas/projects/psp/config.py
  - pyspedas/projects/psp/load.py
  - pyspedas/projects/psp/fields.py
  - pyspedas/projects/psp/spc.py
  - pyspedas/projects/psp/spe.py
  - pyspedas/projects/psp/spi.py
  - pyspedas/projects/psp/epihi.py
  - pyspedas/projects/psp/epilo.py
  - pyspedas/projects/psp/epi.py
  - pyspedas/projects/psp/rfs.py
  - pyspedas/projects/psp/filter.py
  - pyspedas/projects/psp/README.md
  - pyspedas/projects/psp/tests/test_psp.py
  - pyspedas/utilities/download.py
  - pyspedas/preferences.py
  - .github/workflows/quick_tests.yml
maintenance: |
  Update when load.py changes a path template, the server or credential logic,
  the version handling or the automatic prefixes, when a wrapper changes its
  level defaults, or when the quality-flag link between fields.py and filter.py
  changes.
---

# Parker Solar Probe

Loaders for PSP: FIELDS (magnetometer, RFS radio, DFB spectra, QTN, SCaM),
SWEAP (SPC, SPAN-e, SPAN-i) and ISOIS (EPI-Hi, EPI-Lo, merged EPI). Public data
are CDF files from SPDF. Given a username and password, the FIELDS, SPC and
SPAN-i loaders first try the instrument teams' servers for unpublished data.

## Layout

- `fields.py`, `spc.py`, `spe.py`, `spi.py`, `epihi.py`, `epilo.py`, `epi.py`:
  one wrapper per instrument, each calling `load()`.
- `load.py`: `load()`, path templates, server choice and loading.
- `rfs.py`: `rfs_variables_to_load()`, picks the `psp_fld_*` variables that hold
  data out of the ~1500 in an RFS file.
- `filter.py`: `filter_fields()`, quality-flag filtering of FIELDS MAG and RFS
  variables.
- `config.py`, `tests/test_psp.py`, `README.md` (user guide; its examples use the
  pre-2.0 path `pyspedas.psp`).

## How `load()` works

1. It lowercases `datatype`, except when `username` is set and the datatype is
   one of the unpublished upper-case names (`mag_RTN`, `mag_SC_1min`,
   `mag_RTN_4_Sa_per_Cyc`, `sqtn_rfs_V1V2`, ...).
2. An instrument branch picks the template and the variable prefix. SPDF paths
   start with `fields/<level>/<datatype>/%Y/psp_fld_...`, `sweap/spc/`,
   `sweap/spe/`, `sweap/spi/`, `isois/epihi/`, `isois/epilo/` or
   `isois/merged/`. Full-resolution `mag_rtn`, `mag_sc` and the generic FIELDS
   fallback are 6-hour files (`%Y%m%d%H`, `res=6*3600`); the rest are daily.
   `dfb_dc_spec`, `dfb_ac_spec` and their `xspec` forms call `load()` again for
   each spectrum type in the `spec_types` list that `fields()` supplies.
3. Download. Without `username`: `CONFIG['remote_data_dir']` (SPDF). With
   `username` and `password`, sent as basic auth through `download()`
   (`pyspedas/utilities/download.py`):
   - FIELDS: `CONFIG['fields_remote_data_dir']` (Berkeley SPRG), with monthly
     `%Y/%m/` folders and `spp_fld` names for L1; falls back to SPDF if nothing
     is found.
   - SPAN-i: `CONFIG['sweap_remote_data_dir']` (SWEAP at Harvard CfA), same
     fallback.
   - SPC: the SWEAP server with `psp_swp_spc_` names, then `spp_swp_spc_`
     (pre-release) names for the remaining days, then SPDF.
4. `cdf_to_tplot()` loads the files. For RFS datatypes with no `varformat` or
   `varnames`, only `rfs_variables_to_load()` is loaded, with support data.

## Things to know

- Versions: with `version=None` (default) `load()` matches `v??` (`v?.?` for
  `sqtn_rfs_v1v2` and `v3v4`) and sets `last_version=True`, so only the highest
  version is kept. `version='v02'` pins one file version and sets it False. The
  `last_version` keyword the wrappers expose is overwritten either way.
- Prefixes: `load()` adds `psp_spc_`, `psp_spe_`, `psp_spi_`, `psp_epihi_`,
  `psp_epilo_` or `psp_isois_` after the user prefix (`spp_spc_` for pre-release
  SPC files). FIELDS gets none: most of its CDF names already start with
  `psp_fld_`, but QTN files use bare names such as `electron_density`.
- Levels: `fields()` defaults `level` to `l3` for `rfs_hfr` and `rfs_lfr` and to
  `l2` otherwise, and forces `l3` for `merged_scam_wf` and the QTN types. `spc()`
  sets the level from `l3i`/`l2i` (upper case `L3`/`L2` with credentials).
  `spi()` turns `sf00_l3_mom`-style datatypes into `spi_sf00_l3_mom` at `l3`.
- Credentials come only from the `username` and `password` keywords of
  `fields()`, `spc()` and `spi()`; nothing is read from config or the
  environment. `spe()`, `epihi()`, `epilo()` and `epi()` have no credential
  keywords.
- Quality flags: `fields()` also loads `psp_fld_<level>_quality_flags` when MAG
  or RFS variables are loaded and stores its name in each variable's `qf_root`
  attribute. `filter_fields(tvars, dqflag=...)` reads `qf_root` and writes
  `<name>_<flags>` variables with flagged points removed (or kept, with
  `keep=True`).
- The local data folder is `PSP_DATA_DIR`, else `SPEDAS_DATA_DIR/psp`, else
  `psp_data/` (`config.py`, which first applies saved preferences from
  `pyspedas/preferences.py`); public and unpublished files share it. Setting
  `PSP_NO_DOWNLOAD` turns downloads off.

## Tests

`python -m pyspedas.projects.psp.tests.test_psp` downloads data. Several tests
pass dummy credentials (`username='hello'`) to route requests to the team
servers and their SPDF fallback. CI runs the module in
`.github/workflows/quick_tests.yml`.
