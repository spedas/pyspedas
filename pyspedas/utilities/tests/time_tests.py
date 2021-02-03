import unittest
from datetime import datetime, timezone

from pyspedas.utilities.time_string import time_string, time_datetime, time_string_one
from pyspedas.utilities.time_double import time_float_one, time_float, time_double

class TimeTestCases(unittest.TestCase):
    def test_time_datetime(self):
        """Test time_datetime function."""
        self.assertTrue(time_datetime(1450137600.0000000) == datetime(2015, 12, 15, 0, 0, tzinfo=timezone.utc))
        self.assertTrue([time_datetime(1450137600.0000000), time_datetime(1444953600.0000000)] 
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

if __name__ == '__main__':
    unittest.main()