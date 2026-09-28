---
related_files:
  - AGENTS.md
  - pyspedas/particles/README.md
  - pyspedas/particles/__init__.py
  - pyspedas/particles/moments/moments_3d.py
  - pyspedas/particles/moments/moments_3d_omega_weights.py
  - pyspedas/particles/moments/spd_pgs_moments.py
  - pyspedas/particles/moments/spd_pgs_moments_tplot.py
  - pyspedas/particles/spd_part_products/spd_pgs_do_fac.py
  - pyspedas/particles/spd_part_products/spd_pgs_regrid.py
  - pyspedas/particles/spd_part_products/spd_pgs_v_shift.py
  - pyspedas/particles/spd_part_products/spd_pgs_limit_range.py
  - pyspedas/particles/spd_part_products/spd_pgs_make_e_spec.py
  - pyspedas/particles/spd_part_products/spd_pgs_make_phi_spec.py
  - pyspedas/particles/spd_part_products/spd_pgs_make_theta_spec.py
  - pyspedas/particles/spd_part_products/spd_pgs_make_tplot.py
  - pyspedas/particles/spd_part_products/spd_pgs_progress_update.py
  - pyspedas/particles/spd_slice2d/slice2d.py
  - pyspedas/particles/spd_slice2d/slice2d_plot.py
  - pyspedas/particles/spd_slice2d/slice1d_plot.py
  - pyspedas/particles/spd_slice2d/slice2d_get_data.py
  - pyspedas/particles/spd_slice2d/tplot_average.py
  - pyspedas/particles/spd_slice2d/quaternions.py
  - pyspedas/particles/spd_units_string.py
  - pyspedas/particles/tests/test_particles.py
  - pyspedas/__init__.py
  - pyspedas/projects/mms/particles/mms_part_products.py
  - pyspedas/projects/mms/particles/mms_part_slice2d.py
  - pyspedas/projects/mms/fpi_tools/mms_pad_fpi.py
  - pyspedas/projects/erg/satellite/erg/particle/erg_lep_part_products.py
  - pyspedas/cotrans_tools/quaternions.py
  - .github/workflows/full_coverage.yml
maintenance: |
  Update when the particle distribution dict gains or changes required keys,
  when a mission starts or stops using these routines, or when a routine moves
  between moments/, spd_part_products/ and spd_slice2d/.
---

# particles

Mission-independent pieces for 3-D particle distributions, ported from IDL SPEDAS:
moments, spectrogram and FAC helpers for "part_products", and 2-D slices. The README
marks the folder experimental. Missions supply the distributions and the driver
routines; MMS and ERG are the users.

## Layout

- `moments/`: `moments_3d()` (density, flux, velocity, pressure and temperature tensors, ...), `spd_pgs_moments()` (thin wrapper), `spd_pgs_moments_tplot()` (moment dicts to tplot variables).
- `spd_part_products/`: steps of a part_products run: `spd_pgs_limit_range` (turn off bins outside phi, theta, energy limits), `spd_pgs_regrid`, `spd_pgs_do_fac`, `spd_pgs_v_shift`, `spd_pgs_make_e_spec`/`_phi_spec`/`_theta_spec`, `spd_pgs_make_tplot`, `spd_pgs_progress_update`.
- `spd_slice2d/`: `slice2d()` (interpolated 2-D slice from a list of distributions), `slice2d_plot()`, `slice1d_plot()`, and the `slice2d_*` helpers; `tplot_average()` averages a variable over a time range.
- `spd_units_string.py`: unit label strings.
- `tests/test_particles.py`: builds spectra from ERG LEP-e data (downloads).

## How it is used

A mission routine (`mms_get_fpi_dist`, `erg_lepe_get_dist`, ...) returns distribution dicts,
and the mission's own driver loops over times, calling the routines here.
`pyspedas/projects/mms/particles/mms_part_products.py` uses `spd_pgs_limit_range`,
`spd_pgs_regrid`, `spd_pgs_do_fac`, `spd_pgs_v_shift`, the moments routines and
`spd_pgs_make_tplot`, but its own `mms_pgs_make_*_spec`.
`pyspedas/projects/erg/satellite/erg/particle/erg_lep_part_products.py` and its siblings use
only `spd_pgs_moments` and `spd_pgs_regrid`. `mms_part_slice2d` wraps `slice2d()` and
`slice2d_plot()`, and `pyspedas/projects/mms/fpi_tools/mms_pad_fpi.py` reuses slice2d helpers.
There is no generic part_products driver in this folder.

## Things to know

- A distribution is a dict of numpy arrays with keys such as `data`, `energy`, `denergy`,
  `theta`, `dtheta`, `phi`, `dphi`, `bins` (1 = use the bin), `mass`, `charge` and `magf`;
  `moments_3d()` needs all of these. Angles are in degrees.
- `moments_3d()` expects `data` in energy flux, with `mass` in eV/(km/s)^2 (proton 0.0104535),
  and energies below 0.1 eV raised to 0.1. `sc_pot` shifts energies by `charge * sc_pot`.
- `slice2d()` takes a list of distributions, not tplot names; time selection is by
  `time` with `samples` or `window`, or by `trange`. Rotations such as 'BV' and 'perp' need
  the `mag_data` and/or `vel_data` tplot names.
- `slice2d_plot()` reads style, `charsize` and `axis_font_size` from
  `pyspedas.tplot_tools.tplot_opt_glob`.
- `spd_slice2d/quaternions.py` is a small private copy of `qtom` and `qcompose`; the full
  library is `pyspedas/cotrans_tools/quaternions.py`.
- Public names re-exported from `pyspedas/__init__.py`: `moments_3d`, `spd_pgs_moments`,
  `spd_pgs_moments_tplot`, `spd_pgs_do_fac`, `spd_pgs_regrid`, `spd_pgs_v_shift`, `slice2d`,
  `slice2d_plot`, `slice1d_plot`.

## Tests

`tests/test_particles.py` runs in `.github/workflows/full_coverage.yml`. MMS and ERG tests
exercise the rest through the mission drivers.
