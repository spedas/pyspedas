import os
import logging
import unittest
from pytplot import data_exists
import pyspedas


class LoadTestCases(unittest.TestCase):
    def test_downloadonly(self):
        files = pyspedas.projects.wind.mfi(trange=['2013-11-5', '2013-11-6'], downloadonly=True)
        self.assertTrue(os.path.exists(files[0]))

    def test_load_3dp_data(self):
        tdp_vars = pyspedas.projects.wind.threedp(trange=['2003-09-5', '2003-09-6'], notplot=True)
        self.assertTrue('N_e_dens_wi_3dp' in tdp_vars)

    def test_load_3dp_pm_data(self):
        tdp_vars = pyspedas.projects.wind.threedp(trange=['2018-11-06', '2018-11-07'], datatype='3dp_pm', time_clip=True, notplot=True, addmaster=True)
        self.assertTrue('wi_3dp_pm_P_VELS' in tdp_vars)

    def test_load_3dp_ehpd_data(self):
        tdp_vars = pyspedas.projects.wind.threedp(trange=['2018-11-06', '2018-11-07'], datatype='3dp_ehpd', time_clip=True,
                                         notplot=True, addmaster=True)
        self.assertTrue('wi_3dp_ehpd_FLUX' in tdp_vars)

    def test_load_3dp_ehsp_data(self):
        tdp_vars = pyspedas.projects.wind.threedp(trange=['2019-11-06', '2019-11-07'], datatype='3dp_ehsp', time_clip=True,
                                         notplot=True, addmaster=True)
        self.assertTrue('wi_3dp_ehsp_FLUX' in tdp_vars)

    def test_load_3dp_elm2_data(self):
        tdp_vars = pyspedas.projects.wind.threedp(trange=['2019-11-06', '2019-11-07'], datatype='3dp_elm2', time_clip=True,
                                         notplot=True, addmaster=True)
        self.assertTrue('wi_3dp_elm2_FLUX' in tdp_vars)

    def test_load_3dp_elpd_data(self):
        tdp_vars = pyspedas.projects.wind.threedp(trange=['2019-11-06', '2019-11-07'], datatype='3dp_elpd', time_clip=True,
                                         notplot=True, addmaster=True)
        self.assertTrue('wi_3dp_elpd_FLUX' in tdp_vars)

    def test_load_3dp_elsp_data(self):
        tdp_vars = pyspedas.projects.wind.threedp(trange=['2019-11-06', '2019-11-07'], datatype='3dp_elsp', time_clip=True,
                                         notplot=True, addmaster=True)
        self.assertTrue('wi_3dp_elsp_FLUX' in tdp_vars)

    def test_load_3dp_em_data(self):
        tdp_vars = pyspedas.projects.wind.threedp(trange=['2019-11-06', '2019-11-07'], datatype='3dp_em', time_clip=True,
                                         notplot=True, addmaster=True)
        self.assertTrue('wi_3dp_em_E_DENS' in tdp_vars)

    def test_load_3dp_emfits_e0_data(self):
        tdp_vars = pyspedas.projects.wind.threedp(trange=['2003-10-11', '2003-10-12'], datatype='3dp_emfits_e0', time_clip=True,
                                         notplot=True, addmaster=True)
        self.assertTrue('N_e_dens_wi_3dp' in tdp_vars)

    def test_load_3dp_emfits_e0_data_prefix_suffix(self):
        tdp_vars = pyspedas.projects.wind.threedp(trange=['2003-10-11', '2003-10-12'], datatype='3dp_emfits_e0', time_clip=True,
                                         prefix='pre_', suffix='_suf', notplot=True, addmaster=True)
        self.assertTrue('pre_N_e_dens_wi_3dp_suf' in tdp_vars)

    def test_load_3dp_k0_data(self):
        # Note: this datatype is periodically pruned, SPDF seems to keep the last 3 years worth.
        tdp_vars = pyspedas.projects.wind.threedp(trange=['2023-01-01', '2023-01-02'], datatype='3dp_k0', time_clip=True,
                                         notplot=True, addmaster=True)
        self.assertTrue('wi_3dp_k0_elect_density' in tdp_vars)

    def test_load_3dp_phsp_data(self):
        tdp_vars = pyspedas.projects.wind.threedp(trange=['2019-11-06', '2019-11-07'], datatype='3dp_phsp', time_clip=True,
                                         notplot=True, addmaster=True)
        self.assertTrue('wi_3dp_phsp_FLUX' in tdp_vars)
    def test_varformat_star(self):
        tdp_vars = pyspedas.projects.wind.threedp(trange=['2019-11-06', '2019-11-07'], datatype='3dp_phsp', time_clip=True,
                                         notplot=True, addmaster=True, varformat='*')
        self.assertTrue('wi_3dp_phsp_FLUX' in tdp_vars)

    def test_varformat_dots(self):
        tdp_vars = pyspedas.projects.wind.threedp(trange=['2019-11-06', '2019-11-07'], datatype='3dp_phsp', time_clip=True,
                                         notplot=True, addmaster=True, varformat='....')
        self.assertTrue('wi_3dp_phsp_FLUX' in tdp_vars)

    def test_load_3dp_plsp_data(self):
        tdp_vars = pyspedas.projects.wind.threedp(trange=['2019-11-06', '2019-11-07'], datatype='3dp_plsp', time_clip=True,
                                         notplot=True, addmaster=True)
        self.assertTrue('wi_3dp_plsp_FLUX' in tdp_vars)

    def test_load_3dp_varformat_alternation(self):
        tdp_vars = pyspedas.projects.wind.threedp(trange=['2019-11-06', '2019-11-07'], datatype='3dp_plsp', time_clip=True,
                                         notplot=True, addmaster=True,varformat=r'MOM\.P\.FLUX|MOM\.P\.VELOCITY|MOM\.P\.PTENS')
        self.assertTrue('wi_3dp_plsp_MOM.P.FLUX' in tdp_vars)
        self.assertTrue('wi_3dp_plsp_MOM.P.VELOCITY' in tdp_vars)
        self.assertTrue('wi_3dp_plsp_MOM.P.PTENS' in tdp_vars)
        # Make sure we only got what we asked for
        self.assertFalse('wi_3dp_plsp_FLUX' in tdp_vars)

    def test_load_3dp_sfpd_data(self):
        tdp_vars = pyspedas.projects.wind.threedp(trange=['2019-11-06', '2019-11-07'], datatype='3dp_sfpd', time_clip=True,
                                         notplot=True, addmaster=True)
        self.assertTrue('wi_3dp_sfpd_FLUX' in tdp_vars)

    def test_load_3dp_sfpd_data_prefix_none(self):
        tdp_vars = pyspedas.projects.wind.threedp(trange=['2019-11-06', '2019-11-07'], datatype='3dp_sfpd', time_clip=True,
                                         prefix=None, notplot=True, addmaster=True)
        self.assertTrue('wi_3dp_sfpd_FLUX' in tdp_vars)

    def test_load_3dp_sfpd_data_suffix_none(self):
        tdp_vars = pyspedas.projects.wind.threedp(trange=['2019-11-06', '2019-11-07'], datatype='3dp_sfpd', time_clip=True,
                                         suffix=None, notplot=True, addmaster=True)
        self.assertTrue('wi_3dp_sfpd_FLUX' in tdp_vars)

    def test_load_3dp_sfpd_data_prefix_suffix(self):
        tdp_vars = pyspedas.projects.wind.threedp(trange=['2019-11-06', '2019-11-07'], datatype='3dp_sfpd', time_clip=True,
                                         prefix='pre_', suffix='_suf', notplot=True, addmaster=True)
        self.assertTrue('pre_wi_3dp_sfpd_FLUX_suf' in tdp_vars)

    def test_load_3dp_sfsp_data(self):
        tdp_vars = pyspedas.projects.wind.threedp(trange=['2019-11-06', '2019-11-07'], datatype='3dp_sfsp', time_clip=True,
                                         notplot=True, addmaster=True)
        self.assertTrue('wi_3dp_sfsp_FLUX' in tdp_vars)

    def test_load_3dp_sopd_data(self):
        tdp_vars = pyspedas.projects.wind.threedp(trange=['2019-11-06', '2019-11-07'], datatype='3dp_sopd', time_clip=True,
                                         notplot=True, addmaster=True)
        self.assertTrue('wi_3dp_sopd_FLUX' in tdp_vars)

    def test_load_3dp_sosp_data(self):
        tdp_vars = pyspedas.projects.wind.threedp(trange=['2019-11-06', '2019-11-07'], datatype='3dp_sosp', time_clip=True,
                                         notplot=True, addmaster=True)
        self.assertTrue('wi_3dp_sosp_FLUX' in tdp_vars)

    def test_load_mfi_data(self):
        mfi_vars = pyspedas.projects.wind.mfi(trange=['2013-11-5', '2013-11-6'], time_clip=True)
        self.assertTrue('BGSE' in mfi_vars)

    def test_load_swe_data(self):
        swe_vars = pyspedas.projects.wind.swe(trange=['2013-11-5', '2013-11-6'])
        self.assertTrue('N_elec' in swe_vars)
        self.assertTrue('T_elec' in swe_vars)
        self.assertTrue('W_elec' in swe_vars)

    def test_load_waves_data(self):
        wav_vars = pyspedas.projects.wind.waves(trange=['2013-11-5', '2013-11-6'])
        self.assertTrue('E_VOLTAGE_RAD1' in wav_vars)
        self.assertTrue('E_VOLTAGE_RAD2' in wav_vars)
        self.assertTrue('E_VOLTAGE_TNR' in wav_vars)

    def test_load_waves_rad1_rad2_data(self):
        import pyspedas
        from pytplot import tplot, tplot_names
        # example of a Type III radio burst
        trange = ['2019-04-02/15:00', '2019-04-02/16:30']
        rad2_vars = pyspedas.wind.waves(trange=trange, time_clip=True, datatype='rad2')
        rad1_vars = pyspedas.wind.waves(trange=trange, time_clip=True, datatype='rad1')
        self.assertTrue('wi_l2_wav_rad1_PSD_V2_Z' in rad1_vars)
        self.assertTrue('wi_l2_wav_rad2_PSD_V2_Z' in rad2_vars)
        #tplot_names()
        #tplot('wi_l2_wav_rad?_PSD_V2_Z')

    def test_load_orbit_pre_data(self):
        orb_vars = pyspedas.projects.wind.orbit(trange=['2013-11-5', '2013-11-6'])
        self.assertTrue('GSM_POS' in orb_vars)
        self.assertTrue('GSM_VEL' in orb_vars)
        self.assertTrue('SUN_VECTOR' in orb_vars)
        self.assertTrue('GCI_POS' in orb_vars)
        self.assertTrue('GCI_VEL' in orb_vars)

    def test_load_orbit_def_data(self):
        orb_vars = pyspedas.projects.wind.orbit(trange=['1997-06-5', '1997-06-6'],datatype='def_or')
        self.assertTrue('GSM_POS' in orb_vars)
        self.assertTrue('GSM_VEL' in orb_vars)
        self.assertTrue('SUN_VECTOR' in orb_vars)
        self.assertTrue('GCI_POS' in orb_vars)
        self.assertTrue('GCI_VEL' in orb_vars)

    def test_load_sms_data(self):
        sms_vars = pyspedas.projects.wind.sms()
        self.assertTrue('Alpha_vel' in sms_vars)
        self.assertTrue('C/O_ratio' in sms_vars)
        self.assertTrue('C_ion_temp' in sms_vars)
        self.assertTrue('O_ion_temp' in sms_vars)


if __name__ == '__main__':
    unittest.main()
