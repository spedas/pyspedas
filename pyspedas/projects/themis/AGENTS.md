---
related_files:
  - pyspedas/projects/AGENTS.md
  - pyspedas/projects/themis/spacecraft/AGENTS.md
  - pyspedas/projects/themis/state_tools/AGENTS.md
  - pyspedas/projects/themis/__init__.py
  - pyspedas/projects/themis/config.py
  - pyspedas/projects/themis/ground/gmag.py
  - pyspedas/projects/themis/tests/test_themis_versions.py
  - pyspedas/projects/themis/tests/test_themis_s3.py
  - pyspedas/projects/themis/load.py
  - pyspedas/projects/themis/common/check_args.py
  - pyspedas/projects/themis/tests/test_themis_check_args.py
  - pyspedas/projects/themis/spacecraft/fields/fgm.py
  - pyspedas/projects/themis/README.md
  - pyspedas/utilities/dailynames.py
  - pyspedas/utilities/download.py
  - pyspedas/tplot_tools/importers/cdf_to_tplot.py
  - RULES.md
maintenance: |
  Update when load.py's instrument chain or keywords change, when __init__.py
  adds or renames a loader, or when a subfolder gets its own AGENTS.md.
---

# THEMIS / ARTEMIS

Every change here follows `RULES.md` at the repository root. Read it before
you change code here.

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
`CONFIG['ssc_remote_data_dir']` instead of the main URL. A new loader needs a branch in `load.py`, a
wrapper module, and an import in `__init__.py`.

## Things to know

- `__init__.py` imports each loader function over its module name, so
  `pyspedas.projects.themis.fgm` is the function, not the module.
- Wrappers don't pass every `load()` keyword through (`fgm()` has no `prefix` or
  `force_download`), so check the wrapper's signature before relying on one.
- The local data folder is `THM_DATA_DIR`, else `SPEDAS_DATA_DIR/themis`, else
  the `local_data_dir` preference, else `themis_data/` (`config.py`). Setting
  `THM_NO_DOWNLOAD` to `true`, `1` or `yes` turns downloads off.

## Source routing

`config.py` defines explicit `remote_data_layout` (`themis` or `spdf`) alongside
`remote_data_dir`. THEMIS and UCLA use `themis`; SPDF and heliocloud use `spdf`.
`resolve_source()` validates the main or variometer URL/layout pair. State with
no version uses an unversioned link for `themis`, or a version wildcard with
highest-version selection for `spdf`. Explicit versions request exact files.
Other instrument version defaults are unchanged.

GMAG variometers use `variometer_remote_data_dir` and
`variometer_remote_data_layout`; mixed-station requests associate each file path
with its source. `ground/gmag.py` downloads metadata from the full URL in
`gmag_metadata_file` to `thg/gmags_meta.csv` beneath the local cache root.
`no_update` and `no_download` apply to metadata; an unavailable metadata file
raises `FileNotFoundError`. The in-memory metadata table is invalidated when
its URL or cache root changes. Both SSC products use `ssc_remote_data_dir`.

Source settings support matching `THM_*` environment variables after stored
preferences. Data URLs name mission roots. Cache paths follow server layouts;
there is no automatic source fallback. `tests/test_themis_versions.py` checks
routing, versions, metadata caching and preferences offline.
`tests/test_themis_s3.py` uses S3 science data with separately configured THEMIS
variometers and metadata in temporary caches.
