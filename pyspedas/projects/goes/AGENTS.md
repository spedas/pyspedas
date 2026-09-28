---
related_files:
  - pyspedas/projects/AGENTS.md
  - pyspedas/projects/goes/__init__.py
  - pyspedas/projects/goes/config.py
  - pyspedas/projects/goes/load.py
  - pyspedas/projects/goes/load_orbit.py
  - pyspedas/projects/goes/README.md
  - pyspedas/projects/goes/tests/test_goes.py
  - pyspedas/utilities/pyspedas_functools.py
  - pyspedas/tplot_tools/importers/netcdf_to_tplot.py
  - .github/workflows/full_coverage.yml
maintenance: |
  Update when load() or loadr() gains an instrument, datatype branch or keyword,
  when a NOAA or SPDF server URL changes, or when __init__.py adds a loader.
---

# GOES

Loaders for the GOES geostationary satellites: GOES 1-15 in the original NOAA
NetCDF format, GOES-R (GOES-16 and later), and GOES 8-15 data reprocessed into
the GOES-R format. Unlike most missions the science files are NetCDF, not CDF.

## Layout

- `load.py`: `load()` (GOES 1-15, and the entry point for all probes) and
  `loadr()` (GOES-R format files).
- `load_orbit.py`: `load_orbit()`, SSC ephemeris CDFs from SPDF; exported as
  `orbit`.
- `__init__.py`: defines the instrument loaders; there are no wrapper modules.
- `config.py`, `tests/test_goes.py`, `README.md` (user guide).

## How `load()` works

`__init__.py` makes each instrument loader with
`better_partial(load, instrument=...)` (`pyspedas/utilities/pyspedas_functools.py`,
a plain `functools.partial`), so `fgm`, `eps`, `epead`, `maged`, `magpd`,
`hepad`, `xrs`, `euvs`, `mag`, `mpsh` and `sgps` all have `load()`'s signature.
The first seven are GOES 1-15 instruments; `euvs`, `xrs`, `mag`, `mpsh`, `sgps`
are GOES-R instruments.

`probe` and `instrument` may be lists. `load()` sends probes above 15, and every
probe when `goes_r=True`, to `loadr()`; it loads the rest itself:

- GOES 1-15: templates under `CONFIG['remote_data_dir']` (NCEI
  `.../goes-space-environment-monitor/access/`). Averaged data are monthly files
  under `avg/%Y/%m/goes<N>/netcdf/`; full-resolution data are daily files under
  `full/`. The time variable is `time_tag`.
- `loadr()`: daily files from NGDC
  (`https://data.ngdc.noaa.gov/platforms/solar-space-observing-satellites/goes/goes<N>/l2/data/`)
  or, for reprocessed GOES 8-15, from NCEI `.../access/science/`. Both URLs are
  hard-coded in `loadr()`, not read from `CONFIG`. Reprocessed data exist only
  for `mag` (hires) and `xrs`; `euvs`, `mpsh` and `sgps` are skipped with a
  warning, and GOES 1-15 instrument names have no branch in `loadr()`.

Each probe and instrument goes through `dailynames()`, `download()` and
`netcdf_to_tplot()` (`pyspedas/tplot_tools/importers/netcdf_to_tplot.py`). When
`xrs` is requested, the `*_xrs_*_flux` variables get `ylog`.

## Things to know

- `datatype` roughly means resolution, and the accepted strings differ per
  instrument and generation (`fgm`: `512ms`/`full`, `5min`, else 1 min; GOES-R
  `mag`: `hi`/`full`/`hires`/`0.1sec`, else 1 min). An unrecognized value falls
  into the instrument's `else` branch, which is low resolution for some
  instruments and full resolution for others, so read the branch in `load.py`.
- Names: an empty `prefix` or `'probename'` gives `g<probe>_<instrument>_`
  (`g15_fgm_BX_1`, `g16_mag_b_gsm`, `g15_orbit_XYZ_GSM`). Any other `prefix`
  replaces it entirely, so multi-probe loads then collide.
- `load()` has no `varformat`, `varnames`, `get_support_data` or `notplot`;
  `load_orbit()` has them. `time_clip` defaults to True in both.
- `load_orbit()` uses the hard-coded SPDF URL `https://spdf.gsfc.nasa.gov/pub/data/goes/`
  (yearly `goes<N>_ephemeris_ssc_%Y0101_v??.cdf` files).
- All three servers share one local folder, each mirroring its server paths:
  `GOES_DATA_DIR`, else `SPEDAS_DATA_DIR/goes`, else `goes_data/` (`config.py`).
  Setting `GOES_NO_DOWNLOAD` turns downloads off.

## Tests

`python -m pyspedas.projects.goes.tests.test_goes` covers both generations and
the reprocessed data (large files). CI runs it in
`.github/workflows/full_coverage.yml`.
