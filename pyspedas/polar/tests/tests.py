
import os
import unittest
from pyspedas.utilities.data_exists import data_exists

import pyspedas

class LoadTestCases(unittest.TestCase):
    def test_downloadonly(self):
        files = pyspedas.polar.efi(downloadonly=True)
        self.assertTrue(os.path.exists(files[0]))

    def test_load_mfe_data(self):
        mfe_vars = pyspedas.polar.mfe(trange=['2003-10-28', '2003-10-29'], get_support_data=True)
        self.assertTrue(data_exists('B_GSE'))
        self.assertTrue(data_exists('B_GSM'))

    def test_load_efi_data(self):
        efi_vars = pyspedas.polar.efi(time_clip=True)
        self.assertTrue(data_exists('ESPIN'))

    def test_load_pwi_data(self):
        pwi_vars = pyspedas.polar.pwi()
        self.assertTrue(data_exists('Fce'))

    def test_load_hydra_data(self):
        hydra_vars = pyspedas.polar.hydra()
        self.assertTrue(data_exists('ELE_DENSITY'))

    def test_load_tide_data(self):
        tide_vars = pyspedas.polar.tide()
        self.assertTrue(data_exists('total_den'))
        self.assertTrue(data_exists('total_v'))
        self.assertTrue(data_exists('total_t'))

    def test_load_timas_data(self):
        timas_vars = pyspedas.polar.timas()
        self.assertTrue(data_exists('Density_H'))

    def test_load_cammice_data(self):
        cammice_vars = pyspedas.polar.cammice()
        self.assertTrue(data_exists('Protons'))

    def test_load_ceppad_data(self):
        ceppad_vars = pyspedas.polar.ceppad()
        self.assertTrue(data_exists('IPS_10_ERR'))

    def test_load_uvi_data(self):
        uvi_vars = pyspedas.polar.uvi()
        self.assertTrue(data_exists('IMAGE_DATA'))

    def test_load_pixie_data(self):
        pixie_vars = pyspedas.polar.pixie()
        self.assertTrue(data_exists('TXF_HIGH'))

    def test_load_orbit_data(self):
        orbit_vars = pyspedas.polar.orbit()
        self.assertTrue(data_exists('AVG_SPIN_RATE'))
        self.assertTrue(data_exists('SPIN_PHASE'))

if __name__ == '__main__':
    unittest.main()