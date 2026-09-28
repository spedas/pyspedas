---
related_files:
  - pyspedas/tplot_tools/AGENTS.md
  - pyspedas/tplot_tools/importers/cdf_to_tplot.py
  - pyspedas/tplot_tools/importers/netcdf_to_tplot.py
  - pyspedas/tplot_tools/importers/sts_to_tplot.py
  - pyspedas/tplot_tools/importers/tplot_restore.py
  - pyspedas/tplot_tools/exporters/tplot_save.py
  - pyspedas/tplot_tools/store_data.py
  - pyspedas/tplot_tools/options.py
  - pyspedas/tplot_tools/data_att_getters_setters.py
  - pyspedas/projects/goes/load.py
  - pyspedas/projects/poes/load.py
  - pyspedas/projects/maven/maven_load.py
maintenance: |
  Update when cdf_to_tplot changes which CDF attributes it reads or how it fills
  .attrs and plot options, when a reader gains or loses a keyword, or when a new
  file format reader is added here.
---

# importers

Readers that turn data files into tplot variables. Mission loaders call them after
downloading; all four are re-exported from `pyspedas`.

## Layout

- `cdf_to_tplot.py`: ISTP CDF reader built on cdflib. Nearly every loader uses it.
- `netcdf_to_tplot.py`: netCDF4 reader, used by GOES (`pyspedas/projects/goes/load.py`) and POES L1b (`pyspedas/projects/poes/load.py`).
- `sts_to_tplot.py`: MAVEN STS text files (`pyspedas/projects/maven/maven_load.py`).
- `tplot_restore.py`: a `.tplot` file from IDL `tplot_save` (read with `scipy.io.readsav`), or any other suffix as a pickle from `tplot_save()` (`pyspedas/tplot_tools/exporters/tplot_save.py`).

## How cdf_to_tplot() works

1. Attributes come from `mastercdf` when given, else from each file itself.
2. Variables are kept by `VAR_TYPE`: `data` always, `support_data` with `get_support_data=True`,
   `ignore_data` with `get_ignore_data=True`. Passing `varformat` or `varnames` turns support
   data on, so named variables load whatever their type.
3. The time variable is `DEPEND_TIME`, else `DEPEND_0`; a variable with neither is
   non-record-varying. Epochs go through `cdflib.cdfepoch.to_datetime` and are cached per file;
   `center_measurement=True` shifts them by `DELTA_PLUS_VAR`/`DELTA_MINUS_VAR`.
4. `FILLVAL` becomes NaN in float variables and 0 in integer ones. `DEPEND_1`..`DEPEND_3`
   become `v1`..`v3` (or `v`), and their `UNITS` go into `data_att`.
5. Arrays from all files are concatenated per variable, then `store_data()` is called with
   `attrs['CDF']` (`VATT`, `GATT`, `FILENAME`, `LABELS`) and `attrs['data_att']` (`units`,
   `depend_N_units`, `coord_sys` from a `COORDINATE_SYSTEM` attribute).
6. Plot options from attributes: `DISPLAY_TYPE` spectrogram sets `spec`, `SCALETYP` log sets
   `ylog` or `zlog`, `LABLAXIS` sets `ytitle`, `UNITS` sets `ysubtitle` (or `ztitle` for spectra).
7. Returns the list of names. `notplot=True` returns a dict of arrays instead, and
   `merge=True` concatenates onto existing variables of the same name along time.

## Things to know

- `varformat` and `exclude_format` are regular expressions matched with `re.match` after `*` is
  turned into `.*`; a list or a space-separated string becomes an alternation. A `?` is a regex
  quantifier here, not a one-character wildcard.
- Names are `prefix + cdf_name + suffix`; filters also try the prefixed name when a prefix or
  suffix is set.
- Without `merge=True`, each call overwrites existing variables of the same name.
- `netcdf_to_tplot()` finds each variable's time from its first dimension (falling back to
  `time` or `time_tag`) and converts it using the `units` attribute; `strict_time=False` also loads
  variables whose length differs from the time axis.
- `sts_to_tplot()` supports `merge` and `notplot` like the CDF reader.
- `tplot_restore()` of a pickle also replaces `pyspedas.tplot_tools.tplot_opt_glob`.
