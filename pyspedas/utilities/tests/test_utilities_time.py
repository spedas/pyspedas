import unittest
from datetime import datetime, timezone
import numpy as np
from pyspedas import time_string, time_datetime, time_double, degap, store_data, get_data, options, data_exists, time_ephemeris, is_timezone_aware
from numpy.testing import assert_allclose
import logging
import pandas as pd

class TimeTestCases(unittest.TestCase):
    def test_time_datetime(self):
        """Test time_datetime function."""
        now = time_datetime()
        self.assertTrue(isinstance(now, datetime))
        self.assertTrue(time_datetime("2015-12-15/00:00") == datetime(2015, 12, 15, 0, 0, tzinfo=timezone.utc))
        self.assertTrue(time_datetime(1450137600.0000000) == datetime(2015, 12, 15, 0, 0, tzinfo=timezone.utc))
        self.assertTrue(
            [time_datetime(1450137600.0000000), time_datetime(1444953600.0000000)]
            == [datetime(2015, 12, 15, 0, 0, tzinfo=timezone.utc), datetime(2015, 10, 16, 0, 0, tzinfo=timezone.utc)]
        )
        self.assertTrue(
            time_datetime([1450137600.0000000, 1444953600.0000000])
            == [datetime(2015, 12, 15, 0, 0, tzinfo=timezone.utc), datetime(2015, 10, 16, 0, 0, tzinfo=timezone.utc)]
        )

    def test_numpy_time_get_store(self):
        trange = time_double(np.array(['2007-03-23', '2007-03-24']))
        trange_np = np.array(trange)
        # Create the same timestamps in three different time resolutions
        np_sec = np.array(trange_np,dtype="datetime64[s]")
        np_us = np_sec.astype('datetime64[us]')
        np_ns = np_sec.astype("datetime64[ns]")
        print('original trange:', trange)
        print('trange as numpy array: ',trange_np)
        print('npdatetime64[s]: ', np_sec)
        print('npdatetime64[us]: ', np_us)
        print('npdatetime64[ns]: ', np_ns)
        data = [1.0, 2.0]
        store_data('tvar_sec', data={'x': np_sec, 'y': data})
        store_data('tvar_us',  data={'x': np_us,  'y': data})
        store_data('tvar_ns',  data={'x': np_ns,  'y': data})
        # Check that different resolutions return the same unix times
        tv_secdata = get_data('tvar_sec')
        tv_usdata = get_data('tvar_us')
        tv_nsdata = get_data('tvar_ns')
        print('max time converted from sec: ', np.max(tv_secdata.times))
        print('max time converted from us: ', np.max(tv_usdata.times))
        print('max time converted from ns: ', np.max(tv_nsdata.times))
        assert_allclose(trange_np, tv_nsdata.times)
        assert_allclose(trange_np, tv_secdata.times)
        assert_allclose(trange_np, tv_usdata.times)
        # plot_options["trange"] is derived from the input times, need to check that too
        tv_secmd = get_data('tvar_sec',metadata=True)
        tv_usmd = get_data('tvar_us',metadata=True)
        tv_nsmd = get_data('tvar_ns',metadata=True)
        assert_allclose(tv_secmd['plot_options']['trange'],trange_np)
        assert_allclose(tv_usmd['plot_options']['trange'],trange_np)
        assert_allclose(tv_nsmd['plot_options']['trange'],trange_np)


    def test_time_string(self):
        """Test time_string function."""
        self.assertTrue(time_string(fmt="%Y-%m-%d") == datetime.now().strftime("%Y-%m-%d"))
        self.assertTrue(time_string(1450181243.767, fmt="%Y-%m-%d") == "2015-12-15")
        self.assertTrue(time_string(1450181243.767, fmt="%Y-%m-%d/%H:%M:%S") == "2015-12-15/12:07:23")
        self.assertTrue(time_string(1450181243.767) == "2015-12-15 12:07:23.767000")
        self.assertTrue(
            time_string([1450181243.767, 1450181263.767]) == ["2015-12-15 12:07:23.767000", "2015-12-15 12:07:43.767000"]
        )

    def test_time_double(self):
        """Test time_double function."""
        self.assertTrue(time_string(time_double(), fmt="%Y-%m-%d") == datetime.now().strftime("%Y-%m-%d"))
        self.assertTrue(time_double("2015-12-15/12:00") == 1450180800.0000000)
        self.assertTrue(time_double("2015-12-15/12") == 1450180800.0000000)
        # self.assertTrue(time_double('2015-12-15/6') == 1450159200.0000000) #this one doesn't work
        self.assertTrue(time_double("2015-12-15/6:00") == 1450159200.0000000)
        self.assertTrue(time_double("2015-12-15/06:00") == 1450159200.0000000)
        self.assertTrue(time_double("2015-12-15") == 1450137600.0000000)
        self.assertTrue(time_double("2015 12 15") == 1450137600.0000000)
        self.assertTrue(time_double("2015-12") == 1448928000.0000000)
        self.assertTrue(time_double("2015") == 1420070400.0000000)
        self.assertTrue(time_double("2015-12-15 12:07:23.767000") == 1450181243.767)
        self.assertTrue(
            time_double(["2015-12-15 12:07:23.767000", "2015-12-15 12:07:43.767000"]) == [1450181243.767, 1450181263.767]
        )

    def test_degap(self):
        float_times = np.array([1.0, 2.0, 3.0, 11.0, 12.0, 13.0, 21.0, 22.0, 23.0])
        int_times = np.array(float_times, dtype=np.int64)
        str_times = time_string(float_times)
        dtimes = np.array(float_times * 1e9, dtype="datetime64[ns]")
        data = [1.0, 2.0, 3.0, 11.0, 12.0, 13.0, 21.0, 22.0, 23.0]
        sp = np.array([1, 2, 3])
        spdata = [sp, sp, sp, sp, sp, sp, sp, sp, sp]
        spv = [100, 200, 300]
        # Scalar data with floating point times
        store_data("degap_test_float", data={"x": float_times, "y": data})
        # Spectral data with floating point times
        store_data("degap_test_float_spec", data={"x": float_times, "y": spdata, "v": spv})
        options("degap_test_float_spec", "spec", 1)
        # Scalar data with integer times
        store_data("degap_test_int", data={"x": int_times, "y": data})
        # Spectral data with integer times
        store_data("degap_test_int_spec", data={"x": int_times, "y": spdata, "v": spv})
        options("degap_test_int_spec", "spec", 1)
        # Scalar data with datetime64[ns] times
        store_data("degap_test_dt64", data={"x": dtimes, "y": data})
        # Spectral data with datetime64[ns] times
        store_data("degap_test_dt64_spec", data={"x": dtimes, "y": spdata, "v": spv})
        options("degap_test_dt64_spec", "spec", 1)
        # Scalar data with string times
        store_data("degap_test_string", data={"x": str_times, "y": data})
        # Spectral data with string times
        store_data("degap_test_string_spec", data={"x": str_times, "y": spdata, "v": spv})
        options("degap_test_string_spec", "spec", 1)

        degap("degap_test_float", dt=2.0, maxgap=5.0, newname="degap_maxgap")
        dg_data = get_data("degap_maxgap")
        # Should NOT insert a data point with timestamp 5.0, value NaN
        self.assertEqual(dg_data.times[3], 11.0)
        self.assertTrue(np.isfinite(dg_data.y[3]))
        self.assertTrue(len(dg_data.times), 9)

        degap("degap_test_float", dt=2.0, newname="degap_default_gapfill")
        dg_data = get_data("degap_default_gapfill")
        # Should NOT insert a data point with timestamp 5.0, value NaN
        self.assertEqual(dg_data.times[3], 5.0)
        self.assertFalse(np.isfinite(dg_data.y[3]))
        self.assertTrue(len(dg_data.times), 15)

        degap("degap_test_float", dt=2.0, onenanpergap=True, newname="degap_onenanpergap")
        dg_data = get_data("degap_onenanpergap")
        # Should insert a data point with timestamp 5.0, value NaN
        self.assertEqual(dg_data.times[3], 5.0)
        self.assertEqual(dg_data.times[7], 15.0)
        self.assertFalse(np.isfinite(dg_data.y[3]))
        self.assertFalse(np.isfinite(dg_data.y[7]))
        self.assertTrue(len(dg_data.times), 11)

        degap("degap_test_float", dt=2.0, twonanpergap=True, newname="degap_twonanpergap")
        dg_data = get_data("degap_twonanpergap")
        # Should insert a data point with timestamp 5.0, value NaN
        self.assertEqual(dg_data.times[3], 3.25)
        self.assertEqual(dg_data.times[4], 10.75)
        self.assertFalse(np.isfinite(dg_data.y[3]))
        self.assertFalse(np.isfinite(dg_data.y[4]))
        self.assertTrue(len(dg_data.times), 13)

        degap("degap_test_float", dt=2.0)
        dg_data = get_data("degap_test_float")
        # Should insert a data point with timestamp 5.0, value NaN
        self.assertEqual(dg_data.times[3], 5.0)
        self.assertFalse(np.isfinite(dg_data.y[3]))

        degap("degap_test_int", dt=2.0)
        dg_data = get_data("degap_test_int")
        # Should insert a data point with timestamp 5.0, value NaN
        self.assertEqual(dg_data.times[3], 5.0)
        self.assertFalse(np.isfinite(dg_data.y[3]))

        degap("degap_test_float_spec", dt=2.0)
        dg_data = get_data("degap_test_float_spec")
        # Should insert a data point with timestamp 5.0, value [NaN, NaN, NaN]
        self.assertEqual(dg_data.times[3], 5.0)
        self.assertFalse(np.isfinite(dg_data.y[3][1]))

        degap("degap_test_int_spec", dt=2.0)
        dg_data = get_data("degap_test_int_spec")
        # Should insert a data point with timestamp 5.0, value [NaN, NaN, NaN]
        self.assertEqual(dg_data.times[3], 5.0)
        self.assertFalse(np.isfinite(dg_data.y[3][1]))

        degap("degap_test_dt64", dt=2.0)
        dg_data = get_data("degap_test_dt64")
        # Should insert a data point with timestamp 5.0, value NaN
        self.assertEqual(dg_data.times[3], 5.0)
        self.assertFalse(np.isfinite(dg_data.y[3]))

        degap("degap_test_dt64_spec", dt=2.0)
        dg_data = get_data("degap_test_dt64_spec")
        # Should insert a data point with timestamp 5.0, value [NaN, NaN, NaN]
        self.assertEqual(dg_data.times[3], 5.0)
        self.assertFalse(np.isfinite(dg_data.y[3][1]))

        degap("degap_test_string", dt=2.0)
        dg_data = get_data("degap_test_string")
        # Should insert a data point with timestamp 5.0, value NaN
        self.assertEqual(dg_data.times[3], 5.0)
        self.assertFalse(np.isfinite(dg_data.y[3]))

        degap("degap_test_string_spec", dt=2.0)
        dg_data = get_data("degap_test_string_spec")
        # Should insert a data point with timestamp 5.0, value [NaN, NaN, NaN]
        self.assertEqual(dg_data.times[3], 5.0)
        self.assertFalse(np.isfinite(dg_data.y[3][1]))

    def test_missing_pseudovar(self):
        times = np.array([1.0, 2.0, 3.0, 11.0, 12.0, 13.0, 21.0, 22.0, 23.0])
        data = [1.0, 2.0, 3.0, 11.0, 12.0, 13.0, 21.0, 22.0, 23.0]

        store_data("basevar1", data={"x": times, "y": data})
        store_data("basevar2", data={"x": times, "y": data})
        store_data("pseudovar_missing", data=["basevar1", "basevar2", "missing_var"])
        self.assertTrue(data_exists("pseudovar_missing"))
        store_data("pseudovar_empty_list", data=[])
        self.assertFalse(data_exists("pseudovar_empty_list"))
        store_data("pseudovar_all_bad", data=["missing_var1", "missing_var2", "missing_var3"])
        self.assertFalse(data_exists("pseudovar_all_bad"))

    def test_time_ephemeris(self):
        testdate = "2025-01-01/00:00:00"
        ut = time_double(testdate)
        et = time_ephemeris(ut)
        self.assertAlmostEqual(ut, 1735689600.0000000, places=5)
        self.assertAlmostEqual(et, 788961669.18399811, places=5)
        et_to_ut = time_ephemeris(et, et2ut=True)
        self.assertAlmostEqual(ut, et_to_ut, places=6)

    def test_time_ephemeris_leapsec_update (self):
        disable_time = time_double('2027-01-01')  # time of next possible leap second
        now = time_double()

        days_to_failure = (disable_time - now)/86400.0
        if days_to_failure < 120:
            logging.warning(f"time_ephemeris may need a leap second update in {int(days_to_failure)} days")
        else:
            logging.info(f"time_ephemeris may need a leap second update in {int(days_to_failure)} days")

        # If this bombs, we need to check if a leap second will be applied, and update the
        # disable_time variable here and in time_ephemeris().
        self.assertTrue(days_to_failure > 60)

    def test_store_data_time_conversions(self):
        # Test different ways of passing times to store_data, ensure that they
        # all round-trip through store_data/get_data correctly
        # Try different times: before Unix epoch, just at Unix epoch, after epoch

        # String timestamps with list as container
        time_string_list = ["1965-01-01","1970-01-01", "2001-01-01"]
        # Numeric types, with list as container
        time_dbl_list = time_double(time_string_list)
        time_int_list = [int(x) for x in time_dbl_list]
        # Timezone-aware and timezone-naive datetime objects, with list as container
        time_dt_list = time_datetime(time_string_list)
        self.assertTrue(is_timezone_aware(time_dt_list))
        time_dt_tz_naive_list = [aware_dt.replace(tzinfo=None) for aware_dt in time_dt_list]
        self.assertFalse(is_timezone_aware(time_dt_tz_naive_list[0]))
        time_string_np = np.array(time_string_list)
        # Same set of types, but with numpy arrays as the container
        time_dbl_np = np.array(time_dbl_list)
        time_int_np = np.array(time_int_list)
        time_dt_np = np.array(time_dt_list)
        # Numpy datetime64, ms and ns resolution, in numpy arrays and lists
        time_dbl_ns_np = time_dbl_np*1e9
        time_dbl_msec_np = time_dbl_np*1e3
        time_npdt_ns_np = time_dbl_ns_np.astype('datetime64[ns]')
        time_npdt_ms_np = time_dbl_msec_np.astype('datetime64[ms]')
        time_npdt_ns_list = [x for x in time_npdt_ns_np]
        time_npdt_ms_list = [x for x in time_npdt_ms_np]
        self.assertFalse(is_timezone_aware(time_npdt_ns_list))
        self.assertFalse(is_timezone_aware(time_npdt_ms_np))
        # Python datetimes and numpy datetimes [ms] with Pandas pd.Series as container
        time_dt_pd = pd.Series(time_dt_np)
        time_npdt_ms_pd = pd.Series(time_npdt_ms_np)


        data = [1,2,3]

        # Create tplot variables from each input type and container type
        store_data('time_string_list',data={'x': time_string_list, 'y': data})
        store_data('time_dbl_list',data={'x': time_dbl_list, 'y': data})
        store_data('time_int_list',data={'x': time_int_list, 'y': data})
        store_data('time_dt_list',data={'x': time_dt_list, 'y': data})
        store_data('time_dt_tz_naive_list',data={'x': time_dt_list, 'y': data})
        store_data('time_npdt_ns_list',data={'x': time_npdt_ns_list, 'y': data})
        store_data('time_npdt_ms_list',data={'x': time_npdt_ms_list, 'y': data})
        store_data('time_string_np',data={'x': time_string_np, 'y': data})
        store_data( 'time_dbl_np',data={'x': time_dbl_np, 'y': data})
        store_data('time_dt_np',data={'x': time_dt_np, 'y': data})
        store_data('time_int_np',data={'x': time_int_np, 'y': data})
        store_data('time_npdt_ns_np',data={'x': time_npdt_ns_np, 'y': data})
        store_data('time_npdt_ms_np',data={'x': time_npdt_ms_np, 'y': data})
        store_data('time_dt_pd',data={'x': time_dt_pd, 'y': data})
        store_data('time_npdt_ms_pd', data={'x': time_npdt_ms_pd, 'y': data})

        # Test xarray DataArray object as time variable.  This can happen (for now)
        # in tools like degap().

        xr = get_data('time_dt_np',xarray=True)
        store_data('time_dt_xr',data={'x':xr.coords["time"], 'y':xr.values})

        # Complete the round trip with get_data
        time_string_list_rt = get_data('time_string_list')
        time_dbl_list_rt = get_data('time_dbl_list')
        time_dt_list_rt = get_data('time_dt_list')
        time_dt_tz_naive_list_rt = get_data('time_dt_tz_naive_list')
        time_int_list_rt = get_data('time_int_list')
        time_npdt_ms_list_rt = get_data('time_npdt_ms_list')
        time_npdt_ns_list_rt = get_data('time_npdt_ns_list')
        time_string_np_rt = get_data('time_string_np')
        time_dbl_np_rt = get_data('time_dbl_np')
        time_dt_np_rt = get_data('time_dt_np')
        time_int_np_rt = get_data('time_int_np')
        time_npdt_ms_np_rt = get_data('time_npdt_ms_np')
        time_npdt_ns_np_rt = get_data('time_npdt_ns_np')
        time_dt_pd_rt = get_data('time_dt_pd')
        time_npdt_ms_pd_rt = get_data('time_npdt_ms_pd')
        time_dt_xr_rt = get_data('time_dt_xr')

        # Compare the retrieved timestamps to original timestamps
        assert_allclose(time_string_list_rt.times, time_dbl_np)
        assert_allclose(time_dbl_list_rt.times, time_dbl_np)
        assert_allclose(time_dt_list_rt.times, time_dbl_np)
        assert_allclose(time_dt_tz_naive_list_rt.times, time_dbl_np)
        assert_allclose(time_int_list_rt.times, time_dbl_np)
        assert_allclose(time_npdt_ms_list_rt.times, time_dbl_np)
        assert_allclose(time_npdt_ns_list_rt.times, time_dbl_np)
        assert_allclose(time_string_np_rt.times, time_dbl_np)
        assert_allclose(time_dbl_np_rt.times, time_dbl_np)
        assert_allclose(time_dt_np_rt.times, time_dbl_np)
        assert_allclose(time_int_np_rt.times, time_dbl_np)
        assert_allclose(time_npdt_ms_np_rt.times, time_dbl_np)
        assert_allclose(time_npdt_ns_np_rt.times, time_dbl_np)
        assert_allclose(time_dt_pd_rt.times, time_dbl_np)
        assert_allclose(time_npdt_ms_pd_rt.times, time_dbl_np)
        assert_allclose(time_dt_xr_rt.times, time_dbl_np)

if __name__ == "__main__":
    unittest.main()
