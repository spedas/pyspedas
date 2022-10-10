import unittest
from pyspedas.utilities.data_exists import data_exists
import pyspedas


class LoadTestCases(unittest.TestCase):
    def test_load_dst_data(self):
        # final
        dst_vars = pyspedas.kyoto.dst(trange=['2015-10-15', '2015-10-16'])
        self.assertTrue(data_exists('kyoto_dst'))
        # provisional
        dst_vars = pyspedas.kyoto.dst(trange=['2019-10-15', '2019-10-16'])
        self.assertTrue(data_exists('kyoto_dst'))
        # real time
        dst_vars = pyspedas.kyoto.dst(trange=['2022-7-15', '2022-7-16'])
        self.assertTrue(data_exists('kyoto_dst'))

    def test_errors(self):
        pyspedas.kyoto.dst(trange=None)
        pyspedas.kyoto.dst(trange=['1015-10-15', '1015-10-16'])


if __name__ == '__main__':
    unittest.main()
