import unittest
from pyspedas import hapi
from pytplot import data_exists, del_data


class HAPITests(unittest.TestCase):
    def test_print_servers(self):
        with self.assertLogs(level='ERROR') as log: 
            hapi(trange=['2003-10-20', '2003-11-30'])
            self.assertIn("No server specified; example servers include:", log.output[0])

    def test_return_catalog(self):
        id_list = hapi(server='https://cdaweb.gsfc.nasa.gov/hapi', catalog=True, quiet=True)
        self.assertTrue('MMS1_EDI_BRST_L2_EFIELD' in id_list)

    def test_dataset_not_specified(self):
        # dataset not specified
        with self.assertLogs(level='ERROR') as log:
            h_vars = hapi(trange=['2003-10-20', '2003-11-30'],
                        server='https://cdaweb.gsfc.nasa.gov/hapi')
            self.assertIn("Error, no dataset specified; please see the catalog for a list of available data sets.", log.output[0])

    def test_trange_not_specified(self):
        # trange not specified
        with self.assertLogs(level='ERROR') as log:
            h_vars = hapi(dataset='OMNI_HRO2_1MIN',
                        server='https://cdaweb.gsfc.nasa.gov/hapi')
            self.assertIn("Error, no trange specified", log.output[0])

    def test_cdaweb_mms_spec(self):
        h_vars = hapi(trange=['2019-10-16', '2019-10-17'],
                      server='https://cdaweb.gsfc.nasa.gov/hapi',
                      dataset='MMS4_EDP_SRVY_L2_HFESP')

    def test_cdaweb_omni(self):
        del_data()
        h_vars = hapi(trange=['2003-10-20', '2003-11-30'],
                      server='https://cdaweb.gsfc.nasa.gov/hapi',
                      dataset='OMNI_HRO2_1MIN')
        self.assertTrue(data_exists('BX_GSE'))
        self.assertTrue(data_exists('BY_GSE'))
        self.assertTrue(data_exists('BZ_GSE'))


if __name__ == '__main__':
    unittest.main()
