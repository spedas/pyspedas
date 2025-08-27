import unittest
import pyspedas
import logging
from pyspedas.tplot_tools import data_exists, del_data

try:
    from viresclient import SwarmRequest
except ImportError:
    logging.info('The viresclient package is needed for this operation, but does not appear to be installed.')
    logging.info('To use this feature, install viresclient with "pip install viresclient".')
    logging.info('If pip install fails, try "conda install viresclient".')


class LoadTestCases(unittest.TestCase):
    def test_get_collections(self):
        from pyspedas.vires.config import CONFIG
        self.assertNotEqual(CONFIG['access_token'],'')
        collections = SwarmRequest(url="https://vires.services/ows",token=CONFIG['access_token']).available_collections(details=False)
        self.assertTrue('SW_OPER_MAGA_LR_1B' in collections['MAG'])
        self.assertTrue('SW_OPER_MODC_SC_1B' in collections['MOD_SC'])

    def test_load_mag_data(self):
        vires_vars = pyspedas.vires.load(trange=['2014-01-01T00:00', '2014-01-01T01:00'],
                                       collection="SW_OPER_MAGA_LR_1B",
                                       measurements=["F", "B_NEC"],
                                       models=["CHAOS-Core"],
                                       sampling_step="PT10S",
                                       auxiliaries=["QDLat", "QDLon"])
        self.assertTrue('Longitude' in vires_vars)
        self.assertTrue('Latitude' in vires_vars)
        self.assertTrue('B_NEC' in vires_vars)
        self.assertTrue(data_exists('Longitude'))
        self.assertTrue(data_exists('Latitude'))
        self.assertTrue(data_exists('B_NEC'))

    def test_load_no_trange(self):
        del_data('*')
        vires_vars = pyspedas.vires.load(collection="SW_OPER_MAGA_LR_1B",
                                       measurements=["F", "B_NEC"],
                                       models=["CHAOS-Core"],
                                       sampling_step="PT10S",
                                       auxiliaries=["QDLat", "QDLon"])
        self.assertTrue(vires_vars is None)
        self.assertFalse(data_exists('Longitude'))
        self.assertFalse(data_exists('Latitude'))
        self.assertFalse(data_exists('B_NEC'))

if __name__ == '__main__':
    unittest.main()
