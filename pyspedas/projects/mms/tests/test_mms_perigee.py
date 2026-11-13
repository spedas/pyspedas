import unittest

import numpy as np

from pyspedas.projects.mms import mms_find_perigee_times
from pyspedas.tplot_tools import time_double, time_float_one


class PerigeeTestCases(unittest.TestCase):
    def test_default(self):
        """Find the perigees around a time in the early mission."""
        perigees = mms_find_perigee_times("2015-09-02")
        expected = time_double(["2015-09-01/04:57:30", "2015-09-02/04:51:00"])
        np.testing.assert_array_equal(perigees, expected)

    def test_numeric_time_and_probe(self):
        """Accept Unix time and an integer spacecraft number."""
        perigees = mms_find_perigee_times(time_float_one("2015-09-02"), probe=1)
        expected = time_double(["2015-09-01/04:57:30", "2015-09-02/04:51:00"])
        np.testing.assert_array_equal(perigees, expected)

    def test_compare_with_idl(self):
        """Match the corrected IDL routine using real MEC data."""
        # Results from IDL with the NaN handling fixed:
        # MMS> mms_find_perigee_times('2026-01-01/03:00:00', probe=1)
        # 1767084240.0000000       1767388590.0000000
        expected = [1767084240.0, 1767388590.0]

        # Both times lie between these perigees. Midnight also checks that
        # missing positions are skipped rather than accepted as a perigee.
        for time in ["2026-01-01", "2026-01-01/03:00:00"]:
            with self.subTest(time=time):
                perigees = mms_find_perigee_times(time, probe="1")
                np.testing.assert_array_equal(perigees, expected)


if __name__ == "__main__":
    unittest.main()
