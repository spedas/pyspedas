
import unittest

from pyspedas.mms.spd_mms_load_bss import spd_mms_load_bss
from pyspedas.mms.mms_load_sroi_segments import mms_load_sroi_segments
from pyspedas.mms.mms_load_fast_segments import mms_load_fast_segments
from pyspedas.mms.mms_load_brst_segments import mms_load_brst_segments
from pyspedas.utilities.data_exists import data_exists


class SegmentTestCases(unittest.TestCase):
    def test_sroi(self):
        sroi = mms_load_sroi_segments(trange=['2019-10-01', '2019-11-01'])
        self.assertTrue(data_exists('mms1_bss_sroi'))
        self.assertTrue(len(sroi[0]) == 28)
        self.assertTrue(sroi[0][0] == 1569849345.0)
        self.assertTrue(sroi[1][0] == 1569923029.0)

    def test_brst(self):
        brst = mms_load_brst_segments(trange=['2015-10-16', '2015-10-17'])
        self.assertTrue(len(brst[0]) == 53)
        self.assertTrue(brst[0][0] == 1444975174.0)
        self.assertTrue(brst[1][0] == 1444975244.0)
        self.assertTrue(data_exists('mms_bss_burst'))

    def test_fast(self):
        fast = mms_load_fast_segments(trange=['2015-10-01', '2015-11-01'])
        self.assertTrue(data_exists('mms_bss_fast'))
        self.assertTrue(len(fast[0]) == 35)
        self.assertTrue(fast[0][0] == 1443504404.0)
        self.assertTrue(fast[1][0] == 1443554774.0)

    def test_spd_mms_load_bss(self):
        spd_mms_load_bss(trange=['2015-10-01', '2015-11-01'])
        self.assertTrue(data_exists('mms_bss_fast'))
        self.assertTrue(data_exists('mms_bss_burst'))
        spd_mms_load_bss(trange=['2019-10-01', '2019-11-01'])
        self.assertTrue(data_exists('mms_bss_burst'))
        self.assertTrue(data_exists('mms1_bss_sroi'))

    def test_spd_mms_load_bss_err(self):
        spd_mms_load_bss(trange=['2015-10-01', '2015-11-01'], datatype='brst', include_labels=True)
        self.assertTrue(~data_exists('mms_bss_fast'))


if __name__ == '__main__':
    unittest.main()
