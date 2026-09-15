"""Offline regression tests for interp_nan gap limits (issue #1457)."""

import unittest
import warnings

import numpy as np
from numpy.testing import assert_allclose, assert_array_equal

from pyspedas import del_data, get_data, interp_nan, store_data


class InterpNanTests(unittest.TestCase):
    def setUp(self):
        self.times = np.array([0., 1., 2., 3., 10., 11., 20.])
        self.values = np.array([0., np.nan, np.nan, 3., 10., np.nan, 20.])
        store_data('interp_nan_test', data={'x': self.times, 'y': self.values},
                   attr_dict={'custom': {'units': 'test'}})

    def tearDown(self):
        del_data('interp_nan_test*')

    def test_time_limit_uses_elapsed_seconds(self):
        # Fill two missing samples across 3 seconds, but not one across 10.
        interp_nan('interp_nan_test', 'interp_nan_test_out', max_gap_time=3)
        assert_allclose(get_data('interp_nan_test_out').y,
                        [0, 1, 2, 3, 10, np.nan, 20], equal_nan=True)

    def test_time_threshold(self):
        interp_nan('interp_nan_test', 'interp_nan_test_out', max_gap_time=2.5)
        assert_allclose(get_data('interp_nan_test_out').y, self.values, equal_nan=True)
        interp_nan('interp_nan_test', 'interp_nan_test_out', max_gap_time=0)
        assert_allclose(get_data('interp_nan_test_out').y, self.values, equal_nan=True)

    def test_subsecond_time_limit(self):
        store_data('interp_nan_test', data={'x': [0, .125, .25],
                                           'y': [0, np.nan, 2]})
        interp_nan('interp_nan_test', 'interp_nan_test_out', max_gap_time=.25)
        assert_allclose(get_data('interp_nan_test_out').y, [0, 1, 2])
        interp_nan('interp_nan_test', 'interp_nan_test_out', max_gap_time=.2)
        assert_allclose(get_data('interp_nan_test_out').y, [0, np.nan, 2], equal_nan=True)

    def test_sample_limit(self):
        # Xarray fills the first N NaNs even when a run is longer than N.
        interp_nan('interp_nan_test', 'interp_nan_test_out', max_gap_samples=1)
        assert_allclose(get_data('interp_nan_test_out').y,
                        [0, 1, np.nan, 3, 10, 11, 20], equal_nan=True)

    def test_both_limits(self):
        interp_nan('interp_nan_test', 'interp_nan_test_out', max_gap_time=3, max_gap_samples=1)
        assert_allclose(get_data('interp_nan_test_out').y,
                        [0, 1, np.nan, 3, 10, np.nan, 20], equal_nan=True)

    def test_deprecated_positional_alias(self):
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter('always', DeprecationWarning)
            interp_nan('interp_nan_test', 'interp_nan_test_out', 3)
        self.assertEqual(len(caught), 1)
        self.assertIs(caught[0].category, DeprecationWarning)
        self.assertEqual(caught[0].filename, __file__)
        assert_allclose(get_data('interp_nan_test_out').y,
                        [0, 1, 2, 3, 10, np.nan, 20], equal_nan=True)

    def test_alias_and_sample_limit(self):
        with self.assertWarns(DeprecationWarning):
            interp_nan('interp_nan_test', 'interp_nan_test_out', s_limit=3, max_gap_samples=1)
        assert_allclose(get_data('interp_nan_test_out').y, [0, 1, np.nan, 3, 10, np.nan, 20], equal_nan=True)

    def test_conflicting_alias(self):
        with self.assertWarns(DeprecationWarning):
            with self.assertRaises(ValueError):
                interp_nan('interp_nan_test', s_limit=3, max_gap_time=5)
        assert_allclose(get_data('interp_nan_test').y, self.values, equal_nan=True)

    def test_invalid_limits(self):
        for value in [-1, np.nan, np.inf, '3s', True]:
            with self.subTest(time=value), self.assertRaises(ValueError):
                interp_nan('interp_nan_test', 'interp_nan_test_out', max_gap_time=value)
        for value in [-1, 0, 1.5, '2', True]:
            with self.subTest(samples=value), self.assertRaises(ValueError):
                interp_nan('interp_nan_test', 'interp_nan_test_out', max_gap_samples=value)

    def test_default_in_place(self):
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter('always', DeprecationWarning)
            self.assertIsNone(interp_nan('interp_nan_test'))
        self.assertEqual(caught, [])
        assert_allclose(get_data('interp_nan_test').y, self.times)

    def test_named_output_preserves_source_times_and_metadata(self):
        interp_nan('interp_nan_test', 'interp_nan_test_out', max_gap_time=3)
        assert_allclose(get_data('interp_nan_test').y, self.values, equal_nan=True)
        assert_array_equal(get_data('interp_nan_test_out').times, self.times)
        output = get_data('interp_nan_test_out', xarray=True)
        self.assertEqual(output.name, 'interp_nan_test_out')
        self.assertEqual(output.attrs['custom']['units'], 'test')
        output.attrs['custom']['units'] = 'changed'
        self.assertEqual(get_data('interp_nan_test', metadata=True)['custom']['units'], 'test')

    def test_vector_gaps_edges_and_all_nan_component(self):
        values = [[np.nan, 0, np.nan], [1, np.nan, np.nan],
                  [np.nan, 2, np.nan], [3, np.nan, np.nan]]
        store_data('interp_nan_test', data={'x': [0, 1, 2, 3], 'y': values})
        interp_nan('interp_nan_test', 'interp_nan_test_out', max_gap_time=2)
        assert_allclose(get_data('interp_nan_test_out').y,
                        [[np.nan, 0, np.nan], [1, 1, np.nan],
                         [2, 2, np.nan], [3, np.nan, np.nan]], equal_nan=True)


if __name__ == '__main__':
    unittest.main()
