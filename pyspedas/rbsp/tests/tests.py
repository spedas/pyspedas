import os
import unittest
from pyspedas.utilities.data_exists import data_exists
import pyspedas
from pytplot import del_data


class LoadTestCases(unittest.TestCase):
    def tearDown(self):
        del_data('*')

    def test_downloadonly(self):
        files = pyspedas.rbsp.efw(trange=['2015-11-3', '2015-11-4'], level='l3', downloadonly=True)
        self.assertTrue(os.path.exists(files[0]))

    def test_notplot(self):
        data = pyspedas.rbsp.efw(trange=['2015-11-6', '2015-11-7'], level='l3', notplot=True)
        self.assertTrue('density' in data.keys())
        self.assertTrue('efield_in_inertial_frame_spinfit_mgse' in data.keys())
        self.assertTrue('x' in data['density'].keys())
        self.assertTrue('y' in data['density'].keys())

    def test_load_emfisis_data(self):
        emfisis_vars = pyspedas.rbsp.emfisis(trange=['2018-11-5', '2018-11-6'], datatype='magnetometer', level='l3', time_clip=True)
        self.assertTrue(data_exists('Mag'))
        emfisis_vars = pyspedas.rbsp.emfisis(trange=['2018-11-5', '2018-11-6'], datatype='magnetometer', level='l2')
        wfr_vars = pyspedas.rbsp.emfisis(trange=['2018-11-5', '2018-11-6'], level='l2', datatype='wfr')
        hfr_vars = pyspedas.rbsp.emfisis(trange=['2018-11-5', '2018-11-6'], level='l2', datatype='hfr')
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
        dens = pyspedas.rbsp.emfisis(trange=['2018-11-5', '2018-11-6'], datatype='density', level='l4')
        self.assertTrue(data_exists('density'))

    def test_load_efw_data(self):
        efw_vars = pyspedas.rbsp.efw(trange=['2015-11-5', '2015-11-6'], level='l2')
        self.assertTrue(data_exists('spec64_e12ac'))
        efw_vars = pyspedas.rbsp.efw(trange=['2015-11-5', '2015-11-6'], level='l3')
        self.assertTrue(data_exists('density'))

    def test_load_rbspice_data(self):
        files = pyspedas.rbsp.rbspice(downloadonly=True, trange=['2018-11-5', '2018-11-6'], datatype='tofxeh', level='l3')
        self.assertTrue(isinstance(files, list))

    def test_load_mageis_data(self):
        mageis_vars = pyspedas.rbsp.mageis(trange=['2018-11-5', '2018-11-6'], level='l3', rel='rel04')
        self.assertTrue(data_exists('I'))

    def test_load_hope_data(self):
        hope_vars = pyspedas.rbsp.hope(trange=['2018-11-5', '2018-11-6'], datatype='moments', level='l3', rel='rel04')
        self.assertTrue(data_exists('Ion_density'))
        hope_vars = pyspedas.rbsp.hope(trange=['2018-11-5', '2018-11-6'], datatype='pitchangle', level='l3')
        self.assertTrue(data_exists('FEDO'))
        hope_vars = pyspedas.rbsp.hope(trange=['2018-11-5', '2018-11-6'], datatype='spinaverage', level='l2')
        self.assertTrue(data_exists('I_Ele'))

    def test_load_rep_data(self):
        rept_vars = pyspedas.rbsp.rept(trange=['2018-11-4', '2018-11-5'], level='l2', rel='rel03')
        self.assertTrue(data_exists('FESA'))
        self.assertTrue(data_exists('FEDU'))
        self.assertTrue(data_exists('FPSA'))
        self.assertTrue(data_exists('FPDU'))

    def test_load_rps1min_data(self):
        rps_vars = pyspedas.rbsp.rps()
        self.assertTrue(data_exists('DOSE2_RATE'))
        rps_vars = pyspedas.rbsp.rps(datatype='rps')
        self.assertTrue(data_exists('FPDU_Energy'))


if __name__ == '__main__':
    unittest.main()
