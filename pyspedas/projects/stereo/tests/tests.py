import os
import unittest
from pytplot import data_exists
import pyspedas


class LoadTestCases(unittest.TestCase):
    def test_downloadonly(self):
        files = pyspedas.projects.stereo.mag(trange=['2013-11-5', '2013-11-6'], downloadonly=True)
        self.assertTrue(os.path.exists(files[0]))

    def test_load_mag_data(self):
        mag_vars = pyspedas.projects.stereo.mag(trange=['2013-11-5', '2013-11-6'], time_clip=True)
        self.assertTrue(data_exists('BFIELD'))
        mag_vars = pyspedas.projects.stereo.mag(trange=['2013-11-5', '2013-11-6'], datatype='32hz')
        mag_vars = pyspedas.projects.stereo.mag(trange=['2013-11-5', '2013-11-6'], notplot=True)
        self.assertTrue('BFIELD' in mag_vars)

    def test_load_swea_data(self):
        swea_vars = pyspedas.projects.stereo.swea(trange=['2013-1-5', '2013-1-6'], time_clip=True)
        self.assertTrue(data_exists('SWEASpectra'))

    def test_load_ste_data(self):
        ste_vars = pyspedas.projects.stereo.ste(trange=['2013-1-5', '2013-1-6'], time_clip=True)
        self.assertTrue(data_exists('STE_spectra'))

    def test_load_sept_data(self):
        sept_vars = pyspedas.projects.stereo.sept(trange=['2013-1-5', '2013-1-6'], time_clip=True)
        self.assertTrue(data_exists('Spec_0_E'))

    def test_load_sit_data(self):
        sit_vars = pyspedas.projects.stereo.sit(trange=['2013-1-5', '2013-1-6'], time_clip=True)
        self.assertTrue(data_exists('H_Intensity'))

    def test_load_let_data(self):
        let_vars = pyspedas.projects.stereo.let(trange=['2013-1-5', '2013-1-6'], time_clip=True)
        self.assertTrue(data_exists('H_Hi_sec_flux'))

    def test_load_het_data(self):
        het_vars = pyspedas.projects.stereo.het(trange=['2013-1-5', '2013-1-6'], time_clip=True)
        self.assertTrue(data_exists('Electron_Flux'))
        self.assertTrue(data_exists('Proton_Flux'))

    def test_load_plastic_data(self):
        p_vars = pyspedas.projects.stereo.plastic(trange=['2013-11-5', '2013-11-6'], probe='b')
        self.assertTrue(data_exists('proton_number_density'))
        self.assertTrue(data_exists('proton_bulk_speed'))
        self.assertTrue(data_exists('proton_temperature'))

    def test_load_waves_data_a(self):
        w_vars = pyspedas.projects.stereo.waves(trange=['2013-11-5', '2013-11-6'], probe='a')
        self.assertTrue(data_exists('PSD_FLUX'))
        self.assertTrue(data_exists('PSD_SFU'))

    def test_load_waves_data_b(self):
        w_vars = pyspedas.projects.stereo.waves(trange=['2013-11-5', '2013-11-6'], probe='b')
        self.assertTrue(data_exists('PSD_FLUX'))
        self.assertTrue(data_exists('PSD_SFU'))

    def test_load_beacon_data_a(self):
        w_vars = pyspedas.projects.stereo.beacon(trange=['2013-11-5', '2013-11-6'], probe='a')
        self.assertTrue(data_exists('MAGBField'))

    def test_load_beacon_data_b(self):
        w_vars = pyspedas.projects.stereo.beacon(trange=['2013-11-5', '2013-11-6'], probe='b')
        self.assertTrue(data_exists('MAGBField'))

if __name__ == '__main__':
    unittest.main()
