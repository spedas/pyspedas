import unittest
import pyspedas
from pyspedas import sosmag_load
from pyspedas.utilities.data_exists import data_exists

pyspedas.sosmag.load.sosmag_parameters['print_messages'] = True


class SOSMAG_Tests(unittest.TestCase):
    def test_mag(self):
        t_ok, var_names = sosmag_load(trange=['2021-01-01 02:00', '2021-01-01 03:00'])
        self.assertTrue(data_exists('sosmag_b_gse'))
        self.assertTrue(data_exists('sosmag_position'))

    def test_1m(self):
        t_ok, var_names = sosmag_load(datatype='1m', trange=['2021-01-01 02:00', '2021-01-01 03:00'])
        self.assertTrue(data_exists('sosmag_1m_b_gse'))
        self.assertTrue(data_exists('sosmag_1m_position'))

    def test_invalid_user(self):
        pyspedas.sosmag.load.sosmag_parameters['username'] = 'not_valid'
        try:
            t_ok, var_names = sosmag_load(datatype='1m', trange=['2021-01-01 02:00', '2021-01-01 03:00'])
        except:
            pass
        pyspedas.sosmag.load.sosmag_parameters['username'] = 'spedas'

    def test_invalid_cookies(self):
        authenticated, auth_cookie = pyspedas.sosmag.load.sosmag_get_auth_cookie()
        # shouldn't work
        invalid = pyspedas.sosmag.load.sosmag_get_session('')
        invalid = pyspedas.sosmag.load.sosmag_get_capabilities('', '')
        invalid = pyspedas.sosmag.load.sosmag_get_data('', '')
        invalid = pyspedas.sosmag.load.sosmag_to_tplot([1], '', '')
        invalid = pyspedas.sosmag.load.sosmag_to_tplot(None, '', '')
        with self.assertRaises(TypeError):
            sosmag_load(trange=['2000-01-01', '2000-01-02'])


if __name__ == '__main__':
    unittest.main()
