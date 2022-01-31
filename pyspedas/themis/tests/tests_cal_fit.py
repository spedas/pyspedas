"""Tests of cal_fit function."""

import pyspedas
import pytplot
import unittest
import numpy as np
from pyspedas.themis.spacecraft.fields.fit import cal_fit


class TestCalFitDataValidation(unittest.TestCase):
    """Tests of the data been identical to SPEDAS (IDL)."""

    def setUp(self):
        """ IDL Data has to be downloaded to perform these tests"""
        from pyspedas.utilities.download import download
        from pyspedas.themis.config import CONFIG
        import pytplot

        # Testing time range
        self.t = ['2008-03-15', '2008-03-16']

        # Testing tollerange
        self.tol = 1e-10

        # Download tplot files
        remote_server = 'https://spedas.org/'
        remote_name = 'testfiles/cal_fit.tplot'
        calfile = download(remote_file=remote_name,
                           remote_path=remote_server,
                           local_path=CONFIG['local_data_dir'],
                           no_download=False)
        if not calfile:
            # Skip tests
            self.skipTest("Cannot download data validation file")

        # Load validation variables from the test file
        filename = calfile[0]
        pytplot.tplot_restore(filename)
        self.tha_fit = pytplot.get_data('tha_fit')
        self.tha_fgs = pytplot.get_data('tha_fgs')
        self.tha_fgs_sigma = pytplot.get_data('tha_fgs_sigma')
        self.tha_fit_bfit = pytplot.get_data('tha_fit_bfit')
        self.tha_fit_efit = pytplot.get_data('tha_fit_efit')
        self.tha_efs = pytplot.get_data('tha_efs')
        self.tha_efs_sigma = pytplot.get_data('tha_efs_sigma')
        self.tha_efs_0 = pytplot.get_data('tha_efs_0')
        self.tha_efs_dot0 = pytplot.get_data('tha_efs_dot0')

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
        pyspedas.themis.fit(trange=self.t, probe='a', level='l1', varnames=['tha_fit', 'tha_fit_code'], time_clip=True)
        cal_fit(probe='a')
        tha_fit_efit = pytplot.get_data('tha_fit_efit')
        diff = np.nanmedian(tha_fit_efit.y - self.tha_fit_efit.y, axis=0, keepdims=True)
        self.assertAlmostEqual(diff.sum(), 0)

    def test_fit_efit(self):
        """Validate tha_fit_efit."""
        pyspedas.themis.fit(trange=self.t, probe='a', level='l1', varnames=['tha_fit', 'tha_fit_code'], time_clip=True)
        cal_fit(probe='a')
        tha_fit_efit = pytplot.get_data('tha_fit_efit')
        diff = np.nanmedian(tha_fit_efit.y - self.tha_fit_efit.y, axis=0, keepdims=True)
        self.assertAlmostEqual(diff.sum(), 0)

    def test_efs(self):
        """Validate tha_efs."""
        pyspedas.themis.fit(trange=self.t, probe='a', level='l1', varnames=['tha_fit', 'tha_fit_code'],
                            time_clip=True)
        cal_fit(probe='a')
        tha_efs = pytplot.get_data('tha_efs')
        diff = np.nanmedian(tha_efs.y - self.tha_efs.y, axis=0, keepdims=True)
        self.assertAlmostEqual(diff.sum(), 0)

    def test_efs_sigma(self):
        """Validate tha_efs_sigma."""
        pyspedas.themis.fit(trange=self.t, probe='a', level='l1', varnames=['tha_fit', 'tha_fit_code'],
                            time_clip=True)
        cal_fit(probe='a')
        tha_efs_sigma = pytplot.get_data('tha_efs_sigma')
        diff = np.nanmedian(tha_efs_sigma.y - self.tha_efs_sigma.y, axis=0, keepdims=True)
        self.assertAlmostEqual(diff.sum(), 0)

    def test_efs_0(self):
        """Validate tha_efs_0."""
        pyspedas.themis.fit(trange=self.t, probe='a', level='l1', varnames=['tha_fit', 'tha_fit_code'],
                            time_clip=True)
        cal_fit(probe='a')
        tha_efs_0 = pytplot.get_data('tha_efs_0')
        diff = np.nanmedian(tha_efs_0.y - self.tha_efs_0.y, axis=0, keepdims=True)
        self.assertAlmostEqual(diff.sum(), 0)

    def test_efs_dot0(self):
        """Validate tha_efs_sigma."""
        pyspedas.themis.fit(trange=self.t, probe='a', level='l1', varnames=['tha_fit', 'tha_fit_code'],
                            time_clip=True)
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
        import pytplot

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
        pytplot.tplot_restore(filename)
        self.tha_efs = pytplot.get_data('tha_efs')

        pytplot.del_data('*')

    def test_efs(self):
        """Validate tha_efs."""
        pyspedas.themis.fit(trange=self.t, probe='a', level='l1', varnames=['tha_fit', 'tha_fit_code'],
                            time_clip=True)
        cal_fit(probe='a', no_cal=True)
        tha_efs = pytplot.get_data('tha_efs')
        diff = np.nanmedian(tha_efs.y - self.tha_efs.y, axis=0, keepdims=True)
        self.assertAlmostEqual(diff.sum(), 0)

if __name__ == '__main__':
    unittest.main()
