
import os
import unittest

from pyspedas.utilities.download import download

from pyspedas.projects.themis.config import CONFIG
# Use whichever remote server is configured for THEMIS, in case the Berkeley server is unavailable
themis_remote = CONFIG['remote_data_dir']


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

    def test_wildcard(self):
        # Test a wildcard pattern with several matches
        files = download(remote_path='https://themis-data.igpp.ucla.edu/tha/l1/state/2008/tha_l1_state_20080323_v??.cdf')
        self.assertTrue(len(files) == 4)  # v00, v01, v02, v03 should be available on this date
        self.assertTrue(files[3] == os.path.join(os.getcwd(), 'tha_l1_state_20080323_v03.cdf'))

    def test_missing_index(self):
        # Test a wildcard pattern on a nonexistent directory
        # This should warn "Remote index not found"
        files = download(remote_path=themis_remote+'l1/state/2006/tha_l1_state_20060323_v??.cdf')
        self.assertTrue(len(files) == 0)

    def test_last_version(self):
        # Test a wildcard pattern with several matches, and last_version=True, returning the final (lexicographic) value
        files = download(remote_path=themis_remote+'tha/l1/state/2008/tha_l1_state_20080323_v??.cdf',last_version=True)
        self.assertTrue(len(files) == 1)  # v00, v01, v02, v03 should be available on this date, should only return v03
        self.assertTrue(files[0] == os.path.join(os.getcwd(), 'tha_l1_state_20080323_v03.cdf'))

    def test_last_version_nomatch(self):
        # Test a wildcard pattern that doesn't match anything.
        # This should warn about no matching file found in the index.
        files = download(remote_path=themis_remote+'tha/l1/state/2008/tha_l1_state_20080332_v??.cdf',last_version=True)
        self.assertTrue(len(files) == 0)  # Nonexistent date, nothing should be found

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


    def test_force_download(self):
        # specifying both remote_path and remote_file saves the files to the current working directory + the path specified in remote_file
        files = download(remote_path='https://spdf.gsfc.nasa.gov/pub/data/', remote_file='themis/tha/l1/state/2007/tha_l1_state_20070217_v01.cdf')
        self.assertTrue(len(files) == 1)
        self.assertTrue(files[0] == os.path.join(os.getcwd(), 'themis/tha/l1/state/2007/tha_l1_state_20070217_v01.cdf'))
        # Download the same file without force_download, should not re-download
        with self.assertLogs(level='INFO') as log:
            files = download(remote_path='https://spdf.gsfc.nasa.gov/pub/data/',
                             remote_file='themis/tha/l1/state/2007/tha_l1_state_20070217_v01.cdf')
            self.assertIn("File is current", log.output[0])
        # Download the same file with force_download, should re-download
        with self.assertLogs(level='INFO') as log:
            files = download(remote_path='https://spdf.gsfc.nasa.gov/pub/data/',
                             remote_file='themis/tha/l1/state/2007/tha_l1_state_20070217_v01.cdf',
                             force_download=True)
            self.assertIn("Downloading", log.output[0])

if __name__ == '__main__':
    unittest.main()