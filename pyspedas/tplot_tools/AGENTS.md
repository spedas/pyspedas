---
related_files:
  - AGENTS.md
  - pyspedas/tplot_tools/MPLPlotter/AGENTS.md
  - pyspedas/tplot_tools/importers/AGENTS.md
  - pyspedas/tplot_tools/tplot_math/AGENTS.md
  - pyspedas/tplot_tools/__init__.py
  - pyspedas/tplot_tools/store_data.py
  - pyspedas/tplot_tools/get_data.py
  - pyspedas/tplot_tools/del_data.py
  - pyspedas/tplot_tools/tplot_rename.py
  - pyspedas/tplot_tools/tplot_copy.py
  - pyspedas/tplot_tools/replace_data.py
  - pyspedas/tplot_tools/tnames.py
  - pyspedas/tplot_tools/wildcard_routines.py
  - pyspedas/tplot_tools/is_pseudovariable.py
  - pyspedas/tplot_tools/options.py
  - pyspedas/tplot_tools/tplot_options.py
  - pyspedas/tplot_tools/timespan.py
  - pyspedas/tplot_tools/xlim.py
  - pyspedas/tplot_tools/tlimit.py
  - pyspedas/tplot_tools/ylim.py
  - pyspedas/tplot_tools/zlim.py
  - pyspedas/tplot_tools/timebar.py
  - pyspedas/tplot_tools/databar.py
  - pyspedas/tplot_tools/link.py
  - pyspedas/tplot_tools/spedas_colorbar.py
  - pyspedas/tplot_tools/rgb_color.py
  - pyspedas/tplot_tools/data_att_getters_setters.py
  - pyspedas/tplot_tools/time_double.py
  - pyspedas/tplot_tools/time_string.py
  - pyspedas/tplot_tools/exporters/tplot_save.py
  - pyspedas/tplot_tools/exporters/tplot_ascii.py
  - pyspedas/tplot_tools/importers/tplot_restore.py
  - pyspedas/__init__.py
  - pyspedas/utilities/tcopy.py
  - pyspedas/utilities/tests/test_math.py
  - pyspedas/utilities/tests/test_utilities_plot.py
  - pyspedas/utilities/tests/test_utilities_tplot_wildcard.py
  - pyspedas/utilities/tests/test_utilities_time.py
maintenance: |
  Update when the layout of a stored variable changes (store_data, plot_options,
  data_att), when a module-level global is added or rebound, or when a function
  moves between tplot_tools and its subfolders.
---

# tplot_tools

Storage, lookup, options, time helpers and plotting for tplot variables. This is the
former PyTplot package, vendored into pySPEDAS; file headers still credit PyTplot.
Most names are re-exported from `pyspedas` itself (`pyspedas/__init__.py`).

## Layout

- `__init__.py`: defines the globals `data_quants`, `tplot_opt_glob`, `lim_info`, then imports every public function.
- `store_data.py`, `get_data.py`, `del_data.py`, `tplot_rename.py`, `tplot_copy.py`, `replace_data.py`: create, read, delete, rename, copy and overwrite variables.
- `tnames.py`, `wildcard_routines.py`: name lookup; most functions expand names with `tplot_wildcard_expand()`.
- `options.py` (per variable), `tplot_options.py` (global), `xlim.py`, `ylim.py`, `zlim.py`, `tlimit.py`, `timespan.py`: plot settings.
- `data_att_getters_setters.py`: `get_coords`/`set_coords`, `get_units`/`set_units`.
- `time_double.py`, `time_string.py`: `time_double`/`time_float` and `time_string`/`time_datetime`, used package-wide.
- `timebar.py`, `databar.py`, `link.py`, `spedas_colorbar.py`, `rgb_color.py`: decorations, linked variables, color tables.
- `MPLPlotter/`: `tplot()` and the matplotlib renderers ([MPLPlotter/AGENTS.md](MPLPlotter/AGENTS.md)).
- `tplot_math/`: arithmetic, cleaning and spectra on variables ([tplot_math/AGENTS.md](tplot_math/AGENTS.md)).
- `importers/`: CDF, netCDF, STS and saved-file readers ([importers/AGENTS.md](importers/AGENTS.md)).
- `exporters/`: `tplot_save()` (pickle, `exporters/tplot_save.py`) and `tplot_ascii()` (CSV, `exporters/tplot_ascii.py`).

## How a variable is stored

- `store_data(name, data={'x': t, 'y': y, 'v': v}, attr_dict={})` converts `x` (Unix seconds,
  datetimes, datetime64 or strings) to `datetime64[ns]` and stores an `xarray.DataArray` with dims
  `time` plus `v_dim` or `v1_dim`, `v2_dim`, `v3_dim`. `v` (or `v2` when `v1`, `v2` are given) also
  becomes the `spec_bins` coordinate used by spectrograms. Optional `dy` holds error bars.
- `attr_dict` becomes `.attrs`, and a fresh `.attrs['plot_options']` is added (`xaxis_opt`,
  `yaxis_opt`, `zaxis_opt`, `line_opt`, `extras`, `overplots_mpl`, `time_bar`, `error`, ...).
  Calling `store_data` on an existing name replaces the variable and its options;
  `replace_data()` swaps in values of the same shape and keeps them.
- No `x` key means non-record-varying: stored as a plain dict `{'data': ..., 'name': ...}`, which
  many routines special-case with `isinstance(..., dict)`.
- `data=['a', 'b']` (or `'a b'`) makes a pseudovariable: a copy of the first component whose
  `plot_options['overplots_mpl']` lists all components; `is_pseudovariable()` detects it.
- `get_data(name)` returns a namedtuple (`times`, `y`, then `v`/`v1`/`v2`/`v3` or `dy`) with times
  as float Unix seconds; `dt=True` gives datetime64, `xarray=True` the DataArray, and
  `metadata=True` the live `.attrs` dict. `pyspedas.get()` defaults to `dt=True, units=True`.
  A missing name returns `None` with only an info-level log.
- Loaders fill `.attrs['CDF']` (`VATT`, `GATT`, `FILENAME`, `LABELS`) and `.attrs['data_att']`
  (`coord_sys`, `units`, `depend_1_units`, ...). cotrans and the geopack wrappers read
  `coord_sys` and `units` through `data_att_getters_setters.py`.

## Things to know

- Read globals through the module: `pyspedas.tplot_tools.data_quants[name]`. `tplot_rename()`
  rebinds `data_quants` to a new `OrderedDict` and `tplot_restore()`
  (`importers/tplot_restore.py`) rebinds `tplot_opt_glob`, so a name imported with
  `from pyspedas.tplot_tools import data_quants` goes stale.
- `__init__.py` imports each function over its module name (`pyspedas.tplot_tools.store_data`
  is the function, not the module). Modules import siblings from `pyspedas.tplot_tools`, so the
  import order in `__init__.py` matters when adding a module.
- `tplot_copy()` here and `tcopy()` in `pyspedas/utilities/tcopy.py` both deep-copy variables.
- `timespan()`, `xlim()` and `tlimit()` store `x_range` in `tplot_opt_glob`; it applies to every
  later `tplot()` until `tlimit('full')` or `timespan(reset=True)`.
- `options()` lowercases option names, accepts many aliases, and only warns on unknown ones.
- Strings passed to `time_double()` are parsed with dateutil and taken as UTC.
- Importing the package calls `xr.set_options(keep_attrs=True)` globally.

## Tests

There is no `tests/` folder here. Tplot tests live in `pyspedas/utilities/tests/`
(`test_math.py`, `test_utilities_plot.py`, `test_utilities_tplot_wildcard.py`,
`test_utilities_time.py`) and in `MPLPlotter/plot_tests/`.
