# Quick-test inventory

This file is the inventory for the manually selected tests in
`.github/workflows/quick_tests.yml`.

- Active tests: 68
- Commented tests: 2
- Total listed test entries: 70

The commented entries are included so that any future split or cleanup can be
checked against the complete list in the workflow. They are not currently
executed.

| Inventory ID | Status | Test module |
|---:|---|---|
| 1 | Active | `pyspedas.utilities.tests.test_find_ip_address` |
| 2 | Active | `pyspedas.hapi_tools.tests.test_hapi_testdata` |
| 3 | Commented; future `missions-non-spdf` | `pyspedas.projects.galileo.tests.test_galileo` |
| 4 | Commented; future `missions-non-spdf` | `pyspedas.projects.juno.tests.test_juno` |
| 5 | Active | `pyspedas.utilities.tests.test_doi` |
| 6 | Active | `pyspedas.utilities.tests.test_zenodo_draft` |
| 7 | Active | `pyspedas.projects.ace.tests.test_ace` |
| 8 | Active | `pyspedas.projects.themis.tests.test_themis_tplot_time` |
| 9 | Active | `pyspedas.projects.themis.tests.test_themis_versions` |
| 10 | Active | `pyspedas.projects.barrel.tests.test_barrel` |
| 11 | Active | `pyspedas.projects.soho.tests.test_soho` |
| 12 | Active | `pyspedas.projects.de2.tests.test_de2` |
| 13 | Active | `pyspedas.projects.st5.tests.test_st5` |
| 14 | Active | `pyspedas.projects.lanl.tests.test_lanl` |
| 15 | Active | `pyspedas.cotrans_tools.tests.test_quaternions` |
| 16 | Active | `pyspedas.projects.cnofs.tests.test_cnofs` |
| 17 | Active | `pyspedas.projects.dmsp.tests.test_dmsp` |
| 18 | Active | `pyspedas.projects.swfo.tests.test_swfo` |
| 19 | Active | `pyspedas.projects.dscovr.tests.test_dscovr` |
| 20 | Active | `pyspedas.utilities.tests.test_utilities_download` |
| 21 | Active | `pyspedas.utilities.tests.test_utilities_misc` |
| 22 | Active | `pyspedas.utilities.tests.test_preferences` |
| 23 | Active | `pyspedas.utilities.tests.test_utilities_download_uri` |
| 24 | Active | `pyspedas.utilities.tests.test_xdegap` |
| 25 | Active | `pyspedas.utilities.tests.test_math` |
| 26 | Active | `pyspedas.utilities.tests.test_interp_nan` |
| 27 | Active | `pyspedas.utilities.tests.test_utilities_tplot_wildcard` |
| 28 | Active | `pyspedas.utilities.tests.test_utilities_plot` |
| 29 | Active | `pyspedas.tplot_tools.MPLPlotter.plot_tests.test_wrap_label` |
| 30 | Active | `pyspedas.tplot_tools.MPLPlotter.plot_tests.test_fill_between` |
| 31 | Active | `pyspedas.tplot_tools.MPLPlotter.plot_tests.test_grid_background_options` |
| 32 | Active | `pyspedas.utilities.tests.test_utilities_tplotxy` |
| 33 | Active | `pyspedas.utilities.tests.test_tplotxy_ranges` |
| 34 | Active | `pyspedas.utilities.tests.test_utilities_time` |
| 35 | Active | `pyspedas.utilities.tests.test_utilities_libs` |
| 36 | Active | `pyspedas.cotrans_tools.tests.test_cotrans` |
| 37 | Active | `pyspedas.cotrans_tools.tests.test_minvar` |
| 38 | Active | `pyspedas.cotrans_tools.tests.test_fac` |
| 39 | Active | `pyspedas.cotrans_tools.tests.test_lmn` |
| 40 | Active | `pyspedas.projects.csswe.tests.test_csswe` |
| 41 | Active | `pyspedas.projects.equator_s.tests.test_equator_s` |
| 42 | Active | `pyspedas.projects.image.tests.test_image` |
| 43 | Active | `pyspedas.projects.psp.tests.test_psp` |
| 44 | Active | `pyspedas.projects.rbsp.tests.test_rbsp` |
| 45 | Active | `pyspedas.projects.stereo.tests.test_stereo` |
| 46 | Active | `pyspedas.projects.twins.tests.test_twins` |
| 47 | Active | `pyspedas.projects.wind.tests.test_wind` |
| 48 | Active | `pyspedas.projects.polar.tests.test_polar` |
| 49 | Active | `pyspedas.projects.geotail.tests.test_geotail` |
| 50 | Active | `pyspedas.analysis.tests.test_analysis` |
| 51 | Active | `pyspedas.utilities.tests.test_tinterpol_mxn` |
| 52 | Active | `pyspedas.utilities.tests.test_interpolate_rotation` |
| 53 | Active | `pyspedas.analysis.tests.test_twavpol` |
| 54 | Active | `pyspedas.analysis.tests.test_wavelet` |
| 55 | Active | `pyspedas.projects.fast.tests.test_fast` |
| 56 | Active | `pyspedas.projects.omni.tests.test_omni` |
| 57 | Active | `pyspedas.projects.themis.tests.test_themis` |
| 58 | Active | `pyspedas.projects.themis.tests.test_themis_s3` |
| 59 | Active | `pyspedas.projects.ulysses.tests.test_ulysses` |
| 60 | Active | `pyspedas.projects.solo.tests.test_solo` |
| 61 | Active | `pyspedas.projects.kyoto.tests.test_kyoto` |
| 62 | Active | `pyspedas.projects.swarm.tests.test_swarm` |
| 63 | Active | `pyspedas.projects.themis.tests.test_themis_check_args` |
| 64 | Active | `pyspedas.projects.themis.tests.test_themis_autoload_support` |
| 65 | Active | `pyspedas.projects.themis.tests.test_themis_cal_fit` |
| 66 | Active | `pyspedas.projects.themis.tests.test_themis_dsl_cotrans` |
| 67 | Active | `pyspedas.projects.themis.tests.test_themis_lunar_cotrans` |
| 68 | Active | `pyspedas.projects.themis.tests.test_themis_spinmodel` |
| 69 | Active | `pyspedas.projects.themis.tests.test_themis_state` |
| 70 | Active | `pyspedas.projects.themis.tests.test_themis_scpot2dens` |

## Validation rule

Any future split of the quick tests must account for every row in this table.
Every active module must appear exactly once in `quick_tests.yml`, and no active
workflow module may be missing from this inventory. The two commented rows
should remain marked as commented unless they are explicitly re-enabled in
`quick_tests.yml`.

## Logical test groups

The active tests are organized by subsystem or documented data-source
boundary. The inventory IDs below refer to the table above.

| Group | Purpose | Inventory entries | Count |
|---|---|---|---:|
| `utilities` | Shared utilities, downloads, preferences, and interpolation helpers | 1, 5, 6, 20-26, 34, 35, 51, 52 | 14 |
| `tplot` | tplot wildcard, plotting, and tplot-XY behavior | 27-33 | 7 |
| `cotrans` | Coordinate transformation routines | 15, 36-39 | 5 |
| `analysis` | General analysis, wave polarization, and wavelet routines | 50, 53-54 | 3 |
| `hapi` | Direct HAPI client coverage | 2 | 1 |
| `themis` | THEMIS/ARTEMIS loader and THEMIS-specific functionality | 8-9, 57, 63-70 | 11 |
| `themis-s3` | THEMIS loader coverage using the S3-backed test module | 58 | 1 |
| `psp` | Parker Solar Probe mission loader coverage | 43 | 1 |
| `rbsp` | Radiation Belt Storm Probes mission loader coverage | 44 | 1 |
| `missions-spdf` | Mission loaders documented as using SPDF, excluding separately grouped PSP and RBSP coverage | 7, 10-14, 16-17, 19, 40-42, 46-49, 55-56, 59-60 | 20 |
| `missions-non-spdf` | Mission loaders using non-SPDF sources | 18, 45, 61-62 | 4 |

Total active tests assigned: **68**.

The mission groups follow the source descriptions in
`pyspedas/projects/AGENTS.md`. In particular, SWFO uses the NOAA NCEI
S3-compatible archive, STEREO uses a Berkeley mirror, Kyoto uses WDC indices,
Swarm uses the VirES HAPI server, and Galileo and Juno use Iowa DAS2 servers.
HAPI remains a separate group because `test_hapi_testdata` directly tests the
shared HAPI client rather than a mission loader.
