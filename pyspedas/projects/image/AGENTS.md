---
related_files:
  - pyspedas/projects/AGENTS.md
  - pyspedas/projects/image/__init__.py
  - pyspedas/projects/image/config.py
  - pyspedas/projects/image/load.py
  - pyspedas/projects/image/lena.py
  - pyspedas/projects/image/mena.py
  - pyspedas/projects/image/hena.py
  - pyspedas/projects/image/rpi.py
  - pyspedas/projects/image/euv.py
  - pyspedas/projects/image/fuv.py
  - pyspedas/projects/image/orbit.py
  - pyspedas/projects/image/datasets.py
  - pyspedas/projects/image/README.md
  - pyspedas/projects/image/tests/test_image.py
  - pyspedas/utilities/datasets.py
  - .github/workflows/full_coverage.yml
maintenance: |
  Update when load.py gains or changes an instrument branch or keyword, or when
  a wrapper is added to __init__.py.
---

# IMAGE

Loaders for the IMAGE magnetospheric imaging mission (neutral atom imagers,
radio sounder, EUV and FUV imagers) and its orbit files. All data are CDF files
from SPDF.

## Layout

- `lena.py`, `mena.py`, `hena.py`, `rpi.py`, `euv.py`, `fuv.py`, `orbit.py`: one
  wrapper per instrument, each calling `load()`.
- `load.py`: `load()`, the file-path chain and loading for all instruments.
- `datasets.py`: `datasets()`, lists IMAGE datasets on CDAWeb through
  `find_datasets()` (`pyspedas/utilities/datasets.py`).
- `config.py`, `tests/test_image.py`, `README.md` (user guide).

## How it works

Each wrapper calls `load(instrument=...)`, which picks a path template under
`CONFIG['remote_data_dir']` (`https://spdf.gsfc.nasa.gov/pub/data/image/`) and
runs the usual `dailynames()`, `download()`, `cdf_to_tplot()` pipeline. The
instrument templates are all
`<instrument>/<instrument>_<datatype>/%Y/im_<datatype>_<instrument>_%Y%m%d_v??.cdf`
with two exceptions:

- `fuv` loads only the WIC camera: `fuv/wic_<datatype>/%Y/im_<datatype>_wic_...`.
- `orbit` takes `datatype='def_or'` (default) or `'pre_or'`, mapped to
  `orbit/<datatype>/%Y/im_or_def_...` or `im_or_pre_...`.

Every instrument wrapper defaults to `datatype='k0'` (key parameters).

## Things to know

- Variable names come straight from the CDF with no instrument prefix
  (`WIC_PIXELS`, `GSM_POS`); both orbit datatypes create the same names.
- `time_clip` defaults to False in the wrappers and in `load()`.
- The local data folder is `IMAGE_DATA_DIR`, else `SPEDAS_DATA_DIR/image`, else
  `image_data/` (`config.py`). Setting `IMAGE_NO_DOWNLOAD` turns downloads off.

## Tests

`python -m pyspedas.projects.image.tests.test_image`. CI runs it in
`.github/workflows/full_coverage.yml`.
