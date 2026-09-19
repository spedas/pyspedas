# PyHC dependency smoke tests

Run this module explicitly, rather than discovering every PySPEDAS test:

```sh
MPLBACKEND=Agg python -m unittest -v pyspedas.tests.test_pyhc_integration
```

The suite is included in the PySPEDAS package, so the same command works with
an installed wheel. To test the installed PyHC environment, run from outside a
PySPEDAS source checkout so it does not shadow the installed package. Do not
upgrade or reinstall dependencies just to run the suite: that would change the
environment being tested. The environment must include the `maps` and `mth5`
extras (`basemap` and `mth5[obspy]`) for the full run. Missing or broken dependencies
are errors, not automatic skips. No pytest, credentials, IDL validation files,
external test-data repositories, or manual fixtures are needed.

The module contains two independently runnable groups:

```sh
python -m unittest -v pyspedas.tests.test_pyhc_integration.LocalTests
python -m unittest -v pyspedas.tests.test_pyhc_integration.NetworkTests
```

`LocalTests` uses synthetic inputs and packaged calibration CSVs. Geopack may
check for IGRF coefficient updates on its first import. `NetworkTests` uses
ordinary public load routines. A failed request or empty data fails the test,
so inspect the traceback and service status before diagnosing a dependency
conflict. CDAWeb and HAPI have 30-second request/socket timeouts here; these are
not whole-suite deadlines. Use a CI job timeout (for example, 10 minutes) to
bound retries, downloads, and the MTH5/ObsPy client.

Downloads use the normal mission caches. Set `SPEDAS_DATA_DIR` before starting
Python to choose a writable persistent cache. MTH5 reuses its five-minute HDF5
file if present. Cold and cached timings differ; rerun with an empty cache when
checking the download path. Plots are rendered with Agg into temporary files,
checked for nonblank image content, and removed. Tests clear the global tplot
variable store, so run them in a dedicated process.

## Selected candidates and adaptations

Source paths below are relative to `pyspedas/`. Test bodies are copied/adapted
locally, without importing the original suites and their expensive setup code.

| Smoke test | Source test | Coverage and size reduction |
| --- | --- | --- |
| `test_csv_sector_masks` | `projects/mms/tests/test_mms_feeps.py::test_sector_masks` | Packaged CSV reader and NumPy; two exact mask comparisons, no MMS login/download. |
| `test_line_plot` | `utilities/tests/test_utilities_plot.py::test_markers_and_symbols` | Matplotlib line/marker rendering through tplot; one six-point plot. |
| `test_basemap` | `tplot_tools/MPLPlotter/plot_tests/test_tplot_map.py::test_basic_map` | Basemap, pyproj, coastline data and Matplotlib; coarse map and 100 DPI instead of intermediate resolution/300 DPI. Replaces SECS' ~79 MB archive. |
| `test_wavelet_and_spectrogram` | `analysis/tests/test_analysis.py::test_wavelet` | PyWavelets, NumPy, xarray, Matplotlib spectrogram; original 4,000-point synthetic wave, output/shape/finite-value checks and a plot. |
| `test_numpy_interp` | `analysis/tests/test_analysis.py::test_numpy_interp` | NumPy interpolation at an exact input timestamp. |
| `test_tinterpol_slinear` | `analysis/tests/test_analysis.py::test_tinterpol_slinear` | PySPEDAS → xarray → SciPy spline interpolation; three points, no known-failing `interp1d` assertion. |
| `test_interpolate_nan_gaps` | `utilities/tests/test_interp_nan.py::test_time_limit_uses_elapsed_seconds` | xarray interpolation and bottleneck forward filling; seven synthetic points and an elapsed-time gap limit. |
| `test_t89` | `geopack/tests/test_geopack.py::test_tt89` and `gen_circle` | Geopack T89/IGRF with six synthetic GSM positions and fixed activity, replacing MMS ephemeris loading; also checks Astropy quantity conversion. |
| `test_wave_polarization` | `analysis/tests/test_twavpol.py::test_multiple_twavpol_call` | NumPy FFT/polarization and xarray storage; 512 synthetic samples replace the IDL fixture. Checks populated outputs, repeatability and spectral peak. |
| `test_cdf_ace` | `projects/ace/tests/test_ace.py::test_load_mfi_data` | requests, cdflib, NumPy/xarray; one hour of one variable from a daily ACE MFI CDF at SPDF. |
| `test_cdaweb_netcdf` | `cdagui_tools/tests/test_cdagui.py::test_load_icon_netcdf` | cdasws and its dependencies, requests, netCDF4/HDF5, xarray; one daily ICON file (~17 MB), served by NASA rather than NCEI. Uses dataset ID without a changing date label. |
| `test_hapi_calgary` | `hapi_tools/tests/test_hapi.py::test_calgary_specbins` | hapiclient, HAPI spectrogram bins and Matplotlib; five minutes of Calgary SWAN HSR power and frequency bins instead of a full day. Avoids SPDF for HAPI. |
| `test_mth5_fdsn` | `mth5/tests/test_load_fdsn.py::test02_load_fdsn_basic` | MTH5, mt_metadata, ObsPy, h5py and pandas through EarthScope; one station/five minutes rather than two stations/35 minutes. Failures are not swallowed. |

This is a compatibility probe, not scientific validation or exhaustive dependency
coverage. For example, CSV masks use the standard-library CSV reader; pandas is
exercised by MTH5. SpacePy is imported through cdasws, but its CDF backend is not
explicitly exercised. Cloud transports and VIRES are omitted per issue #1301;
particle processing, credentials, JAXA/ERG/NCEI services and IDL comparisons are
also excluded. Warnings remain visible to help diagnose binary/version issues.
