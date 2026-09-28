---
related_files:
  - pyspedas/tplot_tools/AGENTS.md
  - pyspedas/tplot_tools/tplot_math/add.py
  - pyspedas/tplot_tools/tplot_math/subtract.py
  - pyspedas/tplot_tools/tplot_math/multiply.py
  - pyspedas/tplot_tools/tplot_math/divide.py
  - pyspedas/tplot_tools/tplot_math/tinterp.py
  - pyspedas/tplot_tools/tplot_math/tdotp.py
  - pyspedas/tplot_tools/tplot_math/tcrossp.py
  - pyspedas/tplot_tools/tplot_math/crop.py
  - pyspedas/tplot_tools/tplot_math/add_across.py
  - pyspedas/tplot_tools/tplot_math/avg_res_data.py
  - pyspedas/tplot_tools/tplot_math/clip.py
  - pyspedas/tplot_tools/tplot_math/derive.py
  - pyspedas/tplot_tools/tplot_math/tnormalize.py
  - pyspedas/tplot_tools/tplot_math/tkm2re.py
  - pyspedas/tplot_tools/tplot_math/spec_mult.py
  - pyspedas/tplot_tools/tplot_math/split_vec.py
  - pyspedas/tplot_tools/tplot_math/join_vec.py
  - pyspedas/tplot_tools/tplot_math/deflag.py
  - pyspedas/tplot_tools/tplot_math/tdeflag.py
  - pyspedas/tplot_tools/tplot_math/degap.py
  - pyspedas/tplot_tools/tplot_math/makegap.py
  - pyspedas/tplot_tools/tplot_math/interp_nan.py
  - pyspedas/tplot_tools/tplot_math/clean_spikes.py
  - pyspedas/tplot_tools/tplot_math/tsmooth.py
  - pyspedas/tplot_tools/tplot_math/subtract_average.py
  - pyspedas/tplot_tools/tplot_math/subtract_median.py
  - pyspedas/tplot_tools/tplot_math/time_clip.py
  - pyspedas/tplot_tools/tplot_math/pwrspc.py
  - pyspedas/tplot_tools/tplot_math/dpwrspc.py
  - pyspedas/tplot_tools/tplot_math/tpwrspc.py
  - pyspedas/tplot_tools/tplot_math/tdpwrspc.py
  - pyspedas/tplot_tools/tplot_math/pwr_spec.py
  - pyspedas/tplot_tools/__init__.py
  - pyspedas/analysis/tinterpol.py
  - pyspedas/utilities/time_interpolate.py
  - pyspedas/utilities/tests/test_math.py
  - pyspedas/utilities/tests/test_interp_nan.py
  - pyspedas/analysis/tests/test_analysis.py
maintenance: |
  Update when a function is added here (and imported in tplot_tools/__init__.py),
  or when a function changes how it names or overwrites its output variables.
---

# tplot_math

Operations on tplot variables: arithmetic, interpolation, clipping, gap and flag
handling, smoothing and power spectra. Each module holds one public function (plus
helpers), imported in `pyspedas/tplot_tools/__init__.py` and re-exported from `pyspedas`.

## Layout

- Two-variable arithmetic: `add.py`, `subtract.py`, `multiply.py`, `divide.py` (these call `tinterp.py` first), `tdotp.py`, `tcrossp.py`, `crop.py` (trim two variables to their common time range).
- One-variable transforms: `add_across.py`, `avg_res_data.py`, `clip.py`, `derive.py`, `tnormalize.py`, `tkm2re.py` (km and Re, 6371.2 km), `spec_mult.py`, `split_vec.py`, `join_vec.py`.
- Gaps, flags and noise: `degap.py`, `makegap.py`, `deflag.py`, `tdeflag.py`, `interp_nan.py`, `clean_spikes.py`, `tsmooth.py` (`smooth` on arrays, `tsmooth` on variables), `subtract_average.py`, `subtract_median.py`.
- Time range: `time_clip.py`, used by nearly every loader.
- Power spectra: `pwrspc.py` and `dpwrspc.py` work on arrays (ports of the IDL routines); `tpwrspc.py` and `tdpwrspc.py` wrap them for variables; `pwr_spec.py` is a separate scipy periodogram version.

## Output naming

Two conventions coexist; check the function before relying on either.

- PyTplot style (`newname` only): `add`, `subtract`, `multiply`, `divide`, `clip`, `derive`,
  `degap`, `interp_nan`, `deflag` overwrite the input variable when `newname` is None.
  `tdotp`, `tcrossp`, `tnormalize`, `spec_mult`, `pwr_spec`, `join_vec` instead invent a name
  (`a_dot_b`, `a_cross_b`, `_normalized`, `_specmult`, `_pwrspec`, `_joined`).
- SPEDAS style (`newname`, `suffix`, `overwrite`): `time_clip` (default suffix `-tclip`),
  `tdeflag` (`-deflag`), `tsmooth` (`-s`), `clean_spikes` (`-despike`), `subtract_average` (`-d`),
  `subtract_median` (`-m`). These take wildcards and lists of names.
- `split_vec` appends `_x`, `_y`, `_z` (or `_0`, `_1`, ...); `tkm2re` appends `_re` or `_km`.

## Things to know

- `tinterp(a, b)` interpolates `b` onto the times of `a` with xarray `interp_like` and stores
  `b_tinterp`, so the arithmetic functions leave `*_tinterp` variables behind.
  `tinterpol()` (`pyspedas/analysis/tinterpol.py`) and `time_interpolate()`
  (`pyspedas/utilities/time_interpolate.py`) are the IDL-style interpolators.
- `makegap()` takes and returns a `get_data()` tuple, not a name; it round-trips through a
  scratch variable `makegap_tmp`. `tplot()` calls it for the `data_gap` option.
- `time_clip` keeps samples with `time_start <= t <= time_end`; `interior_clip=True` removes
  that interval instead. Loaders call it with `suffix=''`, which replaces the variables in place.
- Most functions work on `pyspedas.tplot_tools.data_quants[name]` directly and copy `.attrs`
  onto the output, so plot options and `data_att` carry over. Some in-place paths rebuild the
  variable with `store_data()` instead and drop them, so check before relying on it.

## Tests

Tests for these functions are in `pyspedas/utilities/tests/test_math.py`,
`pyspedas/utilities/tests/test_interp_nan.py` and `pyspedas/analysis/tests/test_analysis.py`.
