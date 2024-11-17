import os
import unittest
from pytplot import data_exists
import pyspedas
from pytplot import del_data, tplot
from pyspedas.projects.rbsp.rbspice_lib.rbsp_rbspice_pad import rbsp_rbspice_pad

global_display=False

class LoadTestCases(unittest.TestCase):
    def tearDown(self):
        del_data('*')

    def test_downloadonly(self):
        files = pyspedas.projects.rbsp.efw(trange=['2015-11-3', '2015-11-4'], level='l3', downloadonly=True)
        self.assertTrue(os.path.exists(files[0]))

    def test_notplot(self):
        data = pyspedas.projects.rbsp.efw(trange=['2015-11-6', '2015-11-7'], level='l3', notplot=True)
        self.assertTrue('density' in data.keys())
        self.assertTrue('efield_in_inertial_frame_spinfit_mgse' in data.keys())
        self.assertTrue('x' in data['density'].keys())
        self.assertTrue('y' in data['density'].keys())

    def test_load_emfisis_data(self):
        del_data('*')
        emfisis_vars = pyspedas.projects.rbsp.emfisis(trange=['2018-11-5', '2018-11-6'], datatype='magnetometer', level='l3', time_clip=True)
        self.assertTrue(data_exists('Mag'))
        emfisis_vars = pyspedas.projects.rbsp.emfisis(trange=['2018-11-5', '2018-11-6'], datatype='magnetometer', level='l2')
        wfr_vars = pyspedas.projects.rbsp.emfisis(trange=['2018-11-5', '2018-11-6'], level='l2', datatype='wfr')
        hfr_vars = pyspedas.projects.rbsp.emfisis(trange=['2018-11-5', '2018-11-6'], level='l2', datatype='hfr')
        self.assertTrue(data_exists('Mag'))
        # WFR waveform data
        self.assertTrue(data_exists('BuSamples'))
        self.assertTrue(data_exists('BvSamples'))
        self.assertTrue(data_exists('BwSamples'))
        self.assertTrue(data_exists('EuSamples'))
        self.assertTrue(data_exists('EvSamples'))
        self.assertTrue(data_exists('EwSamples'))
        # HFR waveform data
        self.assertTrue(data_exists('HFRsamples'))
        # L4 density
        dens = pyspedas.projects.rbsp.emfisis(trange=['2018-11-5', '2018-11-6'], datatype='density', level='l4')
        self.assertTrue(data_exists('density'))

    def test_load_hfr_spectra(self):
        from pytplot import tplot
        del_data('*')
        pyspedas.projects.rbsp.emfisis(trange=['2013-01-17', '2013-01-18'], datatype='hfr', level='l2', wavetype='spectra')
        self.assertTrue(data_exists('HFR_Spectra'))
        tplot(['HFR_Spectra'], display=global_display, save_png='emphisis_hfr.png')

    def test_load_efw_data(self):
        del_data('*')
        efw_vars = pyspedas.projects.rbsp.efw(trange=['2015-11-5', '2015-11-6'], level='l2')
        self.assertTrue(data_exists('spec64_e12ac'))
        efw_vars = pyspedas.projects.rbsp.efw(trange=['2015-11-5', '2015-11-6'], level='l3')
        self.assertTrue(data_exists('density'))

    def test_load_rbspice_download(self):
        del_data('*')
        files = pyspedas.projects.rbsp.rbspice(downloadonly=True, trange=['2018-11-5', '2018-11-6'], datatype='tofxeh', level='l3')
        self.assertTrue(isinstance(files, list))

    def test_load_rbspice_esrhelt(self):
        del_data('*')
        rbspice_vars = pyspedas.projects.rbsp.rbspice(trange=['2013-11-5', '2013-11-6'], datatype='ESRHELT', level='l3')
        self.assertTrue(data_exists('rbspa_rbspice_l3_ESRHELT_FEDU'))

    def test_load_rbspice_esrhelt_prefix_none(self):
        del_data('*')
        rbspice_vars = pyspedas.projects.rbsp.rbspice(trange=['2013-11-5', '2013-11-6'], datatype='ESRHELT', level='l3', prefix=None)
        self.assertTrue(data_exists('rbspa_rbspice_l3_ESRHELT_FEDU'))

    def test_load_rbspice_esrhelt_suffix_none(self):
        del_data('*')
        rbspice_vars = pyspedas.projects.rbsp.rbspice(trange=['2013-11-5', '2013-11-6'], datatype='ESRHELT', level='l3', suffix=None)
        self.assertTrue(data_exists('rbspa_rbspice_l3_ESRHELT_FEDU'))

    def test_load_rbspice_esrhelt_prefix_suffix(self):
        del_data('*')
        rbspice_vars = pyspedas.projects.rbsp.rbspice(trange=['2013-11-5', '2013-11-6'], datatype='ESRHELT', level='l3', prefix='pre_', suffix='_suf')
        self.assertTrue(data_exists('pre_rbspa_rbspice_l3_ESRHELT_FEDU_suf'))

    def test_load_rbspice_data(self):
        del_data('*')
        data = pyspedas.projects.rbsp.rbspice(trange=['2018-11-5', '2018-11-6'], datatype='TOFxEH', level='l3')
        self.assertTrue(data_exists('rbspa_rbspice_l3_TOFxEH_proton_omni_spin'))
        self.assertTrue(data_exists('rbspa_rbspice_l3_TOFxEH_proton_omni'))
        rbsp_rbspice_pad(probe='a', datatype='TOFxEH', level='l3')
        rbsp_rbspice_pad(probe='a', datatype='TOFxEH', level='l3', scopes=[0, 1, 2, 3])
        self.assertTrue(data_exists('rbspa_rbspice_l3_TOFxEH_proton_omni_0-1000keV_pad'))
        self.assertTrue(data_exists('rbspa_rbspice_l3_TOFxEH_proton_omni_0-1000keV_pad_spin'))
        data = pyspedas.projects.rbsp.rbspice(trange=['2018-11-5', '2018-11-6'], datatype='TOFxPHHHELT')
        rbsp_rbspice_pad(probe='a', datatype='TOFxPHHHELT', level='l3')
        self.assertTrue(data_exists('rbspa_rbspice_l3_TOFxPHHHELT_oxygen_omni_spin'))
        self.assertTrue(data_exists('rbspa_rbspice_l3_TOFxPHHHELT_oxygen_omni_0-1000keV_pad_spin'))
        data = pyspedas.projects.rbsp.rbspice(trange=['2018-11-5', '2018-11-6'], datatype='TOFxEnonH')
        rbsp_rbspice_pad(probe='a', datatype='TOFxEnonH', level='l3')
        self.assertTrue(data_exists('rbspa_rbspice_l3_TOFxEnonH_oxygen_omni_spin'))
        self.assertTrue(data_exists('rbspa_rbspice_l3_TOFxEnonH_oxygen_omni_0-1000keV_pad_spin'))
        rbsp_rbspice_pad(probe='a', datatype='TOFxEH', level='l3', energy=[0, 1000.0])
        self.assertTrue(data_exists('rbspa_rbspice_l3_TOFxEH_proton_omni_0-1000.0keV_pad'))
        self.assertTrue(data_exists('rbspa_rbspice_l3_TOFxEH_proton_omni_0-1000.0keV_pad_spin'))

    def test_load_mageis_data(self):
        del_data('*')
        mageis_vars = pyspedas.projects.rbsp.mageis(trange=['2018-11-5', '2018-11-6'], level='l3', rel='rel04')
        self.assertTrue(data_exists('I'))

    def test_load_hope_data(self):
        del_data('*')
        hope_vars = pyspedas.projects.rbsp.hope(trange=['2018-11-5', '2018-11-6'], datatype='moments', level='l3', rel='rel04')
        self.assertTrue(data_exists('Ion_density'))
        hope_vars = pyspedas.projects.rbsp.hope(trange=['2018-11-5', '2018-11-6'], datatype='pitchangle', level='l3')
        self.assertTrue(data_exists('FEDO'))
        hope_vars = pyspedas.projects.rbsp.hope(trange=['2018-11-5', '2018-11-6'], datatype='spinaverage', level='l2')
        self.assertTrue(data_exists('I_Ele'))

    def test_load_rep_data(self):
        del_data('*')
        rept_vars = pyspedas.projects.rbsp.rept(trange=['2018-11-4', '2018-11-5'], level='l2', rel='rel03')
        self.assertTrue(data_exists('FESA'))
        self.assertTrue(data_exists('FEDU'))
        self.assertTrue(data_exists('FPSA'))
        self.assertTrue(data_exists('FPDU'))

    def test_load_rps1min_data(self):
        del_data('*')
        rps_vars = pyspedas.projects.rbsp.rps()
        self.assertTrue(data_exists('DOSE2_RATE'))
        rps_vars = pyspedas.projects.rbsp.rps(datatype='rps')
        self.assertTrue(data_exists('FPDU_Energy'))

    def test_load_magephem_data(self):
        del_data('*')
        magephem_vars = pyspedas.projects.rbsp.magephem()
        print(magephem_vars)
        self.assertTrue(data_exists('Rgse'))
        self.assertTrue('Rgse' in magephem_vars)

if __name__ == '__main__':
    unittest.main()
