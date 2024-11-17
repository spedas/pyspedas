
import os
import unittest
from pytplot import data_exists, del_data, tplot_names, get_data
from pyspedas.projects.erg.satellite.erg.particle.erg_lepi_get_dist import erg_lepi_get_dist
from pyspedas.projects.erg.satellite.erg.particle.erg_mepi_get_dist import erg_mepi_get_dist
from pyspedas.projects.erg.satellite.erg.particle.erg_lepe_get_dist import erg_lepe_get_dist
from pyspedas.projects.erg.satellite.erg.particle.erg_mepe_get_dist import erg_mepe_get_dist
from pyspedas.projects.erg.satellite.erg.particle.erg_hep_get_dist import erg_hep_get_dist
from pyspedas.projects.erg.satellite.erg.particle.erg_xep_get_dist import erg_xep_get_dist
import numpy as np
import pyspedas

class LoadTestCases(unittest.TestCase):
    def test_load_att_data(self):
        del_data()
        att_vars = pyspedas.projects.erg.att()
        tplot_names()
        self.assertTrue(data_exists('erg_att_sprate'))
        self.assertTrue(data_exists('erg_att_spphase'))
        self.assertTrue('erg_att_sprate' in att_vars)
        self.assertTrue('erg_att_spphase' in att_vars)

    def test_load_att_data_notplot(self):
        del_data()
        att_dict = pyspedas.projects.erg.att(notplot=True)
        self.assertTrue('erg_att_sprate' in att_dict)
        self.assertTrue('erg_att_spphase' in att_dict)


    def test_load_hep_data(self):
        del_data()
        hep_vars = pyspedas.projects.erg.hep()
        self.assertTrue(data_exists('erg_hep_l2_FEDO_L'))
        self.assertTrue(data_exists('erg_hep_l2_FEDO_H'))
        self.assertTrue('erg_hep_l2_FEDO_L' in hep_vars)
        self.assertTrue('erg_hep_l2_FEDO_H' in hep_vars)

    def test_load_hep_3dflux(self):
        del_data()
        hep_vars = pyspedas.projects.erg.hep(datatype='3dflux')
        self.assertTrue(data_exists('erg_hep_l2_FEDU_L'))
        self.assertTrue(data_exists('erg_hep_l2_FEDU_H'))
        self.assertTrue('erg_hep_l2_FEDU_L' in hep_vars)
        self.assertTrue('erg_hep_l2_FEDU_H' in hep_vars)

    def test_load_hep_l3_data(self):
        del_data()
        hep_vars = pyspedas.projects.erg.hep(level='l3')
        self.assertTrue(data_exists('erg_hep_l3_FEDU_L_paspec_ene00'))
        self.assertTrue(data_exists('erg_hep_l3_FEDU_H'))
        self.assertTrue('erg_hep_l3_FEDU_L_paspec_ene00' in hep_vars)
        self.assertTrue('erg_hep_l3_FEDU_H' in hep_vars)


    def test_load_xep_l3_data(self):
        del_data()
        # There are no XEP L3 products yet, but we can at least get some code coverage
        xep_vars = pyspedas.projects.erg.xep(level='l3')

    def test_load_xep_l2_omniflux_data(self):
        del_data()
        xep_vars = pyspedas.projects.erg.xep(level='l2')
        self.assertTrue('erg_xep_l2_FEDO_SSD' in xep_vars)
        self.assertTrue(data_exists('erg_xep_l2_FEDO_SSD'))


    def test_load_xep_l2_2dflux_data(self):
        del_data()
        xep_vars = pyspedas.projects.erg.xep(level='l2', datatype='2dflux')
        self.assertTrue('erg_xep_l2_FEDU_SSD' in xep_vars)
        self.assertTrue(data_exists('erg_xep_l2_FEDU_SSD'))

    def test_load_orb_data(self):
        del_data()
        orb_vars = pyspedas.projects.erg.orb()
        self.assertTrue(data_exists('erg_orb_l2_pos_gse'))
        self.assertTrue(data_exists('erg_orb_l2_pos_gsm'))
        self.assertTrue(data_exists('erg_orb_l2_pos_sm'))
        self.assertTrue(data_exists('erg_orb_l2_vel_gse'))
        self.assertTrue(data_exists('erg_orb_l2_vel_gsm'))
        self.assertTrue(data_exists('erg_orb_l2_vel_sm'))
        self.assertTrue('erg_orb_l2_pos_gse' in orb_vars)
        self.assertTrue('erg_orb_l2_pos_gsm' in orb_vars)
        self.assertTrue('erg_orb_l2_pos_sm' in orb_vars)
        self.assertTrue('erg_orb_l2_vel_gse' in orb_vars)
        self.assertTrue('erg_orb_l2_vel_gsm' in orb_vars)
        self.assertTrue('erg_orb_l2_vel_sm' in orb_vars)

    def test_load_orb_pre_data(self):
        del_data()
        orb_vars = pyspedas.projects.erg.orb(datatype='pre')
        self.assertTrue(data_exists('erg_orb_pre_l2_pos_gse'))
        self.assertTrue(data_exists('erg_orb_pre_l2_pos_gsm'))
        self.assertTrue(data_exists('erg_orb_pre_l2_pos_sm'))
        self.assertTrue(data_exists('erg_orb_pre_l2_vel_gse'))
        self.assertTrue(data_exists('erg_orb_pre_l2_vel_gsm'))
        self.assertTrue(data_exists('erg_orb_pre_l2_vel_sm'))
        self.assertTrue('erg_orb_pre_l2_pos_gse' in orb_vars)
        self.assertTrue('erg_orb_pre_l2_pos_gsm' in orb_vars)
        self.assertTrue('erg_orb_pre_l2_pos_sm' in orb_vars)
        self.assertTrue('erg_orb_pre_l2_vel_gse' in orb_vars)
        self.assertTrue('erg_orb_pre_l2_vel_gsm' in orb_vars)
        self.assertTrue('erg_orb_pre_l2_vel_sm' in orb_vars)

    def test_load_l3_orb_data(self):
        del_data()
        orb_vars = pyspedas.projects.erg.orb(level='l3')
        self.assertTrue(data_exists('erg_orb_l3_pos_eq_op'))
        self.assertTrue(data_exists('erg_orb_l3_pos_iono_north_op'))
        self.assertTrue(data_exists('erg_orb_l3_pos_iono_south_op'))
        self.assertTrue('erg_orb_l3_pos_eq_op' in orb_vars)
        self.assertTrue('erg_orb_l3_pos_iono_north_op' in orb_vars)
        self.assertTrue('erg_orb_l3_pos_iono_south_op' in orb_vars)

    def test_load_mgf_data(self):
        del_data()
        mgf_vars = pyspedas.projects.erg.mgf(time_clip=True)
        self.assertTrue(data_exists('erg_mgf_l2_mag_8sec_sm'))
        self.assertTrue('erg_mgf_l2_mag_8sec_sm' in mgf_vars)

    def test_load_lepe_data(self):
        del_data()
        lepe_vars = pyspedas.projects.erg.lepe()
        self.assertTrue(data_exists('erg_lepe_l2_omniflux_FEDO'))
        self.assertTrue('erg_lepe_l2_omniflux_FEDO' in lepe_vars)

    def test_load_lepe_3dflux(self):
        del_data()
        lepe_vars = pyspedas.projects.erg.lepe(datatype='3dflux')
        # No tplot variables, just a list with strings and dicts
        self.assertTrue('erg_lepe_l2_3dflux_FEDU' in lepe_vars)


    def test_load_lepe_l3_data(self):
        del_data()
        lepe_vars = pyspedas.projects.erg.lepe(level='l3', et_diagram=True)
        self.assertTrue(data_exists('erg_lepe_l3_pa_FEDU'))
        self.assertTrue('erg_lepe_l3_pa_FEDU' in lepe_vars)
        self.assertTrue(data_exists('erg_lepe_l3_pa_enech_01_FEDU'))
        self.assertTrue('erg_lepe_l3_pa_enech_01_FEDU' in lepe_vars)
        self.assertTrue(data_exists('erg_lepe_l3_pa_pabin_01_FEDU'))
        self.assertTrue('erg_lepe_l3_pa_pabin_01_FEDU' in lepe_vars)


    def test_load_lepi_data(self):
        del_data()
        lepi_vars = pyspedas.projects.erg.lepi()
        self.assertTrue(data_exists('erg_lepi_l2_omniflux_FPDO'))
        self.assertTrue(data_exists('erg_lepi_l2_omniflux_FHEDO'))
        self.assertTrue(data_exists('erg_lepi_l2_omniflux_FODO'))
        self.assertTrue('erg_lepi_l2_omniflux_FPDO' in lepi_vars)
        self.assertTrue('erg_lepi_l2_omniflux_FHEDO' in lepi_vars)
        self.assertTrue('erg_lepi_l2_omniflux_FODO' in lepi_vars)

    def test_load_lepi_3dflux_data(self):
        del_data()
        lepi_vars = pyspedas.projects.erg.lepi(datatype='3dflux')
        self.assertTrue(data_exists('erg_lepi_l2_3dflux_FPDU'))
        self.assertTrue(data_exists('erg_lepi_l2_3dflux_FHEDU'))
        self.assertTrue('erg_lepi_l2_3dflux_FPDU' in lepi_vars)
        self.assertTrue('erg_lepi_l2_3dflux_FHEDU' in lepi_vars)


    def test_load_mepi_get_dist(self):
        del_data()
        mepi_vars = pyspedas.projects.erg.mepi_nml(datatype='3dflux')
        base = "erg_mepi_l2_3dflux_"
        for species in ['FPDU', 'FHEDU', 'FODU']:
            var = base + species
            vardat = get_data(var)
            varmeta = get_data(var, metadata=True)
            t = vardat[0]
            dist = erg_mepi_get_dist(var, single_time="2017-07-01 00:00:00", species=None)
            self.assertTrue(len(dist['time']) == 1)
            dist = erg_mepi_get_dist(var, index=[0], species=None)
            self.assertTrue(len(dist['time']) == 1)
            dist = erg_mepi_get_dist(var, index=0, species=None)
            self.assertTrue(len(dist['time']) == 1)
            dist = erg_mepi_get_dist(var, index=[0,1,2], species=None)
            self.assertTrue(len(dist['time']) == 3)
            dist = erg_mepi_get_dist(var, index=np.array([0,1,2]), species=None)
            self.assertTrue(len(dist['time']) == 3)
            dist = erg_mepi_get_dist(var, trange=[t[0,], t[-1]], species=None)
            self.assertTrue(len(dist['time']) == len(t))

        self.assertTrue(data_exists('erg_mepi_l2_3dflux_FPDU'))
        self.assertTrue(data_exists('erg_mepi_l2_3dflux_FHEDU'))
        self.assertTrue('erg_mepi_l2_3dflux_FPDU' in mepi_vars)
        self.assertTrue('erg_mepi_l2_3dflux_FHEDU' in mepi_vars)

    def test_load_lepi_get_dist(self):
        del_data()
        lepi_vars = pyspedas.projects.erg.lepi(datatype='3dflux')
        base = "erg_lepi_l2_3dflux_"
        for species in ['FPDU', 'FHEDU', 'FODU']:
            var = base + species
            vardat = get_data(var)
            varmeta = get_data(var, metadata=True)
            t = vardat[0]
            dist = erg_lepi_get_dist(var, single_time="2017-07-01 00:00:00", species=None)
            self.assertTrue(len(dist['time']) == 1)
            dist = erg_lepi_get_dist(var, index=[0], species=None)
            self.assertTrue(len(dist['time']) == 1)
            dist = erg_lepi_get_dist(var, index=0, species=None)
            self.assertTrue(len(dist['time']) == 1)
            dist = erg_lepi_get_dist(var, index=[0,1,2], species=None)
            self.assertTrue(len(dist['time']) == 3)
            dist = erg_lepi_get_dist(var, index=np.array([0,1,2]), species=None)
            self.assertTrue(len(dist['time']) == 3)
            dist = erg_lepi_get_dist(var, trange=[t[0,], t[-1]], species=None)
            self.assertTrue(len(dist['time']) == len(t))

        self.assertTrue(data_exists('erg_lepi_l2_3dflux_FPDU'))
        self.assertTrue(data_exists('erg_lepi_l2_3dflux_FHEDU'))
        self.assertTrue('erg_lepi_l2_3dflux_FPDU' in lepi_vars)
        self.assertTrue('erg_lepi_l2_3dflux_FHEDU' in lepi_vars)

    def test_load_lepe_get_dist(self):
        del_data()
        lepe_vars = pyspedas.projects.erg.lepe(datatype='3dflux')
        base = "erg_lepe_l2_3dflux_"
        for species in ['FEDU']:
            var = base + species
            vardat = get_data(var)
            varmeta = get_data(var, metadata=True)
            t = vardat[0]
            dist = erg_lepe_get_dist(var, single_time="2017-04-04 00:00:00", species=None)
            self.assertTrue(len(dist['time']) == 1)
            dist = erg_lepe_get_dist(var, index=[0], species=None)
            self.assertTrue(len(dist['time']) == 1)
            dist = erg_lepe_get_dist(var, index=0, species=None)
            self.assertTrue(len(dist['time']) == 1)
            dist = erg_lepe_get_dist(var, index=[0,1,2], species=None)
            self.assertTrue(len(dist['time']) == 3)
            dist = erg_lepe_get_dist(var, index=np.array([0,1,2]), species=None)
            self.assertTrue(len(dist['time']) == 3)
            dist = erg_lepe_get_dist(var, trange=[t[0,], t[-1]], species=None)
            self.assertTrue(len(dist['time']) == len(t))
        self.assertTrue(data_exists('erg_lepe_l2_3dflux_FEDU'))
        self.assertTrue('erg_lepe_l2_3dflux_FEDU' in lepe_vars)

    def test_load_mepe_get_dist(self):
        del_data()
        mepe_vars = pyspedas.projects.erg.mepe(datatype='3dflux')
        base = "erg_mepe_l2_3dflux_"
        for species in ['FEDU']:
            var = base + species
            vardat = get_data(var)
            varmeta = get_data(var, metadata=True)
            t = vardat[0]
            dist = erg_mepe_get_dist(var, single_time="2017-03-27 00:00:00", species=None)
            self.assertTrue(len(dist['time']) == 1)
            dist = erg_mepe_get_dist(var, index=[0], species=None)
            self.assertTrue(len(dist['time']) == 1)
            dist = erg_mepe_get_dist(var, index=0, species=None)
            self.assertTrue(len(dist['time']) == 1)
            dist = erg_mepe_get_dist(var, index=[0,1,2], species=None)
            self.assertTrue(len(dist['time']) == 3)
            dist = erg_mepe_get_dist(var, index=np.array([0,1,2]), species=None)
            self.assertTrue(len(dist['time']) == 3)
            dist = erg_mepe_get_dist(var, trange=[t[0,], t[-1]], species=None)
            self.assertTrue(len(dist['time']) == len(t))
        self.assertTrue(data_exists('erg_mepe_l2_3dflux_FEDU'))
        self.assertTrue('erg_mepe_l2_3dflux_FEDU' in mepe_vars)

    def test_load_hep_get_dist(self):
        del_data()
        hep_vars = pyspedas.projects.erg.hep(datatype='3dflux')
        base = "erg_hep_l2_"
        for species in ['FEDU_L', 'FEDU_H']:
            var = base + species
            vardat = get_data(var)
            varmeta = get_data(var, metadata=True)
            t = vardat[0]
            dist = erg_hep_get_dist(var, single_time="2017-03-27 00:00:00", species=None)
            self.assertTrue(len(dist['time']) == 1)
            dist = erg_hep_get_dist(var, index=[0], species=None)
            self.assertTrue(len(dist['time']) == 1)
            dist = erg_hep_get_dist(var, index=0, species=None)
            self.assertTrue(len(dist['time']) == 1)
            dist = erg_hep_get_dist(var, index=[0,1,2], species=None)
            self.assertTrue(len(dist['time']) == 3)
            dist = erg_hep_get_dist(var, index=np.array([0,1,2]), species=None)
            self.assertTrue(len(dist['time']) == 3)
            dist = erg_hep_get_dist(var, trange=[t[0,], t[-1]], species=None)
            # This assertion doesn't necessarily hold for HEP.  Something to do with
            # availability of support data?
            # self.assertTrue(len(dist['time']) == len(t))
        self.assertTrue(data_exists('erg_hep_l2_FEDU_L'))
        self.assertTrue('erg_hep_l2_FEDU_L' in hep_vars)

    def test_load_xep_get_dist(self):
        del_data()
        xep_vars = pyspedas.projects.erg.xep(datatype='2dflux')
        base = "erg_xep_l2_"
        for species in ['FEDU_SSD']:
            var = base + species
            vardat = get_data(var)
            varmeta = get_data(var, metadata=True)
            t = vardat[0]
            dist = erg_xep_get_dist(var, single_time="2017-06-01 00:00:00", species=None)
            self.assertTrue(len(dist['time']) == 1)
            dist = erg_xep_get_dist(var, index=[0], species=None)
            self.assertTrue(len(dist['time']) == 1)
            dist = erg_xep_get_dist(var, index=0, species=None)
            self.assertTrue(len(dist['time']) == 1)
            dist = erg_xep_get_dist(var, index=[0,1,2], species=None)
            self.assertTrue(len(dist['time']) == 3)
            dist = erg_xep_get_dist(var, index=np.array([0,1,2]), species=None)
            self.assertTrue(len(dist['time']) == 3)
            dist = erg_xep_get_dist(var, trange=[t[0,], t[-1]], species=None)
            # This assertion doesn't necessarily hold for HEP.  Something to do with
            # availability of support data?
            # self.assertTrue(len(dist['time']) == len(t))
        self.assertTrue(data_exists('erg_xep_l2_FEDU_SSD'))
        self.assertTrue('erg_xep_l2_FEDU_SSD' in xep_vars)


    def test_load_lepi_l3_data(self):
        del_data()
        lepi_vars = pyspedas.projects.erg.lepi(level='l3')
        self.assertTrue(data_exists('erg_lepi_l3_pa_FPDU'))
        self.assertTrue('erg_lepi_l3_pa_FPDU' in lepi_vars)
        self.assertTrue(data_exists('erg_lepi_l3_pa_pabin_01_FPDU'))
        self.assertTrue('erg_lepi_l3_pa_pabin_01_FPDU' in lepi_vars)

    def test_load_mepe_data(self):
        del_data()
        mepe_vars = pyspedas.projects.erg.mepe()
        self.assertTrue(data_exists('erg_mepe_l2_omniflux_FEDO'))
        self.assertTrue('erg_mepe_l2_omniflux_FEDO' in mepe_vars)

    def test_load_mepe_l3_data(self):
        del_data()
        mepe_vars = pyspedas.projects.erg.mepe(level='l3')
        self.assertTrue(data_exists('erg_mepe_l3_3dflux_FEDU'))
        self.assertTrue('erg_mepe_l3_3dflux_FEDU' in mepe_vars)

    def test_load_mepe_3dflux(self):
        del_data()
        mepe_vars = pyspedas.projects.erg.mepe(datatype='3dflux')
        self.assertTrue(data_exists('erg_mepe_l2_3dflux_FEDU'))
        self.assertTrue('erg_mepe_l2_3dflux_FEDU' in mepe_vars)

    def test_load_mepi_nml_data(self):
        del_data()
        mepi_vars = pyspedas.projects.erg.mepi_nml()
        self.assertTrue(data_exists('erg_mepi_l2_omniflux_epoch_tof'))
        self.assertTrue('erg_mepi_l2_omniflux_epoch_tof' in mepi_vars)

    def test_load_mepi_nml_3dflux_data(self):
        del_data()
        mepi_vars = pyspedas.projects.erg.mepi_nml(datatype='3dflux')
        self.assertTrue(data_exists('erg_mepi_l2_3dflux_FPDU'))
        self.assertTrue('erg_mepi_l2_3dflux_FPDU' in mepi_vars)

    def test_load_mepi_tof_data(self):
        del_data()
        mepi_vars = pyspedas.projects.erg.mepi_tof()
        self.assertTrue(data_exists('erg_mepi_l2_tofflux_FPDU'))
        self.assertTrue(data_exists('erg_mepi_l2_tofflux_FODU'))
        self.assertTrue('erg_mepi_l2_tofflux_FPDU' in mepi_vars)
        self.assertTrue('erg_mepi_l2_tofflux_FODU' in mepi_vars)

    def test_load_mepi_nml_l3_3dflux_data(self):
        del_data()
        mepi_vars = pyspedas.projects.erg.mepi_nml(level='l3', datatype='3dflux')
        self.assertTrue(data_exists('erg_mepi_l3_3dflux_FPDU'))
        self.assertTrue('erg_mepi_l3_3dflux_FPDU' in mepi_vars)

    def test_load_mepi_nml_l3_pa_data(self):
        del_data()
        mepi_vars = pyspedas.projects.erg.mepi_nml(level='l3', datatype='pa')
        self.assertTrue(data_exists('erg_mepi_l3_pa_FPDU'))
        self.assertTrue('erg_mepi_l3_pa_FPDU' in mepi_vars)


    def test_load_pwe_ofa_data(self):
        del_data()
        pwe_vars = pyspedas.projects.erg.pwe_ofa()
        self.assertTrue(data_exists('erg_pwe_ofa_l2_spec_E_spectra_132'))
        self.assertTrue(data_exists('erg_pwe_ofa_l2_spec_B_spectra_132'))
        self.assertTrue('erg_pwe_ofa_l2_spec_E_spectra_132' in pwe_vars)
        self.assertTrue('erg_pwe_ofa_l2_spec_B_spectra_132' in pwe_vars)

    def test_load_pwe_efd_data(self):
        del_data()
        pwe_vars = pyspedas.projects.erg.pwe_efd()
        self.assertTrue(data_exists('erg_pwe_efd_l2_E_spin_Eu_dsi'))
        self.assertTrue('erg_pwe_efd_l2_E_spin_Eu_dsi' in pwe_vars)

    def test_load_pwe_efd_e64hz_data(self):
        del_data()
        pwe_vars = pyspedas.projects.erg.pwe_efd(datatype='E64Hz')
        self.assertTrue(data_exists('erg_pwe_efd_l2_E64Hz_dsi_Ex_waveform'))
        self.assertTrue('erg_pwe_efd_l2_E64Hz_dsi_Ex_waveform' in pwe_vars)

    def test_load_pwe_efd_pot_data(self):
        del_data()
        pwe_vars = pyspedas.projects.erg.pwe_efd(datatype='pot')
        self.assertTrue(data_exists('erg_pwe_efd_l2_pot_Vu1'))
        self.assertTrue('erg_pwe_efd_l2_pot_Vu1' in pwe_vars)

    def test_load_pwe_efd_spec_data(self):
        del_data()
        pwe_vars = pyspedas.projects.erg.pwe_efd(datatype='spec')
        self.assertTrue(data_exists('erg_pwe_efd_l2_spec_spectra'))
        self.assertTrue('erg_pwe_efd_l2_spec_spectra' in pwe_vars)

    def test_load_pwe_hfa_data(self):
        del_data()
        pwe_vars = pyspedas.projects.erg.pwe_hfa()
        self.assertTrue(data_exists('erg_pwe_hfa_l2_low_spectra_eu'))
        self.assertTrue(data_exists('erg_pwe_hfa_l2_low_spectra_ev'))
        self.assertTrue(data_exists('erg_pwe_hfa_l2_low_spectra_esum'))
        self.assertTrue(data_exists('erg_pwe_hfa_l2_low_spectra_er'))
        self.assertTrue('erg_pwe_hfa_l2_low_spectra_eu' in pwe_vars)
        self.assertTrue('erg_pwe_hfa_l2_low_spectra_ev' in pwe_vars)
        self.assertTrue('erg_pwe_hfa_l2_low_spectra_esum' in pwe_vars)
        self.assertTrue('erg_pwe_hfa_l2_low_spectra_er' in pwe_vars)

    def test_load_pwe_wfc_data(self):
        del_data()
        pwe_vars = pyspedas.projects.erg.pwe_wfc(trange=['2017-04-01/12:00:00', '2017-04-01/13:00:00'])
        self.assertTrue(data_exists('erg_pwe_wfc_l2_e_65khz_Ex_waveform'))
        self.assertTrue('erg_pwe_wfc_l2_e_65khz_Ex_waveform' in pwe_vars)

    def test_load_pwe_wfc_spec_data(self):
        del_data()
        pwe_vars = pyspedas.projects.erg.pwe_wfc(trange=['2017-04-01/12:00:00', '2017-04-01/13:00:00'], datatype='spec')
        self.assertTrue(data_exists('erg_pwe_wfc_l2_e_65khz_E_spectra'))
        self.assertTrue('erg_pwe_wfc_l2_e_65khz_E_spectra' in pwe_vars)

    def test_downloadonly(self):
        del_data()
        files = pyspedas.projects.erg.mgf(downloadonly=True, trange=['2017-03-27', '2017-03-28'])
        self.assertTrue(os.path.exists(files[0]))

if __name__ == '__main__':
    unittest.main()