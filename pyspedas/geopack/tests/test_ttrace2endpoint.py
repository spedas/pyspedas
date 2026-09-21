"""Regression tests for incomplete field-line traces (issue #1388)."""

import unittest
from types import SimpleNamespace
from unittest.mock import patch

import numpy as np

from pyspedas import del_data, get_data, store_data, time_double
from pyspedas.geopack import ttrace2endpoint


class TestTraceFootPoints(unittest.TestCase):
    endpoints = ('ionosphere-north', 'ionosphere-south', 'equator')

    def setUp(self):
        store_data('endpoint_start', data={
            'x': [time_double('2015-10-16')], 'y': [[-5., 0., 1.]]})

    def tearDown(self):
        del_data('endpoint_*')

    def trace(self, endpoint, **kwargs):
        ttrace2endpoint(
            'endpoint_start', 'igrf', endpoint, units_in='Re', coord_in='gsm',
            foot_name='endpoint_foot', trace_name='endpoint_trace',
            diag_reached_name='endpoint_reached', **kwargs)

    def test_path_limit_has_nan_foot_point(self):
        for endpoint in self.endpoints:
            for coord, units in [('gsm', 'Re'), ('geo', 'km')]:
                with self.subTest(endpoint=endpoint, coord=coord, units=units):
                    self.trace(endpoint, max_s=0.01,
                               foot_out_coord=coord, foot_out_units=units,
                               bvec_name='endpoint_bvec',
                               diag_npts_name='endpoint_npts')
                    foot = get_data('endpoint_foot').y
                    self.assertEqual(foot.shape, (1, 3))
                    self.assertTrue(np.isnan(foot).all())
                    np.testing.assert_array_equal(get_data('endpoint_reached').y, [0])
                    # The partial trace and field vectors remain useful diagnostics.
                    trace = get_data('endpoint_trace').y
                    self.assertGreater(trace.shape[1], 1)
                    self.assertTrue(np.isfinite(trace).all())
                    self.assertTrue(np.isfinite(get_data('endpoint_bvec').y).all())
                    self.assertEqual(get_data('endpoint_npts').y[0], trace.shape[1])

    def test_completed_trace_keeps_foot_point(self):
        for endpoint in self.endpoints:
            with self.subTest(endpoint=endpoint):
                self.trace(endpoint)
                np.testing.assert_array_equal(get_data('endpoint_reached').y, [1])
                foot = get_data('endpoint_foot').y
                self.assertTrue(np.isfinite(foot).all())
                np.testing.assert_allclose(foot[0], get_data('endpoint_trace').y[0, -1])

    def test_inside_ionosphere_traces_to_conjugate_hemisphere(self):
        boundary_radius = 1.1
        for endpoint, start_z_sign, direction in [
                ('ionosphere-south', 1, -1),
                ('ionosphere-north', -1, 1)]:
            with self.subTest(endpoint=endpoint):
                # Start above Earth's surface, but inside the requested boundary.
                start = 1.01 * np.array([0.6, 0., start_z_sign * 0.8])
                store_data('endpoint_start', data={
                    'x': [time_double('2015-10-16')], 'y': [start]})
                self.assertLess(np.linalg.norm(start), boundary_radius)

                self.trace(endpoint, r_iono_re=boundary_radius, max_step=0.05,
                           bvec_name='endpoint_bvec')
                trace = get_data('endpoint_trace').y[0]
                bvec = get_data('endpoint_bvec').y[0]
                foot = get_data('endpoint_foot').y[0]
                np.testing.assert_array_equal(get_data('endpoint_reached').y, [1])
                self.assertTrue(np.isfinite(trace).all())
                np.testing.assert_allclose(trace[0], start)
                # Ignore the outward crossing and stop at the inward crossing
                # in the conjugate hemisphere, on the specified radius.
                self.assertGreater(np.max(np.linalg.norm(trace, axis=1)), boundary_radius)
                self.assertGreater(direction * np.dot(bvec[0], start), 0.)
                self.assertLess(direction * np.dot(bvec[-1], foot), 0.)
                self.assertLess(start[2] * foot[2], 0.)
                np.testing.assert_allclose(np.linalg.norm(foot), boundary_radius,
                                           rtol=0., atol=1e-8)
                np.testing.assert_allclose(foot, trace[-1])

    def test_unsuccessful_or_empty_trace(self):
        # Unknown failure statuses must not be treated as successful endpoints.
        for status, points in [('bad_B', np.array([[-5., 0., 1.]])),
                               ('max_s', np.empty((0, 3)))]:
            with self.subTest(status=status):
                with patch('pyspedas.geopack.trace_to_event',
                           return_value=(points, status, SimpleNamespace())):
                    ttrace2endpoint(
                        'endpoint_start', 'igrf', 'ionosphere-north',
                        units_in='Re', coord_in='gsm', foot_name='endpoint_foot',
                        diag_reached_name='endpoint_reached')
                self.assertTrue(np.isnan(get_data('endpoint_foot').y).all())
                np.testing.assert_array_equal(get_data('endpoint_reached').y, [0])


if __name__ == '__main__':
    unittest.main()
