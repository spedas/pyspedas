
import os
import unittest
from pytplot import data_exists, del_data, timespan,tplot
from pyspedas.erg import erg_lep_part_products, erg_hep_part_products, erg_mep_part_products

import pyspedas
import pytplot

display=False

class LoadTestCases(unittest.TestCase):

    @unittest.skip
    def test_lepe_en_pad_limit(self):
        del_data('*')
        # Load LEP-e Lv.2 3-D flux data
        timespan('2017-04-05 21:45:00', 2.25, keyword='hours')
        pyspedas.erg.lepe( trange=[ '2017-04-05 21:45:00', '2017-04-05 23:59:59'], datatype='3dflux')
        pytplot.tplot_names()
        vars = pyspedas.erg.mgf(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary B-field data
        vars = pyspedas.erg.orb(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary orbit data
        mag_vn = 'erg_mgf_l2_mag_8sec_dsi'
        pos_vn = 'erg_orb_l2_pos_gse'
        # Calculate energy-time spectra of electron flux for limited pitch-angle (PA) ranges
        ## Here we calculate energy-time spectra for PA = 0-10 deg and PA = 80-100 deg.
        vars = erg_lep_part_products('erg_lepe_l2_3dflux_FEDU', outputs='fac_energy', pitch=[80., 100.],
                                     fac_type='xdsi', mag_name=mag_vn, pos_name=pos_vn,
                                     trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'], suffix='_pa80-100')
        vars = erg_lep_part_products('erg_lepe_l2_3dflux_FEDU', outputs='fac_energy', pitch=[0., 10.], fac_type='xdsi',
                                     mag_name=mag_vn, pos_name=pos_vn,
                                     trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'], suffix='_pa0-10')

        ## Decorate the obtained spectrum variables
        pytplot.options('erg_lepe_l2_3dflux_FEDU_energy_mag_pa80-100', 'ytitle', 'LEP-e flux\nPA: 80-100\n\n[eV]')
        pytplot.options('erg_lepe_l2_3dflux_FEDU_energy_mag_pa0-10', 'ytitle', 'LEP-e flux\nPA: 0-10\n\n[eV]')
        tplot(['erg_lepe_l2_3dflux_FEDU_energy_mag_pa80-100', 'erg_lepe_l2_3dflux_FEDU_energy_mag_pa0-10'], display=display, save_png='erg_lepe_en_pa_limit.png')

    def test_lepi_en_pad_limit(self):
        del_data('*')
        # Load LEP-i Lv.2 3-D flux data
        timespan('2017-04-05 21:45:00', 2.25, keyword='hours')
        pyspedas.erg.lepi( trange=[ '2017-04-05 21:45:00', '2017-04-05 23:59:59'], datatype='3dflux')
        pytplot.tplot_names()
        vars = pyspedas.erg.mgf(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary B-field data
        vars = pyspedas.erg.orb(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary orbit data
        mag_vn = 'erg_mgf_l2_mag_8sec_dsi'
        pos_vn = 'erg_orb_l2_pos_gse'
        # Calculate energy-time spectra of electron flux for limited pitch-angle (PA) ranges
        ## Here we calculate energy-time spectra for PA = 0-10 deg and PA = 80-100 deg.
        vars = erg_lep_part_products('erg_lepi_l2_3dflux_FPDU', outputs='fac_energy', pitch=[80., 100.],
                                     fac_type='xdsi', mag_name=mag_vn, pos_name=pos_vn,
                                     trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'], suffix='_pa80-100')
        vars = erg_lep_part_products('erg_lepi_l2_3dflux_FPDU', outputs='fac_energy', pitch=[0., 10.], fac_type='xdsi',
                                     mag_name=mag_vn, pos_name=pos_vn,
                                     trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'], suffix='_pa0-10')

        ## Decorate the obtained spectrum variables
        pytplot.options('erg_lepi_l2_3dflux_FPDU_energy_mag_pa80-100', 'ytitle', 'LEP-e flux\nPA: 80-100\n\n[eV]')
        pytplot.options('erg_lepi_l2_3dflux_FPDU_energy_mag_pa0-10', 'ytitle', 'LEP-e flux\nPA: 0-10\n\n[eV]')
        tplot(['erg_lepi_l2_3dflux_FPDU_energy_mag_pa80-100', 'erg_lepi_l2_3dflux_FPDU_energy_mag_pa0-10'], display=display, save_png='erg_lepi_en_pa_limit.png')

    @unittest.skip
    def test_hep_en_pad_limit(self):
        del_data('*')
        # Load LEP-e Lv.2 3-D flux data
        timespan('2017-04-05 21:45:00', 2.25, keyword='hours')

        pyspedas.erg.hep( trange=[ '2017-04-05 21:45:00', '2017-04-05 23:59:59'], datatype='3dflux')
        pytplot.tplot_names()
        vars = pyspedas.erg.mgf(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary B-field data
        vars = pyspedas.erg.orb(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary orbit data
        mag_vn = 'erg_mgf_l2_mag_8sec_dsi'
        pos_vn = 'erg_orb_l2_pos_gse'
        # Calculate energy-time spectra of electron flux for limited pitch-angle (PA) ranges
        ## Here we calculate energy-time spectra for PA = 0-10 deg and PA = 80-100 deg.
        vars = erg_hep_part_products('erg_hep_l2_FEDU_L', outputs='fac_energy', pitch=[80., 100.],
                                     fac_type='xdsi', mag_name=mag_vn, pos_name=pos_vn,
                                     trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'], suffix='_pa80-100')
        vars = erg_hep_part_products('erg_hep_l2_FEDU_L', outputs='fac_energy', pitch=[0., 10.], fac_type='xdsi',
                                     mag_name=mag_vn, pos_name=pos_vn,
                                     trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'], suffix='_pa0-10')

        ## Decorate the obtained spectrum variables
        pytplot.options('erg_hep_l2_FEDU_Lenergy_mag_pa80-100', 'ytitle', 'HEP-e flux\nPA: 80-100\n\n[eV]')
        pytplot.options('erg_hep_l2_FEDU_Lenergy_mag_pa0-10', 'ytitle', 'HEP-e flux\nPA: 0-10\n\n[eV]')
        tplot(['erg_hep_l2_FEDU_Lenergy_mag_pa80-100', 'erg_hep_l2_FEDU_L_energy_mag_pa0-10'], display=display, save_png='erg_lepe_en_pa_limit.png')

    def test_mepe_theta(self):
        del_data('*')
        # Load MEP-e Lv.2 3-D flux data
        timespan('2017-04-05 21:45:00', 2.25, keyword='hours')
        pyspedas.erg.mepe( trange=[ '2017-04-05 21:45:00', '2017-04-05 23:59:59'], datatype='3dflux' )
        # Calculate and plot energy spectrum
        vars = erg_mep_part_products( 'erg_mepe_l2_3dflux_FEDU', outputs='theta', trange=[ '2017-04-05 21:45:00', '2017-04-05 23:59:59'] )
        tplot( 'erg_mepe_l2_3dflux_FEDU_theta', display=display, save_png='erg_mepe_theta.png' )

    def test_mepe_phi(self):
        del_data('*')
        # Load MEP-e Lv.2 3-D flux data
        timespan('2017-04-05 21:45:00', 2.25, keyword='hours')
        pyspedas.erg.mepe( trange=[ '2017-04-05 21:45:00', '2017-04-05 23:59:59'], datatype='3dflux' )
        # Calculate and plot energy spectrum
        vars = erg_mep_part_products( 'erg_mepe_l2_3dflux_FEDU', outputs='phi', trange=[ '2017-04-05 21:45:00', '2017-04-05 23:59:59'] )
        tplot( 'erg_mepe_l2_3dflux_FEDU_phi', display=display, save_png='erg_mepe_phi.png' )


    def test_mepe_pa(self):
        del_data('*')
        # Load MEP-e Lv.2 3-D flux data
        timespan('2017-04-05 21:45:00', 2.25, keyword='hours')
        pyspedas.erg.mepe( trange=[ '2017-04-05 21:45:00', '2017-04-05 23:59:59'], datatype='3dflux' )
        vars = pyspedas.erg.mgf(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary B-field data
        vars = pyspedas.erg.orb(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary orbit data
        mag_vn = 'erg_mgf_l2_mag_8sec_dsi'
        pos_vn = 'erg_orb_l2_pos_gse'

        # Calculate and plot energy spectrum
        vars = erg_mep_part_products( 'erg_mepe_l2_3dflux_FEDU', mag_name=mag_vn, pos_name=pos_vn, outputs='pa', trange=[ '2017-04-05 21:45:00', '2017-04-05 23:59:59'] )
        tplot( 'erg_mepe_l2_3dflux_FEDU_pa', display=display, save_png='erg_mepe_pa.png' )

    def test_mepe_moments(self):
        del_data('*')
        # Load MEP-e Lv.2 3-D flux data
        timespan('2017-04-05 21:45:00', 2.25, keyword='hours')
        pyspedas.erg.mepe( trange=[ '2017-04-05 21:45:00', '2017-04-05 23:59:59'], datatype='3dflux' )
        vars = pyspedas.erg.mgf(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary B-field data
        vars = pyspedas.erg.orb(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary orbit data
        mag_vn = 'erg_mgf_l2_mag_8sec_dsi'
        pos_vn = 'erg_orb_l2_pos_gse'

        # Calculate and plot energy spectrum
        vars = erg_mep_part_products( 'erg_mepe_l2_3dflux_FEDU', mag_name=mag_vn, pos_name=pos_vn, outputs='moments', trange=[ '2017-04-05 21:45:00', '2017-04-05 23:59:59'] )
        print(vars)
        tplot(vars, display=display, save_png='erg_mepe_moments.png' )

    def test_mepe_fac_moments(self):
        del_data('*')
        # Load MEP-e Lv.2 3-D flux data
        timespan('2017-04-05 21:45:00', 2.25, keyword='hours')
        pyspedas.erg.mepe( trange=[ '2017-04-05 21:45:00', '2017-04-05 23:59:59'], datatype='3dflux' )
        vars = pyspedas.erg.mgf(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary B-field data
        vars = pyspedas.erg.orb(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary orbit data
        mag_vn = 'erg_mgf_l2_mag_8sec_dsi'
        pos_vn = 'erg_orb_l2_pos_gse'

        # Calculate and plot energy spectrum
        vars = erg_mep_part_products( 'erg_mepe_l2_3dflux_FEDU', mag_name=mag_vn, pos_name=pos_vn, outputs='fac_moments', trange=[ '2017-04-05 21:45:00', '2017-04-05 23:59:59'] )
        print(vars)
        tplot(vars, display=display, save_png='erg_mepe_fac_moments.png' )

    def test_mepe_fac_energy(self):
        del_data('*')
        # Load MEP-e Lv.2 3-D flux data
        timespan('2017-04-05 21:45:00', 2.25, keyword='hours')
        pyspedas.erg.mepe( trange=[ '2017-04-05 21:45:00', '2017-04-05 23:59:59'], datatype='3dflux' )
        vars = pyspedas.erg.mgf(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary B-field data
        vars = pyspedas.erg.orb(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary orbit data
        mag_vn = 'erg_mgf_l2_mag_8sec_dsi'
        pos_vn = 'erg_orb_l2_pos_gse'

        # Calculate and plot energy spectrum
        vars = erg_mep_part_products( 'erg_mepe_l2_3dflux_FEDU', mag_name=mag_vn, pos_name=pos_vn, outputs='fac_energy', trange=[ '2017-04-05 21:45:00', '2017-04-05 23:59:59'] )
        print(vars)
        tplot(vars, display=display, save_png='erg_mepe_fac_energy.png' )

    def test_mepe_en_spec(self):
        del_data('*')
        # Load MEP-e Lv.2 3-D flux data
        timespan('2017-04-05 21:45:00', 2.25, keyword='hours')
        pyspedas.erg.mepe( trange=[ '2017-04-05 21:45:00', '2017-04-05 23:59:59'], datatype='3dflux' )
        # Calculate and plot energy spectrum
        vars = erg_mep_part_products( 'erg_mepe_l2_3dflux_FEDU', outputs='energy', trange=[ '2017-04-05 21:45:00', '2017-04-05 23:59:59'] )
        tplot( 'erg_mepe_l2_3dflux_FEDU_energy', display=display, save_png='erg_mepe_en_spec.png' )

    def test_mepe_pad(self):
        del_data('*')
        # Load MEP-e Lv.2 3-D flux data
        timespan('2017-04-05 21:45:00', 2.25, keyword='hours')
        pyspedas.erg.mepe( trange=[ '2017-04-05 21:45:00', '2017-04-05 23:59:59'], datatype='3dflux' )
        vars = pyspedas.erg.mgf(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary B-field data
        vars = pyspedas.erg.orb(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary orbit data
        mag_vn = 'erg_mgf_l2_mag_8sec_dsi'
        pos_vn = 'erg_orb_l2_pos_gse'
        # Calculate the pitch angle distribution
        vars = erg_mep_part_products('erg_mepe_l2_3dflux_FEDU', outputs='pa', energy=[15000., 22000.], fac_type='xdsi',
                                     mag_name=mag_vn, pos_name=pos_vn,
                                     trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])

        tplot( 'erg_mepe_l2_3dflux_FEDU_pa', display=display, save_png='erg_mepe_pad.png' )

    def test_mepe_en_pad_limit(self):
        del_data('*')
        # Load MEP-e Lv.2 3-D flux data
        timespan('2017-04-05 21:45:00', 2.25, keyword='hours')
        pyspedas.erg.mepe( trange=[ '2017-04-05 21:45:00', '2017-04-05 23:59:59'], datatype='3dflux' )
        vars = pyspedas.erg.mgf(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary B-field data
        vars = pyspedas.erg.orb(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary orbit data
        mag_vn = 'erg_mgf_l2_mag_8sec_dsi'
        pos_vn = 'erg_orb_l2_pos_gse'
        # Calculate energy-time spectra of electron flux for limited pitch-angle (PA) ranges
        ## Here we calculate energy-time spectra for PA = 0-10 deg and PA = 80-100 deg.
        vars = erg_mep_part_products('erg_mepe_l2_3dflux_FEDU', outputs='fac_energy', pitch=[80., 100.],
                                     fac_type='xdsi', mag_name=mag_vn, pos_name=pos_vn,
                                     trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'], suffix='_pa80-100')
        vars = erg_mep_part_products('erg_mepe_l2_3dflux_FEDU', outputs='fac_energy', pitch=[0., 10.], fac_type='xdsi',
                                     mag_name=mag_vn, pos_name=pos_vn,
                                     trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'], suffix='_pa0-10')

        ## Decorate the obtained spectrum variables
        pytplot.options('erg_mepe_l2_3dflux_FEDU_energy_mag_pa80-100', 'ytitle', 'MEP-e flux\nPA: 80-100\n\n[eV]')
        pytplot.options('erg_mepe_l2_3dflux_FEDU_energy_mag_pa0-10', 'ytitle', 'MEP-e flux\nPA: 0-10\n\n[eV]')
        tplot(['erg_mepe_l2_3dflux_FEDU_energy_mag_pa80-100', 'erg_mepe_l2_3dflux_FEDU_energy_mag_pa0-10'], display=display, save_png='erg_mep_en_pa_limit.png')

    def test_mepi_en_spec(self):
        del_data('*')
        # Load MEP-e Lv.2 3-D flux data
        timespan('2017-04-05 21:45:00', 1.0, keyword='hours')
        mepi_vars = pyspedas.erg.mepi_nml( trange=[ '2017-04-05 21:45:00', '2017-04-05 22:26:00'], datatype='3dflux' )
        print(mepi_vars)
        # Calculate and plot energy spectrum
        vars = erg_mep_part_products( 'erg_mepi_l2_3dflux_FPDU', outputs='energy', trange=[ '2017-04-05 21:45:00', '2017-04-05 23:59:59'] )
        tplot( 'erg_mepi_l2_3dflux_FPDU_energy', display=display, save_png='erg_mepi_en_spec.png' )

    def test_mepi_pad(self):
        del_data('*')
        # Load MEP-e Lv.2 3-D flux data
        timespan('2017-04-05 21:45:00', 1.0, keyword='hours')
        pyspedas.erg.mepi_nml( trange=[ '2017-04-05 21:45:00', '2017-04-05 23:59:59'], datatype='3dflux' )
        vars = pyspedas.erg.mgf(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary B-field data
        vars = pyspedas.erg.orb(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary orbit data
        mag_vn = 'erg_mgf_l2_mag_8sec_dsi'
        pos_vn = 'erg_orb_l2_pos_gse'
        # Calculate the pitch angle distribution
        vars = erg_mep_part_products('erg_mepi_l2_3dflux_FPDU', outputs='pa', energy=[15000., 22000.], fac_type='xdsi',
                                     mag_name=mag_vn, pos_name=pos_vn,
                                     trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])

        tplot( 'erg_mepi_l2_3dflux_FPDU_pa', display=display, save_png='erg_mepi_pad.png' )

    def test_mepi_en_pad_limit(self):
        del_data('*')
        # Load MEP-e Lv.2 3-D flux data
        timespan('2017-04-05 21:45:00', 1.0, keyword='hours')
        pyspedas.erg.mepi_nml( trange=[ '2017-04-05 21:45:00', '2017-04-05 23:59:59'], datatype='3dflux' )
        vars = pyspedas.erg.mgf(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary B-field data
        vars = pyspedas.erg.orb(trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'])  # Load necessary orbit data
        mag_vn = 'erg_mgf_l2_mag_8sec_dsi'
        pos_vn = 'erg_orb_l2_pos_gse'
        # Calculate energy-time spectra of electron flux for limited pitch-angle (PA) ranges
        ## Here we calculate energy-time spectra for PA = 0-10 deg and PA = 80-100 deg.
        vars = erg_mep_part_products('erg_mepi_l2_3dflux_FPDU', outputs='fac_energy', pitch=[80., 100.],
                                     fac_type='xdsi', mag_name=mag_vn, pos_name=pos_vn,
                                     trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'], suffix='_pa80-100')
        vars = erg_mep_part_products('erg_mepi_l2_3dflux_FPDU', outputs='fac_energy', pitch=[0., 10.], fac_type='xdsi',
                                     mag_name=mag_vn, pos_name=pos_vn,
                                     trange=['2017-04-05 21:45:00', '2017-04-05 23:59:59'], suffix='_pa0-10')

        ## Decorate the obtained spectrum variables
        pytplot.options('erg_mepi_l2_3dflux_FPDU_energy_mag_pa80-100', 'ytitle', 'MEP-i flux\nPA: 80-100\n\n[eV]')
        pytplot.options('erg_mepi_l2_3dflux_FPDU_energy_mag_pa0-10', 'ytitle', 'MEP-i flux\nPA: 0-10\n\n[eV]')
        tplot(['erg_mepi_l2_3dflux_FPDU_energy_mag_pa80-100', 'erg_mepi_l2_3dflux_FPDU_energy_mag_pa0-10'], display=display, save_png='erg_mepi_en_pa_limit.png')

if __name__ == '__main__':
    unittest.main()