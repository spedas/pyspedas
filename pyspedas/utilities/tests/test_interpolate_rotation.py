"""Rotation interpolation tests, including the shared IDL baseline CDF."""

from copy import deepcopy
import unittest

import numpy as np
from numpy.testing import assert_allclose, assert_array_equal

from pyspedas import (del_data, get_data, interpolate_rotation, qtom,
                      rotmat_get_coords, rotmat_set_coords, store_data, tvector_rotate)
from pyspedas.tplot_tools import data_quants
from pyspedas.utilities.tests.test_tinterpol_mxn import _reference_cdf


def z_matrices(degrees):
    angles = np.deg2rad(degrees)
    result = np.zeros((len(angles), 3, 3))
    result[:, 0, 0] = result[:, 1, 1] = np.cos(angles)
    result[:, 0, 1] = -np.sin(angles)
    result[:, 1, 0] = np.sin(angles)
    result[:, 2, 2] = 1
    return result


class InterpolateRotationTests(unittest.TestCase):
    def tearDown(self):
        del_data('rot_test_*')

    def test_matrix_midpoint_and_orthogonality(self):
        result = interpolate_rotation({'x': [0, 2], 'y': z_matrices([0, 90])}, [1])
        assert_allclose(result['y'], z_matrices([45]), atol=1e-12)
        assert_allclose(result['y'] @ result['y'].transpose(0, 2, 1), [np.eye(3)], atol=1e-12)
        assert_allclose(np.linalg.det(result['y']), [1])

    def test_left_handed_midpoint(self):
        matrices = z_matrices([0, 90])
        matrices[:, 0, :] *= -1
        expected = z_matrices([45])
        expected[:, 0, :] *= -1
        result = interpolate_rotation({'x': [0, 2], 'y': matrices}, [1])
        assert_allclose(result['y'], expected, atol=1e-12)
        assert_allclose(np.linalg.det(result['y']), [-1])

    def test_agrees_with_tvector_rotate_on_basis_vectors(self):
        target = np.array([-1, 0, .5, 1, 2, 4, 6, 8.])
        for left in [False, True]:
            with self.subTest(left=left):
                # Changing axes exercises quaternion conversion beyond planar rotations.
                quaternions = np.array([[1, 0, 0, 0], [.5, .5, .5, .5], [0, 1, 0, 0]])
                matrices = qtom(quaternions)
                if left:
                    matrices[:, 0, :] *= -1
                store_data('rot_test_matrix', data={'x': [0, 2, 6], 'y': matrices,
                                                   'v1': np.arange(3), 'v2': np.arange(3)})
                rotmat_set_coords('rot_test_matrix', 'A', 'B')
                result = interpolate_rotation('rot_test_matrix', target, return_data=True)
                for axis in range(3):
                    vectors = np.tile(np.eye(3)[axis], (len(target), 1))
                    store_data('rot_test_basis', data={'x': target, 'y': vectors},
                               attr_dict={'data_att': {'coord_sys': 'A'}})
                    tvector_rotate('rot_test_matrix', 'rot_test_basis', newname='rot_test_rotated')
                    assert_allclose(result['y'] @ np.eye(3)[axis], get_data('rot_test_rotated').y,
                                    atol=1e-12)

    def test_matching_matrix_samples_are_exact(self):
        matrices = z_matrices([0, 45, 90])
        matrices[1, 0, 0] += 1e-7  # Accepted roundoff must not be silently repaired at exact times.
        result = interpolate_rotation({'x': [0, 1, 2], 'y': matrices}, [2, 0, 1, 1])
        assert_array_equal(result['y'], matrices[[2, 0, 1, 1]])

    def test_descending_times_and_duplicate_targets(self):
        result = interpolate_rotation({'x': [2, 0], 'y': z_matrices([90, 0])}, [1.5, .5, 1.5])
        assert_allclose(result['y'], z_matrices([67.5, 22.5, 67.5]), atol=1e-12)

    def test_quaternion_signs_and_output_conversion(self):
        source = {'x': [0, 1, 2], 'y': [[1, 0, 0, 0], [-1, 0, 0, 0], [1, 0, 0, 0]]}
        result = interpolate_rotation(source, [0, .5, 1, 1.5, 2])
        assert_allclose(result['y'], np.tile([1, 0, 0, 0], (5, 1)), atol=1e-12)
        result = interpolate_rotation(source, [.5], output='matrix')
        assert_allclose(result['y'], [np.eye(3)], atol=1e-12)
        result = interpolate_rotation({'x': [0, 2], 'y': z_matrices([0, 90])}, [1], output='quaternion')
        assert_allclose(qtom(result['y']), z_matrices([45]), atol=1e-12)

    def test_shortest_path_across_180_degrees(self):
        result = interpolate_rotation({'x': [0, 2], 'y': z_matrices([170, 190])}, [1])
        assert_allclose(result['y'], z_matrices([180]), atol=1e-12)
        result = interpolate_rotation({'x': [0, 2], 'y': z_matrices([0, 180])}, [0, 1, 2])
        assert_allclose(result['y'], z_matrices([0, 90, 180]), atol=1e-12)

    def test_bounds_and_singleton(self):
        source = {'x': [0, 2], 'y': z_matrices([0, 90])}
        result = interpolate_rotation(source, [-1, 1, 3])
        assert_allclose(result['y'], z_matrices([0, 45, 90]), atol=1e-12)
        result = interpolate_rotation(source, [-1, 1, 3], bounds='nan')
        self.assertTrue(np.isnan(result['y'][[0, 2]]).all())
        assert_allclose(result['y'][1], z_matrices([45])[0], atol=1e-12)
        result = interpolate_rotation(source, [-1, 1, 3], bounds='trim')
        assert_allclose(result['y'], z_matrices([45]), atol=1e-12)
        with self.assertRaises(ValueError):
            interpolate_rotation(source, [-1], bounds='raise')
        matrices = z_matrices([30])
        matrices[:, 0, :] *= -1
        result = interpolate_rotation({'x': [1], 'y': matrices}, [-1, 1, 3])
        assert_array_equal(result['y'], np.repeat(matrices, 3, axis=0))
        result = interpolate_rotation({'x': [1], 'y': matrices}, [-1, 1, 3], bounds='nan')
        self.assertTrue(np.isnan(result['y'][[0, 2]]).all())
        assert_array_equal(result['y'][1], matrices[0])

    def test_whole_sample_nan_handling(self):
        matrices = z_matrices([0, 45, 90])
        matrices[1, 0, 0] = np.nan
        source = {'x': [0, 1, 2], 'y': matrices}
        result = interpolate_rotation(source, [0, .5, 1, 1.5, 2])
        self.assertTrue(np.isnan(result['y'][1:4]).all())
        assert_allclose(result['y'][[0, 4]], z_matrices([0, 90]), atol=1e-12)
        result = interpolate_rotation(source, [.5, 1, 1.5], ignore_nans=True)
        assert_allclose(result['y'], z_matrices([22.5, 45, 67.5]), atol=1e-12)

    def test_gap_limits_count_rotations(self):
        matrices = z_matrices([0, 30, 60, 90])
        matrices[1, 0, 0] = matrices[2, 2, 2] = np.nan
        source = {'x': [0, 1, 2, 3], 'y': matrices}
        result = interpolate_rotation(source, [0, 1.5, 3], ignore_nans=True, max_gap_samples=1)
        self.assertTrue(np.isnan(result['y'][1]).all())
        result = interpolate_rotation(source, [1.5], ignore_nans=True,
                                      max_gap_samples=2, max_gap_time=3)
        assert_allclose(result['y'], z_matrices([45]), atol=1e-12)
        result = interpolate_rotation({'x': [0, 3], 'y': z_matrices([0, 90])},
                                      [1.5], max_gap_time=2)
        self.assertTrue(np.isnan(result['y']).all())

    def test_leading_missing_and_all_missing(self):
        source = {'x': [0, 1, 2], 'y': [[np.nan]*4, [1, 0, 0, 0], [np.nan]*4]}
        result = interpolate_rotation(source, [-1, .5, 1, 3], ignore_nans=True)
        assert_allclose(result['y'], np.tile([1, 0, 0, 0], (4, 1)))
        result = interpolate_rotation(source, [-1, .5, 1, 3], ignore_nans=True, bounds='nan')
        self.assertTrue(np.isnan(result['y'][[0, 3]]).all())
        result = interpolate_rotation({'x': [0, 1], 'y': np.full((2, 3, 3), np.nan)}, [.5],
                                      ignore_nans=True)
        self.assertTrue(np.isnan(result['y']).all())

    def test_nanosecond_times(self):
        times = np.datetime64('2020-01-01', 'ns') + np.array([0, 2]) * np.timedelta64(1, 'ns')
        result = interpolate_rotation({'x': times, 'y': z_matrices([0, 90])},
                                      times[:1] + np.timedelta64(1, 'ns'))
        assert_allclose(result['y'], z_matrices([45]), atol=1e-12)

    def test_metadata_naming_and_target_snapshot(self):
        store_data('rot_test_matrix', data={'x': [0, 2], 'y': z_matrices([0, 90]),
                                           'v1': np.arange(3), 'v2': np.arange(3)})
        rotmat_set_coords('rot_test_matrix', 'GSE', 'FAC')
        store_data('rot_test_target', data={'x': [1], 'y': [0]})
        names = interpolate_rotation('rot_test_matrix', 'rot_test_target')
        self.assertEqual(names, ['rot_test_matrix_rot_interp'])
        self.assertEqual(rotmat_get_coords(names[0]), ('GSE', 'FAC'))
        original_metadata = deepcopy(get_data('rot_test_matrix', metadata=True))
        result = interpolate_rotation('rot_test_matrix', [1], return_data=True, output='quaternion')
        result['metadata']['data_att']['input_coord_sys'] = 'changed'
        self.assertEqual(get_data('rot_test_matrix', metadata=True)['data_att'],
                         original_metadata['data_att'])
        names = interpolate_rotation('rot_test_matrix', 'rot_test_target', newname='rot_test_target')
        assert_allclose(get_data(names[0]).y, z_matrices([45]), atol=1e-12)
        names = interpolate_rotation('rot_test_matrix', [1], overwrite=True)
        self.assertEqual(names, ['rot_test_matrix'])
        assert_allclose(get_data(names[0]).y, z_matrices([45]), atol=1e-12)

    def test_batch_is_atomic_on_validation_failure(self):
        store_data('rot_test_a', data={'x': [0, 2], 'y': [[1, 0, 0, 0], [1, 0, 0, 0]]})
        store_data('rot_test_b', data={'x': [0, 2], 'y': [[0, 0, 0, 0], [0, 0, 0, 0]]})
        with self.assertRaises(ValueError):
            interpolate_rotation('rot_test_[ab]', [1], overwrite=True)
        self.assertEqual(len(get_data('rot_test_a').times), 2)
        store_data('rot_test_b', data={'x': [0, 2], 'y': [[1, 0, 0, 0], [1, 0, 0, 0]]})
        names = interpolate_rotation('rot_test_[ab]', [1], suffix='_done')
        self.assertEqual(names, ['rot_test_a_done', 'rot_test_b_done'])

    def test_invalid_rotations(self):
        mixed = z_matrices([0, 90])
        mixed[0, 0, :] *= -1
        for values in [np.ones((2, 3)), np.zeros((2, 4)), np.full((2, 4), np.inf),
                       np.ones((2, 3, 3)), mixed, np.ones((2, 4), dtype=complex)]:
            with self.subTest(shape=values.shape), self.assertRaises((ValueError, TypeError)):
                interpolate_rotation({'x': [0, 1], 'y': values}, [.5])
        left = z_matrices([0])
        left[:, 0, :] *= -1
        with self.assertRaisesRegex(ValueError, 'left-handed'):
            interpolate_rotation({'x': [0], 'y': left}, [0], output='quaternion')
        result = interpolate_rotation({'x': [0], 'y': [[1 + 1e-7, 0, 0, 0]]}, [0])
        assert_array_equal(result['y'], [[1, 0, 0, 0]])

    def test_invalid_times_and_options(self):
        for times in [[0, 0], [0, np.nan], [0, np.inf]]:
            with self.subTest(times=times), self.assertRaises(ValueError):
                interpolate_rotation({'x': times, 'y': z_matrices([0, 90])}, [.5])
        for options in [dict(bounds='extrapolate'), dict(output='vector'), dict(max_gap_time=-1),
                        dict(max_gap_time=True), dict(max_gap_time=np.inf), dict(max_gap_samples=0),
                        dict(max_gap_samples=1.5), dict(max_gap_samples=True),
                        dict(newname='rot_test_out', return_data=True), dict(overwrite=True)]:
            with self.subTest(options=options), self.assertRaises(ValueError):
                interpolate_rotation({'x': [0, 1], 'y': z_matrices([0, 90])}, [.5], **options)

    def test_empty_targets_and_stored_conversion(self):
        result = interpolate_rotation({'x': [0], 'y': z_matrices([0])}, [])
        self.assertEqual(result['y'].shape, (0, 3, 3))
        result = interpolate_rotation({'x': [0], 'y': [[1, 0, 0, 0]]}, [1], bounds='trim')
        self.assertEqual(result['y'].shape, (0, 4))
        names = interpolate_rotation({'x': [0], 'y': [[1, 0, 0, 0]]}, [1],
                                     bounds='trim', newname='rot_test_empty')
        self.assertEqual(names, [])
        self.assertNotIn('rot_test_empty', data_quants)
        names = interpolate_rotation({'x': [0, 2], 'y': [[1, 0, 0, 0], [0, 0, 0, 1]]}, [1],
                                     output='matrix', newname='rot_test_stored')
        self.assertEqual(get_data(names[0]).y.shape, (1, 3, 3))


class InterpolateRotationIDLValidation(unittest.TestCase):
    """Use the single tinterpol_mxn_validate CDF for all interpolation baselines."""

    @classmethod
    def setUpClass(cls):
        from pyspedas import cdf_to_tplot
        filename = _reference_cdf()
        cls.addClassCleanup(del_data, 'rot_idl_*')
        del_data('rot_idl_*')
        required = ['matrix', 'quaternion', 'left', 'single', 'basis0', 'basis1', 'basis2',
                    'right0', 'right1', 'right2', 'left0', 'left1', 'left2',
                    'single0', 'single1', 'single2']
        cdf_to_tplot(str(filename), varnames=['rot_idl_' + suffix for suffix in required])
        for suffix in required:
            if get_data('rot_idl_' + suffix) is None:
                raise AssertionError(f'Missing reference variable rot_idl_{suffix} in {filename}')

    def assert_basis_matches(self, result, prefix):
        for axis in range(3):
            expected = get_data(prefix + str(axis), dt=True)
            assert_array_equal(result['x'], expected.times)
            assert_allclose(result['y'] @ np.eye(3)[axis], expected.y, atol=1e-12, rtol=1e-12)

    def test_right_handed_idl(self):
        result = interpolate_rotation('rot_idl_matrix', 'rot_idl_basis0', return_data=True)
        self.assert_basis_matches(result, 'rot_idl_right')

    def test_left_handed_idl(self):
        result = interpolate_rotation('rot_idl_left', 'rot_idl_basis0', return_data=True)
        self.assert_basis_matches(result, 'rot_idl_left')

    def test_quaternion_idl(self):
        result = interpolate_rotation('rot_idl_quaternion', 'rot_idl_basis0',
                                      output='matrix', return_data=True)
        self.assert_basis_matches(result, 'rot_idl_right')

    def test_singleton_idl(self):
        result = interpolate_rotation('rot_idl_single', 'rot_idl_basis0', return_data=True)
        self.assert_basis_matches(result, 'rot_idl_single')


if __name__ == '__main__':
    unittest.main()
