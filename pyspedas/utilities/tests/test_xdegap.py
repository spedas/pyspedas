import numpy as np
import unittest
from pyspedas import xdegap


class TestXdegap(unittest.TestCase):
    def test_no_nan_values(self):
        """Test array with no NaN values"""
        input_array = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        result = xdegap(input_array)
        np.testing.assert_array_equal(result, input_array)

    def test_single_nan_middle(self):
        """Test array with single NaN value in the middle"""
        input_array = np.array([1.0, 2.0, np.nan, 4.0, 5.0])
        expected = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        result = xdegap(input_array)
        np.testing.assert_array_almost_equal(result, expected)

    def test_multiple_consecutive_nans(self):
        """Test array with multiple consecutive NaN values"""
        input_array = np.array([1.0, np.nan, np.nan, 4.0, 5.0])
        # Naive expectation: multiple nans will be linearly interpolated to
        # the array indices:
        # expected = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        # Actual behavior: Pairwise averaging,left to right, of surrounding non-nan values
        # 2.5 is halfway between 1.0 and 4.0
        # 3.25 is halfway between 2.5 and 4.0
        expected = np.array([1.0, 2.5, 3.25, 4.0, 5.0])
        result = xdegap(input_array)
        np.testing.assert_array_almost_equal(result, expected)

    def test_nan_at_start(self):
        """Test array with NaN at the start"""
        input_array = np.array([np.nan, 2.0, 3.0, 4.0, 5.0])
        expected = np.array([2.0, 2.0, 3.0, 4.0, 5.0])
        result = xdegap(input_array)
        np.testing.assert_array_almost_equal(result, expected)

    def test_nan_at_end(self):
        """Test array with NaN at the end"""
        input_array = np.array([1.0, 2.0, 3.0, 4.0, np.nan])
        expected = np.array([1.0, 2.0, 3.0, 4.0, 4.0])
        result = xdegap(input_array)
        np.testing.assert_array_almost_equal(result, expected)

    def test_all_nan(self):
        """Test array with all NaN values"""
        input_array = np.array([np.nan, np.nan, np.nan])
        result = xdegap(input_array)
        self.assertTrue(np.all(np.isnan(result)))


if __name__ == "__main__":
    unittest.main()
