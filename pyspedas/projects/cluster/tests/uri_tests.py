import os
import time
import requests
import unittest
import subprocess

from pytplot import data_exists
from pyspedas.projects.cluster import load_csa, config

#==========================================================

# moto server mock details
localhost = "http://localhost:3000"
bucket_name = "test-bucket"

# Set up mock AWS environment variables (fake credentials)
os.environ["AWS_ACCESS_KEY_ID"] = "test"
os.environ["AWS_SECRET_ACCESS_KEY"] = "test"
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

# Set environment to use the local Moto S3 server
# S3 ENDPOINT for fsspec
# ENDPOINT URL for cdflib/boto3
os.environ["AWS_S3_ENDPOINT"] = localhost
os.environ["AWS_ENDPOINT_URL"] = localhost

class LoadTestCases(unittest.TestCase):
    """
    Cloud Awareness Unit Tests

    Depends upon moto[server] package. Install via:
        pip install moto[server]

    These tests essentially create a local mock-AWS server as a background
    process at port 3000.
    Note: The environment variables are used as mock credentials in order
          to avoid having to pass the endpoint url to fsspec calls.
    """

    @classmethod
    def setUpClass(cls):
        # Start the moto server for S3 in the background
        # https://github.com/getmoto/moto/issues/4418
        cls.moto_server = subprocess.Popen(
                ["moto_server", "-p3000"],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        # Allow the server to start properly
        time.sleep(2)

        # Create a bucket using direct HTTP requests
        response = requests.put(f"http://localhost:3000/{bucket_name}")
        assert response.status_code == 200, "Bucket creation failed"

    @classmethod
    def tearDownClass(cls):
        # Terminate the moto server after tests
        cls.moto_server.terminate()
        cls.moto_server.communicate()
    
    def clean_data(self):
        # reset moto server to original state
        response = requests.post("http://localhost:3000/moto-api/reset")
        assert response.status_code == 200, "Moto Server reset failed"
        
        # create bucket again
        response = requests.put(f"http://localhost:3000/{bucket_name}")
        assert response.status_code == 200, "Bucket creation failed"

    #==========================================================================
    # Cloud Awareness Note: Cluster implementation does not stream data due to
    #                       lack of functionality already present in PySPEDAS.

    # Adapted unit tests for AWS-specific URI testing.
    def test_load_csa_CE_WBD_WAVEFORM_CDF_data(self):
        self.clean_data()
        config.CONFIG['local_data_dir'] = f"s3://{bucket_name}"

        trange = ['2012-11-06T02:19:00Z', '2012-11-06T02:19:59Z']
        wbd_data = load_csa(probes=['C1'],
                            trange=trange,
                            datatypes=['CE_WBD_WAVEFORM_CDF'], time_clip=True)
        print(wbd_data)
        self.assertTrue('WBD_Elec' in wbd_data)
        self.assertTrue(data_exists('WBD_Elec'))
    
    def test_load_csa_CP_AUX_POSGSE_1M_data(self):
        self.clean_data()
        config.CONFIG['local_data_dir'] = f"s3://{bucket_name}"

        trange = ['2001-02-01T00:00:00Z', '2001-02-04T00:00:00Z']
        pos_data = load_csa(probes=['C1'],
                            trange=trange,
                            datatypes=['CP_AUX_POSGSE_1M'], time_clip=True)
        self.assertTrue('sc_r_xyz_gse__C1_CP_AUX_POSGSE_1M' in pos_data)
        self.assertTrue(data_exists('sc_r_xyz_gse__C1_CP_AUX_POSGSE_1M'))
    
    def test_load_csa_CP_AUX_POSGSE_1M_data_prefix_none(self):
        self.clean_data()
        config.CONFIG['local_data_dir'] = f"s3://{bucket_name}"

        trange = ['2001-02-01T00:00:00Z', '2001-02-04T00:00:00Z']
        pos_data = load_csa(probes=['C1'],
                            trange=trange,
                            prefix=None,
                            datatypes=['CP_AUX_POSGSE_1M'], time_clip=True)
        self.assertTrue('sc_r_xyz_gse__C1_CP_AUX_POSGSE_1M' in pos_data)
        self.assertTrue(data_exists('sc_r_xyz_gse__C1_CP_AUX_POSGSE_1M'))
    
    def test_load_csa_CP_AUX_POSGSE_1M_data_suffix_none(self):
        self.clean_data()
        config.CONFIG['local_data_dir'] = f"s3://{bucket_name}"

        trange = ['2001-02-01T00:00:00Z', '2001-02-04T00:00:00Z']
        pos_data = load_csa(probes=['C1'],
                            trange=trange,
                            suffix=None,
                            datatypes=['CP_AUX_POSGSE_1M'], time_clip=True)
        self.assertTrue('sc_r_xyz_gse__C1_CP_AUX_POSGSE_1M' in pos_data)
        self.assertTrue(data_exists('sc_r_xyz_gse__C1_CP_AUX_POSGSE_1M'))
    
    def test_load_csa_CP_AUX_POSGSE_1M_data_prefix_suffix(self):
        self.clean_data()
        config.CONFIG['local_data_dir'] = f"s3://{bucket_name}"

        trange = ['2001-02-01T00:00:00Z', '2001-02-04T00:00:00Z']
        pos_data = load_csa(probes=['C1'],
                            trange=trange,
                            prefix='pre_',
                            suffix='_suf',
                            datatypes=['CP_AUX_POSGSE_1M'], time_clip=True)
        self.assertTrue('pre_sc_r_xyz_gse__C1_CP_AUX_POSGSE_1M_suf' in pos_data)
        self.assertTrue(data_exists('pre_sc_r_xyz_gse__C1_CP_AUX_POSGSE_1M_suf'))
    
    def test_load_csa_CP_CIS_CODIF_HS_H1_MOMENTS_data(self):
        self.clean_data()
        config.CONFIG['local_data_dir'] = f"s3://{bucket_name}"

        trange = ['2001-02-01T00:00:00Z', '2001-02-04T00:00:00Z']
        mom_data = load_csa(probes=['C1'],
                            trange=trange,
                            datatypes=['CP_CIS-CODIF_HS_H1_MOMENTS'], time_clip=True)
        print(mom_data)
        self.assertTrue('density__C1_CP_CIS_CODIF_HS_H1_MOMENTS' in mom_data)
        self.assertTrue(data_exists('density__C1_CP_CIS_CODIF_HS_H1_MOMENTS'))

    def test_load_csa_CP_CIS_CODIF_HS_He1_MOMENTS_data(self):
        self.clean_data()
        config.CONFIG['local_data_dir'] = f"s3://{bucket_name}"

        trange = ['2001-02-01T00:00:00Z', '2001-02-04T00:00:00Z']
        mom_data = load_csa(probes=['C1'],
                            trange=trange,
                            datatypes=['CP_CIS-CODIF_HS_He1_MOMENTS'], time_clip=True)
        print(mom_data)
        self.assertTrue('density__C1_CP_CIS_CODIF_HS_He1_MOMENTS' in mom_data)
        self.assertTrue(data_exists('density__C1_CP_CIS_CODIF_HS_He1_MOMENTS'))

    def test_load_csa_CP_CIS_CODIF_HS_O1_MOMENTS_data(self):
        self.clean_data()
        config.CONFIG['local_data_dir'] = f"s3://{bucket_name}"

        trange = ['2001-02-01T00:00:00Z', '2001-02-04T00:00:00Z']
        mom_data = load_csa(probes=['C1'],
                            trange=trange,
                            datatypes=['CP_CIS-CODIF_HS_O1_MOMENTS'], time_clip=True)
        print(mom_data)
        self.assertTrue('density__C1_CP_CIS_CODIF_HS_O1_MOMENTS' in mom_data)
        self.assertTrue(data_exists('density__C1_CP_CIS_CODIF_HS_O1_MOMENTS'))

    def test_load_csa_CP_CIS_CODIF_PAD_HS_H1_PF_data(self):
        self.clean_data()
        config.CONFIG['local_data_dir'] = f"s3://{bucket_name}"

        trange = ['2001-02-01T00:00:00Z', '2001-02-04T00:00:00Z']
        mom_data = load_csa(probes=['C1'],
                            trange=trange,
                            datatypes=['CP_CIS-CODIF_PAD_HS_H1_PF'], time_clip=True)
        print(mom_data)
        self.assertTrue('Differential_Particle_Flux__C1_CP_CIS_CODIF_PAD_HS_H1_PF' in mom_data)
        self.assertTrue(data_exists('Differential_Particle_Flux__C1_CP_CIS_CODIF_PAD_HS_H1_PF'))

    def test_load_csa_CP_CIS_CODIF_PAD_HS_He1_PF_data(self):
        self.clean_data()
        config.CONFIG['local_data_dir'] = f"s3://{bucket_name}"

        trange = ['2001-02-01T00:00:00Z', '2001-02-04T00:00:00Z']
        mom_data = load_csa(probes=['C1'],
                            trange=trange,
                            datatypes=['CP_CIS-CODIF_PAD_HS_He1_PF'], time_clip=True)
        print(mom_data)
        self.assertTrue('Differential_Particle_Flux__C1_CP_CIS_CODIF_PAD_HS_He1_PF' in mom_data)
        self.assertTrue(data_exists('Differential_Particle_Flux__C1_CP_CIS_CODIF_PAD_HS_He1_PF'))

    def test_load_csa_CP_CIS_CODIF_PAD_HS_O1_PF_data(self):
        self.clean_data()
        config.CONFIG['local_data_dir'] = f"s3://{bucket_name}"

        trange = ['2001-02-01T00:00:00Z', '2001-02-04T00:00:00Z']
        mom_data = load_csa(probes=['C1'],
                            trange=trange,
                            datatypes=['CP_CIS-CODIF_PAD_HS_O1_PF'], time_clip=True)
        print(mom_data)
        self.assertTrue('Differential_Particle_Flux__C1_CP_CIS_CODIF_PAD_HS_O1_PF' in mom_data)
        self.assertTrue(data_exists('Differential_Particle_Flux__C1_CP_CIS_CODIF_PAD_HS_O1_PF'))

    def test_load_csa_CP_CIS_HIA_ONBOARD_MOMENTS_data(self):
        self.clean_data()
        config.CONFIG['local_data_dir'] = f"s3://{bucket_name}"

        trange = ['2001-02-01T00:00:00Z', '2001-02-04T00:00:00Z']
        mom_data = load_csa(probes=['C1'],
                            trange=trange,
                            datatypes=['CP_CIS-HIA_ONBOARD_MOMENTS'], time_clip=True)
        print(mom_data)
        self.assertTrue('density__C1_CP_CIS_HIA_ONBOARD_MOMENTS' in mom_data)
        self.assertTrue(data_exists('density__C1_CP_CIS_HIA_ONBOARD_MOMENTS'))

    # This test uses a different time range from test_load_csa_CP_CIS_HIA_ONBOARD_MOMENTS_data,
    # and loads for all four probes.
    def test_load_csa_mom_data(self):
        self.clean_data()
        config.CONFIG['local_data_dir'] = f"s3://{bucket_name}"

        mom_data = load_csa(probes=['C1', 'C2', 'C3', 'C4'],
                            trange=['2003-08-17/16:40', '2003-08-17/16:45'],
                            datatypes=['CP_CIS-HIA_ONBOARD_MOMENTS'], time_clip=True)
        self.assertTrue('density__C1_CP_CIS_HIA_ONBOARD_MOMENTS' in mom_data)
        self.assertTrue(data_exists('density__C1_CP_CIS_HIA_ONBOARD_MOMENTS'))

    def test_load_csa_CP_CIS_HIA_PAD_HS_MAG_IONS_PF_data(self):
        self.clean_data()
        config.CONFIG['local_data_dir'] = f"s3://{bucket_name}"

        trange = ['2001-02-01T00:00:00Z', '2001-02-04T00:00:00Z']
        mom_data = load_csa(probes=['C1'],
                            trange=trange,
                            datatypes=['CP_CIS-HIA_PAD_HS_MAG_IONS_PF'], time_clip=True)
        print(mom_data)
        self.assertTrue('Differential_Particle_Flux__C1_CP_CIS_HIA_PAD_HS_MAG_IONS_PF' in mom_data)
        self.assertTrue(data_exists('Differential_Particle_Flux__C1_CP_CIS_HIA_PAD_HS_MAG_IONS_PF'))

    def test_load_csa_CP_EDI_AEDC_data(self):
        self.clean_data()
        config.CONFIG['local_data_dir'] = f"s3://{bucket_name}"

        trange = ['2005-08-01T00:00:00Z', '2005-08-02T00:00:00Z']
        edi_data = load_csa(probes=['C1'],
                            trange=trange,
                            datatypes=['CP_EDI_AEDC'], time_clip=True)
        print(edi_data)
        self.assertTrue('counts_GDU1_PA_90__C1_CP_EDI_AEDC' in edi_data)
        self.assertTrue(data_exists('counts_GDU1_PA_90__C1_CP_EDI_AEDC'))

    def test_load_csa_CP_EDI_MP_data(self):
        self.clean_data()
        config.CONFIG['local_data_dir'] = f"s3://{bucket_name}"

        trange = ['2001-02-01T00:00:00Z', '2001-02-04T00:00:00Z']
        edi_data = load_csa(probes=['C1'],
                            trange=trange,
                            datatypes=['CP_EDI_MP'], time_clip=True)
        self.assertTrue('V_ed_xyz_gse__C1_CP_EDI_MP' in edi_data)
        self.assertTrue(data_exists('V_ed_xyz_gse__C1_CP_EDI_MP'))

    def test_load_csa_CP_EDI_SPIN_data(self):
        self.clean_data()
        config.CONFIG['local_data_dir'] = f"s3://{bucket_name}"

        trange = ['2001-02-01T00:00:00Z', '2001-02-04T00:00:00Z']
        edi_data = load_csa(probes=['C1'],
                            trange=trange,
                            datatypes=['CP_EDI_SPIN'], time_clip=True)
        self.assertTrue('V_ed_xyz_gse__C1_CP_EDI_SPIN' in edi_data)
        self.assertTrue(data_exists('V_ed_xyz_gse__C1_CP_EDI_SPIN'))

    # multidimensional DEPEND_0 array for dsettings/caveat variables
    def test_load_csa_CP_EFW_L2_E3D_INERT_data(self):
        self.clean_data()
        config.CONFIG['local_data_dir'] = f"s3://{bucket_name}"

        trange = ['2001-02-01T00:00:00Z', '2001-02-02T00:00:00Z']
        efw_data = load_csa(probes=['C1'],
                            trange=trange,
                            datatypes=['CP_EFW_L2_E3D_INERT'], time_clip=True)
        self.assertTrue('E_Vec_xyz_ISR2__C1_CP_EFW_L2_E3D_INERT' in efw_data)
        self.assertTrue(data_exists('E_Vec_xyz_ISR2__C1_CP_EFW_L2_E3D_INERT'))

    def test_load_csa_CP_EFW_L2_P_data(self):
        self.clean_data()
        config.CONFIG['local_data_dir'] = f"s3://{bucket_name}"

        trange = ['2001-02-01T00:00:00Z', '2001-02-04T00:00:00Z']
        efw_data = load_csa(probes=['C1'],
                            trange=trange,
                            datatypes=['CP_EFW_L2_P'], time_clip=True)
        self.assertTrue('Spacecraft_potential__C1_CP_EFW_L2_P' in efw_data)
        self.assertTrue(data_exists('Spacecraft_potential__C1_CP_EFW_L2_P'))

    def test_load_csa_CP_EFW_L2_V3D_INERT_data(self):
        self.clean_data()
        config.CONFIG['local_data_dir'] = f"s3://{bucket_name}"

        trange = ['2001-02-01T00:00:00Z', '2001-02-02T00:00:00Z']
        efw_data = load_csa(probes=['C1'],
                            trange=trange,
                            datatypes=['CP_EFW_L2_V3D_INERT'], time_clip=True)
        self.assertTrue('v_drift_ISR2__C1_CP_EFW_L2_V3D_INERT' in efw_data)
        self.assertTrue(data_exists('v_drift_ISR2__C1_CP_EFW_L2_V3D_INERT'))

    def test_load_csa_CP_EFW_L3_E3D_INERT_data(self):
        self.clean_data()
        config.CONFIG['local_data_dir'] = f"s3://{bucket_name}"

        trange = ['2001-02-01T00:00:00Z', '2001-02-02T00:00:00Z']
        efw_data = load_csa(probes=['C1'],
                            trange=trange,
                            datatypes=['CP_EFW_L3_E3D_INERT'], time_clip=True)
        self.assertTrue('E_Vec_xyz_ISR2__C1_CP_EFW_L3_E3D_INERT' in efw_data)
        self.assertTrue(data_exists('E_Vec_xyz_ISR2__C1_CP_EFW_L3_E3D_INERT'))

    def test_load_csa_CP_EFW_L3_P_data(self):
        self.clean_data()
        config.CONFIG['local_data_dir'] = f"s3://{bucket_name}"

        trange = ['2001-02-01T00:00:00Z', '2001-02-02T00:00:00Z']
        efw_data = load_csa(probes=['C1'],
                            trange=trange,
                            datatypes=['CP_EFW_L3_P'], time_clip=True)
        self.assertTrue('Spacecraft_potential__C1_CP_EFW_L3_P' in efw_data)
        self.assertTrue(data_exists('Spacecraft_potential__C1_CP_EFW_L3_P'))

    def test_load_csa_CP_EFW_L3_V3D_INERT_data(self):
        self.clean_data()
        config.CONFIG['local_data_dir'] = f"s3://{bucket_name}"

        trange = ['2001-02-01T00:00:00Z', '2001-02-02T00:00:00Z']
        efw_data = load_csa(probes=['C1'],
                            trange=trange,
                            datatypes=['CP_EFW_L3_V3D_INERT'], time_clip=True)
        self.assertTrue('v_drift_ISR2__C1_CP_EFW_L3_V3D_INERT' in efw_data)
        self.assertTrue(data_exists('v_drift_ISR2__C1_CP_EFW_L3_V3D_INERT'))

    def test_load_csa_CP_FGM_5VPS_data(self):
        self.clean_data()
        config.CONFIG['local_data_dir'] = f"s3://{bucket_name}"

        trange = ['2001-02-01T00:00:00Z', '2001-02-02T00:00:00Z']
        fgm_data = load_csa(probes=['C1'],
                            trange=trange,
                            datatypes=['CP_FGM_5VPS'], time_clip=True)
        self.assertTrue('B_vec_xyz_gse__C1_CP_FGM_5VPS' in fgm_data)
        self.assertTrue(data_exists('B_vec_xyz_gse__C1_CP_FGM_5VPS'))

    def test_load_csa_CP_FGM_FULL_data(self):
        self.clean_data()
        config.CONFIG['local_data_dir'] = f"s3://{bucket_name}"

        trange = ['2001-02-01T00:00:00Z', '2001-02-02T00:00:00Z']
        fgm_data = load_csa(probes=['C1'],
                            trange=trange,
                            datatypes=['CP_FGM_FULL'], time_clip=True)
        self.assertTrue('B_vec_xyz_gse__C1_CP_FGM_FULL' in fgm_data)
        self.assertTrue(data_exists('B_vec_xyz_gse__C1_CP_FGM_FULL'))

    def test_load_csa_CP_FGM_SPIN_data(self):
        self.clean_data()
        config.CONFIG['local_data_dir'] = f"s3://{bucket_name}"

        trange = ['2001-02-01T00:00:00Z', '2001-02-02T00:00:00Z']
        fgm_data = load_csa(probes=['C1'],
                            trange=trange,
                            datatypes=['CP_FGM_SPIN'], time_clip=True)
        self.assertTrue('B_vec_xyz_gse__C1_CP_FGM_SPIN' in fgm_data)
        self.assertTrue(data_exists('B_vec_xyz_gse__C1_CP_FGM_SPIN'))

    def test_load_csa_CP_PEA_MOMENTS_data(self):
        self.clean_data()
        config.CONFIG['local_data_dir'] = f"s3://{bucket_name}"

        trange = ['2001-02-01T00:00:00Z', '2001-02-02T00:00:00Z']
        mom_data = load_csa(probes=['C1'],
                            trange=trange,
                            datatypes=['CP_PEA_MOMENTS'], time_clip=True)
        self.assertTrue('Data_Density__C1_CP_PEA_MOMENTS' in mom_data)
        self.assertTrue(data_exists('Data_Density__C1_CP_PEA_MOMENTS'))

    # multidimensional DEPEND_0 array for dsettings/caveat variables
    def test_load_csa_CP_PEA_PITCH_SPIN_DEFlux_data(self):
        self.clean_data()
        config.CONFIG['local_data_dir'] = f"s3://{bucket_name}"

        trange = ['2001-02-01T00:00:00Z', '2001-02-02T00:00:00Z']
        pea_data = load_csa(probes=['C1'],
                            trange=trange,
                            datatypes=['CP_PEA_PITCH_SPIN_DEFlux'], time_clip=True)
        self.assertTrue('Data__C1_CP_PEA_PITCH_SPIN_DEFlux' in pea_data)
        self.assertTrue(data_exists('Data__C1_CP_PEA_PITCH_SPIN_DEFlux'))

    # multidimensional DEPEND_0 array for dsettings/caveat variables
    def test_load_csa_CP_PEA_PITCH_SPIN_DPFlux_data(self):
        self.clean_data()
        config.CONFIG['local_data_dir'] = f"s3://{bucket_name}"

        trange = ['2001-02-01T00:00:00Z', '2001-02-02T00:00:00Z']
        pea_data = load_csa(probes=['C1'],
                            trange=trange,
                            datatypes=['CP_PEA_PITCH_SPIN_DPFlux'], time_clip=True)
        self.assertTrue('Data__C1_CP_PEA_PITCH_SPIN_DPFlux' in pea_data)
        self.assertTrue(data_exists('Data__C1_CP_PEA_PITCH_SPIN_DPFlux'))

    # multidimensional DEPEND_0 array for dsettings/caveat variables
    def test_load_csa_CP_PEA_PITCH_SPIN_PSD_data(self):
        self.clean_data()
        config.CONFIG['local_data_dir'] = f"s3://{bucket_name}"

        trange = ['2001-02-01T00:00:00Z', '2001-02-02T00:00:00Z']
        pea_data = load_csa(probes=['C1'],
                            trange=trange,
                            datatypes=['CP_PEA_PITCH_SPIN_PSD'], time_clip=True)
        self.assertTrue('Data__C1_CP_PEA_PITCH_SPIN_PSD' in pea_data)
        self.assertTrue(data_exists('Data__C1_CP_PEA_PITCH_SPIN_PSD'))

    # compressed file error
    @unittest.skip
    def test_load_csa_CP_RAP_ESPCT6_data(self):
        self.clean_data()
        config.CONFIG['local_data_dir'] = f"s3://{bucket_name}"

        trange = ['2008-02-03T00:00:00Z', '2008-02-05T00:00:00Z']
        rap_data = load_csa(probes=['C1'],
                            trange=trange,
                            datatypes=['CP_RAP_ESPCT6'], time_clip=True)
        print(rap_data)
        self.assertTrue('Electron_Dif_flux__C1_CP_RAP_ESPCT6' in rap_data)
        self.assertTrue(data_exists('Electron_Dif_flux__C1_CP_RAP_ESPCT6'))

    # multidimensional DEPEND_0 array for dsettings/caveat variables
    def test_load_csa_CP_RAP_ESPCT6_R_data(self):
        self.clean_data()
        config.CONFIG['local_data_dir'] = f"s3://{bucket_name}"

        trange = ['2001-02-01T00:00:00Z', '2001-02-02T00:00:00Z']
        rap_data = load_csa(probes=['C1'],
                            trange=trange,
                            datatypes=['CP_RAP_ESPCT6_R'], time_clip=True)
        self.assertTrue('Electron_Rate__C1_CP_RAP_ESPCT6_R' in rap_data)
        self.assertTrue(data_exists('Electron_Rate__C1_CP_RAP_ESPCT6_R'))

    # multidimensional DEPEND_0 array for dsettings/caveat variables
    def test_load_csa_CP_RAP_HSPCT_data(self):
        self.clean_data()
        config.CONFIG['local_data_dir'] = f"s3://{bucket_name}"

        trange = ['2001-02-01T00:00:00Z', '2001-02-02T00:00:00Z']
        rap_data = load_csa(probes=['C1'],
                            trange=trange,
                            datatypes=['CP_RAP_HSPCT'], time_clip=True)
        self.assertTrue('Proton_Dif_flux__C1_CP_RAP_HSPCT' in rap_data)
        self.assertTrue(data_exists('Proton_Dif_flux__C1_CP_RAP_HSPCT'))

    # multidimensional DEPEND_0 array for dsettings/caveat variables
    def test_load_csa_CP_RAP_HSPCT_R_data(self):
        self.clean_data()
        config.CONFIG['local_data_dir'] = f"s3://{bucket_name}"

        trange = ['2001-02-01T00:00:00Z', '2001-02-02T00:00:00Z']
        rap_data = load_csa(probes=['C1'],
                            trange=trange,
                            datatypes=['CP_RAP_HSPCT_R'], time_clip=True)
        self.assertTrue('Proton_Rate__C1_CP_RAP_HSPCT_R' in rap_data)
        self.assertTrue(data_exists('Proton_Rate__C1_CP_RAP_HSPCT_R'))

    # multidimensional DEPEND_0 array for dsettings/caveat variables
    def test_load_csa_CP_RAP_ISPCT_CNO_data(self):
        self.clean_data()
        config.CONFIG['local_data_dir'] = f"s3://{bucket_name}"

        trange = ['2001-02-01T00:00:00Z', '2001-02-02T00:00:00Z']
        rap_data = load_csa(probes=['C1'],
                            trange=trange,
                            datatypes=['CP_RAP_ISPCT_CNO'], time_clip=True)
        self.assertTrue('CNO_Dif_flux__C1_CP_RAP_ISPCT_CNO' in rap_data)
        self.assertTrue(data_exists('CNO_Dif_flux__C1_CP_RAP_ISPCT_CNO'))

    # multidimensional DEPEND_0 array for dsettings/caveat variables
    def test_load_csa_CP_RAP_ISPCT_He_data(self):
        self.clean_data()
        config.CONFIG['local_data_dir'] = f"s3://{bucket_name}"

        trange = ['2001-02-01T00:00:00Z', '2001-02-02T00:00:00Z']
        rap_data = load_csa(probes=['C1'],
                            trange=trange,
                            datatypes=['CP_RAP_ISPCT_He'], time_clip=True)
        self.assertTrue('Helium_Dif_flux__C1_CP_RAP_ISPCT_He' in rap_data)
        self.assertTrue(data_exists('Helium_Dif_flux__C1_CP_RAP_ISPCT_He'))

    # This date returns data, but it's large enough (tens of megabytes that there's a significant
    # chance of the server not completing the request.
    @unittest.skip
    def test_load_csa_CP_STA_CS_HBR_data(self):
        self.clean_data()
        config.CONFIG['local_data_dir'] = f"s3://{bucket_name}"

        trange = ['2001-01-31T00:00:00Z', '2001-01-31T23:59:59Z']
        sta_data = load_csa(probes=['C1'],
                            trange=trange,
                            datatypes=['CP_STA_CS_HBR'], time_clip=True)
        print(sta_data)
        self.assertTrue('Complex_Spectrum__C1_CP_STA_CS_HBR' in sta_data)
        self.assertTrue(data_exists('Complex_Spectrum__C1_CP_STA_CS_HBR'))

    # This date returns data, but it's large enough (tens of megabytes that there's a significant
    # chance of the server not completing the request.
    @unittest.skip
    def test_load_csa_CP_STA_CS_NBR_data(self):
        self.clean_data()
        config.CONFIG['local_data_dir'] = f"s3://{bucket_name}"

        trange = ['2001-01-31T00:00:00Z', '2001-01-31T23:59:59Z']
        sta_data = load_csa(probes=['C1'],
                            trange=trange,
                            datatypes=['CP_STA_CS_NBR'], time_clip=True)
        print(sta_data)
        self.assertTrue('Complex_Spectrum__C1_CP_STA_CS_NBR' in sta_data)
        self.assertTrue(data_exists('Complex_Spectrum__C1_CP_STA_CS_NBR'))

    # compressed file error
    @unittest.skip
    def test_load_csa_CP_STA_CWF_GSE_data(self):
        self.clean_data()
        config.CONFIG['local_data_dir'] = f"s3://{bucket_name}"

        trange = ['2001-02-01T00:00:00Z', '2001-02-02T00:00:00Z']
        sta_data = load_csa(probes=['C1'],
                            trange=trange,
                            datatypes=['CP_STA_CWF_GSE'], time_clip=True)
        self.assertTrue('B_vec_xyz_Instrument__C1_CP_STA_CWF_GSE' in sta_data)
        self.assertTrue(data_exists('B_vec_xyz_Instrument__C1_CP_STA_CWF_GSE'))

    # 404 error, no data?
    @unittest.skip
    def test_load_csa_CP_STA_CWF_HBR_ISR2_data(self):
        self.clean_data()
        config.CONFIG['local_data_dir'] = f"s3://{bucket_name}"

        trange = ['2001-02-01T00:00:00Z', '2001-02-02T00:00:00Z']
        sta_data = load_csa(probes=['C1'],
                            trange=trange,
                            datatypes=['CP_STA_CWF_HBR_ISR2'], time_clip=True)
        print(sta_data)
        self.assertTrue('B_vec_xyz_Instrument__C1_CP_STA_CWF_GSE' in sta_data)
        self.assertTrue(data_exists('B_vec_xyz_Instrument__C1_CP_STA_CWF_GSE'))

    # 404 error, no data?
    @unittest.skip
    def test_load_csa_CP_STA_CWF_NBR_ISR2_data(self):
        self.clean_data()
        config.CONFIG['local_data_dir'] = f"s3://{bucket_name}"

        trange = ['2001-02-01T00:00:00Z', '2001-02-02T00:00:00Z']
        sta_data = load_csa(probes=['C1'],
                            trange=trange,
                            datatypes=['CP_STA_CWF_NBR_ISR2'], time_clip=True)
        print(sta_data)
        self.assertTrue('B_vec_xyz_Instrument__C1_CP_STA_CWF_GSE' in sta_data)
        self.assertTrue(data_exists('B_vec_xyz_Instrument__C1_CP_STA_CWF_GSE'))

    # Spectrogram variables have string-valued DEPEND_2, which is not ISTP compliant.
    @unittest.skip
    def test_load_csa_CP_STA_PSD_data(self):
        self.clean_data()
        config.CONFIG['local_data_dir'] = f"s3://{bucket_name}"

        trange = ['2001-02-01T00:00:00Z', '2001-02-02T00:00:00Z']
        sta_data = load_csa(probes=['C1'],
                            trange=trange,
                            datatypes=['CP_STA_PSD'], time_clip=True)
        print(sta_data)
        #self.assertTrue('B_vec_xyz_Instrument__C1_CP_STA_CWF_GSE' in sta_data)
        #self.assertTrue(data_exists('B_vec_xyz_Instrument__C1_CP_STA_CWF_GSE'))

    # data load seemed rather large; potential timeout issue (works separately)
    @unittest.skip
    def test_load_csa_CP_WBD_WAVEFORM_data(self):
        self.clean_data()
        config.CONFIG['local_data_dir'] = f"s3://{bucket_name}"

        trange = ['2001-02-04T13:40:00Z', '2001-02-04T13:49:59Z']
        wbd_data = load_csa(probes=['C1'],
                            trange=trange,
                            datatypes=['CP_WBD_WAVEFORM'], time_clip=True)
        print(wbd_data)
        self.assertTrue('E__C1_CP_WBD_WAVEFORM' in wbd_data)
        self.assertTrue(data_exists('E__C1_CP_WBD_WAVEFORM'))

    def test_load_csa_CP_WHI_ELECTRON_DENSITY_data(self):
        self.clean_data()
        config.CONFIG['local_data_dir'] = f"s3://{bucket_name}"

        trange = ['2018-01-12T00:00:00Z', '2018-01-13T00:00:00Z']
        whi_data = load_csa(probes=['C1'],
                            trange=trange,
                            datatypes=['CP_WHI_ELECTRON_DENSITY'], time_clip=True)
        print(whi_data)
        self.assertTrue('Electron_Density__C1_CP_WHI_ELECTRON_DENSITY' in whi_data)
        self.assertTrue(data_exists('Electron_Density__C1_CP_WHI_ELECTRON_DENSITY'))

    def test_load_csa_CP_CP_WHI_NATURAL_data(self):
        self.clean_data()
        config.CONFIG['local_data_dir'] = f"s3://{bucket_name}"

        trange = ['2001-02-01T00:00:00Z', '2001-02-02T00:00:00Z']
        whi_data = load_csa(probes=['C1'],
                            trange=trange,
                            datatypes=['CP_WHI_NATURAL'], time_clip=True)
        self.assertTrue('Electric_Spectral_Power_Density__C1_CP_WHI_NATURAL' in whi_data)
        self.assertTrue(data_exists('Electric_Spectral_Power_Density__C1_CP_WHI_NATURAL'))

    def test_load_csa_JP_AUX_PMP_data(self):
        self.clean_data()
        config.CONFIG['local_data_dir'] = f"s3://{bucket_name}"

        trange = ['2017-01-01T00:00:00Z', '2017-02-01T00:00:00Z']
        jp_data = load_csa(probes=['C1'],
                           trange=trange,
                           datatypes=['JP_AUX_PMP'], time_clip=True)
        print(jp_data)
        self.assertTrue('L_value__C1_JP_AUX_PMP' in jp_data)
        self.assertTrue(data_exists('L_value__C1_JP_AUX_PMP'))

    def test_load_csa_JP_PSE_data(self):
        self.clean_data()
        config.CONFIG['local_data_dir'] = f"s3://{bucket_name}"

        trange = ['2017-01-01T00:00:00Z', '2018-01-02T00:00:00Z']
        jp_data = load_csa(probes=['C1'],
                           trange=trange,
                           datatypes=['JP_AUX_PSE'], time_clip=True)
        print(jp_data)
        self.assertTrue('sc_r1_xyz_gse__C1_JP_AUX_PSE' in jp_data)
        self.assertTrue(data_exists('sc_r1_xyz_gse__C1_JP_AUX_PSE'))

if __name__ == '__main__':
    unittest.main(verbosity=2)
