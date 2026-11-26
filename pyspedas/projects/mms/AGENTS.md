---
related_files:
  - pyspedas/projects/AGENTS.md
  - pyspedas/projects/mms/feeps_tools/AGENTS.md
  - pyspedas/projects/mms/fpi_tools/AGENTS.md
  - pyspedas/projects/mms/particles/AGENTS.md
  - pyspedas/projects/mms/__init__.py
  - pyspedas/projects/mms/config.py
  - pyspedas/projects/mms/mms_load_data.py
  - pyspedas/projects/mms/mms_load_data_spdf.py
  - pyspedas/projects/mms/mms_load_data_archive.py
  - pyspedas/projects/mms/tests/test_mms_sources.py
  - pyspedas/projects/mms/tests/test_mms_fpi.py
  - pyspedas/utilities/last_version_per_identity.py
  - pyspedas/projects/mms/mec_ascii/mms_get_state_data.py
  - pyspedas/projects/mms/mec_ascii/mms_get_tetrahedron_qf.py
  - pyspedas/projects/mms/databar_tools/mms_update_fast_intervals.py
  - pyspedas/projects/mms/databar_tools/mms_update_brst_intervals.py
  - pyspedas/projects/mms/databar_tools/mms_load_sroi_segments.py
  - pyspedas/projects/mms/mms_remove_old_files.py
  - pyspedas/projects/mms/mms_login_lasp.py
  - pyspedas/projects/mms/mms_files_in_interval.py
  - pyspedas/projects/mms/mms_get_local_files.py
  - pyspedas/projects/mms/mms_file_filter.py
  - pyspedas/projects/mms/fgm_tools/fgm.py
  - pyspedas/projects/mms/feeps_tools/feeps.py
  - pyspedas/projects/mms/mec_ascii/state.py
  - pyspedas/projects/mms/databar_tools/spd_mms_load_bss.py
  - pyspedas/projects/mms/deprecated/mms_load_fast_segments.py
  - pyspedas/projects/mms/mms_orbit_plot.py
  - pyspedas/projects/mms/mms_find_perigee_times.py
  - pyspedas/projects/mms/tests/test_mms_perigee.py
  - pyspedas/projects/mms/tests/test_mms_remove_old_files.py
  - .github/workflows/quick_tests.yml
  - .github/workflows/full_coverage.yml
  - pyspedas/projects/mms/mms_events.py
  - pyspedas/projects/mms/print_vars.py
  - pyspedas/projects/mms/mms_python_startup.py
  - pyspedas/projects/mms/README.md
  - pyspedas/projects/mms/tests/test_mms_login_lasp.py
  - pyspedas/__init__.py
  - pyspedas/preferences.py
  - pyspedas/utilities/dailynames.py
  - pyspedas/utilities/download.py
  - pyspedas/tplot_tools/importers/cdf_to_tplot.py
  - RULES.md
maintenance: |
  Update when mms_load_data.py or mms_load_data_spdf.py change how files are found or
  grouped, when mms_login_lasp.py changes credential handling, or when __init__.py adds,
  renames or removes a wrapper or an instrument package.
---

# MMS

Every change here follows `RULES.md` at the repository root. Read it before
you change code here.

Loaders and analysis tools for the four Magnetospheric Multiscale spacecraft. All CDF
instrument loaders go through `mms_load_data.py`, which selects the configured
SDC API or archive implementation for archive-capable products.

## Layout

- `<instr>_tools/`: one package per instrument (`aspoc`, `dsp`, `edi`, `edp`, `eis`,
  `feeps`, `fgm`, `fpi`, `fsm`, `hpca`, `mec`, `scm`). Each has `<instr>.py` with the
  loader `mms_load_<instr>`, usually a `mms_<instr>_set_metadata.py` for plot options,
  and extra analysis (EIS pitch angles, HPCA anode sums, curlometer `mms_curl` and
  linear gradient/curl estimator `mms_lingradest` in `fgm_tools/`). `feeps_tools/` and
  `fpi_tools/` have their own AGENTS.md.
- `particles/`: spectra, moments and 2D slices from FPI and HPCA distributions. Own AGENTS.md.
- `mec_ascii/`: `mms_load_state` (`mec_ascii/state.py`) and `mms_load_tetrahedron_qf`,
  which read the SDC's ASCII ancillary files (ephemeris/attitude and tetrahedron quality
  factor), not CDFs.
- `databar_tools/`: burst, fast and SROI segment bars and `spd_mms_load_bss`.
- `cotrans/`: `mms_qcotrans` (uses MEC quaternions), `mms_cotrans_lmn` and helpers.
- `plots/`, `mms_orbit_plot.py`, `mms_events.py`: overview and orbit plots, burst event text.
- `mms_find_perigee_times.py`: finds perigees bracketing an input time using
  survey L2 `epht89d` MEC ECI positions. Returns two Unix times, or None if
  both perigees cannot be found.
- `mms_remove_old_files.py`: previews obsolete local cache files by default;
  deletion with `dry_run=False` requires SDC checks before removing files.
- `deprecated/`: `mms_load_fast_segments` only logs an error and returns None. Skip it.

## How `mms_load_fgm()` loads data

The source-routing configuration API is experimental; its interface is being
evaluated with user feedback before it is finalized (see `config.py`).

`fgm_tools/fgm.py` calls `mms_load_data(instrument='fgm', ...)` and then post-processes
(flag removal, splitting, metadata). `mms_load_data()`:

1. With `spdf=True` or `CONFIG['data_access'] == 'archive'`, selects
   `mms_load_data_archive()` for supported instruments and levels (see below).
   SDC-only requests continue through the SDC path.
2. Unless `no_update` or `CONFIG['no_download']` is set, calls `mms_login_lasp()` for a
   `requests` session and user name.
3. Per probe, data rate, level and datatype, queries `.../files/api/v1/file_info/science`
   (under `sdc/public` when anonymous, `sdc/sitl` when logged in), and
   `mms_files_in_interval()` trims the list to `trange`.
4. Reuses a local file of the same size, else downloads it to
   `<local_data_dir>/mms<probe>/<instr>/<rate>/<level>/[<datatype>/]YYYY/MM[/DD for brst]`.
5. If nothing was found (offline or `no_update`), `mms_get_local_files()` searches that tree,
   then `CONFIG['mirror_data_dir']`.
6. `mms_file_filter()` applies `latest_version`, `major_version`, `min_version` and
   `cdf_version`, and each (probe, rate, level, datatype) group goes to `cdf_to_tplot()` separately.

`available=True` returns file names without downloading; `CONFIG['download_only']` returns
paths. `mms_load_data_archive()` builds per-instrument path templates and uses
`dailynames()` / `download()` against `CONFIG['remote_data_dir']`, whose default
is SPDF. `mms_load_data_spdf()` remains a compatibility wrapper and does not
modify configuration at import. The archive implementation preserves dictionary
results across groups, prefix/suffix, clipping, offline flags, download-only mode
and version filtering. `available` lists files without CDF transfers. Archive
requests select the lexicographically last CDF per product/timestamp identity
using `download(last_version=True, versioned_regex=MMS_VERSIONED_REGEX)`.
Explicit version filters defer selection until after `mms_file_filter()` runs;
its global latest/major-version semantics remain intact. The same selection
applies to available listings and local/mirror fallback results.

`config.py` defaults `data_access` to `sdc`, `remote_data_dir` to the SPDF MMS root,
and `sdc_data_dir` to `https://lasp.colorado.edu/mms/sdc/`. Matching `MMS_*`
environment variables override stored preferences. `sdc_url(path)` constructs
all SDC endpoints, including public/sitl science and ancillary queries,
authentication, burst/fast/SROI intervals, DES models, and cache-cleanup queries.
These support products use SDC regardless of archive selection. FSM, SITL/trigger
levels, and restricted FEEPS L1b requests also use SDC. A mixed-level request
containing SDC-only levels uses SDC for the whole request. Missing archive data
never trigger a switch to SDC. The archive URL names a mission root containing
`mms1/` through `mms4/`; no hostname inference or separate layout setting is used.

## Things to know

- The wrappers in `__init__.py` (`fgm`, `fpi`, `feeps`, `state`, `bss`, `curlometer`, ...)
  are `@wraps(f) def fgm(*args, **kwargs)`. The real signature is on the wrapped function:
  `mms_load_<instr>` in `<instr>_tools/<instr>.py`, `mms_load_state` in `mec_ascii/`,
  `spd_mms_load_bss` in `databar_tools/`. `pyspedas/__init__.py` also exports the
  `mms_load_*` names at top level.
- Login: `mms_login_lasp()` reads `~/mms_auth_info.pkl`, then the IDL `~/mms_auth_info.sav`
  (which wins if both exist), else prompts with `input()` and `getpass()`; a blank user
  means public access. A good prompted login is pickled; a 401 falls back to public.
  `always_prompt=True` forces the prompt. Logged-in users query `sdc/sitl`. The `feeps.py`
  docstring says FEEPS L1b data is "restricted to MMS team members at present".
- Names: `mms<probe>_<instr>_<quantity>_<rate>_<level>` (`mms1_fgm_b_gsm_srvy_l2`); FPI drops
  the level (`mms1_dis_numberdensity_fast`). Probes are strings `'1'`-`'4'`.
- Burst queries start 10 min early near midnight and `mms_files_in_interval()` keeps one
  file before `trange`, so use `time_clip=True` for exact ranges.
- Data folder (`config.py`): `MMS_DATA_DIR`, else `SPEDAS_DATA_DIR/mms`, else `pydata`,
  after stored preferences (`pyspedas/preferences.py`). `MMS_MIRROR_DATA_DIR` sets the read-only mirror.
- `print_vars.py` is an unused decorator; `mms_python_startup.py` is a PYTHONSTARTUP
  script, not imported by the package. `README.md` examples still use `pyspedas.mms`.

## Tests

`tests/` has test modules for loaders and tools; most download from the SDC.
`tests/test_mms_login_lasp.py` mocks the network and covers the credential fallbacks.

`tests/test_mms_sources.py` tests routing, SDC-only services, configurable URLs,
archive options, real cached CDFs, authentication and preferences without network
access; it is registered in quick_tests and full_coverage.
`tests/test_mms_remove_old_files.py` also uses mocked responses and temporary
local fixtures and runs in both workflows. `tests/test_mms_perigee.py` uses real
MEC data and runs only in `.github/workflows/full_coverage.yml`, since it can
contact the configured data source when data are not cached.
The offline source and cleanup tests are registered in `.github/workflows/quick_tests.yml`.

## Provider shortcuts

`config.py` defines provider-preset dictionaries and these setter/getter pairs:

- `set_data_source()` / `get_data_source()`: sdc, spdf, heliocloud.
- `set_sdc_source()` / `get_sdc_source()`: sdc.

Setters validate a case-sensitive tag before updating its CONFIG keys together,
log the resulting settings at INFO level, and neither access the network nor
save preferences. Getters match relevant current settings exactly and return
`None` for custom or incomplete settings, including direct CONFIG edits.
The existing offline routing tests also cover these APIs.
`tests/test_mms_fpi.py` includes live SPDF/heliocloud HPCA and EDP regressions
for issue #1582; each restores the complete configuration after running.

The main `sdc` preset resets its canonical SDC URL and access mode while
retaining the inactive archive URL. Archive presets retain the separate SDC
support URL. The independent SDC setter does not change access mode.
