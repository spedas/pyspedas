---
related_files:
  - pyspedas/tplot_tools/AGENTS.md
  - pyspedas/tplot_tools/MPLPlotter/tplot.py
  - pyspedas/tplot_tools/MPLPlotter/lineplot.py
  - pyspedas/tplot_tools/MPLPlotter/specplot.py
  - pyspedas/tplot_tools/MPLPlotter/var_labels.py
  - pyspedas/tplot_tools/MPLPlotter/get_var_label_ticks.py
  - pyspedas/tplot_tools/MPLPlotter/save_plot.py
  - pyspedas/tplot_tools/MPLPlotter/label_wrap.py
  - pyspedas/tplot_tools/MPLPlotter/_plot_range.py
  - pyspedas/tplot_tools/MPLPlotter/annotate.py
  - pyspedas/tplot_tools/MPLPlotter/highlight.py
  - pyspedas/tplot_tools/MPLPlotter/ctime.py
  - pyspedas/tplot_tools/MPLPlotter/tplotxy.py
  - pyspedas/tplot_tools/MPLPlotter/tplotxy3.py
  - pyspedas/tplot_tools/MPLPlotter/tplot_map.py
  - pyspedas/tplot_tools/MPLPlotter/plot_tests
  - pyspedas/tplot_tools/__init__.py
  - pyspedas/tplot_tools/reduce_spec_dataset.py
  - pyspedas/tplot_tools/timebar.py
  - pyspedas/tplot_tools/spedas_colorbar.py
  - pyspedas/tplot_tools/tplot_math/makegap.py
  - pyspedas/config.py
  - pyproject.toml
  - pyspedas/utilities/tests/test_utilities_plot.py
  - pyspedas/utilities/tests/test_utilities_tplotxy.py
  - .github/workflows/quick_tests.yml
maintenance: |
  Update when tplot() changes its call path (pseudovariable recursion, spec/line
  dispatch, time range, saving), when a plot option is read from a new place, or
  when a plotting module is added here.
---

# MPLPlotter

Matplotlib rendering of tplot variables. `tplot()` draws stacked time-series panels;
the other modules draw one panel type, orbit plots, or add interactive features.

## Layout

- `tplot.py`: `tplot()`, pseudovariable helpers (`gather_pseudovar_props`), var-label axes and the `slice` window.
- `lineplot.py`: line panels; `get_trace_options()` spreads per-trace options (colors, styles) across traces.
- `specplot.py`: spectrogram panels; `specplot_make_1d_ybins()` regrids time-varying or uneven bins onto one y grid for `pcolormesh`.
- `var_labels.py`, `get_var_label_ticks.py`: `var_label` values printed under the time axis.
- `save_plot.py`: writes `save_png`, `save_pdf`, etc.
- `annotate.py`, `highlight.py`: store text annotations and shaded intervals on a variable; `tplot()` draws them.
- `ctime.py`: click on a figure to collect times (experimental, backend dependent).
- `tplotxy.py`, `tplotxy3.py`: orbit-style plots of position variables in one plane or three projections, with `tplotxy3_add_mpause()` and `tplotxy3_add_neutral_sheet()` overlays.
- `tplot_map.py`: field-line footprints on a Basemap globe. It needs the optional `basemap` extra (`pyproject.toml`) and is not imported by `pyspedas/tplot_tools/__init__.py`.
- `label_wrap.py`, `_plot_range.py`: small helpers for the `xwrap`/`ywrap` options and inverted axes.
- `plot_tests/`: unittest modules.

## How tplot() works

1. `display` defaults to `CONFIG['plotting']['global_display']` (`pyspedas/config.py`, env
   `PYSPEDAS_GLOBAL_DISPLAY`). Names go through `tplot_wildcard_expand()`.
2. One panel per variable, sized by `extras['panel_size']`; figure size from the `xsize`/`ysize`
   arguments or the same keys in `tplot_opt_glob`. With `tplot_options('varlabel_style', 'extra_panel')` the var labels get their
   own panel, otherwise extra axes below the last panel.
3. A variable with both `v1` and `v2` coordinates is reduced to 2-D by `reduce_spec_dataset()`
   (`pyspedas/tplot_tools/reduce_spec_dataset.py`), keeping `extras['spec_dim_to_plot']`.
4. A pseudovariable (non-empty `overplots_mpl`) is drawn by calling `tplot()` again for each
   component with the same `fig` and `axis`, passing `pseudo_idx` and the parent's option dicts,
   which override the component's own options.
5. Gaps: `makegap()` (`pyspedas/tplot_tools/tplot_math/makegap.py`) with the variable's
   `data_gap` option or the global one.
6. The time axis uses the `trange` argument, else `tplot_opt_glob['x_range']`, else the full data.
7. `extras['spec']` true calls `specplot()`, otherwise `lineplot()`. Time bars
   (`pyspedas/tplot_tools/timebar.py`), highlights and annotations are drawn afterwards.
8. `save_plot()`, then `plt.show()` if displaying; `return_plot_objects=True` returns `(fig, axes)`.

## Things to know

- `tplot()` reads options at draw time from each variable's `.attrs['plot_options']`
  (`yaxis_opt`, `zaxis_opt`, `line_opt`, `extras`) and from
  `pyspedas.tplot_tools.tplot_opt_glob`; changing them later doesn't update a drawn figure.
- A bare file name in `save_png` and friends is written under
  `CONFIG['plotting']['plot_directory']` (env `PYSPEDAS_PLOT_DIRECTORY`); an extension is added
  if missing.
- Times on the axes are `datetime64`/UTC; `ctime()` returns float Unix seconds.
- Colormaps: `extras['colormap']` holds a list. Without it, and without a matplotlib `style`,
  spectrograms use the 'spedas' table built from `pyspedas/tplot_tools/spedas_colorbar.py`.

## Tests

`plot_tests/` holds a few tests (CI runs `test_wrap_label` and
`test_grid_background_options`, see `.github/workflows/quick_tests.yml`). Most plotting tests
are in `pyspedas/utilities/tests/test_utilities_plot.py` and
`pyspedas/utilities/tests/test_utilities_tplotxy.py`.
