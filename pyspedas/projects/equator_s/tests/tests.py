import unittest
from pytplot import data_exists, del_data
import pyspedas


class EquatorS_Tests(unittest.TestCase):
    def test_load_notplot(self):
        mam_vars = pyspedas.equator_s.mam(notplot=True)
        self.assertTrue("B_xyz_gse%eq_pp_mam" in mam_vars)

    def test_load_mam_data(self):
        mam_vars = pyspedas.equator_s.mam(time_clip=True)
        self.assertTrue(data_exists("B_xyz_gse%eq_pp_mam"))

    def test_load_aux_data(self):
        aux_vars = pyspedas.equator_s.load(instrument="aux", prefix="test_")
        self.assertTrue(data_exists("test_sc_r_xyz_gse%eq_pp_aux"))

    def test_load_edi_data(self):
        edi_vars = pyspedas.equator_s.edi(downloadonly=True)
        edi_vars = pyspedas.equator_s.edi(no_update=True)
        self.assertTrue(data_exists("V_ed_xyz_gse%eq_pp_edi"))
        self.assertTrue(data_exists("E_xyz_gse%eq_pp_edi"))

    def test_load_edi_sp(self):
        edi_vars = pyspedas.equator_s.edi(datatype="sp")
        self.assertTrue(data_exists("V_ed_xyz_gse%eq_sp_edi"))

    def test_load_epi_data(self):
        epi_vars = pyspedas.equator_s.epi()
        self.assertTrue(data_exists("J_e_1%eq_pp_epi"))
        self.assertTrue(data_exists("J_e_2%eq_pp_epi"))

    def test_load_ici_data(self):
        ici_vars = pyspedas.equator_s.ici()
        self.assertTrue(data_exists("N_p%eq_pp_ici"))

    def test_load_pcd_data(self):
        pcd_vars = pyspedas.equator_s.pcd()
        self.assertTrue(data_exists("I_ion%eq_pp_pcd"))

    def test_load_sfd_data(self):
        sfd_vars = pyspedas.equator_s.sfd(trange=["1998-01-26", "1998-01-27"])
        self.assertTrue(data_exists("F_e>0.26%eq_sp_sfd"))

    def test_load_all_data(self):
        all_vars = pyspedas.equator_s.load(instrument="all")
        self.assertTrue(data_exists("J_e_1%eq_pp_epi"))
        self.assertTrue(data_exists("J_e_2%eq_pp_epi"))

    def test_load_invalid_trange(self):
        del_data()
        t_all = pyspedas.equator_s.load(trange="bad input")
        self.assertTrue(len(t_all) == 0)
        del_data()
        t_all = pyspedas.equator_s.load(trange=["2018-12-15"])
        self.assertTrue(len(t_all) == 0)
        del_data()
        t_all = pyspedas.equator_s.load(trange=["2018-12-15", "2018-12-14"])
        self.assertTrue(len(t_all) == 0)

    def test_load_invalid_instrument(self):
        del_data()
        t_all = pyspedas.equator_s.load(instrument="bad input")
        self.assertTrue(len(t_all) == 0)


if __name__ == "__main__":
    unittest.main()
