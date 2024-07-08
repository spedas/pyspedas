
import os
import unittest
from pytplot import data_exists, del_data, timespan,tplot, tplot_names
from pyspedas.erg import erg_hep_part_products

import pyspedas
import pytplot

display=False

class LoadTestCases(unittest.TestCase):

    def test_hep_theta(self):
        del_data('*')
        # Load HEP-e Lv.2 3-D flux data
        timespan('2017-04-05 21:45:00', 2.25, keyword='hours')
        pyspedas.erg.hep( trange=[ '2017-04-05 21:45:00', '2017-04-05 23:59:59'], datatype='3dflux' )
        # Calculate and plot energy spectrum
        vars = erg_hep_part_products( 'erg_hep_l2_FEDU_L', outputs='theta' )
        self.assertTrue('erg_hep_l2_FEDU_L_theta' in vars)
        self.assertTrue(data_exists('erg_hep_l2_FEDU_L_theta'))
        tplot( 'erg_hep_l2_FEDU_L_theta', display=display, save_png='erg_hep_theta.png' )

    def test_hep_theta_trange(self):
        del_data('*')
        # Load HEP-e Lv.2 3-D flux data
        timespan('2017-04-05 21:45:00', 2.25, keyword='hours')
        pyspedas.erg.hep( trange=[ '2017-04-05 21:45:00', '2017-04-05 23:59:59'], datatype='3dflux' )
        # Calculate and plot energy spectrum
        vars = erg_hep_part_products( 'erg_hep_l2_FEDU_L',trange=[ '2017-04-05 21:45:00', '2017-04-05 22:45:00'], outputs='theta' )
        self.assertTrue('erg_hep_l2_FEDU_L_theta' in vars)
        self.assertTrue(data_exists('erg_hep_l2_FEDU_L_theta'))
        tplot( 'erg_hep_l2_FEDU_L_theta', display=display, save_png='erg_hep_theta_trange.png' )

    def test_hep_theta_limit_phi(self):
        del_data('*')
        # Load LEP-e Lv.2 3-D flux data
        timespan('2017-04-05 21:45:00', 2.25, keyword='hours')
        pyspedas.erg.hep( trange=[ '2017-04-05 21:45:00', '2017-04-05 22:45:00'], datatype='3dflux' )
        # Calculate and plot energy spectrum
        vars = erg_hep_part_products( 'erg_hep_l2_FEDU_L', outputs='theta', trange=[ '2017-04-05 21:45:00', '2017-04-05 23:59:59'], phi_in=[0., 180.0] )
        tplot( 'erg_hep_l2_FEDU_L_theta', display=display, save_png='erg_hep_theta_limit_phi.png' )
        self.assertTrue(data_exists('erg_hep_l2_FEDU_L_theta'))
        self.assertTrue('erg_hep_l2_FEDU_L_theta' in vars)

    def test_hep_phi(self):
        del_data('*')
        # Load HEP-e Lv.2 3-D flux data
        timespan('2017-04-05 21:45:00', 2.25, keyword='hours')
        pyspedas.erg.hep( trange=[ '2017-04-05 21:45:00', '2017-04-05 23:59:59'], datatype='3dflux' )
        # Calculate and plot energy spectrum
        vars = erg_hep_part_products( 'erg_hep_l2_FEDU_L', outputs='phi')
        self.assertTrue('erg_hep_l2_FEDU_L_phi' in vars)
        self.assertTrue(data_exists('erg_hep_l2_FEDU_L_phi'))
        tplot( 'erg_hep_l2_FEDU_L_phi', display=display, save_png='erg_hep_phi.png' )


    def test_hep_pa(self):
        del_data('*')
        # Load HEP-e Lv.2 3-D flux data
        timespan('2017-04-05 21:45:00', 2.25, keyword='hours')
        pyspedas.erg.hep( trange=[ '2017-04-05 21:45:00', '2017-04-05 23:59:59'], datatype='3dflux' )
        vars = pyspedas.erg.mgf(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary B-field data
        vars = pyspedas.erg.orb(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary orbit data
        mag_vn = 'erg_mgf_l2_mag_8sec_dsi'
        pos_vn = 'erg_orb_l2_pos_gse'
        # Calculate and plot energy spectrum
        vars = erg_hep_part_products( 'erg_hep_l2_FEDU_L', mag_name=mag_vn, pos_name=pos_vn, outputs='pa' )
        self.assertTrue('erg_hep_l2_FEDU_L_pa' in vars)
        self.assertTrue(data_exists('erg_hep_l2_FEDU_L_pa'))
        tplot( 'erg_hep_l2_FEDU_L_pa', display=display, save_png='erg_hep_pa.png' )

    # erg_hep_part_products doesn't support moments yet?

    def test_hep_moments(self):
        del_data('*')
        # Load HEP-e Lv.2 3-D flux data
        timespan('2017-04-05 21:45:00', 2.25, keyword='hours')
        pyspedas.erg.hep( trange=[ '2017-04-05 21:45:00', '2017-04-05 23:59:59'], datatype='3dflux' )
        vars = pyspedas.erg.mgf(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary B-field data
        vars = pyspedas.erg.orb(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary orbit data
        mag_vn = 'erg_mgf_l2_mag_8sec_dsi'
        pos_vn = 'erg_orb_l2_pos_gse'
        # Calculate and plot energy spectrum
        vars = erg_hep_part_products( 'erg_hep_l2_FEDU_L', mag_name=mag_vn, pos_name=pos_vn, outputs='moments' )
        tplot(vars, display=display, save_png='erg_hep_moments.png')
        self.assertTrue('erg_hep_l2_FEDU_L_density' in vars)
        self.assertTrue(data_exists('erg_hep_l2_FEDU_L_density'))

    def test_hep_fac_moments(self):
        del_data('*')
        # Load HEP-e Lv.2 3-D flux data
        timespan('2017-04-05 21:45:00', 2.25, keyword='hours')
        pyspedas.erg.hep( trange=[ '2017-04-05 21:45:00', '2017-04-05 23:59:59'], datatype='3dflux' )
        vars = pyspedas.erg.mgf(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary B-field data
        vars = pyspedas.erg.orb(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary orbit data
        mag_vn = 'erg_mgf_l2_mag_8sec_dsi'
        pos_vn = 'erg_orb_l2_pos_gse'
        # Calculate and plot energy spectrum
        vars = erg_hep_part_products( 'erg_hep_l2_FEDU_L', mag_name=mag_vn, pos_name=pos_vn, outputs='fac_moments')
        tplot(vars, display=display, save_png='erg_hep_fac_moments.png' )
        self.assertTrue('erg_hep_l2_FEDU_L_density_mag' in vars)
        self.assertTrue(data_exists('erg_hep_l2_FEDU_L_density_mag'))

    def test_hep_fac_energy(self):
        del_data('*')
        # Load HEP-e Lv.2 3-D flux data
        timespan('2017-04-05 21:45:00', 2.25, keyword='hours')
        pyspedas.erg.hep( trange=[ '2017-04-05 21:45:00', '2017-04-05 23:59:59'], datatype='3dflux' )
        vars = pyspedas.erg.mgf(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary B-field data
        vars = pyspedas.erg.orb(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary orbit data
        mag_vn = 'erg_mgf_l2_mag_8sec_dsi'
        pos_vn = 'erg_orb_l2_pos_gse'
        # Calculate and plot energy spectrum
        vars = erg_hep_part_products( 'erg_hep_l2_FEDU_L', mag_name=mag_vn, pos_name=pos_vn, outputs='fac_energy' )
        tplot(vars, display=display, save_png='erg_hep_fac_energy.png' )
        self.assertTrue('erg_hep_l2_FEDU_L_energy_mag' in vars)
        self.assertTrue(data_exists('erg_hep_l2_FEDU_L_energy_mag'))

    def test_hep_gyro(self):
        del_data('*')
        # Load HEP-e Lv.2 3-D flux data
        timespan('2017-04-05 21:45:00', 2.25, keyword='hours')
        pyspedas.erg.hep( trange=[ '2017-04-05 21:45:00', '2017-04-05 23:59:59'], datatype='3dflux' )
        vars = pyspedas.erg.mgf(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary B-field data
        vars = pyspedas.erg.orb(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary orbit data
        mag_vn = 'erg_mgf_l2_mag_8sec_dsi'
        pos_vn = 'erg_orb_l2_pos_gse'
        # Calculate and plot energy spectrum
        vars = erg_hep_part_products( 'erg_hep_l2_FEDU_L', mag_name=mag_vn, pos_name=pos_vn, outputs='gyro' )
        tplot(vars, display=display, save_png='erg_hep_gyro.png' )
        self.assertTrue('erg_hep_l2_FEDU_L_gyro' in vars)
        self.assertTrue(data_exists('erg_hep_l2_FEDU_L_gyro'))

    def test_hep_energy(self):
        del_data('*')
        # Load HEP-e Lv.2 3-D flux data
        timespan('2017-04-05 21:45:00', 2.25, keyword='hours')
        pyspedas.erg.hep( trange=[ '2017-04-05 21:45:00', '2017-04-05 23:59:59'], datatype='3dflux' )
        # Calculate and plot energy spectrum
        vars = erg_hep_part_products( 'erg_hep_l2_FEDU_L', outputs='energy' )
        tplot( 'erg_hep_l2_FEDU_L_energy', display=display, save_png='erg_hep_en_spec.png' )
        self.assertTrue('erg_hep_l2_FEDU_L_energy' in vars)
        self.assertTrue(data_exists('erg_hep_l2_FEDU_L_energy'))

    def test_hep_energy_limit_gyro(self):
        del_data('*')
        # Load LEP-e Lv.2 3-D flux data
        timespan('2017-04-05 21:45:00', 2.25, keyword='hours')
        pyspedas.erg.hep(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'], datatype='3dflux')
        vars = pyspedas.erg.mgf(
            trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary B-field data
        vars = pyspedas.erg.orb(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary orbit data
        mag_vn = 'erg_mgf_l2_mag_8sec_dsi'
        pos_vn = 'erg_orb_l2_pos_gse'
        # Calculate the pitch angle distribution
        vars = erg_hep_part_products('erg_hep_l2_FEDU_L', outputs='energy', gyro=[0., 180.],
                                     fac_type='xdsi',
                                     mag_name=mag_vn, pos_name=pos_vn,
                                     trange=['2017-04-05 21:45:00', '2017-04-05 22:45:00'])
        tplot( 'erg_hep_l2_FEDU_L_energy_mag', display=display, save_png='erg_hep_energy_limit_gyro.png' )
        self.assertTrue(data_exists('erg_hep_l2_FEDU_L_energy_mag'))
        self.assertTrue('erg_hep_l2_FEDU_L_energy_mag' in vars)

    def test_hep_pad(self):
        del_data('*')
        # Load HEP-e Lv.2 3-D flux data
        timespan('2017-04-05 21:45:00', 2.25, keyword='hours')
        pyspedas.erg.hep( trange=[ '2017-04-05 21:45:00', '2017-04-05 23:59:59'], datatype='3dflux' )
        vars = pyspedas.erg.mgf(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary B-field data
        vars = pyspedas.erg.orb(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary orbit data
        mag_vn = 'erg_mgf_l2_mag_8sec_dsi'
        pos_vn = 'erg_orb_l2_pos_gse'
        # Calculate the pitch angle distribution
        vars = erg_hep_part_products('erg_hep_l2_FEDU_L', outputs='pa', energy=[15000., 22000.], fac_type='xdsi',
                                     mag_name=mag_vn, pos_name=pos_vn)
        tplot( 'erg_hep_l2_FEDU_L_pa', display=display, save_png='erg_hep_pad.png' )
        self.assertTrue('erg_hep_l2_FEDU_L_pa' in vars)
        self.assertTrue(data_exists('erg_hep_l2_FEDU_L_pa'))

    def test_hep_en_pad_limit(self):
        del_data('*')
        # Load HEP-e Lv.2 3-D flux data
        timespan('2017-04-05 21:45:00', 2.25, keyword='hours')
        pyspedas.erg.hep( trange=[ '2017-04-05 21:45:00', '2017-04-05 23:59:59'], datatype='3dflux' )
        vars = pyspedas.erg.mgf(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary B-field data
        vars = pyspedas.erg.orb(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary orbit data
        mag_vn = 'erg_mgf_l2_mag_8sec_dsi'
        pos_vn = 'erg_orb_l2_pos_gse'
        # Calculate energy-time spectra of electron flux for limited pitch-angle (PA) ranges
        ## Here we calculate energy-time spectra for PA = 0-10 deg and PA = 80-100 deg.
        vars1 = erg_hep_part_products('erg_hep_l2_FEDU_L', outputs='fac_energy', pitch=[80., 100.],
                                     fac_type='xdsi', mag_name=mag_vn, pos_name=pos_vn,
                                     suffix='_pa80-100')
        vars2 = erg_hep_part_products('erg_hep_l2_FEDU_L', outputs='fac_energy', pitch=[0., 10.], fac_type='xdsi',
                                     mag_name=mag_vn, pos_name=pos_vn,
                                     suffix='_pa0-10')

        ## Decorate the obtained spectrum variables
        pytplot.options('erg_hep_l2_FEDU_L_energy_mag_pa80-100', 'ytitle', 'HEP-e flux\nPA: 80-100\n\n[eV]')
        pytplot.options('erg_hep_l2_FEDU_L_energy_mag_pa0-10', 'ytitle', 'HEP-e flux\nPA: 0-10\n\n[eV]')
        tplot(['erg_hep_l2_FEDU_L_energy_mag_pa80-100', 'erg_hep_l2_FEDU_L_energy_mag_pa0-10'], display=display, save_png='erg_lep_en_pa_limit.png')
        self.assertTrue('erg_hep_l2_FEDU_L_energy_mag_pa0-10' in vars2)
        self.assertTrue(data_exists('erg_hep_l2_FEDU_L_energy_mag_pa0-10'))
        self.assertTrue('erg_hep_l2_FEDU_L_energy_mag_pa80-100' in vars1)
        self.assertTrue(data_exists('erg_hep_l2_FEDU_L_energy_mag_pa80-100'))

if __name__ == '__main__':
    unittest.main()