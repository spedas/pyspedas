---
related_files:
  - AGENTS.md
  - pyspedas/geopack/__init__.py
  - pyspedas/geopack/README.md
  - pyspedas/geopack/generic_geopack_adapters.py
  - pyspedas/geopack/prepare_pos_variable.py
  - pyspedas/geopack/clean_model_parameters.py
  - pyspedas/geopack/igrf.py
  - pyspedas/geopack/t89.py
  - pyspedas/geopack/t96.py
  - pyspedas/geopack/t01.py
  - pyspedas/geopack/ts04.py
  - pyspedas/geopack/kp2iopt.py
  - pyspedas/geopack/get_tsy_params.py
  - pyspedas/geopack/get_w_params.py
  - pyspedas/geopack/ttrace2endpoint.py
  - pyspedas/geopack/trace_to_event.py
  - pyspedas/geopack/calculate_lshell.py
  - pyspedas/geopack/tests
  - pyspedas/geopack/tests/test_geopack_idl_validation.py
  - pyspedas/__init__.py
  - pyproject.toml
  - pyspedas/cotrans_tools/cotrans.py
  - pyspedas/cotrans_tools/igrf.py
  - pyspedas/projects/noaa/noaa_load_kp.py
  - pyspedas/projects/kyoto/load_dst.py
  - pyspedas/projects/omni/load.py
  - pyspedas/tplot_tools/MPLPlotter/tplot_map.py
  - .github/workflows/full_coverage.yml
maintenance: |
  Update when a field model or tracing option is added, when the model wrappers
  change how they read positions or parameters, or when the dependency on the
  external geopack package changes.
---

# geopack

tplot wrappers around the external `geopack` package (Sheng Tian's Python port of
Tsyganenko's GEOPACK, a dependency in `pyproject.toml`): model field along a position
variable (IGRF, T89, T96, T01, TS04), field-line tracing, L-shell, and the model input
parameters. Public names are re-exported from `pyspedas/__init__.py`.

## Layout

- `igrf.py` (`tigrf`), `t89.py` (`tt89`), `t96.py` (`tt96`), `t01.py` (`tt01`), `ts04.py` (`tts04`): field at each position; each also has a `get_<model>_parameters()` that builds the N x 10 `parmod` array.
- `generic_geopack_adapters.py`: `make_model(name, time, parmod)` calls `geopack.recalc(time)` and returns an object whose `B_gsm(pos_re)` adds the external model to IGRF.
- `prepare_pos_variable.py`: converts the input position to GSM and Re, using its `data_att` metadata or `coord_in`/`units_in`.
- `clean_model_parameters.py`: turns a scalar, array or tplot name into one value per position time (nearest or interpolated).
- `ttrace2endpoint.py`, `trace_to_event.py`: trace field lines to the northern or southern ionosphere or the equator with `scipy.integrate.solve_ivp`; `calculate_lshell.py`: L from an IGRF trace to the equator.
- `get_tsy_params.py`: parmod variable (`t96_par`, `t01_par`, `ts04_par`) from Dst, IMF, density and velocity variables; `get_w_params.py`: `get_w()` downloads the TS05 W1-W6 values; `kp2iopt.py`: Kp to T89 `iopt`.
- `README.md`: short examples. `tests/`: unittest modules.

## How tt89() works

`tt89('pos_var', kp=...)` calls `prepare_pos_variable()` (converting with `cotrans` and
`tkm2re` when needed), builds `parmod` with `get_t89_parameters()`, then loops over times:
`make_model('t89', t, parmod[i])` and `model.B_gsm(pos_re[i])`. The result is rotated to
`coord_out` if not GSM and stored as `<pos_var>_bt89<suffix>` in nT with `coord_sys` set. The
other models follow the same path (`_btigrf`, `_bt96`, `_bt01`, `_bts04`).

## Things to know

- Model parameters: a `parmod` array or tplot name wins; otherwise the individual inputs
  (`kp`/`iopt`, `pdyn`, `dst`, `byimf`, `bzimf`, `g1`, `g2`, `w1`..`w6`) are used, each a scalar,
  array or tplot name, with logged defaults (T89 `iopt=3`, `pdyn=2.0`) for missing ones.
- `autoload=True` loads NOAA Kp for T89 (`pyspedas/projects/noaa/noaa_load_kp.py`) and Kyoto Dst
  plus OMNI for T96 (`pyspedas/projects/kyoto/load_dst.py`, `pyspedas/projects/omni/load.py`);
  T01 and TS04 raise `ValueError` for it.
- Positions need units (km or Re) and a coordinate system, from metadata or arguments;
  otherwise `prepare_pos_variable()` raises `ValueError`. It writes scratch variables
  `input_var_re` and `input_var_gsm`, and `calculate_lshell()` writes `eq_foot` and `eq_trace`.
- `geopack.recalc()` sets module-level state inside the external package, so every
  evaluation goes through `make_model()` for its own time. Evaluation is a Python loop per time
  step and slow for long intervals.
- Name clashes: this package shares its name with the external `geopack`, which the code imports
  as `geopack.geopack`, `geopack.t89`, and so on. `pyspedas/cotrans_tools/igrf.py` is an unrelated
  IGRF coefficient table used by cotrans.
- `ttrace2endpoint()` returns NaN foot points for traces that don't reach the endpoint; its
  output names come from keywords (`foot_name`, `trace_name`, `bvec_name`, `diag_*_name`).
  `pyspedas/tplot_tools/MPLPlotter/tplot_map.py` maps the foot points.

## Tests

`tests/` compares against IDL SPEDAS results (`test_geopack_idl_validation.py`) and checks
input handling. They run in `.github/workflows/full_coverage.yml`, not in the quick tests.
