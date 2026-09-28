---
related_files:
  - pyspedas/projects/mms/AGENTS.md
  - pyspedas/projects/mms/fpi_tools/fpi.py
  - pyspedas/projects/mms/fpi_tools/mms_fpi_set_metadata.py
  - pyspedas/projects/mms/fpi_tools/mms_load_fpi_calc_pad.py
  - pyspedas/projects/mms/fpi_tools/mms_fpi_make_errorflagbars.py
  - pyspedas/projects/mms/fpi_tools/mms_fpi_make_compressionlossbars.py
  - pyspedas/projects/mms/fpi_tools/mms_get_fpi_dist.py
  - pyspedas/projects/mms/fpi_tools/mms_pad_fpi.py
  - pyspedas/projects/mms/fpi_tools/mms_fpi_ang_ang.py
  - pyspedas/projects/mms/fpi_tools/mms_fpi_split_tensor.py
  - pyspedas/projects/mms/mms_load_data.py
  - pyspedas/projects/mms/particles/mms_part_products.py
  - pyspedas/projects/mms/particles/mms_part_slice2d.py
  - pyspedas/projects/mms/particles/moka_mms_clean_data.py
  - pyspedas/projects/mms/particles/mms_part_des_photoelectrons.py
  - pyspedas/particles/spd_slice2d
  - pyspedas/projects/mms/tests/test_mms_fpi.py
maintenance: |
  Update when mms_load_fpi() changes its datatype defaults or the errorflags renaming, or
  when mms_get_fpi_dist() changes the layout, units or angle convention of the
  distribution dicts it returns.
---

# MMS FPI tools

Loader and helpers for the Fast Plasma Investigation: DES (electrons) and DIS (ions)
moments, 3D distributions, and quantities derived from them.

## Layout

- `fpi.py`: `mms_load_fpi()`.
- `mms_fpi_set_metadata.py`: plot options for the loaded variables.
- `mms_fpi_make_errorflagbars.py`, `mms_fpi_make_compressionlossbars.py`: turn the
  `errorflags` and `compressionloss` variables into flag-bar variables for plots.
- `mms_load_fpi_calc_pad.py`: summed and averaged omni pitch angle spectra from the
  low/mid/high energy `pitchAngDist` variables (does nothing if they weren't loaded).
- `mms_get_fpi_dist.py`: converts a loaded `mms<p>_d<s>s_dist_<rate>` variable into a list
  of 3D particle dicts, one per time sample, for the particle code.
- `mms_pad_fpi.py`: pitch angle and energy spectra (omni, para, perp, anti-para) at one
  time or averaged over an interval, from those dicts.
- `mms_fpi_ang_ang.py`: angle-angle and angle-energy plots at one time; loads FPI and FGM itself.
- `mms_fpi_split_tensor.py`: splits a 3x3 tensor variable into `_xx` ... `_zz` variables.

## How `mms_load_fpi()` works

1. `datatype='*'` expands to all eight L2 types: `des-dist`, `dis-dist`, `des-moms`,
   `dis-moms`, `des-momsaux`, `dis-momsaux`, `des-partmoms`, `dis-partmoms`. For survey
   `level='ql'` it becomes `des`, `dis`; for `sitl` and `trig` it is empty.
2. Without `varformat` or `varnames`, `get_support_data` is forced on.
3. `mms_load_data(instrument='fpi')` (`pyspedas/projects/mms/mms_load_data.py`) loads the
   files, then `mms_fpi_set_metadata()` runs.
4. Moments and distribution files both contain `mms<p>_d<s>s_errorflags_<rate>` and
   `..._compressionloss_<rate>`, so one would overwrite the other. When both `-dist` and
   `-moms` are requested, these are deleted and reloaded with `_dist` and `_moms`
   suffixes; otherwise the loaded one is renamed with the matching suffix.
5. For each probe, rate, datatype and level: `mms_load_fpi_calc_pad()`, error flag bars
   for moms and dist, and compression loss bars for burst data.

## Things to know

- Names are `mms<p>_d<e|i>s_<quantity>_<rate>` with no level: `mms1_dis_bulkv_gse_fast`,
  `mms1_des_dist_brst`, `mms1_dis_temptensor_gse_brst`. Rates are `fast` and `brst`.
- `mms_get_fpi_dist()` returns dicts in `df_cm` units (s^3/cm^6) with arrays ordered
  [energy, phi, theta] per sample. It converts the CDF's look directions to flow
  directions: theta from colatitude to latitude and negated, phi + 180 deg. Mass is in
  eV/(km/s)^2. `start_time` is the time tag and `end_time` adds the integration time
  (4.5 s fast; 0.03 s DES, 0.15 s DIS burst), so it assumes uncentered time tags.
- Users of `mms_get_fpi_dist()`: `pyspedas/projects/mms/particles/mms_part_products.py`,
  `pyspedas/projects/mms/particles/mms_part_slice2d.py`, `mms_pad_fpi()` and `mms_fpi_ang_ang()`.
- `mms_pad_fpi()` borrows `slice2d` helpers from `pyspedas/particles/spd_slice2d/` and
  cleans data with `pyspedas/projects/mms/particles/moka_mms_clean_data.py`.
- The DES photoelectron model used for electron moments is loaded by
  `pyspedas/projects/mms/particles/mms_part_des_photoelectrons.py`, not here.
- `center_measurement=True` is passed to `cdf_to_tplot()` and moves time tags to the
  middle of each accumulation interval.

## Tests

`pyspedas/projects/mms/tests/test_mms_fpi.py` (downloads data).
