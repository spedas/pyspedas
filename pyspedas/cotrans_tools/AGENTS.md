---
related_files:
  - AGENTS.md
  - pyspedas/cotrans_tools/cotrans.py
  - pyspedas/cotrans_tools/cotrans_lib.py
  - pyspedas/cotrans_tools/igrf.py
  - pyspedas/cotrans_tools/j2000.py
  - pyspedas/cotrans_tools/matrix_array_lib.py
  - pyspedas/cotrans_tools/quaternions.py
  - pyspedas/cotrans_tools/tvector_rotate.py
  - pyspedas/cotrans_tools/fac_matrix_make.py
  - pyspedas/cotrans_tools/lmn_matrix_make.py
  - pyspedas/cotrans_tools/minvar_matrix_make.py
  - pyspedas/cotrans_tools/minvar.py
  - pyspedas/cotrans_tools/gsm2lmn.py
  - pyspedas/cotrans_tools/rotmat_get_coords.py
  - pyspedas/cotrans_tools/rotmat_set_coords.py
  - pyspedas/cotrans_tools/cart2spc.py
  - pyspedas/cotrans_tools/spc2cart.py
  - pyspedas/cotrans_tools/cart_to_sphere.py
  - pyspedas/cotrans_tools/sphere_to_cart.py
  - pyspedas/cotrans_tools/xyz_to_polar.py
  - pyspedas/cotrans_tools/sm2mlt.py
  - pyspedas/cotrans_tools/tests
  - pyspedas/__init__.py
  - pyspedas/tplot_tools/data_att_getters_setters.py
  - pyspedas/projects/omni/omni_solarwind_load.py
  - pyspedas/projects/themis/cotrans
  - pyspedas/projects/mms/cotrans
  - pyspedas/projects/erg/satellite/erg/common/cotrans/erg_cotrans.py
  - pyspedas/particles/spd_slice2d/quaternions.py
  - pyspedas/geopack/igrf.py
maintenance: |
  Update when a coordinate system or a sub<a>2<b> transform is added to
  cotrans_lib.py (and its path table), when cotrans() changes its metadata
  handling, or when a new rotation-matrix maker is added here.
---

# cotrans_tools

Geophysical coordinate transforms and rotation-matrix tools, ported from IDL SPEDAS.
`cotrans()` converts vectors between GSE, GSEQ, GSM, SM, GEI, GEO, MAG, J2000, HEE, HAE
and HEEQ; the other modules build and apply rotation matrices (FAC, LMN, minimum variance).
Public names are re-exported from `pyspedas/__init__.py`.

## Layout

- `cotrans.py`: `cotrans()`, the entry point for tplot variables or arrays.
- `cotrans_lib.py`: `subcotrans()`, the path search, and one `sub<a>2<b>()` function per transform edge.
- `igrf.py`: IGRF coefficient table for the dipole direction (`cdipdir`); `j2000.py`: nutation table for GEI to J2000.
- `tvector_rotate.py`: apply a matrix variable to vector variables, interpolating matrices with `qslerp`.
- `fac_matrix_make.py`, `lmn_matrix_make.py`, `minvar_matrix_make.py`: build matrix variables; `minvar.py` and `gsm2lmn.py` are the array-level math.
- `rotmat_set_coords.py`, `rotmat_get_coords.py`: record a matrix variable's input and output systems.
- `quaternions.py`: quaternion library (`qslerp`, `mtoq`, `qtom`, ...); `matrix_array_lib.py`: batch 3x3 matrix checks (`ctv_verify_mats`, `ctv_swap_hands`).
- `cart2spc.py`, `spc2cart.py`, `cart_to_sphere.py`, `sphere_to_cart.py`, `xyz_to_polar.py`, `sm2mlt.py`: small conversions.
- `tests/`: unittest modules.

## How cotrans() works

1. The input system is `coord_in`, else the variable's `data_att['coord_sys']` via
   `get_coords()` (`pyspedas/tplot_tools/data_att_getters_setters.py`). If both are given and
   differ, it logs an error and returns 0.
2. Data must be N x 3 (or N x M x 3 for field-line traces, handled trace by trace).
3. `subcotrans()` finds a chain of systems with `find_path_t1_t2()` over the edge table in
   `get_all_paths_t1_t2()`, shortens it, and calls each step by name:
   `globals()['sub' + c1 + '2' + c2]`. GSE and GEI are the hubs; SM, MAG, J2000 and the
   heliocentric systems each connect through one neighbor.
4. With `name_in`, the result goes to `name_out` (default `<name_in>_<coord_out>`) via
   `tplot_copy()`, and `set_coords()` records the new system, also editing legends and the
   y title that contain the old one. Without names, the array is returned.

## Things to know

- A new transform needs both the `sub<a>2<b>` function and an entry in `get_all_paths_t1_t2()`;
  the function is only found by its name string.
- Times are Unix seconds (floats). Geophysical steps rotate only, so units don't matter. The
  HEE, HAE and HEEQ steps use astropy's built-in ephemeris and add the Earth-Sun offset only when
  `position=True` (data in km). For variables the default is `data_att['st_type'] == 'pos'`,
  which pySPEDAS loaders don't set (IDL `.tplot` files restored with `tplot_restore()` can carry
  it), so pass `position=True` for positions.
- Matrix variables store `input_coord_sys` and `output_coord_sys` in `data_att`;
  `tvector_rotate()` checks them against the vectors' `coord_sys` and sets the output system.
- `lmn_matrix_make()` downloads OMNI solar wind data
  (`pyspedas/projects/omni/omni_solarwind_load.py`) for the Shue et al. magnetopause model.
- Mission systems live with the missions: `pyspedas/projects/themis/cotrans` (DSL, SSL, SSE,
  SEL), `pyspedas/projects/mms/cotrans` (quaternion-based), and
  `pyspedas/projects/erg/satellite/erg/common/cotrans/erg_cotrans.py`.
- Duplicate names: `pyspedas/particles/spd_slice2d/quaternions.py` has its own `qtom` and
  `qcompose`; `pyspedas/geopack/igrf.py` is the IGRF field model, unrelated to `igrf.py` here.
