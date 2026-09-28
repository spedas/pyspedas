---
related_files:
  - pyspedas/projects/AGENTS.md
  - pyspedas/projects/kyoto/__init__.py
  - pyspedas/projects/kyoto/config.py
  - pyspedas/projects/kyoto/load_dst.py
  - pyspedas/projects/kyoto/load_ae.py
  - pyspedas/projects/kyoto/load_geomagnetic_indices.py
  - pyspedas/projects/kyoto/README.md
  - pyspedas/projects/kyoto/tests/test_kyoto.py
  - pyspedas/projects/themis/ground/gmag.py
  - pyspedas/projects/noaa/noaa_load_kp.py
  - pyspedas/projects/omni/load.py
  - pyspedas/utilities/download.py
  - .github/workflows/quick_tests.yml
maintenance: |
  Update when the Kyoto page layout or server paths change (parse_dst_html,
  parse_ae_html, the provisional/realtime date limits in load_ae.py), or when
  load_geomagnetic_indices() gains or drops a source.
---

# Kyoto geomagnetic indices

Loaders for the Dst and AE-family indices from the World Data Center for
Geomagnetism, Kyoto. The data are HTML and text pages, not CDF; the code here
parses them and stores the result with `store_data()`. There is no `load.py`.

## Layout

- `load_dst.py`: `dst()` and the page parser `parse_dst_html()`.
- `load_ae.py`: `load_ae()`, its worker `load_ae_worker()` and `parse_ae_html()`,
  for the AE, AL, AO, AU and AX indices.
- `load_geomagnetic_indices.py`: `load_geomagnetic_indices()`, loads indices from
  several sources in one call.
- `config.py`, `tests/test_kyoto.py`, `README.md`.

## How it works

- `dst()` expands `%Y%m/index.html` over the time range with `dailynames()`, then
  tries `dst_final/`, `dst_provisional/` and `dst_realtime/` in that order,
  downloading each monthly page with `download(..., text_only=True)`
  (`pyspedas/utilities/download.py`). It stops at the first type that yields
  data and stores `kyoto_dst`, naming the type in the `ytitle`. Values are
  stamped at half past each hour.
- `load_ae()` fetches daily files: provisional
  `ae_provisional/%Y%m/<index>%y%m%d.for.request` and realtime
  `ae_realtime/data_dir/%Y/%m/%d/<index>%y%m%d`. Ranges ending by 2021-01-01 use
  only provisional data, ranges starting on or after 2024-05-15 only realtime;
  in between both are fetched and provisional wins on days found in both. Each
  index becomes `kyoto_<index>` (`kyoto_ae`, `kyoto_al`, ...).
- `load_geomagnetic_indices(missions=..., datatypes=None)` loops over `kyoto`
  (`dst()` and `load_ae()`), `themis` (`gmag(sites='idx')`,
  `pyspedas/projects/themis/ground/gmag.py`), `noaa` and `gfz`
  (`noaa_load_kp()`, `pyspedas/projects/noaa/noaa_load_kp.py`, with `noaa_` or
  `gfz_` added to the prefix) and `omni` (`pyspedas/projects/omni/load.py`, with
  `omni_` added and a short variable list unless `omni_load_all=True`).

## Things to know

- `dst()` and `load_ae()` keywords differ from the CDF loaders: `download_only`
  instead of `downloadonly`, `no_download` instead of `no_update` (`None` means
  use `CONFIG['no_download']`), `local_data_dir` and `remote_data_dir`
  arguments, no `notplot` or `varnames`, and `time_clip` defaults to True (also
  in `load_geomagnetic_indices()`). `trange` is required.
- `dst()` has `http://wdc.kugi.kyoto-u.ac.jp/` as its `remote_data_dir` default,
  so `CONFIG['remote_data_dir_dst']` is used only when `''` is passed.
  `load_ae()` defaults to `''` and uses `CONFIG['remote_data_dir_ae']`.
- The earliest data are 1957-01-01 for Dst and 1996-01-01 for AE; earlier ranges
  log an error and return `[]`.
- Each call logs the WDC acknowledgement; the data are not for redistribution.
- The local data folder is `SPEDAS_DATA_DIR/geom_indices/kyoto/`, else
  `pydata/geom_indices/kyoto/` (`config.py`); there is no `KYOTO_DATA_DIR`.
  `KYOTO_NO_DOWNLOAD` turns downloads off. Local subfolders follow IDL SPEDAS:
  `dst_<type>/<yyyymm>/`, `ae_provisional/<index>/<yyyymm>/`,
  `ae_realtime/data_dir/<index>/<yyyy>/<mm>/<dd>/`.

## Tests

`python -m pyspedas.projects.kyoto.tests.test_kyoto` (downloads data, including
THEMIS, NOAA and OMNI for `load_geomagnetic_indices`). CI runs it in
`.github/workflows/quick_tests.yml`.
