import unittest
from pyspedas.hapi.hapi import hapi
from pyspedas.utilities.data_exists import data_exists


class HAPITests(unittest.TestCase):
    def test_print_servers(self):
        hapi(trange=['2003-10-20', '2003-11-30'])

    def test_print_catalog(self):
        hapi(server='https://cdaweb.gsfc.nasa.gov/hapi', catalog=True)

    def test_dataset_not_specified(self):
        # dataset not specified
        h_vars = hapi(trange=['2003-10-20', '2003-11-30'],
                      server='https://cdaweb.gsfc.nasa.gov/hapi')

    def test_trange_not_specified(self):
        # trange not specified
        h_vars = hapi(dataset='OMNI_HRO2_1MIN',
                      server='https://cdaweb.gsfc.nasa.gov/hapi')

    def test_cdaweb_mms_spec(self):
        h_vars = hapi(trange=['2019-10-16', '2019-10-17'],
                      server='https://cdaweb.gsfc.nasa.gov/hapi',
                      dataset='MMS4_EDP_SRVY_L2_HFESP')

    def test_cdaweb_omni(self):
        h_vars = hapi(trange=['2003-10-20', '2003-11-30'],
                      server='https://cdaweb.gsfc.nasa.gov/hapi',
                      dataset='OMNI_HRO2_1MIN')
        self.assertTrue(data_exists('BX_GSE'))
        self.assertTrue(data_exists('BY_GSE'))
        self.assertTrue(data_exists('BZ_GSE'))


if __name__ == '__main__':
    unittest.main()
