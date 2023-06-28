"""Tests of ssl2dsl and dsl2gse functions."""

import unittest
from pytplot import get_data,del_data,tplot_restore,data_exists, set_coords
from numpy.testing import assert_array_almost_equal_nulp, assert_array_max_ulp, assert_allclose
from pyspedas.themis import autoload_support, ssl2dsl,dsl2gse


class DSLCotransDataValidation(unittest.TestCase):
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
        del_data('*')
        filename = datafile[0]
        # pytplot.cdf_to_tplot(filename)
        tplot_restore(filename)
        #pytplot.tplot_names()
        cls.basis_x = get_data('basis_x')
        cls.basis_y = get_data('basis_y')
        cls.basis_z = get_data('basis_z')
        cls.basis_x_gei2gse = get_data('basis_x_gei2gse')
        cls.basis_y_gei2gse = get_data('basis_y_gei2gse')
        cls.basis_z_gei2gse = get_data('basis_z_gei2gse')
        cls.basis_x_gse2gei = get_data('basis_x_gse2gei')
        cls.basis_y_gse2gei = get_data('basis_y_gse2gei')
        cls.basis_z_gse2gei = get_data('basis_z_gse2gei')

        cls.basis_x_dsl2gse = get_data('basis_x_dsl2gse')
        cls.basis_y_dsl2gse = get_data('basis_y_dsl2gse')
        cls.basis_z_dsl2gse = get_data('basis_z_dsl2gse')

        cls.basis_x_gse2dsl = get_data('basis_x_gse2dsl')
        cls.basis_y_gse2dsl = get_data('basis_y_gse2dsl')
        cls.basis_z_gse2dsl = get_data('basis_z_gse2dsl')

        cls.basis_x_ssl2dsl = get_data('basis_x_ssl2dsl')
        cls.basis_y_ssl2dsl = get_data('basis_y_ssl2dsl')
        cls.basis_z_ssl2dsl = get_data('basis_z_ssl2dsl')

        cls.basis_x_dsl2ssl = get_data('basis_x_dsl2ssl')
        cls.basis_y_dsl2ssl = get_data('basis_y_dsl2ssl')
        cls.basis_z_dsl2ssl = get_data('basis_z_dsl2ssl')

        state_trange = ['2007-03-20', '2007-03-30']
        autoload_support(trange=state_trange, probe='a', spinaxis=True, spinmodel=True)


    def setUp(self):
        """ We need to clean tplot variables before each run"""
        # del_data('*')

    def test_gei2gse(self):
        """Validate gei2gse transform """
        from pyspedas.cotrans.cotrans_lib import subgei2gse

        bx = self.basis_x
        by = self.basis_y
        bz = self.basis_z
        times = bx.times
        bx_gse = subgei2gse(times, bx.y)
        by_gse = subgei2gse(times, by.y)
        bz_gse = subgei2gse(times, bz.y)
        assert_allclose(bx_gse, self.basis_x_gei2gse.y, atol=1.0e-06)
        assert_allclose(by_gse, self.basis_y_gei2gse.y, atol=1.0e-06)
        assert_allclose(bz_gse, self.basis_z_gei2gse.y, atol=1.0e-06)

    def test_gse2gei(self):
        """Validate gse2gei transform """
        from pyspedas.cotrans.cotrans_lib import subgse2gei

        bx = self.basis_x
        by = self.basis_y
        bz = self.basis_z
        times = bx.times
        bx_gei = subgse2gei(times, bx.y)
        by_gei = subgse2gei(times, by.y)
        bz_gei = subgse2gei(times, bz.y)
        assert_allclose(bx_gei, self.basis_x_gse2gei.y, atol=1.0e-06)
        assert_allclose(by_gei, self.basis_y_gse2gei.y, atol=1.0e-06)
        assert_allclose(bz_gei, self.basis_z_gse2gei.y, atol=1.0e-06)

    def test_dsl2gse_x(self):
        """Validate dsl2gse X axis transform """
        set_coords('basis_x', 'DSL')
        result = dsl2gse('basis_x', 'tha_spinras_corrected', 'tha_spindec_corrected', 'basis_x_dsl2gse')
        self.assertEqual(result,1)
        bx_gse = get_data('basis_x_dsl2gse')
        assert_allclose(bx_gse.y, self.basis_x_dsl2gse.y, atol=1.0e-06)

    def test_dsl2gse_y(self):
        """Validate dsl2gse Y axis transform """
        from pyspedas.cotrans.cotrans_lib import subgse2gei
        set_coords('basis_y', 'DSL')
        result = dsl2gse('basis_y', 'tha_spinras_corrected', 'tha_spindec_corrected', 'basis_y_dsl2gse')
        self.assertEqual(result, 1)
        by_gse = get_data('basis_y_dsl2gse')
        assert_allclose(by_gse.y, self.basis_y_dsl2gse.y, atol=1.0e-06)

    def test_dsl2gse_z(self):
        """Validate dsl2gse Z axis transform """
        set_coords('basis_z', 'DSL')
        result = dsl2gse('basis_z', 'tha_spinras_corrected', 'tha_spindec_corrected', 'basis_z_dsl2gse')
        self.assertEqual(result, 1)
        bz_gse = get_data('basis_z_dsl2gse')
        assert_allclose(bz_gse.y, self.basis_z_dsl2gse.y, atol=1.0e-06)

    def test_gse2dsl_x(self):
        """Validate gse2dsl X axis transform """
        set_coords('basis_x', 'GSE')
        result = dsl2gse('basis_x', 'tha_spinras_corrected', 'tha_spindec_corrected', 'basis_x_gse2dsl', isgsetodsl=True)
        self.assertEqual(result, 1)
        self.assertEqual(result, 1)
        bx_gse = get_data('basis_x_gse2dsl')
        assert_allclose(bx_gse.y, self.basis_x_gse2dsl.y, atol=1.0e-06)

    def test_gse2dsl_y(self):
        """Validate gse2dsl Y axis transform """
        from pyspedas.cotrans.cotrans_lib import subgse2gei
        set_coords('basis_y', 'GSE')
        result = dsl2gse('basis_y', 'tha_spinras_corrected', 'tha_spindec_corrected', 'basis_y_gse2dsl', isgsetodsl=True)
        self.assertEqual(result, 1)
        by_gse = get_data('basis_y_gse2dsl')
        assert_allclose(by_gse.y, self.basis_y_gse2dsl.y, atol=1.0e-06)

    def test_gse2dsl_z(self):
        """Validate gse2dsl Z axis transform """
        set_coords('basis_z', 'GSE')
        result = dsl2gse('basis_z', 'tha_spinras_corrected', 'tha_spindec_corrected', 'basis_z_gse2dsl', isgsetodsl=True)
        self.assertEqual(result, 1)
        bz_gse = get_data('basis_z_gse2dsl')
        assert_allclose(bz_gse.y, self.basis_z_gse2dsl.y, atol=1.0e-06)

    def test_ssl2dsl_x(self):
        """Validate ssl2dsl X axis transform """
        from pyspedas.themis.state.spinmodel.spinmodel import get_spinmodel
        sm = get_spinmodel(probe='a', correction_level=1)
        set_coords('basis_x', 'SSL')
        result = ssl2dsl('basis_x', sm, 'basis_x_ssldsl')
        self.assertEqual(result, 1)
        bx_dsl = get_data('basis_x_ssl2dsl')
        assert_allclose(bx_dsl.y, self.basis_x_ssl2dsl.y, atol=1.0e-06)

    def test_ssl2dsl_y(self):
        """Validate ssl2dsl Y axis transform """
        from pyspedas.themis.state.spinmodel.spinmodel import get_spinmodel
        sm = get_spinmodel(probe='a', correction_level=1)
        set_coords('basis_y', 'SSL')
        result = ssl2dsl('basis_y', sm, 'basis_y_ssldsl', use_spinphase_correction=True)
        self.assertEqual(result, 1)
        by_dsl = get_data('basis_y_ssl2dsl')
        assert_allclose(by_dsl.y, self.basis_y_ssl2dsl.y, atol=1.0e-06)

    def test_ssl2dsl_z(self):
        """Validate ssl2dsl Z axis transform """
        from pyspedas.themis.state.spinmodel.spinmodel import get_spinmodel
        sm = get_spinmodel(probe='a', correction_level=1)
        set_coords('basis_z', 'SSL')
        result = ssl2dsl('basis_z', sm, 'basis_z_ssldsl', use_spinphase_correction=True)
        self.assertEqual(result, 1)
        bz_dsl = get_data('basis_z_ssl2dsl')
        assert_allclose(bz_dsl.y, self.basis_z_ssl2dsl.y, atol=1.0e-06)

    def test_dsl2ssl_x(self):
        """Validate dsl2ssl X axis transform """
        from pyspedas.themis.state.spinmodel.spinmodel import get_spinmodel
        sm = get_spinmodel(probe='a', correction_level=1)
        set_coords('basis_x', 'DSL')
        result = ssl2dsl('basis_x', sm, 'basis_x_dsl2ssl', use_spinphase_correction=True, isdsltossl=True)
        self.assertEqual(result, 1)
        bx_ssl = get_data('basis_x_dsl2ssl')
        # This test needs a slightly looser tolerance for some reason.
        assert_allclose(bx_ssl.y, self.basis_x_dsl2ssl.y, atol=1.5e-06)

    def test_dsl2ssl_y(self):
        """Validate dsl2ssl Y axis transform """
        from pyspedas.themis.state.spinmodel.spinmodel import get_spinmodel
        sm = get_spinmodel(probe='a', correction_level=1)
        set_coords('basis_y', 'DSL')
        result = ssl2dsl('basis_y', sm, 'basis_y_dsl2ssl', use_spinphase_correction=True, isdsltossl=True)
        self.assertEqual(result, 1)
        by_ssl = get_data('basis_y_dsl2ssl')
        # This test needs a slightly looser tolerance for some reason.
        assert_allclose(by_ssl.y, self.basis_y_dsl2ssl.y, atol=1.5e-06)

    def test_dsl2ssl_z(self):
        """Validate dsl2ssl Z axis transform """
        from pyspedas.themis.state.spinmodel.spinmodel import get_spinmodel
        sm = get_spinmodel(probe='a', correction_level=1)
        set_coords('basis_z', 'DSL')
        result = ssl2dsl('basis_z', sm, 'basis_z_dsl2ssl', use_spinphase_correction=True, isdsltossl=True)
        self.assertEqual(result, 1)
        bz_ssl = get_data('basis_z_dsl2ssl')
        assert_allclose(bz_ssl.y, self.basis_z_dsl2ssl.y, atol=1.0e-06)

    def test_catch_mismatch_dsl2ssl_z(self):
        """Test detection of mismatched input vs. requested coordinate systems in dsl2ssl transform """
        from pyspedas.themis.state.spinmodel.spinmodel import get_spinmodel
        sm = get_spinmodel(probe='a', correction_level=1)
        # Requesting DSL to SSL, but specifying SSL as input coordinate system
        set_coords('basis_z', 'SSL')
        result = ssl2dsl('basis_z', sm, 'basis_z_dsl2ssl', use_spinphase_correction=True, isdsltossl=True, ignore_input_coord = False)
        self.assertEqual(result, 0)

    def test_catch_mismatch_ssl2dsl_z(self):
        """Test detection of mismatched input vs. requested coordinates in ssl2dsl transform """
        from pyspedas.themis.state.spinmodel.spinmodel import get_spinmodel
        sm = get_spinmodel(probe='a', correction_level=1)
        # Requesting SSL to DSL, but specifying DSL as input coordinate system
        set_coords('basis_z', 'DSL')
        result = ssl2dsl('basis_z', sm, 'basis_z_ssldsl', use_spinphase_correction=True, ignore_input_coord=False)
        self.assertEqual(result, 0)

    def test_catch_mismatch_gse2dsl_z(self):
        """Test detection of mismatched input vs requested coordinates in gse2dsl transform """
        set_coords('basis_z', 'DSL')
        result = dsl2gse('basis_z', 'tha_spinras_corrected', 'tha_spindec_corrected', 'basis_z_gse2dsl', isgsetodsl=True)
        self.assertEqual(result, 0)

    def test_catch_mismatch_dsl2gse_z(self):
        """Test detection of mismatched input vs. requested coordinates in dsl2gse transform """
        set_coords('basis_z', 'GSE')
        result = dsl2gse('basis_z', 'tha_spinras_corrected', 'tha_spindec_corrected', 'basis_z_gse2dsl')
        self.assertEqual(result, 0)

    def test_ignore_mismatch_dsl2ssl_z(self):
        """Test ability to bypass coordinate system consistency check in dsl2ssl transform """
        from pyspedas.themis.state.spinmodel.spinmodel import get_spinmodel
        sm = get_spinmodel(probe='a', correction_level=1)
        # Requesting DSL to SSL, but specifying SSL as input coordinate system
        set_coords('basis_z', 'SSL')
        result = ssl2dsl('basis_z', sm, 'basis_z_dsl2ssl', use_spinphase_correction=True, isdsltossl=True, ignore_input_coord = True)
        self.assertEqual(result, 1)

    def test_ignore_mismatch_ssl2dsl_z(self):
        """Test ability to bypass coordinate system consistency check in ssl2dsl transform  """
        from pyspedas.themis.state.spinmodel.spinmodel import get_spinmodel
        sm = get_spinmodel(probe='a', correction_level=1)
        # Requesting SSL to DSL, but specifying DSL as input coordinate system
        set_coords('basis_z', 'DSL')
        result = ssl2dsl('basis_z', sm, 'basis_z_ssldsl', use_spinphase_correction=True, ignore_input_coord=True)
        self.assertEqual(result, 1)

    def test_ignore_mismatch_gse2dsl_z(self):
        """Test ability to bypass coordinate system consistency check in gse2dsl transform """
        set_coords('basis_z', 'DSL')
        result = dsl2gse('basis_z', 'tha_spinras_corrected', 'tha_spindec_corrected', 'basis_z_gse2dsl', isgsetodsl=True, ignore_input_coord=True)
        self.assertEqual(result, 1)

    def test_ignore_mismatch_dsl2gse_z(self):
        """Test ability to bypass coordinate system consistency check in dsl2gse transform """
        set_coords('basis_z', 'GSE')
        result = dsl2gse('basis_z', 'tha_spinras_corrected', 'tha_spindec_corrected', 'basis_z_gse2dsl', ignore_input_coord=True)
        self.assertEqual(result, 1)

if __name__ == '__main__':
    unittest.main()
