import unittest
import logging
import numpy as np
from numpy.testing import assert_allclose, assert_array_equal
from pyspedas.projects.mms.spd_mms_load_bss import spd_mms_load_bss
from pyspedas.projects.mms.mms_load_sroi_segments import mms_load_sroi_segments, get_mms_srois
from pyspedas.projects.mms.deprecated.mms_load_fast_segments import mms_load_fast_segments
from pyspedas.projects.mms.mms_load_brst_segments import mms_load_brst_segments
from pyspedas.projects.mms.mms_update_brst_intervals import mms_update_brst_intervals
from pyspedas.tplot_tools import data_exists, del_data, time_string, time_double
from pyspedas.projects.mms.mms_tai2unix import mms_tai2unix, mms_unix2tai
from pyspedas.projects.mms.mms_update_fast_intervals import mms_update_fast_intervals
from pyspedas import unix2tai, tai2unix


class SegmentTestCases(unittest.TestCase):

    def test_cdfepoch_leap(self):
        from cdflib import cdfepoch
        t1=np.int64(536500867184000000) # 23:59:59
        t2=t1+1000000000 # Leap second: 23:59:60
        t3=t2+1000000000 # First second of 2017, 00:00:00
        t4=t3+1000000000 # 00:00:01
        t5=t3+60*60*1000000000 # One hour after midnight, 2017-01-01/01:00:00
        b3=cdfepoch.breakdown_tt2000(t3) # t3 converts correctly to 2017-01-01/00:00:00
        assert_array_equal(b3, [2017, 1, 1, 0, 0, 0, 0, 0, 0])
        print("t3 ",b3)

        b23=cdfepoch.breakdown_tt2000([t2,t3]) # wrong: t3 comes out with min=60
        # Assertion disabled pending bug fix in cdflib
        #assert_array_equal(b23[1,:], [2017, 1, 1, 0, 0, 0, 0, 0, 0])
        print("t2 t3",b23)

        b13=cdfepoch.breakdown_tt2000([t1,t3]) # min = 60
        #assert_array_equal(b13[1::], [2017, 1, 1, 0, 0, 0, 0, 0, 0])
        print("t1 t3", b13)

        b14=cdfepoch.breakdown_tt2000([t1,t4]) # correct
        assert_array_equal(b14[1,:], [2017, 1, 1, 0, 0, 1, 0, 0, 0])
        print("t1 t4",b14)

        b15=cdfepoch.breakdown_tt2000([t1,t5]) # wrong: comes out as 00:60 rather than 01:00
        #assert_array_equal(b15[1,:], [2017, 1, 1, 1, 0, 0, 0, 0, 0])
        print("t1 t5",b15)


    def test_tai2unix_scalar(self):
        from pyspedas import unix2tai, tai2unix
        start_date='2016-12-31/23:59:00'
        start_unix = time_double(start_date)
        unix=np.zeros(70,np.float64)
        rt_unix=np.zeros(70,np.float64)

        for i in range(70):
            unix[i] = start_unix + i
            unix_str = time_string(unix[i])
            tai = unix2tai(unix[i])
            rt_unix[i] = tai2unix(tai)
            tai2unix_str = time_string(rt_unix[i])
            print(unix[i],unix_str,tai,rt_unix[i],tai2unix_str)
        assert_allclose(unix,rt_unix)

    def test_tai2unix_array(self):
        from pyspedas import unix2tai, tai2unix
        start_date='2016-12-31/23:59:00'
        start_unix = time_double(start_date)
        unix=np.array([start_unix + i for i in range(70)])

        unix_str = time_string(unix)
        tai = unix2tai(unix)
        # Why does this fail when the scalar version does not?
        # It's a cdflib bug that's overeager about marking leap second transitions.
        # We can avoid this by iterating over each input value. rather than all in one shot,
        # so we can catch cdflib exceptions and work around the bog.   Once cdflib is fixed,
        # we should be able to go back to a completely vectorized version of tai2unix.
        rt_unix = tai2unix(tai)
        assert_allclose(unix,rt_unix)
        t1 = unix2tai(time_double('2016-12-31/23:59:59')) # just before 2017 leap second
        t2 = t1 + 1.0 # the leap second itself...last second of 2016, 23:59:60
        t3 = t2 + 1.0 # first second of 2017, 00:00:0
        t4 = t3 + 1.0 # 00:00:01
        t5 = t3 + 60*60 # 01:00:00, one hour after leap sec boundary

        # Here we're testing that no uncaught exceptions are raised.  A few of these will
        # trigger cdflib bugs, but tai2unix should catch them
        t1_str = time_string(tai2unix(t1))
        t2_str = time_string(tai2unix(t2))
        t3_str = time_string(tai2unix(t3))
        t12_str = time_string(tai2unix([t1,t2]))
        t13_str = time_string(tai2unix([t1,t3]))
        t134_str = time_string(tai2unix([t1,t3, t4]))
        t15_str = time_string(tai2unix([t1,t5]))


    def test_sroi(self):
        del_data("*")
        sroi = mms_load_sroi_segments(trange=['2019-10-01', '2019-11-01'])
        self.assertTrue(data_exists('mms1_bss_sroi'))
        self.assertTrue(len(sroi[0]) == 28)
        self.assertTrue(sroi[0][0] == 1569849345.0)
        self.assertTrue(sroi[1][0] == 1569923029.0)
        with self.assertLogs(level='ERROR') as log:
            # error, no trange specified
            sroi = mms_load_sroi_segments()
            self.assertIn("Error; no trange specified.", log.output[0])

            # error, start time not specified
            none = get_mms_srois(end_time=1569849345.0)
            self.assertIn("Error, start time not specified", log.output[1])

            # error, end time not specified
            none = get_mms_srois(start_time=1569849345.0)
            self.assertIn("Error, end time not specified", log.output[2])

            # error, probe not specified
            none = get_mms_srois(start_time=1569849345.0, end_time=1569849345.0)
            self.assertIn("Error, sc_id not specified", log.output[3])

    def test_brst(self):
        del_data("*")
        brst = mms_load_brst_segments(trange=['2015-10-16', '2015-10-17'])
        self.assertTrue(len(brst[0]) == 53)
        self.assertTrue(brst[0][0] == 1444975174.0)
        self.assertTrue(brst[1][0] == 1444975244.0)
        self.assertTrue(data_exists('mms_bss_burst'))
        with self.assertLogs(level='ERROR') as log:
            # error, no trange specified
            brst = mms_load_brst_segments()
            self.assertIn("Error; no trange specified.", log.output[0])

    def test_spd_mms_load_bss(self):
        del_data("*")
        spd_mms_load_bss(trange=['2015-10-01', '2015-11-01'])
        self.assertTrue(data_exists('mms_bss_burst'))
        spd_mms_load_bss(trange=['2019-10-01', '2019-11-01'])
        self.assertTrue(data_exists('mms_bss_burst'))
        self.assertTrue(data_exists('mms1_bss_sroi'))

    def test_spd_mms_load_bss_err(self):
        del_data("*")
        with self.assertLogs(level='ERROR') as log:
            spd_mms_load_bss(trange=['2015-10-01', '2015-11-01'], datatype='brst', include_labels=True)
            self.assertFalse(data_exists('mms_bss_fast'))
            self.assertIn("Unsupported datatype: brst; valid options: \"fast\" and \"burst\"", log.output[0])

    def test_tai_unix_conversions(self):
        dates = [
            '2015-10-01 00:00',
            '2016-12-31 23:59:58',
            '2016-12-31 23:59:59',
            '2017-01-01 00:00:00',
            '2017-01-01 00:00:01',
        ]

        unix_times = np.array(time_double(dates))
        tai_times = np.array(mms_unix2tai(unix_times))
        rt_unix = np.array(mms_tai2unix(tai_times))
        assert_allclose(unix_times, rt_unix, atol=0.0001)

    def test_mms_tai_unix_wrappers_match_generic_converters(self):
        from pyspedas import tai2unix, unix2tai

        dates = [
            '2016-12-31 23:59:58',
            '2016-12-31 23:59:59',
            '2017-01-01 00:00:00',
            '2017-01-01 00:00:01',
        ]

        unix_times = np.array(time_double(dates))
        tai_times = unix2tai(unix_times)

        assert_allclose(mms_unix2tai(unix_times), tai_times)
        assert_allclose(mms_tai2unix(tai_times), tai2unix(tai_times))

        scalar_tai = mms_unix2tai(unix_times[0])
        self.assertTrue(np.isscalar(scalar_tai))

        scalar_unix = mms_tai2unix(tai_times[0])
        self.assertIsInstance(scalar_unix, np.ndarray)
        self.assertEqual(scalar_unix.shape, (1,))
        assert_allclose(scalar_unix[0], unix_times[0])

    def test_tai_unix_input_types(self):
        unix_dbl = time_double('2017-01-01')
        tai_dbl = unix2tai(unix_dbl)
        unix_uint64 = np.uint64(unix_dbl)
        tai = unix2tai(unix_uint64)
        self.assertEqual(tai_dbl, tai)
        unix_rt1 = tai2unix(tai)
        # This used to fail due to issues with signed vs unsigned values
        unix_rt2 = tai2unix(np.uint64(tai))
        self.assertEqual(unix_dbl, unix_rt1)
        self.assertEqual(unix_dbl, unix_rt2)

    def test_mms_update_fast_intervals(self):
        trange=['2016-01-01','2016-02-01']
        starts, ends = mms_update_fast_intervals(trange=trange)
        self.assertEqual(len(starts), len(ends))
        # Test that intervals are properly time clipped
        self.assertTrue(ends[0] >= time_double(trange[0]) )
        self.assertTrue(starts[-1] <= time_double(trange[1]))


if __name__ == '__main__':
    unittest.main()
