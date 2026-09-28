---
related_files:
  - AGENTS.md
  - pyspedas/utilities/download.py
  - pyspedas/utilities/download_ftp.py
  - pyspedas/utilities/dailynames.py
  - pyspedas/utilities/datasets.py
  - pyspedas/utilities/pyspedas_functools.py
  - pyspedas/utilities/time_interpolate.py
  - pyspedas/utilities/interpolate_rotation.py
  - pyspedas/utilities/tinterpol_mxn.py
  - pyspedas/utilities/interpol.py
  - pyspedas/utilities/xdegap.py
  - pyspedas/utilities/tcopy.py
  - pyspedas/utilities/leap_seconds.py
  - pyspedas/utilities/unix2tai.py
  - pyspedas/utilities/tai2unix.py
  - pyspedas/utilities/month_intervals.py
  - pyspedas/utilities/is_timezone_aware.py
  - pyspedas/utilities/spice/time_ephemeris.py
  - pyspedas/utilities/mpause_2.py
  - pyspedas/utilities/mpause_t96.py
  - pyspedas/utilities/bshock_2.py
  - pyspedas/utilities/libs.py
  - pyspedas/utilities/doi.py
  - pyspedas/utilities/is_gzip.py
  - pyspedas/utilities/find_ip_address.py
  - pyspedas/utilities/rate_connection_quality.py
  - pyspedas/utilities/config_testing.py
  - pyspedas/utilities/zenodo_draft.py
  - pyspedas/utilities/das2/README.md
  - pyspedas/utilities/tests
  - pyspedas/__init__.py
  - pyspedas/config.py
  - pyspedas/tplot_tools/time_double.py
  - pyspedas/tplot_tools/time_string.py
  - .github/workflows/quick_tests.yml
  - .github/workflows/zenodo_draft.yml
maintenance: |
  Update when download() or dailynames() change their matching, caching or
  fallback behavior, when a helper is added here or re-exported from
  pyspedas/__init__.py, or when tests for other folders move in or out of tests/.
---

# utilities

Shared helpers: downloading and file-name generation for the mission loaders,
interpolation, time-scale conversions, magnetopause and bow shock models, and
maintenance scripts. Most public names are re-exported from `pyspedas/__init__.py`.

## Layout

- `download.py`: `download()` (the loaders' fetcher), `download_file()`, `check_downloaded_file()`, retrying `requests` session; `download_ftp.py`: FTP.
- `dailynames.py`: `dailynames()` and `yearlynames()` expand a path template over a time range.
- `datasets.py`: `find_datasets()` lists CDAWeb dataset IDs through `cdasws`.
- `pyspedas_functools.py`: `better_partial()`, used by missions to define instrument loaders.
- `time_interpolate.py`: `time_interpolate()`, IDL-style component-wise interpolation (`tinterpol_mxn.py` is an alias under the IDL name); `interpolate_rotation.py`: interpolation of rotation matrices; `interpol.py`, `xdegap.py`: array helpers.
- `tcopy.py`: deep copy of variables with wildcards.
- `leap_seconds.py`, `unix2tai.py`, `tai2unix.py`: TAI conversions; `spice/time_ephemeris.py`: Unix to ephemeris time; `month_intervals.py`; `is_timezone_aware.py`.
- `mpause_2.py`, `mpause_t96.py`, `bshock_2.py`: magnetopause and bow shock models.
- `das2/`: das2 server client used by the Galileo and Juno loaders (see `das2/README.md`).
- `libs.py`: `libs('name')` searches pyspedas for functions by name; `doi.py`: `get_doi()`.
- `config_testing.py`: `test_data_download_file()` for validation files in tests.
- `zenodo_draft.py`, `rate_connection_quality.py`, `find_ip_address.py`, `is_gzip.py`: CI and troubleshooting helpers.
- `tests/`: tests for this folder and for much of `pyspedas/tplot_tools`.

## How download() works

1. Each URL is `remote_path + remote_file`; the local file is `local_path` plus the same
   relative path unless `local_file` is given.
2. A `*`, `?` (fnmatch) or `regex=True` in the file name fetches the parent directory's HTML
   index, parses the links, and keeps the matches. Index results are cached per call, and a
   failing index is skipped for the rest of the call. `last_version=True` keeps only the
   lexically last match; otherwise every matching version is fetched.
3. `download_file()` sends `If-Modified-Since` for an existing local file, writes to a
   temporary file, checks it with `check_downloaded_file()` (CDF and netCDF files are opened),
   then copies it into place; a bad download is retried once.
4. If nothing was downloaded (including `no_download=True`), it walks `local_path` for files
   whose name matches the pattern. This is how `no_update` and offline use work.
5. fsspec URIs (for example `s3://`) are streamed in place instead of downloaded;
   `CONFIG['s3']['use_anon_access']` (`pyspedas/config.py`) controls anonymous S3 access.

## Things to know

- `dailynames(file_format=..., trange=..., res=...)` treats `file_format` as a whole relative
  path with strftime codes and returns one name per `res` step (daily by default), with duplicates
  removed. Wildcards in it pass through to `download()`.
- The general time helpers `time_double`, `time_string` and `time_datetime` are in
  `pyspedas/tplot_tools/time_double.py` and `pyspedas/tplot_tools/time_string.py`, not here.
- `load_leap_table()` reads `CDFLeapSeconds.txt` from `CDF_LEAPSECONDSTABLE`, else
  `SPEDAS_DATA_DIR`, and downloads it from the CDF site when missing.
- `download()` sets a `pySPEDAS <version>` User-Agent and uses digest auth when `username` is
  given (`basic_auth=True` for basic auth).

## Tests

`tests/` runs in CI (`.github/workflows/quick_tests.yml`). Besides download and time tests it
holds the tplot math, wildcard and plotting tests. `zenodo_draft.py` is run by
`.github/workflows/zenodo_draft.yml`.
