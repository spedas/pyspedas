import unittest
from pytplot import data_exists
import pyspedas


class LoadTestCases(unittest.TestCase):
    def test_load_mfi_data(self):
        mfi_vars = pyspedas.projects.ace.mfi(trange=['2018-11-5', '2018-11-6'], time_clip=True)
        self.assertTrue(data_exists('Magnitude'))

    def test_load_mfi_prefix_none(self):
        mfi_vars = pyspedas.projects.ace.mfi(trange=['2018-11-5', '2018-11-6'], prefix=None)
        self.assertTrue(data_exists('Magnitude'))

    def test_load_mfi_suffix_none(self):
        mfi_vars = pyspedas.projects.ace.mfi(trange=['2018-11-5', '2018-11-6'], suffix=None)
        self.assertTrue(data_exists('Magnitude'))

    def test_load_mfi_prefix_suffix(self):
        mfi_vars = pyspedas.projects.ace.mfi(trange=['2018-11-5', '2018-11-6'], prefix='pre_', suffix='_suf')
        self.assertTrue(data_exists('pre_Magnitude_suf'))

    def test_load_mfi_notplot(self):
        mfi_vars = pyspedas.projects.ace.mfi(trange=['2018-11-5', '2018-11-6'], notplot=True)
        self.assertTrue(isinstance(mfi_vars, dict))

    def test_load_mfi_downloadonly(self):
        mfi_vars = pyspedas.projects.ace.mfi(trange=['2018-11-5', '2018-11-6'], downloadonly=True)
        self.assertTrue(isinstance(mfi_vars, list))

    def test_load_swe_data(self):
        swe_vars = pyspedas.projects.ace.swe()
        self.assertTrue(data_exists('Np'))
        self.assertTrue(data_exists('Vp'))

    def test_load_epm_data(self):
        epm_vars = pyspedas.projects.ace.epam()
        self.assertTrue(data_exists('H_lo'))
        self.assertTrue(data_exists('Ion_very_lo'))
        self.assertTrue(data_exists('Ion_mid'))
        self.assertTrue(data_exists('Electron_hi'))

    def test_load_cris_data(self):
        cris_vars = pyspedas.projects.ace.cris()
        self.assertTrue(data_exists('flux_N'))

    def test_load_sis_data(self):
        sis_vars = pyspedas.projects.ace.sis()
        self.assertTrue(data_exists('H_lo'))
        self.assertTrue(data_exists('H_hi'))

    def test_load_ule_data(self):
        ule_vars = pyspedas.projects.ace.uleis()
        self.assertTrue(data_exists('H_S1'))

    def test_load_sep_data(self):
        sep_vars = pyspedas.projects.ace.sepica()
        self.assertTrue(data_exists('H1'))
        self.assertTrue(data_exists('H2'))
        self.assertTrue(data_exists('H3'))

    def test_load_swi_data(self):
        swi_vars = pyspedas.projects.ace.swics()
        self.assertTrue(data_exists('vHe2'))

    def test_data_dir(self):
        self.assertTrue(pyspedas.projects.ace.config.CONFIG['local_data_dir'] == 'ace_data/')


if __name__ == '__main__':
    unittest.main()
