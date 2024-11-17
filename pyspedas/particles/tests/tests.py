import unittest
import logging
import pyspedas
from pyspedas.projects.erg.satellite.erg.particle.erg_lepe_get_dist import erg_lepe_get_dist
from pyspedas.particles.spd_part_products.spd_pgs_make_theta_spec import spd_pgs_make_theta_spec
from pyspedas.particles.spd_part_products.spd_pgs_make_phi_spec import spd_pgs_make_phi_spec
from pyspedas.particles.spd_part_products.spd_pgs_make_e_spec import spd_pgs_make_e_spec

class MyTestCase(unittest.TestCase):
    def test_theta_spec(self):
        trange=['2017-04-05 21:45:00', '2017-04-05 22:45:00']
        pyspedas.projects.erg.lepe(trange=trange,datatype='3dflux')
        times=erg_lepe_get_dist('erg_lepe_l2_3dflux_FEDU', trange=['2017-04-05 21:45:00', '2017-04-05 22:45:00'], time_only=True)
        # spd_pgs_make_theta_spec does bin weighting, which is horribly slow in practice.  So we'll just do a single distribution.
        single_time=times[0]
        dist=erg_lepe_get_dist('erg_lepe_l2_3dflux_FEDU', single_time=single_time)
        self.assertTrue(dist is not None)
        theta_vals, spectra = spd_pgs_make_theta_spec(dist)
        self.assertTrue(theta_vals is not None)
        self.assertTrue(spectra is not None)

    def test_phi_spec(self):
        trange=['2017-04-05 21:45:00', '2017-04-05 22:45:00']
        pyspedas.projects.erg.lepe(trange=trange,datatype='3dflux')
        times=erg_lepe_get_dist('erg_lepe_l2_3dflux_FEDU', trange=['2017-04-05 21:45:00', '2017-04-05 22:45:00'], time_only=True)
        # spd_pgs_make_phi_spec does bin weighting, which is horribly slow in practice.  So we'll just do a single distribution.
        single_time=times[0]
        dist=erg_lepe_get_dist('erg_lepe_l2_3dflux_FEDU', single_time=single_time)
        self.assertTrue(dist is not None)
        phi_vals, spectra = spd_pgs_make_phi_spec(dist)
        self.assertTrue(phi_vals is not None)
        self.assertTrue(spectra is not None)

    def test_e_spec(self):
        trange=['2017-04-05 21:45:00', '2017-04-05 22:45:00']
        pyspedas.projects.erg.lepe(trange=trange,datatype='3dflux')
        times=erg_lepe_get_dist('erg_lepe_l2_3dflux_FEDU', trange=['2017-04-05 21:45:00', '2017-04-05 22:45:00'], time_only=True)
        dist=erg_lepe_get_dist('erg_lepe_l2_3dflux_FEDU', trange=trange)
        self.assertTrue(dist is not None)
        e_vals, spectra = spd_pgs_make_e_spec(dist)
        self.assertTrue(e_vals is not None)
        self.assertTrue(spectra is not None)




if __name__ == '__main__':
    unittest.main()
