
import os
import unittest
from pytplot import data_exists, del_data, timespan,tplot, tplot_names
from pyspedas.projects.erg import erg_xep_part_products

import pyspedas
import pytplot

display=False

class LoadTestCases(unittest.TestCase):

    # XEP has a single theta bin and only produces 2-D (energy x phi) distributions.
    # Therefore, theta and gyro spectrograms and moments are not available for this instrument.


    def test_xep_phi(self):
        del_data('*')
        # Load XEP-e Lv.2 3-D flux data
        timespan('2017-04-05 21:45:00', 2.25, keyword='hours')
        pyspedas.projects.erg.xep( trange=[ '2017-04-05 21:45:00', '2017-04-05 23:59:59'], datatype='2dflux' )
        # Calculate and plot energy spectrum
        vars = erg_xep_part_products( 'erg_xep_l2_FEDU_SSD', outputs='phi', trange=[ '2017-04-05 21:45:00', '2017-04-05 23:59:59'] )
        tplot( 'erg_xep_l2_FEDU_SSD_phi', display=display, save_png='erg_xep_phi.png' )
        self.assertTrue('erg_xep_l2_FEDU_SSD_phi' in vars)
        self.assertTrue(data_exists('erg_xep_l2_FEDU_SSD_phi'))

    def test_xep_phi_no_trange(self):
        del_data('*')
        # Load XEP-e Lv.2 3-D flux data
        timespan('2017-04-05 21:45:00', 2.25, keyword='hours')
        pyspedas.projects.erg.xep( trange=[ '2017-04-05 21:45:00', '2017-04-05 23:59:59'], datatype='2dflux' )
        # Calculate and plot energy spectrum
        vars = erg_xep_part_products( 'erg_xep_l2_FEDU_SSD', outputs='phi', trange=[ '2017-04-05 21:45:00', '2017-04-05 23:59:59'] )
        tplot( 'erg_xep_l2_FEDU_SSD_phi', display=display, save_png='erg_xep_phi_no_trange.png' )
        self.assertTrue('erg_xep_l2_FEDU_SSD_phi' in vars)
        self.assertTrue(data_exists('erg_xep_l2_FEDU_SSD_phi'))


    def test_xep_pa(self):
        del_data('*')
        # Load XEP-e Lv.2 3-D flux data
        timespan('2017-04-05 21:45:00', 2.25, keyword='hours')
        pyspedas.projects.erg.xep( trange=[ '2017-04-05 21:45:00', '2017-04-05 23:59:59'], datatype='2dflux' )
        vars = pyspedas.projects.erg.mgf(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary B-field data
        vars = pyspedas.projects.erg.orb(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary orbit data
        mag_vn = 'erg_mgf_l2_mag_8sec_dsi'
        pos_vn = 'erg_orb_l2_pos_gse'
        # Calculate and plot energy spectrum
        vars = erg_xep_part_products( 'erg_xep_l2_FEDU_SSD', mag_name=mag_vn, pos_name=pos_vn, outputs='pa', trange=[ '2017-04-05 21:45:00', '2017-04-05 23:59:59'] )
        tplot( 'erg_xep_l2_FEDU_SSD_pa', display=display, save_png='erg_xep_pa.png' )
        self.assertTrue('erg_xep_l2_FEDU_SSD_pa' in vars)
        self.assertTrue(data_exists('erg_xep_l2_FEDU_SSD_pa'))

    def test_xep_fac_energy(self):
        del_data('*')
        # Load XEP-e Lv.2 3-D flux data
        timespan('2017-04-05 21:45:00', 2.25, keyword='hours')
        pyspedas.projects.erg.xep( trange=[ '2017-04-05 21:45:00', '2017-04-05 23:59:59'], datatype='2dflux' )
        vars = pyspedas.projects.erg.mgf(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary B-field data
        vars = pyspedas.projects.erg.orb(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary orbit data
        mag_vn = 'erg_mgf_l2_mag_8sec_dsi'
        pos_vn = 'erg_orb_l2_pos_gse'
        # Calculate and plot energy spectrum
        vars = erg_xep_part_products( 'erg_xep_l2_FEDU_SSD', mag_name=mag_vn, pos_name=pos_vn, outputs='fac_energy', trange=[ '2017-04-05 21:45:00', '2017-04-05 23:59:59'] )
        tplot(vars, display=display, save_png='erg_xep_fac_energy.png' )
        self.assertTrue('erg_xep_l2_FEDU_SSD_energy_mag' in vars)
        self.assertTrue(data_exists('erg_xep_l2_FEDU_SSD_energy_mag'))

    def test_xep_energy(self):
        del_data('*')
        # Load XEP-e Lv.2 3-D flux data
        timespan('2017-04-05 21:45:00', 2.25, keyword='hours')
        pyspedas.projects.erg.xep( trange=[ '2017-04-05 21:45:00', '2017-04-05 23:59:59'], datatype='2dflux' )
        # Calculate and plot energy spectrum
        vars = erg_xep_part_products( 'erg_xep_l2_FEDU_SSD', outputs='energy', trange=[ '2017-04-05 21:45:00', '2017-04-05 23:59:59'] )
        tplot( 'erg_xep_l2_FEDU_SSD_energy', display=display, save_png='erg_xep_en_spec.png' )
        self.assertTrue('erg_xep_l2_FEDU_SSD_energy' in vars)
        self.assertTrue(data_exists('erg_xep_l2_FEDU_SSD_energy'))

    def test_xep_energy_limit_phi(self):
        del_data('*')
        # Load XEP-e Lv.2 3-D flux data
        timespan('2017-04-05 21:45:00', 2.25, keyword='hours')
        pyspedas.projects.erg.xep( trange=[ '2017-04-05 21:45:00', '2017-04-05 23:59:59'], datatype='2dflux' )
        # Calculate and plot energy spectrum
        vars = erg_xep_part_products( 'erg_xep_l2_FEDU_SSD', outputs='energy', trange=[ '2017-04-05 21:45:00', '2017-04-05 23:59:59'], phi_in=[0., 180.] )
        tplot( 'erg_xep_l2_FEDU_SSD_energy', display=display, save_png='erg_xep_en_spec_limit_phi.png' )
        self.assertTrue('erg_xep_l2_FEDU_SSD_energy' in vars)
        self.assertTrue(data_exists('erg_xep_l2_FEDU_SSD_energy'))

    # The pa output comes out all zeroes for this test.  Maybe correct if there's only one theta bin?
    def test_xep_pa_limit_energy(self):
        del_data('*')
        # Load XEP-e Lv.2 3-D flux data
        timespan('2017-04-05 21:45:00', 2.25, keyword='hours')
        pyspedas.projects.erg.xep( trange=[ '2017-04-05 21:45:00', '2017-04-05 23:59:59'], datatype='2dflux' )
        vars = pyspedas.projects.erg.mgf(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary B-field data
        vars = pyspedas.projects.erg.orb(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary orbit data
        mag_vn = 'erg_mgf_l2_mag_8sec_dsi'
        pos_vn = 'erg_orb_l2_pos_gse'
        # Calculate the pitch angle distribution
        vars = erg_xep_part_products('erg_xep_l2_FEDU_SSD', outputs='pa', energy=[0., 1e06], fac_type='xdsi',
                                     mag_name=mag_vn, pos_name=pos_vn,
                                     trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])
        tplot( 'erg_xep_l2_FEDU_SSD_pa', display=display, save_png='erg_xep_pad_limit_energy.png' )
        self.assertTrue('erg_xep_l2_FEDU_SSD_pa' in vars)
        self.assertTrue(data_exists('erg_xep_l2_FEDU_SSD_pa'))

    def test_xep_en_pad_limit(self):
        del_data('*')
        # Load XEP-e Lv.2 3-D flux data
        timespan('2017-04-05 21:45:00', 2.25, keyword='hours')
        pyspedas.projects.erg.xep( trange=[ '2017-04-05 21:45:00', '2017-04-05 23:59:59'], datatype='2dflux' )
        vars = pyspedas.projects.erg.mgf(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary B-field data
        vars = pyspedas.projects.erg.orb(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary orbit data
        mag_vn = 'erg_mgf_l2_mag_8sec_dsi'
        pos_vn = 'erg_orb_l2_pos_gse'
        # Calculate energy-time spectra of electron flux for limited pitch-angle (PA) ranges
        ## Here we calculate energy-time spectra for PA = 0-10 deg and PA = 80-100 deg.
        vars1 = erg_xep_part_products('erg_xep_l2_FEDU_SSD', outputs='fac_energy', pitch=[80., 100.],
                                     fac_type='xdsi', mag_name=mag_vn, pos_name=pos_vn,
                                     trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'], suffix='_pa80-100')
        vars2 = erg_xep_part_products('erg_xep_l2_FEDU_SSD', outputs='fac_energy', pitch=[0., 10.], fac_type='xdsi',
                                     mag_name=mag_vn, pos_name=pos_vn,
                                     trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'], suffix='_pa0-10')
        ## Decorate the obtained spectrum variables
        pytplot.options('erg_xep_l2_FEDU_SSD_energy_mag_pa80-100', 'ytitle', 'XEP-e flux\nPA: 80-100\n\n[eV]')
        pytplot.options('erg_xep_l2_FEDU_SSD_energy_mag_pa0-10', 'ytitle', 'XEP-e flux\nPA: 0-10\n\n[eV]')
        tplot(['erg_xep_l2_FEDU_SSD_energy_mag_pa80-100', 'erg_xep_l2_FEDU_SSD_energy_mag_pa0-10'], display=display, save_png='erg_xep_en_pa_limit.png')
        self.assertTrue('erg_xep_l2_FEDU_SSD_energy_mag_pa80-100' in vars1)
        self.assertTrue(data_exists('erg_xep_l2_FEDU_SSD_energy_mag_pa80-100'))
        self.assertTrue('erg_xep_l2_FEDU_SSD_energy_mag_pa0-10' in vars2)
        self.assertTrue(data_exists('erg_xep_l2_FEDU_SSD_energy_mag_pa0-10'))

if __name__ == '__main__':
    unittest.main()