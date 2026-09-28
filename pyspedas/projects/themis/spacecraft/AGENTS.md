---
related_files:
  - pyspedas/projects/themis/AGENTS.md
  - pyspedas/projects/themis/__init__.py
  - pyspedas/projects/themis/spacecraft/__init__.py
  - pyspedas/projects/themis/load.py
  - pyspedas/projects/themis/spacecraft/fields/fgm.py
  - pyspedas/projects/themis/spacecraft/fields/fit.py
  - pyspedas/projects/themis/spacecraft/fields/efi.py
  - pyspedas/projects/themis/spacecraft/fields/scm.py
  - pyspedas/projects/themis/spacecraft/fields/fft.py
  - pyspedas/projects/themis/spacecraft/fields/fbk.py
  - pyspedas/projects/themis/spacecraft/particles/esa.py
  - pyspedas/projects/themis/spacecraft/particles/esd.py
  - pyspedas/projects/themis/spacecraft/particles/sst.py
  - pyspedas/projects/themis/spacecraft/particles/mom.py
  - pyspedas/projects/themis/spacecraft/particles/gmom.py
  - pyspedas/projects/themis/state_tools/AGENTS.md
  - pyspedas/projects/themis/state_tools/autoload_support.py
  - pyspedas/projects/themis/state_tools/spinmodel/eclipse_spinmodel_corrections_vector.py
  - pyspedas/projects/themis/state_tools/spinmodel/eclipse_spinmodel_corrections_tensor.py
  - pyspedas/projects/themis/cotrans/dsl2gse.py
  - pyspedas/tplot_tools/importers/cdf_to_tplot.py
  - pyspedas/projects/themis/tests/test_themis.py
  - pyspedas/projects/themis/tests/test_themis_cal_fit.py
maintenance: |
  Update when a loader here is added or renamed, when the eclipse-correction rules
  (which variables get vector, tensor or no correction) change, or when a wrapper starts
  doing its own post-processing after load().
---

# THEMIS spacecraft loaders

Wrappers for the on-board THEMIS/ARTEMIS instruments: fields in `fields/`, particles in
`particles/`. Each wrapper calls `load()` in `pyspedas/projects/themis/load.py` (see the
parent AGENTS.md) and some post-process the result.

## Layout

- `fields/fgm.py`: `fgm()` and a module-level `check_args()` that builds the default
  `varformat` regex from `level` and `coord`.
- `fields/fit.py`: `fit()` (on-board spin fits) and `cal_fit()`, which calibrates raw
  `th?_fit` into `th?_fgs`, `th?_efs` and related variables using calibration text files
  downloaded from `th?/l1/fgm/0000/` and `th?/l1/eff/0000/`.
- `fields/efi.py`: `efi()`. `datatype` selects files: L1 `eff efp efw vaf vap vaw vbf
  vbp vbw` (default omits `vb*`), L2 `efi efp efw` (default `efi`).
- `fields/scm.py`, `fields/fft.py`, `fields/fbk.py`: search coil, FFT spectra and filter
  bank. At L1, `scm` loads the `scp`/`scf`/`scw` files and `fft` nine `ff?_<n>` files.
- `particles/esa.py`: ESA L2 moments and energy spectra (full, reduced and burst modes).
- `particles/esd.py`: L2 3D ESA distributions, one file per `datatype` (`peif`, `peef`, ...).
- `particles/sst.py`, `particles/mom.py`, `particles/gmom.py`: SST data, on-board moments,
  and ground moments (ESA and SST combined).
- The `__init__.py` files are empty; `pyspedas/projects/themis/__init__.py` exports the loaders.

## How eclipse corrections work

`fgm`, `fit`, `efi`, `scm`, `esa`, `sst`, `mom` and `gmom` take
`apply_eclipse_corrections` (default False). When it is set, the level is `l2` and
`downloadonly` is off, each wrapper, per probe:

1. calls `autoload_support(probe=p, trange=trange, spinmodel=True)`
   (`pyspedas/projects/themis/state_tools/autoload_support.py`), which loads state data
   with support variables if the spin model doesn't cover `trange` (see
   `pyspedas/projects/themis/state_tools/AGENTS.md`);
2. logs each eclipse's correction status from the level-2 spin model;
3. picks variables by substring: tensors (`ptens`, `mftens`) go to
   `eclipse_spinmodel_corrections_tensor()`, vectors to
   `eclipse_spinmodel_corrections_vector()`; magnitudes, spectra, scalars, SSL and
   field-aligned quantities are skipped. Each wrapper has its own name rules.

`spin_based=True` (spin model correction level 2, for spin fits and particle moments) is
used for `fgs`, `efs` in `fit()`, and ESA/SST/MOM/GMOM; waveform data (`fgl`, `fgh`, `fge`,
SCM, all EFI including `efs`) uses `spin_based=False` (level 1). The correction rotates
the spin-plane components in DSL, in place; GSE/GSM inputs go through
`pyspedas/projects/themis/cotrans/dsl2gse.py` and back.

## Things to know

- Variable names are `th<probe>_<type>[_<coord>]`: `thc_fgs_gse`, `thd_peim_density`,
  `thd_psif_density`, `thd_fb_edc12`, `thd_efs_dot0_gse`.
- `fgm()`'s default `varformat` is a regular expression (`^th[a-e]{1}_(fgs|fgl|...)`), not a
  glob. `cdf_to_tplot()` (`pyspedas/tplot_tools/importers/cdf_to_tplot.py`) turns each
  `*` into `.*` and then uses it as a regex, so both forms work.
- `load()` forces level `l2` for `esd`, and ESD files are named `th?_l2_esa_<datatype>_...`
  inside the `esd/` directory. `esd()` defaults to a 2021 time range.
- Eclipse corrections load state data as a side effect and log a lot at INFO level.
- `cal_fit()` expects `th?_fit` to be loaded already (`fit(level='l1')`).

## Tests

`pyspedas/projects/themis/tests/test_themis.py` covers the loaders;
`pyspedas/projects/themis/tests/test_themis_cal_fit.py` covers `cal_fit()`.
