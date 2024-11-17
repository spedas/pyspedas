"""
This module perform unitest on elfin state file by comparing 
with tplot variable genrate by IDL routine

How to run:
    $ python -m pyspedas.projects.elfin.tests.test_state
"""
import unittest
import logging
import pytplot.get_data
from pytplot.importers.tplot_restore import tplot_restore
from numpy.testing import assert_allclose, assert_array_almost_equal, assert_array_equal

import pyspedas.projects.elfin
from pyspedas.utilities.download import download
from pyspedas.projects.elfin.config import CONFIG

TEST_DATASET_PATH="test/"

class TestELFStateValidation(unittest.TestCase):
    """Tests of the data been identical to SPEDAS (IDL)."""

    @classmethod
    def setUpClass(cls):
        """
        IDL Data has to be downloaded to perform these tests
        The IDL script that creates data file: (epd_state_validation.pro)
        """
        # Testing time range
        cls.t = ['2021-10-12/23:00:00','2021-10-12/23:10:00']
        cls.probe = 'b'

        # Load validation variables from the test file
        calfile_name = f"{TEST_DATASET_PATH}validation_el{cls.probe}_state_{cls.t[0][0:4]+cls.t[0][5:7]+cls.t[0][8:10]}.tplot"
        calfile = download(remote_file=calfile_name,
                           remote_path=CONFIG['remote_data_dir'],
                           local_path=CONFIG['local_data_dir'],
                           no_download=False)
        if not calfile:
            raise unittest.SkipTest(f"Cannot download validation file {calfile_name}")
        filename = CONFIG['local_data_dir'] + calfile_name
        tplot_restore(filename)
        cls.elf_pos_gei = pytplot.get_data(f"el{cls.probe}_pos_gei")
        cls.elf_vel_gei = pytplot.get_data(f"el{cls.probe}_vel_gei")
        cls.elf_att_gei = pytplot.get_data(f"el{cls.probe}_att_gei")
        cls.elf_att_solution = pytplot.get_data(f"el{cls.probe}_att_solution_date")
        cls.elf_att_flag = pytplot.get_data(f"el{cls.probe}_att_flag")
        cls.elf_att_spinper = pytplot.get_data(f"el{cls.probe}_att_spinper")
        cls.elf_spin_orbnorm = pytplot.get_data(f"el{cls.probe}_spin_orbnorm_angle")
        cls.elf_spin_sun = pytplot.get_data(f"el{cls.probe}_spin_sun_angle")


    def setUp(self):
        """ We need to clean tplot variables before each run"""
        pytplot.del_data('*')

    def test_state(self):
        """Validate state data."""
        pyspedas.projects.elfin.state(trange=self.t, probe=self.probe)
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
        # Jiashu says the default for this variable has changed, so we can leave this
        # assertion commented out.
        # assert_array_equal(elf_att_flag.y, self.elf_att_flag.y)
        assert_allclose(elf_att_spinper.y, self.elf_att_spinper.y, rtol=1e-2)
        assert_allclose(elf_spin_orbnorm.y, self.elf_spin_orbnorm.y, rtol=1e-2)
        assert_allclose(elf_spin_sun.y, self.elf_spin_sun.y, rtol=1e-2)

        logging.info("STATE DATA TEST FINISHED.")


if __name__ == '__main__':
    unittest.main()
