---
related_files:
  - pyspedas/projects/AGENTS.md
  - pyspedas/projects/ace/__init__.py
  - pyspedas/projects/ace/config.py
  - pyspedas/projects/ace/load.py
  - pyspedas/projects/ace/mfi.py
  - pyspedas/projects/ace/swe.py
  - pyspedas/projects/ace/epam.py
  - pyspedas/projects/ace/cris.py
  - pyspedas/projects/ace/sis.py
  - pyspedas/projects/ace/uleis.py
  - pyspedas/projects/ace/sepica.py
  - pyspedas/projects/ace/swics.py
  - pyspedas/projects/ace/datasets.py
  - pyspedas/projects/ace/README.md
  - pyspedas/projects/ace/tests/test_ace.py
  - pyspedas/utilities/datasets.py
  - pyspedas/preferences.py
  - .github/workflows/quick_tests.yml
maintenance: |
  Update when load.py adds or changes an instrument branch or path template, when
  a wrapper's instrument code or default datatype changes, or when __init__.py
  adds a loader.
---

# ACE

Loaders for the Advanced Composition Explorer at L1: magnetic field, solar wind
plasma, energetic particles and composition. All data are daily CDF files from
SPDF (`https://spdf.gsfc.nasa.gov/pub/data/ace/`).

## Layout

- `mfi.py`, `swe.py`, `epam.py`, `cris.py`, `sis.py`, `uleis.py`, `sepica.py`,
  `swics.py`: one wrapper per instrument, each calling `load()`.
- `load.py`: `load()`, the path-template chain for all instruments.
- `datasets.py`: `datasets()`, lists ACE datasets on CDAWeb through
  `find_datasets()` (`pyspedas/utilities/datasets.py`).
- `config.py`, `tests/test_ace.py`, `README.md` (user guide; its examples use the
  pre-2.0 path `pyspedas.ace`).

## How it works

Each wrapper calls `load()` with an instrument code; four differ from the
wrapper name: `mfi()` passes `'fgm'`, `epam()` `'epm'`, `uleis()` `'ule'` and
`sepica()` `'sep'`. `load()` picks a template such as
`mag/level_2_cdaweb/mfi_<datatype>/%Y/ac_<datatype>_mfi_%Y%m%d_v??.cdf` and runs
the usual `dailynames()`, `download()`, `cdf_to_tplot()` pipeline, then
`time_clip` if asked. `swics` is the odd one: its datatype has the form
`<product>_<cadence>` (`sw2_h3`, `swi_h2`), names the folder as given, and is
reversed in the file name (`ac_h3_sw2_...`).

## Things to know

- `datatype` is the CDAWeb product code (`h0`-`h3` Level 2, `k0`-`k2` key
  parameters). Defaults differ: `mfi` `h3`, `swe` `h0`, `epam` and `sis` `k0`,
  `cris`, `uleis` and `sepica` `h2`, `swics` `sw2_h3`.
- There is no automatic prefix. Variables keep their CDF names (`BGSEc`, `Np`,
  `H_lo`), and `epam()` and `sis()` both create `H_lo`, so use `prefix` or
  `suffix` when loading several instruments or cadences together.
- Only `mfi()` post-processes: it sets `ytitle` and `legend_names` on `BGSEc` and
  `Magnitude`.
- The local data folder is `ACE_DATA_DIR`, else `SPEDAS_DATA_DIR/ace`, else
  `ace_data/` (`config.py`, which first applies saved preferences from
  `pyspedas/preferences.py`). Setting `ACE_NO_DOWNLOAD` turns downloads off.

## Tests

`python -m pyspedas.projects.ace.tests.test_ace` (downloads data). CI runs it in
`.github/workflows/quick_tests.yml`.
