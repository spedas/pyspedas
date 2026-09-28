---
related_files:
  - pyspedas/projects/AGENTS.md
  - pyspedas/projects/elfin/__init__.py
  - pyspedas/projects/elfin/config.py
  - pyspedas/projects/elfin/load.py
  - pyspedas/projects/elfin/epd/epd.py
  - pyspedas/projects/elfin/epd/postprocessing.py
  - pyspedas/projects/elfin/epd/calibration_l1.py
  - pyspedas/projects/elfin/epd/calibration_l2.py
  - pyspedas/projects/elfin/epd/ela_epde_cal_data.txt
  - pyspedas/projects/elfin/epd/elb_epde_cal_data.txt
  - pyspedas/projects/elfin/fgm/fgm.py
  - pyspedas/projects/elfin/state/state.py
  - pyspedas/projects/elfin/mrma/mrma.py
  - pyspedas/projects/elfin/mrmi/mrmi.py
  - pyspedas/projects/elfin/eng/eng.py
  - pyspedas/projects/elfin/README.md
  - pyspedas/projects/elfin/tests/test_elfin.py
  - pyspedas/projects/elfin/tests/test_epd_l1.py
  - pyspedas/projects/elfin/tests/test_epd_l2.py
  - pyspedas/projects/elfin/tests/test_epd_calibration.py
  - pyspedas/projects/elfin/tests/test_state.py
  - pyspedas/projects/elfin/tests/test_epde_cal_data.txt
  - pyspedas/preferences.py
  - pyproject.toml
  - .github/workflows/full_coverage.yml
maintenance: |
  Update when load.py changes a path template, when the EPD L1 or L2
  post-processing or its keywords change, when a calibration data file is added,
  or when __init__.py adds a loader.
---

# ELFIN

Loaders for the ELFIN-A and ELFIN-B CubeSats: energetic particles (EPD),
magnetometer (FGM), state (orbit and attitude), magnetoresistive magnetometers
(MRMa, MRMi) and engineering data. Daily CDF files come from UCLA
(`https://data.elfin.ucla.edu/`).

## Layout

- `epd/`: `epd.py` (`epd_load()`), `postprocessing.py` (L1 and L2 steps),
  `calibration_l1.py` (counts to flux), `calibration_l2.py` (energy and
  pitch-angle spectrograms), and the EPDE calibration tables
  `ela_epde_cal_data.txt` and `elb_epde_cal_data.txt`.
- `fgm/`, `state/`, `mrma/`, `mrmi/`, `eng/`: one module each with an
  `<name>_load()` wrapper and an empty `<name>_postprocessing()` placeholder.
- `load.py`: `load()`, the path-template chain for all instruments.
- `config.py`, `tests/`, `README.md` (user guide; its examples use the pre-2.0
  path `pyspedas.elfin`).

## How it works

`__init__.py` exports the wrappers under short names (`epd`, `fgm`, `state`,
`mrma`, `mrmi`, `eng`). Each calls `load()`, which builds
`el<probe>/<level>/<instrument>/...` paths, downloads with
`last_version=True` and loads with `cdf_to_tplot()`. EPD datatypes map to
folders: `pef`/`pif` are `fast/electron`/`fast/ion`, `pes`/`pis` are
`survey/electron`/`survey/ion`. FGM `datatype='fast'` reads `fgf` files, anything
else `fgs`.

`epd()` then post-processes (`epd/postprocessing.py`):

- `level='l1'` (the default): `epd_l1_postprocessing()` renames each data
  variable to `<name>_<type_>` (`ela_pef_nflux`) and calibrates it with
  `calibrate_epd()` into `type_` units (`raw`, `cps`, `nflux`, `eflux`; unknown
  values become `nflux`). EPDE uses the latest entry of
  `el<probe>_epde_cal_data.txt` dated before the start of `trange`; EPDI uses
  constants in `get_epdi_calibration()`.
- `level='l2'`: `epd_l2_postprocessing()` builds energy and pitch-angle
  spectrograms (`epd_l2_Espectra()`, `epd_l2_PAspectra()`), half-spin (`hs`) or,
  with `fullspin=True`, full-spin (`fs`) resolution, preferring 32-sector data
  when it is not all NaN. `type_` must be `nflux` or `eflux`; anything else
  falls back to `nflux`.

## Things to know

- `pyspedas.projects.elfin.epd` is the function, not the `epd/` subpackage;
  import submodules by full path
  (`from pyspedas.projects.elfin.epd.calibration_l2 import spec_pa_sort`).
- `load()` has no `prefix` keyword, and `probe` is a single string (`'a'` or
  `'b'`), not a list.
- `epd()` and `state()` default to `time_clip=True`; the others to False. All
  wrappers default to `level='l1'`.
- The calibration tables must ship with the package; `pyproject.toml` lists them
  under `package-data`.
- The local data folder is `ELFIN_DATA_DIR`, else `SPEDAS_DATA_DIR/elfin/`, else
  `elfin_data/` (`config.py`, which first applies saved preferences from
  `pyspedas/preferences.py`). Setting `ELFIN_NO_DOWNLOAD` turns downloads off.

## Tests

`tests/test_epd_calibration.py` reads `tests/test_epde_cal_data.txt` and needs no
network. The others download data; `tests/test_epd_l2.py` also downloads IDL
tplot save files and compares against them. Run one with
`python -m pyspedas.projects.elfin.tests.test_epd_l1`. CI runs all five in
`.github/workflows/full_coverage.yml`.
