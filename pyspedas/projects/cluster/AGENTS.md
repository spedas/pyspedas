---
related_files:
  - pyspedas/projects/AGENTS.md
  - pyspedas/projects/cluster/__init__.py
  - pyspedas/projects/cluster/config.py
  - pyspedas/projects/cluster/load.py
  - pyspedas/projects/cluster/load_csa.py
  - pyspedas/projects/cluster/fgm.py
  - pyspedas/projects/cluster/aspoc.py
  - pyspedas/projects/cluster/cis.py
  - pyspedas/projects/cluster/dwp.py
  - pyspedas/projects/cluster/edi.py
  - pyspedas/projects/cluster/efw.py
  - pyspedas/projects/cluster/peace.py
  - pyspedas/projects/cluster/rapid.py
  - pyspedas/projects/cluster/staff.py
  - pyspedas/projects/cluster/wbd.py
  - pyspedas/projects/cluster/whi.py
  - pyspedas/projects/cluster/datasets.py
  - pyspedas/projects/cluster/particle_tools/cluster_get_codif_dist.py
  - pyspedas/projects/cluster/particle_tools/cluster_get_hia_dist.py
  - pyspedas/projects/cluster/README.md
  - pyspedas/projects/cluster/tests/test_cluster.py
  - pyspedas/projects/cluster/tests/test_cluster_uri.py
  - pyspedas/utilities/datasets.py
  - pyspedas/utilities/download.py
  - pyspedas/preferences.py
  - .github/workflows/full_coverage.yml
maintenance: |
  Update when load.py changes an instrument branch or the CIS distribution paths,
  when load_csa.py changes its CSA query or keywords, or when __init__.py adds a
  loader or particle tool.
---

# Cluster

Loaders for the four Cluster spacecraft. There are two routes: per-instrument
wrappers that read CDAWeb CDFs from SPDF, and `load_csa()`, which requests any
dataset from the ESA Cluster Science Archive (CSA).

## Layout

- `fgm.py`, `aspoc.py`, `cis.py`, `dwp.py`, `edi.py`, `efw.py`, `peace.py`,
  `rapid.py`, `staff.py`, `wbd.py`, `whi.py`: one wrapper per instrument, each
  calling `load()` in `load.py`.
- `load_csa.py`: `load_csa()`, the CSA route.
- `particle_tools/`: `cluster_get_codif_dist()` and `cluster_get_hia_dist()` turn
  loaded CIS 3D distributions into the list-of-dicts form used by
  `pyspedas.slice2d()` and the other particle routines.
- `datasets.py`: `datasets()`, lists Cluster datasets on CDAWeb through
  `find_datasets()` (`pyspedas/utilities/datasets.py`).
- `config.py`, `tests/`, `README.md` (user guide; its examples use the pre-2.0
  path `pyspedas.cluster`).

## How `load()` works

`load()` loops over `probe` (`'1'`-`'4'`, a string, int or list) and picks a
template from `CONFIG['remote_data_dir']` (SPDF), mostly
`c<probe>/<datatype>/<instr>/%Y/c<probe>_<datatype>_<instr>_%Y%m%d_v??.cdf`,
where `<instr>` is shortened for some instruments (`asp`, `pea`, `rap`, `sta`).
It then runs `dailynames()`, `download()` and one `cdf_to_tplot()` call for all
probes. Special cases:

- `fgm(datatype='cp')` reads the spin-resolution files
  (`c<probe>/cp/%Y/c<probe>_cp_fgm_spin_...`). The `fgm` default is `'up'`,
  `wbd`'s is `'waveform'`, and the rest default to `'pp'`.
- `cis(option=...)`: `'mom'` loads moments; `'psd_<species>'` or
  `'def_<species>'` (`h1`, `he1`, `o1` from CODIF, `ions` from HIA) loads 3D
  distributions from `c<probe>/cis-codif/...` or `c<probe>/cis-hia/...`.
- `wbd` files are 10-minute (`res=600`) and use a time wildcard, so they are
  downloaded without `last_version`; every other instrument passes
  `last_version=True` (`pyspedas/utilities/download.py`).

## How `load_csa()` works

It builds one CSA TAP query
(`https://csa.esac.esa.int/csa-sl-tap/data?retrieval_type=PRODUCT...`) for every
`<probe>_<datatype>` pair, downloads a `.tar.gz` into the local data folder,
extracts it there, deletes the archive and loads the CDFs. Its keywords differ:
`probes=['C1']` and `datatypes=['CP_FGM_SPIN']` use CSA names, `time_clip`
defaults to True, and there is no `no_update` or `force_download`; every call
downloads again. `probes=['*']` means all four.

## Things to know

- Variable names come from the CDFs and already carry the spacecraft and
  dataset (`B_vec_xyz_gse__C1_CP_FGM_SPIN`, `N_p__C1_PP_CIS`), so probes don't
  collide.
- The particle tools read the energy and angle axes from the distribution
  variable, so load it with `get_support_data=True`; `tests/test_cluster.py`
  shows the full slice2d workflow.
- The local data folder is `CLUSTER_DATA_DIR`, else `SPEDAS_DATA_DIR/cluster`,
  else `cluster_data/` (`config.py`, which first applies saved preferences from
  `pyspedas/preferences.py`); it may be an S3 or other fsspec URI. Setting
  `CLUSTER_NO_DOWNLOAD` turns downloads off for `load()`.

## Tests

`python -m pyspedas.projects.cluster.tests.test_cluster` downloads data.
`tests/test_cluster_uri.py` repeats loads against a local moto S3 server
(needs `moto[server]`). CI runs both in `.github/workflows/full_coverage.yml`.
