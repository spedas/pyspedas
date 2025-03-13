import unittest

import numpy as np
from geopack import geopack

from pytplot import data_exists,del_data,cdf_to_tplot,tplot,subtract,tlimit
import pyspedas
from pyspedas import time_double
from pyspedas.geopack import tt89
from pyspedas.geopack import tt96
from pyspedas.geopack import tt01
from pyspedas.geopack import tts04
from pyspedas.geopack.get_tsy_params import get_tsy_params
from pyspedas.geopack.get_w_params import get_w
from pyspedas import tinterpol, tvectot
from pytplot import join_vec, store_data, get_data, tkm2re, tplot_names

from numpy.testing import assert_array_almost_equal_nulp, assert_array_max_ulp, assert_allclose


trange = ['2015-10-16', '2015-10-17']

display=False

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


class LoadGeopackIdlValidationTestCases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        IDL Data has to be downloaded to perform these tests
        The SPEDAS script that creates the file: projects/themis/state/cotrans/thm_cotrans_validate.pro
        """
        from pyspedas.utilities.download import download
        from pyspedas.projects.themis.config import CONFIG

        # Testing time range
        cls.t = ['2008-03-23', '2008-03-28']

        # Testing tolerance
        cls.tol = 1e-10

        # Download tplot files
        remote_server = 'https://github.com/spedas/test_data/raw/refs/heads/main/'
        remote_name = 'analysis_tools/geopack_idl_validate.cdf'

        datafile = download(remote_file=remote_name,
                            remote_path=remote_server,
                            local_path=CONFIG['local_data_dir'],
                            no_download=False)
        if not datafile:
            # Skip tests
            raise unittest.SkipTest("Cannot download data validation file")

        del_data('*')
        filename = datafile[0]
        cdf_to_tplot(filename)
        # Input parameters
        cls.iopt=3
        cls.kp=2.0
        cls.pdyn = 2.0
        cls.dsti = -30.0
        cls.yimf = 0.0
        cls.zimf = -5.0
        cls.g1 = 6.0
        cls.g2 = 10.0
        cls.w1 = 8.0
        cls.w2 = 5.0
        cls.w3 = 9.5
        cls.w4 = 30.0
        cls.w5 = 18.5
        cls.w6 = 60.0

    def test_tilt(self):
        tilt_times,tilt_vals = get_data('bt89_tilt')
        py_tilt_vals=np.zeros(len(tilt_times))
        for idx,t in enumerate(tilt_times):
            py_tilt_vals[idx] = np.degrees(geopack.recalc(t))
        store_data('py_tilt',data={'x':tilt_times,'y':py_tilt_vals})
        idl_tilt = get_data('bt89_tilt')
        py_tilt = get_data('py_tilt')
        assert_allclose(idl_tilt.y, py_tilt.y, atol=.0003)

    def test_igrf(self):
        tt89('tha_state_pos_gsm', igrf_only=True)
        py_b = get_data('tha_state_pos_gsm_bt89')
        idl_b = get_data('bt89_igrf')
        assert_allclose(py_b.y, idl_b.y, rtol = .001, atol=1.0)

    def test_tt89(self):
        tt89('tha_state_pos_gsm')
        py_b = get_data('tha_state_pos_gsm_bt89')
        idl_b = get_data('bt89')
        assert_allclose(py_b.y, idl_b.y, rtol=.001, atol=0.5)

    def test_tt96(self):
        tv_pos=get_data('tha_state_pos_gsm')
        t1=tv_pos.times[0]
        t2=tv_pos.times[-1]
        params = np.zeros([2,10])
        params[:,0] = self.pdyn
        params[:,1] = self.dsti
        params[:,2] = self.yimf
        params[:,3] = self.zimf
        store_data('parmod',data={'x':[t1,t2],'y':params})
        tinterpol('parmod','tha_state_pos_gsm',method='nearest',newname='parmod_interp')
        tt96('tha_state_pos_gsm', parmod='parmod_interp')
        tkm2re('tha_state_pos_gsm')
        tvectot('tha_state_pos_gsm_re',join_component=True)
        py_b = get_data('tha_state_pos_gsm_bt96')
        idl_b = get_data('bt96')
        subtract('bt96','tha_state_pos_gsm_bt96','bt96_diff')
        tplot(['bt96','tha_state_pos_gsm_bt96','bt96_diff','tha_state_pos_gsm_re_tot'], display=display, save_png='t96_diffs')
        tlimit(['2007-03-23/15:00','2007-03-23/17:00'])
        tplot(['bt96','tha_state_pos_gsm_bt96','bt96_diff','tha_state_pos_gsm_re_tot'], display=display)
        tlimit(full=True)
        assert_allclose(py_b.y, idl_b.y, rtol=.001, atol=0.5)

    def test_tt96_circ(self):
        tv_pos=get_data('circle_magpoles_5re_km')
        t1=tv_pos.times[0]
        t2=tv_pos.times[-1]
        params = np.zeros([2,10])
        params[:,0] = self.pdyn
        params[:,1] = self.dsti
        params[:,2] = self.yimf
        params[:,3] = self.zimf
        store_data('parmod',data={'x':[t1,t2],'y':params})
        tinterpol('parmod','circle_magpoles_5re',method='nearest',newname='parmod_interp')
        tt96('circle_magpoles_5re_km', parmod='parmod_interp')
        #tkm2re('tha_state_pos_gsm')
        #tvectot('tha_state_pos_gsm_re',join_component=True)
        py_b = get_data('circle_magpoles_5re_km_bt96')
        idl_b = get_data('tst5re_bt96')
        subtract('tst5re_bt96','circle_magpoles_5re_km_bt96','bt96_diff')
        tplot(['tst5re_bt96','circle_magpoles_5re_km_bt96','bt96_diff'], display=display, save_png='circ_t96_diffs')
        #tlimit(['2007-03-23/15:00','2007-03-23/17:00'])
        #tplot(['bt96','tha_state_pos_gsm_bt96','bt96_diff','tha_state_pos_gsm_re_tot'], display=display)
        tlimit(full=True)
        assert_allclose(py_b.y, idl_b.y, rtol=.001, atol=0.5)


    def test_tt01(self):
        tv_pos=get_data('tha_state_pos_gsm')
        t1=tv_pos.times[0]
        t2=tv_pos.times[-1]
        params = np.zeros([2,10])
        params[:,0] = self.pdyn
        params[:,1] = self.dsti
        params[:,2] = self.yimf
        params[:,3] = self.zimf
        params[:,4] = self.g1
        params[:,5] = self.g2
        store_data('parmod',data={'x':[t1,t2],'y':params})
        tinterpol('parmod', 'tha_state_pos_gsm', method='nearest',newname='parmod_interp')
        tt01('tha_state_pos_gsm', parmod='parmod_interp')
        py_b = get_data('tha_state_pos_gsm_bt01')
        idl_b = get_data('bt01')
        subtract('bt01','tha_state_pos_gsm_bt01','bt01_diff')
        tkm2re('tha_state_pos_gsm')
        tvectot('tha_state_pos_gsm_re',join_component=True)
        tplot(['bt01','tha_state_pos_gsm_bt01','bt01_diff','tha_state_pos_gsm_re_tot'], display=display,save_png='t01_diffs')
        assert_allclose(py_b.y, idl_b.y, rtol=.001, atol=0.5)

    def test_tt01_circ(self):
        tv_pos=get_data('circle_magpoles_5re_km')
        t1=tv_pos.times[0]
        t2=tv_pos.times[-1]
        params = np.zeros([2,10])
        params[:,0] = self.pdyn
        params[:,1] = self.dsti
        params[:,2] = self.yimf
        params[:,3] = self.zimf
        params[:,4] = self.g1
        params[:,5] = self.g2
        store_data('parmod',data={'x':[t1,t2],'y':params})
        tinterpol('parmod', 'circle_magpoles_5re_km', method='nearest',newname='parmod_interp')
        tt01('circle_magpoles_5re_km', parmod='parmod_interp')
        py_b = get_data('circle_magpoles_5re_km_bt01')
        idl_b = get_data('tst5re_bt01')
        subtract('tst5re_bt01','circle_magpoles_5re_km_bt01','bt01_diff')
        #tkm2re('tha_state_pos_gsm')
        #tvectot('tha_state_pos_gsm_re',join_component=True)
        tplot(['tst5re_bt01','circle_magpoles_5re_km_bt01','bt01_diff'], display=display,save_png='circ_t01_diffs')
        assert_allclose(py_b.y, idl_b.y, rtol=.001, atol=0.5)



    def test_tts04(self):
        tv_pos=get_data('tha_state_pos_gsm')
        t1=tv_pos.times[0]
        t2=tv_pos.times[-1]
        params = np.zeros([2,10])
        params[:,0] = self.pdyn
        params[:,1] = self.dsti
        params[:,2] = self.yimf
        params[:,3] = self.zimf
        params[:,4] = self.w1
        params[:,5] = self.w2
        params[:,6] = self.w3
        params[:,7] = self.w4
        params[:,8] = self.w5
        params[:,9] = self.w6
        store_data('parmod',data={'x':[t1,t2],'y':params})
        tinterpol('parmod', 'tha_state_pos_gsm', method='nearest',newname='parmod_interp')
        tts04('tha_state_pos_gsm', parmod='parmod_interp')
        py_b = get_data('tha_state_pos_gsm_bts04')
        idl_b = get_data('bts04')
        subtract('bts04','tha_state_pos_gsm_bts04','bts04_diff')
        tplot(['bts04','tha_state_pos_gsm_bts04','bts04_diff'], display=display, save_png='ts04_diffs')
        assert_allclose(py_b.y, idl_b.y, rtol=.001, atol=0.5)

    def test_circ_tts04(self):
        tv_pos=get_data('circle_magpoles_5re_km')
        t1=tv_pos.times[0]
        t2=tv_pos.times[-1]
        params = np.zeros([2,10])
        params[:,0] = self.pdyn
        params[:,1] = self.dsti
        params[:,2] = self.yimf
        params[:,3] = self.zimf
        params[:,4] = self.w1
        params[:,5] = self.w2
        params[:,6] = self.w3
        params[:,7] = self.w4
        params[:,8] = self.w5
        params[:,9] = self.w6
        store_data('parmod',data={'x':[t1,t2],'y':params})
        tinterpol('parmod', 'circle_magpoles_5re_km', method='nearest',newname='parmod_interp')
        tts04('circle_magpoles_5re_km', parmod='parmod_interp')
        py_b = get_data('circle_magpoles_5re_km_bts04')
        idl_b = get_data('tst5re_bts04')
        subtract('tst5re_bts04','circle_magpoles_5re_km_bts04','bts04_diff')
        tplot(['tst5re_bts04','circle_magpoles_5re_km_bts04','bts04_diff'], display=display, save_png='circ_ts04_diffs')
        assert_allclose(py_b.y, idl_b.y, rtol=.001, atol=0.5)


if __name__ == '__main__':
    unittest.main()
