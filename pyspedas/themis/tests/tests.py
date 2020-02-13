
import os
import unittest
from pyspedas.utilities.data_exists import data_exists

import pyspedas

class LoadTestCases(unittest.TestCase):
    def test_load_efi_data(self):
        efi_vars = pyspedas.themis.efi(time_clip=True)
        self.assertTrue(data_exists('thc_eff_e12_efs'))
        self.assertTrue(data_exists('thc_eff_e34_efs'))

    def test_downloadonly(self):
        files = pyspedas.themis.efi(downloadonly=True, trange=['2014-2-15', '2014-2-16'])
        self.assertTrue(os.path.exists(files[0]))

if __name__ == '__main__':
    unittest.main()