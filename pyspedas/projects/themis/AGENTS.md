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
`resolve_source()` validates the single mission URL/layout pair. Satellite
products and every ground network, including GMAG variometers, use that source.
State with no version uses an unversioned link for `themis`, or a version wildcard
with highest-version selection for `spdf`. Explicit versions request exact files.
Other instrument version defaults are unchanged.

`ground/gmag.py` derives metadata from `thg/gmags_meta.csv` beneath the main URL
and caches it at the same relative path beneath `local_data_dir`. S3 metadata is
copied locally instead of streamed, preserving offline use. `no_update` and
`no_download` apply to metadata; unavailable metadata raises `FileNotFoundError`.
The in-memory metadata table is invalidated when the main URL or cache root
changes. Both SSC products independently use `ssc_remote_data_dir`.

The three source settings support matching `THM_*` environment variables after
stored preferences. Data URLs name mission roots. Cache paths follow server
layouts; there is no automatic source fallback. `tests/test_themis_versions.py`
checks routing, versions, S3 metadata caching and preferences offline.
`tests/test_themis_s3.py` uses only S3 mission data in temporary caches. Its GMAG
class is temporarily skipped pending metadata/variometer synchronization; no
alternate metadata or station source is injected.

## Provider shortcuts

`config.py` defines provider-preset dictionaries and these setter/getter pairs:

- `set_data_source()` / `get_data_source()`: berkeley, ucla, spdf, heliocloud.
- `set_ssc_source()` / `get_ssc_source()`: spdf.

Setters validate a case-sensitive tag before updating its CONFIG keys together,
log the resulting settings at INFO level, and neither access the network nor
save preferences. Getters match relevant current settings exactly and return
`None` for custom or incomplete settings, including direct CONFIG edits.
The existing offline routing tests also cover these APIs.
The SSC `spdf` preset uses the existing CDAWeb endpoint. All main presets include
GMAG variometers and station metadata through the common mission root. Source
changes trigger lazy in-memory metadata cache invalidation. Incomplete heliocloud
holdings are an ingest/backfill issue, not a different layout or routing policy.
