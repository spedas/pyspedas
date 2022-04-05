import pyspedas
import unittest

from pyspedas.utilities.data_exists import data_exists
from pyspedas.mms.fpi.mms_fpi_split_tensor import mms_fpi_split_tensor

class FPITestCases(unittest.TestCase):
    def test_split_tensors(self):
        data = pyspedas.mms.fpi(trange=['2015-10-16/13:06', '2015-10-16/13:07'],
                                data_rate='brst',
                                datatype=['dis-moms', 'des-moms'])

        split_vars = mms_fpi_split_tensor('mms1_dis_temptensor_gse_brst')

        components = ['xx', 'xy', 'xz', 'yx', 'yy', 'yz', 'zx', 'zy', 'zz']
        output = ['mms1_dis_temptensor_gse_brst_' + component for component in components]

        for v in output:
            self.assertTrue(data_exists(v))

        split_vars = mms_fpi_split_tensor('mms1_des_temptensor_gse_brst')

        components = ['xx', 'xy', 'xz', 'yx', 'yy', 'yz', 'zx', 'zy', 'zz']
        output = ['mms1_des_temptensor_gse_brst_' + component for component in components]

        for v in output:
            self.assertTrue(data_exists(v))