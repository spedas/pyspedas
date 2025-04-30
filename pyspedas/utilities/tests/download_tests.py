import os
import unittest

import pyspedas
from pyspedas.utilities.download import download
from pyspedas.utilities.download_ftp import download_ftp

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
        files = download(remote_path="https://themis-data.igpp.ucla.edu/tha/l1/state/2008/tha_l1_state_20080323_v??.cdf", last_version=False)
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

    def test_cdf_to_tplot_varformat(self):
        # Check varnamea, varformat, exclude_format, and suffixes in various combinations
        # single varformat pattern
        vars = pyspedas.projects.themis.state(probe='a',varformat='*pos*')
        vars.sort()
        self.assertEqual(vars, ['tha_pos', 'tha_pos_gse', 'tha_pos_gsm', 'tha_pos_sel', 'tha_pos_sse'])
        # single varformat pattern with "|", should include both options
        vars = pyspedas.projects.themis.state(probe='a', varformat='*pos*|*vel*')
        vars.sort()
        self.assertEqual(vars,['tha_pos', 'tha_pos_gse', 'tha_pos_gsm', 'tha_pos_sel', 'tha_pos_sse', 'tha_vel', 'tha_vel_gse', 'tha_vel_gsm', 'tha_vel_sel', 'tha_vel_sse'])
        # varformat pattern with spaces, should treat as alternate patterns
        vars = pyspedas.projects.themis.state(probe='a', varformat='*pos*  *vel*')
        vars.sort()
        self.assertEqual(vars,['tha_pos', 'tha_pos_gse', 'tha_pos_gsm', 'tha_pos_sel', 'tha_pos_sse', 'tha_vel', 'tha_vel_gse', 'tha_vel_gsm', 'tha_vel_sel', 'tha_vel_sse'])
        # varformat and exclude_format patterns with spaces
        vars = pyspedas.projects.themis.state(probe='a', varformat='*pos*  *vel*', exclude_format='*sel* *sse*')
        vars.sort()
        self.assertEqual(vars,['tha_pos', 'tha_pos_gse', 'tha_pos_gsm', 'tha_vel', 'tha_vel_gse', 'tha_vel_gsm'])
        # varformat patterns as array, should treat as alternate patterns
        vars = pyspedas.projects.themis.state(probe='a', varformat=['*pos*','*vel*'])
        vars.sort()
        self.assertEqual(vars,['tha_pos', 'tha_pos_gse', 'tha_pos_gsm', 'tha_pos_sel', 'tha_pos_sse', 'tha_vel', 'tha_vel_gse', 'tha_vel_gsm', 'tha_vel_sel', 'tha_vel_sse'])
        # varformat and exclude_format patterns as arrays
        vars = pyspedas.projects.themis.state(probe='a', varformat=['*pos*','*vel*'], exclude_format=['*sel*', '*sse*'])
        vars.sort()
        self.assertEqual(vars,['tha_pos', 'tha_pos_gse', 'tha_pos_gsm', 'tha_vel', 'tha_vel_gse', 'tha_vel_gsm'])
        # varnames with suffix specified, should return requested variables even though CDF names don't have suffix
        vars = pyspedas.projects.themis.state(probe='a',suffix='_suf', varnames=['tha_pos_suf', 'tha_pos_gse_suf'])
        vars.sort()
        self.assertEqual(vars, ['tha_pos_gse_suf', 'tha_pos_suf'])
        # varformat with suffix specified, should return values
        vars = pyspedas.projects.themis.state(probe='a',suffix='_suf', varformat=['*pos_suf', '*pos_gse_suf'])
        vars.sort()
        self.assertEqual(vars, ['tha_pos_gse_suf', 'tha_pos_suf'])
        # exclude_format with suffix specified, should remove variables with or without suffixes
        vars = pyspedas.projects.themis.state(probe='a',suffix='_suf', exclude_format=['*vel*', '*spin*','*sse*_suf', '*sel'])
        vars.sort()
        self.assertEqual(vars, ['tha_pos_gse_suf', 'tha_pos_gsm_suf', 'tha_pos_suf'])

    def test_download_ftp(self):
        from pyspedas.projects.noaa.config import CONFIG
        kp_mirror = "ftp.gfz-potsdam.de"
        remote_kp_dir = "/pub/home/obs/kp-ap/wdc/yearly/"
        local_data_dir = CONFIG['local_data_dir']
        pre = "kp"
        suf = ".wdc"
        start_year = 2019
        end_year = 2021
        # Remote names
        remote_names = [
            pre + str(year) + suf for year in range(start_year, end_year + 1)
        ]
        files=[]
        for yearstr in remote_names:
            dfile = download_ftp(
                kp_mirror,
                remote_kp_dir,
                yearstr,
                local_data_dir,
                force_download=True,
            )
            if len(dfile) > 0:
                files.append(dfile[0])
        self.assertTrue(os.path.exists(files[0]))
        self.assertTrue(os.path.exists(files[1]))
        self.assertTrue(os.path.exists(files[2]))
        # repeat download of first file to exercise 'file not modified' path
        dfile = download_ftp(
            kp_mirror,
            remote_kp_dir,
            remote_names[0],
            local_data_dir,
            force_download=False,
        )
        self.assertTrue(len(dfile) == 1)



if __name__ == "__main__":
    unittest.main()
