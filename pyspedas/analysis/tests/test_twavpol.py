"""Tests of twavpol functions."""
import pyspedas
from pyspedas import get_data, cdf_to_tplot, tplot, data_exists, tplot_rename, tplot_copy
import unittest
from numpy.testing import assert_array_almost_equal_nulp, assert_array_max_ulp, assert_allclose
import numpy as np
from pyspedas.analysis.twavpol import twavpol
import logging

global_display = False

class TwavpolDataValidation(unittest.TestCase):
    """ Compares cotrans results between Python and IDL """

    @classmethod
    def setUpClass(cls):
        """
        IDL Data has to be downloaded to perform these tests
        The SPEDAS script that creates the file: projects/themis/state/cotrans/thm_cotrans_validate.pro
        """
        from pyspedas.utilities.download import download
        from pyspedas.projects.themis.config import CONFIG

        # Numpy diagnostic info
        print("Numpy pocketfft:")
        print(np.fft._pocketfft)
        print("Numpy config:")
        print(np.__config__.show())
        print("Numpy CPU features:")
        print(np._core._multiarray_umath.__cpu_features__)

        # Testing tolerance
        cls.tol = 1e-10

        # Download tplot files
        remote_server = 'https://github.com/spedas/test_data/raw/refs/heads/main/'
        # remote_name = 'testfiles/thm_cotrans_validate.cdf'
        remote_name = 'analysis_tools/thc_twavpol_validate.tplot'
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
        #pyspedas.tplot('thc_scf_fac')
        #pyspedas.tplot('thc_scf_fac_powspec')
        #pyspedas.tplot('thc_scf_fac')
        cls.thc_scf_fac = pyspedas.get_data('thc_scf_fac')
        cls.thc_scf_fac_attr = pyspedas.get_data('thc_scf_fac',metadata=True)
        cls.thc_scf_fac_powspec = pyspedas.get_data('thc_scf_fac_powspec')
        cls.thc_scf_fac_powspec_attr = pyspedas.get_data('thc_scf_fac_powspec',metadata=True)
        cls.thc_scf_fac_degpol = pyspedas.get_data('thc_scf_fac_degpol')
        cls.thc_scf_fac_waveangle = pyspedas.get_data('thc_scf_fac_waveangle')
        cls.thc_scf_fac_elliptict = pyspedas.get_data('thc_scf_fac_elliptict')
        cls.thc_scf_fac_helict = pyspedas.get_data('thc_scf_fac_helict')

        tplot_copy('thc_scf_fac', 'idl_thc_scf_fac')
        tplot_rename('thc_scf_fac_powspec', 'idl_thc_scf_fac_powspec')
        tplot_rename('thc_scf_fac_degpol', 'idl_thc_scf_fac_degpol')
        tplot_rename('thc_scf_fac_waveangle', 'idl_thc_scf_fac_waveangle')
        tplot_rename('thc_scf_fac_elliptict', 'idl_thc_scf_fac_elliptict')
        tplot_rename('thc_scf_fac_helict', 'idl_thc_scf_fac_helict')

        twavpol('thc_scf_fac')



    def setUp(self):
        """ We need to clean tplot variables before each run"""
        # pyspedas.del_data('*')

    def test_powspec(self):
        """ Validate twavpol power spectrum output """

        py_powspec = get_data('thc_scf_fac_powspec')
        logging.info("nanmin/nanmax of powspec: %f %f ",np.nanmin(py_powspec.y),np.nanmax(py_powspec.y))
        assert_allclose(py_powspec.times,self.thc_scf_fac_powspec.times,atol=1.0e-06)
        assert_allclose(py_powspec.y, self.thc_scf_fac_powspec.y, atol=1.0e-06,rtol=1.0e-06)
        tplot(['thc_scf_fac_powspec', 'idl_thc_scf_fac_powspec'] ,display=global_display, save_png='powspec.png' )

    def test_degpol(self):
        """ Validate twavpol degpol output """

        py_degpol = pyspedas.get_data('thc_scf_fac_degpol')
        logging.info("nanmin/nanmax of degpol: %f %f ",np.nanmin(py_degpol.y),np.nanmax(py_degpol.y))
        assert_allclose(py_degpol.times,self.thc_scf_fac_degpol.times,atol=1.0e-06)
        assert_allclose(py_degpol.y, self.thc_scf_fac_degpol.y, atol=1.0e-06,rtol=1.0e-06)
        tplot(['thc_scf_fac_degpol', 'idl_thc_scf_fac_degpol'] ,display=global_display, save_png='degpol.png' )


    def test_waveangle(self):
        """ Validate twavpol waveangle output """

        py_waveangle = pyspedas.get_data('thc_scf_fac_waveangle')
        logging.info("nanmin/nanmax of waveangle: %f %f ",np.nanmin(py_waveangle.y),np.nanmax(py_waveangle.y))
        assert_allclose(py_waveangle.times,self.thc_scf_fac_waveangle.times,atol=1.0e-05)
        assert_allclose(py_waveangle.y, self.thc_scf_fac_waveangle.y, atol=1.0e-05,rtol=1.0e-06)
        tplot(['thc_scf_fac_waveangle', 'idl_thc_scf_fac_waveangle'], display=global_display, save_png='waveangle.png')

    def test_elliptict(self):
        """ Validate twavpol elliptict output """

        py_elliptict = pyspedas.get_data('thc_scf_fac_elliptict')
        logging.info("nanmin/nanmax of elliptict: %f %f ",np.nanmin(py_elliptict.y),np.nanmax(py_elliptict.y))
        assert_allclose(py_elliptict.times,self.thc_scf_fac_elliptict.times,atol=1.0e-06)
        assert_allclose(py_elliptict.y, self.thc_scf_fac_elliptict.y, atol=1.0e-06,rtol=1.0e-06)
        tplot(['thc_scf_fac_elliptict', 'idl_thc_scf_fac_elliptict'], display=global_display, save_png='elliptict.png')

    def test_helict(self):
        """ Validate twavpol helict output """

        py_helict = pyspedas.get_data('thc_scf_fac_helict')
        logging.info("nanmin/nanmax of helict: %f %f ",np.nanmin(py_helict.y),np.nanmax(py_helict.y))
        assert_allclose(py_helict.times,self.thc_scf_fac_helict.times,atol=1.0e-06)
        assert_allclose(py_helict.y, self.thc_scf_fac_helict.y, atol=1.0e-06,rtol=1.0e-06)
        tplot(['thc_scf_fac_helict', 'idl_thc_scf_fac_helict'] ,display=global_display, save_png='helict.png' )


if __name__ == '__main__':
    unittest.main()
