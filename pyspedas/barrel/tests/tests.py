
import os
import unittest
import pyspedas


class LoadTestCases(unittest.TestCase):
    def test_downloadonly(self):
        mag_files = pyspedas.barrel.sspc(probe='1A', downloadonly=True)
        self.assertTrue(os.path.exists(mag_files[0]))


if __name__ == '__main__':
    unittest.main()