
import os
import unittest

from pyspedas.utilities.download import download

class DownloadTestCases(unittest.TestCase):
    def test_remote_path(self):
        # only specifying remote_path saves the files to the current working directory
        files = download(remote_path='https://spdf.gsfc.nasa.gov/pub/data/psp/sweap/spc/l3/l3i/2019/psp_swp_spc_l3i_20190401_v01.cdf')
        self.assertTrue(len(files) == 1)
        self.assertTrue(files[0] == os.path.join(os.getcwd(), 'psp_swp_spc_l3i_20190401_v01.cdf'))

    def test_remote_file(self):
        # only specifying remote_file saves the files to the current working directory
        files = download(remote_file='https://spdf.gsfc.nasa.gov/pub/data/psp/sweap/spc/l3/l3i/2019/psp_swp_spc_l3i_20190401_v01.cdf')
        self.assertTrue(len(files) == 1)
        self.assertTrue(files[0] == os.path.join(os.getcwd(), 'psp_swp_spc_l3i_20190401_v01.cdf'))

    def test_remote_path_file(self):
        # specifying both remote_path and remote_file saves the files to the current working directory + the path specified in remote_file
        files = download(remote_path='https://spdf.gsfc.nasa.gov/pub/data/', remote_file='psp/sweap/spc/l3/l3i/2019/psp_swp_spc_l3i_20190401_v01.cdf')
        self.assertTrue(len(files) == 1)
        self.assertTrue(files[0] == os.path.join(os.getcwd(), 'psp/sweap/spc/l3/l3i/2019/psp_swp_spc_l3i_20190401_v01.cdf'))

    def test_local_file(self):
        # specifying local_file changes the local file name
        files = download(local_file='psp_data.cdf', remote_file='https://spdf.gsfc.nasa.gov/pub/data/psp/sweap/spc/l3/l3i/2019/psp_swp_spc_l3i_20190401_v01.cdf')
        self.assertTrue(len(files) == 1)
        self.assertTrue(files[0] == os.path.join(os.getcwd(), 'psp_data.cdf'))

    def test_local_path(self):
        # specifying local_path changes the local data directory
        files = download(local_path='psp_data/spc/l3', remote_file='https://spdf.gsfc.nasa.gov/pub/data/psp/sweap/spc/l3/l3i/2019/psp_swp_spc_l3i_20190401_v01.cdf')
        self.assertTrue(len(files) == 1)
        self.assertTrue(files[0] == os.path.join('psp_data/spc/l3', 'psp_swp_spc_l3i_20190401_v01.cdf'))

    def test_auth(self):
        files = download(remote_file='https://postman-echo.com/digest-auth', local_file='test_auth')
        self.assertTrue(len(files) == 0)
        files = download(remote_file='https://postman-echo.com/digest-auth', local_file='test_auth_works', username='postman', password='password')
        self.assertTrue(len(files) == 1)
        
if __name__ == '__main__':
    unittest.main()