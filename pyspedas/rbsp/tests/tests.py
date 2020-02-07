
import unittest
from pyspedas.utilities.data_exists import data_exists

import pyspedas

class LoadTestCases(unittest.TestCase):
    def test_load_emfisis_data(self):
        emfisis_vars = pyspedas.rbsp.emfisis(trange=['2018-11-5', '2018-11-6'], datatype='magnetometer', level='l3')
        self.assertTrue(data_exists('Mag'))

    def test_load_efw_data(self):
        efw_vars = pyspedas.rbsp.efw(trange=['2015-11-5', '2015-11-6'], level='l3')
        self.assertTrue(data_exists('density'))

    def test_load_rbspice_data(self):
        rbspice_vars = pyspedas.rbsp.rbspice(trange=['2018-11-5', '2018-11-6'], datatype='tofxeh', level='l3')
        self.assertTrue(data_exists('Alpha'))

    def test_load_mageis_data(self):
        mageis_vars = pyspedas.rbsp.mageis(trange=['2018-11-5', '2018-11-6'], level='l3', rel='rel04')
        self.assertTrue(data_exists('I'))

    def test_load_hope_data(self):
        hope_vars = pyspedas.rbsp.hope(trange=['2018-11-5', '2018-11-6'], datatype='moments', level='l3', rel='rel04')
        self.assertTrue(data_exists('Ion_density'))

    def test_load_rep_data(self):
        rept_vars = pyspedas.rbsp.rept(trange=['2018-11-5', '2018-11-6'], level='l3', rel='rel03')
        self.assertTrue(data_exists('Tperp_e_200'))

if __name__ == '__main__':
    unittest.main()