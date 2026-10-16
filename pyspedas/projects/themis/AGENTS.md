---
related_files:
  - pyspedas/projects/AGENTS.md
  - pyspedas/projects/themis/spacecraft/AGENTS.md
  - pyspedas/projects/themis/state_tools/AGENTS.md
  - pyspedas/projects/themis/__init__.py
  - pyspedas/projects/themis/config.py
  - pyspedas/projects/themis/load.py
  - pyspedas/projects/themis/common/check_args.py
  - pyspedas/projects/themis/tests/test_themis_check_args.py
  - pyspedas/projects/themis/spacecraft/fields/fgm.py
  - pyspedas/projects/themis/README.md
  - pyspedas/utilities/dailynames.py
  - pyspedas/utilities/download.py
  - pyspedas/tplot_tools/importers/cdf_to_tplot.py
maintenance: |
  Update when load.py's instrument chain or keywords change, when __init__.py
  adds or renames a loader, or when a subfolder gets its own AGENTS.md.
---

# THEMIS / ARTEMIS

## Layout

- `spacecraft/fields/` (`fgm`, `fit`, `efi`, `fft`, `fbk`, `scm`),
  `spacecraft/particles/` (`esa`, `esd`, `sst`, `mom`, `gmom`) and `ground/`
  (`gmag`, `ask`): one loader per module. `spacecraft/` has its own AGENTS.md.
- `state_tools/`: orbit and attitude (`state`), the spin model, Solar and
  Lunar Ephemeris data (`slp`), and CDAWeb/SSCWeb orbit data (`ssc`). Has its
  own AGENTS.md.
- `cotrans/`: THEMIS coordinate systems (`dsl2gse`, `ssl2dsl`, `gse2sse`, `sse2sel`).
- `analysis/`: density from spacecraft potential (`scpot2dens`).
- `common/check_args.py`: validates and normalizes `probe` and `level`
  arguments; no loader imports it, only `tests/test_themis_check_args.py`.
- `tests/`: unittest modules; most download data.
- `README.md`: user guide with examples.

## How `fgm()` loads data

`spacecraft/fields/fgm.py` calls `load(instrument='fgm')` in `load.py`. `load()`
picks the file path template for the instrument in an if/elif chain, expands it
over the time range with `dailynames()` (`pyspedas/utilities/dailynames.py`),
downloads from `CONFIG['remote_data_dir']` (set in `config.py`) with `download()`
(`pyspedas/utilities/download.py`), and stores the files as tplot variables with
`cdf_to_tplot()` (`pyspedas/tplot_tools/importers/cdf_to_tplot.py`). The other
loaders here also call `load()`; for `ssc` and `ssc_pre`, `load()` downloads from
CDAWeb instead of `CONFIG['remote_data_dir']`. A new loader needs a branch in `load.py`, a
wrapper module, and an import in `__init__.py`.

## Things to know

- `__init__.py` imports each loader function over its module name, so
  `pyspedas.projects.themis.fgm` is the function, not the module.
- Wrappers don't pass every `load()` keyword through (`fgm()` has no `prefix` or
  `force_download`), so check the wrapper's signature before relying on one.
- The local data folder is `THM_DATA_DIR`, else `SPEDAS_DATA_DIR/themis`, else
  the `local_data_dir` preference, else `themis_data/` (`config.py`). Setting
  `THM_NO_DOWNLOAD` to `true`, `1` or `yes` turns downloads off.
