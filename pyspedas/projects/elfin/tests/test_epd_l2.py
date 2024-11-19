"""
This module perform unitest on elfin epd l2 spectrogram by comparing 
with tplot variable genrate by IDL routine

How to run:
    $ python -m pyspedas.projects.elfin.tests.test_epd_l2
"""
import unittest
import logging
from numpy.testing import assert_allclose
import pytplot.get_data
from pytplot.importers.tplot_restore import tplot_restore

import pyspedas.projects.elfin
from pyspedas.projects.elfin.epd.calibration_l2 import spec_pa_sort
from pyspedas.utilities.download import download
from pyspedas.projects.elfin.config import CONFIG

TEST_DATASET_PATH="test/"

class TestELFL2Validation(unittest.TestCase):
    """Tests of the data been identical to SPEDAS (IDL)."""

    @classmethod
    def setUpClass(cls):
        """
        IDL Data has to be downloaded to perform these tests
        The IDL script that creates data file: epd_level2_check2.pro
        """

        # Testing time range
        #cls.t = ['2022-04-01/09:45:00','2022-04-01/10:10:00'] # elb with inner belt, pass
        #cls.probe = 'b'
        cls.t = ['2022-08-28/15:54','2022-08-28/16:15'] # pass
        cls.probe = 'a'

        # load epd l2 hs nflux spectrogram
        calfile_name = f"{TEST_DATASET_PATH}validation_el{cls.probe}_epd_l2_hs_nflux_{cls.t[0][0:4]+cls.t[0][5:7]+cls.t[0][8:10]}.tplot"
        calfile = download(remote_file=calfile_name,
                           remote_path=CONFIG['remote_data_dir'],
                           local_path=CONFIG['local_data_dir'],
                           no_download=False)
        if not calfile:
            # Skip tests
            raise unittest.SkipTest(f"Cannot download validation file {calfile_name}")
        filename = CONFIG['local_data_dir'] + calfile_name
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
        cls.elf_pef_hs_Epat_nflux_ch0 = pytplot.get_data(f"el{cls.probe}_pef_hs_Epat_nflux_ch0")
        # Epat is 3d, can't save it with idl
        cls.elf_pef_hs_Epat_nflux_ch1 = pytplot.get_data(f"el{cls.probe}_pef_hs_Epat_nflux_ch1")

        # load epd l2 hs eflux spectrogram
        calfile_name = f"{TEST_DATASET_PATH}validation_el{cls.probe}_epd_l2_hs_eflux_{cls.t[0][0:4]+cls.t[0][5:7]+cls.t[0][8:10]}.tplot"
        calfile = download(remote_file=calfile_name,
                           remote_path=CONFIG['remote_data_dir'],
                           local_path=CONFIG['local_data_dir'],
                           no_download=False)
        if not calfile:
            raise unittest.SkipTest(f"Cannot download validation file {calfile_name}")
        filename = CONFIG['local_data_dir'] + calfile_name
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
        cls.elf_pef_hs_Epat_eflux_ch0 = pytplot.get_data(f"el{cls.probe}_pef_hs_Epat_eflux_ch0")
        # Epat is 3d, can't save it with idl
        cls.elf_pef_hs_Epat_eflux_ch1 = pytplot.get_data(f"el{cls.probe}_pef_hs_Epat_eflux_ch1")


        # load epd l2 fs nflux spectrogram
        calfile_name = f"{TEST_DATASET_PATH}validation_el{cls.probe}_epd_l2_fs_nflux_{cls.t[0][0:4]+cls.t[0][5:7]+cls.t[0][8:10]}.tplot"
        calfile = download(remote_file=calfile_name,
                           remote_path=CONFIG['remote_data_dir'],
                           local_path=CONFIG['local_data_dir'],
                           no_download=False)
        if not calfile:
            raise unittest.SkipTest(f"Cannot download validation file {calfile_name}")
        filename = CONFIG['local_data_dir'] + calfile_name
        tplot_restore(filename)
        cls.elf_pef_fs_nflux_ch0 = pytplot.get_data(f"el{cls.probe}_pef_fs_nflux_ch0")
        cls.elf_pef_fs_nflux_ch1 = pytplot.get_data(f"el{cls.probe}_pef_fs_nflux_ch1")
        cls.elf_pef_fs_nflux_omni = pytplot.get_data(f"el{cls.probe}_pef_fs_nflux_omni")
        cls.elf_pef_fs_nflux_para = pytplot.get_data(f"el{cls.probe}_pef_fs_nflux_para")
        cls.elf_pef_fs_nflux_anti = pytplot.get_data(f"el{cls.probe}_pef_fs_nflux_anti")
        cls.elf_pef_fs_nflux_perp = pytplot.get_data(f"el{cls.probe}_pef_fs_nflux_perp")
        cls.elf_pef_fs_antiLCdeg = pytplot.get_data(f"el{cls.probe}_pef_fs_antiLCdeg")
        cls.elf_pef_fs_LCdeg = pytplot.get_data(f"el{cls.probe}_pef_fs_LCdeg")
        cls.elf_pef_fs_Epat_nflux_ch0 = pytplot.get_data(f"el{cls.probe}_pef_fs_Epat_nflux_ch0")
        # Epat is 3d, can't save it with idl
        cls.elf_pef_fs_Epat_nflux_ch1 = pytplot.get_data(f"el{cls.probe}_pef_fs_Epat_nflux_ch1")


        # load epd l2 fs eflux spectrogram
        calfile_name = f"{TEST_DATASET_PATH}validation_el{cls.probe}_epd_l2_fs_eflux_{cls.t[0][0:4]+cls.t[0][5:7]+cls.t[0][8:10]}.tplot"
        calfile = download(remote_file=calfile_name,
                           remote_path=CONFIG['remote_data_dir'],
                           local_path=CONFIG['local_data_dir'],
                           no_download=False)
        if not calfile:
            raise unittest.SkipTest(f"Cannot download validation file {calfile_name}")
        filename = CONFIG['local_data_dir'] + calfile_name
        tplot_restore(filename)
        cls.elf_pef_fs_eflux_ch0 = pytplot.get_data(f"el{cls.probe}_pef_fs_eflux_ch0")
        cls.elf_pef_fs_eflux_ch1 = pytplot.get_data(f"el{cls.probe}_pef_fs_eflux_ch1")
        cls.elf_pef_fs_eflux_omni = pytplot.get_data(f"el{cls.probe}_pef_fs_eflux_omni")
        cls.elf_pef_fs_eflux_para = pytplot.get_data(f"el{cls.probe}_pef_fs_eflux_para")
        cls.elf_pef_fs_eflux_anti = pytplot.get_data(f"el{cls.probe}_pef_fs_eflux_anti")
        cls.elf_pef_fs_eflux_perp = pytplot.get_data(f"el{cls.probe}_pef_fs_eflux_perp")
        cls.elf_pef_fs_Epat_eflux_ch0 = pytplot.get_data(f"el{cls.probe}_pef_fs_Epat_eflux_ch0")
        # Epat is 3d, can't save it with idl
        cls.elf_pef_fs_Epat_eflux_ch1 = pytplot.get_data(f"el{cls.probe}_pef_fs_Epat_eflux_ch1")


    def setUp(self):
        """ We need to clean tplot variables before each run"""
        pytplot.del_data('*')


    def test_epd_l2_hs_nflux(self):
        """Validate epd l2 halfspin nflux spectogram"""
        pyspedas.projects.elfin.epd(trange=self.t, probe=self.probe, level='l2',no_update=True)
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
        
        assert_allclose(elf_pef_hs_Epat_nflux.v1, self.elf_pef_hs_Epat_nflux_ch1.v, rtol=1)
        assert_allclose(elf_pef_hs_Epat_nflux.y[:,:,0], self.elf_pef_hs_Epat_nflux_ch0.y, rtol=1e-02)
        assert_allclose(elf_pef_hs_Epat_nflux.y[:,:,1], self.elf_pef_hs_Epat_nflux_ch1.y, rtol=1e-02)
        assert_allclose(elf_pef_hs_LCdeg.y, self.elf_pef_hs_LCdeg.y, rtol=1e-02)
        assert_allclose(elf_pef_hs_antiLCdeg.y, self.elf_pef_hs_antiLCdeg.y, rtol=1e-02)
        assert_allclose(elf_pef_pa.y, self.elf_pef_pa.y, rtol=1e-02)
        assert_allclose(elf_pef_Et_nflux.y, self.elf_pef_Et_nflux.y, rtol=1e-02)
        assert_allclose(elf_pef_hs_nflux_omni.y, self.elf_pef_hs_nflux_omni.y, rtol=1e-02)
        assert_allclose(elf_pef_hs_nflux_para.y, self.elf_pef_hs_nflux_para.y, rtol=1e-02)
        assert_allclose(elf_pef_hs_nflux_anti.y, self.elf_pef_hs_nflux_anti.y, rtol=1e-02)
        assert_allclose(elf_pef_hs_nflux_perp.y, self.elf_pef_hs_nflux_perp.y, rtol=1e-02)
        # test pa spectogram ch0
        spec2plot, _ = spec_pa_sort(self.elf_pef_hs_nflux_ch0.y, self.elf_pef_hs_nflux_ch0.v) 
        # idl variable use aceding and decending pa
        assert_allclose(elf_pef_hs_nflux_ch0.y, spec2plot, rtol=1e-02)
        # test pa spectogram ch1
        spec2plot, _ = spec_pa_sort(self.elf_pef_hs_nflux_ch1.y, self.elf_pef_hs_nflux_ch1.v)
        assert_allclose(elf_pef_hs_nflux_ch1.y, spec2plot, rtol=1e-02)
        # test pa spectogram ch2
        spec2plot, _ = spec_pa_sort(self.elf_pef_hs_nflux_ch2.y, self.elf_pef_hs_nflux_ch2.v)
        assert_allclose(elf_pef_hs_nflux_ch2.y, spec2plot, rtol=1e-02)
        # test pa spectogram ch3
        spec2plot, _ = spec_pa_sort(self.elf_pef_hs_nflux_ch3.y, self.elf_pef_hs_nflux_ch3.v)
        assert_allclose(elf_pef_hs_nflux_ch3.y, spec2plot, rtol=1e-02)

        logging.info("HALFSPIN NFLUX DATA TEST FINISHED.")


    def test_epd_l2_hs_eflux(self):
        """Validate epd l2 halfspin eflux spectogram"""
        pyspedas.projects.elfin.epd(
            trange=self.t,
            probe=self.probe,
            level='l2',
            no_update=False,
            type_='eflux',
            Espec_LCfatol=40,
            Espec_LCfptol=5,)
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

        assert_allclose(elf_pef_hs_Epat_eflux.v1, self.elf_pef_hs_Epat_eflux_ch1.v, rtol=1)
        assert_allclose(elf_pef_hs_Epat_eflux.y[:,:,0], self.elf_pef_hs_Epat_eflux_ch0.y,  rtol=1e-02)
        assert_allclose(elf_pef_hs_Epat_eflux.y[:,:,1], self.elf_pef_hs_Epat_eflux_ch1.y,  rtol=1e-02)
        assert_allclose(elf_pef_Et_eflux.y,  self.elf_pef_Et_eflux.y, rtol=1e-02)
        assert_allclose(elf_pef_hs_eflux_omni.y, self.elf_pef_hs_eflux_omni.y, rtol=2e-02)
        assert_allclose(elf_pef_hs_eflux_para.y, self.elf_pef_hs_eflux_para.y, rtol=2e-02)
        assert_allclose(elf_pef_hs_eflux_anti.y, self.elf_pef_hs_eflux_anti.y, rtol=2e-02)
        assert_allclose(elf_pef_hs_eflux_perp.y, self.elf_pef_hs_eflux_perp.y, rtol=2e-02)
        # test pa spectogram ch0
        spec2plot, _ = spec_pa_sort(self.elf_pef_hs_eflux_ch0.y, self.elf_pef_hs_eflux_ch0.v) 
        # idl variable use aceding and decending pa
        assert_allclose(elf_pef_hs_eflux_ch0.y, spec2plot, rtol=1e-02)
        # test pa spectogram ch1
        spec2plot, _ = spec_pa_sort(self.elf_pef_hs_eflux_ch1.y, self.elf_pef_hs_eflux_ch1.v)
        assert_allclose(elf_pef_hs_eflux_ch1.y, spec2plot, rtol=1e-02)
        # test pa spectogram ch2
        spec2plot, _ = spec_pa_sort(self.elf_pef_hs_eflux_ch2.y, self.elf_pef_hs_eflux_ch2.v)
        assert_allclose(elf_pef_hs_eflux_ch2.y, spec2plot, rtol=1e-02)
        # test pa spectogram ch3
        spec2plot, _ = spec_pa_sort(self.elf_pef_hs_eflux_ch3.y, self.elf_pef_hs_eflux_ch3.v)
        assert_allclose(elf_pef_hs_eflux_ch3.y, spec2plot, rtol=1e-02)    
  
        logging.info("HALFSPIN EFLUX DATA TEST FINISHED.")


    def test_epd_l2_fs_nflux(self):
        """Validate epd l2 fullspin nflux spectogram"""
        pyspedas.projects.elfin.epd(
            trange=self.t,
            probe=self.probe,
            level='l2',
            no_update=False,
            fullspin=True,
            PAspec_energybins=[(0,3),(4,6)],
            )
        elf_pef_fs_nflux_ch0 = pytplot.get_data(f"el{self.probe}_pef_fs_nflux_ch0")
        elf_pef_fs_nflux_ch1 = pytplot.get_data(f"el{self.probe}_pef_fs_nflux_ch1")
        elf_pef_fs_nflux_perp = pytplot.get_data(f"el{self.probe}_pef_fs_nflux_perp")
        elf_pef_fs_nflux_anti = pytplot.get_data(f"el{self.probe}_pef_fs_nflux_anti")
        elf_pef_fs_nflux_para = pytplot.get_data(f"el{self.probe}_pef_fs_nflux_para")
        elf_pef_fs_nflux_omni = pytplot.get_data(f"el{self.probe}_pef_fs_nflux_omni")
        elf_pef_fs_antiLCdeg = pytplot.get_data(f"el{self.probe}_pef_fs_antiLCdeg")
        elf_pef_fs_LCdeg = pytplot.get_data(f"el{self.probe}_pef_fs_LCdeg")
        elf_pef_fs_Epat_nflux = pytplot.get_data(f"el{self.probe}_pef_fs_Epat_nflux")

        assert_allclose(elf_pef_fs_Epat_nflux.v1, self.elf_pef_fs_Epat_nflux_ch1.v, rtol=1)
        assert_allclose(elf_pef_fs_Epat_nflux.y[:,:,0], self.elf_pef_fs_Epat_nflux_ch0.y, rtol=1e-02)
        assert_allclose(elf_pef_fs_Epat_nflux.y[:,:,1], self.elf_pef_fs_Epat_nflux_ch1.y, rtol=1e-02)
        assert_allclose(elf_pef_fs_LCdeg.y, self.elf_pef_fs_LCdeg.y, rtol=1e-02)
        assert_allclose(elf_pef_fs_antiLCdeg.y, self.elf_pef_fs_antiLCdeg.y, rtol=1e-02)
        assert_allclose(elf_pef_fs_nflux_omni.y, self.elf_pef_fs_nflux_omni.y, rtol=1e-02)
        assert_allclose(elf_pef_fs_nflux_para.y, self.elf_pef_fs_nflux_para.y, rtol=1e-02)
        assert_allclose(elf_pef_fs_nflux_anti.y, self.elf_pef_fs_nflux_anti.y, rtol=1e-02)
        assert_allclose(elf_pef_fs_nflux_perp.y, self.elf_pef_fs_nflux_perp.y, rtol=1e-02)
        # test pa spectogram ch0
        spec2plot, _ = spec_pa_sort(self.elf_pef_fs_nflux_ch0.y, self.elf_pef_fs_nflux_ch0.v) 
        # idl variable use aceding and decending pa
        assert_allclose(elf_pef_fs_nflux_ch0.y, spec2plot, rtol=1e-02)
        # test pa spectogram ch1
        spec2plot, _ = spec_pa_sort(self.elf_pef_fs_nflux_ch1.y, self.elf_pef_fs_nflux_ch1.v)
        assert_allclose(elf_pef_fs_nflux_ch1.y, spec2plot, rtol=1e-02)

        logging.info("FULLSPIN NFLUX DATA TEST FINISHED.")


    def test_epd_l2_fs_eflux(self):
        """Validate epd l2 fullspin eflux spectogram"""
        pyspedas.projects.elfin.epd(
            trange=self.t,
            probe=self.probe,
            level='l2',
            no_update=False,
            fullspin=True,
            type_='eflux',
            PAspec_energies=[(50,250),(250,430)],
            )
        elf_pef_fs_eflux_ch0 = pytplot.get_data(f"el{self.probe}_pef_fs_eflux_ch0")
        elf_pef_fs_eflux_ch1 = pytplot.get_data(f"el{self.probe}_pef_fs_eflux_ch1")
        elf_pef_fs_eflux_perp = pytplot.get_data(f"el{self.probe}_pef_fs_eflux_perp")
        elf_pef_fs_eflux_anti = pytplot.get_data(f"el{self.probe}_pef_fs_eflux_anti")
        elf_pef_fs_eflux_para = pytplot.get_data(f"el{self.probe}_pef_fs_eflux_para")
        elf_pef_fs_eflux_omni = pytplot.get_data(f"el{self.probe}_pef_fs_eflux_omni")
        elf_pef_fs_Epat_eflux = pytplot.get_data(f"el{self.probe}_pef_fs_Epat_eflux")
        
        assert_allclose(elf_pef_fs_Epat_eflux.v1, self.elf_pef_fs_Epat_eflux_ch1.v, rtol=1)
        assert_allclose(elf_pef_fs_Epat_eflux.y[:,:,0], self.elf_pef_fs_Epat_eflux_ch0.y, rtol=1e-02)
        assert_allclose(elf_pef_fs_Epat_eflux.y[:,:,1], self.elf_pef_fs_Epat_eflux_ch1.y, rtol=1e-02)
        assert_allclose(elf_pef_fs_eflux_omni.y, self.elf_pef_fs_eflux_omni.y, rtol=1e-02)
        assert_allclose(elf_pef_fs_eflux_para.y, self.elf_pef_fs_eflux_para.y, rtol=1e-02)
        assert_allclose(elf_pef_fs_eflux_anti.y, self.elf_pef_fs_eflux_anti.y, rtol=1e-02)
        assert_allclose(elf_pef_fs_eflux_perp.y, self.elf_pef_fs_eflux_perp.y, rtol=1e-02)
        # test pa spectogram ch0
        spec2plot, _ = spec_pa_sort(self.elf_pef_fs_eflux_ch0.y, self.elf_pef_fs_eflux_ch0.v) 
        # idl variable use aceding and decending pa
        assert_allclose(elf_pef_fs_eflux_ch0.y, spec2plot, rtol=1e-02)
        # test pa spectogram ch1
        spec2plot, _ = spec_pa_sort(self.elf_pef_fs_eflux_ch1.y, self.elf_pef_fs_eflux_ch1.v)
        assert_allclose(elf_pef_fs_eflux_ch1.y, spec2plot, rtol=1e-02)

        logging.info("FULLSPIN EFLUX DATA TEST FINISHED.")
    

if __name__ == '__main__':
    unittest.main()
