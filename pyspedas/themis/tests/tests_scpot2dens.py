import unittest

import pytplot

import pyspedas
from pyspedas.themis.analysis.scpot2dens import dens_pot
from pyspedas.themis.analysis import scpot2dens
import numpy as np


class TestScpo2densValidation(unittest.TestCase):
    def test_dens_pot_values(self):
        """ Test supporting function dens_pot for initial values"""
        d1 = dens_pot(-1, 0)
        d2 = dens_pot(-1, 1)

        idl_d1 = 3048.9753
        idl_d2 = 34381.586

        self.assertAlmostEqual(d1, idl_d1, delta=0.1)
        self.assertAlmostEqual(d2, idl_d2, delta=0.1)

    def test_dens_pot_pder_values(self):
        """ Test supporting function dens_pot for derivative values"""
        _, d1 = dens_pot(-1, 0, True)
        _, d2 = dens_pot(-1, 1, True)

        idl_d1 = 6278.0029
        idl_d2 = 95702.727

        self.assertAlmostEqual(d1, idl_d1, delta=0.1)
        self.assertAlmostEqual(d2, idl_d2, delta=0.1)

    def test_dens_pot_list_values(self):
        """ Test supporting function dens_pot for tuple of values and derivative"""
        r1, d1 = dens_pot(np.array([0, -1]), 1, True)

        idl_r1 = np.array([3048.9753, 34381.586])
        idl_d1 = np.array([6278.0029, 95702.727])

        for p, idl in zip(r1, idl_r1):
            self.assertAlmostEqual(p, idl, delta=0.1)

        for p, idl in zip(d1, idl_d1):
            self.assertAlmostEqual(p, idl, delta=0.1)

    def test_scpot2dens(self):
        """
        Test satellite case of retrieving density with the change of the spacecraft potential offset.
        The offset if setup for probe c on (2007-7-20/17:24)
        """

        trange = ['2007-7-20/17:23:55', '2007-7-20/17:24:05']
        pyspedas.themis.esa(trange=trange, probe='c',
                            varnames=['thc_peer_density', 'thc_peir_density', 'thc_peer_sc_pot', 'thc_peer_avgtemp'],
                            level='l2', time_clip=True)

        dens_e_time, dens_e = pytplot.get_data('thc_peer_density')
        dens_i_time, dens_i = pytplot.get_data('thc_peir_density')
        sc_pot_time, sc_pot = pytplot.get_data('thc_peer_sc_pot')
        Te_time, Te = pytplot.get_data('thc_peer_avgtemp')

        Npot = scpot2dens(sc_pot, sc_pot_time, Te, Te_time, dens_e, dens_e_time, dens_i, dens_i_time, 'c')

        idl_Npot = np.array([19.2729, 53.6906, 53.0732])

        for p, idl in zip(Npot, idl_Npot):
            self.assertAlmostEqual(p, idl, delta=0.1)

if __name__ == '__main__':
    unittest.main()
