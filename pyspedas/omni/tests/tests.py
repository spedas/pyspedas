import os
import unittest
from pyspedas.utilities.data_exists import data_exists
import pyspedas


class LoadTestCases(unittest.TestCase):
    def test_utc_timestamp_regression(self):
        varname = 'BX_GSE'
        data_omni = pyspedas.omni.data(trange=['2010-01-01/00:00:00', '2010-01-02/00:00:00'],notplot=True,varformat=varname,time_clip=True)
        self.assertTrue(str(data_omni[varname]['x'][0]) == '2010-01-01 00:00:00')

    def test_load_hro2_data(self):
        omni_vars = pyspedas.omni.data()
        self.assertTrue(data_exists('BX_GSE'))
        self.assertTrue(data_exists('BY_GSE'))
        self.assertTrue(data_exists('BZ_GSE'))
        self.assertTrue(data_exists('BY_GSM'))
        self.assertTrue(data_exists('BZ_GSM'))
        self.assertTrue(data_exists('proton_density'))

    def test_load_hro_data(self):
        omni_vars = pyspedas.omni.data(level='hro')
        self.assertTrue(data_exists('BX_GSE'))
        self.assertTrue(data_exists('BY_GSE'))
        self.assertTrue(data_exists('BZ_GSE'))
        self.assertTrue(data_exists('BY_GSM'))
        self.assertTrue(data_exists('BZ_GSM'))
        self.assertTrue(data_exists('proton_density'))

    def test_load_hro_5min_data(self):
        omni_vars = pyspedas.omni.data(level='hro', datatype='5min')
        self.assertTrue(data_exists('BX_GSE'))
        self.assertTrue(data_exists('BY_GSE'))
        self.assertTrue(data_exists('BZ_GSE'))
        self.assertTrue(data_exists('BY_GSM'))
        self.assertTrue(data_exists('BZ_GSM'))
        self.assertTrue(data_exists('proton_density'))

    def test_load_hro_hour_data(self):
        omni_vars = pyspedas.omni.data(level='hro2', datatype='hour', trange=['2013-01-01', '2013-01-02'])

    def test_load_invalid_datatype(self):
        omni_vars = pyspedas.omni.data(datatype='1')

    def test_downloadonly(self):
        files = pyspedas.omni.data(downloadonly=True, trange=['2014-2-15', '2014-2-16'])
        self.assertTrue(os.path.exists(files[0]))


if __name__ == '__main__':
    unittest.main()
