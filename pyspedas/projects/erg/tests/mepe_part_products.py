
import os
import unittest
from pytplot import data_exists, del_data, timespan,tplot
from pyspedas.projects.erg import erg_mep_part_products

import pyspedas
import pytplot

display=False

class LoadTestCases(unittest.TestCase):

    def test_mepe_theta(self):
        del_data('*')
        # Load MEP-e Lv.2 3-D flux data
        timespan('2017-04-05 21:45:00', 2.25, keyword='hours')
        pyspedas.projects.erg.mepe( trange=[ '2017-04-05 21:45:00', '2017-04-05 23:59:59'], datatype='3dflux' )
        # Calculate and plot energy spectrum
        vars = erg_mep_part_products( 'erg_mepe_l2_3dflux_FEDU', outputs='theta', trange=[ '2017-04-05 21:45:00', '2017-04-05 23:59:59'] )
        tplot( 'erg_mepe_l2_3dflux_FEDU_theta', display=display, save_png='erg_mepe_theta.png' )
        self.assertTrue('erg_mepe_l2_3dflux_FEDU_theta' in vars)
        self.assertTrue(data_exists('erg_mepe_l2_3dflux_FEDU_theta'))

    def test_mepe_theta_no_trange(self):
        del_data('*')
        # Load MEP-e Lv.2 3-D flux data
        timespan('2017-04-05 21:45:00', 2.25, keyword='hours')
        pyspedas.projects.erg.mepe( trange=[ '2017-04-05 21:45:00', '2017-04-05 23:59:59'], datatype='3dflux' )
        # Calculate and plot energy spectrum
        vars = erg_mep_part_products( 'erg_mepe_l2_3dflux_FEDU', outputs='theta' )
        tplot( 'erg_mepe_l2_3dflux_FEDU_theta', display=display, save_png='erg_mepe_theta_no_trange.png' )
        self.assertTrue('erg_mepe_l2_3dflux_FEDU_theta' in vars)
        self.assertTrue(data_exists('erg_mepe_l2_3dflux_FEDU_theta'))

    def test_mepe_phi(self):
        del_data('*')
        # Load MEP-e Lv.2 3-D flux data
        timespan('2017-04-05 21:45:00', 2.25, keyword='hours')
        pyspedas.projects.erg.mepe( trange=[ '2017-04-05 21:45:00', '2017-04-05 23:59:59'], datatype='3dflux' )
        # Calculate and plot energy spectrum
        vars = erg_mep_part_products( 'erg_mepe_l2_3dflux_FEDU', outputs='phi', trange=[ '2017-04-05 21:45:00', '2017-04-05 23:59:59'] )
        tplot( 'erg_mepe_l2_3dflux_FEDU_phi', display=display, save_png='erg_mepe_phi.png' )
        self.assertTrue('erg_mepe_l2_3dflux_FEDU_phi' in vars)
        self.assertTrue(data_exists('erg_mepe_l2_3dflux_FEDU_phi'))


    def test_mepe_pa(self):
        del_data('*')
        # Load MEP-e Lv.2 3-D flux data
        timespan('2017-04-05 21:45:00', 2.25, keyword='hours')
        pyspedas.projects.erg.mepe( trange=[ '2017-04-05 21:45:00', '2017-04-05 23:59:59'], datatype='3dflux' )
        vars = pyspedas.projects.erg.mgf(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary B-field data
        vars = pyspedas.projects.erg.orb(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary orbit data
        mag_vn = 'erg_mgf_l2_mag_8sec_dsi'
        pos_vn = 'erg_orb_l2_pos_gse'
        # Calculate and plot energy spectrum
        vars = erg_mep_part_products( 'erg_mepe_l2_3dflux_FEDU', mag_name=mag_vn, pos_name=pos_vn, outputs='pa', trange=[ '2017-04-05 21:45:00', '2017-04-05 23:59:59'] )
        tplot( 'erg_mepe_l2_3dflux_FEDU_pa', display=display, save_png='erg_mepe_pa.png' )
        self.assertTrue('erg_mepe_l2_3dflux_FEDU_pa' in vars)
        self.assertTrue(data_exists('erg_mepe_l2_3dflux_FEDU_pa'))

    def test_mepe_gyro(self):
        del_data('*')
        # Load MEP-e Lv.2 3-D flux data
        timespan('2017-04-05 21:45:00', 2.25, keyword='hours')
        pyspedas.projects.erg.mepe( trange=[ '2017-04-05 21:45:00', '2017-04-05 23:59:59'], datatype='3dflux' )
        vars = pyspedas.projects.erg.mgf(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary B-field data
        vars = pyspedas.projects.erg.orb(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary orbit data
        mag_vn = 'erg_mgf_l2_mag_8sec_dsi'
        pos_vn = 'erg_orb_l2_pos_gse'
        # Calculate and plot energy spectrum
        vars = erg_mep_part_products( 'erg_mepe_l2_3dflux_FEDU', mag_name=mag_vn, pos_name=pos_vn, outputs='gyro', trange=[ '2017-04-05 21:45:00', '2017-04-05 23:59:59'] )
        tplot( 'erg_mepe_l2_3dflux_FEDU_gyro', display=display, save_png='erg_mepe_gyro.png' )
        self.assertTrue('erg_mepe_l2_3dflux_FEDU_gyro' in vars)
        self.assertTrue(data_exists('erg_mepe_l2_3dflux_FEDU_gyro'))

    def test_mepe_moments(self):
        del_data('*')
        # Load MEP-e Lv.2 3-D flux data
        timespan('2017-04-05 21:45:00', 2.25, keyword='hours')
        pyspedas.projects.erg.mepe( trange=[ '2017-04-05 21:45:00', '2017-04-05 23:59:59'], datatype='3dflux' )
        vars = pyspedas.projects.erg.mgf(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary B-field data
        vars = pyspedas.projects.erg.orb(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary orbit data
        mag_vn = 'erg_mgf_l2_mag_8sec_dsi'
        pos_vn = 'erg_orb_l2_pos_gse'
        # Calculate and plot energy spectrum
        vars = erg_mep_part_products( 'erg_mepe_l2_3dflux_FEDU', mag_name=mag_vn, pos_name=pos_vn, outputs='moments', trange=[ '2017-04-05 21:45:00', '2017-04-05 23:59:59'] )
        tplot(vars, display=display, save_png='erg_mepe_moments.png' )
        self.assertTrue('erg_mepe_l2_3dflux_FEDU_density' in vars)
        self.assertTrue(data_exists('erg_mepe_l2_3dflux_FEDU_density'))

    def test_mepe_fac_moments(self):
        del_data('*')
        # Load MEP-e Lv.2 3-D flux data
        timespan('2017-04-05 21:45:00', 2.25, keyword='hours')
        pyspedas.projects.erg.mepe( trange=[ '2017-04-05 21:45:00', '2017-04-05 23:59:59'], datatype='3dflux' )
        vars = pyspedas.projects.erg.mgf(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary B-field data
        vars = pyspedas.projects.erg.orb(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary orbit data
        mag_vn = 'erg_mgf_l2_mag_8sec_dsi'
        pos_vn = 'erg_orb_l2_pos_gse'
        # Calculate and plot energy spectrum
        vars = erg_mep_part_products( 'erg_mepe_l2_3dflux_FEDU', mag_name=mag_vn, pos_name=pos_vn, outputs='fac_moments', trange=[ '2017-04-05 21:45:00', '2017-04-05 23:59:59'] )
        tplot(vars, display=display, save_png='erg_mepe_fac_moments.png' )
        self.assertTrue('erg_mepe_l2_3dflux_FEDU_density_mag' in vars)
        self.assertTrue(data_exists('erg_mepe_l2_3dflux_FEDU_density_mag'))

    def test_mepe_fac_energy(self):
        del_data('*')
        # Load MEP-e Lv.2 3-D flux data
        timespan('2017-04-05 21:45:00', 2.25, keyword='hours')
        pyspedas.projects.erg.mepe( trange=[ '2017-04-05 21:45:00', '2017-04-05 23:59:59'], datatype='3dflux' )
        vars = pyspedas.projects.erg.mgf(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary B-field data
        vars = pyspedas.projects.erg.orb(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary orbit data
        mag_vn = 'erg_mgf_l2_mag_8sec_dsi'
        pos_vn = 'erg_orb_l2_pos_gse'
        # Calculate and plot energy spectrum
        vars = erg_mep_part_products( 'erg_mepe_l2_3dflux_FEDU', mag_name=mag_vn, pos_name=pos_vn, outputs='fac_energy', trange=[ '2017-04-05 21:45:00', '2017-04-05 23:59:59'] )
        tplot(vars, display=display, save_png='erg_mepe_fac_energy.png' )
        self.assertTrue('erg_mepe_l2_3dflux_FEDU_energy_mag' in vars)
        self.assertTrue(data_exists('erg_mepe_l2_3dflux_FEDU_energy_mag'))

    def test_mepe_energy(self):
        del_data('*')
        # Load MEP-e Lv.2 3-D flux data
        timespan('2017-04-05 21:45:00', 2.25, keyword='hours')
        pyspedas.projects.erg.mepe( trange=[ '2017-04-05 21:45:00', '2017-04-05 23:59:59'], datatype='3dflux' )
        # Calculate and plot energy spectrum
        vars = erg_mep_part_products( 'erg_mepe_l2_3dflux_FEDU', outputs='energy', trange=[ '2017-04-05 21:45:00', '2017-04-05 23:59:59'] )
        tplot( 'erg_mepe_l2_3dflux_FEDU_energy', display=display, save_png='erg_mepe_en_spec.png' )
        self.assertTrue('erg_mepe_l2_3dflux_FEDU_energy' in vars)
        self.assertTrue(data_exists('erg_mepe_l2_3dflux_FEDU_energy'))


    def test_mepe_pad_xdsi(self):
        del_data('*')
        # Load MEP-e Lv.2 3-D flux data
        timespan('2017-04-05 21:45:00', 2.25, keyword='hours')
        pyspedas.projects.erg.mepe( trange=[ '2017-04-05 21:45:00', '2017-04-05 23:59:59'], datatype='3dflux' )
        vars = pyspedas.projects.erg.mgf(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary B-field data
        vars = pyspedas.projects.erg.orb(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary orbit data
        mag_vn = 'erg_mgf_l2_mag_8sec_dsi'
        pos_vn = 'erg_orb_l2_pos_gse'
        # Calculate the pitch angle distribution
        vars = erg_mep_part_products('erg_mepe_l2_3dflux_FEDU', outputs='pa', energy=[15000., 22000.], fac_type='xdsi',
                                     mag_name=mag_vn, pos_name=pos_vn,
                                     trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])
        tplot( 'erg_mepe_l2_3dflux_FEDU_pa', display=display, save_png='erg_mepe_pad_xdsi.png' )
        self.assertTrue('erg_mepe_l2_3dflux_FEDU_pa' in vars)
        self.assertTrue(data_exists('erg_mepe_l2_3dflux_FEDU_pa'))

    def test_mepe_pad_mphigeo(self):
        del_data('*')
        # Load MEP-e Lv.2 3-D flux data
        timespan('2017-04-05 21:45:00', 2.25, keyword='hours')
        pyspedas.projects.erg.mepe( trange=[ '2017-04-05 21:45:00', '2017-04-05 23:59:59'], datatype='3dflux' )
        vars = pyspedas.projects.erg.mgf(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary B-field data
        vars = pyspedas.projects.erg.orb(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary orbit data
        mag_vn = 'erg_mgf_l2_mag_8sec_dsi'
        pos_vn = 'erg_orb_l2_pos_gse'
        # Calculate the pitch angle distribution
        vars = erg_mep_part_products('erg_mepe_l2_3dflux_FEDU', outputs='pa', energy=[15000., 22000.], fac_type='mphigeo',
                                     mag_name=mag_vn, pos_name=pos_vn,
                                     trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])
        tplot( 'erg_mepe_l2_3dflux_FEDU_pa', display=display, save_png='erg_mepe_pad_mphigeo.png' )
        self.assertTrue('erg_mepe_l2_3dflux_FEDU_pa' in vars)
        self.assertTrue(data_exists('erg_mepe_l2_3dflux_FEDU_pa'))

    def test_mepe_pad_phigeo(self):
        del_data('*')
        # Load MEP-e Lv.2 3-D flux data
        timespan('2017-04-05 21:45:00', 2.25, keyword='hours')
        pyspedas.projects.erg.mepe( trange=[ '2017-04-05 21:45:00', '2017-04-05 23:59:59'], datatype='3dflux' )
        vars = pyspedas.projects.erg.mgf(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary B-field data
        vars = pyspedas.projects.erg.orb(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary orbit data
        mag_vn = 'erg_mgf_l2_mag_8sec_dsi'
        pos_vn = 'erg_orb_l2_pos_gse'
        # Calculate the pitch angle distribution
        vars = erg_mep_part_products('erg_mepe_l2_3dflux_FEDU', outputs='pa', energy=[15000., 22000.], fac_type='phigeo',
                                     mag_name=mag_vn, pos_name=pos_vn,
                                     trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])
        self.assertTrue('erg_mepe_l2_3dflux_FEDU_pa' in vars)
        self.assertTrue(data_exists('erg_mepe_l2_3dflux_FEDU_pa'))

    def test_mepe_pad_xgse(self):
        del_data('*')
        # Load MEP-e Lv.2 3-D flux data
        timespan('2017-04-05 21:45:00', 2.25, keyword='hours')
        pyspedas.projects.erg.mepe(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'], datatype='3dflux')
        vars = pyspedas.projects.erg.mgf(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary B-field data
        vars = pyspedas.projects.erg.orb(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary orbit data
        mag_vn = 'erg_mgf_l2_mag_8sec_dsi'
        pos_vn = 'erg_orb_l2_pos_gse'
        # Calculate the pitch angle distribution
        vars = erg_mep_part_products('erg_mepe_l2_3dflux_FEDU', outputs='pa', energy=[15000., 22000.],
                                     fac_type='xgse',
                                     mag_name=mag_vn, pos_name=pos_vn,
                                     trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])
        tplot( 'erg_mepe_l2_3dflux_FEDU_pa', display=display, save_png='erg_mepe_pad_xgse.png' )
        self.assertTrue('erg_mepe_l2_3dflux_FEDU_pa' in vars)
        self.assertTrue(data_exists('erg_mepe_l2_3dflux_FEDU_pa'))

    def test_mepe_pad_phism(self):
        del_data('*')
        # Load MEP-e Lv.2 3-D flux data
        timespan('2017-04-05 21:45:00', 2.25, keyword='hours')
        pyspedas.projects.erg.mepe(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'], datatype='3dflux')
        vars = pyspedas.projects.erg.mgf(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary B-field data
        vars = pyspedas.projects.erg.orb(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary orbit data
        mag_vn = 'erg_mgf_l2_mag_8sec_dsi'
        pos_vn = 'erg_orb_l2_pos_gse'
        # Calculate the pitch angle distribution
        vars = erg_mep_part_products('erg_mepe_l2_3dflux_FEDU', outputs='pa', energy=[15000., 22000.],
                                     fac_type='phism',
                                     mag_name=mag_vn, pos_name=pos_vn,
                                     trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])
        tplot( 'erg_mepe_l2_3dflux_FEDU_pa', display=display, save_png='erg_mepe_pad_phism.png' )
        self.assertTrue('erg_mepe_l2_3dflux_FEDU_pa' in vars)
        self.assertTrue(data_exists('erg_mepe_l2_3dflux_FEDU_pa'))

    def test_mepe_pad_mphism(self):
        del_data('*')
        # Load MEP-e Lv.2 3-D flux data
        timespan('2017-04-05 21:45:00', 2.25, keyword='hours')
        pyspedas.projects.erg.mepe(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'], datatype='3dflux')
        vars = pyspedas.projects.erg.mgf(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary B-field data
        vars = pyspedas.projects.erg.orb(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary orbit data
        mag_vn = 'erg_mgf_l2_mag_8sec_dsi'
        pos_vn = 'erg_orb_l2_pos_gse'
        # Calculate the pitch angle distribution
        vars = erg_mep_part_products('erg_mepe_l2_3dflux_FEDU', outputs='pa', energy=[15000., 22000.],
                                     fac_type='mphism',
                                     mag_name=mag_vn, pos_name=pos_vn,
                                     trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])
        tplot( 'erg_mepe_l2_3dflux_FEDU_pa', display=display, save_png='erg_mepe_pad_mphism.png' )
        self.assertTrue('erg_mepe_l2_3dflux_FEDU_pa' in vars)
        self.assertTrue(data_exists('erg_mepe_l2_3dflux_FEDU_pa'))


    def test_mepe_en_pad_limit_gyro(self):
        del_data('*')
        # Load MEP-e Lv.2 3-D flux data
        timespan('2017-04-05 21:45:00', 2.25, keyword='hours')
        pyspedas.projects.erg.mepe( trange=[ '2017-04-05 21:45:00', '2017-04-05 23:59:59'], datatype='3dflux' )
        vars = pyspedas.projects.erg.mgf(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary B-field data
        vars = pyspedas.projects.erg.orb(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary orbit data
        mag_vn = 'erg_mgf_l2_mag_8sec_dsi'
        pos_vn = 'erg_orb_l2_pos_gse'
        # Calculate energy-time spectra of electron flux for limited pitch-angle (PA) ranges
        ## Here we calculate energy-time spectra for PA = 0-10 deg and PA = 80-100 deg.
        vars = erg_mep_part_products('erg_mepe_l2_3dflux_FEDU', outputs='fac_energy', gyro=[0.0, 90.0],
                                     fac_type='xdsi', mag_name=mag_vn, pos_name=pos_vn,
                                     trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])
        ## Decorate the obtained spectrum variables
        pytplot.options('erg_mepe_l2_3dflux_FEDU_energy_mag', 'ytitle', 'MEP-e flux\nPA: 80-100\n\n[eV]')
        tplot(['erg_mepe_l2_3dflux_FEDU_energy_mag'], display=display, save_png='erg_mep_en_pa_limit_gyro.png')
        self.assertTrue('erg_mepe_l2_3dflux_FEDU_energy_mag' in vars)
        self.assertTrue(data_exists('erg_mepe_l2_3dflux_FEDU_energy_mag'))


    def test_mepe_en_pad_limit_theta(self):
        del_data('*')
        # Load MEP-e Lv.2 3-D flux data
        timespan('2017-04-05 21:45:00', 2.25, keyword='hours')
        pyspedas.projects.erg.mepe( trange=[ '2017-04-05 21:45:00', '2017-04-05 23:59:59'], datatype='3dflux' )
        vars = pyspedas.projects.erg.mgf(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary B-field data
        vars = pyspedas.projects.erg.orb(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary orbit data
        mag_vn = 'erg_mgf_l2_mag_8sec_dsi'
        pos_vn = 'erg_orb_l2_pos_gse'
        # Calculate energy-time spectra of electron flux for limited pitch-angle (PA) ranges
        ## Here we calculate energy-time spectra for PA = 0-10 deg and PA = 80-100 deg.
        vars = erg_mep_part_products('erg_mepe_l2_3dflux_FEDU', outputs='fac_energy', theta=[0.0, 90.0],
                                     fac_type='xdsi', mag_name=mag_vn, pos_name=pos_vn,
                                     trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])
        ## Decorate the obtained spectrum variables
        pytplot.options('erg_mepe_l2_3dflux_FEDU_energy_mag', 'ytitle', 'MEP-e flux\nPA: 80-100\n\n[eV]')
        tplot(['erg_mepe_l2_3dflux_FEDU_energy_mag'], display=display, save_png='erg_mep_en_pa_limit_theta.png')
        self.assertTrue('erg_mepe_l2_3dflux_FEDU_energy_mag' in vars)
        self.assertTrue(data_exists('erg_mepe_l2_3dflux_FEDU_energy_mag'))

    def test_mepe_en_pad_limit_phi_in(self):
        del_data('*')
        # Load MEP-e Lv.2 3-D flux data
        timespan('2017-04-05 21:45:00', 2.25, keyword='hours')
        pyspedas.projects.erg.mepe( trange=[ '2017-04-05 21:45:00', '2017-04-05 23:59:59'], datatype='3dflux' )
        vars = pyspedas.projects.erg.mgf(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary B-field data
        vars = pyspedas.projects.erg.orb(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary orbit data
        mag_vn = 'erg_mgf_l2_mag_8sec_dsi'
        pos_vn = 'erg_orb_l2_pos_gse'
        # Calculate energy-time spectra of electron flux for limited pitch-angle (PA) ranges
        ## Here we calculate energy-time spectra for PA = 0-10 deg and PA = 80-100 deg.
        vars = erg_mep_part_products('erg_mepe_l2_3dflux_FEDU', outputs='fac_energy', phi_in=[0.0, 180.0],
                                     fac_type='xdsi', mag_name=mag_vn, pos_name=pos_vn,
                                     trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])
        ## Decorate the obtained spectrum variables
        pytplot.options('erg_mepe_l2_3dflux_FEDU_energy_mag', 'ytitle', 'MEP-e flux\nPA: 80-100\n\n[eV]')
        tplot(['erg_mepe_l2_3dflux_FEDU_energy_mag'], display=display, save_png='erg_mep_en_pa_limit_phi_in.png')
        self.assertTrue('erg_mepe_l2_3dflux_FEDU_energy_mag' in vars)
        self.assertTrue(data_exists('erg_mepe_l2_3dflux_FEDU_energy_mag'))

    def test_mepe_en_pad_limit_energy(self):
        del_data('*')
        # Load MEP-e Lv.2 3-D flux data
        timespan('2017-04-05 21:45:00', 2.25, keyword='hours')
        pyspedas.projects.erg.mepe( trange=[ '2017-04-05 21:45:00', '2017-04-05 23:59:59'], datatype='3dflux' )
        vars = pyspedas.projects.erg.mgf(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary B-field data
        vars = pyspedas.projects.erg.orb(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary orbit data
        mag_vn = 'erg_mgf_l2_mag_8sec_dsi'
        pos_vn = 'erg_orb_l2_pos_gse'
        # Calculate energy-time spectra of electron flux for limited pitch-angle (PA) ranges
        ## Here we calculate energy-time spectra for PA = 0-10 deg and PA = 80-100 deg.
        vars = erg_mep_part_products('erg_mepe_l2_3dflux_FEDU', outputs='fac_energy', energy=[15000., 22000.],
                                     fac_type='xdsi', mag_name=mag_vn, pos_name=pos_vn,
                                     trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])
        ## Decorate the obtained spectrum variables
        pytplot.options('erg_mepe_l2_3dflux_FEDU_energy_mag', 'ytitle', 'MEP-e flux\nPA: 80-100\n\n[eV]')
        tplot(['erg_mepe_l2_3dflux_FEDU_energy_mag'], display=display, save_png='erg_mep_en_pa_limit_energy.png')
        self.assertTrue('erg_mepe_l2_3dflux_FEDU_energy_mag' in vars)
        self.assertTrue(data_exists('erg_mepe_l2_3dflux_FEDU_energy_mag'))

if __name__ == '__main__':
    unittest.main()