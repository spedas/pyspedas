import unittest

import numpy as np
from numpy.testing import assert_allclose

import pyspedas
from pyspedas import (
    data_exists,
    time_double,
    tinterpol,
    join_vec,
    store_data,
    get_data,
    tdeflag,
    del_data,
    set_coords,
)
from pyspedas.geopack import tt89, tt96, tt01, tts04, tigrf
from pyspedas.geopack.get_tsy_params import get_tsy_params
from pyspedas.geopack.get_w_params import get_w

trange = ["2015-10-16", "2015-10-17"]

from pyspedas.geopack import clean_model_parameters, clean_parmod_data

class LoadTestCases(unittest.TestCase):
    def test_bad_inputs(self):
        input_times=np.array([10.0, 20.0, 30.0, 40.0, 50.0])
        param_times1= np.array([20.0, 30.0, 40.0,50.0, 60.0])
        param_vals1 = np.array([20.0, 30.0, 40.0, 50.0, 60.0])
        param_times2 = np.array([0.0, 10.0, 20.0, 30.0])
        param_vals2 = np.array([0.0, 10.0, 20.0, 30.0])

        store_data('param_tvar1', data={'x':param_times1, 'y':param_vals1})
        store_data('param_tvar2', data={'x':param_times2, 'y':param_vals2})

        got_exception = False
        try:
            out_array = clean_model_parameters(input_times, None)
        except ValueError:
            got_exception = True
        self.assertTrue(got_exception)

        got_exception = False
        try:
            out_array = clean_model_parameters(input_times, 'foo')
        except ValueError:
            got_exception = True
        self.assertTrue(got_exception)

        got_exception = False
        try:
            out_array = clean_model_parameters(input_times, np.nan)
        except ValueError:
            got_exception = True
        self.assertTrue(got_exception)

        got_exception = False
        try:
            out_array = clean_model_parameters(input_times, [11.0,12.0,13.0])
        except ValueError:
            got_exception = True
        self.assertTrue(got_exception)

        got_exception = False
        try:
            out_array = clean_model_parameters(input_times, [[11.0, 12.0, 13.0, 14.0, 15.0]])
        except ValueError as e:
            got_exception = True
        self.assertTrue(got_exception)

        got_exception = False
        try:
            out_array = clean_model_parameters(input_times, [11.0, 12.0, np.nan, 14.0, 15.0])
        except ValueError as e:
            got_exception = True
        self.assertTrue(got_exception)

        got_exception = False
        try:
            out_array = clean_model_parameters(input_times, ['foo', 'bar','baz', 'quux', 'fnord'])
        except ValueError:
            got_exception = True
        self.assertTrue(got_exception)

        got_exception = False
        try:
            out_array = clean_model_parameters(input_times, np.array([11.0,12.0,13.0]))
        except ValueError:
            got_exception = True
        self.assertTrue(got_exception)

        got_exception = False
        try:
            out_array = clean_model_parameters(input_times, np.array([[11.0, 12.0, 13.0, 14.0, 15.0]]))
        except ValueError as e:
            got_exception = True
        self.assertTrue(got_exception)

        got_exception = False
        try:
            out_array = clean_model_parameters(input_times, np.array(['foo', 'bar','baz', 'quux', 'fnord']))
        except ValueError:
            got_exception = True
        self.assertTrue(got_exception)

        got_exception = False
        try:
            out_array = clean_model_parameters(input_times, np.array([11.0, 12.0, np.nan, 14.0, 15.0]))
        except ValueError as e:
            got_exception = True
        self.assertTrue(got_exception)

        got_exception = False
        try:
            out_array = clean_model_parameters(input_times, 'param_tvar1')
        except ValueError as e:
            got_exception = True
        self.assertTrue(got_exception)

        got_exception = False
        try:
            out_array = clean_model_parameters(input_times, 'param_tvar2')
        except ValueError as e:
            got_exception = True
        self.assertTrue(got_exception)

    def test_clean_parmod_errors(self):
        input_times=np.array([10.0, 20.0, 30.0, 40.0, 50.0])

        got_exception = False
        try:
            out_array = clean_parmod_data(input_times, 'nonexistent')
        except ValueError as e:
            got_exception = True
        self.assertTrue(got_exception)

        parmod_times = np.array([5.0, 15.0, 25.0, 35.0, 45.0, 55.0])
        parmod_data = np.zeros((6,9))
        store_data('parmod_baddata', data={'x':parmod_times, 'y':parmod_data})

        got_exception = False
        try:
            out_array = clean_parmod_data(input_times, 'parmod_baddata')
        except ValueError as e:
            got_exception = True
        self.assertTrue(got_exception)

        parmod_times = np.array([15.0, 25.0, 35.0, 45.0, 55.0])
        parmod_data = np.zeros((5,10))
        store_data('parmod_badstart', data={'x':parmod_times, 'y':parmod_data})
        parmod_times = np.array([5.0, 15.0, 25.0, 35.0, 45.0])
        store_data('parmod_badend', data={'x':parmod_times, 'y':parmod_data})

        got_exception = False
        try:
            out_array = clean_parmod_data(input_times, 'parmod_badstart')
        except ValueError as e:
            got_exception = True
        self.assertTrue(got_exception)

        got_exception = False
        try:
            out_array = clean_parmod_data(input_times, 'parmod_badend')
        except ValueError as e:
            got_exception = True
        self.assertTrue(got_exception)

    def test_clean_parmod_data(self):
        input_times=np.array([10.0, 20.0, 30.0, 40.0, 50.0])
        parmod_times = np.array([5.0, 15.0, 25.0, 35.0, 45.0, 55.0])
        parmod_data = np.zeros((6,10))
        parmod_data[0,:] = 5.0
        parmod_data[1,:] = 15.0
        parmod_data[2,:] = 25.0
        parmod_data[3,:] = np.nan
        parmod_data[4,:] = 45.0
        parmod_data[5,:] = 55.0
        store_data('parmod_vals', data={'x':parmod_times, 'y':parmod_data})
        parmod_out = clean_parmod_data(input_times, 'parmod_vals')
        assert_allclose(parmod_out[:,0], input_times)
        assert_allclose(parmod_out[:,9], input_times)


    def test_scalar(self):
        input_times=np.array([10.0, 20.0, 30.0, 40.0, 50.0])
        params = clean_model_parameters(input_times, 1.0)
        assert_allclose(params,[1.0, 1.0, 1.0, 1.0, 1.0])

    def test_list(self):
        input_times=np.array([10.0, 20.0, 30.0, 40.0, 50.0])
        params = clean_model_parameters(input_times, [1.0, 2.0, 3.0, 4.0, 5.0])
        assert_allclose(params,[1.0, 2.0, 3.0, 4.0, 5.0])
        self.assertTrue(isinstance(params, np.ndarray))

    def test_ndarray(self):
        input_times=np.array([10.0, 20.0, 30.0, 40.0, 50.0])
        params = clean_model_parameters(input_times, np.array([1.0, 2.0, 3.0, 4.0, 5.0]))
        assert_allclose(params,[1.0, 2.0, 3.0, 4.0, 5.0])
        self.assertTrue(isinstance(params, np.ndarray))

    def test_tvar(self):
        input_times=np.array([10.0, 20.0, 30.0, 40.0, 50.0])
        tvar_times = np.array([0.0, 100.0, 200.0])
        tvar_vals = np.array([0.0, np.nan, 200.0])
        store_data('param_tvar1', data={'x':tvar_times, 'y':tvar_vals})
        params = clean_model_parameters(input_times, 'param_tvar1')
        assert_allclose(params,[10.0, 20.0, 30.0, 40.0, 50.0])

if __name__ == "__main__":
    unittest.main()
