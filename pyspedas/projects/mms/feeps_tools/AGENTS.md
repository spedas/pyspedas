---
related_files:
  - pyspedas/projects/mms/AGENTS.md
  - pyspedas/projects/mms/feeps_tools/feeps.py
  - pyspedas/projects/mms/feeps_tools/mms_feeps_correct_energies.py
  - pyspedas/projects/mms/feeps_tools/mms_feeps_energy_table.py
  - pyspedas/projects/mms/feeps_tools/mms_feeps_flat_field_corrections.py
  - pyspedas/projects/mms/feeps_tools/mms_feeps_remove_bad_data.py
  - pyspedas/projects/mms/feeps_tools/mms_feeps_active_eyes.py
  - pyspedas/projects/mms/feeps_tools/mms_feeps_split_integral_ch.py
  - pyspedas/projects/mms/feeps_tools/mms_feeps_remove_sun.py
  - pyspedas/projects/mms/feeps_tools/mms_read_feeps_sector_masks_csv.py
  - pyspedas/projects/mms/feeps_tools/mms_feeps_omni.py
  - pyspedas/projects/mms/feeps_tools/mms_feeps_spin_avg.py
  - pyspedas/projects/mms/feeps_tools/mms_feeps_pad.py
  - pyspedas/projects/mms/feeps_tools/mms_feeps_pad_spinavg.py
  - pyspedas/projects/mms/feeps_tools/mms_feeps_pitch_angles.py
  - pyspedas/projects/mms/feeps_tools/mms_feeps_gpd.py
  - pyspedas/projects/mms/feeps_tools/mms_feeps_getgyrophase.py
  - pyspedas/projects/mms/feeps_tools/sun
  - pyspedas/projects/mms/mms_load_data.py
  - pyspedas/projects/mms/tests/test_mms_feeps.py
maintenance: |
  Update when the correction chain in feeps.py changes order or gains a step, when a
  helper changes the variable-name suffix it writes, or when new sun-contamination CSV
  dates are added to sun/ and mms_read_feeps_sector_masks_csv.py.
---

# MMS FEEPS tools

Loader and post-processing for the Fly's Eye Energetic Particle Sensor (FEEPS), which
measures energetic electrons and ions on each MMS spacecraft. `mms_load_feeps()` loads the
CDFs and always runs a fixed correction chain; the pitch angle and gyrophase routines work
on its output.

## Layout

- `feeps.py`: `mms_load_feeps()`.
- `mms_feeps_correct_energies.py`, `mms_feeps_energy_table.py`: per-probe, per-eye energy
  tables; bad eyes get NaN energies.
- `mms_feeps_flat_field_corrections.py`: per-eye gain factors (mostly the ion eyes).
- `mms_feeps_remove_bad_data.py`: NaNs bad eyes and bad low-energy channels from dated tables.
- `mms_feeps_active_eyes.py`: which sensor IDs are active for a date, probe, rate, species, level.
- `mms_feeps_split_integral_ch.py`: removes the top (integral) channel into `_500keV_int`.
- `mms_feeps_remove_sun.py`, `mms_read_feeps_sector_masks_csv.py`, `sun/`: NaNs
  sun-contaminated spin sectors using `MMS<n>_FEEPS_ContaminatedSectors_<YYYYMMDD>.csv`.
- `mms_feeps_omni.py`, `mms_feeps_spin_avg.py`: omni-directional spectra and spin averages.
- `mms_feeps_pad.py`, `mms_feeps_pad_spinavg.py`, `mms_feeps_pitch_angles.py`: pitch
  angle distributions (PADs).
- `mms_feeps_gpd.py`, `mms_feeps_getgyrophase.py`: gyrophase distributions.

## How `mms_load_feeps()` works

It calls `mms_load_data(instrument='feeps')` (`pyspedas/projects/mms/mms_load_data.py`), then:
`mms_feeps_correct_energies()` and `mms_feeps_flat_field_corrections()` on all probes;
`mms_feeps_remove_bad_data()` per probe, level, rate and datatype; then per unit
`mms_feeps_active_eyes()`, `mms_feeps_split_integral_ch()`, `mms_feeps_remove_sun()`,
`mms_feeps_omni()` and `mms_feeps_spin_avg()`. Each step reads the previous step's
variables by name, so the chain builds up suffixes on
`mms<p>_epd_feeps_<rate>_<level>_<species>_<top|bottom>_<units>_sensorid_<n>`:
`_clean` (integral channel removed), then `_clean_sun_removed`. Omni spectra are
`..._<species>_<units>_omni`, spin averages `..._omni_spin`.

`mms_feeps_pad()` runs on already-loaded data and writes
`..._<units>_<E0>-<E1>keV_pad` plus a `_spin` average. For burst data it reads the CDF's
`_pitch_angle` variable; otherwise (or with `angles_from_bfield=True`)
`mms_feeps_pitch_angles()` loads FGM `b_bcs` data and computes angles per telescope.
`mms_feeps_gpd()` loads FEEPS itself, and `mms_feeps_getgyrophase()` loads MEC
quaternions and survey FGM.

## Things to know

- Sensor IDs 1-12 exist on a top and a bottom head; IDs 6-8 are ion eyes, the rest electron.
  Which eyes are active changed on 2017-08-16 for survey data, and SITL uses top eyes only.
- With no version keyword, the loader sets `major_version=True` because the SDC mixes
  incompatible major CDF versions. It also filters "record-varying" warnings from the
  `pyspedas` logger (`filter_recvary_warnings`).
- The sun mask CSV nearest in time to `trange[0]` is used for all four probes. A new mask
  set needs both the CSV files in `sun/` and a new entry in the `dates` list of
  `mms_read_feeps_sector_masks_csv.py`.
- `mms_feeps_pad()` refuses energies below 32 keV and uses an angular response of
  21.4 deg for electrons, 10 deg for ions.
- `quality_flag` in `mms_feeps_omni()` selects eyes by sun-contamination quality;
  `get_err=True` needs L1b counts, which are team-only.
- Units are `intensity` (1/(cm^2 sr s keV)) and `count_rate`.

## Tests

`pyspedas/projects/mms/tests/test_mms_feeps.py` (downloads data).
