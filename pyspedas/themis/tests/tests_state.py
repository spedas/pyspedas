import pytplot.get_data
from pytplot.importers.cdf_to_tplot import cdf_to_tplot
import unittest
import pyspedas
import pytplot
import pyspedas.themis
from numpy.testing import assert_allclose

class StateDataValidation(unittest.TestCase):
    """ Tests creation of support variables in themis.state() """

    @classmethod
    def setUpClass(cls):
        """
        IDL Data has to be downloaded to perform these tests
        The IDL script that creates data file: projects/themis/state/thm_state_validate.pro
        """
        from pyspedas.utilities.download import download
        from pyspedas.themis.config import CONFIG

        # Testing time range
        cls.t = ['2008-03-23', '2008-03-28']


        # Download validation file
        remote_server = 'https://spedas.org/'
        remote_name = 'testfiles/thm_state_validate.tplot'
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
        pytplot.tplot_restore(filename)
        pytplot.tplot_names()
        cls.tha_pos = pytplot.get_data('tha_state_pos')
        cls.tha_vel = pytplot.get_data('tha_state_vel')
        cls.tha_spinras = pytplot.get_data('tha_state_spinras')
        cls.tha_spindec = pytplot.get_data('tha_state_spindec')
        cls.tha_spinras_correction = pytplot.get_data('tha_state_spinras_correction')
        cls.tha_spindec_correction = pytplot.get_data('tha_state_spindec_correction')
        cls.tha_spinras_corrected = pytplot.get_data('tha_state_spinras_corrected')
        cls.tha_spindec_corrected = pytplot.get_data('tha_state_spindec_corrected')

        # Load with pyspedas
        pyspedas.themis.state(probe='a',trange=cls.t,get_support_data=True)

    def setUp(self):
        """ We need to clean tplot variables before each run"""
        # pytplot.del_data('*')

    def test_state_spinras(self):
        """Validate state variables """
        my_data = pytplot.get_data('tha_state_spinras')
        assert_allclose(my_data.y,self.tha_spinras.y,rtol=1.0e-06)

    def test_state_spindec(self):
        """Validate state variables """
        my_data = pytplot.get_data('tha_state_spindec')
        assert_allclose(my_data.y,self.tha_spindec.y,rtol=1.0e-06)

    def test_state_spinras_correction(self):
        """Validate state variables """
        my_data = pytplot.get_data('tha_state_spinras_correction')
        assert_allclose(my_data.y,self.tha_spinras_correction.y,rtol=1.0e-06)

    def test_state_spindec_correction(self):
        """Validate state variables """
        my_data = pytplot.get_data('tha_state_spindec_correction')
        assert_allclose(my_data.y,self.tha_spindec_correction.y,rtol=1.0e-06)

    def test_state_spinras_corrected(self):
        """Validate state variables """
        my_data = pytplot.get_data('tha_state_spinras_corrected')
        assert_allclose(my_data.y,self.tha_spinras_corrected.y,rtol=1.0e-06)

    def test_state_spindec_corrected(self):
        """Validate state variables """
        my_data = pytplot.get_data('tha_state_spindec_corrected')
        assert_allclose(my_data.y,self.tha_spindec_corrected.y,rtol=1.0e-06)

if __name__ == '__main__':
    unittest.main()
