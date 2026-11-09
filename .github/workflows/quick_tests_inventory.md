# Quick-test inventory

This file is the inventory for the manually selected tests in
`.github/workflows/quick_tests.yml`.

- Active tests: 68
- Commented tests: 2
- Total listed test entries: 70

The commented entries are included so that any future split or cleanup can be
checked against the complete list in the workflow.

| # | Status | Test module | Original workflow line |
|---:|---|---|---:|
| 1 | Active | `pyspedas.utilities.tests.test_find_ip_address` | 165 |
| 2 | Active | `pyspedas.hapi_tools.tests.test_hapi_testdata` | 167 |
| 3 | Commented; future `missions-non-spdf` | `pyspedas.projects.galileo.tests.test_galileo` | 170 |
| 4 | Commented; future `missions-non-spdf` | `pyspedas.projects.juno.tests.test_juno` | 172 |
| 5 | Active | `pyspedas.utilities.tests.test_doi` | 174 |
| 6 | Active | `pyspedas.utilities.tests.test_zenodo_draft` | 176 |
| 7 | Active | `pyspedas.projects.ace.tests.test_ace` | 178 |
| 8 | Active | `pyspedas.projects.themis.tests.test_themis_tplot_time` | 180 |
| 9 | Active | `pyspedas.projects.themis.tests.test_themis_versions` | 182 |
| 10 | Active | `pyspedas.projects.barrel.tests.test_barrel` | 184 |
| 11 | Active | `pyspedas.projects.soho.tests.test_soho` | 186 |
| 12 | Active | `pyspedas.projects.de2.tests.test_de2` | 188 |
| 13 | Active | `pyspedas.projects.st5.tests.test_st5` | 190 |
| 14 | Active | `pyspedas.projects.lanl.tests.test_lanl` | 192 |
| 15 | Active | `pyspedas.cotrans_tools.tests.test_quaternions` | 194 |
| 16 | Active | `pyspedas.projects.cnofs.tests.test_cnofs` | 196 |
| 17 | Active | `pyspedas.projects.dmsp.tests.test_dmsp` | 198 |
| 18 | Active | `pyspedas.projects.swfo.tests.test_swfo` | 200 |
| 19 | Active | `pyspedas.projects.dscovr.tests.test_dscovr` | 202 |
| 20 | Active | `pyspedas.utilities.tests.test_utilities_download` | 204 |
| 21 | Active | `pyspedas.utilities.tests.test_utilities_misc` | 206 |
| 22 | Active | `pyspedas.utilities.tests.test_preferences` | 208 |
| 23 | Active | `pyspedas.utilities.tests.test_utilities_download_uri` | 210 |
| 24 | Active | `pyspedas.utilities.tests.test_xdegap` | 212 |
| 25 | Active | `pyspedas.utilities.tests.test_math` | 214 |
| 26 | Active | `pyspedas.utilities.tests.test_interp_nan` | 216 |
| 27 | Active | `pyspedas.utilities.tests.test_utilities_tplot_wildcard` | 218 |
| 28 | Active | `pyspedas.utilities.tests.test_utilities_plot` | 220 |
| 29 | Active | `pyspedas.tplot_tools.MPLPlotter.plot_tests.test_wrap_label` | 222 |
| 30 | Active | `pyspedas.tplot_tools.MPLPlotter.plot_tests.test_fill_between` | 224 |
| 31 | Active | `pyspedas.tplot_tools.MPLPlotter.plot_tests.test_grid_background_options` | 226 |
| 32 | Active | `pyspedas.utilities.tests.test_utilities_tplotxy` | 228 |
| 33 | Active | `pyspedas.utilities.tests.test_tplotxy_ranges` | 230 |
| 34 | Active | `pyspedas.utilities.tests.test_utilities_time` | 232 |
| 35 | Active | `pyspedas.utilities.tests.test_utilities_libs` | 234 |
| 36 | Active | `pyspedas.cotrans_tools.tests.test_cotrans` | 236 |
| 37 | Active | `pyspedas.cotrans_tools.tests.test_minvar` | 238 |
| 38 | Active | `pyspedas.cotrans_tools.tests.test_fac` | 240 |
| 39 | Active | `pyspedas.cotrans_tools.tests.test_lmn` | 242 |
| 40 | Active | `pyspedas.projects.csswe.tests.test_csswe` | 244 |
| 41 | Active | `pyspedas.projects.equator_s.tests.test_equator_s` | 246 |
| 42 | Active | `pyspedas.projects.image.tests.test_image` | 248 |
| 43 | Active | `pyspedas.projects.psp.tests.test_psp` | 250 |
| 44 | Active | `pyspedas.projects.rbsp.tests.test_rbsp` | 252 |
| 45 | Active | `pyspedas.projects.stereo.tests.test_stereo` | 254 |
| 46 | Active | `pyspedas.projects.twins.tests.test_twins` | 256 |
| 47 | Active | `pyspedas.projects.wind.tests.test_wind` | 258 |
| 48 | Active | `pyspedas.projects.polar.tests.test_polar` | 260 |
| 49 | Active | `pyspedas.projects.geotail.tests.test_geotail` | 262 |
| 50 | Active | `pyspedas.analysis.tests.test_analysis` | 264 |
| 51 | Active | `pyspedas.utilities.tests.test_tinterpol_mxn` | 266 |
| 52 | Active | `pyspedas.utilities.tests.test_interpolate_rotation` | 268 |
| 53 | Active | `pyspedas.analysis.tests.test_twavpol` | 270 |
| 54 | Active | `pyspedas.analysis.tests.test_wavelet` | 272 |
| 55 | Active | `pyspedas.projects.fast.tests.test_fast` | 274 |
| 56 | Active | `pyspedas.projects.omni.tests.test_omni` | 276 |
| 57 | Active | `pyspedas.projects.themis.tests.test_themis` | 278 |
| 58 | Active | `pyspedas.projects.themis.tests.test_themis_s3` | 280 |
| 59 | Active | `pyspedas.projects.ulysses.tests.test_ulysses` | 282 |
| 60 | Active | `pyspedas.projects.solo.tests.test_solo` | 284 |
| 61 | Active | `pyspedas.projects.kyoto.tests.test_kyoto` | 286 |
| 62 | Active | `pyspedas.projects.swarm.tests.test_swarm` | 288 |
| 63 | Active | `pyspedas.projects.themis.tests.test_themis_check_args` | 290 |
| 64 | Active | `pyspedas.projects.themis.tests.test_themis_autoload_support` | 292 |
| 65 | Active | `pyspedas.projects.themis.tests.test_themis_cal_fit` | 294 |
| 66 | Active | `pyspedas.projects.themis.tests.test_themis_dsl_cotrans` | 296 |
| 67 | Active | `pyspedas.projects.themis.tests.test_themis_lunar_cotrans` | 298 |
| 68 | Active | `pyspedas.projects.themis.tests.test_themis_spinmodel` | 300 |
| 69 | Active | `pyspedas.projects.themis.tests.test_themis_state` | 302 |
| 70 | Active | `pyspedas.projects.themis.tests.test_themis_scpot2dens` | 304 |

## Validation rule

Any future split of the quick tests must account for every row in this table.
The two commented rows should remain marked as commented unless they are
explicitly re-enabled in `quick_tests.yml`.

## Logical test groups

The active tests are organized by subsystem or documented data-source
boundary. The numbers below refer to the inventory rows above.

| Group | Purpose | Inventory entries | Count |
|---|---|---|---:|
| `utilities` | Shared utilities, downloads, preferences, and interpolation helpers | 1, 5, 6, 20-26, 34, 35, 51, 52 | 14 |
| `tplot` | tplot wildcard, plotting, and tplot-XY behavior | 27-33 | 7 |
| `cotrans` | Coordinate transformation routines | 15, 36-39 | 5 |
| `analysis` | General analysis, wave polarization, and wavelet routines | 50, 53-54 | 3 |
| `hapi` | Direct HAPI client coverage | 2 | 1 |
| `themis` | THEMIS/ARTEMIS loader and THEMIS-specific functionality | 8-9, 57-58, 63-70 | 12 |
| `missions-spdf` | Mission loaders documented as using SPDF, including PSP's SPDF/team-server support | 7, 10-14, 16-17, 19, 40-44, 46-49, 55-56, 59-60 | 22 |
| `missions-non-spdf` | Mission loaders using non-SPDF sources | 18, 45, 61-62 | 4 |

Total active tests assigned: **68**.

The mission groups follow the source descriptions in
`pyspedas/projects/AGENTS.md`. In particular, SWFO uses the NOAA NCEI
S3-compatible archive, STEREO uses a Berkeley mirror, Kyoto uses WDC indices,
Swarm uses the VirES HAPI server, and Galileo and Juno use Iowa DAS2 servers.
HAPI remains a separate group because `test_hapi_testdata` directly tests the
shared HAPI client rather than a mission loader.
