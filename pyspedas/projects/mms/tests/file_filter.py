
import unittest
import numpy as np

from ...mms.mms_file_filter import mms_file_filter

TEST_DATA = ['C:\\Users\\admin\\data\\mms\\mms1\\dfg\\srvy\\ql\\2016\\01\\mms1_dfg_srvy_ql_20160115_v2.13.2.cdf',
    'C:\\Users\\admin\\data\\mms\\mms1\\dfg\\srvy\\ql\\2016\\01\\mms1_dfg_srvy_ql_20160116_v2.13.2.cdf',
    'C:\\Users\\admin\\data\\mms\\mms1\\dfg\\srvy\\ql\\2016\\01\\mms1_dfg_srvy_ql_20160117_v2.13.3.cdf',
    'C:\\Users\\admin\\data\\mms\\mms1\\dfg\\srvy\\ql\\2016\\01\\mms1_dfg_srvy_ql_20160118_v2.13.2.cdf',
    'C:\\Users\\admin\\data\\mms\\mms1\\dfg\\srvy\\ql\\2016\\01\\mms1_dfg_srvy_ql_20160119_v2.14.1.cdf',
    'C:\\Users\\admin\\data\\mms\\mms1\\dfg\\srvy\\ql\\2016\\01\\mms1_dfg_srvy_ql_20160120_v2.14.1.cdf']

class FileFilterTestCases(unittest.TestCase):
    def test_version_eq(self):
        version_eqs =  ['C:\\Users\\admin\\data\\mms\\mms1\\dfg\\srvy\\ql\\2016\\01\\mms1_dfg_srvy_ql_20160115_v2.13.2.cdf',
                        'C:\\Users\\admin\\data\\mms\\mms1\\dfg\\srvy\\ql\\2016\\01\\mms1_dfg_srvy_ql_20160116_v2.13.2.cdf',
                        'C:\\Users\\admin\\data\\mms\\mms1\\dfg\\srvy\\ql\\2016\\01\\mms1_dfg_srvy_ql_20160118_v2.13.2.cdf']
        version_eq_files = mms_file_filter(TEST_DATA, version='2.13.2')
        self.assertTrue(np.array_equal(version_eqs, version_eq_files))

    def test_latest_version(self):
        latest_version = ['C:\\Users\\admin\\data\\mms\\mms1\\dfg\\srvy\\ql\\2016\\01\\mms1_dfg_srvy_ql_20160119_v2.14.1.cdf',
                      'C:\\Users\\admin\\data\\mms\\mms1\\dfg\\srvy\\ql\\2016\\01\\mms1_dfg_srvy_ql_20160120_v2.14.1.cdf']
        latest_files = mms_file_filter(TEST_DATA, latest_version=True)
        self.assertTrue(np.array_equal(latest_version, latest_files))

    def test_min_version(self):
        min_v = ['C:\\Users\\admin\\data\\mms\\mms1\\dfg\\srvy\\ql\\2016\\01\\mms1_dfg_srvy_ql_20160117_v2.13.3.cdf',
                'C:\\Users\\admin\\data\\mms\\mms1\\dfg\\srvy\\ql\\2016\\01\\mms1_dfg_srvy_ql_20160119_v2.14.1.cdf',
                'C:\\Users\\admin\\data\\mms\\mms1\\dfg\\srvy\\ql\\2016\\01\\mms1_dfg_srvy_ql_20160120_v2.14.1.cdf']
        min_versions = mms_file_filter(TEST_DATA, min_version='2.13.3')
        self.assertTrue(np.array_equal(min_versions, min_v))

    def test_major_version(self):
        all_versions = ['C:\\Users\\admin\\data\\mms\\mms1\\dfg\\srvy\\ql\\2016\\01\\mms1_dfg_srvy_ql_20160117_v2.13.3.cdf',
             'C:\\Users\\admin\\data\\mms\\mms1\\dfg\\srvy\\ql\\2016\\01\\mms1_dfg_srvy_ql_20160119_v2.14.1.cdf', 
             'C:\\Users\\admin\\data\\mms\\mms1\\dfg\\srvy\\ql\\2016\\01\\mms1_dfg_srvy_ql_20160120_v2.14.1.cdf', 
             'C:\\Users\\admin\\data\\mms\\mms1\\dfg\\srvy\\ql\\2016\\01\\mms1_dfg_srvy_ql_20160120_v1.14.1.cdf', 
             'C:\\Users\\admin\\data\\mms\\mms1\\dfg\\srvy\\ql\\2016\\01\\mms1_dfg_srvy_ql_20160120_v1.14.1.cdf', 
             'C:\\Users\\admin\\data\\mms\\mms1\\dfg\\srvy\\ql\\2016\\01\\mms1_dfg_srvy_ql_20160120_v1.14.1.cdf']
        major_versions_real = ['C:\\Users\\admin\\data\\mms\\mms1\\dfg\\srvy\\ql\\2016\\01\\mms1_dfg_srvy_ql_20160117_v2.13.3.cdf',
             'C:\\Users\\admin\\data\\mms\\mms1\\dfg\\srvy\\ql\\2016\\01\\mms1_dfg_srvy_ql_20160119_v2.14.1.cdf', 
             'C:\\Users\\admin\\data\\mms\\mms1\\dfg\\srvy\\ql\\2016\\01\\mms1_dfg_srvy_ql_20160120_v2.14.1.cdf']

        filtered_files = mms_file_filter(all_versions, major_version=True)
        self.assertTrue(np.array_equal(filtered_files, major_versions_real))

if __name__ == '__main__':
    unittest.main()