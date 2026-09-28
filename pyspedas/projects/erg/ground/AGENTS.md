---
related_files:
  - pyspedas/projects/erg/AGENTS.md
  - pyspedas/projects/erg/__init__.py
  - pyspedas/projects/erg/ground/__init__.py
  - pyspedas/projects/erg/ground/geomag/gmag_isee_fluxgate.py
  - pyspedas/projects/erg/ground/geomag/gmag_isee_induction.py
  - pyspedas/projects/erg/ground/geomag/gmag_stel_fluxgate.py
  - pyspedas/projects/erg/ground/geomag/gmag_stel_induction.py
  - pyspedas/projects/erg/ground/geomag/gmag_magdas_1sec.py
  - pyspedas/projects/erg/ground/geomag/gmag_mm210.py
  - pyspedas/projects/erg/ground/camera/camera_omti_asi.py
  - pyspedas/projects/erg/ground/radar/superdarn/sd_fit.py
  - pyspedas/projects/erg/ground/radar/superdarn/get_sphcntr.py
  - pyspedas/projects/erg/ground/riometer/isee_brio.py
  - pyspedas/projects/erg/ground/vlf/isee_vlf.py
  - pyspedas/projects/erg/satellite/erg/load.py
  - pyspedas/projects/erg/satellite/erg/get_gatt_ror.py
  - pyspedas/projects/erg/tests/test_erg_ground.py
maintenance: |
  Update when a ground loader is added or renamed, when a loader's hard-coded site list or
  output naming changes, or when the ground loaders stop sharing the satellite load().
---

# ERG-SC ground-based data

Loaders for ground networks whose data the ERG Science Center serves: magnetometers,
all-sky imagers, SuperDARN radars, riometers and VLF receivers. There is no ground-specific
`load()`; every module reuses `pyspedas/projects/erg/satellite/erg/load.py`.

## Layout

- `geomag/gmag_isee_fluxgate.py`, `geomag/gmag_isee_induction.py`: ISEE (formerly STEL)
  fluxgate and induction magnetometers.
- `geomag/gmag_stel_fluxgate.py`, `geomag/gmag_stel_induction.py`: old names that pass all
  arguments to the ISEE loaders.
- `geomag/gmag_magdas_1sec.py`: MAGDAS 1-second magnetometer data.
- `geomag/gmag_mm210.py`: 210 MM magnetometer chain.
- `camera/camera_omti_asi.py`: OMTI all-sky imagers, by site and `wavelength` (default 5577).
- `radar/superdarn/sd_fit.py`: SuperDARN fitacf data by radar; `get_sphcntr.py` computes
  cell-centre positions for the range-gate tables.
- `riometer/isee_brio.py`: ISEE broad-beam riometers.
- `vlf/isee_vlf.py`: ISEE VLF receivers (`cal_gain=True` applies the CDF's gain calibration).
- The `__init__.py` files are empty; `pyspedas/projects/erg/__init__.py` exports the loaders.

## How a ground loader works

Take `gmag_isee_fluxgate()`:

1. `site` (`'all'`, a list, or a space-separated string) is lower-cased and intersected
   with a hard-coded list of station codes; unknown codes are dropped silently. `datatype`
   (time resolution) is handled the same way.
2. For each site and resolution it builds a template such as
   `ground/geomag/isee/fluxgate/1min/<site>/%Y/isee_fluxgate_1min_<site>_%Y%m%d_v??.cdf`
   (hourly files for 64 Hz) and calls `load()` with prefix `isee_fluxgate_` and suffix
   `_<site>`.
3. It prints the station's PI and rules of the road from the CDF global attributes
   (`pyspedas/projects/erg/satellite/erg/get_gatt_ror.py`).
4. It renames the loaded variables to the IDL SPEDAS names
   (`isee_fluxgate_mag_<site>_<res>_hdz`), clips fill values, and sets ylim and labels.

The other loaders follow the same site loop. Several (`isee_brio`, `isee_vlf`,
`gmag_isee_induction`, `camera_omti_asi`, `sd_fit`) reopen the CDF with cdflib after
loading, to read fill values, calibration or position tables that `cdf_to_tplot()` skips.

## Things to know

- The returned names come from the post-load renaming, not from `prefix` + CDF name:
  `isee_brio()` loads with a temporary `iseetmp_` prefix and renames to
  `isee_brio<freq>_<site>_<res>_<param>`.
- Hourly 1h fluxgate data live in the 1min files, so `datatype='1h'` loads 1min files.
- `sd_fit()` loads one file per radar per day (version wildcard `*`) and builds numbered
  variables that follow the CDF's `position_tbl_<n>` tables (`sd_<site>_pwr_<n>`,
  `sd_<site>_vlos_<n>`, ...); `compact=True` keeps only a minimal set.
- Site lists are fixed in each module; a new station needs an edit there.
- None of these loaders take `probe` or `level`; the level is part of the template.

## Tests

`pyspedas/projects/erg/tests/test_erg_ground.py` (downloads data).
