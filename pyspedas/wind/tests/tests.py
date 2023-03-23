import os
import logging
import unittest
from pyspedas.utilities.data_exists import data_exists
import pyspedas


class LoadTestCases(unittest.TestCase):
    def test_downloadonly(self):
        files = pyspedas.wind.mfi(trange=['2013-11-5', '2013-11-6'], downloadonly=True)
        self.assertTrue(os.path.exists(files[0]))

    def test_load_3dp_data(self):
        tdp_vars = pyspedas.wind.threedp(trange=['2003-09-5', '2003-09-6'], notplot=True)
        self.assertTrue('N_e_dens_wi_3dp' in tdp_vars)

    def test_load_3dp_pm_data(self):
        tdp_vars = pyspedas.wind.threedp(trange=['2018-11-06', '2018-11-07'], datatype='3dp_pm', time_clip=True, notplot=True, addmaster=True)
        self.assertTrue('wi_3dp_pm_P_VELS' in tdp_vars)

    def test_load_3dp_ehpd_data(self):
        tdp_vars = pyspedas.wind.threedp(trange=['2018-11-06', '2018-11-07'], datatype='3dp_ehpd', time_clip=True,
                                         notplot=True, addmaster=True)
        self.assertTrue('wi_3dp_ehpd_FLUX' in tdp_vars)

    def test_load_3dp_ehsp_data(self):
        tdp_vars = pyspedas.wind.threedp(trange=['2019-11-06', '2019-11-07'], datatype='3dp_ehsp', time_clip=True,
                                         notplot=True, addmaster=True)
        self.assertTrue('wi_3dp_ehsp_FLUX' in tdp_vars)

    def test_load_3dp_elm2_data(self):
        tdp_vars = pyspedas.wind.threedp(trange=['2019-11-06', '2019-11-07'], datatype='3dp_elm2', time_clip=True,
                                         notplot=True, addmaster=True)
        self.assertTrue('wi_3dp_elm2_FLUX' in tdp_vars)

    def test_load_3dp_elpd_data(self):
        tdp_vars = pyspedas.wind.threedp(trange=['2019-11-06', '2019-11-07'], datatype='3dp_elpd', time_clip=True,
                                         notplot=True, addmaster=True)
        self.assertTrue('wi_3dp_elpd_FLUX' in tdp_vars)

    def test_load_3dp_elsp_data(self):
        tdp_vars = pyspedas.wind.threedp(trange=['2019-11-06', '2019-11-07'], datatype='3dp_elsp', time_clip=True,
                                         notplot=True, addmaster=True)
        self.assertTrue('wi_3dp_elsp_FLUX' in tdp_vars)

    def test_load_3dp_em_data(self):
        tdp_vars = pyspedas.wind.threedp(trange=['2019-11-06', '2019-11-07'], datatype='3dp_em', time_clip=True,
                                         notplot=True, addmaster=True)
        self.assertTrue('wi_3dp_em_E_DENS' in tdp_vars)

    def test_load_3dp_emfits_e0_data(self):
        tdp_vars = pyspedas.wind.threedp(trange=['2003-10-11', '2003-10-12'], datatype='3dp_emfits_e0', time_clip=True,
                                         notplot=True, addmaster=True)
        self.assertTrue('N_e_dens_wi_3dp' in tdp_vars)

    def test_load_3dp_k0_data(self):
        # Note: this datatype is periodically pruned, SPDF seems to keep the last 3 years worth.
        tdp_vars = pyspedas.wind.threedp(trange=['2023-01-01', '2023-01-02'], datatype='3dp_k0', time_clip=True,
                                         notplot=True, addmaster=True)
        self.assertTrue('wi_3dp_k0_elect_density' in tdp_vars)

    def test_load_3dp_phsp_data(self):
        tdp_vars = pyspedas.wind.threedp(trange=['2019-11-06', '2019-11-07'], datatype='3dp_phsp', time_clip=True,
                                         notplot=True, addmaster=True)
        self.assertTrue('wi_3dp_phsp_FLUX' in tdp_vars)
    def test_varformat_star(self):
        tdp_vars = pyspedas.wind.threedp(trange=['2019-11-06', '2019-11-07'], datatype='3dp_phsp', time_clip=True,
                                         notplot=True, addmaster=True, varformat='*')
        self.assertTrue('wi_3dp_phsp_FLUX' in tdp_vars)

    def test_varformat_dots(self):
        tdp_vars = pyspedas.wind.threedp(trange=['2019-11-06', '2019-11-07'], datatype='3dp_phsp', time_clip=True,
                                         notplot=True, addmaster=True, varformat='....')
        self.assertTrue('wi_3dp_phsp_FLUX' in tdp_vars)

    def test_load_3dp_plsp_data(self):
        tdp_vars = pyspedas.wind.threedp(trange=['2019-11-06', '2019-11-07'], datatype='3dp_plsp', time_clip=True,
                                         notplot=True, addmaster=True)
        self.assertTrue('wi_3dp_plsp_FLUX' in tdp_vars)

    def test_load_3dp_varformat_alternation(self):
        tdp_vars = pyspedas.wind.threedp(trange=['2019-11-06', '2019-11-07'], datatype='3dp_plsp', time_clip=True,
                                         notplot=True, addmaster=True,varformat='MOM\.P\.FLUX|MOM\.P\.VELOCITY|MOM\.P\.PTENS')
        self.assertTrue('wi_3dp_plsp_MOM.P.FLUX' in tdp_vars)
        self.assertTrue('wi_3dp_plsp_MOM.P.VELOCITY' in tdp_vars)
        self.assertTrue('wi_3dp_plsp_MOM.P.PTENS' in tdp_vars)

    def test_load_3dp_sfpd_data(self):
        tdp_vars = pyspedas.wind.threedp(trange=['2019-11-06', '2019-11-07'], datatype='3dp_sfpd', time_clip=True,
                                         notplot=True, addmaster=True)
        self.assertTrue('wi_3dp_sfpd_FLUX' in tdp_vars)
    def test_load_3dp_sfsp_data(self):
        tdp_vars = pyspedas.wind.threedp(trange=['2019-11-06', '2019-11-07'], datatype='3dp_sfsp', time_clip=True,
                                         notplot=True, addmaster=True)
        self.assertTrue('wi_3dp_sfsp_FLUX' in tdp_vars)

    def test_load_3dp_sopd_data(self):
        tdp_vars = pyspedas.wind.threedp(trange=['2019-11-06', '2019-11-07'], datatype='3dp_sopd', time_clip=True,
                                         notplot=True, addmaster=True)
        self.assertTrue('wi_3dp_sopd_FLUX' in tdp_vars)

    def test_load_3dp_sosp_data(self):
        tdp_vars = pyspedas.wind.threedp(trange=['2019-11-06', '2019-11-07'], datatype='3dp_sosp', time_clip=True,
                                         notplot=True, addmaster=True)
        self.assertTrue('wi_3dp_sosp_FLUX' in tdp_vars)

    def test_load_mfi_data(self):
        mfi_vars = pyspedas.wind.mfi(trange=['2013-11-5', '2013-11-6'], time_clip=True)
        self.assertTrue(data_exists('BGSE'))

    def test_load_swe_data(self):
        swe_vars = pyspedas.wind.swe(trange=['2013-11-5', '2013-11-6'])
        self.assertTrue(data_exists('N_elec'))
        self.assertTrue(data_exists('T_elec'))
        self.assertTrue(data_exists('W_elec'))

    def test_load_waves_data(self):
        swe_vars = pyspedas.wind.waves(trange=['2013-11-5', '2013-11-6'])
        self.assertTrue(data_exists('E_VOLTAGE_RAD1'))
        self.assertTrue(data_exists('E_VOLTAGE_RAD2'))
        self.assertTrue(data_exists('E_VOLTAGE_TNR'))

    def test_load_orbit_data(self):
        orb_vars = pyspedas.wind.orbit(trange=['2013-11-5', '2013-11-6'])
        self.assertTrue(data_exists('GSM_POS'))
        self.assertTrue(data_exists('GSM_VEL'))
        self.assertTrue(data_exists('SUN_VECTOR'))
        self.assertTrue(data_exists('GCI_POS'))
        self.assertTrue(data_exists('GCI_VEL'))

    def test_load_sms_data(self):
        sms_vars = pyspedas.wind.sms()
        self.assertTrue(data_exists('Alpha_vel'))
        self.assertTrue(data_exists('C/O_ratio'))
        self.assertTrue(data_exists('C_ion_temp'))
        self.assertTrue(data_exists('O_ion_temp'))


if __name__ == '__main__':
    unittest.main()
