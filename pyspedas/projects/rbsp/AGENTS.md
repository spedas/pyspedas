---
related_files:
  - pyspedas/projects/AGENTS.md
  - pyspedas/projects/rbsp/__init__.py
  - pyspedas/projects/rbsp/config.py
  - pyspedas/projects/rbsp/load.py
  - pyspedas/projects/rbsp/emfisis.py
  - pyspedas/projects/rbsp/efw.py
  - pyspedas/projects/rbsp/rbspice.py
  - pyspedas/projects/rbsp/mageis.py
  - pyspedas/projects/rbsp/hope.py
  - pyspedas/projects/rbsp/rept.py
  - pyspedas/projects/rbsp/rps.py
  - pyspedas/projects/rbsp/magephem.py
  - pyspedas/projects/rbsp/datasets.py
  - pyspedas/projects/rbsp/rbspice_lib/rbsp_load_rbspice_read.py
  - pyspedas/projects/rbsp/rbspice_lib/rbsp_rbspice_omni.py
  - pyspedas/projects/rbsp/rbspice_lib/rbsp_rbspice_spin_avg.py
  - pyspedas/projects/rbsp/rbspice_lib/rbsp_rbspice_pad.py
  - pyspedas/projects/rbsp/rbspice_lib/rbsp_rbspice_pad_spinavg.py
  - pyspedas/projects/rbsp/README.md
  - pyspedas/projects/rbsp/tests/test_rbsp.py
  - pyspedas/utilities/datasets.py
  - pyspedas/preferences.py
  - .github/workflows/quick_tests.yml
maintenance: |
  Update when load.py changes an instrument branch or its instrument-specific
  keywords, when the RBSPICE post-processing in rbspice.py or rbspice_lib/
  changes, or when __init__.py adds a loader.
---

# RBSP (Van Allen Probes)

Loaders for the two Van Allen Probes, `a` and `b`: EMFISIS, EFW, RBSPICE, the
ECT suite (MagEIS, HOPE, REPT), the RPS proton spectrometer and the ECT magnetic
ephemeris. All data are daily CDF files from SPDF
(`https://spdf.gsfc.nasa.gov/pub/data/rbsp/`).

## Layout

- `emfisis.py`, `efw.py`, `rbspice.py`, `mageis.py`, `hope.py`, `rept.py`,
  `rps.py`, `magephem.py`: one wrapper per instrument, each calling `load()`.
- `load.py`: `load()`, the path-template chain for all instruments.
- `rbspice_lib/`: RBSPICE post-processing. `rbsp_load_rbspice_read()` adds
  energy tables and per-telescope variables; `rbsp_rbspice_omni()` and
  `rbsp_rbspice_spin_avg()` make omni-directional and spin-averaged spectra;
  `rbsp_rbspice_pad()` (exported by `__init__.py`, called by the user, not the
  loader) makes pitch-angle distributions and their spin averages through
  `rbsp_rbspice_pad_spinavg()`.
- `datasets.py`: `datasets()`, lists RBSP datasets on CDAWeb through
  `find_datasets()` (`pyspedas/utilities/datasets.py`).
- `config.py`, `tests/test_rbsp.py`, `README.md` (user guide; most examples use
  the pre-2.0 path `pyspedas.rbsp`).

## How it works

`load()` loops over `probe` (`'a'`, `'b'` or a list), builds an f-string
template rooted at `rbsp<probe>/<level>/...`, downloads with `dailynames()` and
`download()`, and loads with `cdf_to_tplot()` inside the loop. ECT files sit
under `rbsp<probe>/<level>/ect/<instr>/...` and the ephemeris under
`rbsp<probe>/ephemeris/ect-mag-ephem/cdf/def-<cadence>-<coord>/`. Templates end
in `_v*.cdf` (EFW `_v??.cdf`), and `last_version` is not passed, so every
matching version on the server is downloaded.

`rbspice()` then runs, for each probe, `rbsp_load_rbspice_read()`,
`rbsp_rbspice_omni()` and `rbsp_rbspice_spin_avg()` and adds the new variable
names to its return list.

## Things to know

- `load()` takes several instrument-specific keywords, exposed only by the
  matching wrapper: `cadence`, `coord` and `wavetype` for EMFISIS (`'4sec'`,
  `'sm'`, `'waveform'`); `cadence` (`'1min'`/`'5min'`) and `coord` (`op77q`,
  `t89d`, `t89q`, `ts04d`) for `magephem`, which falls back to `1min`/`op77q`
  on bad values; `rel` for MagEIS, HOPE and REPT (default `'rel04'`, but
  `'rel03'` for `rept()`).
- EMFISIS `datatype='magnetometer'` with `level='l2'` reads the `uvw` files and
  ignores `cadence` and `coord`.
- Only RBSPICE gets an automatic prefix, `rbsp<probe>_rbspice_<level>_<datatype>_`
  after any user prefix. The `rbspice_lib` helpers look variables up by that
  bare prefix, so a user `prefix` or `suffix` makes the post-processing find
  nothing. Other instruments keep their CDF names (`Mag`, `Magnitude`), so
  probes overwrite each other unless loaded with separate prefixes.
- `rbspice()` and `rps()` default to `get_support_data=True`.
- The local data folder is `RBSP_DATA_DIR`, else `SPEDAS_DATA_DIR/rbsp`, else
  `rbsp_data/` (`config.py`, which first applies saved preferences from
  `pyspedas/preferences.py`). Setting `RBSP_NO_DOWNLOAD` turns downloads off.

## Tests

`python -m pyspedas.projects.rbsp.tests.test_rbsp` (downloads data). CI runs it
in `.github/workflows/quick_tests.yml`.
