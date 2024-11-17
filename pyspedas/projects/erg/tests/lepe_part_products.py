
import os
import unittest
from pytplot import data_exists, del_data, timespan,tplot
from pyspedas.projects.erg import erg_lep_part_products

import pyspedas
import pytplot

display=False

class LoadTestCases(unittest.TestCase):

    def test_lepe_theta(self):
        del_data('*')
        # Load LEP-e Lv.2 3-D flux data
        timespan('2017-04-05 21:45:00', 2.25, keyword='hours')
        pyspedas.projects.erg.lepe( trange=[ '2017-04-05 21:45:00', '2017-04-05 22:45:00'], datatype='3dflux' )
        # Calculate and plot energy spectrum
        vars = erg_lep_part_products( 'erg_lepe_l2_3dflux_FEDU', outputs='theta', trange=[ '2017-04-05 21:45:00', '2017-04-05 23:59:59'] )
        tplot( 'erg_lepe_l2_3dflux_FEDU_theta', display=display, save_png='erg_lepe_theta.png' )
        self.assertTrue(data_exists('erg_lepe_l2_3dflux_FEDU_theta'))
        self.assertTrue('erg_lepe_l2_3dflux_FEDU_theta' in vars)

    def test_lepe_theta_limit_phi(self):
        del_data('*')
        # Load LEP-e Lv.2 3-D flux data
        timespan('2017-04-05 21:45:00', 2.25, keyword='hours')
        pyspedas.projects.erg.lepe( trange=[ '2017-04-05 21:45:00', '2017-04-05 22:45:00'], datatype='3dflux' )
        # Calculate and plot energy spectrum
        vars = erg_lep_part_products( 'erg_lepe_l2_3dflux_FEDU', outputs='theta', trange=[ '2017-04-05 21:45:00', '2017-04-05 23:59:59'], phi_in=[0., 180.0] )
        tplot( 'erg_lepe_l2_3dflux_FEDU_theta', display=display, save_png='erg_lepe_theta_limit_phi.png' )
        self.assertTrue(data_exists('erg_lepe_l2_3dflux_FEDU_theta'))
        self.assertTrue('erg_lepe_l2_3dflux_FEDU_theta' in vars)

    def test_lepe_theta_no_trange(self):
        del_data('*')
        # Load LEP-e Lv.2 3-D flux data
        timespan('2017-04-05 21:45:00', 2.25, keyword='hours')
        pyspedas.projects.erg.lepe( trange=[ '2017-04-05 21:45:00', '2017-04-05 22:45:00'], datatype='3dflux' )
        # Calculate and plot energy spectrum
        vars = erg_lep_part_products( 'erg_lepe_l2_3dflux_FEDU', outputs='theta' )
        tplot( 'erg_lepe_l2_3dflux_FEDU_theta', display=display, save_png='erg_lepe_theta_no_trange.png' )
        self.assertTrue(data_exists('erg_lepe_l2_3dflux_FEDU_theta'))
        self.assertTrue('erg_lepe_l2_3dflux_FEDU_theta' in vars)

    def test_lepe_phi(self):
        del_data('*')
        # Load LEP-e Lv.2 3-D flux data
        timespan('2017-04-05 21:45:00', 2.25, keyword='hours')
        pyspedas.projects.erg.lepe( trange=[ '2017-04-05 21:45:00', '2017-04-05 23:59:59'], datatype='3dflux' )
        # Calculate and plot energy spectrum
        vars = erg_lep_part_products( 'erg_lepe_l2_3dflux_FEDU', outputs='phi', trange=[ '2017-04-05 21:45:00', '2017-04-05 22:45:00'] )
        tplot( 'erg_lepe_l2_3dflux_FEDU_phi', display=display, save_png='erg_lepe_phi.png' )
        self.assertTrue(data_exists('erg_lepe_l2_3dflux_FEDU_phi'))
        self.assertTrue('erg_lepe_l2_3dflux_FEDU_phi' in vars)


    def test_lepe_pa(self):
        del_data('*')
        # Load LEP-e Lv.2 3-D flux data
        timespan('2017-04-05 21:45:00', 2.25, keyword='hours')
        pyspedas.projects.erg.lepe( trange=[ '2017-04-05 21:45:00', '2017-04-05 23:59:59'], datatype='3dflux' )
        vars = pyspedas.projects.erg.mgf(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary B-field data
        vars = pyspedas.projects.erg.orb(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary orbit data
        mag_vn = 'erg_mgf_l2_mag_8sec_dsi'
        pos_vn = 'erg_orb_l2_pos_gse'
        # Calculate and plot energy spectrum
        vars = erg_lep_part_products( 'erg_lepe_l2_3dflux_FEDU', mag_name=mag_vn, pos_name=pos_vn, outputs='pa', trange=[ '2017-04-05 21:45:00', '2017-04-05 22:45:00'] )
        tplot( 'erg_lepe_l2_3dflux_FEDU_pa', display=display, save_png='erg_lepe_pa.png' )
        self.assertTrue(data_exists('erg_lepe_l2_3dflux_FEDU_pa'))
        self.assertTrue('erg_lepe_l2_3dflux_FEDU_pa' in vars)

    def test_lepe_gyro(self):
        del_data('*')
        # Load LEP-e Lv.2 3-D flux data
        timespan('2017-04-05 21:45:00', 2.25, keyword='hours')
        pyspedas.projects.erg.lepe( trange=[ '2017-04-05 21:45:00', '2017-04-05 23:59:59'], datatype='3dflux' )
        vars = pyspedas.projects.erg.mgf(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary B-field data
        vars = pyspedas.projects.erg.orb(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary orbit data
        mag_vn = 'erg_mgf_l2_mag_8sec_dsi'
        pos_vn = 'erg_orb_l2_pos_gse'
        # Calculate and plot energy spectrum
        vars = erg_lep_part_products( 'erg_lepe_l2_3dflux_FEDU', mag_name=mag_vn, pos_name=pos_vn, outputs='gyro', trange=[ '2017-04-05 21:45:00', '2017-04-05 22:45:00'] )
        tplot( 'erg_lepe_l2_3dflux_FEDU_gyro', display=display, save_png='erg_lepe_gyro.png' )
        self.assertTrue(data_exists('erg_lepe_l2_3dflux_FEDU_gyro'))
        self.assertTrue('erg_lepe_l2_3dflux_FEDU_gyro' in vars)

    def test_lepe_moments(self):
        del_data('*')
        # Load LEP-e Lv.2 3-D flux data
        timespan('2017-04-05 21:45:00', 2.25, keyword='hours')
        pyspedas.projects.erg.lepe( trange=[ '2017-04-05 21:45:00', '2017-04-05 23:59:59'], datatype='3dflux' )
        vars = pyspedas.projects.erg.mgf(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary B-field data
        vars = pyspedas.projects.erg.orb(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary orbit data
        mag_vn = 'erg_mgf_l2_mag_8sec_dsi'
        pos_vn = 'erg_orb_l2_pos_gse'
        # Calculate and plot energy spectrum
        vars = erg_lep_part_products( 'erg_lepe_l2_3dflux_FEDU', mag_name=mag_vn, pos_name=pos_vn, outputs='moments', trange=[ '2017-04-05 21:45:00', '2017-04-05 22:45:00'] )
        tplot(vars, display=display, save_png='erg_lepe_moments.png' )
        self.assertTrue(data_exists('erg_lepe_l2_3dflux_FEDU_density'))
        self.assertTrue('erg_lepe_l2_3dflux_FEDU_density' in vars)

    def test_lepe_fac_moments(self):
        del_data('*')
        # Load LEP-e Lv.2 3-D flux data
        timespan('2017-04-05 21:45:00', 2.25, keyword='hours')
        pyspedas.projects.erg.lepe( trange=[ '2017-04-05 21:45:00', '2017-04-05 23:59:59'], datatype='3dflux' )
        vars = pyspedas.projects.erg.mgf(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary B-field data
        vars = pyspedas.projects.erg.orb(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary orbit data
        mag_vn = 'erg_mgf_l2_mag_8sec_dsi'
        pos_vn = 'erg_orb_l2_pos_gse'
        # Calculate and plot energy spectrum
        vars = erg_lep_part_products( 'erg_lepe_l2_3dflux_FEDU', mag_name=mag_vn, pos_name=pos_vn, outputs='fac_moments', trange=[ '2017-04-05 21:45:00', '2017-04-05 22:45:00'] )
        tplot(vars, display=display, save_png='erg_lepe_fac_moments.png' )
        self.assertTrue(data_exists('erg_lepe_l2_3dflux_FEDU_density_mag'))
        self.assertTrue('erg_lepe_l2_3dflux_FEDU_density_mag' in vars)

    def test_lepe_fac_energy(self):
        del_data('*')
        # Load LEP-e Lv.2 3-D flux data
        timespan('2017-04-05 21:45:00', 2.25, keyword='hours')
        pyspedas.projects.erg.lepe( trange=[ '2017-04-05 21:45:00', '2017-04-05 23:59:59'], datatype='3dflux' )
        vars = pyspedas.projects.erg.mgf(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary B-field data
        vars = pyspedas.projects.erg.orb(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary orbit data
        mag_vn = 'erg_mgf_l2_mag_8sec_dsi'
        pos_vn = 'erg_orb_l2_pos_gse'
        # Calculate and plot energy spectrum
        vars = erg_lep_part_products( 'erg_lepe_l2_3dflux_FEDU', mag_name=mag_vn, pos_name=pos_vn, outputs='fac_energy', trange=[ '2017-04-05 21:45:00', '2017-04-05 22:45:00'] )
        self.assertTrue('erg_lepe_l2_3dflux_FEDU_energy_mag' in vars)
        self.assertTrue(data_exists('erg_lepe_l2_3dflux_FEDU_energy_mag'))
        tplot('erg_lepe_l2_3dflux_FEDU_energy_mag', display=display, save_png='erg_lepe_fac_energy.png' )

    def test_lepe_energy(self):
        del_data('*')
        # Load LEP-e Lv.2 3-D flux data
        timespan('2017-04-05 21:45:00', 2.25, keyword='hours')
        pyspedas.projects.erg.lepe( trange=[ '2017-04-05 21:45:00', '2017-04-05 23:59:59'], datatype='3dflux' )
        # Calculate and plot energy spectrum
        vars = erg_lep_part_products( 'erg_lepe_l2_3dflux_FEDU', outputs='energy', trange=[ '2017-04-05 21:45:00', '2017-04-05 22:45:00'] )
        tplot( 'erg_lepe_l2_3dflux_FEDU_energy', display=display, save_png='erg_lepe_en_spec.png' )
        self.assertTrue(data_exists('erg_lepe_l2_3dflux_FEDU_energy'))
        self.assertTrue('erg_lepe_l2_3dflux_FEDU_energy' in vars)

    def test_lepe_pad(self):
        del_data('*')
        # Load LEP-e Lv.2 3-D flux data
        timespan('2017-04-05 21:45:00', 2.25, keyword='hours')
        pyspedas.projects.erg.lepe( trange=[ '2017-04-05 21:45:00', '2017-04-05 23:59:59'], datatype='3dflux' )
        vars = pyspedas.projects.erg.mgf(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary B-field data
        vars = pyspedas.projects.erg.orb(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary orbit data
        mag_vn = 'erg_mgf_l2_mag_8sec_dsi'
        pos_vn = 'erg_orb_l2_pos_gse'
        # Calculate the pitch angle distribution
        vars = erg_lep_part_products('erg_lepe_l2_3dflux_FEDU', outputs='pa', energy=[15000., 22000.], fac_type='xdsi',
                                     mag_name=mag_vn, pos_name=pos_vn,
                                     trange=[ '2017-04-05 21:45:00', '2017-04-05 22:45:00'])
        self.assertTrue(data_exists('erg_lepe_l2_3dflux_FEDU_pa'))
        self.assertTrue('erg_lepe_l2_3dflux_FEDU_pa' in vars)
        tplot('erg_lepe_l2_3dflux_FEDU_pa', display=display, save_png='erg_lepe_pa.png')

    def test_lepe_energy_limit_gyro(self):
        del_data('*')
        # Load LEP-e Lv.2 3-D flux data
        timespan('2017-04-05 21:45:00', 2.25, keyword='hours')
        pyspedas.projects.erg.lepe(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'], datatype='3dflux')
        vars = pyspedas.projects.erg.mgf(
            trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary B-field data
        vars = pyspedas.projects.erg.orb(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary orbit data
        mag_vn = 'erg_mgf_l2_mag_8sec_dsi'
        pos_vn = 'erg_orb_l2_pos_gse'
        # Calculate the pitch angle distribution
        vars = erg_lep_part_products('erg_lepe_l2_3dflux_FEDU', outputs='energy', gyro=[0., 180.],
                                     fac_type='xdsi',
                                     mag_name=mag_vn, pos_name=pos_vn,
                                     trange=['2017-04-05 21:45:00', '2017-04-05 22:45:00'])
        tplot( 'erg_lepe_l2_3dflux_FEDU_energy_mag', display=display, save_png='erg_lepe_energy_limit_gyro.png' )
        self.assertTrue(data_exists('erg_lepe_l2_3dflux_FEDU_energy_mag'))
        self.assertTrue('erg_lepe_l2_3dflux_FEDU_energy_mag' in vars)

    def test_lepe_en_pad_limit(self):
        del_data('*')
        # Load LEP-e Lv.2 3-D flux data
        timespan('2017-04-05 21:45:00', 2.25, keyword='hours')
        pyspedas.projects.erg.lepe( trange=[ '2017-04-05 21:45:00', '2017-04-05 23:59:59'], datatype='3dflux' )
        vars = pyspedas.projects.erg.mgf(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary B-field data
        vars = pyspedas.projects.erg.orb(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary orbit data
        mag_vn = 'erg_mgf_l2_mag_8sec_dsi'
        pos_vn = 'erg_orb_l2_pos_gse'
        # Calculate energy-time spectra of electron flux for limited pitch-angle (PA) ranges
        ## Here we calculate energy-time spectra for PA = 0-10 deg and PA = 80-100 deg.
        vars1 = erg_lep_part_products('erg_lepe_l2_3dflux_FEDU', outputs='fac_energy', pitch=[80., 100.],
                                     fac_type='xdsi', mag_name=mag_vn, pos_name=pos_vn,
                                     trange=['2017-04-05 21:45:00', '2017-04-05 22:45:00'], suffix='_pa80-100')
        vars2 = erg_lep_part_products('erg_lepe_l2_3dflux_FEDU', outputs='fac_energy', pitch=[0., 10.], fac_type='xdsi',
                                     mag_name=mag_vn, pos_name=pos_vn,
                                     trange=['2017-04-05 21:45:00', '2017-04-05 22:45:00'], suffix='_pa0-10')
        ## Decorate the obtained spectrum variables
        pytplot.options('erg_lepe_l2_3dflux_FEDU_energy_mag_pa80-100', 'ytitle', 'LEP-e flux\nPA: 80-100\n\n[eV]')
        pytplot.options('erg_lepe_l2_3dflux_FEDU_energy_mag_pa0-10', 'ytitle', 'LEP-e flux\nPA: 0-10\n\n[eV]')
        tplot(['erg_lepe_l2_3dflux_FEDU_energy_mag_pa80-100', 'erg_lepe_l2_3dflux_FEDU_energy_mag_pa0-10'], display=display, save_png='erg_lepe_en_pa_limit.png')
        self.assertTrue(data_exists('erg_lepe_l2_3dflux_FEDU_energy_mag_pa80-100'))
        self.assertTrue('erg_lepe_l2_3dflux_FEDU_energy_mag_pa80-100' in vars1)
        self.assertTrue(data_exists('erg_lepe_l2_3dflux_FEDU_energy_mag_pa0-10'))
        self.assertTrue('erg_lepe_l2_3dflux_FEDU_energy_mag_pa0-10' in vars2)

if __name__ == '__main__':
    unittest.main()