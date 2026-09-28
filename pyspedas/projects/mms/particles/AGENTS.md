---
related_files:
  - pyspedas/projects/mms/AGENTS.md
  - pyspedas/projects/mms/particles/__init__.py
  - pyspedas/projects/mms/particles/mms_part_getspec.py
  - pyspedas/projects/mms/particles/mms_part_products.py
  - pyspedas/projects/mms/particles/mms_part_slice2d.py
  - pyspedas/projects/mms/particles/mms_convert_flux_units.py
  - pyspedas/projects/mms/particles/mms_pgs_clean_data.py
  - pyspedas/projects/mms/particles/mms_pgs_clean_support.py
  - pyspedas/projects/mms/particles/mms_pgs_make_e_spec.py
  - pyspedas/projects/mms/particles/mms_pgs_make_theta_spec.py
  - pyspedas/projects/mms/particles/mms_pgs_make_phi_spec.py
  - pyspedas/projects/mms/particles/mms_pgs_make_fac.py
  - pyspedas/projects/mms/particles/mms_pgs_split_hpca.py
  - pyspedas/projects/mms/particles/mms_part_des_photoelectrons.py
  - pyspedas/projects/mms/particles/moka_mms_clean_data.py
  - pyspedas/projects/mms/fpi_tools/mms_get_fpi_dist.py
  - pyspedas/projects/mms/fpi_tools/mms_pad_fpi.py
  - pyspedas/projects/mms/hpca_tools/mms_get_hpca_dist.py
  - pyspedas/particles/spd_part_products
  - pyspedas/particles/moments
  - pyspedas/particles/spd_slice2d
  - pyspedas/projects/mms/tests/test_mms_part_getspec.py
  - pyspedas/projects/mms/tests/test_mms_getspec_bulkv.py
  - pyspedas/projects/mms/tests/test_mms_slice2d.py
maintenance: |
  Update when mms_part_getspec() changes which support data it loads or their default
  variable names, when mms_part_products() gains or renames an output, or when the
  generic routines it calls in pyspedas/particles/ move.
---

# MMS particle distribution tools

Spectrograms, moments and 2D slices from MMS FPI and HPCA 3D distributions. These are the
MMS front ends to the generic particle code in `pyspedas/particles/`.

## Layout

- `mms_part_getspec.py`: `mms_part_getspec()`, the main entry point. Loads data and
  support data, then calls `mms_part_products()` for each probe.
- `mms_part_products.py`: the per-sample loop that builds spectra and moments.
- `mms_part_slice2d.py`: `mms_part_slice2d()`, loads data and calls `slice2d()` and
  `slice2d_plot()` from `pyspedas/particles/spd_slice2d/`.
- `mms_convert_flux_units.py`: converts distribution dicts between `flux`, `eflux`,
  `df_cm` and `df_km`.
- `mms_pgs_clean_data.py`, `mms_pgs_clean_support.py`: reshape a sample to energy x angle
  and compute `denergy`; interpolate B, bulk velocity and spacecraft potential to the
  distribution times.
- `mms_pgs_make_e_spec.py`, `mms_pgs_make_theta_spec.py`, `mms_pgs_make_phi_spec.py`,
  `mms_pgs_make_fac.py`: spectrum builders and field-aligned rotation matrices.
- `mms_pgs_split_hpca.py`: splits HPCA elevation bins so dphi equals dtheta.
- `mms_part_des_photoelectrons.py`: downloads the DES photoelectron model CDF from
  `https://lasp.colorado.edu/mms/sdc/public/data/models/fpi/`.
- `moka_mms_clean_data.py`: used by `pyspedas/projects/mms/fpi_tools/mms_pad_fpi.py`, not here.

## How `mms_part_getspec()` works

1. Loads the distributions with `time_clip=True`: `instrument='fpi'` calls
   `mms.fpi(datatype='d<species>s-dist')`; `'hpca'` calls `mms.hpca(datatype='ion')`,
   turns rate `fast` into `srvy`, species `i`/`e` into `hplus`, and forces
   `center_measurement=True`. With `subtract_bulk`, it also loads bulk velocity moments.
2. Loads support data over `trange` plus 60 s on each side: MEC, FGM and EDP `scpot`.
3. Default support names, overridable with `mag_name`, `pos_name`, `sc_pot_name`,
   `vel_name`: `mms<p>_fgm_b_gse_<rate>_l2_bvec`, `mms<p>_mec_r_gse`,
   `mms<p>_edp_scpot_<rate>_l2`, `mms<p>_d<s>s_bulkv_gse_<rate>`. The support `<rate>` is
   `brst` for burst data, else `srvy` (`fast` for EDP); `*_data_rate` keywords change it.
4. `mms_part_products()` takes `mms<p>_d<s>s_dist_<rate>` or
   `mms<p>_hpca_<species>_phase_space_density`. It gets one dict per sample from
   `mms_get_fpi_dist()` (`pyspedas/projects/mms/fpi_tools/mms_get_fpi_dist.py`) or
   `mms_get_hpca_dist()` (`pyspedas/projects/mms/hpca_tools/mms_get_hpca_dist.py`), subtracts the
   DES photoelectron model if needed, converts units, cleans, shifts by bulk velocity,
   limits ranges and builds the spectra. FAC outputs use `spd_pgs_do_fac` and
   `spd_pgs_regrid` from `pyspedas/particles/spd_part_products/`; moments use
   `spd_pgs_moments` from `pyspedas/particles/moments/`.

Outputs are named `<prefix><input name>_<output><suffix>`, e.g. `mms1_dis_dist_fast_energy`
or `mms1_des_dist_brst_pa`; moments get names like `mms1_dis_dist_fast_density`.

## Things to know

- Species: FPI `i` or `e`; HPCA `hplus`, `heplus`, `heplusplus`, `oplus`, `oplusplus`.
- Outputs: `energy`, `theta`, `phi`, `pa`, `gyro`, `moments`, `fac_energy`,
  `fac_moments`. Setting `pitch` or `gyro` limits swaps `energy` and `moments` for their
  FAC versions. `fac_type` defaults to `mphigeo`.
- Moments need `units='eflux'` (the default); nothing enforces it.
- For DES with `moments` requested, photoelectron correction is on unless
  `disable_photoelectron_corrections=True`. The model file is chosen from the stepper ID
  (`Energy_table_name` global attribute) of the loaded FPI variable.
- `sdc_units=True` reports the pressure tensor in nPa and heat flux in mW/m^2, like SDC files.
- `mms_part_getspec()` always reloads the distributions, MEC, FGM and EDP data, even when
  `mag_name` and the other names are given. To reuse loaded data, call
  `mms_part_products()` directly.

## Tests

`pyspedas/projects/mms/tests/test_mms_part_getspec.py`,
`pyspedas/projects/mms/tests/test_mms_getspec_bulkv.py` and
`pyspedas/projects/mms/tests/test_mms_slice2d.py` (all download data).
