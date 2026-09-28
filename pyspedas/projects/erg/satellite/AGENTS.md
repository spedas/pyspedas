---
related_files:
  - pyspedas/projects/erg/AGENTS.md
  - pyspedas/projects/erg/__init__.py
  - pyspedas/projects/erg/satellite/__init__.py
  - pyspedas/projects/erg/satellite/erg/load.py
  - pyspedas/projects/erg/satellite/erg/get_gatt_ror.py
  - pyspedas/projects/erg/satellite/erg/att/att.py
  - pyspedas/projects/erg/satellite/erg/mgf/mgf.py
  - pyspedas/projects/erg/satellite/erg/orb/orb.py
  - pyspedas/projects/erg/satellite/erg/orb/remove_duplicated_tframe.py
  - pyspedas/projects/erg/satellite/erg/hep/hep.py
  - pyspedas/projects/erg/satellite/erg/lepe/lepe.py
  - pyspedas/projects/erg/satellite/erg/lepi/lepi.py
  - pyspedas/projects/erg/satellite/erg/mepe/mepe.py
  - pyspedas/projects/erg/satellite/erg/mepi/mepi_nml.py
  - pyspedas/projects/erg/satellite/erg/mepi/mepi_tof.py
  - pyspedas/projects/erg/satellite/erg/xep/xep.py
  - pyspedas/projects/erg/satellite/erg/pwe/pwe_efd.py
  - pyspedas/projects/erg/satellite/erg/pwe/pwe_hfa.py
  - pyspedas/projects/erg/satellite/erg/pwe/pwe_ofa.py
  - pyspedas/projects/erg/satellite/erg/pwe/pwe_wfc.py
  - pyspedas/projects/erg/satellite/erg/common/cotrans/erg_cotrans.py
  - pyspedas/projects/erg/satellite/erg/common/cotrans/sga2sgi.py
  - pyspedas/projects/erg/satellite/erg/common/cotrans/sgi2dsi.py
  - pyspedas/projects/erg/satellite/erg/common/cotrans/dsi2j2000.py
  - pyspedas/projects/erg/satellite/erg/common/cotrans/erg_interpolate_att.py
  - pyspedas/projects/erg/satellite/erg/particle/erg_mep_part_products.py
  - pyspedas/projects/erg/satellite/erg/particle/erg_lep_part_products.py
  - pyspedas/projects/erg/satellite/erg/particle/erg_hep_part_products.py
  - pyspedas/projects/erg/satellite/erg/particle/erg_xep_part_products.py
  - pyspedas/projects/erg/satellite/erg/particle/erg_pgs_make_fac.py
  - pyspedas/particles/moments/spd_pgs_moments.py
  - pyspedas/particles/spd_part_products/spd_pgs_regrid.py
  - pyspedas/cotrans_tools/cotrans.py
  - pyspedas/projects/erg/tests/test_erg_mepe.py
maintenance: |
  Update when an instrument wrapper is added or renamed, when a wrapper changes how it
  handles notplot or builds its own variables, or when the cotrans chain or the support
  data it loads automatically changes.
---

# Arase satellite

Loaders, coordinate transforms and particle products for the Arase (ERG) spacecraft. All
code is under `erg/`; this folder level only holds that package.

## Layout

- `erg/load.py`: the shared `load()`, also used by the ground loaders.
- `erg/get_gatt_ror.py`: gets CDF global attributes for the rules-of-the-road printout.
- Instrument wrappers, one module each: `erg/att/att.py` (attitude, from text files),
  `erg/mgf/mgf.py` (magnetic field), `erg/orb/orb.py` (orbit), `erg/hep/hep.py`,
  `erg/lepe/lepe.py`, `erg/lepi/lepi.py`, `erg/mepe/mepe.py`, `erg/mepi/mepi_nml.py`,
  `erg/mepi/mepi_tof.py`, `erg/xep/xep.py` (particles), and `erg/pwe/pwe_efd.py`,
  `erg/pwe/pwe_hfa.py`, `erg/pwe/pwe_ofa.py`, `erg/pwe/pwe_wfc.py` (plasma waves).
- `erg/common/cotrans/`: `erg_cotrans()` and the steps it chains.
- `erg/particle/`: `erg_hep_part_products()`, `erg_lep_part_products()`,
  `erg_mep_part_products()`, `erg_xep_part_products()`, the `erg_<inst>_get_dist.py`
  converters, `erg_pgs_*` helpers, and `get_*_in_sga.py` detector look directions.
- All `__init__.py` files are empty; `pyspedas/projects/erg/__init__.py` exports the names.

## How a wrapper works

`mgf()` maps `datatype` aliases (`8s` to `8sec`, `64` to `64hz`), sets the prefix
`erg_mgf_<level>_`, builds the path template (daily files for `8sec`, hourly
`_<coord>_%Y%m%d%H_` files at 64/128/256 Hz), and calls `load()`. After the
rules-of-the-road printout it clips the -1e30 fill values and sets `ylim` and labels.

`hep()`, `lepe()` and `xep()` call `load()` with `notplot=True` for their
multi-dimensional products (2D/3D flux, omni flux, L3 pitch angle data) and then create the
tplot variables themselves with `store_data()`, using the CDF attributes that `load()`
attaches. They remember the caller's `notplot` in `initial_notplot_flag`. `orb()` also
removes duplicated time frames from position variables (`erg/orb/remove_duplicated_tframe.py`).

## Coordinate transforms

`erg_cotrans()` (`erg/common/cotrans/erg_cotrans.py`) converts between the spacecraft
frames SGA, SGI, DSI and J2000 by chaining `sga2sgi.py`, `sgi2dsi.py` and `dsi2j2000.py`.
Geophysical frames (GSE, GSM, SM, ...) are reached from J2000 with `cotrans()` in
`pyspedas/cotrans_tools/cotrans.py`.

- If `in_coord`/`out_coord` are not given, the frame is taken from the last `_`-part of
  the variable name (`..._dsi`), and multi-step conversions create intermediate
  variables named by replacing that suffix.
- `erg_interpolate_att.py` loads attitude data with `att()` when `erg_att_sprate` is
  missing or too short, and `dsi2j2000.py` loads `erg_orb_l2_pos_gse` with `orb()` for
  the Sun direction. `noload=True` stops both loads.

## Particle products

The `*_part_products` routines take the name of a loaded 3D flux variable, such as
`erg_mepe_l2_3dflux_FEDU` or `erg_xep_l2_FEDU_SSD`, and read the instrument from the second
`_`-part of the name, so renamed variables fail. They follow the same design as MMS
`mms_part_products()` but use their own `erg_pgs_*` helpers, borrowing only
`spd_pgs_moments()` and `spd_pgs_regrid()` from `pyspedas/particles/`. The outputs `pa`,
`gyro`, `fac_energy` and `fac_moments` need `mag_name` (MGF in DSI, e.g.
`erg_mgf_l2_mag_8sec_dsi`) and `pos_name` (e.g. `erg_orb_l2_pos_gse`), loaded beforehand;
`erg_pgs_make_fac.py` builds the rotation (`fac_type` defaults to `mphism`, `phigeo`
for HEP). See
`pyspedas/projects/erg/tests/test_erg_mepe.py` for a worked sequence.
