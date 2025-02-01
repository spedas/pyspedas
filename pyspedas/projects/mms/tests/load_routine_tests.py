import unittest
from unittest.mock import patch, Mock
import numpy as np
from pyspedas.projects.mms import mms_load_state, mms_load_tetrahedron_qf, mms_load_mec, mms_load_fgm, mms_load_scm, mms_load_fpi, mms_load_hpca, mms_load_feeps, mms_load_edp, mms_load_edi, mms_load_aspoc, mms_load_dsp
from pytplot import data_exists
from pyspedas.projects.mms.hpca_tools.mms_hpca_calc_anodes import mms_hpca_calc_anodes
from pyspedas.projects.mms.hpca_tools.mms_hpca_spin_sum import mms_hpca_spin_sum
from pyspedas.projects.mms.hpca_tools.mms_get_hpca_info import mms_get_hpca_info
from pyspedas import tdpwrspc
import pyspedas
from pytplot import get_data, del_data, tplot
import logging


class FSMLoadTestCases(unittest.TestCase):
    def test_load_basic(self):
        files = pyspedas.projects.mms.fsm(trange=['2015-10-16/06:00', '2015-10-16/06:05'], available=True)
        fsm = pyspedas.projects.mms.fsm(trange=['2015-10-16/06:00', '2015-10-16/06:05'])
        self.assertTrue(data_exists('mms1_fsm_b_mag_brst_l3'))
        self.assertTrue(data_exists('mms1_fsm_b_gse_brst_l3'))
        tplot(['mms1_fsm_b_mag_brst_l3', 'mms1_fsm_b_gse_brst_l3'], display=False)


class StateLoadTestCases(unittest.TestCase):
    def test_load_eph_no_update(self):
        data = mms_load_state(datatypes=['pos', 'vel']) # ensure the files are stored locally
        del_data('*') # remove the current tplot vars
        data = mms_load_state(datatypes=['pos', 'vel'], no_update=True) # ensure the files are stored locally
        self.assertTrue(data_exists('mms1_defeph_pos'))
        self.assertTrue(data_exists('mms1_defeph_vel'))
        self.assertTrue('mms1_defeph_pos' in data)
        self.assertTrue('mms1_defeph_vel' in data)

    def test_load_eph_data(self):
        data = mms_load_state(datatypes=['pos', 'vel'])
        self.assertTrue(data_exists('mms1_defeph_pos'))
        self.assertTrue(data_exists('mms1_defeph_vel'))
        tplot(['mms1_defeph_pos', 'mms1_defeph_vel'], display=False)
        self.assertTrue('mms1_defeph_pos' in data)
        self.assertTrue('mms1_defeph_vel' in data)

    @patch('requests.Session.get')
    def test_load_eph_data_sdc_503_response(self, mock_get):
        # Create a mock response object with a 503 status code
        mock_response = Mock()
        mock_response.status_code = 503
        mock_response.text = "Service Unavailable"

        # Set the mock object to be returned by sdc_session.get()
        mock_get.return_value = mock_response

        # Run the function and verify that the logging warnings were called
        with self.assertLogs(level='WARNING') as log:
            mms_load_state(datatypes=['pos', 'vel'])
            self.assertIn("Request to MMS SDC returned HTTP status code 503", log.output[0])
            self.assertIn("Text: Service Unavailable", log.output[1])
            self.assertIn("URL:", log.output[2])


    def test_load_eph_multiprobe_data(self):
        data = mms_load_state(datatypes=['pos', 'vel'],probe=['1','2','3','4'])
        self.assertTrue(data_exists('mms1_defeph_pos'))
        self.assertTrue(data_exists('mms1_defeph_vel'))
        tplot(['mms1_defeph_pos', 'mms1_defeph_vel'], display=False)
        self.assertTrue('mms1_defeph_pos' in data)
        self.assertTrue('mms1_defeph_vel' in data)
        self.assertTrue('mms2_defeph_pos' in data)
        self.assertTrue('mms2_defeph_vel' in data)
        self.assertTrue('mms3_defeph_pos' in data)
        self.assertTrue('mms3_defeph_vel' in data)
        self.assertTrue('mms4_defeph_pos' in data)
        self.assertTrue('mms4_defeph_vel' in data)

    def test_load_tqf(self):
        data = mms_load_tetrahedron_qf()
        self.assertTrue(data_exists('mms_tetrahedron_qf'))
        tplot('mms_tetrahedron_qf',display=False)
        self.assertTrue('mms_tetrahedron_qf' in data)

    @patch('requests.Session.get')
    def test_load_tqf_sdc_503_response(self, mock_get):
        # Create a mock response object with a 503 status code
        mock_response = Mock()
        mock_response.status_code = 503
        mock_response.text = "Service Unavailable"

        # Set the mock object to be returned by sdc_session.get()
        mock_get.return_value = mock_response

        # Run the function and verify that the logging warnings were called
        with self.assertLogs(level='WARNING') as log:
            data = mms_load_tetrahedron_qf()
            self.assertIn("Request to MMS SDC returned HTTP status code 503", log.output[0])
            self.assertIn("Text: Service Unavailable", log.output[1])
            self.assertIn("URL:", log.output[2])

    def test_load_tqf_no_update(self):
        data = mms_load_tetrahedron_qf()  # Ensure that some data is downloaded
        del_data('mms_tetrahedron_qf')    # Delete the tplot variable
        data = mms_load_tetrahedron_qf(no_update=True)  # Ensure that it can be loaded from previously downloaded files
        self.assertTrue(data_exists('mms_tetrahedron_qf'))
        self.assertTrue('mms_tetrahedron_qf' in data)
        tplot('mms_tetrahedron_qf',display=False)

    def test_load_att_data(self):
        data = mms_load_state(trange=['2015-10-16', '2015-10-16/06:00'], datatypes=['spinras', 'spindec'])
        self.assertTrue(data_exists('mms1_defatt_spinras'))
        self.assertTrue(data_exists('mms1_defatt_spindec'))
        self.assertTrue('mms1_defatt_spinras' in data)
        self.assertTrue('mms1_defatt_spindec' in data)
        tplot(['mms1_defatt_spinras', 'mms1_defatt_spindec'], display=False)


############### DSP ############### 
class DSPLoadTestCases(unittest.TestCase):
    # def test_load_default_data(self):
    #     data = mms_load_dsp(trange=['2015-08-01','2015-09-01'], datatype='swd', level='l2', data_rate='fast')
    #     self.assertTrue(data_exists('mms1_dsp_swd_E12_Counts'))

    def test_load_epsd_bpsd_data(self):
        data = mms_load_dsp(trange=['2015-08-01','2015-08-02'], datatype=['epsd', 'bpsd'], level='l2', data_rate='fast')
        self.assertTrue(data_exists('mms1_dsp_epsd_omni'))
        self.assertTrue(data_exists('mms1_dsp_bpsd_omni'))
        tplot(['mms1_dsp_epsd_omni', 'mms1_dsp_bpsd_omni'], display=False)

    def test_load_bpsd_data(self):
        data = mms_load_dsp(trange=['2015-10-16','2015-10-17'], datatype='bpsd', level='l2', data_rate='fast', available=True)
        data = mms_load_dsp(trange=['2015-10-16','2015-10-17'], datatype='bpsd', level='l2', data_rate='fast')
        self.assertTrue(data_exists('mms1_dsp_bpsd_omni_fast_l2'))
        tplot(['mms1_dsp_bpsd_omni_fast_l2'], display=False)

    def test_load_epsd_spdf(self):
        data = mms_load_dsp(trange=['2015-08-01','2015-08-02'], datatype='epsd', level='l2', data_rate='fast', spdf=True)
        self.assertTrue(data_exists('mms1_dsp_epsd_omni'))
        tplot(['mms1_dsp_epsd_omni'], display=False)

    def test_load_epsd_suffix(self):
        data = mms_load_dsp(trange=['2015-08-01','2015-08-02'], datatype='epsd', level='l2', data_rate='fast', suffix='_test')
        self.assertTrue(data_exists('mms1_dsp_epsd_omni_test'))
        tplot(['mms1_dsp_epsd_omni_test'], display=False)


############### FEEPS ############### 
# class FEEPSLoadTestCases(unittest.TestCase):
#     def test_load_default_data(self):
#         data = mms_load_feeps(trange=['2015-10-16', '2015-10-16/01:00'], available=True)
#         data = mms_load_feeps(trange=['2015-10-16', '2015-10-16/01:00'])
#         self.assertTrue(data_exists('mms1_epd_feeps_srvy_l2_electron_intensity_omni'))
#         self.assertTrue(data_exists('mms1_epd_feeps_srvy_l2_electron_intensity_omni_spin'))
#
#     def test_load_spdf_data(self):
#         del_data('*')
#         data = mms_load_feeps(trange=['2015-10-16/13:06', '2015-10-16/13:07'], data_rate='brst', spdf=True)
#         self.assertTrue(data_exists('mms1_epd_feeps_brst_l2_electron_intensity_omni'))
#         self.assertTrue(data_exists('mms1_epd_feeps_brst_l2_electron_intensity_omni_spin'))
#
#     def test_load_suffix(self):
#         data = mms_load_feeps(trange=['2015-10-16/13:06', '2015-10-16/13:07'], data_rate='brst', suffix='_test')
#         self.assertTrue(data_exists('mms1_epd_feeps_brst_l2_electron_intensity_omni_test'))
#         self.assertTrue(data_exists('mms1_epd_feeps_brst_l2_electron_intensity_omni_spin_test'))
#
#     def test_load_brst_ion_data(self):
#         del_data('*')
#         data = mms_load_feeps(probe=4, data_rate='brst', datatype='ion', trange=['2015-10-01/10:48:16', '2015-10-01/10:49:16'])
#         self.assertTrue(data_exists('mms4_epd_feeps_brst_l2_ion_intensity_omni'))
#         self.assertTrue(data_exists('mms4_epd_feeps_brst_l2_ion_intensity_omni_spin'))
#
#     def test_load_brst_multi_probe(self):
#         del_data('*')
#         data = mms_load_feeps(trange=['2015-10-16/13:06', '2015-10-16/13:07'], data_rate='brst', probe=[1, 2, 3, 4])
#         self.assertTrue(data_exists('mms1_epd_feeps_brst_l2_electron_intensity_omni'))
#         self.assertTrue(data_exists('mms1_epd_feeps_brst_l2_electron_intensity_omni_spin'))
#         self.assertTrue(data_exists('mms2_epd_feeps_brst_l2_electron_intensity_omni'))
#         self.assertTrue(data_exists('mms2_epd_feeps_brst_l2_electron_intensity_omni_spin'))
#         self.assertTrue(data_exists('mms3_epd_feeps_brst_l2_electron_intensity_omni'))
#         self.assertTrue(data_exists('mms3_epd_feeps_brst_l2_electron_intensity_omni_spin'))
#         self.assertTrue(data_exists('mms4_epd_feeps_brst_l2_electron_intensity_omni'))
#         self.assertTrue(data_exists('mms4_epd_feeps_brst_l2_electron_intensity_omni_spin'))



############### HPCA ############### 
class HPCALoadTestCases(unittest.TestCase):
    def test_load_default_data(self):
        data = mms_load_hpca(trange=['2015-10-16', '2015-10-16/01:00'], available=True)
        data = mms_load_hpca(trange=['2015-10-16', '2015-10-16/01:00'])
        self.assertTrue(data_exists('mms1_hpca_hplus_number_density'))
        tplot(['mms1_hpca_hplus_number_density'], display=False)

    def test_load_spdf_data(self):
        data = mms_load_hpca(trange=['2015-10-16', '2015-10-16/01:00'], spdf=True)
        self.assertTrue(data_exists('mms1_hpca_hplus_number_density'))
        tplot(['mms1_hpca_hplus_number_density'], display=False)

    def test_load_ion_omni_suffix(self):
        del_data('*')
        data = mms_load_hpca(probe=2, trange=['2016-08-09/09:10', '2016-08-09/10:10:00'], datatype='ion', data_rate='brst', suffix='_brst')
        mms_hpca_calc_anodes(fov=[0, 360], probe=2, suffix='_brst')
        mms_hpca_spin_sum(probe=2, suffix='_brst', avg=True)
        self.assertTrue(data_exists('mms2_hpca_hplus_flux_brst_elev_0-360_spin'))
        tplot(['mms2_hpca_hplus_flux_brst_elev_0-360_spin'], display=False)

    def test_load_ion_omni(self):
        del_data('*')
        data = mms_load_hpca(trange=['2016-10-16', '2016-10-16/6:00'], datatype='ion')
        mms_hpca_calc_anodes(fov=[0, 360], probe='1')
        mms_hpca_spin_sum()
        self.assertTrue(data_exists('mms1_hpca_hplus_flux_elev_0-360_spin'))
        self.assertTrue(data_exists('mms1_hpca_heplus_flux_elev_0-360_spin'))
        self.assertTrue(data_exists('mms1_hpca_heplusplus_flux_elev_0-360_spin'))
        self.assertTrue(data_exists('mms1_hpca_oplus_flux_elev_0-360_spin'))
        tplot(['mms1_hpca_hplus_flux_elev_0-360_spin',
               'mms1_hpca_heplus_flux_elev_0-360_spin',
               'mms1_hpca_heplusplus_flux_elev_0-360_spin',
               'mms1_hpca_oplus_flux_elev_0-360_spin'], display=False)

    def test_center_fast_moments_data(self):
        data = mms_load_hpca(trange=['2015-10-16/14:00', '2015-10-16/15:00'])
        centered = mms_load_hpca(trange=['2015-10-16/14:00', '2015-10-16/15:00'], center_measurement=True, suffix='_centered')
        
        t, d = get_data('mms1_hpca_hplus_ion_bulk_velocity')
        c, d = get_data('mms1_hpca_hplus_ion_bulk_velocity_centered')
        self.assertTrue(np.round(c[0]-t[0], decimals=3) == 5.0)

    def test_center_brst_moments_data(self):
        data = mms_load_hpca(trange=['2015-10-16/13:06', '2015-10-16/13:07'], data_rate='brst')
        centered = mms_load_hpca(trange=['2015-10-16/13:06', '2015-10-16/13:07'], data_rate='brst', center_measurement=True, suffix='_centered')
        
        t, d = get_data('mms1_hpca_hplus_ion_bulk_velocity')
        c, d = get_data('mms1_hpca_hplus_ion_bulk_velocity_centered')
        self.assertTrue(np.round(c[0]-t[0], decimals=3) == 5.0)

    def test_hpca_info(self):
        info = mms_get_hpca_info()
        self.assertTrue(list(info.keys()) == ['elevation', 't_spin', 't_sweep', 'azimuth_energy_offset'])


############### EDI ############### 
class EDILoadTestCases(unittest.TestCase):
    def test_load_default_data(self):
        data = mms_load_edi(trange=['2016-10-17/13:00', '2016-10-17/14:00'], available=True)
        data = mms_load_edi(trange=['2016-10-17/13:00', '2016-10-17/14:00'])
        self.assertTrue(data_exists('mms1_edi_e_gse_srvy_l2'))
        tplot(['mms1_edi_e_gse_srvy_l2'], display=False)

    def test_load_spdf_data(self):
        data = mms_load_edi(trange=['2016-10-17/13:00', '2016-10-17/14:00'], spdf=True)
        self.assertTrue(data_exists('mms1_edi_e_gse_srvy_l2'))
        tplot(['mms1_edi_e_gse_srvy_l2'], display=False)

    def test_load_suffix(self):
        data = mms_load_edi(trange=['2016-10-17/13:00', '2016-10-17/14:00'], suffix='_test')
        self.assertTrue(data_exists('mms1_edi_e_gse_srvy_l2_test'))
        tplot(['mms1_edi_e_gse_srvy_l2_test'], display=False)


############### ASPOC ############### 
class ASPOCLoadTestCases(unittest.TestCase):
    def test_load_default_data(self):
        data = mms_load_aspoc(trange=['2015-10-16', '2015-10-16/01:00'], available=True)
        data = mms_load_aspoc(trange=['2015-10-16', '2015-10-16/01:00'])
        self.assertTrue(data_exists('mms1_aspoc_ionc_l2'))
        tplot(['mms1_aspoc_ionc_l2'], display=False)

    def test_load_spdf_data(self):
        data = mms_load_aspoc(trange=['2015-10-16', '2015-10-16/01:00'], spdf=True)
        self.assertTrue(data_exists('mms1_aspoc_ionc_l2'))

    def test_load_suffix(self):
        data = mms_load_aspoc(trange=['2015-10-16', '2015-10-16/01:00'], suffix='_test')
        self.assertTrue(data_exists('mms1_aspoc_ionc_l2_test'))


############### EDP ############### 
class EDPLoadTestCases(unittest.TestCase):
    def test_load_default_data(self):
        data = mms_load_edp(trange=['2015-10-16', '2015-10-16/01:00'], available=True)
        data = mms_load_edp(trange=['2015-10-16', '2015-10-16/01:00'])
        self.assertTrue(data_exists('mms1_edp_dce_gse_fast_l2'))
        tplot(['mms1_edp_dce_gse_fast_l2'], display=False)

    def test_load_hfesp_data(self):
        data = mms_load_edp(trange=['2015-10-16', '2015-10-16/01:00'], datatype='hfesp', data_rate='srvy')
        self.assertTrue(data_exists('mms1_edp_hfesp_srvy_l2'))
        tplot(['mms1_edp_hfesp_srvy_l2'], display=False)

    def test_load_spdf_data(self):
        data = mms_load_edp(trange=['2015-10-16', '2015-10-16/01:00'], spdf=True)
        self.assertTrue(data_exists('mms1_edp_dce_gse_fast_l2'))
        tplot(['mms1_edp_dce_gse_fast_l2'], display=False)

    def test_load_suffix(self):
        data = mms_load_edp(trange=['2015-10-16', '2015-10-16/01:00'], suffix='_test')
        self.assertTrue(data_exists('mms1_edp_dce_gse_fast_l2'))

    # def test_load_multiple_sc(self):
    #     data = mms_load_edp(probe=['1', '2', '3', '4'], trange=['2015-10-16', '2015-10-16/01:00'])
    #     self.assertTrue(data_exists('mms1_edp_dce_gse_fast_l2'))
    #     self.assertTrue(data_exists('mms2_edp_dce_gse_fast_l2'))
    #     self.assertTrue(data_exists('mms3_edp_dce_gse_fast_l2'))
    #     self.assertTrue(data_exists('mms4_edp_dce_gse_fast_l2'))

    def test_load_brst_data(self):
        data = mms_load_edp(data_rate='brst', trange=['2015-10-16/13:06', '2015-10-16/13:10'])
        self.assertTrue(data_exists('mms1_edp_dce_gse_brst_l2'))
        tplot(['mms1_edp_dce_gse_brst_l2'], display=False)


############### FGM ############### 
class FGMLoadTestCases(unittest.TestCase):
    def test_regression_multi_imports_spdf(self):
        data = mms_load_fgm(data_rate='brst', trange=['2015-10-16/13:06', '2015-10-16/13:10'], spdf=True)
        t1, d1 = get_data('mms1_fgm_b_gse_brst_l2')
        data = mms_load_fgm(data_rate='brst', trange=['2015-10-16/13:06', '2015-10-16/13:10'], spdf=True)
        t2, d2 = get_data('mms1_fgm_b_gse_brst_l2')
        self.assertTrue(t1.shape == t2.shape)
        self.assertTrue(d1.shape == d2.shape)

    def test_load_default_data(self):
        data = mms_load_fgm(trange=['2015-10-16', '2015-10-16/01:00'],available=True)
        data = mms_load_fgm(trange=['2015-10-16', '2015-10-16/01:00'])
        self.assertTrue(data_exists('mms1_fgm_b_gse_srvy_l2'))
        self.assertTrue(data_exists('Epoch'))
        self.assertTrue(data_exists('Epoch_state'))
        tplot(['mms1_fgm_b_gse_srvy_l2'], display=False)

    def test_load_default_data_exclude(self):
        # Capture all log messages of level INFO or above
        with self.assertLogs(level=logging.INFO) as captured:
            # assertLogs fails if there are no log messages, so we make sure there's at least one
            logging.info("Dummy log message")
            data = mms_load_fgm(trange=['2015-10-16', '2015-10-16/01:00'],exclude_format='*rdeltahalf*',available=True)
            data = mms_load_fgm(trange=['2015-10-16', '2015-10-16/01:00'],exclude_format='*rdeltahalf*')
            self.assertTrue(data_exists('mms1_fgm_b_gse_srvy_l2'))
            self.assertTrue(data_exists('Epoch'))
            self.assertTrue(data_exists('Epoch_state'))
            tplot(['mms1_fgm_b_gse_srvy_l2'], display=False)
        # Assert that none of the log messages contain the string "rdeltahalf"
        logging.info("Captured log messages:")
        for rec in captured.records:
            logging.info(rec.msg)
            self.assertTrue("rdeltahalf" not in rec.msg)

    def test_load_spdf_data(self):
        data = mms_load_fgm(data_rate='brst', trange=['2015-10-16/13:06', '2015-10-16/13:10'], spdf=True)
        self.assertTrue(data_exists('mms1_fgm_b_gse_brst_l2'))

    def test_load_suffix(self):
        data = mms_load_fgm(data_rate='brst', trange=['2015-10-16/13:06', '2015-10-16/13:10'], suffix='_test')
        self.assertTrue(data_exists('mms1_fgm_b_gse_brst_l2_test'))

    def test_load_multiple_sc(self):
        data = mms_load_fgm(probe=[1, 2, 3, 4], data_rate='brst', trange=['2015-10-16/13:06', '2015-10-16/13:10'])
        self.assertTrue(data_exists('mms1_fgm_b_gse_brst_l2'))
        self.assertTrue(data_exists('mms2_fgm_b_gse_brst_l2'))
        self.assertTrue(data_exists('mms3_fgm_b_gse_brst_l2'))
        self.assertTrue(data_exists('mms4_fgm_b_gse_brst_l2'))

    def test_load_brst_data(self):
        data = mms_load_fgm(data_rate='brst', trange=['2015-10-16/13:06', '2015-10-16/13:10'])
        self.assertTrue(data_exists('mms1_fgm_b_gse_brst_l2'))
        tplot(['mms1_fgm_b_gse_brst_l2'], display=False)

    @patch('requests.Session.get')
    def test_load_fgm_sdc_503_response(self, mock_get):
        # Create a mock response object with a 503 status code
        mock_response = Mock()
        mock_response.status_code = 503
        mock_response.text = "Service Unavailable"

        # Set the mock object to be returned by sdc_session.get()
        mock_get.return_value = mock_response

        # Run the function and verify that the logging warnings were called
        with self.assertLogs(level='WARNING') as log:
            data = mms_load_fgm()
            self.assertIn("Request to MMS SDC returned HTTP status code 503", log.output[0])
            self.assertIn("Text: Service Unavailable", log.output[1])
            self.assertIn("URL:", log.output[2])


    def test_load_data_no_update(self):
        data = mms_load_fgm(trange=['2015-10-16', '2015-10-16/01:00']) # make sure the files exist locally
        del_data('*') 
        data = mms_load_fgm(trange=['2015-10-16', '2015-10-16/01:00'], no_update=True) # load the file from the local cache
        self.assertTrue(data_exists('mms1_fgm_b_gse_srvy_l2'))


############### MEC ###############
class MECLoadTestCases(unittest.TestCase):
    def test_load_default_data(self):
        data = mms_load_mec(trange=['2015-10-16', '2015-10-16/01:00'], available=True)
        data = mms_load_mec(trange=['2015-10-16', '2015-10-16/01:00'])
        self.assertTrue(data_exists('mms1_mec_r_sm'))
        tplot(['mms1_mec_r_sm'], display=False)

    def test_load_spdf_data(self):
        data = mms_load_mec(trange=['2015-10-16', '2015-10-16/01:00'], spdf=True)
        self.assertTrue(data_exists('mms1_mec_r_sm'))

    def test_load_suffix(self):
        data = mms_load_mec(trange=['2015-10-16', '2015-10-16/01:00'], suffix='_test')
        self.assertTrue(data_exists('mms1_mec_r_sm_test'))


class SCMLoadTestCases(unittest.TestCase):
    def test_brst_dpwrspc_data(self):
        data = mms_load_scm(probe=4, data_rate='brst', datatype='scb', trange=['2015-10-01/10:48:16', '2015-10-01/10:49:16'])
        tdpwrspc('mms4_scm_acb_gse_scb_brst_l2', notmvariance=True)
        self.assertTrue(data_exists('mms4_scm_acb_gse_scb_brst_l2'))
        self.assertTrue(data_exists('mms4_scm_acb_gse_scb_brst_l2_x_dpwrspc'))
        self.assertTrue(data_exists('mms4_scm_acb_gse_scb_brst_l2_y_dpwrspc'))
        self.assertTrue(data_exists('mms4_scm_acb_gse_scb_brst_l2_z_dpwrspc'))
        tplot(['mms4_scm_acb_gse_scb_brst_l2',
               'mms4_scm_acb_gse_scb_brst_l2_x_dpwrspc',
               'mms4_scm_acb_gse_scb_brst_l2_y_dpwrspc',
               'mms4_scm_acb_gse_scb_brst_l2_z_dpwrspc'], display=False)

    def test_load_default_data(self):
        data = mms_load_scm(trange=['2015-10-16', '2015-10-16/01:00'], available=True)
        data = mms_load_scm(trange=['2015-10-16', '2015-10-16/01:00'])
        self.assertTrue(data_exists('mms1_scm_acb_gse_scsrvy_srvy_l2'))

    def test_load_schb(self):
        data = pyspedas.projects.mms.scm(probe=4, data_rate='brst', datatype='schb', trange=['2015-10-01/10:48:16', '2015-10-01/10:49:16'])
        self.assertTrue(data_exists('mms4_scm_acb_gse_schb_brst_l2'))

    def test_load_suffix(self):
        data = mms_load_scm(trange=['2015-10-16', '2015-10-16/01:00'], suffix='_test')
        self.assertTrue(data_exists('mms1_scm_acb_gse_scsrvy_srvy_l2_test'))

    def test_load_multiple_sc(self):
        data = mms_load_scm(probe=['1', '2', '3', '4'], trange=['2017-12-15', '2017-12-16'])
        # self.assertTrue(data_exists('mms1_scm_acb_gse_scsrvy_srvy_l2'))
        # self.assertTrue(data_exists('mms2_scm_acb_gse_scsrvy_srvy_l2'))
        self.assertTrue(data_exists('mms3_scm_acb_gse_scsrvy_srvy_l2'))
        self.assertTrue(data_exists('mms4_scm_acb_gse_scsrvy_srvy_l2'))

    def test_load_brst_data(self):
        data = mms_load_scm(data_rate='brst', trange=['2015-10-16/13:06', '2015-10-16/13:10'], datatype='scb')
        self.assertTrue(data_exists('mms1_scm_acb_gse_scb_brst_l2'))

    def test_available(self):
        files = mms_load_scm(data_rate='brst', trange=['2015-10-16/13:06', '2015-10-16/13:10'], datatype='scb', available=True)
        self.assertTrue(len(files) == 2)


if __name__ == '__main__':
    unittest.main()
