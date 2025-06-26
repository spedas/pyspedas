"""Tests of waelet tool."""
import pyspedas
from pyspedas import get_data, cdf_to_tplot, tplot, data_exists, tplot_rename, tplot_copy, ylim, zlim, options
import unittest
from numpy.testing import assert_array_almost_equal_nulp, assert_array_max_ulp, assert_allclose
import numpy as np
from pyspedas.analysis.wavelet import wavelet
import logging

global_display = True

class TwaveletDataValidation(unittest.TestCase):
    """ Compares wavelet results between Python and IDL """

    @classmethod
    def setUpClass(cls):
        """
        IDL Data has to be downloaded to perform these tests
        The SPEDAS script that creates the file: general/tools/tplot/wvlt/wavelet_python_validate.pro
        """
        from pyspedas.utilities.download import download
        from pyspedas.projects.themis.config import CONFIG

        # Testing tolerance
        cls.tol = 1e-10

        # Download tplot files
        remote_server = 'https://github.com/spedas/test_data/raw/refs/heads/main/'
        remote_name = 'analysis_tools/wavelet_test.tplot'
        datafile = download(remote_file=remote_name,
                            remote_path=remote_server,
                            local_path=CONFIG['local_data_dir'],
                            no_download=False)
        if not datafile:
            # Skip tests
            raise unittest.SkipTest("Cannot download data validation file")
        # Load validation variables from the test file
        pyspedas.del_data('*')
        filename = datafile[0]
        # pyspedas.cdf_to_tplot(filename)
        pyspedas.tplot_restore(filename)
        pyspedas.tplot_names()

        # Test 1: simple sine waves
        cls.sin_wav = pyspedas.get_data('sin_wav')
        cls.sin_wav_wv_pow = pyspedas.get_data('sin_wav_wv_pow')

        # Test 2: Vassilis homework example using THEMIS FGM data
        cls.tha_fgs_fac_bp_x = pyspedas.get_data('tha_fgs_fac_bp_x')
        cls.tha_fgs_fac_bp_y = pyspedas.get_data('tha_fgs_fac_bp_y')
        cls.tha_fgs_fac_bp_z = pyspedas.get_data('tha_fgs_fac_bp_z')
        cls.tha_fgs_fac_bp_x_wv_pow = pyspedas.get_data('tha_fgs_fac_bp_x_wv_pow')
        cls.tha_fgs_fac_bp_y_wv_pow = pyspedas.get_data('tha_fgs_fac_bp_y_wv_pow')
        cls.tha_fgs_fac_bp_z_wv_pow = pyspedas.get_data('tha_fgs_fac_bp_z_wv_pow')

        tplot_rename('sin_wav_wv_pow', 'idl_sin_wav_wv_pow')

        zlim('tha_fgs_fac_bp_?_wv_pow', 1.0e-1,1.0e2)
        ylim('tha_fgs_fac_bp_?_wv_pow', 1.0e-3,4.1e-2)
        options('tha_fgs_fac_bp_?_wv_pow', 'zlog', True)
        options('tha_fgs_fac_bp_?_wv_pow', 'ylog', False)

        tplot_rename('tha_fgs_fac_bp_x_wv_pow', 'idl_fgs_fac_bp_x_wv_pow')
        tplot_rename('tha_fgs_fac_bp_y_wv_pow', 'idl_fgs_fac_bp_y_wv_pow')
        tplot_rename('tha_fgs_fac_bp_z_wv_pow', 'idl_fgs_fac_bp_z_wv_pow')


    def setUp(self):
        """ We need to clean tplot variables before each run"""
        # pyspedas.del_data('*')

    def test_sin_wav(self):
        # The default is 'morl' rather than 'cmorl0.5-1.0, but it doesn't appear to make that much difference.
        # cmorl0.5-1.0 is what Eric used in the wiki example.
        wavelet('sin_wav',wavename='cmorl0.5-1.0')
        pvar='sin_wav_pow'
        pyspedas.options(pvar, 'colormap', 'jet')
        pyspedas.ylim(pvar, 0.001, 0.1)
        pyspedas.options(pvar, 'ylog', True)
        pyspedas.options(pvar, 'ytitle', pvar)
        d=get_data('sin_wav_pow')
        print(f"Python frequencies: bin count {d.y.shape[1]}, min {np.min(d.v)}, max: {np.max(d.v)}" )
        print(f"Python power: min {np.min(d.y)}, max {np.max(d.y)}")
        d_idl = get_data('idl_sin_wav_wv_pow')
        print(f"IDL frequencies: bin count {d_idl.y.shape[1]}, min {np.min(d_idl.v)}, max: {np.max(d_idl.v)}" )
        print(f"IDL power: min {np.min(d_idl.y)}, max {np.max(d_idl.y)}")
        tplot(['sin_wav', 'sin_wav_pow', 'idl_sin_wav_wv_pow'])

    def test_themis_fgm_wavelet(self):
        pyspedas.wavelet('tha_fgs_fac_bp_x')
        pyspedas.wavelet('tha_fgs_fac_bp_y')
        pyspedas.wavelet('tha_fgs_fac_bp_z')

        zlim('tha_fgs_fac_bp_?_pow', 1.0e-1,1.0e2)
        ylim('tha_fgs_fac_bp_?_pow', 1.0e-3,4.1e-2)
        options('tha_fgs_fac_bp_?_pow', 'zlog', True)
        options('tha_fgs_fac_bp_?_pow', 'ylog', False)
        d=get_data('tha_fgs_fac_bp_x_pow')
        print(f"Python frequencies: bin count {d.y.shape[1]}, min {np.min(d.v)}, max: {np.max(d.v)}" )
        print(f"Python power: min {np.min(d.y)}, max {np.max(d.y)}")
        d_idl=get_data('idl_fgs_fac_bp_x_wv_pow')
        print(f"IDL frequencies: bin count {d_idl.y.shape[1]}, min {np.min(d_idl.v)}, max: {np.max(d_idl.v)}" )
        print(f"IDL power: min {np.min(d_idl.y)}, max {np.max(d_idl.y)}")

        tplot(['tha_fgs_fac_bp_x_pow', 'idl_fgs_fac_bp_x_wv_pow'])

if __name__ == '__main__':
    unittest.main()
