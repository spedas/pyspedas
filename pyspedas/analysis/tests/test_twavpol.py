"""Tests of twavpol functions."""
import pytplot.get_data
from pytplot.importers.cdf_to_tplot import cdf_to_tplot
import unittest
import pytplot
from numpy.testing import assert_array_almost_equal_nulp, assert_array_max_ulp, assert_allclose
import numpy as np

from pyspedas.utilities.data_exists import data_exists

from pyspedas.analysis.twavpol import twavpol

class TwavpolDataValidation(unittest.TestCase):
    """ Compares cotrans results between Python and IDL """

    @classmethod
    def setUpClass(cls):
        """
        IDL Data has to be downloaded to perform these tests
        The SPEDAS script that creates the file: projects/themis/state/cotrans/thm_cotrans_validate.pro
        """
        from pyspedas.utilities.download import download
        from pyspedas.themis.config import CONFIG

        # Testing tolerance
        cls.tol = 1e-10

        # Download tplot files
        remote_server = 'https://spedas.org/'
        # remote_name = 'testfiles/thm_cotrans_validate.cdf'
        remote_name = 'testfiles/thc_twavpol_validate.tplot'
        datafile = download(remote_file=remote_name,
                            remote_path=remote_server,
                            local_path=CONFIG['local_data_dir'],
                            no_download=False)
        if not datafile:
            # Skip tests
            raise unittest.SkipTest("Cannot download data validation file")

        # Load validation variables from the test file
        pytplot.del_data('*')
        filename = datafile[0]
        # pytplot.cdf_to_tplot(filename)
        pytplot.tplot_restore(filename)
        pytplot.tplot_names()
        #pytplot.tplot('thc_scf_fac')
        #pytplot.tplot('thc_scf_fac_powspec')
        #pytplot.tplot('thc_scf_fac')
        cls.thc_scf_fac = pytplot.get_data('thc_scf_fac')
        cls.thc_scf_fac_attr = pytplot.get_data('thc_scf_fac',metadata=True)
        cls.thc_scf_fac_powspec = pytplot.get_data('thc_scf_fac_powspec')
        cls.thc_scf_fac_powspec_attr = pytplot.get_data('thc_scf_fac_powspec',metadata=True)
        cls.thc_scf_fac_degpol = pytplot.get_data('thc_scf_fac_degpol')
        cls.thc_scf_fac_waveangle = pytplot.get_data('thc_scf_fac_waveangle')
        cls.thc_scf_fac_elliptict = pytplot.get_data('thc_scf_fac_elliptict')
        cls.thc_scf_fac_helict = pytplot.get_data('thc_scf_fac_helict')

        twavpol('thc_scf_fac')


    def setUp(self):
        """ We need to clean tplot variables before each run"""
        # pytplot.del_data('*')

    def test_powspec(self):
        """ Validate twavpol power spectrum output """

        py_powspec = pytplot.get_data('thc_scf_fac_powspec')
        #print(np.nanmin(py_powspec.y),np.nanmax(py_powspec.y))
        assert_allclose(py_powspec.times,self.thc_scf_fac_powspec.times,atol=1.0e-06)
        assert_allclose(py_powspec.y, self.thc_scf_fac_powspec.y, atol=1.0e-06)
        #pytplot.tplot('thc_scf_fac_powspec')

    def test_degpol(self):
        """ Validate twavpol degpol output """

        py_degpol = pytplot.get_data('thc_scf_fac_degpol')
        #print(np.min(py_degpol.y),np.nanmax(py_degpol.y))
        assert_allclose(py_degpol.times,self.thc_scf_fac_degpol.times,atol=1.0e-06)
        assert_allclose(py_degpol.y, self.thc_scf_fac_degpol.y, atol=1.0e-06)
        #pytplot.tplot('thc_scf_fac_degpol')

    def test_waveangle(self):
        """ Validate twavpol waveangle output """

        py_waveangle = pytplot.get_data('thc_scf_fac_waveangle')
        #print(np.nanmin(py_waveangle.y),np.nanmax(py_waveangle.y))
        assert_allclose(py_waveangle.times,self.thc_scf_fac_waveangle.times,atol=1.0e-05)
        assert_allclose(py_waveangle.y, self.thc_scf_fac_waveangle.y, atol=1.0e-05)
        #pytplot.tplot('thc_scf_fac_waveangle')

    def test_elliptict(self):
        """ Validate twavpol elliptict output """

        py_elliptict = pytplot.get_data('thc_scf_fac_elliptict')
        #print(np.nanmin(py_elliptict.y),np.nanmax(py_elliptict.y))
        assert_allclose(py_elliptict.times,self.thc_scf_fac_elliptict.times,atol=1.0e-06)
        assert_allclose(py_elliptict.y, self.thc_scf_fac_elliptict.y, atol=1.0e-06)
        #pytplot.tplot('thc_scf_fac_elliptict')

    def test_helict(self):
        """ Validate twavpol helict output """

        py_helict = pytplot.get_data('thc_scf_fac_helict')
        #print(np.nanmin(py_helict.y),np.nanmax(py_helict.y))
        assert_allclose(py_helict.times,self.thc_scf_fac_helict.times,atol=1.0e-06)
        assert_allclose(py_helict.y, self.thc_scf_fac_helict.y, atol=1.0e-06)
        #pytplot.tplot('thc_scf_fac_helict')


if __name__ == '__main__':
    unittest.main()
