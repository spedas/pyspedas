"""Tests of epd l2 spectogram."""
import pyspedas.elfin
import pytplot.get_data
from pytplot.importers.tplot_restore import tplot_restore
import unittest
from numpy.testing import assert_allclose, assert_array_almost_equal, assert_array_equal, assert_array_almost_equal_nulp
import numpy as np
from pyspedas.elfin.epd.calibration_l2 import spec_pa_sort
import logging

class TestELFStateValidation(unittest.TestCase):
    """Tests of the data been identical to SPEDAS (IDL)."""

    @classmethod
    def setUpClass(cls):
        """
        IDL Data has to be downloaded to perform these tests
        The IDL script that creates data file:
        https://github.com/spedas/pyspedas-validation/blob/cal_fit/src/themis/validation_files/thm_load_fit_validation_files.pro
        """
        # TODO:
        # 1. upload .pro file to repo and change the directory here
        # 2. upload .tplot file to server and change the directory here
        # 3. add download file from server

        # Testing time range
        cls.t = ['2022-08-03/08:30:00','2022-08-03/09:00:00']
        #cls.probe = 'a'
        #cls.t = ['2021-04-26/00:34:18','2021-04-26/00:40:18']
        #cls.probe = 'b'
        #cls.t = ['2022-08-28/15:54','2022-08-28/16:15']
        cls.probe = 'a'
        # Load state validation variables from the test file
        filename = f"elfin_data/validation_el{cls.probe}_state_{cls.t[0][0:4]+cls.t[0][5:7]+cls.t[0][8:10]}.tplot"
        tplot_restore(filename)
        cls.elf_pos_gei = pytplot.get_data(f"el{cls.probe}_pos_gei")
        cls.elf_vel_gei = pytplot.get_data(f"el{cls.probe}_vel_gei")
        cls.elf_att_gei = pytplot.get_data(f"el{cls.probe}_att_gei")
        cls.elf_att_solution = pytplot.get_data(f"el{cls.probe}_att_solution_date")
        cls.elf_att_flag = pytplot.get_data(f"el{cls.probe}_att_flag")
        cls.elf_att_spinper = pytplot.get_data(f"el{cls.probe}_att_spinper")
        cls.elf_spin_orbnorm = pytplot.get_data(f"el{cls.probe}_spin_orbnorm_angle")
        cls.elf_spin_sun = pytplot.get_data(f"el{cls.probe}_spin_sun_angle")

        # load epd l2 hs nflux spectrogram 
        filename = f"elfin_data/validation_el{cls.probe}_epd_l2_hs_nflux_{cls.t[0][0:4]+cls.t[0][5:7]+cls.t[0][8:10]}.tplot"
        tplot_restore(filename)
        cls.elf_pef_hs_nflux_ch0 = pytplot.get_data(f"el{cls.probe}_pef_hs_nflux_ch0")
        cls.elf_pef_hs_nflux_ch1 = pytplot.get_data(f"el{cls.probe}_pef_hs_nflux_ch1")
        cls.elf_pef_hs_nflux_ch2 = pytplot.get_data(f"el{cls.probe}_pef_hs_nflux_ch2")
        cls.elf_pef_hs_nflux_ch3 = pytplot.get_data(f"el{cls.probe}_pef_hs_nflux_ch3")
        cls.elf_pef_hs_nflux_omni = pytplot.get_data(f"el{cls.probe}_pef_hs_nflux_omni")
        cls.elf_pef_hs_nflux_para = pytplot.get_data(f"el{cls.probe}_pef_hs_nflux_para")
        cls.elf_pef_hs_nflux_anti = pytplot.get_data(f"el{cls.probe}_pef_hs_nflux_anti")
        cls.elf_pef_hs_nflux_perp = pytplot.get_data(f"el{cls.probe}_pef_hs_nflux_perp")
        cls.elf_pef_hs_antiLCdeg = pytplot.get_data(f"el{cls.probe}_pef_hs_antiLCdeg")
        cls.elf_pef_hs_LCdeg = pytplot.get_data(f"el{cls.probe}_pef_hs_LCdeg")
        cls.elf_pef_Et_nflux = pytplot.get_data(f"el{cls.probe}_pef_Et_nflux")
        cls.elf_pef_pa = pytplot.get_data(f"el{cls.probe}_pef_pa")
        cls.elf_pef_hs_Epat_nflux_ch0 = pytplot.get_data(f"el{cls.probe}_pef_hs_Epat_nflux_ch0") # Epat is 3d, can't save it with idl
        cls.elf_pef_hs_Epat_nflux_ch1 = pytplot.get_data(f"el{cls.probe}_pef_hs_Epat_nflux_ch1")

        # load epd l2 hs eflux spectrogram
        filename = f"elfin_data/validation_el{cls.probe}_epd_l2_hs_eflux_{cls.t[0][0:4]+cls.t[0][5:7]+cls.t[0][8:10]}.tplot"
        tplot_restore(filename)
        cls.elf_pef_hs_eflux_ch0 = pytplot.get_data(f"el{cls.probe}_pef_hs_eflux_ch0")
        cls.elf_pef_hs_eflux_ch1 = pytplot.get_data(f"el{cls.probe}_pef_hs_eflux_ch1")
        cls.elf_pef_hs_eflux_ch2 = pytplot.get_data(f"el{cls.probe}_pef_hs_eflux_ch2")
        cls.elf_pef_hs_eflux_ch3 = pytplot.get_data(f"el{cls.probe}_pef_hs_eflux_ch3")
        cls.elf_pef_hs_eflux_omni = pytplot.get_data(f"el{cls.probe}_pef_hs_eflux_omni")
        cls.elf_pef_hs_eflux_para = pytplot.get_data(f"el{cls.probe}_pef_hs_eflux_para")
        cls.elf_pef_hs_eflux_anti = pytplot.get_data(f"el{cls.probe}_pef_hs_eflux_anti")
        cls.elf_pef_hs_eflux_perp = pytplot.get_data(f"el{cls.probe}_pef_hs_eflux_perp")
        cls.elf_pef_Et_eflux = pytplot.get_data(f"el{cls.probe}_pef_Et_eflux")
        cls.elf_pef_hs_Epat_eflux_ch0 = pytplot.get_data(f"el{cls.probe}_pef_hs_Epat_eflux_ch0") # Epat is 3d, can't save it with idl
        cls.elf_pef_hs_Epat_eflux_ch1 = pytplot.get_data(f"el{cls.probe}_pef_hs_Epat_eflux_ch1")
       
        # load epd l2 fs nflux spectrogram 
        filename = f"elfin_data/validation_el{cls.probe}_epd_l2_fs_nflux_{cls.t[0][0:4]+cls.t[0][5:7]+cls.t[0][8:10]}.tplot"
        tplot_restore(filename)
        cls.elf_pef_fs_nflux_ch0 = pytplot.get_data(f"el{cls.probe}_pef_fs_nflux_ch0")
        cls.elf_pef_fs_nflux_ch1 = pytplot.get_data(f"el{cls.probe}_pef_fs_nflux_ch1")
        cls.elf_pef_fs_nflux_ch2 = pytplot.get_data(f"el{cls.probe}_pef_fs_nflux_ch2")
        cls.elf_pef_fs_nflux_ch3 = pytplot.get_data(f"el{cls.probe}_pef_fs_nflux_ch3")
        cls.elf_pef_fs_nflux_omni = pytplot.get_data(f"el{cls.probe}_pef_fs_nflux_omni")
        cls.elf_pef_fs_nflux_para = pytplot.get_data(f"el{cls.probe}_pef_fs_nflux_para")
        cls.elf_pef_fs_nflux_anti = pytplot.get_data(f"el{cls.probe}_pef_fs_nflux_anti")
        cls.elf_pef_fs_nflux_perp = pytplot.get_data(f"el{cls.probe}_pef_fs_nflux_perp")
        cls.elf_pef_fs_antiLCdeg = pytplot.get_data(f"el{cls.probe}_pef_fs_antiLCdeg")
        cls.elf_pef_fs_LCdeg = pytplot.get_data(f"el{cls.probe}_pef_fs_LCdeg")
        cls.elf_pef_fs_Epat_nflux_ch0 = pytplot.get_data(f"el{cls.probe}_pef_fs_Epat_nflux_ch0") # Epat is 3d, can't save it with idl
        cls.elf_pef_fs_Epat_nflux_ch1 = pytplot.get_data(f"el{cls.probe}_pef_fs_Epat_nflux_ch1")

        # load epd l2 fs eflux spectrogram 
        filename = f"elfin_data/validation_el{cls.probe}_epd_l2_fs_eflux_{cls.t[0][0:4]+cls.t[0][5:7]+cls.t[0][8:10]}.tplot"
        tplot_restore(filename)
        cls.elf_pef_fs_eflux_ch0 = pytplot.get_data(f"el{cls.probe}_pef_fs_eflux_ch0")
        cls.elf_pef_fs_eflux_ch1 = pytplot.get_data(f"el{cls.probe}_pef_fs_eflux_ch1")
        cls.elf_pef_fs_eflux_omni = pytplot.get_data(f"el{cls.probe}_pef_fs_eflux_omni")
        cls.elf_pef_fs_eflux_para = pytplot.get_data(f"el{cls.probe}_pef_fs_eflux_para")
        cls.elf_pef_fs_eflux_anti = pytplot.get_data(f"el{cls.probe}_pef_fs_eflux_anti")
        cls.elf_pef_fs_eflux_perp = pytplot.get_data(f"el{cls.probe}_pef_fs_eflux_perp")
        cls.elf_pef_fs_Epat_eflux_ch0 = pytplot.get_data(f"el{cls.probe}_pef_fs_Epat_eflux_ch0") # Epat is 3d, can't save it with idl
        cls.elf_pef_fs_Epat_eflux_ch1 = pytplot.get_data(f"el{cls.probe}_pef_fs_Epat_eflux_ch1")


    def setUp(self):
        """ We need to clean tplot variables before each run"""
        pytplot.del_data('*')

   
    def test_state(self):
        """Validate state data."""
        pyspedas.elfin.state(trange=self.t, probe=self.probe)
        elf_pos_gei = pytplot.get_data(f"el{self.probe}_pos_gei")
        elf_vel_gei = pytplot.get_data(f"el{self.probe}_vel_gei")
        elf_att_gei = pytplot.get_data(f"el{self.probe}_att_gei")
        elf_att_solution = pytplot.get_data(f"el{self.probe}_att_solution_date")
        elf_att_flag = pytplot.get_data(f"el{self.probe}_att_flag")
        elf_att_spinper = pytplot.get_data(f"el{self.probe}_att_spinper")
        elf_spin_orbnorm = pytplot.get_data(f"el{self.probe}_spin_orbnorm_angle")
        elf_spin_sun = pytplot.get_data(f"el{self.probe}_spin_sun_angle")
   
        assert_array_almost_equal(elf_pos_gei.y, self.elf_pos_gei.y, decimal=4)
        assert_array_almost_equal(elf_vel_gei.y, self.elf_vel_gei.y, decimal=4)
        assert_array_almost_equal(elf_att_gei.y, self.elf_att_gei.y, decimal=2)
        assert_allclose(elf_att_solution.times, self.elf_att_solution.y, rtol=1e-3)
        assert_array_equal(elf_att_flag.y, self.elf_att_flag.y)
        assert_allclose(elf_att_spinper.y, self.elf_att_spinper.y, rtol=1e-2)
        assert_allclose(elf_spin_orbnorm.y, self.elf_spin_orbnorm.y, rtol=1e-2)
        assert_allclose(elf_spin_sun.y, self.elf_spin_sun.y, rtol=1e-2)

        logging.info("STATE DATA TEST FINISHED.")


    def test_epd_l2_hs_nflux(self):
        """Validate epd l2 halfspin nflux spectogram"""
        pyspedas.elfin.epd(trange=self.t, probe=self.probe, level='l2',no_update=True)
        elf_pef_hs_nflux_ch0 = pytplot.get_data(f"el{self.probe}_pef_hs_nflux_ch0")
        elf_pef_hs_nflux_ch1 = pytplot.get_data(f"el{self.probe}_pef_hs_nflux_ch1")
        elf_pef_hs_nflux_ch2 = pytplot.get_data(f"el{self.probe}_pef_hs_nflux_ch2")
        elf_pef_hs_nflux_ch3 = pytplot.get_data(f"el{self.probe}_pef_hs_nflux_ch3")
        elf_pef_hs_nflux_perp = pytplot.get_data(f"el{self.probe}_pef_hs_nflux_perp")
        elf_pef_hs_nflux_anti = pytplot.get_data(f"el{self.probe}_pef_hs_nflux_anti")
        elf_pef_hs_nflux_para = pytplot.get_data(f"el{self.probe}_pef_hs_nflux_para")
        elf_pef_hs_nflux_omni = pytplot.get_data(f"el{self.probe}_pef_hs_nflux_omni")
        elf_pef_hs_antiLCdeg = pytplot.get_data(f"el{self.probe}_pef_hs_antiLCdeg")
        elf_pef_hs_LCdeg = pytplot.get_data(f"el{self.probe}_pef_hs_LCdeg")
        elf_pef_hs_Epat_nflux = pytplot.get_data(f"el{self.probe}_pef_hs_Epat_nflux")
        elf_pef_Et_nflux = pytplot.get_data(f"el{self.probe}_pef_Et_nflux")
        elf_pef_pa = pytplot.get_data(f"el{self.probe}_pef_pa")

        assert_array_almost_equal(elf_pef_hs_Epat_nflux.v1, self.elf_pef_hs_Epat_nflux_ch1.v, decimal=1)      
        assert_array_almost_equal(elf_pef_hs_Epat_nflux.y[:,:,0], self.elf_pef_hs_Epat_nflux_ch0.y, decimal=1)
        assert_array_almost_equal(elf_pef_hs_Epat_nflux.y[:,:,1], self.elf_pef_hs_Epat_nflux_ch1.y, decimal=1)
        assert_array_almost_equal(elf_pef_hs_LCdeg.y, self.elf_pef_hs_LCdeg.y, decimal=1)
        assert_array_almost_equal(elf_pef_hs_antiLCdeg.y, self.elf_pef_hs_antiLCdeg.y, decimal=1)
        assert_array_almost_equal(elf_pef_pa.y, self.elf_pef_pa.y, decimal=1)
        assert_allclose(elf_pef_Et_nflux.y, self.elf_pef_Et_nflux.y, rtol=1e-03)
        assert_allclose(elf_pef_hs_nflux_omni.y, self.elf_pef_hs_nflux_omni.y, rtol=1e-02)
        assert_allclose(elf_pef_hs_nflux_para.y, self.elf_pef_hs_nflux_para.y, rtol=1e-02)
        assert_allclose(elf_pef_hs_nflux_anti.y, self.elf_pef_hs_nflux_anti.y, rtol=1e-02)
        assert_allclose(elf_pef_hs_nflux_perp.y, self.elf_pef_hs_nflux_perp.y, rtol=1e-02)
        # test pa spectogram ch0
        spec2plot, pas2plot = spec_pa_sort(self.elf_pef_hs_nflux_ch0.y, self.elf_pef_hs_nflux_ch0.v) # idl variable use aceding and decending pa
        assert_allclose(elf_pef_hs_nflux_ch0.y, spec2plot, rtol=1e-02)
        # test pa spectogram ch1
        spec2plot, pas2plot = spec_pa_sort(self.elf_pef_hs_nflux_ch1.y, self.elf_pef_hs_nflux_ch1.v)
        assert_allclose(elf_pef_hs_nflux_ch1.y, spec2plot, rtol=1e-02)
        # test pa spectogram ch2
        spec2plot, pas2plot = spec_pa_sort(self.elf_pef_hs_nflux_ch2.y, self.elf_pef_hs_nflux_ch2.v)
        assert_allclose(elf_pef_hs_nflux_ch2.y, spec2plot, rtol=1e-02)
        # test pa spectogram ch3
        spec2plot, pas2plot = spec_pa_sort(self.elf_pef_hs_nflux_ch3.y, self.elf_pef_hs_nflux_ch3.v)
        assert_allclose(elf_pef_hs_nflux_ch3.y, spec2plot, rtol=1e-02)

        logging.info("HALFSPIN NFLUX DATA TEST FINISHED.")


    def test_epd_l2_hs_eflux(self):
        """Validate epd l2 halfspin eflux spectogram"""
        pyspedas.elfin.epd(trange=self.t, probe=self.probe, level='l2',no_update=True, type_='eflux')
        elf_pef_hs_eflux_ch0 = pytplot.get_data(f"el{self.probe}_pef_hs_eflux_ch0")
        elf_pef_hs_eflux_ch1 = pytplot.get_data(f"el{self.probe}_pef_hs_eflux_ch1")
        elf_pef_hs_eflux_ch2 = pytplot.get_data(f"el{self.probe}_pef_hs_eflux_ch2")
        elf_pef_hs_eflux_ch3 = pytplot.get_data(f"el{self.probe}_pef_hs_eflux_ch3")
        elf_pef_hs_eflux_perp = pytplot.get_data(f"el{self.probe}_pef_hs_eflux_perp")
        elf_pef_hs_eflux_anti = pytplot.get_data(f"el{self.probe}_pef_hs_eflux_anti")
        elf_pef_hs_eflux_para = pytplot.get_data(f"el{self.probe}_pef_hs_eflux_para")
        elf_pef_hs_eflux_omni = pytplot.get_data(f"el{self.probe}_pef_hs_eflux_omni")
        elf_pef_hs_Epat_eflux = pytplot.get_data(f"el{self.probe}_pef_hs_Epat_eflux")
        elf_pef_Et_eflux = pytplot.get_data(f"el{self.probe}_pef_Et_eflux")

        assert_array_almost_equal(elf_pef_hs_Epat_eflux.v1, self.elf_pef_hs_Epat_eflux_ch1.v, decimal=1)      
        assert_array_almost_equal(elf_pef_hs_Epat_eflux.y[:,:,0], self.elf_pef_hs_Epat_eflux_ch0.y, decimal=1)
        assert_array_almost_equal(elf_pef_hs_Epat_eflux.y[:,:,1], self.elf_pef_hs_Epat_eflux_ch1.y, decimal=1)
        assert_allclose(elf_pef_Et_eflux.y,  self.elf_pef_Et_eflux.y, rtol=1e-03)
        assert_allclose(elf_pef_hs_eflux_omni.y, self.elf_pef_hs_eflux_omni.y, rtol=1e-02)
        assert_allclose(elf_pef_hs_eflux_para.y, self.elf_pef_hs_eflux_para.y, rtol=1e-02)
        assert_allclose(elf_pef_hs_eflux_anti.y, self.elf_pef_hs_eflux_anti.y, rtol=1e-02)
        assert_allclose(elf_pef_hs_eflux_perp.y, self.elf_pef_hs_eflux_perp.y, rtol=1e-02)
        # test pa spectogram ch0
        spec2plot, pas2plot = spec_pa_sort(self.elf_pef_hs_eflux_ch0.y, self.elf_pef_hs_eflux_ch0.v) # idl variable use aceding and decending pa
        assert_allclose(elf_pef_hs_eflux_ch0.y, spec2plot, rtol=1e-02)
        # test pa spectogram ch1
        spec2plot, pas2plot = spec_pa_sort(self.elf_pef_hs_eflux_ch1.y, self.elf_pef_hs_eflux_ch1.v)
        assert_allclose(elf_pef_hs_eflux_ch1.y, spec2plot, rtol=1e-02)
        # test pa spectogram ch2
        spec2plot, pas2plot = spec_pa_sort(self.elf_pef_hs_eflux_ch2.y, self.elf_pef_hs_eflux_ch2.v)
        assert_allclose(elf_pef_hs_eflux_ch2.y, spec2plot, rtol=1e-02)
        # test pa spectogram ch3
        spec2plot, pas2plot = spec_pa_sort(self.elf_pef_hs_eflux_ch3.y, self.elf_pef_hs_eflux_ch3.v)
        assert_allclose(elf_pef_hs_eflux_ch3.y, spec2plot, rtol=1e-02)    
  
        logging.info("HALFSPIN EFLUX DATA TEST FINISHED.")


    def test_epd_l2_fs_nflux(self):
        """Validate epd l2 fullspin nflux spectogram"""
        pyspedas.elfin.epd(
            trange=self.t, 
            probe=self.probe, 
            level='l2',
            no_update=True, 
            fullspin=True,
            PAspec_energybins=[(0,3),(4,6)],
            )
        elf_pef_fs_nflux_ch0 = pytplot.get_data(f"el{self.probe}_pef_fs_nflux_ch0")
        elf_pef_fs_nflux_ch1 = pytplot.get_data(f"el{self.probe}_pef_fs_nflux_ch1")
        elf_pef_fs_nflux_ch2 = pytplot.get_data(f"el{self.probe}_pef_fs_nflux_ch2")
        elf_pef_fs_nflux_ch3 = pytplot.get_data(f"el{self.probe}_pef_fs_nflux_ch3")
        elf_pef_fs_nflux_perp = pytplot.get_data(f"el{self.probe}_pef_fs_nflux_perp")
        elf_pef_fs_nflux_anti = pytplot.get_data(f"el{self.probe}_pef_fs_nflux_anti")
        elf_pef_fs_nflux_para = pytplot.get_data(f"el{self.probe}_pef_fs_nflux_para")
        elf_pef_fs_nflux_omni = pytplot.get_data(f"el{self.probe}_pef_fs_nflux_omni")
        elf_pef_fs_antiLCdeg = pytplot.get_data(f"el{self.probe}_pef_fs_antiLCdeg")
        elf_pef_fs_LCdeg = pytplot.get_data(f"el{self.probe}_pef_fs_LCdeg")
        elf_pef_fs_Epat_nflux = pytplot.get_data(f"el{self.probe}_pef_fs_Epat_nflux")

        assert_array_almost_equal(elf_pef_fs_Epat_nflux.v1, self.elf_pef_fs_Epat_nflux_ch1.v, decimal=1)      
        assert_array_almost_equal(elf_pef_fs_Epat_nflux.y[:,:,0], self.elf_pef_fs_Epat_nflux_ch0.y, decimal=1)
        assert_array_almost_equal(elf_pef_fs_Epat_nflux.y[:,:,1], self.elf_pef_fs_Epat_nflux_ch1.y, decimal=1)
        assert_array_almost_equal(elf_pef_fs_LCdeg.y, self.elf_pef_fs_LCdeg.y, decimal=1)
        assert_array_almost_equal(elf_pef_fs_antiLCdeg.y, self.elf_pef_fs_antiLCdeg.y, decimal=1)
        assert_allclose(elf_pef_fs_nflux_omni.y, self.elf_pef_fs_nflux_omni.y, rtol=1e-02)
        assert_allclose(elf_pef_fs_nflux_para.y, self.elf_pef_fs_nflux_para.y, rtol=1e-02)
        assert_allclose(elf_pef_fs_nflux_anti.y, self.elf_pef_fs_nflux_anti.y, rtol=1e-02)
        assert_allclose(elf_pef_fs_nflux_perp.y, self.elf_pef_fs_nflux_perp.y, rtol=1e-02)
        # test pa spectogram ch0
        spec2plot, pas2plot = spec_pa_sort(self.elf_pef_fs_nflux_ch0.y, self.elf_pef_fs_nflux_ch0.v) # idl variable use aceding and decending pa
        assert_allclose(elf_pef_fs_nflux_ch0.y, spec2plot, rtol=1e-02)
        # test pa spectogram ch1
        spec2plot, pas2plot = spec_pa_sort(self.elf_pef_fs_nflux_ch1.y, self.elf_pef_fs_nflux_ch1.v)
        assert_allclose(elf_pef_fs_nflux_ch1.y, spec2plot, rtol=1e-02)

        logging.info("FULLSPIN NFLUX DATA TEST FINISHED.")


    def test_epd_l2_fs_eflux(self):
        """Validate epd l2 fullspin eflux spectogram"""
        pyspedas.elfin.epd(
            trange=self.t, 
            probe=self.probe, 
            level='l2',
            no_update=True, 
            fullspin=True, 
            type_='eflux', 
            PAspec_energies=[(50,250),(250,430)]
            )
        elf_pef_fs_eflux_ch0 = pytplot.get_data(f"el{self.probe}_pef_fs_eflux_ch0")
        elf_pef_fs_eflux_ch1 = pytplot.get_data(f"el{self.probe}_pef_fs_eflux_ch1")
        elf_pef_fs_eflux_perp = pytplot.get_data(f"el{self.probe}_pef_fs_eflux_perp")
        elf_pef_fs_eflux_anti = pytplot.get_data(f"el{self.probe}_pef_fs_eflux_anti")
        elf_pef_fs_eflux_para = pytplot.get_data(f"el{self.probe}_pef_fs_eflux_para")
        elf_pef_fs_eflux_omni = pytplot.get_data(f"el{self.probe}_pef_fs_eflux_omni")
        elf_pef_fs_Epat_eflux = pytplot.get_data(f"el{self.probe}_pef_fs_Epat_eflux")

        assert_array_almost_equal(elf_pef_fs_Epat_eflux.v1, self.elf_pef_fs_Epat_eflux_ch1.v, decimal=1)      
        assert_array_almost_equal(elf_pef_fs_Epat_eflux.y[:,:,0], self.elf_pef_fs_Epat_eflux_ch0.y, decimal=1)
        assert_array_almost_equal(elf_pef_fs_Epat_eflux.y[:,:,1], self.elf_pef_fs_Epat_eflux_ch1.y, decimal=1)
        assert_allclose(elf_pef_fs_eflux_omni.y, self.elf_pef_fs_eflux_omni.y, rtol=1e-02)
        assert_allclose(elf_pef_fs_eflux_para.y, self.elf_pef_fs_eflux_para.y, rtol=1e-02)
        assert_allclose(elf_pef_fs_eflux_anti.y, self.elf_pef_fs_eflux_anti.y, rtol=1e-02)
        assert_allclose(elf_pef_fs_eflux_perp.y, self.elf_pef_fs_eflux_perp.y, rtol=1e-02)
        # test pa spectogram ch0
        spec2plot, pas2plot = spec_pa_sort(self.elf_pef_fs_eflux_ch0.y, self.elf_pef_fs_eflux_ch0.v) # idl variable use aceding and decending pa
        assert_allclose(elf_pef_fs_eflux_ch0.y, spec2plot, rtol=1e-02)
        # test pa spectogram ch1
        spec2plot, pas2plot = spec_pa_sort(self.elf_pef_fs_eflux_ch1.y, self.elf_pef_fs_eflux_ch1.v)
        assert_allclose(elf_pef_fs_eflux_ch1.y, spec2plot, rtol=1e-02)

        logging.info("FULLSPIN EFLUX DATA TEST FINISHED.")


if __name__ == '__main__':
    unittest.main()
