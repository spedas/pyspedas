---
related_files:
  - pyspedas/projects/AGENTS.md
  - pyspedas/projects/maven/__init__.py
  - pyspedas/projects/maven/config.py
  - pyspedas/projects/maven/maven_load.py
  - pyspedas/projects/maven/download_files_utilities.py
  - pyspedas/projects/maven/file_regex.py
  - pyspedas/projects/maven/orbit_time.py
  - pyspedas/projects/maven/maven_kp_to_tplot.py
  - pyspedas/projects/maven/read_iuvs_file.py
  - pyspedas/projects/maven/read_iuvs_file_unused_modes.py
  - pyspedas/projects/maven/utilities.py
  - pyspedas/projects/maven/kp_utilities.py
  - pyspedas/projects/maven/interp_utilities.py
  - pyspedas/projects/maven/list_utilities.py
  - pyspedas/projects/maven/access.txt
  - pyspedas/projects/maven/mag.py
  - pyspedas/projects/maven/swea.py
  - pyspedas/projects/maven/swia.py
  - pyspedas/projects/maven/sta.py
  - pyspedas/projects/maven/sep.py
  - pyspedas/projects/maven/lpw.py
  - pyspedas/projects/maven/euv.py
  - pyspedas/projects/maven/iuv.py
  - pyspedas/projects/maven/ngi.py
  - pyspedas/projects/maven/rse.py
  - pyspedas/projects/maven/kp.py
  - pyspedas/projects/maven/spdf/__init__.py
  - pyspedas/projects/maven/spdf/load.py
  - pyspedas/projects/maven/spdf/config.py
  - pyspedas/projects/maven/spdf/README.md
  - pyspedas/projects/maven/README.md
  - pyspedas/projects/maven/tests/test_maven.py
  - pyspedas/projects/maven/tests/test_maven_uri.py
  - pyspedas/preferences.py
  - .github/workflows/full_coverage.yml
maintenance: |
  Update when the SDC query or download logic in maven_load.py or
  download_files_utilities.py changes (URLs, credentials, KP linking, variable
  suffixes), when a wrapper gains or loses the spdf route, or when spdf/load.py
  adds an instrument.
---

# MAVEN

Loaders for the MAVEN Mars orbiter. The default route asks the MAVEN Science
Data Center (SDC) file API at LASP which files exist and downloads them one by
one; it is unlike the directory-listing loaders of other missions. Some
wrappers also have `spdf=True`, which reads CDFs from SPDF with the usual
pipeline through the `spdf/` subpackage.

## Layout

- `mag.py`, `swea.py`, `swia.py`, `sta.py`, `sep.py`, `lpw.py`, `euv.py`,
  `iuv.py`, `ngi.py`, `rse.py`, `kp.py`: wrappers calling `load_data()`. SWEA,
  SWIA and STATIC use the SDC instrument codes `swe`, `swi` and `sta`.
- `maven_load.py`: `load_data()` (exported as `maven_load`), `maven_filenames()`
  (the SDC query) and `maven_file_groups()`.
- `download_files_utilities.py`: SDC requests (`get_filenames()`,
  `get_file_from_site()`), `get_new_files()`, local folder helpers and the NAIF
  orbit-file download (`get_orbit_files()`).
- `file_regex.py`: file-name regexes; `orbit_time.py`: orbit number to time.
- `maven_kp_to_tplot.py`, `read_iuvs_file.py`, `utilities.py`: read Key
  Parameter (KP) `.tab` files, insitu and IUVS, into `mvn_kp::...` variables.
- `kp_utilities.py`, `interp_utilities.py`, `list_utilities.py`,
  `read_iuvs_file_unused_modes.py`: not used by the loaders (the tests exercise
  `kp_utilities`). `access.txt` is read only by `get_access()`, whose call in
  `maven_filenames()` is disabled.
- `spdf/`: `load()` and `functools.partial` aliases `mag`, `swea`, `swia`,
  `static`, `sep`, `kp`, with its own `spdf/config.py` and `spdf/README.md`.
- `config.py`, `tests/`, `README.md` (user guide; its examples use the pre-2.0
  path `pyspedas.maven`).

## How `load_data()` works

1. `maven_filenames()` sends `instrument=...&level=...&start_date=...&end_date=...`
   to `https://lasp.colorado.edu/maven/sdc/public/files/api/v1/search/science/fn_metadata/file_names`
   (the `.../sdc/service/...` URL when `public=False`). With `load_kp=True`, the
   default, it also asks for the insitu KP files of the same days. Integer
   `trange` values are orbit numbers, converted with NAIF orbit files and
   `orbit_time()`.
2. `load_data()` keeps the names whose description contains a requested
   `datatype` (for STATIC, `<datatype>-`), skips files already under
   `<local_data_dir>/maven/data/sci/<instr>/<level>/<YYYY>/<MM>/`
   (`get_new_files()`), and downloads the rest with `get_file_from_site()`,
   sleeping 10 s after each file.
3. CDFs go through `cdf_to_tplot()`, MAG `.sts` files through `sts_to_tplot()`
   and KP `.tab` files through `maven_kp_to_tplot()`. Every new variable is then
   `link()`ed to the KP spacecraft position (`mvn_kp::spacecraft::altitude`,
   `mso_x`, `geo_x`, ...).

## Things to know

- Each file's description is appended to its variable names before the user
  `suffix` (`data_d0-32e4d16a8m`); `suffix='empty'` turns this off.
- `auto_yes=True` (the wrappers' default) skips an `input()` prompt that
  `load_data()` shows before downloading. The wrappers have no `time_clip`,
  `notplot` or `no_update`, and `downloadonly=True` returns None.
- `mag(public=False)` sends `CONFIG['maven_username']` and
  `CONFIG['maven_password']` from `config.py` (empty by default; set them in
  code or in the preferences file) as basic auth to the `service` URLs. Only
  `mag()` exposes `public`; `kp()` has `insitu` and `iuvs` but no `load_kp`.
- `spdf=True` (on `mag`, `swea`, `swia`, `sta`, `sep`, `kp`) drops `prefix`,
  `suffix` and `load_kp`, uses SPDF datatype names (`sunstate-1sec` for MAG,
  `c0-64e2m` for STATIC, `kp-4sec` for KP) and skips the KP linking. The
  `spdf/load.py` downloader has no `force_download`.
- Both `config.py` files use `MAVEN_DATA_DIR`, else `SPEDAS_DATA_DIR/maven`;
  the defaults differ (`maven_data/` for SDC, `maven/` for SPDF). Saved
  preferences (`pyspedas/preferences.py`) use the sections `maven` and
  `maven.spdf`. There is no `MAVEN_NO_DOWNLOAD`.

## Tests

`python -m pyspedas.projects.maven.tests.test_maven` downloads data and has
mocked tests for the SDC URLs and credentials; CI runs it in
`.github/workflows/full_coverage.yml`. `tests/test_maven_uri.py` runs loads
against a local moto S3 server; its CI step there is commented out.
