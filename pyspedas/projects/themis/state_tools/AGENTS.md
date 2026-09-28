---
related_files:
  - pyspedas/projects/themis/AGENTS.md
  - pyspedas/projects/themis/spacecraft/AGENTS.md
  - pyspedas/projects/themis/__init__.py
  - pyspedas/projects/themis/load.py
  - pyspedas/projects/themis/state_tools/__init__.py
  - pyspedas/projects/themis/state_tools/state.py
  - pyspedas/projects/themis/state_tools/apply_spinaxis_corrections.py
  - pyspedas/projects/themis/state_tools/autoload_support.py
  - pyspedas/projects/themis/state_tools/slp.py
  - pyspedas/projects/themis/state_tools/ssc.py
  - pyspedas/projects/themis/state_tools/ssc_pre.py
  - pyspedas/projects/themis/state_tools/spinmodel/spinmodel.py
  - pyspedas/projects/themis/state_tools/spinmodel/spinmodel_segment.py
  - pyspedas/projects/themis/state_tools/spinmodel/spinmodel_postprocess.py
  - pyspedas/projects/themis/state_tools/spinmodel/eclipse_spinmodel_corrections_vector.py
  - pyspedas/projects/themis/state_tools/spinmodel/eclipse_spinmodel_corrections_tensor.py
  - pyspedas/projects/themis/cotrans/ssl2dsl.py
  - pyspedas/projects/themis/cotrans/dsl2gse.py
  - pyspedas/projects/themis/cotrans/gse2sse.py
  - pyspedas/projects/themis/cotrans/sse2sel.py
  - pyspedas/projects/themis/tests/test_themis_state.py
  - pyspedas/projects/themis/tests/test_themis_spinmodel.py
  - pyspedas/projects/themis/tests/test_themis_autoload_support.py
  - pyspedas/projects/themis/tests/test_themis_lunar_cotrans.py
maintenance: |
  Update when state() changes what it builds from the support variables, when the spin
  model registry or its correction levels change, or when autoload_support() gains a
  support type or changes its reload rule.
---

# THEMIS state and support data

Orbit, attitude and ephemeris loaders for THEMIS/ARTEMIS, and the support machinery the
coordinate transforms and eclipse corrections depend on: the spin model, spin axis
corrections, and automatic reloading of support data.

## Layout

- `state.py`: `state()` loads L1 STATE CDFs (position, velocity, spin axis, spin model
  segments) and post-processes the spin variables.
- `spinmodel/spinmodel.py`: the `Spinmodel` class (segments from `spinmodel_segment.py`),
  its `interp_t()` method, and the registry functions `get_spinmodel()` and
  `save_spinmodel()`. `__init__.py` re-exports these three names.
- `spinmodel/spinmodel_postprocess.py`: builds and registers the models after a load.
- `spinmodel/eclipse_spinmodel_corrections_vector.py`, `..._tensor.py`: in-place eclipse
  despin corrections, used by the loaders in `pyspedas/projects/themis/spacecraft/`.
- `apply_spinaxis_corrections.py`: applies the V03 STATE spin axis RA/Dec corrections.
- `autoload_support.py`: `autoload_support()`, reloads state or SLP data if what is
  loaded doesn't cover a time range.
- `slp.py`: `slp()`, Sun and Moon positions and lunar attitude (SLP ephemeris).
- `ssc.py`, `ssc_pre.py`: `ssc()` and `ssc_pre()`, actual and predicted orbits from CDAWeb (SSCWeb).

## How `state()` builds the spin model

`state()` calls `load(instrument='state')` in `pyspedas/projects/themis/load.py`. Only with
`get_support_data=True` does it then, per probe:

1. call `spinmodel_postprocess()`, which needs every `th?_spin_*` and `th?_spin_ecl_*`
   segment variable and builds three `Spinmodel` objects: correction level 0 (none, from
   `th?_spin_*`), 1 (waveform, from `th?_spin_ecl_*`) and 2 (spin fit: level 1 plus FGM
   phase offsets when the CDF has them). Each is stored with `save_spinmodel()`;
2. delete the `th?_spin_*` variables unless `keep_spin=True`;
3. call `apply_spinaxis_corrections()` to make `th?_spinras_corrected` and
   `th?_spindec_corrected` (a copy of the raw values if the CDF has no corrections).

`get_spinmodel(probe, correction_level)` returns the stored model or None.
`Spinmodel.interp_t(times)` gives spin phase, spin count, spin period and the eclipse phase
offset at arbitrary times; `pyspedas/projects/themis/cotrans/ssl2dsl.py` uses it to despin.

## How `autoload_support()` works

Given a tplot name, or a `trange` and a `probe`, it checks what is loaded against the
needed range, allowing 120 s of extrapolation: `spinmodel=True` checks the level-1 model's
time range; `spinaxis=True` checks `th?_spinras`, `th?_spindec` and their `_corrected`
versions; `slp=True` checks `slp_lun_att_x`, `slp_lun_att_z`, `slp_lun_pos`, `slp_sun_pos`.
Missing or short coverage calls `state(get_support_data=True)` or `slp()` for the range.
`pyspedas/projects/themis/cotrans/dsl2gse.py`, `ssl2dsl.py`, `gse2sse.py` and
`sse2sel.py` call it before transforming.

## Things to know

- The spin model registry is a module-level dict, `spinmodel_dict`, keyed by
  `(probe, correction_level)`. A new `state()` load for a probe replaces its models, and
  the key ignores `suffix`.
- The spin axis and SLP checks in `autoload_support()`, and the transforms, read
  unsuffixed names (`thc_spinras_corrected`, `slp_sun_pos`), so state or SLP data loaded
  with a `suffix` is not found and gets reloaded.
- STATE files: without `version`, Berkeley's unversioned link `th?_l1_state_YYYYMMDD.cdf`
  is loaded; with `version`, or when the remote is SPDF, the versioned `v??` name is used.
- `slp()` sets GEI coordinates on every variable except the light-time (`ltime`) ones.
- `ssc()` reads monthly files and `ssc_pre()` yearly files from
  `https://cdaweb.gsfc.nasa.gov/pub/data/themis/`, whatever `CONFIG['remote_data_dir']`
  says. Both default to `time_clip=True`.

## Tests

`pyspedas/projects/themis/tests/test_themis_state.py`, `test_themis_spinmodel.py`,
`test_themis_autoload_support.py` and `test_themis_lunar_cotrans.py` (all in
`pyspedas/projects/themis/tests/`; they download data).
