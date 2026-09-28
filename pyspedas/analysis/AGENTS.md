---
related_files:
  - AGENTS.md
  - pyspedas/analysis/README.md
  - pyspedas/analysis/__init__.py
  - pyspedas/analysis/avg_data.py
  - pyspedas/analysis/deriv_data.py
  - pyspedas/analysis/yclip.py
  - pyspedas/analysis/tinterpol.py
  - pyspedas/analysis/tvectot.py
  - pyspedas/analysis/interp_gap.py
  - pyspedas/analysis/rebin.py
  - pyspedas/analysis/reduce_tres.py
  - pyspedas/analysis/roundsig.py
  - pyspedas/analysis/time_domain_filter.py
  - pyspedas/analysis/twavpol.py
  - pyspedas/analysis/wavelet.py
  - pyspedas/analysis/wav_data.py
  - pyspedas/analysis/wavelet2.py
  - pyspedas/analysis/wavelet98.py
  - pyspedas/analysis/wave_signif.py
  - pyspedas/analysis/lingradest.py
  - pyspedas/analysis/find_magnetic_nulls.py
  - pyspedas/analysis/neutral_sheet.py
  - pyspedas/analysis/tests/test_analysis.py
  - pyspedas/analysis/tests/test_twavpol.py
  - pyspedas/analysis/tests/test_wavelet.py
  - pyspedas/analysis/tests/test_magnetic_nulls.py
  - pyspedas/analysis/tests/wavetest.py
  - pyspedas/__init__.py
  - pyspedas/tplot_tools/tplot_math
  - pyspedas/utilities/time_interpolate.py
  - pyspedas/utilities/config_testing.py
  - pyspedas/config.py
maintenance: |
  Update when a routine is added here or re-exported from pyspedas/__init__.py,
  when output naming (suffix defaults, fixed output names) changes, or when a
  routine is ported from or re-validated against IDL SPEDAS.
---

# analysis

General analysis routines ported from IDL SPEDAS: averaging, derivatives,
interpolation, filtering, wave polarization, wavelets, four-spacecraft gradients and
neutral sheet models. `__init__.py` is empty; public names are re-exported from
`pyspedas/__init__.py`, so callers use `pyspedas.avg_data`, `pyspedas.twavpol`, etc.

## Layout

- Variable-in, variable-out: `avg_data.py`, `deriv_data.py`, `yclip.py`, `tinterpol.py`, `tvectot.py` (magnitude, optionally joined to the vector).
- Array helpers: `interp_gap.py`, `rebin.py`, `reduce_tres.py`, `roundsig.py`, `time_domain_filter.py` (band-pass on arrays).
- Waves: `twavpol.py` (polarization from a 3-component field), `wavelet.py` (PyWavelets on a variable), `wav_data.py` (port of IDL `wav_data`, built on `wavelet2.py`, `wavelet98.py` and `wave_signif.py`, the Torrence and Compo routines).
- Multi-spacecraft: `lingradest.py` (gradients, curl, curvature from four probes, arrays in), `find_magnetic_nulls.py` (`find_magnetic_nulls_fote`, `classify_null_type`, tplot names in).
- `neutral_sheet.py`: `neutral_sheet(time, pos, model=...)` dispatches to the `*_ns_model` functions ('sm', 'themis', 'aen', 'den', 'fairfield', 'den_fairfield', 'lopez', 'tag14').
- `README.md`: usage notes. `tests/`: unittest modules.

## How to pick an entry point

Most routines take tplot names (wildcards allowed) and write new variables. Start from the
variable-level function (`twavpol`, `wav_data`, `wavelet`, `find_magnetic_nulls_fote`) and drop
to the array functions (`wavpol`, `wavelet2`, `lingradest`) only for numpy input.

## Things to know

- Output names: `avg_data` adds `-avg`, `deriv_data` `-der`, `yclip` `-clip`, `tinterpol` `-itrp`,
  `tvectot` `_tot` (or `_mag`), `wavelet` `_pow`. `twavpol` writes `<prefix>_powspec`,
  `_degpol`, `_waveangle`, `_elliptict`, `_helict`, with the input name as default prefix.
  `find_magnetic_nulls_fote` writes fixed names (`null_pos`, `null_bary_dist`, ...) and
  overwrites them on each call.
- Similar functions exist in `pyspedas/tplot_tools/tplot_math` with different names and
  conventions: `avg_res_data`, `derive`, `clip`, `tinterp`. The ones here follow IDL SPEDAS
  (`newname`/`suffix`/`overwrite`). `tinterpol` uses xarray `interp`;
  `time_interpolate()` (`pyspedas/utilities/time_interpolate.py`) reproduces IDL `interpol`
  behavior more closely.
- `neutral_sheet()` expects positions in Re and returns Z in Re, GSM unless `in_coord` says
  otherwise (it calls `cotrans`).
- `lingradest()` takes positions in km with `scale_factor=1000.0` as the length divisor.

## Tests

`tests/test_analysis.py` also covers several tplot_math functions (`tdotp`,
`subtract_average`, ...). It, `tests/test_twavpol.py` and `tests/test_wavelet.py` compare
against IDL SPEDAS validation files fetched by `test_data_download_file()`
(`pyspedas/utilities/config_testing.py`) from `CONFIG['testing']['validation_dir']`
(`pyspedas/config.py`). `tests/wavetest.py` is the Torrence and Compo example script.
