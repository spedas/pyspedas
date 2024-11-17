import os
import unittest
from pytplot import data_exists, del_data
import pyspedas

class LoadTestCases(unittest.TestCase):
    def test_utc_timestamp_regression(self):
        varname = 'BX_GSE'
        del_data('*')
        data_omni = pyspedas.projects.omni.data(trange=['2010-01-01/00:00:00', '2010-01-02/00:00:00'],notplot=True,varformat=varname,time_clip=True)
        ts=data_omni[varname]['x'][0]
        # Depending on the version of cdflib in use, ts might be a datetime.datetime, or np.datetime64.  The string representations
        # are slightly different: "2010-01-01 00:00:00" vs "2010-01-01T00:00:00.000000".  So we replace "T" with " " and
        # discard any fractional part before comparing.
        ds=str(ts)
        ds2=ds.replace("T"," ")
        nofrac,frac=ds2.split(".")
        self.assertTrue(nofrac == '2010-01-01 00:00:00')

    def test_load_hro2_data(self):
        del_data('*')
        omni_vars = pyspedas.projects.omni.data()
        self.assertTrue(data_exists('BX_GSE'))
        self.assertTrue(data_exists('BY_GSE'))
        self.assertTrue(data_exists('BZ_GSE'))
        self.assertTrue(data_exists('BY_GSM'))
        self.assertTrue(data_exists('BZ_GSM'))
        self.assertTrue(data_exists('proton_density'))

    def test_load_hro_data(self):
        del_data('*')
        omni_vars = pyspedas.projects.omni.data(level='hro')
        self.assertTrue(data_exists('BX_GSE'))
        self.assertTrue(data_exists('BY_GSE'))
        self.assertTrue(data_exists('BZ_GSE'))
        self.assertTrue(data_exists('BY_GSM'))
        self.assertTrue(data_exists('BZ_GSM'))
        self.assertTrue(data_exists('proton_density'))

    def test_load_hro_5min_data(self):
        del_data('*')
        omni_vars = pyspedas.projects.omni.data(level='hro', datatype='5min', prefix='omni_', suffix='_test')
        self.assertTrue(data_exists('omni_BX_GSE_test'))
        self.assertTrue(data_exists('omni_BY_GSE_test'))
        self.assertTrue(data_exists('omni_BZ_GSE_test'))
        self.assertTrue(data_exists('omni_BY_GSM_test'))
        self.assertTrue(data_exists('omni_BZ_GSM_test'))
        self.assertTrue(data_exists('omni_proton_density_test'))

    def test_load_hro_hour_data(self):
        del_data('*')
        omni_vars = pyspedas.projects.omni.data(level='hro2', datatype='hour', trange=['2013-03-01', '2013-03-02'])
        self.assertTrue(data_exists('BX_GSE'))
        self.assertTrue(data_exists('BY_GSE'))
        self.assertTrue(data_exists('BZ_GSE'))
        self.assertTrue(data_exists('BY_GSM'))
        self.assertTrue(data_exists('BZ_GSM'))

    def test_load_hro_hour_data_long_interval(self):
        from pyspedas.utilities.dailynames import dailynames
        del_data('*')
        trange=['2013-01-05','2013-11-06']
        pathformat = 'hourly/%Y/omni2_h0_mrg1hr_%Y%m01_v??.cdf'
        file_res=24*3600*183 # 1 file every 6 months
        remote_names=dailynames(file_format=pathformat,trange=trange,res=file_res)
        print(remote_names)
        omni_vars = pyspedas.projects.omni.data(datatype='hour', trange=trange)
        self.assertTrue(data_exists('BX_GSE'))
        self.assertTrue(data_exists('BY_GSE'))
        self.assertTrue(data_exists('BZ_GSE'))
        self.assertTrue(data_exists('BY_GSM'))
        self.assertTrue(data_exists('BZ_GSM'))

    def test_load_invalid_datatype(self):
        omni_vars = pyspedas.projects.omni.data(datatype='1')

    def test_downloadonly(self):
        files = pyspedas.projects.omni.data(downloadonly=True, trange=['2014-2-15', '2014-2-16'])
        self.assertTrue(os.path.exists(files[0]))


if __name__ == '__main__':
    unittest.main()
