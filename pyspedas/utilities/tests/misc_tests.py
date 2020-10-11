"""Test fuctions in the utilites folder."""
import unittest

from pyspedas.utilities.dailynames import dailynames
from pyspedas import tcopy, time_double
from pyspedas.utilities.time_string import (time_string, time_datetime,
                                            time_string_one)
from pytplot import get_data, store_data


class UtilTestCases(unittest.TestCase):
    """Test fuctions in the utilites folder."""

    def test_dailynames(self):
        """Test dailynames function."""
        self.assertTrue(dailynames(trange=['2015-12-1', '2015-12-1/2:00'],
                                   hour_res=True) == ['2015120100',
                                                      '2015120101'])
        self.assertTrue(dailynames(trange=['2015-12-1', '2015-12-3'])
                        == ['20151201', '20151202'])
        self.assertTrue(dailynames(trange=['2015-12-3', '2015-12-2'])
                        == ['20151203'])
        self.assertTrue(dailynames() is None)
        self.assertTrue(dailynames(trange=['2015-12-3', '2019-12-2'],
                                   file_format='%Y') ==
                        ['2015', '2016', '2017', '2018', '2019'])
        self.assertTrue(dailynames(trange=['2015-1-1', '2015-3-2'],
                                   file_format='%Y%m') == ['201501', '201502',
                                                           '201503'])
        self.assertTrue(dailynames(trange=['2015-1-1', '2015-3-2'],
                                   file_format='/%Y/%m/') ==
                        ['/2015/01/', '/2015/02/', '/2015/03/'])
        self.assertTrue(dailynames(trange=['2015-1-1', '2015-1-1/3:00'],
                                   file_format='%H', res=60.0) ==
                        ['00', '01', '02'])
        self.assertTrue(dailynames(trange=['2015-1-1/2:00', '2015-1-1/3:00'],
                                   file_format='%M', res=600.) ==
                        ['00', '10', '20', '30', '40', '50'])

    def test_time_string(self):
        """Test time_string function."""
        t0 = time_string(None)
        t1 = time_datetime(None)
        t2 = time_datetime(1000000000.0)
        t3 = time_string_one(None)
        print("Times functions test:", t0, t1, t2, t3)
        self.assertTrue(time_string(1450181243.767) ==
                        '2015-12-15 12:07:23.767000')
        self.assertTrue(time_string([1450181243.767, 1450181263.767])
                        == ['2015-12-15 12:07:23.767000',
                            '2015-12-15 12:07:43.767000'])

    def test_time_double(self):
        """Test time_double function."""
        self.assertTrue(time_double('2015-12-15 12:07:23.767000')
                        == 1450181243.767)
        self.assertTrue(time_double(['2015-12-15 12:07:23.767000',
                                     '2015-12-15 12:07:43.767000'])
                        == [1450181243.767, 1450181263.767])

    def test_tcopy(self):
        """Test tcopy function."""
        store_data('test', data={'x': [1, 2, 3], 'y': [5, 5, 5]})
        tcopy('test')
        tcopy('test', 'another-copy')
        t, d = get_data('test-copy')
        self.assertTrue(t.tolist() == [1, 2, 3])
        self.assertTrue(d.tolist() == [5, 5, 5])
        t, d = get_data('another-copy')
        self.assertTrue(t.tolist() == [1, 2, 3])
        self.assertTrue(d.tolist() == [5, 5, 5])
        # the following should gracefully error
        tcopy('doesnt exist', 'another-copy')
        tcopy(['another-copy', 'test'], 'another-copy')


if __name__ == '__main__':
    unittest.main()
