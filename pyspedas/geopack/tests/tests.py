import unittest

import numpy as np

from pytplot import data_exists
import pyspedas
from pyspedas import time_double
from pyspedas.geopack import tt89
from pyspedas.geopack import tt96
from pyspedas.geopack import tt01
from pyspedas.geopack import tts04
from pyspedas.geopack.get_tsy_params import get_tsy_params
from pyspedas.geopack.get_w_params import get_w
from pyspedas.geopack import trace_equator_89
from pyspedas.geopack import trace_iono_89
from pyspedas import tinterpol
from pytplot import join_vec, store_data, get_data, tdeflag, del_data

trange = ['2015-10-16', '2015-10-17']

def gen_circle():
    import pytplot
    # Generate a circle at 5 RE in the XZ plane
    angle = np.arange(0.0,361.0, 1.0)
    angle_rad = np.deg2rad(angle)
    y=np.zeros(len(angle_rad),np.float64)
    x=5.0*np.sin(angle_rad)*6371.2
    z=5.0*np.cos(angle_rad)*6371.2
    t=np.zeros(len(angle_rad))
    t[:] = pytplot.time_double('2024-01-01/06:31:00') + np.arange(0.0,361.0,1.0)
    pos=np.zeros((len(angle_rad),3), np.float64)
    pos[:,0] = x
    pos[:,1] = y
    pos[:,2] = z
    pytplot.store_data('circle_magpoles_5re',data={'x':t,'y':pos})
    pytplot.set_coords('circle_magpoles_5re', 'GSM')

def get_params(model, g_variables=None):
    support_trange = [time_double(trange[0])-60*60*24, 
                      time_double(trange[1])+60*60*24]
    pyspedas.kyoto.dst(trange=support_trange)
    pyspedas.projects.omni.data(trange=trange)
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
        mec_vars = pyspedas.projects.mms.mec(trange=trange)
        tt89('mms1_mec_r_gsm', igrf_only=True)
        self.assertTrue(data_exists('mms1_mec_r_gsm_bt89'))

    def test_tt89(self):
        mec_vars = pyspedas.projects.mms.mec(trange=trange)
        tt89('mms1_mec_r_gsm')
        self.assertTrue(data_exists('mms1_mec_r_gsm_bt89'))

    def test_tt96(self):
        mec_vars = pyspedas.projects.mms.mec(trange=trange)
        params = get_params('t96')
        # This interpolation can result in NaNs in the position variable, so they need to be cleaned
        tinterpol('mms1_mec_r_gsm', 'proton_density')
        tdeflag('mms1_mec_r_gsm-itrp',newname='mms1_clean')
        tt96('mms1_clean', parmod=params)
        self.assertTrue(data_exists('mms1_clean_bt96'))

    def test_tt01(self):
        mec_vars = pyspedas.projects.mms.mec(trange=trange)
        params = get_params('t01')
        # This can yield nans in the interpolated position variable for times outside the range of proton_density.
        # We don't want to pass NaNs to any of the geopack routines, so deflag
        tinterpol('mms1_mec_r_gsm', 'proton_density')
        tdeflag('mms1_mec_r_gsm-itrp',newname='mms1_clean')
        # No gvariables passed, defaults to two constants which will be replicated to the correct number of points
        tt01('mms1_clean', parmod=params)
        self.assertTrue(data_exists('mms1_clean_bt01'))
        del_data('mms1_clean_bt01')
        mec = get_data('mms1_clean')
        gvars = np.zeros((len(mec.times), 2))
        # Note that mec.times may now have a different number of points than proton_density!
        gvars[:, 0] = np.repeat(6.0, len(mec.times))
        gvars[:, 1] = np.repeat(10.0, len(mec.times))
        store_data('g_variables', data={'x': mec.times, 'y': gvars})
        params = get_params('t01', g_variables='g_variables')
        # Passing g_variables as tplot variable. It will get interpolated onto the correct number of points.
        tt01('mms1_clean', parmod=params)
        self.assertTrue(data_exists('mms1_clean_bt01'))
        del_data('mms1_clean_bt01')
        # Now we'll pass g_variables as an array. No interpolation will be done, so its size
        # needs to match proton_density, not mms1_clean!
        pd=get_data('proton_density')
        gvars = np.zeros((len(pd.times), 2))
        gvars[:, 0] = np.repeat(6.0, len(pd.times))
        gvars[:, 1] = np.repeat(10.0, len(pd.times))
        params = get_params('t01', g_variables=gvars)
        tt01('mms1_clean', parmod=params)
        self.assertTrue(data_exists('mms1_clean_bt01'))

    def test_tts04(self):
        mec_vars = pyspedas.projects.mms.mec(trange=trange)
        params = get_params('ts04')
        tinterpol('mms1_mec_r_gsm', 'proton_density')
        tts04('mms1_mec_r_gsm-itrp', parmod=params)
        self.assertTrue(data_exists('mms1_mec_r_gsm-itrp_bts04'))

    def test_get_w(self):
        w_vals = get_w(trange=['2015-10-16', '2015-10-17'])

    def test_errors(self):
        # exercise some of the error code
        mec_vars = pyspedas.projects.mms.mec(trange=trange)
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

    def test_t89_equ_n(self):
        trace_equator_89(time_double('2007-03-23/00:00:00'),np.array([-2.0,0.0,1.0]),iopt=3)

    def test_t89_equ_s(self):
        trace_equator_89(time_double('2007-03-23/00:00:00'),np.array([-2.0,0.0,-1.0]),iopt=3)

    def test_t89_iono_n_n(self):
        trace_iono_89(time_double('2007-03-23/00:00:00'), np.array([-2.0,0.0,1.0]),iopt=3)

    def test_t89_iono_n_s(self):
        trace_iono_89(time_double('2007-03-23/00:00:00'), np.array([-2.0,0.0,1.0]),iopt=3,south=True)

    def test_t89_iono_s_n(self):
        trace_iono_89(time_double('2007-03-23/00:00:00'), np.array([-2.0,0.0,-1.0]),iopt=3)
    def test_t89_iono_s_s(self):
        trace_iono_89(time_double('2007-03-23/00:00:00'), np.array([-2.0,0.0,-1.0]),iopt=3, south=True)

    def test_t96_roi(self):
        import pytplot
        gen_circle()
        params = get_params('t96')
        dat=get_data(params)
        circ_dat=get_data('circle_magpoles_5re')
        n=len(circ_dat.times)
        newdat=np.zeros((n,10), np.float64)
        newdat[:,:] = dat.y[0,]
        store_data(params,data={'x':circ_dat.times, 'y':newdat})
        tt96('circle_magpoles_5re', parmod=params)
        #pytplot.tplot(['circle_magpoles_5re','circle_magpoles_5re_bt96'])

    def test_t01_roi(self):
        import pytplot
        gen_circle()
        params = get_params('t01')
        dat=get_data(params)
        circ_dat=get_data('circle_magpoles_5re')
        n=len(circ_dat.times)
        newdat=np.zeros((n,10), np.float64)
        newdat[:,:] = dat.y[0,]
        store_data(params,data={'x':circ_dat.times, 'y':newdat})
        tt01('circle_magpoles_5re', parmod=params)
        #pytplot.tplot(['circle_magpoles_5re','circle_magpoles_5re_bt01'])

    def test_t04_roi(self):
        import pytplot
        gen_circle()
        params = get_params('ts04')
        dat=get_data(params)
        circ_dat=get_data('circle_magpoles_5re')
        n=len(circ_dat.times)
        newdat=np.zeros((n,10), np.float64)
        newdat[:,:] = dat.y[0,]
        store_data(params,data={'x':circ_dat.times, 'y':newdat})
        tts04('circle_magpoles_5re', parmod=params)
        #pytplot.tplot(['circle_magpoles_5re','circle_magpoles_5re_bts04'])

if __name__ == '__main__':
    unittest.main()
