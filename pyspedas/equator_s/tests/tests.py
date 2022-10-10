import unittest
from pyspedas.utilities.data_exists import data_exists
import pyspedas


class LoadTestCases(unittest.TestCase):
    def test_load_notplot(self):
        mam_vars = pyspedas.equator_s.mam(notplot=True)
        self.assertTrue('B_xyz_gse%eq_pp_mam' in mam_vars)

    def test_load_mam_data(self):
        mam_vars = pyspedas.equator_s.mam(time_clip=True)
        self.assertTrue(data_exists('B_xyz_gse%eq_pp_mam'))

    def test_load_esa_downloadonly(self):
        esa = pyspedas.equator_s.esa(downloadonly=True)

    def test_load_edi_data(self):
        edi_vars = pyspedas.equator_s.edi()
        self.assertTrue(data_exists('V_ed_xyz_gse%eq_pp_edi'))
        self.assertTrue(data_exists('E_xyz_gse%eq_pp_edi'))

    def test_load_epi_data(self):
        epi_vars = pyspedas.equator_s.epi()
        self.assertTrue(data_exists('J_e_1%eq_pp_epi'))
        self.assertTrue(data_exists('J_e_2%eq_pp_epi'))

    def test_load_ici_data(self):
        ici_vars = pyspedas.equator_s.ici()
        self.assertTrue(data_exists('N_p%eq_pp_ici'))

    def test_load_pcd_data(self):
        pcd_vars = pyspedas.equator_s.pcd()
        self.assertTrue(data_exists('I_ion%eq_pp_pcd'))

    def test_load_sfd_data(self):
        sfd_vars = pyspedas.equator_s.sfd()
        self.assertTrue(data_exists('F_e>0.26%eq_sp_sfd'))


if __name__ == '__main__':
    unittest.main()
