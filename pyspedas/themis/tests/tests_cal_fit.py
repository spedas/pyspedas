"""Tests of cal_fit function."""
import pyspedas.themis.spacecraft.fields.fit
import pytplot.get_data
from pytplot.importers.tplot_restore import tplot_restore
import unittest
import numpy as np
from pyspedas.themis.spacecraft.fields.fit import cal_fit


class TestCalFitDataValidation(unittest.TestCase):
    """Tests of the data been identical to SPEDAS (IDL)."""

    @classmethod
    def setUpClass(cls):
        """
        IDL Data has to be downloaded to perform these tests
        The IDL script that creates data file:
        https://github.com/spedas/pyspedas-validation/blob/cal_fit/src/themis/validation_files/thm_load_fit_validation_files.pro
        """
        from pyspedas.utilities.download import download
        from pyspedas.themis.config import CONFIG

        # Testing time range
        cls.t = ['2008-03-15', '2008-03-16']

        # Testing tollerange
        cls.tol = 1e-10

        # Download tplot files
        remote_server = 'https://spedas.org/'
        remote_name = 'testfiles/cal_fit.tplot'
        calfile = download(remote_file=remote_name,
                           remote_path=remote_server,
                           local_path=CONFIG['local_data_dir'],
                           no_download=False)
        if not calfile:
            # Skip tests
            raise unittest.SkipTest("Cannot download data validation file")

        # Load validation variables from the test file
        filename = calfile[0]
        tplot_restore(filename)
        cls.tha_fit = pytplot.get_data('tha_fit')
        cls.tha_fgs = pytplot.get_data('tha_fgs')
        cls.tha_fgs_sigma = pytplot.get_data('tha_fgs_sigma')
        cls.tha_fit_bfit = pytplot.get_data('tha_fit_bfit')
        cls.tha_fit_efit = pytplot.get_data('tha_fit_efit')
        cls.tha_efs = pytplot.get_data('tha_efs')
        cls.tha_efs_sigma = pytplot.get_data('tha_efs_sigma')
        cls.tha_efs_0 = pytplot.get_data('tha_efs_0')
        cls.tha_efs_dot0 = pytplot.get_data('tha_efs_dot0')

    def setUp(self):
        """ We need to clean tplot variables before each run"""
        pytplot.del_data('*')

    def test_fgs(self):
        """Validate tha_fgs."""
        pyspedas.themis.fit(trange=self.t, probe='a', level='l1', varnames=['tha_fit'], time_clip=True)

        cal_fit(probe='a')
        tha_fgs = pytplot.get_data('tha_fgs')

        diff = np.nanmedian(tha_fgs.y - self.tha_fgs.y, axis=0, keepdims=True)
        self.assertAlmostEqual(diff.sum(), 0)

    def test_fgs_sigma(self):
        """Validate tha_fgs_sigma."""
        pyspedas.themis.fit(trange=self.t, probe='a', level='l1', varnames=['tha_fit'], time_clip=True)
        cal_fit(probe='a')
        tha_fgs_sigma = pytplot.get_data('tha_fgs_sigma')
        diff = np.nanmedian(tha_fgs_sigma.y - self.tha_fgs_sigma.y, axis=0, keepdims=True)
        self.assertAlmostEqual(diff.sum(), 0)

    def test_fit_bfit(self):
        """Validate tha_fit_bfit."""
        pyspedas.themis.fit(trange=self.t, probe='a', level='l1', varnames=['tha_fit'], time_clip=True)
        cal_fit(probe='a')
        tha_fit_bfit = pytplot.get_data('tha_fit_bfit')
        diff = np.nanmedian(tha_fit_bfit.y - self.tha_fit_bfit.y, axis=0, keepdims=True)
        self.assertAlmostEqual(diff.sum(), 0)

    def test_fit_efit(self):
        """Validate tha_fit_efit."""
        pyspedas.themis.fit(trange=self.t, probe='a', level='l1', varnames=['tha_fit', 'tha_fit_code'],
                            get_support_data=True, time_clip=True)
        cal_fit(probe='a')
        tha_fit_efit = pytplot.get_data('tha_fit_efit')
        diff = np.nanmedian(tha_fit_efit.y - self.tha_fit_efit.y, axis=0, keepdims=True)
        self.assertAlmostEqual(diff.sum(), 0)

    def test_efs(self):
        """Validate tha_efs."""
        pyspedas.themis.fit(trange=self.t, probe='a', level='l1', varnames=['tha_fit', 'tha_fit_code'],
                            get_support_data=True, time_clip=True)
        cal_fit(probe='a')
        tha_efs = pytplot.get_data('tha_efs')
        diff = np.nanmedian(tha_efs.y - self.tha_efs.y, axis=0, keepdims=True)
        self.assertAlmostEqual(diff.sum(), 0)

    def test_efs_sigma(self):
        """Validate tha_efs_sigma."""
        pyspedas.themis.fit(trange=self.t, probe='a', level='l1', varnames=['tha_fit', 'tha_fit_code'],
                            get_support_data=True, time_clip=True)
        cal_fit(probe='a')
        tha_efs_sigma = pytplot.get_data('tha_efs_sigma')
        diff = np.nanmedian(tha_efs_sigma.y - self.tha_efs_sigma.y, axis=0, keepdims=True)
        self.assertAlmostEqual(diff.sum(), 0)

    def test_efs_0(self):
        """Validate tha_efs_0."""
        pyspedas.themis.fit(trange=self.t, probe='a', level='l1', varnames=['tha_fit', 'tha_fit_code'],
                            get_support_data=True, time_clip=True)
        cal_fit(probe='a')
        tha_efs_0 = pytplot.get_data('tha_efs_0')
        diff = np.nanmedian(tha_efs_0.y - self.tha_efs_0.y, axis=0, keepdims=True)
        self.assertAlmostEqual(diff.sum(), 0)

    def test_efs_dot0(self):
        """Validate tha_efs_sigma."""
        pyspedas.themis.fit(trange=self.t, probe='a', level='l1', varnames=['tha_fit', 'tha_fit_code'],
                            get_support_data=True, time_clip=True)
        cal_fit(probe='a')
        tha_efs_dot0 = pytplot.get_data('tha_efs_dot0')
        diff = np.nanmedian(tha_efs_dot0.y - self.tha_efs_dot0.y, axis=0, keepdims=True)
        self.assertAlmostEqual(diff.sum(), 0)


class TestCalFitEfsNoCalDataValidation(unittest.TestCase):
    """Tests of the data been identical to SPEDAS (IDL)."""

    def setUp(self):
        """ IDL Data has to be downloaded to perform these tests"""
        from pyspedas.utilities.download import download
        from pyspedas.themis.config import CONFIG

        # Testing time range
        self.t = ['2008-03-15', '2008-03-16']

        # Testing tollerange
        self.tol = 1e-10

        # Download tplot files
        remote_server = 'https://spedas.org/'
        remote_name = 'testfiles/tha_efs_no_cal.tplot'
        calfile = download(remote_file=remote_name,
                           remote_path=remote_server,
                           local_path=CONFIG['local_data_dir'],
                           no_download=False)
        if not calfile:
            # Skip tests
            self.skipTest("Cannot download data validation file")

        # Load validation variables from the test file
        filename = calfile[0]
        tplot_restore(filename)
        self.tha_efs = pytplot.get_data('tha_efs')

        pytplot.del_data('*')

    def test_efs(self):
        """Validate tha_efs."""
        pyspedas.themis.fit(trange=self.t, probe='a', level='l1', varnames=['tha_fit', 'tha_fit_code'],
                            get_support_data=True, time_clip=True)
        cal_fit(probe='a', no_cal=True)
        tha_efs = pytplot.get_data('tha_efs')
        diff = np.nanmedian(tha_efs.y - self.tha_efs.y, axis=0, keepdims=True)
        self.assertAlmostEqual(diff.sum(), 0)


class TestCalFitInput(unittest.TestCase):

    def setUp(self):
        self.t = ['2008-03-15', '2008-03-15']

    def test_wrong_satellite(self):
        """Validate tha_fgs."""
        pyspedas.themis.fit(trange=self.t, probe='x', level='l1', varnames=['tha_fit'], time_clip=True)
        cal_fit(probe='x')

    def test_e34_ss(self):
        t = ['2011-02-27', '2011-02-28']
        pyspedas.themis.fit(trange=t, probe='b', level='l1', varnames=['thb_fit', 'thb_fit_code'],
                            get_support_data=True, time_clip=True)
        cal_fit(probe='b')

    def test_no_input(self):
        cal_fit(probe="")

    def test_probe_f(self):
        cal_fit(probe="f")


class TestCalFitMeta(unittest.TestCase):
    def setUp(self):
        trange = ['2008-03-15', '2008-03-15']
        pyspedas.themis.fit(trange=trange, probe='a', level='l1', varnames=['tha_fit', 'tha_fit_code'],
                            get_support_data=True, time_clip=True)
        cal_fit(probe='a', no_cal=True)

    def test_meta_units(self):
        vars = {'tha_fgs', 'tha_fgs_sigma', 'tha_fit_bfit', 'tha_fit_efit', 'tha_efs', 'tha_efs_sigma', 'tha_efs_0', 'tha_efs_dot0'}
        for var in vars:
            with self.subTest(f'Test of units in {var}', var=var):
                meta = pytplot.get_data(var, metadata=True)
                self.assertIn('units', meta)
                # axis_subtitle currently displays units
                self.assertIn('axis_subtitle', meta['plot_options']['yaxis_opt'])

    def test_meta_legend(self):
        vars = {'tha_fgs', 'tha_fgs_sigma', 'tha_fit_bfit', 'tha_fit_efit', 'tha_efs', 'tha_efs_sigma', 'tha_efs_0', 'tha_efs_dot0'}
        for var in vars:
            with self.subTest(f'Test of legend in {var}', var=var):
                meta = pytplot.get_data(var, metadata=True)
                self.assertIn('legend_names', meta['plot_options']['yaxis_opt'])


if __name__ == '__main__':
    unittest.main()
