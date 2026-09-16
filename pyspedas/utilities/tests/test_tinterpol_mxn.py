"""Unit tests and IDL CDF validation for linear tinterpol_mxn.

Generator (IDL SPEDAS):
    general/tools/python_validate/tinterpol_mxn_validate.pro

Run from the PySPEDAS checkout::

    python -m pyspedas.utilities.tests.test_tinterpol_mxn

The IDL reference CDF is downloaded from spedas/test_data/interpolation_tests
using the standard PySPEDAS testing cache and validation-directory settings.
Set PYSPEDAS_TINTERPOL_MXN_CDF to use a local file generated with IDL
tinterpol_mxn_validate instead. No IDL installation is needed to run the tests.
If the download is unavailable, only the IDL validation class is skipped. An
explicitly configured missing file or an incomplete/corrupt fixture is an error.
"""

from copy import deepcopy
from datetime import datetime, timezone
import os
from pathlib import Path
import unittest

import numpy as np
from numpy.testing import assert_allclose, assert_array_equal

from pyspedas import cdf_to_tplot, del_data, get_data, store_data, tinterpol_mxn
from pyspedas.tplot_tools import data_quants
from pyspedas.utilities.config_testing import (
    TESTING_CONFIG,
    test_data_download_file as download_test_data,
)


class TinterpolMxnTests(unittest.TestCase):
    def tearDown(self):
        del_data('mxn_test*')

    def test_linear_and_default_extrapolation(self):
        result = tinterpol_mxn({'x': [0, 2, 5], 'y': [0, 4, 10]}, [-1, 0, 1, 5, 6])
        assert_array_equal(result['y'], [-2, 0, 2, 10, 12])
        self.assertEqual(result['x'].dtype, np.dtype('datetime64[ns]'))

    def test_nan_boundary(self):
        result = tinterpol_mxn({'x': [0, 2], 'y': [0, 4]}, [-1, 0, 1, 2, 3],
                              nan_extrapolate=True)
        assert_allclose(result['y'], [np.nan, 0, 2, 4, np.nan], equal_nan=True)

    def test_trim_preserves_target_order_and_duplicates(self):
        result = tinterpol_mxn({'x': [0, 2], 'y': [0, 4]}, [3, 2, -1, 1, 1, 0],
                              no_extrapolate=True)
        assert_array_equal(result['y'], [4, 2, 2, 0])
        assert_array_equal(result['x'].astype('datetime64[s]').astype(int), [2, 1, 1, 0])

    def test_tensor_repeat_uses_first_last_finite_components(self):
        values = np.array([[[np.nan, 1], [2, np.nan]],
                           [[3, 4], [np.nan, np.nan]],
                           [[5, np.nan], [6, np.nan]]])
        result = tinterpol_mxn({'x': [0, 1, 2], 'y': values}, [-1, 0, 2, 3],
                              repeat_extrapolate=True)
        assert_allclose(result['y'][0], [[3, 1], [2, np.nan]], equal_nan=True)
        assert_allclose(result['y'][-1], [[5, 4], [6, np.nan]], equal_nan=True)
        assert_allclose(result['y'][1:3], values[[0, 2]], equal_nan=True)

    def test_arbitrary_trailing_dimensions(self):
        for shape in [(3,), (3, 3), (2, 1, 3), (2, 2, 2, 2)]:
            with self.subTest(shape=shape):
                base = np.arange(np.prod(shape)).reshape(shape)
                values = np.stack([base, base + 2, base + 6])
                result = tinterpol_mxn({'x': [0, 1, 3], 'y': values}, [.5, 2])
                assert_array_equal(result['y'], np.stack([base + 1, base + 4]))

    def test_preserve_nan_and_exact_neighbors(self):
        result = tinterpol_mxn({'x': [0, 1, 2], 'y': [0, np.nan, 2]},
                              [0, .5, 1, 1.5, 2])
        assert_allclose(result['y'], [0, np.nan, np.nan, np.nan, 2], equal_nan=True)

    def test_ignore_nans_per_component_and_original_coverage(self):
        source = {'x': [0, 1, 2, 3],
                  'y': [[0, np.nan, np.nan], [np.nan, 2, np.nan],
                        [2, 4, np.nan], [3, np.nan, np.nan]]}
        result = tinterpol_mxn(source, [-1, 0, 1, 2, 3, 4], ignore_nans=True,
                              nan_extrapolate=True)
        assert_allclose(result['y'], [[np.nan]*3, [0, 0, np.nan], [1, 2, np.nan],
                                     [2, 4, np.nan], [3, 6, np.nan], [np.nan]*3],
                        equal_nan=True)

    def test_singleton(self):
        result = tinterpol_mxn({'x': [1], 'y': [[3, 4]]}, [0, 1, 2])
        assert_array_equal(result['y'], [[3, 4]]*3)
        result = tinterpol_mxn({'x': [1], 'y': 3}, [0, 1, 2], nan_extrapolate=True)
        assert_allclose(result['y'], [np.nan, 3, np.nan], equal_nan=True)
        result = tinterpol_mxn({'x': [0, 1, 2], 'y': [np.nan, 3, np.nan]},
                              [0, 1, 2], ignore_nans=True)
        assert_array_equal(result['y'], [3, 3, 3])

    def test_all_nan_and_empty_target(self):
        result = tinterpol_mxn({'x': [0, 1], 'y': [np.nan, np.nan]}, [0, .5, 1],
                              ignore_nans=True, repeat_extrapolate=True)
        self.assertTrue(np.isnan(result['y']).all())
        result = tinterpol_mxn({'x': [0, 1], 'y': [[1, 2], [3, 4]]}, [])
        self.assertEqual(result['y'].shape, (0, 2))
        result = tinterpol_mxn({'x': [0, 1], 'y': [[1, 2], [3, 4]]}, [2],
                              no_extrapolate=True)
        self.assertEqual(result['y'].shape, (0, 2))

    def test_descending_source(self):
        result = tinterpol_mxn({'x': [2, 1, 0], 'y': [4, 2, 0],
                               'metadata': {'units': 'test'}}, [-1, .5, 3])
        assert_array_equal(result['y'], [-2, 1, 6])

    def test_nanosecond_precision_and_exact_zero(self):
        times = np.array(['2018-07-01T13:02:16.922475000',
                          '2018-07-01T13:02:16.922475002',
                          '2018-07-01T13:02:16.922475004'], dtype='datetime64[ns]')
        values = np.array([.028584518, 0., .013626526], dtype=np.float32)
        result = tinterpol_mxn({'x': times, 'y': values}, times)
        assert_array_equal(result['y'], values)
        result = tinterpol_mxn({'x': times, 'y': [0, 2, 4]},
                              times[:1] + np.timedelta64(1, 'ns'))
        assert_array_equal(result['y'], [1])

    def test_datetime_and_string_times(self):
        source = {'x': [datetime(2020, 1, 1, tzinfo=timezone.utc),
                        datetime(2020, 1, 1, 0, 0, 2, tzinfo=timezone.utc)], 'y': [0, 2]}
        result = tinterpol_mxn(source, ['2020-01-01T00:00:01Z'])
        assert_array_equal(result['y'], [1])

    def test_complex_values(self):
        result = tinterpol_mxn({'x': [0, 2], 'y': [1+2j, 3+4j]}, [1])
        assert_array_equal(result['y'], [2+3j])

    def test_dictionary_dependencies_and_no_mutation(self):
        source = {'x': [0, 2], 'y': np.zeros((2, 2, 3)), 'v1': ['x', 'y'],
                  'v2': [[1, 2, 3], [3, 4, 5]], 'metadata': {'units': 'test'}}
        original = deepcopy(source)
        result = tinterpol_mxn(source, [1])
        assert_array_equal(result['v1'], ['x', 'y'])
        assert_array_equal(result['v2'], [[1, 2, 3]])
        result['metadata']['units'] = 'changed'
        self.assertEqual(source['metadata'], original['metadata'])
        assert_array_equal(source['y'], original['y'])

    def test_tplot_target_and_return_mode(self):
        store_data('mxn_test_source', data={'x': [0, 2], 'y': [0, 4]})
        store_data('mxn_test_target', data={'x': [1], 'y': [999]})
        result = tinterpol_mxn('mxn_test_source', 'mxn_test_target', return_data=True)
        assert_array_equal(result['y'], [2])
        self.assertNotIn('mxn_test_source_interp', data_quants)
        names = tinterpol_mxn('mxn_test_source', 'mxn_test_target')
        self.assertEqual(names, ['mxn_test_source_interp'])
        assert_array_equal(get_data(names[0]).y, [2])

    def test_wildcards_independent_trimming_and_naming(self):
        store_data('mxn_test_a', data={'x': [0, 1], 'y': [0, 1]})
        store_data('mxn_test_b', data={'x': [0, 3], 'y': [0, 3]})
        names = tinterpol_mxn('mxn_test_[ab]', [0, 1, 2, 3], no_extrapolate=True,
                              suffix='_out')
        self.assertEqual(names, ['mxn_test_a_out', 'mxn_test_b_out'])
        assert_array_equal(get_data(names[0]).y, [0, 1])
        assert_array_equal(get_data(names[1]).y, [0, 1, 2, 3])
        names = tinterpol_mxn(['mxn_test_b', 'mxn_test_a'], [0, 1, 2, 3],
                              no_extrapolate=True, newname=['mxn_test_c', 'mxn_test_d'])
        assert_array_equal(get_data(names[0]).y, [0, 1, 2, 3])
        self.assertEqual(tinterpol_mxn('mxn_test_a', [10], no_extrapolate=True), [])
        self.assertNotIn('mxn_test_a_interp', data_quants)

    def test_overwrite_snapshots_target(self):
        store_data('mxn_test_a', data={'x': [0, 2], 'y': [0, 2]})
        names = tinterpol_mxn('mxn_test_a', [1], overwrite=True)
        self.assertEqual(names, ['mxn_test_a'])
        assert_array_equal(get_data('mxn_test_a').y, [1])

    def test_preserve_tplot_coordinates_and_metadata(self):
        store_data('mxn_test_a', data={'x': [0, 2], 'y': np.zeros((2, 2, 3)),
                                     'v1': ['x', 'y'], 'v2': [[1, 2, 3], [3, 4, 5]]},
                   attr_dict={'data_att': {'units': 'nT', 'coord_sys': 'GSE'}})
        data_quants['mxn_test_a'].coords['v2'].attrs['units'] = 'eV'
        names = tinterpol_mxn('mxn_test_a', [-1, 1, 3], repeat_extrapolate=True)
        result = get_data(names[0], xarray=True)
        assert_array_equal(result.coords['v1'], ['x', 'y'])
        assert_array_equal(result.coords['v2'], [[1, 2, 3], [1, 2, 3], [3, 4, 5]])
        self.assertEqual(result.coords['v2'].attrs['units'], 'eV')
        self.assertEqual(result.attrs['plot_options']['trange'], [-1, 3])
        self.assertEqual(result.attrs['data_att']['coord_sys'], 'GSE')
        result.attrs['data_att']['units'] = 'changed'
        self.assertEqual(get_data('mxn_test_a', metadata=True)['data_att']['units'], 'nT')

    def test_dictionary_stored_tensor(self):
        names = tinterpol_mxn({'x': [0, 2], 'y': np.ones((2, 2, 2, 2, 2))}, [1],
                              newname='mxn_test_out')
        self.assertEqual(names, ['mxn_test_out'])
        self.assertEqual(get_data(names[0]).y.shape, (1, 2, 2, 2, 2))

    def test_time_coordinate_not_first_axis(self):
        store_data('mxn_test_a', data={'x': [0, 2], 'y': [[0, 1], [2, 3]]})
        source = data_quants['mxn_test_a']
        dim = source.dims[1]
        source.coords['custom'] = ((dim, 'time'), [[1, 3], [10, 30]])
        names = tinterpol_mxn('mxn_test_a', [1])
        assert_array_equal(data_quants[names[0]].coords['custom'], [[2], [20]])

    def test_static_bins_equal_time_length_stay_static(self):
        result = tinterpol_mxn({'x': [0, 2], 'y': [[0, 2], [2, 4]],
                               'v': [10, 20]}, [-1, 1, 3], nan_extrapolate=True)
        assert_array_equal(result['v'], [10, 20])

    def test_descending_error_bars(self):
        store_data('mxn_test_a', data={'x': [2, 0], 'y': [4, 0], 'dy': [3, 1]})
        names = tinterpol_mxn('mxn_test_a', [.5])
        assert_array_equal(get_data(names[0]).dy, [1.5])

    def test_batch_swaps_use_original_sources(self):
        store_data('mxn_test_a', data={'x': [0, 2], 'y': [0, 2]})
        store_data('mxn_test_b', data={'x': [1, 3], 'y': [10, 30]})
        tinterpol_mxn(['mxn_test_a', 'mxn_test_b'], 'mxn_test_b',
                      newname=['mxn_test_b', 'mxn_test_a'])
        assert_array_equal(get_data('mxn_test_b').y, [1, 3])
        assert_array_equal(get_data('mxn_test_a').y, [10, 30])

    def test_invalid_times_and_missing_target(self):
        for times in [[np.datetime64('NaT')], [[0, 1]], [np.inf]]:
            with self.subTest(times=times), self.assertRaises(ValueError):
                tinterpol_mxn({'x': [0, 1], 'y': [0, 1]}, times)
        with self.assertRaises(ValueError):
            tinterpol_mxn({'x': [0, 1], 'y': [0, 1]}, 'mxn_test_missing')
        store_data('mxn_test_nrv', data={'y': [1, 2]})
        with self.assertRaises(ValueError):
            tinterpol_mxn('mxn_test_nrv', [0])

    def test_previous_bins_mode_transition_keeps_y_linear(self):
        source = {'x': [0, 2, 4], 'y': [[0, 0], [20, 40], [40, 80]],
                  'v': [[10, 20], [100, 200], [1000, 2000]]}
        result = tinterpol_mxn(source, [3, 1, 2, 2, 0, 4])
        assert_array_equal(result['v'], [[100, 200], [10, 20], [100, 200],
                                        [100, 200], [10, 20], [1000, 2000]])
        assert_array_equal(result['y'], [[30, 60], [10, 20], [20, 40],
                                        [20, 40], [0, 0], [40, 80]])

    def test_previous_v1_v2_v3_and_spec_bins(self):
        store_data('mxn_test_a', data={'x': [0, 2], 'y': np.zeros((2, 2, 2, 2)),
                                     'v1': [[1, 2], [10, 20]],
                                     'v2': [[3, 4], [30, 40]],
                                     'v3': [[5, 6], [50, 60]]})
        tinterpol_mxn('mxn_test_a', [1, 2], newname='mxn_test_out')
        result = get_data('mxn_test_out', xarray=True)
        assert_array_equal(result.coords['v1'], [[1, 2], [10, 20]])
        assert_array_equal(result.coords['v2'], [[3, 4], [30, 40]])
        assert_array_equal(result.coords['v3'], [[5, 6], [50, 60]])
        assert_array_equal(result.coords['spec_bins'], result.coords['v2'])

    def test_previous_bins_boundary_policies(self):
        source = {'x': [0, 2], 'y': [[0, 0], [2, 4]], 'v': [[10, 20], [100, 200]]}
        result = tinterpol_mxn(source, [-1, 1, 3])
        assert_array_equal(result['v'], [[10, 20], [10, 20], [100, 200]])
        result = tinterpol_mxn(source, [-1, 1, 3], repeat_extrapolate=True)
        assert_array_equal(result['v'], [[10, 20], [10, 20], [100, 200]])
        result = tinterpol_mxn(source, [-1, 1, 3], nan_extrapolate=True)
        assert_allclose(result['v'], [[np.nan, np.nan], [10, 20], [np.nan, np.nan]], equal_nan=True)
        result = tinterpol_mxn(source, [-1, 1, 3], no_extrapolate=True)
        assert_array_equal(result['v'], [[10, 20]])
        result = tinterpol_mxn(source, [3], no_extrapolate=True)
        self.assertEqual(result['v'].shape, (0, 2))

    def test_previous_bins_preserve_nan_maps(self):
        source = {'x': [0, 2], 'y': [[0, np.nan], [2, 4]],
                  'v': [[np.nan, 20], [100, np.nan]]}
        result = tinterpol_mxn(source, [-1, 1, 2, 3], ignore_nans=True,
                              repeat_extrapolate=True)
        assert_allclose(result['v'], [[np.nan, 20], [np.nan, 20],
                                     [100, np.nan], [100, np.nan]], equal_nan=True)

    def test_previous_bins_descending_source(self):
        result = tinterpol_mxn({'x': [2, 0], 'y': [[2, 4], [0, 0]],
                               'v': [[100, 200], [10, 20]]}, [1, 2])
        assert_array_equal(result['v'], [[10, 20], [100, 200]])

    def test_previous_bins_time_axis_and_singleton(self):
        store_data('mxn_test_a', data={'x': [0, 2], 'y': [[0, 1], [2, 3]]})
        source = data_quants['mxn_test_a']
        source.coords['v1'] = ((source.dims[1], 'time'), [[10, 100], [20, 200]])
        tinterpol_mxn('mxn_test_a', [1, 2], newname='mxn_test_out')
        assert_array_equal(data_quants['mxn_test_out'].coords['v1'], [[10, 100], [20, 200]])
        result = tinterpol_mxn({'x': [1], 'y': [[1, 2]], 'v': [[10, 20]]}, [0, 1, 2])
        assert_array_equal(result['v'], [[10, 20]] * 3)

    def test_invalid_inputs_and_options(self):
        for times in [[], [0, 0], [0, 2, 1], [0, np.nan], [0, np.inf]]:
            with self.subTest(times=times), self.assertRaises(ValueError):
                tinterpol_mxn({'x': times, 'y': np.zeros(len(times))}, [1])
        for options in [dict(method='spline'), dict(method='quadratic'),
                        dict(no_extrapolate=True, nan_extrapolate=True),
                        dict(newname='mxn_test_out', overwrite=True),
                        dict(newname='mxn_test_out', return_data=True)]:
            with self.subTest(options=options), self.assertRaises(ValueError):
                tinterpol_mxn({'x': [0, 1], 'y': [0, 1]}, [0], **options)
        with self.assertRaises(ValueError):
            tinterpol_mxn({'x': [0, 1], 'y': [0]}, [0])
        with self.assertRaises(ValueError):
            tinterpol_mxn('mxn_test_missing', [0])
        with self.assertRaises(TypeError):
            tinterpol_mxn({'x': [0, 1], 'y': ['a', 'b']}, [0])

    def test_invalid_batch_does_not_write(self):
        store_data('mxn_test_a', data={'x': [0, 1], 'y': [0, 1]})
        store_data('mxn_test_b', data={'x': [0, 0], 'y': [0, 1]})
        with self.assertRaises(ValueError):
            tinterpol_mxn(['mxn_test_a', 'mxn_test_b'], [.5], overwrite=True)
        assert_array_equal(get_data('mxn_test_a').y, [0, 1])
        with self.assertRaises(ValueError):
            tinterpol_mxn(['mxn_test_a', 'mxn_test_b'], [.5], newname='mxn_test_out')
        with self.assertRaises(ValueError):
            tinterpol_mxn(['mxn_test_a', 'mxn_test_b'], [.5], return_data=True)


class TinterpolMxnIDLValidation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        override = os.environ.get('PYSPEDAS_TINTERPOL_MXN_CDF')
        if override:
            filename = Path(override).expanduser()
            if not filename.is_file():
                raise FileNotFoundError(f'IDL reference CDF not found: {filename}')
        else:
            filename = download_test_data(
                TESTING_CONFIG['remote_validation_dir'],
                'interpolation_tests',
                'tinterpol_mxn_validate.cdf',
                TESTING_CONFIG['local_testing_dir'],
            )
            if not filename:
                raise unittest.SkipTest('Could not download tinterpol_mxn_validate.cdf')
        cls.addClassCleanup(del_data, 'mxn_idl_*')
        required = ['source', 'target', 'linear', 'nan', 'repeat', 'trim',
                    'source_nan', 'target_nan', 'ignore', 'preserve',
                    'matrix_source', 'matrix_linear', 'matrix_nan',
                    'static_source', 'moving_source', 'static', 'moving',
                    'moving_nan', 'single_source', 'single', 'single_nan']
        # Load the named inputs/results, not standalone dependency variables.
        # cdf_to_tplot still attaches the bins through CDF DEPEND_n attributes.
        del_data('mxn_idl_*')
        cdf_to_tplot(str(filename), varnames=['mxn_idl_' + suffix for suffix in required])
        for suffix in required:
            if get_data('mxn_idl_' + suffix) is None:
                raise AssertionError(f'Missing reference variable mxn_idl_{suffix} in {filename}')

    def tearDown(self):
        del_data('mxn_python_*')

    def assert_matches_idl(self, actual_name, expected_name, bins=False):
        """Compare timestamps, shapes, NaN positions, values and optional bins."""
        actual = get_data(actual_name, dt=True)
        expected = get_data(expected_name, dt=True)
        self.assertIsNotNone(actual)
        self.assertEqual(actual.y.shape, expected.y.shape)
        assert_array_equal(actual.times, expected.times)
        assert_array_equal(np.isnan(actual.y), np.isnan(expected.y))
        assert_allclose(actual.y, expected.y, rtol=1e-12, atol=1e-12, equal_nan=True)
        if bins:
            self.assertEqual(actual.v.shape, expected.v.shape)
            assert_allclose(actual.v, expected.v, rtol=1e-12, atol=1e-12, equal_nan=True)

    def test_linear_extrapolation(self):
        tinterpol_mxn('mxn_idl_source', 'mxn_idl_target', newname='mxn_python_linear')
        self.assert_matches_idl('mxn_python_linear', 'mxn_idl_linear')

    def test_nan_extrapolate(self):
        tinterpol_mxn('mxn_idl_source', 'mxn_idl_target', newname='mxn_python_nan',
                      nan_extrapolate=True)
        self.assert_matches_idl('mxn_python_nan', 'mxn_idl_nan')

    def test_repeat_extrapolate(self):
        tinterpol_mxn('mxn_idl_source', 'mxn_idl_target', newname='mxn_python_repeat',
                      repeat_extrapolate=True)
        self.assert_matches_idl('mxn_python_repeat', 'mxn_idl_repeat')

    def test_no_extrapolate(self):
        tinterpol_mxn('mxn_idl_source', 'mxn_idl_target', newname='mxn_python_trim',
                      no_extrapolate=True)
        self.assert_matches_idl('mxn_python_trim', 'mxn_idl_trim')

    def test_ignore_nans_dictionary_return(self):
        source = get_data('mxn_idl_source_nan', dt=True)
        target = get_data('mxn_idl_target_nan', dt=True)
        # Replicates the IDL structure input and OUT keyword, with no storage.
        result = tinterpol_mxn({'x': source.times, 'y': source.y}, target.times,
                              ignore_nans=True, return_data=True)
        expected = get_data('mxn_idl_ignore', dt=True)
        self.assertEqual(result['y'].shape, expected.y.shape)
        assert_array_equal(result['x'], expected.times)
        assert_allclose(result['y'], expected.y, rtol=1e-12, atol=1e-12, equal_nan=True)

    def test_preserve_nans_documented_exact_sample_difference(self):
        source = get_data('mxn_idl_source_nan', dt=True)
        target = get_data('mxn_idl_target_nan', dt=True)
        result = tinterpol_mxn({'x': source.times, 'y': source.y}, target.times,
                              return_data=True)
        expected = get_data('mxn_idl_preserve', dt=True)
        self.assertEqual(result['y'].shape, expected.y.shape)
        assert_array_equal(result['x'], expected.times)
        # IDL 9.0 produces NaN at the exact valid source sample [0, 0].
        # Check this ONE intentional difference explicitly; compare all others.
        self.assertTrue(np.isnan(expected.y[0, 0]))
        self.assertEqual(result['y'][0, 0], source.y[0, 0])
        assert_allclose(result['y'][0, 1:], expected.y[0, 1:], equal_nan=True)
        assert_allclose(result['y'][1:], expected.y[1:],
                        rtol=1e-12, atol=1e-12, equal_nan=True)

    def test_matrix_linear(self):
        tinterpol_mxn('mxn_idl_matrix_source', 'mxn_idl_target', newname='mxn_python_matrix')
        self.assertEqual(get_data('mxn_python_matrix').y.shape, (5, 3, 3))
        self.assert_matches_idl('mxn_python_matrix', 'mxn_idl_matrix_linear')

    def test_matrix_nan_extrapolate(self):
        tinterpol_mxn('mxn_idl_matrix_source', 'mxn_idl_target', newname='mxn_python_matrix_nan',
                      nan_extrapolate=True)
        self.assert_matches_idl('mxn_python_matrix_nan', 'mxn_idl_matrix_nan')

    def test_static_bins(self):
        tinterpol_mxn('mxn_idl_static_source', 'mxn_idl_target', newname='mxn_python_static')
        self.assert_matches_idl('mxn_python_static', 'mxn_idl_static', bins=True)

    def test_time_dependent_bins(self):
        tinterpol_mxn('mxn_idl_moving_source', 'mxn_idl_target', newname='mxn_python_moving')
        self.assert_matches_idl('mxn_python_moving', 'mxn_idl_moving')
        # Y still matches IDL. Bins deliberately select source maps, whereas
        # IDL linearly interpolates/extrapolates them.
        source = get_data('mxn_idl_moving_source')
        actual = get_data('mxn_python_moving')
        assert_array_equal(actual.v, source.v[[0, 0, 0, 2, 2]])
        assert_allclose(get_data('mxn_idl_moving').v,
                        [[9, 19], [10, 20], [11, 21], [15, 25], [16, 26]])

    def test_time_dependent_bins_nan_extrapolate(self):
        tinterpol_mxn('mxn_idl_moving_source', 'mxn_idl_target', newname='mxn_python_moving_nan',
                      nan_extrapolate=True)
        self.assert_matches_idl('mxn_python_moving_nan', 'mxn_idl_moving_nan')
        source = get_data('mxn_idl_moving_source')
        actual = get_data('mxn_python_moving_nan')
        assert_array_equal(actual.v[1:4], source.v[[0, 0, 2]])
        self.assertTrue(np.isnan(actual.v[[0, 4]]).all())
        assert_allclose(get_data('mxn_idl_moving_nan').v,
                        [[np.nan, np.nan], [10, 20], [11, 21], [15, 25], [np.nan, np.nan]],
                        equal_nan=True)

    def test_singleton(self):
        tinterpol_mxn('mxn_idl_single_source', 'mxn_idl_target', newname='mxn_python_single')
        self.assert_matches_idl('mxn_python_single', 'mxn_idl_single')

    def test_singleton_nan_extrapolate(self):
        tinterpol_mxn('mxn_idl_single_source', 'mxn_idl_target', newname='mxn_python_single_nan',
                      nan_extrapolate=True)
        self.assert_matches_idl('mxn_python_single_nan', 'mxn_idl_single_nan')


if __name__ == '__main__':
    unittest.main()
