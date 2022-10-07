import unittest

import numpy as np

from pyspedas.utilities.data_exists import data_exists
import pyspedas
from pyspedas import time_double
from pyspedas.geopack import tt89
from pyspedas.geopack import tt96
from pyspedas.geopack import tt01
from pyspedas.geopack import tts04
from pyspedas.geopack.get_tsy_params import get_tsy_params
from pyspedas.geopack.get_w_params import get_w
from pyspedas import tinterpol
from pytplot import join_vec, store_data, get_data

trange = ['2015-10-16', '2015-10-17']


def get_params(model, g_variables=None):
    support_trange = [time_double(trange[0])-60*60*24, 
                      time_double(trange[1])+60*60*24]
    pyspedas.kyoto.dst(trange=support_trange)
    pyspedas.omni.data(trange=trange)
    join_vec(['BX_GSE', 'BY_GSM', 'BZ_GSM'])
    if model == 't01' and g_variables is None:
        g_variables = [6.0, 10.0]
    else:
        if g_variables is not None:
            if not isinstance(g_variables, str) and not isinstance(g_variables, np.ndarray):
                g_variables = None
    return get_tsy_params('kyoto_dst',
                    'BX_GSE-BY_GSM-BZ_GSM_joined',
                    'proton_density',
                    'flow_speed',
                    model,
                    pressure_tvar='Pressure',
                    g_variables=g_variables,
                    speed=True)


class LoadTestCases(unittest.TestCase):
    def test_igrf(self):
        mec_vars = pyspedas.mms.mec(trange=trange)
        tt89('mms1_mec_r_gsm', igrf_only=True)
        self.assertTrue(data_exists('mms1_mec_r_gsm_bt89'))

    def test_tt89(self):
        mec_vars = pyspedas.mms.mec(trange=trange)
        tt89('mms1_mec_r_gsm')
        self.assertTrue(data_exists('mms1_mec_r_gsm_bt89'))

    def test_tt96(self):
        mec_vars = pyspedas.mms.mec(trange=trange)
        params = get_params('t96')
        tinterpol('mms1_mec_r_gsm', 'proton_density')
        tt96('mms1_mec_r_gsm-itrp', parmod=params)
        self.assertTrue(data_exists('mms1_mec_r_gsm-itrp_bt96'))

    def test_tt01(self):
        mec_vars = pyspedas.mms.mec(trange=trange)
        params = get_params('t01')
        tinterpol('mms1_mec_r_gsm', 'proton_density')
        tt01('mms1_mec_r_gsm-itrp', parmod=params)
        self.assertTrue(data_exists('mms1_mec_r_gsm-itrp_bt01'))
        mec = get_data('mms1_mec_r_gsm-itrp')
        gvars = np.zeros((len(mec.times), 2))
        gvars[:, 0] = np.repeat(6.0, len(mec.times))
        gvars[:, 1] = np.repeat(10.0, len(mec.times))
        store_data('g_variables', data={'x': mec.times, 'y': gvars})
        params = get_params('t01', g_variables='g_variables')
        tt01('mms1_mec_r_gsm-itrp', parmod=params)
        self.assertTrue(data_exists('mms1_mec_r_gsm-itrp_bt01'))
        params = get_params('t01', g_variables=gvars)
        tt01('mms1_mec_r_gsm-itrp', parmod=params)
        self.assertTrue(data_exists('mms1_mec_r_gsm-itrp_bt01'))

    def test_tts04(self):
        mec_vars = pyspedas.mms.mec(trange=trange)
        params = get_params('ts04')
        tinterpol('mms1_mec_r_gsm', 'proton_density')
        tts04('mms1_mec_r_gsm-itrp', parmod=params)
        self.assertTrue(data_exists('mms1_mec_r_gsm-itrp_bts04'))

    def test_get_w(self):
        w_vals = get_w(trange=['2015-10-16', '2015-10-17'])

    def test_errors(self):
        # exercise some of the error code
        mec_vars = pyspedas.mms.mec(trange=trange)
        params = get_params('ts04')
        tinterpol('mms1_mec_r_gsm', 'proton_density')
        tts04('var_doesnt_exist')
        tts04('mms1_mec_r_gsm-itrp', parmod=None)
        tt01('var_doesnt_exist')
        tt01('mms1_mec_r_gsm-itrp', parmod=None)
        tt96('var_doesnt_exist')
        tt96('mms1_mec_r_gsm-itrp', parmod=None)
        tt89('var_doesnt_exist')
        invalidmodel = get_params('89')
        invalidg = get_params('t01', g_variables=1)
        invalidg = get_params('t01', g_variables='g_vars')
        notrange = get_w()  # no trange
        invalidtrange = get_w(trange=['2050-01-01', '2050-01-02'])


if __name__ == '__main__':
    unittest.main()
