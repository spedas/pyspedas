# MTH5 tests overview

## `test_load_fdsn.py`

### `TestMTH5LoadFDSN` — exercises `load_fdsn()`

| Test | Purpose |
|---|---|
| `test10_load_fdsn_notrange` | No `trange` given -> logs `'trange not specified'` ERROR, no tplot var created |
| `test10_load_fdsn_trange_wrong_length` | A `trange` with 1 or 3+ elements -> logs `'trange must have exactly 2 elements'` ERROR, no tplot var created |
| `test10_load_fdsn_nonetwork` | No `network` given -> logs `'Network not specified'` ERROR |
| `test10_load_fdsn_nostation` | No `station` given -> logs `'Station not specified'` ERROR |
| `test20_print_request` | `print_request=True` prints a dataframe containing `network/station/start/end` columns (FDSN/MTH5 mocked to abort immediately after) |
| `test20_downloadonly_returns_path` | `downloadonly=True` returns the downloaded/cached MTH5 file path and never opens `MTH5` (skips tplot creation entirely) |
| `test20_load_fdsn_splits_on_units` | Runs with different units (e.g. a sensor swap) split into `fdsn_TEST_TEST`/`_1`, each keeping its own `data_att['units']` |
| `test20_load_fdsn_splits_on_measurement_type` | Runs with different measurement types split the same way, each keeping its own `data_att['measurements_type']` |
| `test20_load_fdsn_splits_on_coord_sys` | Runs with different coordinate systems split the same way, each keeping its own `get_coords(...)` value |
| `test20_load_fdsn_splits_on_missing_channel_units` | A run missing units on one channel (e.g. `hy`) gets a distinct signature from a fully-populated run and splits instead of merging silently |
| `test20_load_fdsn_fills_missing_channel_with_nan` | A run with only 2 of 3 magnetic components still produces a `(N, 3)` tplot variable, with the missing component's column entirely `NaN` |
| `test20_request_df_parameter` | A custom `request_df` (with different network/station than the positional args) takes precedence, is passed unmodified to `make_mth5_from_fdsn_client` with the expected keyword arguments, and is not mutated by the call |
| `test20_station_data_undefined_unboundlocalerror` | No survey matches the station -> `station_data` is never assigned -> referencing it later raises `UnboundLocalError`, which must be caught and logged as `'station_data was not defined correctly'` |
| `test20_station_data_missing_channels_attributeerror` | `station_data.metadata` has no `channels_recorded` -> `AttributeError`, caught and logged the same as the `UnboundLocalError` case above |
| `test30_connection_errors` | Simulated `URLError` (no internet) propagates as `FDSNException` (exact subclass depends on whether obspy's service-discovery cache is cold or warm; see below) |
| `test40_connection_check` | Real load of a valid station; sets `CONNECTION_FAILED` meant to gate `test50_*` tests that need a reachable network but don't depend on `test40_load_fdsn_basic` |
| `test40_load_fdsn_basic` | Real load of two valid stations; checks both tplot vars exist; also sets `BASIC_TEST_FAILED` meant to gate `test60_*` tests |
| `test50_load_fdsn_samedates` | start == end date -> no exception bubbles up, function returns `None` |
| `test50_load_fdsn_wrong_network_station` | Bad network and bad station each raise `FDSNBadRequestException`, log `'Cannot initialize mth5 object'`, and leave no temp/tplot artifacts |
| `test50_invalid_date` | A day-first date string (`'21-06-2015'`) resolves earlier than the start date -> `load_fdsn`'s end-before-start check logs an ERROR and returns `None` without creating a tplot variable |
| `test50_invalid_date_format` | A `request_df` date string that cannot be parsed as `YYYY-MM-DDThh:mm:ss` (e.g. `'not-a-date'`) raises `ValueError` from date-format validation |
| `test60_load_fdsn_nowarnings` | Confirms `nowarnings=True` suppresses loguru WARNING output that `nowarnings=False` produces |
| `test60_load_fdsn_nodownload` | Confirms `nodownload=True` reuses the cached `.h5` and is faster than the first (downloading) call |
| `test60_load_fdsn_timeclip` | Confirms returned timestamps are clipped and the tplot data is nonempty, ordered, and three-component with matching row count |

Test names encode a bucket number (`test<bucket>_<description>`) that groups
tests sharing the same run-order requirement; tests in the same bucket share
the same number so a later insertion between buckets can use an unused
number (e.g. `test15_`, `test45_`) without renumbering anything else:

- `test10_*`: no real connection and no mocking — return before any network call.
- `test20_*`: mock the network/client (`FDSN.__init__`, `MTH5.__init__`, or
  `make_mth5_from_fdsn_client`), so they never touch the real network.
- `test30_connection_errors`: the one test that needs obspy's service-discovery
  cache to still be cold (see "Setup and teardown" below) — must run before
  any `test40_*`/`test50_*`/`test60_*` test.
- `test40_*`: `test40_load_fdsn_basic` is the real, unmocked baseline load
  (sets `BASIC_TEST_FAILED`, writes the `.h5` cache consumed by
  `test60_load_fdsn_nodownload`); `test40_connection_check` makes its own real
  call and sets `CONNECTION_FAILED` for `test50_*` to check.
- `test50_*`: real FDSN calls that are independent of `test40_load_fdsn_basic`
  and don't consume its cache file, but skip via `self.skipTest(...)` if
  `CONNECTION_FAILED` is `True`.
- `test60_*`: real FDSN calls that depend on `test40_load_fdsn_basic` having
  run (check `BASIC_TEST_FAILED` and/or its cached `.h5` file via
  `self.skipTest(...)`).

Tests that make a real FDSN/EarthScope request (no mocking of the network
layer): 
- `test30_connection_errors` (mocks only the `urllib` opener, not FDSN/MTH5)
- `test40_connection_check`
- `test40_load_fdsn_basic`
- `test50_load_fdsn_samedates`
- `test50_load_fdsn_wrong_network_station`
- `test60_load_fdsn_nowarnings`
- `test60_load_fdsn_nodownload` (first call)
- `test60_load_fdsn_timeclip`

`test10_*`, `test20_*`, and `test50_invalid_date`/`test50_invalid_date_format`
do not reach the real network: the `test20_*` tests mock `FDSN.__init__`,
`MTH5.__init__`, `make_mth5_from_fdsn_client`, or `pyspedas.mth5.load_fdsn.MTH5`
directly, and the two `test50_invalid_date*` tests fail validation or hit
`load_fdsn`'s end-before-start early return before any network call.

### `TestListOfChannels` — pure unit tests, no I/O

| Test | Purpose |
|---|---|
| `test01_list_of_channels_type` | `_list_of_fdsn_channels()` returns a `str` |
| `test02_list_of_channels_divisible_by_three` | Channel count is a multiple of 3 |
| `test03_list_of_channels_contains_F` | Every channel's 2nd character is `'F'` |

### `TestDatasetsFunction` — exercises `datasets()`, mostly mocked

| Test | Purpose |
|---|---|
| `test01_datasets_no_trange` | No `trange` -> returns `None` |
| `test02_datasets_network_failure` | Mocked HTTP 500 -> logs `'HTTP or URL Error'`, returns `{}` |
| `test02_datasets_no_data` | Mocked HTTP 404 -> returns `{}` |
| `test04_datasets_valid_data` | Mocked 3-channel CSV parses into the expected dict |
| `test05_datasets_incorrect_data` | Mocked CSV with a mismatched channel -> filtered out, returns `{}` |
| `test06_url_construction_with_network` | `network=` appears as `net=` in the built URL |
| `test06_url_construction_with_station` | `station=` appears as `sta=` in the built URL |
| `test06_url_construction_with_network_and_station` | Both appear together |
| `test07_datasets_realcall` | Live call to EarthScope; skipped if `setUpClass` couldn't reach the host |
| `test08_datasets_USAarea` | `USAarea=True` adds lat/lon bounding params; `False`/omitted leaves them out |

Only `test07_datasets_realcall` makes a real request to EarthScope; every
other test in this class mocks `urllib.request.urlopen`. `setUpClass` also
makes one real TCP connection attempt (a plain socket probe, not a data
request) to decide whether to skip `test07_datasets_realcall`.

## Setup and teardown

**`TestMTH5LoadFDSN`**
- `setUpClass` (once per class): checks for already-open HDF5 file handles via
  `h5py.h5f.get_obj_ids`, storing the result in `cls.H5OPEN`. Nothing in the
  file currently reads `H5OPEN` afterward.
- `setUp` (before every test): clears all tplot variables if any exist, so
  each test starts with a clean tplot namespace.
- `tearDown`: no cleanup. Downloaded `.h5` cache files on disk persist across
  tests and across runs; `test60_load_fdsn_nodownload` depends on a leftover
  cache file created by `test40_load_fdsn_basic`.
- `BASIC_TEST_FAILED`: a class attribute set inside `test40_load_fdsn_basic`.
  Each `test60_*` test checks it at runtime (`if self.BASIC_TEST_FAILED:
  self.skipTest(...)`) and skips if the basic load failed.
- `CONNECTION_FAILED`: a class attribute set inside `test40_connection_check`
  based on whether its own real `load_fdsn` call raised. Each `test50_*` test
  checks it at runtime the same way, so it can skip cleanly instead of
  failing noisily when there is no network.
- `test30_connection_errors` must run before any test that makes a real FDSN
  call (i.e. before `test40_*`/`test50_*`/`test60_*`). This is required, not
  incidental: obspy's `Client` class (`obspy.clients.fdsn.client.Client`)
  keeps a class-level service-discovery cache (`__service_discovery_cache`)
  shared across every `Client` instance in the process. Once any earlier
  test makes a real FDSN call, that cache is populated for
  `service.earthscope.org`, so a later mocked-network-failure test skips
  real discovery and raises a different `FDSNException` subclass than it
  would on a cold cache. The bucket numbering (`30_` before `40_`/`50_`/
  `60_`) encodes this instead of relying on method-name sort order.

**`TestListOfChannels`**: no setup/teardown — stateless, isolated unit tests.

**`TestDatasetsFunction`**
- `setUpClass`: attempts a real TCP connection to `service.earthscope.org:443`
  once, to decide whether `test07_datasets_realcall` should run or skip.
- No `setUp`/`tearDown`: each test mocks `urllib.request.urlopen` itself, so
  there is no shared mutable state between tests.

## `test_mth5_import.py`

| Test | Purpose |
|---|---|
| `test_pyspedas_mth5_import_error` | Simulates `mth5` not being installed (`sys.modules['mth5'] = None`) and confirms `import pyspedas.mth5` raises `ImportError`/`ModuleNotFoundError` after logging the install instructions |

`setUp`/`tearDown` patch and unpatch `pyspedas.logging.error` with a
`MagicMock`, so the test can assert on what was logged without a real logging
handler.
