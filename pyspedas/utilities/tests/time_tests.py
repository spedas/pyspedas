import unittest
from datetime import datetime, timezone
import numpy as np
from pytplot import time_string, time_datetime
from pytplot import time_float, time_double, degap, store_data, get_data, options, data_exists


class TimeTestCases(unittest.TestCase):
    def test_time_datetime(self):
        """Test time_datetime function."""
        now = time_datetime()
        self.assertTrue(time_datetime('2015-12-15/00:00') == datetime(2015, 12, 15, 0, 0, tzinfo=timezone.utc))
        self.assertTrue(time_datetime(1450137600.0000000) == datetime(2015, 12, 15, 0, 0, tzinfo=timezone.utc))
        self.assertTrue([time_datetime(1450137600.0000000), time_datetime(1444953600.0000000)] 
            == [datetime(2015, 12, 15, 0, 0, tzinfo=timezone.utc), datetime(2015, 10, 16, 0, 0, tzinfo=timezone.utc)])
        self.assertTrue(time_datetime([1450137600.0000000, 1444953600.0000000])
            == [datetime(2015, 12, 15, 0, 0, tzinfo=timezone.utc), datetime(2015, 10, 16, 0, 0, tzinfo=timezone.utc)])


    def test_time_string(self):
        """Test time_string function."""
        self.assertTrue(time_string(fmt='%Y-%m-%d') == datetime.now().strftime('%Y-%m-%d'))
        self.assertTrue(time_string(1450181243.767, fmt='%Y-%m-%d') == '2015-12-15')
        self.assertTrue(time_string(1450181243.767, fmt='%Y-%m-%d/%H:%M:%S') == '2015-12-15/12:07:23')
        self.assertTrue(time_string(1450181243.767) == '2015-12-15 12:07:23.767000')
        self.assertTrue(time_string([1450181243.767, 1450181263.767]) == ['2015-12-15 12:07:23.767000', '2015-12-15 12:07:43.767000'])

    def test_time_double(self):
        """Test time_double function."""
        self.assertTrue(time_string(time_double(), fmt='%Y-%m-%d') == datetime.now().strftime('%Y-%m-%d'))
        self.assertTrue(time_double('2015-12-15/12:00') == 1450180800.0000000)
        self.assertTrue(time_double('2015-12-15/12') == 1450180800.0000000)
        #self.assertTrue(time_double('2015-12-15/6') == 1450159200.0000000) #this one doesn't work
        self.assertTrue(time_double('2015-12-15/6:00') == 1450159200.0000000)
        self.assertTrue(time_double('2015-12-15/06:00') == 1450159200.0000000)
        self.assertTrue(time_double('2015-12-15') == 1450137600.0000000)
        self.assertTrue(time_double('2015 12 15') == 1450137600.0000000)
        self.assertTrue(time_double('2015-12') == 1448928000.0000000)
        self.assertTrue(time_double('2015') == 1420070400.0000000)
        self.assertTrue(time_double('2015-12-15 12:07:23.767000') == 1450181243.767)
        self.assertTrue(time_double(['2015-12-15 12:07:23.767000', '2015-12-15 12:07:43.767000']) == [1450181243.767, 1450181263.767])

    def test_degap(self):
        float_times=np.array([1.0,2.0,3.0,11.0,12.0,13.0,21.0,22.0,23.0])
        int_times = np.array(float_times,dtype=np.int64)
        str_times = time_string(float_times)
        dtimes=np.array(float_times*1e9,dtype='datetime64[ns]')
        data = [1.0,2.0,3.0,11.0,12.0,13.0,21.0,22.0,23.0]
        sp = np.array([1,2,3])
        spdata = [sp,sp,sp,sp,sp,sp,sp,sp,sp]
        spv = [100,200,300]
        # Scalar data with floating point times
        store_data('degap_test_float',data={'x':float_times,'y':data})
        # Spectral data with floating point times
        store_data('degap_test_float_spec',data={'x':float_times,'y':spdata,'v':spv})
        options('degap_test_float_spec','spec',1)
        # Scalar data with integer times
        store_data('degap_test_int',data={'x':int_times,'y':data})
        # Spectral data with integer times
        store_data('degap_test_int_spec',data={'x':int_times,'y':spdata,'v':spv})
        options('degap_test_int_spec','spec',1)
        # Scalar data with datetime64[ns] times
        store_data('degap_test_dt64',data={'x':dtimes,'y':data})
        # Spectral data with datetime64[ns] times
        store_data('degap_test_dt64_spec',data={'x':dtimes,'y':spdata,'v':spv})
        options('degap_test_dt64_spec','spec',1)
        # Scalar data with string times
        store_data('degap_test_string',data={'x':str_times,'y':data})
        # Spectral data with string times
        store_data('degap_test_string_spec',data={'x':str_times,'y':spdata,'v':spv})
        options('degap_test_string_spec','spec',1)

        degap('degap_test_float',dt=2.0, maxgap=5.0, newname='degap_maxgap')
        dg_data=get_data('degap_maxgap')
        # Should NOT insert a data point with timestamp 5.0, value NaN
        self.assertEqual(dg_data.times[3],11.0)
        self.assertTrue(np.isfinite(dg_data.y[3]))
        self.assertTrue(len(dg_data.times), 9)

        degap('degap_test_float',dt=2.0, newname='degap_default_gapfill')
        dg_data=get_data('degap_default_gapfill')
        # Should NOT insert a data point with timestamp 5.0, value NaN
        self.assertEqual(dg_data.times[3],5.0)
        self.assertFalse(np.isfinite(dg_data.y[3]))
        self.assertTrue(len(dg_data.times), 15)

        degap('degap_test_float',dt=2.0, onenanpergap=True, newname='degap_onenanpergap')
        dg_data=get_data('degap_onenanpergap')
        # Should insert a data point with timestamp 5.0, value NaN
        self.assertEqual(dg_data.times[3],5.0)
        self.assertEqual(dg_data.times[7],15.0)
        self.assertFalse(np.isfinite(dg_data.y[3]))
        self.assertFalse(np.isfinite(dg_data.y[7]))
        self.assertTrue(len(dg_data.times), 11)

        degap('degap_test_float',dt=2.0, twonanpergap=True, newname='degap_twonanpergap')
        dg_data=get_data('degap_twonanpergap')
        # Should insert a data point with timestamp 5.0, value NaN
        self.assertEqual(dg_data.times[3],3.25)
        self.assertEqual(dg_data.times[4],10.75)
        self.assertFalse(np.isfinite(dg_data.y[3]))
        self.assertFalse(np.isfinite(dg_data.y[4]))
        self.assertTrue(len(dg_data.times), 13)

        degap('degap_test_float',dt=2.0)
        dg_data=get_data('degap_test_float')
        # Should insert a data point with timestamp 5.0, value NaN
        self.assertEqual(dg_data.times[3],5.0)
        self.assertFalse(np.isfinite(dg_data.y[3]))

        degap('degap_test_int',dt=2.0)
        dg_data=get_data('degap_test_int')
        # Should insert a data point with timestamp 5.0, value NaN
        self.assertEqual(dg_data.times[3],5.0)
        self.assertFalse(np.isfinite(dg_data.y[3]))

        degap('degap_test_float_spec',dt=2.0)
        dg_data=get_data('degap_test_float_spec')
        # Should insert a data point with timestamp 5.0, value [NaN, NaN, NaN]
        self.assertEqual(dg_data.times[3],5.0)
        self.assertFalse(np.isfinite(dg_data.y[3][1]))

        degap('degap_test_int_spec',dt=2.0)
        dg_data=get_data('degap_test_int_spec')
        # Should insert a data point with timestamp 5.0, value [NaN, NaN, NaN]
        self.assertEqual(dg_data.times[3],5.0)
        self.assertFalse(np.isfinite(dg_data.y[3][1]))

        degap('degap_test_dt64',dt=2.0)
        dg_data=get_data('degap_test_dt64')
        # Should insert a data point with timestamp 5.0, value NaN
        self.assertEqual(dg_data.times[3],5.0)
        self.assertFalse(np.isfinite(dg_data.y[3]))

        degap('degap_test_dt64_spec',dt=2.0)
        dg_data=get_data('degap_test_dt64_spec')
        # Should insert a data point with timestamp 5.0, value [NaN, NaN, NaN]
        self.assertEqual(dg_data.times[3], 5.0)
        self.assertFalse(np.isfinite(dg_data.y[3][1]))

        degap('degap_test_string',dt=2.0)
        dg_data=get_data('degap_test_string')
        # Should insert a data point with timestamp 5.0, value NaN
        self.assertEqual(dg_data.times[3],5.0)
        self.assertFalse(np.isfinite(dg_data.y[3]))

        degap('degap_test_string_spec',dt=2.0)
        dg_data=get_data('degap_test_string_spec')
        # Should insert a data point with timestamp 5.0, value [NaN, NaN, NaN]
        self.assertEqual(dg_data.times[3], 5.0)
        self.assertFalse(np.isfinite(dg_data.y[3][1]))

    def test_missing_pseudovar(self):
        times=np.array([1.0,2.0,3.0,11.0,12.0,13.0,21.0,22.0,23.0])
        data = [1.0,2.0,3.0,11.0,12.0,13.0,21.0,22.0,23.0]

        store_data('basevar1', data={'x':times,'y':data})
        store_data('basevar2', data={'x':times,'y':data})
        store_data('pseudovar_missing', data=['basevar1', 'basevar2', 'missing_var'])
        self.assertTrue(data_exists('pseudovar_missing'))
        store_data('pseudovar_empty_list',data=[])
        self.assertFalse(data_exists('pseudovar_empty_list'))
        store_data('pseudovar_all_bad',data=['missing_var1','missing_var2','missing_var3'])
        self.assertFalse(data_exists('pseudovar_all_bad'))


if __name__ == '__main__':
    unittest.main()