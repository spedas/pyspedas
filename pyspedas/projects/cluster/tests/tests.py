import os
import unittest
from pytplot import data_exists, del_data, tplot_names, tplot
import pyspedas
from pyspedas.projects.cluster.load_csa import cl_master_probes, cl_master_datatypes



class LoadTestCases(unittest.TestCase):
    def test_csa(self):
        dtypes = cl_master_datatypes()
        probes = cl_master_probes()
        self.assertTrue('CP_FGM_SPIN' in dtypes)
        self.assertTrue('C1' in probes)

    def test_load_fgm_data(self):
        del_data('*')
        mag_vars = pyspedas.projects.cluster.fgm(time_clip=True)
        self.assertTrue(data_exists('B_xyz_gse__C1_UP_FGM'))
        self.assertTrue('B_xyz_gse__C1_UP_FGM' in mag_vars)

    def test_load_fgm_data_prefix_none(self):
        del_data('*')
        mag_vars = pyspedas.projects.cluster.fgm(prefix=None, time_clip=True)
        self.assertTrue(data_exists('B_xyz_gse__C1_UP_FGM'))
        self.assertTrue('B_xyz_gse__C1_UP_FGM' in mag_vars)

    def test_load_fgm_data_suffix_none(self):
        del_data('*')
        mag_vars = pyspedas.projects.cluster.fgm(suffix=None, time_clip=True)
        self.assertTrue(data_exists('B_xyz_gse__C1_UP_FGM'))
        self.assertTrue('B_xyz_gse__C1_UP_FGM' in mag_vars)

    def test_load_fgm_data_prefix_suffix(self):
        del_data('*')
        mag_vars = pyspedas.projects.cluster.fgm(prefix='pre_', suffix='_suf', time_clip=True)
        self.assertTrue(data_exists('pre_B_xyz_gse__C1_UP_FGM_suf'))
        self.assertTrue('pre_B_xyz_gse__C1_UP_FGM_suf' in mag_vars)

    def test_load_fgm_cp_data(self):
        del_data('*')
        files = pyspedas.projects.cluster.fgm(datatype='cp', trange=['2003-12-15', '2003-12-16'], downloadonly=True)
        self.assertTrue(os.path.exists(files[0]))

    def test_load_asp_data(self):
        del_data('*')
        asp_vars = pyspedas.projects.cluster.aspoc(trange=['2004-04-05', '2004-04-06'])
        self.assertTrue(data_exists('I_ion__C1_PP_ASP'))
        self.assertTrue('I_ion__C1_PP_ASP' in asp_vars)

    def test_load_cis_data(self):
        del_data('*')
        cis_vars = pyspedas.projects.cluster.cis()
        self.assertTrue(data_exists('N_p__C1_PP_CIS'))
        self.assertTrue('N_p__C1_PP_CIS' in cis_vars)

    def test_load_dwp_data(self):
        del_data('*')
        dwp_vars = pyspedas.projects.cluster.dwp()
        self.assertTrue(data_exists('Correl_freq__C1_PP_DWP'))
        self.assertTrue('Correl_freq__C1_PP_DWP' in dwp_vars)

    def test_load_edi_data_download_only(self):
        del_data('*')
        edi_vars = pyspedas.projects.cluster.edi(downloadonly=True)
        self.assertTrue(isinstance(edi_vars, list))

    def test_load_edi_data(self):
        del_data('*')
        edi_vars = pyspedas.projects.cluster.edi()
        self.assertTrue(data_exists('V_ed_xyz_gse__C1_PP_EDI'))
        self.assertTrue('V_ed_xyz_gse__C1_PP_EDI' in edi_vars)

    def test_load_efw_data(self):
        del_data('*')
        efw_vars = pyspedas.projects.cluster.efw()
        self.assertTrue(data_exists('E_pow_f1__C1_PP_EFW'))
        self.assertTrue('E_pow_f1__C1_PP_EFW' in efw_vars)

    def test_load_peace_data(self):
        del_data('*')
        p_vars = pyspedas.projects.cluster.peace()
        self.assertTrue(data_exists('T_e_par__C1_PP_PEA'))
        self.assertTrue('T_e_par__C1_PP_PEA' in p_vars)

    def test_load_rap_data(self):
        del_data('*')
        r_vars = pyspedas.projects.cluster.rapid()
        self.assertTrue(data_exists('J_e_lo__C1_PP_RAP'))
        self.assertTrue('J_e_lo__C1_PP_RAP' in r_vars)

    def test_load_sta_data(self):
        del_data('*')
        sta_vars = pyspedas.projects.cluster.staff()
        self.assertTrue(data_exists('E_pow_f2__C1_PP_STA'))
        self.assertTrue('E_pow_f2__C1_PP_STA' in sta_vars)

    def test_load_wbd_data_notplot(self):
        del_data('*')
        wbd_vars = pyspedas.projects.cluster.wbd(trange=['2012-11-6/02:10', '2012-11-6/02:15'], notplot=True)
        self.assertTrue('WBD_Elec' in wbd_vars)

    def test_load_wbd_data_(self):
        del_data('*')
        wbd_vars = pyspedas.projects.cluster.wbd(trange=['2012-11-6/02:10', '2012-11-6/02:15'])
        self.assertTrue(data_exists('WBD_Elec'))
        self.assertTrue('WBD_Elec' in wbd_vars)

    def test_load_whi_data(self):
        del_data('*')
        whi_vars = pyspedas.projects.cluster.whi()
        self.assertTrue(data_exists('E_pow_f5__C1_PP_WHI'))
        self.assertTrue('E_pow_f5__C1_PP_WHI' in whi_vars)

    def test_load_csa_CE_WBD_WAVEFORM_CDF_data(self):
        del_data('*')
        trange = ['2012-11-06T02:19:00Z', '2012-11-06T02:19:59Z']
        wbd_data = pyspedas.projects.cluster.load_csa(probes=['C1'],
                                             trange=trange,
                                             datatypes=['CE_WBD_WAVEFORM_CDF'], time_clip=True)
        print(wbd_data)
        self.assertTrue('WBD_Elec' in wbd_data)
        self.assertTrue(data_exists('WBD_Elec'))

    def test_load_csa_CP_AUX_POSGSE_1M_data(self):
        del_data('*')
        trange = ['2001-02-01T00:00:00Z', '2001-02-04T00:00:00Z']
        pos_data = pyspedas.projects.cluster.load_csa(probes=['C1'],
                                             trange=trange,
                                             datatypes=['CP_AUX_POSGSE_1M'], time_clip=True)
        self.assertTrue('sc_r_xyz_gse__C1_CP_AUX_POSGSE_1M' in pos_data)
        self.assertTrue(data_exists('sc_r_xyz_gse__C1_CP_AUX_POSGSE_1M'))

    def test_load_csa_CP_AUX_POSGSE_1M_data_prefix_none(self):
        del_data('*')
        trange = ['2001-02-01T00:00:00Z', '2001-02-04T00:00:00Z']
        pos_data = pyspedas.projects.cluster.load_csa(probes=['C1'],
                                             trange=trange,
                                             prefix=None,
                                             datatypes=['CP_AUX_POSGSE_1M'], time_clip=True)
        self.assertTrue('sc_r_xyz_gse__C1_CP_AUX_POSGSE_1M' in pos_data)
        self.assertTrue(data_exists('sc_r_xyz_gse__C1_CP_AUX_POSGSE_1M'))

    def test_load_csa_CP_AUX_POSGSE_1M_data_suffix_none(self):
        del_data('*')
        trange = ['2001-02-01T00:00:00Z', '2001-02-04T00:00:00Z']
        pos_data = pyspedas.projects.cluster.load_csa(probes=['C1'],
                                             trange=trange,
                                             suffix=None,
                                             datatypes=['CP_AUX_POSGSE_1M'], time_clip=True)
        self.assertTrue('sc_r_xyz_gse__C1_CP_AUX_POSGSE_1M' in pos_data)
        self.assertTrue(data_exists('sc_r_xyz_gse__C1_CP_AUX_POSGSE_1M'))

    def test_load_csa_CP_AUX_POSGSE_1M_data_prefix_suffix(self):
        del_data('*')
        trange = ['2001-02-01T00:00:00Z', '2001-02-04T00:00:00Z']
        pos_data = pyspedas.projects.cluster.load_csa(probes=['C1'],
                                             trange=trange,
                                             prefix='pre_',
                                             suffix='_suf',
                                             datatypes=['CP_AUX_POSGSE_1M'], time_clip=True)
        self.assertTrue('pre_sc_r_xyz_gse__C1_CP_AUX_POSGSE_1M_suf' in pos_data)
        self.assertTrue(data_exists('pre_sc_r_xyz_gse__C1_CP_AUX_POSGSE_1M_suf'))


    def test_load_csa_CP_CIS_CODIF_HS_H1_MOMENTS_data(self):
        del_data('*')
        trange = ['2001-02-01T00:00:00Z', '2001-02-04T00:00:00Z']
        mom_data = pyspedas.projects.cluster.load_csa(probes=['C1'],
                                             trange=trange,
                                             datatypes=['CP_CIS-CODIF_HS_H1_MOMENTS'], time_clip=True)
        print(mom_data)
        self.assertTrue('density__C1_CP_CIS_CODIF_HS_H1_MOMENTS' in mom_data)
        self.assertTrue(data_exists('density__C1_CP_CIS_CODIF_HS_H1_MOMENTS'))

    def test_load_csa_CP_CIS_CODIF_HS_He1_MOMENTS_data(self):
        del_data('*')
        trange = ['2001-02-01T00:00:00Z', '2001-02-04T00:00:00Z']
        mom_data = pyspedas.projects.cluster.load_csa(probes=['C1'],
                                             trange=trange,
                                             datatypes=['CP_CIS-CODIF_HS_He1_MOMENTS'], time_clip=True)
        print(mom_data)
        self.assertTrue('density__C1_CP_CIS_CODIF_HS_He1_MOMENTS' in mom_data)
        self.assertTrue(data_exists('density__C1_CP_CIS_CODIF_HS_He1_MOMENTS'))


    def test_load_csa_CP_CIS_CODIF_HS_O1_MOMENTS_data(self):
        del_data('*')
        trange = ['2001-02-01T00:00:00Z', '2001-02-04T00:00:00Z']
        mom_data = pyspedas.projects.cluster.load_csa(probes=['C1'],
                                             trange=trange,
                                             datatypes=['CP_CIS-CODIF_HS_O1_MOMENTS'], time_clip=True)
        print(mom_data)
        self.assertTrue('density__C1_CP_CIS_CODIF_HS_O1_MOMENTS' in mom_data)
        self.assertTrue(data_exists('density__C1_CP_CIS_CODIF_HS_O1_MOMENTS'))


    def test_load_csa_CP_CIS_CODIF_PAD_HS_H1_PF_data(self):
        del_data('*')
        trange = ['2001-02-01T00:00:00Z', '2001-02-04T00:00:00Z']
        mom_data = pyspedas.projects.cluster.load_csa(probes=['C1'],
                                             trange=trange,
                                             datatypes=['CP_CIS-CODIF_PAD_HS_H1_PF'], time_clip=True)
        print(mom_data)
        self.assertTrue('Differential_Particle_Flux__C1_CP_CIS_CODIF_PAD_HS_H1_PF' in mom_data)
        self.assertTrue(data_exists('Differential_Particle_Flux__C1_CP_CIS_CODIF_PAD_HS_H1_PF'))


    def test_load_csa_CP_CIS_CODIF_PAD_HS_He1_PF_data(self):
        del_data('*')
        trange = ['2001-02-01T00:00:00Z', '2001-02-04T00:00:00Z']
        mom_data = pyspedas.projects.cluster.load_csa(probes=['C1'],
                                             trange=trange,
                                             datatypes=['CP_CIS-CODIF_PAD_HS_He1_PF'], time_clip=True)
        print(mom_data)
        self.assertTrue('Differential_Particle_Flux__C1_CP_CIS_CODIF_PAD_HS_He1_PF' in mom_data)
        self.assertTrue(data_exists('Differential_Particle_Flux__C1_CP_CIS_CODIF_PAD_HS_He1_PF'))


    def test_load_csa_CP_CIS_CODIF_PAD_HS_O1_PF_data(self):
        del_data('*')
        trange = ['2001-02-01T00:00:00Z', '2001-02-04T00:00:00Z']
        mom_data = pyspedas.projects.cluster.load_csa(probes=['C1'],
                                             trange=trange,
                                             datatypes=['CP_CIS-CODIF_PAD_HS_O1_PF'], time_clip=True)
        print(mom_data)
        self.assertTrue('Differential_Particle_Flux__C1_CP_CIS_CODIF_PAD_HS_O1_PF' in mom_data)
        self.assertTrue(data_exists('Differential_Particle_Flux__C1_CP_CIS_CODIF_PAD_HS_O1_PF'))


    def test_load_csa_CP_CIS_HIA_ONBOARD_MOMENTS_data(self):
        del_data('*')
        trange = ['2001-02-01T00:00:00Z', '2001-02-04T00:00:00Z']
        mom_data = pyspedas.projects.cluster.load_csa(probes=['C1'],
                                             trange=trange,
                                             datatypes=['CP_CIS-HIA_ONBOARD_MOMENTS'], time_clip=True)
        print(mom_data)
        self.assertTrue('density__C1_CP_CIS_HIA_ONBOARD_MOMENTS' in mom_data)
        self.assertTrue(data_exists('density__C1_CP_CIS_HIA_ONBOARD_MOMENTS'))

    # This test uses a different time range from test_load_csa_CP_CIS_HIA_ONBOARD_MOMENTS_data,
    # and loads for all four probes.
    def test_load_csa_mom_data(self):
        del_data('*')
        mom_data = pyspedas.projects.cluster.load_csa(probes=['C1', 'C2', 'C3', 'C4'],
                                             trange=['2003-08-17/16:40', '2003-08-17/16:45'],
                                             datatypes=['CP_CIS-HIA_ONBOARD_MOMENTS'], time_clip=True)
        self.assertTrue('density__C1_CP_CIS_HIA_ONBOARD_MOMENTS' in mom_data)
        self.assertTrue(data_exists('density__C1_CP_CIS_HIA_ONBOARD_MOMENTS'))


    def test_load_csa_CP_CIS_HIA_PAD_HS_MAG_IONS_PF_data(self):
        del_data('*')
        trange = ['2001-02-01T00:00:00Z', '2001-02-04T00:00:00Z']
        mom_data = pyspedas.projects.cluster.load_csa(probes=['C1'],
                                             trange=trange,
                                             datatypes=['CP_CIS-HIA_PAD_HS_MAG_IONS_PF'], time_clip=True)
        print(mom_data)
        self.assertTrue('Differential_Particle_Flux__C1_CP_CIS_HIA_PAD_HS_MAG_IONS_PF' in mom_data)
        self.assertTrue(data_exists('Differential_Particle_Flux__C1_CP_CIS_HIA_PAD_HS_MAG_IONS_PF'))

    def test_load_csa_CP_EDI_AEDC_data(self):
        del_data('*')
        trange = ['2005-08-01T00:00:00Z', '2005-08-02T00:00:00Z']
        edi_data = pyspedas.projects.cluster.load_csa(probes=['C1'],
                                             trange=trange,
                                             datatypes=['CP_EDI_AEDC'], time_clip=True)
        print(edi_data)
        self.assertTrue('counts_GDU1_PA_90__C1_CP_EDI_AEDC' in edi_data)
        self.assertTrue(data_exists('counts_GDU1_PA_90__C1_CP_EDI_AEDC'))

    def test_load_csa_CP_EDI_MP_data(self):
        del_data('*')
        trange = ['2001-02-01T00:00:00Z', '2001-02-04T00:00:00Z']
        edi_data = pyspedas.projects.cluster.load_csa(probes=['C1'],
                                             trange=trange,
                                             datatypes=['CP_EDI_MP'], time_clip=True)
        self.assertTrue('V_ed_xyz_gse__C1_CP_EDI_MP' in edi_data)
        self.assertTrue(data_exists('V_ed_xyz_gse__C1_CP_EDI_MP'))

    def test_load_csa_CP_EDI_SPIN_data(self):
        del_data('*')
        trange = ['2001-02-01T00:00:00Z', '2001-02-04T00:00:00Z']
        edi_data = pyspedas.projects.cluster.load_csa(probes=['C1'],
                                             trange=trange,
                                             datatypes=['CP_EDI_SPIN'], time_clip=True)
        self.assertTrue('V_ed_xyz_gse__C1_CP_EDI_SPIN' in edi_data)
        self.assertTrue(data_exists('V_ed_xyz_gse__C1_CP_EDI_SPIN'))

    # multidimensional DEPEND_0 array for dsettings/caveat variables
    def test_load_csa_CP_EFW_L2_E3D_INERT_data(self):
        del_data('*')
        trange = ['2001-02-01T00:00:00Z', '2001-02-02T00:00:00Z']
        efw_data = pyspedas.projects.cluster.load_csa(probes=['C1'],
                                             trange=trange,
                                             datatypes=['CP_EFW_L2_E3D_INERT'], time_clip=True)
        self.assertTrue('E_Vec_xyz_ISR2__C1_CP_EFW_L2_E3D_INERT' in efw_data)
        self.assertTrue(data_exists('E_Vec_xyz_ISR2__C1_CP_EFW_L2_E3D_INERT'))

    def test_load_csa_CP_EFW_L2_P_data(self):
        del_data('*')
        trange = ['2001-02-01T00:00:00Z', '2001-02-04T00:00:00Z']
        efw_data = pyspedas.projects.cluster.load_csa(probes=['C1'],
                                             trange=trange,
                                             datatypes=['CP_EFW_L2_P'], time_clip=True)
        self.assertTrue('Spacecraft_potential__C1_CP_EFW_L2_P' in efw_data)
        self.assertTrue(data_exists('Spacecraft_potential__C1_CP_EFW_L2_P'))

    def test_load_csa_CP_EFW_L2_V3D_INERT_data(self):
        del_data('*')
        trange = ['2001-02-01T00:00:00Z', '2001-02-02T00:00:00Z']
        efw_data = pyspedas.projects.cluster.load_csa(probes=['C1'],
                                             trange=trange,
                                             datatypes=['CP_EFW_L2_V3D_INERT'], time_clip=True)
        self.assertTrue('v_drift_ISR2__C1_CP_EFW_L2_V3D_INERT' in efw_data)
        self.assertTrue(data_exists('v_drift_ISR2__C1_CP_EFW_L2_V3D_INERT'))

    def test_load_csa_CP_EFW_L3_E3D_INERT_data(self):
        del_data('*')
        trange = ['2001-02-01T00:00:00Z', '2001-02-02T00:00:00Z']
        efw_data = pyspedas.projects.cluster.load_csa(probes=['C1'],
                                             trange=trange,
                                             datatypes=['CP_EFW_L3_E3D_INERT'], time_clip=True)
        self.assertTrue('E_Vec_xyz_ISR2__C1_CP_EFW_L3_E3D_INERT' in efw_data)
        self.assertTrue(data_exists('E_Vec_xyz_ISR2__C1_CP_EFW_L3_E3D_INERT'))

    def test_load_csa_CP_EFW_L3_P_data(self):
        del_data('*')
        trange = ['2001-02-01T00:00:00Z', '2001-02-02T00:00:00Z']
        efw_data = pyspedas.projects.cluster.load_csa(probes=['C1'],
                                             trange=trange,
                                             datatypes=['CP_EFW_L3_P'], time_clip=True)
        self.assertTrue('Spacecraft_potential__C1_CP_EFW_L3_P' in efw_data)
        self.assertTrue(data_exists('Spacecraft_potential__C1_CP_EFW_L3_P'))

    def test_load_csa_CP_EFW_L3_V3D_INERT_data(self):
        del_data('*')
        trange = ['2001-02-01T00:00:00Z', '2001-02-02T00:00:00Z']
        efw_data = pyspedas.projects.cluster.load_csa(probes=['C1'],
                                             trange=trange,
                                             datatypes=['CP_EFW_L3_V3D_INERT'], time_clip=True)
        self.assertTrue('v_drift_ISR2__C1_CP_EFW_L3_V3D_INERT' in efw_data)
        self.assertTrue(data_exists('v_drift_ISR2__C1_CP_EFW_L3_V3D_INERT'))

    def test_load_csa_CP_FGM_5VPS_data(self):
        del_data('*')
        trange = ['2001-02-01T00:00:00Z', '2001-02-02T00:00:00Z']
        fgm_data = pyspedas.projects.cluster.load_csa(probes=['C1'],
                                             trange=trange,
                                             datatypes=['CP_FGM_5VPS'], time_clip=True)
        self.assertTrue('B_vec_xyz_gse__C1_CP_FGM_5VPS' in fgm_data)
        self.assertTrue(data_exists('B_vec_xyz_gse__C1_CP_FGM_5VPS'))

    def test_load_csa_CP_FGM_FULL_data(self):
        del_data('*')
        trange = ['2001-02-01T00:00:00Z', '2001-02-02T00:00:00Z']
        fgm_data = pyspedas.projects.cluster.load_csa(probes=['C1'],
                                             trange=trange,
                                             datatypes=['CP_FGM_FULL'], time_clip=True)
        self.assertTrue('B_vec_xyz_gse__C1_CP_FGM_FULL' in fgm_data)
        self.assertTrue(data_exists('B_vec_xyz_gse__C1_CP_FGM_FULL'))

    def test_load_csa_CP_FGM_SPIN_data(self):
        del_data('*')
        trange = ['2001-02-01T00:00:00Z', '2001-02-02T00:00:00Z']
        fgm_data = pyspedas.projects.cluster.load_csa(probes=['C1'],
                                             trange=trange,
                                             datatypes=['CP_FGM_SPIN'], time_clip=True)
        self.assertTrue('B_vec_xyz_gse__C1_CP_FGM_SPIN' in fgm_data)
        self.assertTrue(data_exists('B_vec_xyz_gse__C1_CP_FGM_SPIN'))

    def test_load_csa_CP_PEA_MOMENTS_data(self):
        del_data('*')
        trange = ['2001-02-01T00:00:00Z', '2001-02-02T00:00:00Z']
        mom_data = pyspedas.projects.cluster.load_csa(probes=['C1'],
                                             trange=trange,
                                             datatypes=['CP_PEA_MOMENTS'], time_clip=True)
        self.assertTrue('Data_Density__C1_CP_PEA_MOMENTS' in mom_data)
        self.assertTrue(data_exists('Data_Density__C1_CP_PEA_MOMENTS'))

    # multidimensional DEPEND_0 array for dsettings/caveat variables
    def test_load_csa_CP_PEA_PITCH_SPIN_DEFlux_data(self):
        del_data('*')
        trange = ['2001-02-01T00:00:00Z', '2001-02-02T00:00:00Z']
        pea_data = pyspedas.projects.cluster.load_csa(probes=['C1'],
                                             trange=trange,
                                             datatypes=['CP_PEA_PITCH_SPIN_DEFlux'], time_clip=True)
        self.assertTrue('Data__C1_CP_PEA_PITCH_SPIN_DEFlux' in pea_data)
        self.assertTrue(data_exists('Data__C1_CP_PEA_PITCH_SPIN_DEFlux'))

    # multidimensional DEPEND_0 array for dsettings/caveat variables
    def test_load_csa_CP_PEA_PITCH_SPIN_DPFlux_data(self):
        del_data('*')
        trange = ['2001-02-01T00:00:00Z', '2001-02-02T00:00:00Z']
        pea_data = pyspedas.projects.cluster.load_csa(probes=['C1'],
                                             trange=trange,
                                             datatypes=['CP_PEA_PITCH_SPIN_DPFlux'], time_clip=True)
        self.assertTrue('Data__C1_CP_PEA_PITCH_SPIN_DPFlux' in pea_data)
        self.assertTrue(data_exists('Data__C1_CP_PEA_PITCH_SPIN_DPFlux'))

    # multidimensional DEPEND_0 array for dsettings/caveat variables
    def test_load_csa_CP_PEA_PITCH_SPIN_PSD_data(self):
        del_data('*')
        trange = ['2001-02-01T00:00:00Z', '2001-02-02T00:00:00Z']
        pea_data = pyspedas.projects.cluster.load_csa(probes=['C1'],
                                             trange=trange,
                                             datatypes=['CP_PEA_PITCH_SPIN_PSD'], time_clip=True)
        self.assertTrue('Data__C1_CP_PEA_PITCH_SPIN_PSD' in pea_data)
        self.assertTrue(data_exists('Data__C1_CP_PEA_PITCH_SPIN_PSD'))

    def test_load_csa_CP_RAP_ESPCT6_data(self):
        del_data('*')
        trange = ['2008-02-03T00:00:00Z', '2008-02-05T00:00:00Z']
        rap_data = pyspedas.projects.cluster.load_csa(probes=['C1'],
                                             trange=trange,
                                             datatypes=['CP_RAP_ESPCT6'], time_clip=True)
        print(rap_data)
        self.assertTrue('Electron_Dif_flux__C1_CP_RAP_ESPCT6' in rap_data)
        self.assertTrue(data_exists('Electron_Dif_flux__C1_CP_RAP_ESPCT6'))

    # multidimensional DEPEND_0 array for dsettings/caveat variables
    def test_load_csa_CP_RAP_ESPCT6_R_data(self):
        del_data('*')
        trange = ['2001-02-01T00:00:00Z', '2001-02-02T00:00:00Z']
        rap_data = pyspedas.projects.cluster.load_csa(probes=['C1'],
                                             trange=trange,
                                             datatypes=['CP_RAP_ESPCT6_R'], time_clip=True)
        self.assertTrue('Electron_Rate__C1_CP_RAP_ESPCT6_R' in rap_data)
        self.assertTrue(data_exists('Electron_Rate__C1_CP_RAP_ESPCT6_R'))

    # multidimensional DEPEND_0 array for dsettings/caveat variables
    def test_load_csa_CP_RAP_HSPCT_data(self):
        del_data('*')
        trange = ['2001-02-01T00:00:00Z', '2001-02-02T00:00:00Z']
        rap_data = pyspedas.projects.cluster.load_csa(probes=['C1'],
                                             trange=trange,
                                             datatypes=['CP_RAP_HSPCT'], time_clip=True)
        self.assertTrue('Proton_Dif_flux__C1_CP_RAP_HSPCT' in rap_data)
        self.assertTrue(data_exists('Proton_Dif_flux__C1_CP_RAP_HSPCT'))

    # multidimensional DEPEND_0 array for dsettings/caveat variables
    def test_load_csa_CP_RAP_HSPCT_R_data(self):
        del_data('*')
        trange = ['2001-02-01T00:00:00Z', '2001-02-02T00:00:00Z']
        rap_data = pyspedas.projects.cluster.load_csa(probes=['C1'],
                                             trange=trange,
                                             datatypes=['CP_RAP_HSPCT_R'], time_clip=True)
        self.assertTrue('Proton_Rate__C1_CP_RAP_HSPCT_R' in rap_data)
        self.assertTrue(data_exists('Proton_Rate__C1_CP_RAP_HSPCT_R'))

    # multidimensional DEPEND_0 array for dsettings/caveat variables
    def test_load_csa_CP_RAP_ISPCT_CNO_data(self):
        del_data('*')
        trange = ['2001-02-01T00:00:00Z', '2001-02-02T00:00:00Z']
        rap_data = pyspedas.projects.cluster.load_csa(probes=['C1'],
                                             trange=trange,
                                             datatypes=['CP_RAP_ISPCT_CNO'], time_clip=True)
        self.assertTrue('CNO_Dif_flux__C1_CP_RAP_ISPCT_CNO' in rap_data)
        self.assertTrue(data_exists('CNO_Dif_flux__C1_CP_RAP_ISPCT_CNO'))

    # multidimensional DEPEND_0 array for dsettings/caveat variables
    def test_load_csa_CP_RAP_ISPCT_He_data(self):
        del_data('*')
        trange = ['2001-02-01T00:00:00Z', '2001-02-02T00:00:00Z']
        rap_data = pyspedas.projects.cluster.load_csa(probes=['C1'],
                                             trange=trange,
                                             datatypes=['CP_RAP_ISPCT_He'], time_clip=True)
        self.assertTrue('Helium_Dif_flux__C1_CP_RAP_ISPCT_He' in rap_data)
        self.assertTrue(data_exists('Helium_Dif_flux__C1_CP_RAP_ISPCT_He'))

    # This date returns data, but it's large enough (tens of megabytes that there's a significant
    # chance of the server not completing the request.
    @unittest.skip
    def test_load_csa_CP_STA_CS_HBR_data(self):
        del_data('*')
        trange = ['2001-01-31T00:00:00Z', '2001-01-31T23:59:59Z']
        sta_data = pyspedas.projects.cluster.load_csa(probes=['C1'],
                                             trange=trange,
                                             datatypes=['CP_STA_CS_HBR'], time_clip=True)
        print(sta_data)
        self.assertTrue('Complex_Spectrum__C1_CP_STA_CS_HBR' in sta_data)
        self.assertTrue(data_exists('Complex_Spectrum__C1_CP_STA_CS_HBR'))

    # This date returns data, but it's large enough (tens of megabytes that there's a significant
    # chance of the server not completing the request.
    @unittest.skip
    def test_load_csa_CP_STA_CS_NBR_data(self):
        del_data('*')
        trange = ['2001-01-31T00:00:00Z', '2001-01-31T23:59:59Z']
        sta_data = pyspedas.projects.cluster.load_csa(probes=['C1'],
                                             trange=trange,
                                             datatypes=['CP_STA_CS_NBR'], time_clip=True)
        print(sta_data)
        self.assertTrue('Complex_Spectrum__C1_CP_STA_CS_NBR' in sta_data)
        self.assertTrue(data_exists('Complex_Spectrum__C1_CP_STA_CS_NBR'))

    def test_load_csa_CP_STA_CWF_GSE_data(self):
        del_data('*')
        trange = ['2001-02-01T00:00:00Z', '2001-02-02T00:00:00Z']
        sta_data = pyspedas.projects.cluster.load_csa(probes=['C1'],
                                             trange=trange,
                                             datatypes=['CP_STA_CWF_GSE'], time_clip=True)
        self.assertTrue('B_vec_xyz_Instrument__C1_CP_STA_CWF_GSE' in sta_data)
        self.assertTrue(data_exists('B_vec_xyz_Instrument__C1_CP_STA_CWF_GSE'))

    # 404 error, no data?
    @unittest.skip
    def test_load_csa_CP_STA_CWF_HBR_ISR2_data(self):
        del_data('*')
        trange = ['2001-02-01T00:00:00Z', '2001-02-02T00:00:00Z']
        sta_data = pyspedas.projects.cluster.load_csa(probes=['C1'],
                                             trange=trange,
                                             datatypes=['CP_STA_CWF_HBR_ISR2'], time_clip=True)
        print(sta_data)
        self.assertTrue('B_vec_xyz_Instrument__C1_CP_STA_CWF_GSE' in sta_data)
        self.assertTrue(data_exists('B_vec_xyz_Instrument__C1_CP_STA_CWF_GSE'))

    # 404 error, no data?
    @unittest.skip
    def test_load_csa_CP_STA_CWF_NBR_ISR2_data(self):
        del_data('*')
        trange = ['2001-02-01T00:00:00Z', '2001-02-02T00:00:00Z']
        sta_data = pyspedas.projects.cluster.load_csa(probes=['C1'],
                                             trange=trange,
                                             datatypes=['CP_STA_CWF_NBR_ISR2'], time_clip=True)
        print(sta_data)
        self.assertTrue('B_vec_xyz_Instrument__C1_CP_STA_CWF_GSE' in sta_data)
        self.assertTrue(data_exists('B_vec_xyz_Instrument__C1_CP_STA_CWF_GSE'))

    # Spectrogram variables have string-valued DEPEND_2, which is not ISTP compliant.
    def test_load_csa_CP_STA_PSD_data(self):
        del_data('*')
        trange = ['2001-02-01T00:00:00Z', '2001-02-02T00:00:00Z']
        sta_data = pyspedas.projects.cluster.load_csa(probes=['C1'],
                                             trange=trange,
                                             datatypes=['CP_STA_PSD'], time_clip=True)
        print(sta_data)
        #self.assertTrue('B_vec_xyz_Instrument__C1_CP_STA_CWF_GSE' in sta_data)
        #self.assertTrue(data_exists('B_vec_xyz_Instrument__C1_CP_STA_CWF_GSE'))

    def test_load_csa_CP_WBD_WAVEFORM_data(self):
        del_data('*')
        trange = ['2001-02-04T13:40:00Z', '2001-02-04T13:49:59Z']
        wbd_data = pyspedas.projects.cluster.load_csa(probes=['C1'],
                                             trange=trange,
                                             datatypes=['CP_WBD_WAVEFORM'], time_clip=True)
        print(wbd_data)
        self.assertTrue('E__C1_CP_WBD_WAVEFORM' in wbd_data)
        self.assertTrue(data_exists('E__C1_CP_WBD_WAVEFORM'))

    def test_load_csa_CP_WHI_ELECTRON_DENSITY_data(self):
        del_data('*')
        trange = ['2018-01-12T00:00:00Z', '2018-01-13T00:00:00Z']
        whi_data = pyspedas.projects.cluster.load_csa(probes=['C1'],
                                             trange=trange,
                                             datatypes=['CP_WHI_ELECTRON_DENSITY'], time_clip=True)
        print(whi_data)
        self.assertTrue('Electron_Density__C1_CP_WHI_ELECTRON_DENSITY' in whi_data)
        self.assertTrue(data_exists('Electron_Density__C1_CP_WHI_ELECTRON_DENSITY'))

    def test_load_csa_CP_CP_WHI_NATURAL_data(self):
        del_data('*')
        trange = ['2001-02-01T00:00:00Z', '2001-02-02T00:00:00Z']
        whi_data = pyspedas.projects.cluster.load_csa(probes=['C1'],
                                             trange=trange,
                                             datatypes=['CP_WHI_NATURAL'], time_clip=True)
        self.assertTrue('Electric_Spectral_Power_Density__C1_CP_WHI_NATURAL' in whi_data)
        self.assertTrue(data_exists('Electric_Spectral_Power_Density__C1_CP_WHI_NATURAL'))

    def test_load_csa_JP_AUX_PMP_data(self):
        del_data('*')
        trange = ['2017-01-01T00:00:00Z', '2017-02-01T00:00:00Z']
        jp_data = pyspedas.projects.cluster.load_csa(probes=['C1'],
                                            trange=trange,
                                            datatypes=['JP_AUX_PMP'], time_clip=True)
        print(jp_data)
        self.assertTrue('L_value__C1_JP_AUX_PMP' in jp_data)
        self.assertTrue(data_exists('L_value__C1_JP_AUX_PMP'))

    def test_load_csa_JP_PSE_data(self):
        del_data('*')
        trange = ['2017-01-01T00:00:00Z', '2018-01-02T00:00:00Z']
        jp_data = pyspedas.projects.cluster.load_csa(probes=['C1'],
                                            trange=trange,
                                            datatypes=['JP_AUX_PSE'], time_clip=True)
        print(jp_data)
        self.assertTrue('sc_r1_xyz_gse__C1_JP_AUX_PSE' in jp_data)
        self.assertTrue(data_exists('sc_r1_xyz_gse__C1_JP_AUX_PSE'))


if __name__ == '__main__':
    unittest.main()
