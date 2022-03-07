
import os
import unittest
from pyspedas.utilities.data_exists import data_exists
import pyspedas
from pyspedas import time_double
from pyspedas.geopack import tt89
from pyspedas.geopack import tt96
from pyspedas.geopack import tt01
from pyspedas.geopack import tts04
from pyspedas.geopack.get_tsy_params import get_tsy_params
from pyspedas import tinterpol
from pytplot import join_vec

trange = ['2015-10-16', '2015-10-17']

def get_params(model):
    support_trange = [time_double(trange[0])-60*60*24, 
                      time_double(trange[1])+60*60*24]
    pyspedas.kyoto.dst(trange=support_trange)
    pyspedas.omni.data(trange=trange)
    join_vec(['BX_GSE', 'BY_GSM', 'BZ_GSM'])
    return get_tsy_params('kyoto_dst', 
                    'BX_GSE-BY_GSM-BZ_GSM_joined', 
                    'proton_density', 
                    'flow_speed', 
                    model, 
                    pressure_tvar='Pressure',
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

    def test_tts04(self):
        mec_vars = pyspedas.mms.mec(trange=trange)
        params = get_params('ts04')
        tinterpol('mms1_mec_r_gsm', 'proton_density')
        tts04('mms1_mec_r_gsm-itrp', parmod=params)
        self.assertTrue(data_exists('mms1_mec_r_gsm-itrp_bts04'))

if __name__ == '__main__':
    unittest.main()