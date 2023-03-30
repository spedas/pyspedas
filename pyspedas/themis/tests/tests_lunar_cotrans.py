"""Tests of gse2sse and sse2sel functions."""
import pytplot.get_data
from pytplot.importers.cdf_to_tplot import cdf_to_tplot
import unittest
import pytplot
from numpy.testing import assert_array_almost_equal_nulp, assert_array_max_ulp, assert_allclose

from pyspedas.utilities.data_exists import data_exists
from pyspedas.themis.cotrans.gse2sse import gse2sse
from pyspedas.themis.state.autoload_support import autoload_support
from pyspedas.cotrans.cotrans_get_coord import cotrans_get_coord
from pyspedas.cotrans.cotrans_set_coord import cotrans_set_coord


class LunCotransDataValidation(unittest.TestCase):
    """ Compares cotrans results between Python and IDL """

    @classmethod
    def setUpClass(cls):
        """
        IDL Data has to be downloaded to perform these tests
        The SPEDAS script that creates the file: projects/themis/state/cotrans/thm_cotrans_validate.pro
        """
        from pyspedas.utilities.download import download
        from pyspedas.themis.config import CONFIG

        # Testing time range
        cls.t = ['2008-03-23', '2008-03-28']

        # Testing tolerance
        cls.tol = 1e-10

        # Download tplot files
        remote_server = 'https://spedas.org/'
        # remote_name = 'testfiles/thm_cotrans_validate.cdf'
        remote_name = 'testfiles/thm_cotrans_validate.tplot'
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
        #pytplot.tplot_names()
        # Input variables
        cls.tha_state_pos_gse = pytplot.get_data('tha_state_pos_gse')
        cls.tha_state_vel_gse = pytplot.get_data('tha_state_vel_gse')
        # GSE<->SSE results
        cls.tha_state_pos_sse = pytplot.get_data('tha_state_pos_sse')
        cls.tha_state_vel_sse = pytplot.get_data('tha_state_vel_sse')
        cls.tha_state_pos_gse_sse_gse = pytplot.get_data('tha_state_pos_gse_sse_gse')
        cls.tha_state_vel_gse_sse_gse = pytplot.get_data('tha_state_vel_gse_sse_gse')
        # SSE<->SSL results
        cls.tha_state_pos_sel = pytplot.get_data('tha_state_pos_sel')
        cls.tha_state_vel_sel = pytplot.get_data('tha_state_vel_sel')
        cls.tha_state_pos_gse_sel_sse = pytplot.get_data('tha_state_pos_gse_sel_sse')
        cls.tha_state_vel_gse_sel_sse = pytplot.get_data('tha_state_vel_gse_sel_sse')

        autoload_support(varname='tha_state_pos_gse', slp=True)


    def setUp(self):
        """ We need to clean tplot variables before each run"""
        # pytplot.del_data('*')


    def test_gse2sse_pos(self):
        """ Validate gse2sse position transform """
        result = gse2sse('tha_state_pos_gse', 'slp_sun_pos', 'slp_lun_pos', 'tha_state_pos_sse')
        self.assertEqual(result,1)
        pos_sse = pytplot.get_data('tha_state_pos_sse')
        assert_allclose(pos_sse.y, self.tha_state_pos_sse.y, atol=1.0e-06)

    def test_gse2sse_vel(self):
        """ Validate gse2sse velocity transform """
        result = gse2sse('tha_state_vel_gse', 'slp_sun_pos', 'slp_lun_pos', 'tha_state_vel_sse')
        self.assertEqual(result,1)
        vel_sse = pytplot.get_data('tha_state_vel_sse')
        assert_allclose(vel_sse.y, self.tha_state_vel_sse.y, atol=1.0e-06)

    def test_sse2gse_pos(self):
        """ Validate sse2gse position transform """
        result = gse2sse('tha_state_pos_sse', 'slp_sun_pos', 'slp_lun_pos', 'tha_state_pos_gse_sse_gse',issse2gse=True)
        self.assertEqual(result,1)
        pos_gse = pytplot.get_data('tha_state_pos_gse_sse_gse')
        assert_allclose(pos_gse.y, self.tha_state_pos_gse_sse_gse.y, atol=1.0e-06)


    def test_sse2gse_vel(self):
        """ Validate sse2gse velocity transform """
        result = gse2sse('tha_state_vel_sse', 'slp_sun_pos', 'slp_lun_pos', 'tha_state_vel_gse_sse_gse',issse2gse=True)
        self.assertEqual(result,1)
        vel_gse = pytplot.get_data('tha_state_vel_gse_sse_gse')
        assert_allclose(vel_gse.y, self.tha_state_vel_gse_sse_gse.y, atol=1.0e-06)


if __name__ == '__main__':
    unittest.main()
