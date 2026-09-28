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
  - pyspedas/projects/mms/mms_login_lasp.py
  - pyspedas/projects/mms/mms_files_in_interval.py
  - pyspedas/projects/mms/mms_get_local_files.py
  - pyspedas/projects/mms/mms_file_filter.py
  - pyspedas/projects/mms/fgm_tools/fgm.py
  - pyspedas/projects/mms/mec_ascii/state.py
  - pyspedas/projects/mms/databar_tools/spd_mms_load_bss.py
  - pyspedas/projects/mms/deprecated/mms_load_fast_segments.py
  - pyspedas/projects/mms/mms_orbit_plot.py
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
maintenance: |
  Update when mms_load_data.py or mms_load_data_spdf.py change how files are found or
  grouped, when mms_login_lasp.py changes credential handling, or when __init__.py adds,
  renames or removes a wrapper or an instrument package.
---

# MMS

Loaders and analysis tools for the four Magnetospheric Multiscale spacecraft. All CDF
instrument loaders go through `mms_load_data.py`, which asks the LASP Science Data
Center (SDC) file API for file names instead of reading a remote directory listing.

## Layout

- `<instr>_tools/`: one package per instrument (`aspoc`, `dsp`, `edi`, `edp`, `eis`,
  `feeps`, `fgm`, `fpi`, `fsm`, `hpca`, `mec`, `scm`). Each has `<instr>.py` with the
  loader `mms_load_<instr>`, usually a `mms_<instr>_set_metadata.py` for plot options,
  and extra analysis (EIS pitch angles, HPCA anode sums, curlometer `mms_curl` and
  `mms_lingradest` in `fgm_tools/`). `feeps_tools/` and `fpi_tools/` have their own AGENTS.md.
- `particles/`: spectra, moments and 2D slices from FPI and HPCA distributions. Own AGENTS.md.
- `mec_ascii/`: `mms_load_state` (`mec_ascii/state.py`) and `mms_load_tetrahedron_qf`,
  which read the SDC's ASCII ancillary ephemeris/attitude files, not CDFs.
- `databar_tools/`: burst, fast and SROI segment bars and `spd_mms_load_bss`.
- `cotrans/`: `mms_qcotrans` (uses MEC quaternions), `mms_cotrans_lmn` and helpers.
- `plots/`, `mms_orbit_plot.py`, `mms_events.py`: overview and orbit plots, burst event text.
- `deprecated/`: `mms_load_fast_segments` only logs an error and returns None. Skip it.

## How `mms_load_fgm()` loads data

`fgm_tools/fgm.py` calls `mms_load_data(instrument='fgm', ...)` and then post-processes
(flag removal, splitting, metadata). `mms_load_data()`:

1. With `spdf=True`, returns `mms_load_data_spdf()` instead (see below).
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
paths. `mms_load_data_spdf()` instead builds a per-instrument path template in an if/elif
chain and uses `dailynames()` and `download()` against `https://spdf.gsfc.nasa.gov/pub/data/mms/`;
an instrument without a branch there cannot use `spdf=True`.

## Things to know

- The wrappers in `__init__.py` (`fgm`, `fpi`, `feeps`, `state`, `bss`, `curlometer`, ...)
  are `@wraps(f) def fgm(*args, **kwargs)`. The real signature is on the wrapped function:
  `mms_load_<instr>` in `<instr>_tools/<instr>.py`, `mms_load_state` in `mec_ascii/`,
  `spd_mms_load_bss` in `databar_tools/`. `pyspedas/__init__.py` also exports the
  `mms_load_*` names at top level.
- Login: `mms_login_lasp()` reads `~/mms_auth_info.pkl`, then the IDL `~/mms_auth_info.sav`
  (which wins if both exist), else prompts with `input()` and `getpass()`; a blank user
  means public access. A good prompted login is pickled; a 401 falls back to public.
  `always_prompt=True` forces the prompt. Logged-in users query `sdc/sitl`, which also
  serves team-only data (for example FEEPS L1b).
- Names: `mms<probe>_<instr>_<quantity>_<rate>_<level>` (`mms1_fgm_b_gsm_srvy_l2`); FPI drops
  the level (`mms1_dis_numberdensity_fast`). Probes are strings `'1'`-`'4'`.
- Burst queries start 10 min early near midnight and `mms_files_in_interval()` keeps one
  file before `trange`, so use `time_clip=True` for exact ranges.
- Data folder (`config.py`): `MMS_DATA_DIR`, else `SPEDAS_DATA_DIR/mms`, else `pydata`,
  after stored preferences (`pyspedas/preferences.py`). `MMS_MIRROR_DATA_DIR` sets the read-only mirror.
- `print_vars.py` is an unused decorator; `mms_python_startup.py` is a PYTHONSTARTUP
  script, not imported by the package. `README.md` examples still use `pyspedas.mms`.

## Tests

`tests/` has one module per instrument or tool; most download from the SDC.
`tests/test_mms_login_lasp.py` mocks the network and covers the credential fallbacks.
