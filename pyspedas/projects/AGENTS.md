---
related_files:
  - AGENTS.md
  - pyspedas/projects/ace/AGENTS.md
  - pyspedas/projects/akebono/AGENTS.md
  - pyspedas/projects/barrel/AGENTS.md
  - pyspedas/projects/cluster/AGENTS.md
  - pyspedas/projects/elfin/AGENTS.md
  - pyspedas/projects/erg/AGENTS.md
  - pyspedas/projects/fast/AGENTS.md
  - pyspedas/projects/geotail/AGENTS.md
  - pyspedas/projects/goes/AGENTS.md
  - pyspedas/projects/image/AGENTS.md
  - pyspedas/projects/kyoto/AGENTS.md
  - pyspedas/projects/maven/AGENTS.md
  - pyspedas/projects/mms/AGENTS.md
  - pyspedas/projects/polar/AGENTS.md
  - pyspedas/projects/psp/AGENTS.md
  - pyspedas/projects/rbsp/AGENTS.md
  - pyspedas/projects/secs/AGENTS.md
  - pyspedas/projects/soho/AGENTS.md
  - pyspedas/projects/solo/AGENTS.md
  - pyspedas/projects/stereo/AGENTS.md
  - pyspedas/projects/themis/AGENTS.md
  - pyspedas/projects/ulysses/AGENTS.md
  - pyspedas/projects/wind/AGENTS.md
  - pyspedas/projects/__init__.py
  - pyspedas/projects/cnofs/load.py
  - pyspedas/projects/de2/__init__.py
  - pyspedas/projects/galileo/load.py
  - pyspedas/projects/juno/load.py
  - pyspedas/projects/kompsat/load.py
  - pyspedas/projects/kompsat/esa_hapi_data.py
  - pyspedas/projects/mica/load.py
  - pyspedas/projects/noaa/noaa_load_kp.py
  - pyspedas/projects/omni/load.py
  - pyspedas/projects/omni/omni_solarwind_load.py
  - pyspedas/projects/poes/load.py
  - pyspedas/projects/swarm/load.py
  - pyspedas/projects/mms/mms_load_data.py
  - pyspedas/projects/maven/download_files_utilities.py
  - pyspedas/projects/cluster/load_csa.py
  - pyspedas/preferences.py
  - pyspedas/__init__.py
  - pyspedas/utilities/dailynames.py
  - pyspedas/utilities/download.py
  - pyspedas/utilities/datasets.py
  - pyspedas/utilities/pyspedas_functools.py
  - pyspedas/utilities/das2
  - pyspedas/hapi_tools/hapi.py
  - pyspedas/tplot_tools/importers/cdf_to_tplot.py
  - pyspedas/tplot_tools/importers/netcdf_to_tplot.py
  - pyspedas/tplot_tools/importers/sts_to_tplot.py
  - pyspedas/tplot_tools/tplot_math/time_clip.py
maintenance: |
  Update when a mission package is added, removed or renamed (also in __init__.py),
  when a mission gets or loses its own AGENTS.md, or when a mission changes data
  server or leaves the shared config.py/load.py pipeline.
---

# Mission packages

One package per mission (39). `__init__.py` imports all of them, so `import pyspedas`
loads every mission, and `pyspedas.projects.<mission>.<instrument>()` is the entry point.

## Missions

Entries marked AGENTS.md have their own file; the others list their public loaders.

- `ace/`: ACE, SPDF. AGENTS.md: [ace/AGENTS.md](ace/AGENTS.md)
- `akebono/`: Akebono, JAXA DARTS. AGENTS.md: [akebono/AGENTS.md](akebono/AGENTS.md)
- `barrel/`: BARREL balloons, SPDF. AGENTS.md: [barrel/AGENTS.md](barrel/AGENTS.md)
- `cluster/`: Cluster, SPDF and the ESA Cluster Science Archive. AGENTS.md: [cluster/AGENTS.md](cluster/AGENTS.md)
- `cnofs/`: C/NOFS, SPDF: `cindi()`, `plp()`, `vefi()` over `load()`.
- `csswe/`: CSSWE, SPDF: `reptile()` over `load()`.
- `de2/`: Dynamics Explorer 2, SPDF: `mag`, `nacs`, `rpa`, `fpi`, `idm`, `wats`, `vefi`, `lang`, all `better_partial(load, instrument=...)` in `de2/__init__.py`.
- `dscovr/`: DSCOVR, SPDF: `mag`, `fc`, `orb`, `att`, `all` (partials of `load()`).
- `elfin/`: ELFIN, UCLA server. AGENTS.md: [elfin/AGENTS.md](elfin/AGENTS.md)
- `equator_s/`: Equator-S, SPDF: `mam`, `edi`, `epi`, `ici`, `pcd`, `sfd` (partials of `load()`).
- `erg/`: Arase (ERG) satellite and ground networks, ERG Science Center. AGENTS.md: [erg/AGENTS.md](erg/AGENTS.md)
- `fast/`: FAST, SPDF. AGENTS.md: [fast/AGENTS.md](fast/AGENTS.md)
- `galileo/`: Galileo, Iowa das2 server: `load(datatype=...)` in `galileo/load.py`; `get_info()` lists datasets.
- `geotail/`: Geotail, SPDF. AGENTS.md: [geotail/AGENTS.md](geotail/AGENTS.md)
- `goes/`: GOES, NCEI netCDF. AGENTS.md: [goes/AGENTS.md](goes/AGENTS.md)
- `image/`: IMAGE, SPDF. AGENTS.md: [image/AGENTS.md](image/AGENTS.md)
- `juno/`: Juno, Iowa das2 server: `load(datatype=...)` in `juno/load.py`.
- `kompsat/`: GEO-KOMPSAT-2A SOSMAG and KSEM, ESA HAPI server: `load(datatype=...)` in `kompsat/load.py`, also `pyspedas.kompsat_load`.
- `kyoto/`: Kyoto WDC AE and Dst indices. AGENTS.md: [kyoto/AGENTS.md](kyoto/AGENTS.md)
- `lanl/`: LANL geosynchronous MPA and SPA, SPDF: `mpa()`, `spa()`.
- `maven/`: MAVEN, LASP MAVEN SDC. AGENTS.md: [maven/AGENTS.md](maven/AGENTS.md)
- `mica/`: MICA induction magnetometers, UNH server: `induction()` (alias of `load(site=...)` in `mica/load.py`).
- `mms/`: MMS, LASP SDC. AGENTS.md: [mms/AGENTS.md](mms/AGENTS.md)
- `noaa/`: Kp and Ap indices, GFZ Potsdam or NOAA NGDC: `noaa_load_kp()` in `noaa/noaa_load_kp.py`, also `pyspedas.noaa_load_kp`; env `KP_DATA_DIR`.
- `omni/`: OMNI, SPDF: `data()` (alias of `load()` in `omni/load.py`; `datatype` '1min', '5min', 'hourly'); `omni_solarwind_load()` in `omni/omni_solarwind_load.py` feeds `lmn_matrix_make`.
- `poes/`: POES/MetOp SEM, SPDF or NCEI: `sem()` over `load()` in `poes/load.py` (`ncei_server`, `ncei_l1b_server`).
- `polar/`: Polar, SPDF. AGENTS.md: [polar/AGENTS.md](polar/AGENTS.md)
- `psp/`: Parker Solar Probe, SPDF and team servers. AGENTS.md: [psp/AGENTS.md](psp/AGENTS.md)
- `rbsp/`: Van Allen Probes, SPDF. AGENTS.md: [rbsp/AGENTS.md](rbsp/AGENTS.md)
- `secs/`: SECS and EICS ionospheric currents, UCLA and SPDF. AGENTS.md: [secs/AGENTS.md](secs/AGENTS.md)
- `soho/`: SOHO, SPDF. AGENTS.md: [soho/AGENTS.md](soho/AGENTS.md)
- `solo/`: Solar Orbiter, SPDF. AGENTS.md: [solo/AGENTS.md](solo/AGENTS.md)
- `st5/`: Space Technology 5, SPDF: `mag()` over `load()`.
- `stereo/`: STEREO, Berkeley SPRG mirror. AGENTS.md: [stereo/AGENTS.md](stereo/AGENTS.md)
- `swarm/`: Swarm, VirES HAPI server: `mag()` over `load()` in `swarm/load.py`, which calls `hapi()` (`pyspedas/hapi_tools/hapi.py`).
- `themis/`: THEMIS/ARTEMIS, Berkeley. AGENTS.md: [themis/AGENTS.md](themis/AGENTS.md)
- `twins/`: TWINS, SPDF: `ephemeris()`, `lad()`, `imager()`.
- `ulysses/`: Ulysses, SPDF. AGENTS.md: [ulysses/AGENTS.md](ulysses/AGENTS.md)
- `wind/`: Wind, SPDF. AGENTS.md: [wind/AGENTS.md](wind/AGENTS.md)

## Shared loader conventions

- `<mission>/config.py` defines `CONFIG` (`local_data_dir`, `remote_data_dir`, `no_download`),
  then applies user preferences with `apply_mission_preferences()` (`pyspedas/preferences.py`),
  then environment variables: `SPEDAS_DATA_DIR` gives a mission subfolder of it, a mission
  variable such as `CNOFS_DATA_DIR` overrides that, and `<PREFIX>_NO_DOWNLOAD` goes through
  `apply_no_download_environment()`. Precedence: defaults, preferences file, environment,
  explicit arguments. Prefixes don't always match the folder name (`DSC_`, `EQUATORS_`, `ULY_`).
- `<mission>/load.py` has one `load()`; `cnofs/load.py` is a minimal example. It picks a
  path template with strftime codes in an if/elif chain on `instrument`/`datatype`, expands it
  with `dailynames()` (`pyspedas/utilities/dailynames.py`), fetches with `download()`
  (`pyspedas/utilities/download.py`, `no_download=no_update or CONFIG['no_download']`), reads with
  `cdf_to_tplot()` (`pyspedas/tplot_tools/importers/cdf_to_tplot.py`), and with `time_clip=True`
  clips in place via `time_clip(..., suffix='')` (`pyspedas/tplot_tools/tplot_math/time_clip.py`).
- Standard keywords: `trange`, `instrument`, `datatype`, `prefix`, `suffix`, `get_support_data`,
  `varformat`, `varnames`, `downloadonly`, `notplot`, `no_update`, `time_clip`, `force_download`.
  Wrappers don't always pass all of them through.
- Instrument wrappers are either one module per instrument calling `load(instrument=...)`, or
  `better_partial(load, instrument=...)` (`pyspedas/utilities/pyspedas_functools.py`) in
  `__init__.py` (de2, dscovr, equator_s, fast, goes).
- `datasets()` wrappers call `find_datasets()` (`pyspedas/utilities/datasets.py`), which queries
  the CDAWeb CDAS web service. The loaders themselves read SPDF directory listings, not CDAS.

## Missions that leave the shared pipeline

- MMS: `mms/mms_load_data.py` queries the LASP SDC file API; `CONFIG` has no
  `remote_data_dir`; `spdf=True` switches to SPDF.
- MAVEN: LASP MAVEN SDC API (`maven/download_files_utilities.py`), KP and STS files
  (`sts_to_tplot`, `pyspedas/tplot_tools/importers/sts_to_tplot.py`).
- Cluster: `cluster/load_csa.py` reads the ESA Cluster Science Archive in addition to SPDF.
- GOES and POES L1b (`ncei_l1b_server=True`) read netCDF with `netcdf_to_tplot`
  (`pyspedas/tplot_tools/importers/netcdf_to_tplot.py`) from NCEI; GOES orbits come from SPDF CDFs.
- Kyoto, NOAA and SECS parse text or HTML files instead of CDF.
- Galileo and Juno use the das2 helpers in `pyspedas/utilities/das2`; Swarm and KOMPSAT use
  HAPI servers (KOMPSAT gets an OAuth2 token in `kompsat/esa_hapi_data.py` and has no `config.py`).
- PSP takes `username`/`password` for team-only SWEAP and FIELDS data; ERG honors
  `ERG_REMOTE_DATA_DIR`.
