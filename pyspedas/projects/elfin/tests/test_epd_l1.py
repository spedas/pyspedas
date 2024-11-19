"""
This module perform unitest on elfin epd l1 spectrogram by comparing 
with tplot variable genrate by IDL routine 

How to run:
    $ python -m pyspedas.projects.elfin.tests.test_epd_l1
"""
import unittest
import logging
import pytplot.get_data
from pytplot.importers.tplot_restore import tplot_restore
from numpy.testing import assert_allclose

import pyspedas.projects.elfin
from pyspedas.utilities.download import download
from pyspedas.projects.elfin.config import CONFIG

TEST_DATASET_PATH="test/"

class TestELFL1Validation(unittest.TestCase):
    """Tests of the data been identical to SPEDAS (IDL)."""

    @classmethod
    def setUpClass(cls):
        """
        IDL Data has to be downloaded to perform these tests
        The IDL script that creates data file: epd_level1_check.pro
        """
        # Testing time range
        cls.t = ['2022-04-12/19:00:00','2022-04-12/19:15:00']
        cls.probe = 'b'

        # load epd l1 raw flux
        calfile_name = f"{TEST_DATASET_PATH}validation_el{cls.probe}_epd_l1_raw_{cls.t[0][0:4]+cls.t[0][5:7]+cls.t[0][8:10]}.tplot"
        calfile = download(remote_file=calfile_name,
                           remote_path=CONFIG['remote_data_dir'],
                           local_path=CONFIG['local_data_dir'],
                           no_download=False)
        if not calfile:
            raise unittest.SkipTest(f"Cannot download validation file {calfile_name}")
        filename = CONFIG['local_data_dir'] + calfile_name
        tplot_restore(filename)
        cls.elf_pef_raw = pytplot.get_data(f"el{cls.probe}_pef_raw")

        # load epd l1 cps flux
        calfile_name = f"{TEST_DATASET_PATH}validation_el{cls.probe}_epd_l1_cps_{cls.t[0][0:4]+cls.t[0][5:7]+cls.t[0][8:10]}.tplot"
        calfile = download(remote_file=calfile_name,
                           remote_path=CONFIG['remote_data_dir'],
                           local_path=CONFIG['local_data_dir'],
                           no_download=False)
        if not calfile:
            raise unittest.SkipTest(f"Cannot download validation file {calfile_name}")
        filename = CONFIG['local_data_dir'] + calfile_name
        tplot_restore(filename)
        cls.elf_pef_cps = pytplot.get_data(f"el{cls.probe}_pef_cps")

        # load epd l1 nflux flux
        calfile_name = f"{TEST_DATASET_PATH}validation_el{cls.probe}_epd_l1_nflux_{cls.t[0][0:4]+cls.t[0][5:7]+cls.t[0][8:10]}.tplot"
        calfile = download(remote_file=calfile_name,
                           remote_path=CONFIG['remote_data_dir'],
                           local_path=CONFIG['local_data_dir'],
                           no_download=False)
        if not calfile:
            raise unittest.SkipTest(f"Cannot download validation file {calfile_name}")
        filename = CONFIG['local_data_dir'] + calfile_name
        tplot_restore(filename)
        cls.elf_pef_nflux = pytplot.get_data(f"el{cls.probe}_pef_nflux")

        # load epd l1 eflux spectrogram
        calfile_name = f"{TEST_DATASET_PATH}validation_el{cls.probe}_epd_l1_eflux_{cls.t[0][0:4]+cls.t[0][5:7]+cls.t[0][8:10]}.tplot"
        calfile = download(remote_file=calfile_name,
                           remote_path=CONFIG['remote_data_dir'],
                           local_path=CONFIG['local_data_dir'],
                           no_download=False)
        if not calfile:
            raise unittest.SkipTest(f"Cannot download validation file {calfile_name}")
        filename = CONFIG['local_data_dir'] + calfile_name
        tplot_restore(filename)
        cls.elf_pef_eflux = pytplot.get_data(f"el{cls.probe}_pef_eflux")
        cls.elf_pef_sectnum = pytplot.get_data(f"el{cls.probe}_pef_sectnum")
        cls.elf_pef_nspinsinsum = pytplot.get_data(f"el{cls.probe}_pef_nspinsinsum")
        cls.elf_pef_nsectors = pytplot.get_data(f"el{cls.probe}_pef_nsectors")
        cls.elf_pef_spinper = pytplot.get_data(f"el{cls.probe}_pef_spinper")


    def setUp(self):
        """ We need to clean tplot variables before each run"""
        pytplot.del_data('*')


    def test_epd_l1_raw(self):
        """Validate epd l1 raw spectogram"""
        pyspedas.projects.elfin.epd(trange=self.t, probe=self.probe, level='l1', type_='raw')
        elf_pef_raw = pytplot.get_data(f"el{self.probe}_pef_raw")
        assert_allclose(elf_pef_raw.y, self.elf_pef_raw.y, rtol=1e-01)

        logging.info("L1 RAW DATA TEST FINISHED.")


    def test_epd_l1_cps(self):
        """Validate epd l1 nflux spectogram"""
        pyspedas.projects.elfin.epd(trange=self.t, probe=self.probe, level='l1', type_='cps')
        elf_pef_cps = pytplot.get_data(f"el{self.probe}_pef_cps")
        assert_allclose(elf_pef_cps.y, self.elf_pef_cps.y, rtol=1e-01)

        logging.info("L1 CPS DATA TEST FINISHED.")


    def test_epd_l1_nflux(self):
        """Validate epd l1 nflux spectogram"""
        pyspedas.projects.elfin.epd(trange=self.t, probe=self.probe, level='l1', type_='nflux')
        elf_pef_nflux = pytplot.get_data(f"el{self.probe}_pef_nflux")
        assert_allclose(elf_pef_nflux.y, self.elf_pef_nflux.y, rtol=1e-01)

        logging.info("L1 NFLUX DATA TEST FINISHED.")


    def test_epd_l1_eflux(self):
        """Validate epd l1 elux spectogram"""
        pyspedas.projects.elfin.epd(trange=self.t, probe=self.probe, level='l1', type_='eflux')
        elf_pef_eflux = pytplot.get_data(f"el{self.probe}_pef_eflux")
        elf_pef_sectnum = pytplot.get_data(f"el{self.probe}_pef_sectnum")
        elf_pef_nspinsinsum = pytplot.get_data(f"el{self.probe}_pef_nspinsinsum")
        elf_pef_nsectors = pytplot.get_data(f"el{self.probe}_pef_nsectors")
        elf_pef_spinper = pytplot.get_data(f"el{self.probe}_pef_spinper")

        assert_allclose(elf_pef_eflux.y, self.elf_pef_eflux.y, rtol=1)
        assert_allclose(elf_pef_sectnum.y, self.elf_pef_sectnum.y, rtol=1e-02)
        assert_allclose(elf_pef_nspinsinsum.y, self.elf_pef_nspinsinsum.y, rtol=1e-02)
        assert_allclose(elf_pef_nsectors.y, self.elf_pef_nsectors.y, rtol=1e-02)
        assert_allclose(elf_pef_spinper.y, self.elf_pef_spinper.y, rtol=1e-02)

        logging.info("L1 EFLUX DATA TEST FINISHED.")


if __name__ == '__main__':
    unittest.main()
