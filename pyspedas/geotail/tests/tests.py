
import os
import unittest
from pyspedas.utilities.data_exists import data_exists

import pyspedas

class LoadTestCases(unittest.TestCase):
    def test_downloadonly(self):
        files = pyspedas.geotail.mgf(downloadonly=True)
        self.assertTrue(os.path.exists(files[0]))

    def test_load_mgf_data(self):
        mgf_vars = pyspedas.geotail.mgf(time_clip=True)
        self.assertTrue(data_exists('IB_vector'))

        mgf_vars = pyspedas.geotail.mgf(datatype='edb3sec', trange=['1998-11-3/09:18:00', '1998-11-3/09:28:00'])
        self.assertTrue(data_exists('BGSE'))

    def test_load_efd_data(self):
        efd_vars = pyspedas.geotail.efd()
        self.assertTrue(data_exists('Es'))

    def test_load_lep_data(self):
        lep_vars = pyspedas.geotail.lep()
        self.assertTrue(data_exists('N0'))

    def test_load_cpi_data(self):
        cpi_vars = pyspedas.geotail.cpi()
        self.assertTrue(data_exists('SW_P_Den'))

    def test_load_epic_data(self):
        epic_vars = pyspedas.geotail.epic()
        self.assertTrue(data_exists('IDiffI_I'))
        epic_vars = pyspedas.geotail.epic(notplot=True)
        self.assertTrue('IDiffI_I' in epic_vars)

    def test_load_pwi_data(self):
        pwi_vars = pyspedas.geotail.pwi()
        self.assertTrue(data_exists('MCAE_AVE'))

if __name__ == '__main__':
    unittest.main()