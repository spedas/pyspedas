"""Tests of cal_fit function."""
import pyspedas.elfin
import pytplot.get_data
from pytplot.importers.tplot_restore import tplot_restore
import unittest
import numpy as np
from numpy.testing import assert_allclose, assert_array_almost_equal, assert_array_equal


class TestELFStateValidation(unittest.TestCase):
    """Tests of the data been identical to SPEDAS (IDL)."""

    @classmethod
    def setUpClass(cls):
        """
        IDL Data has to be downloaded to perform these tests
        The IDL script that creates data file:
        https://github.com/spedas/pyspedas-validation/blob/cal_fit/src/themis/validation_files/thm_load_fit_validation_files.pro
        """

        # Testing time range
        cls.t = ['2022-01-14/06:28', '2022-01-14/06:35']

        # Testing tollerange
        cls.tol = 1e-3


        # Load validation variables from the test file
        filename = 'elfin_data/elf_state_validation.tplot'
        tplot_restore(filename)
        cls.elf_pos_gei = pytplot.get_data('ela_pos_gei')
        cls.elf_vel_gei = pytplot.get_data('ela_vel_gei')
        cls.elf_att_gei = pytplot.get_data('ela_att_gei')
        cls.elf_att_solution = pytplot.get_data('ela_att_solution_date')
        cls.elf_att_flag = pytplot.get_data('ela_att_flag')
        cls.elf_att_spinper = pytplot.get_data('ela_att_spinper')
        cls.elf_spin_orbnorm = pytplot.get_data('ela_spin_orbnorm_angle')
        cls.elf_spin_sun = pytplot.get_data('ela_spin_sun_angle')


    def setUp(self):
        """ We need to clean tplot variables before each run"""
        pytplot.del_data('*')

    def test_state_pos(self):
        """Validate load data."""
        pyspedas.elfin.state(trange=['2022-01-14/06:28', '2022-01-14/06:35'], probe='a')
        elf_pos_gei = pytplot.get_data('ela_pos_gei')
        elf_vel_gei = pytplot.get_data('ela_vel_gei')
        elf_att_gei = pytplot.get_data('ela_att_gei')
        elf_att_solution = pytplot.get_data('ela_att_solution_date')
        elf_att_flag = pytplot.get_data('ela_att_flag')
        elf_att_spinper = pytplot.get_data('ela_att_spinper')
        elf_spin_orbnorm = pytplot.get_data('ela_spin_orbnorm_angle')
        elf_spin_sun = pytplot.get_data('ela_spin_sun_angle')

        assert_array_almost_equal(elf_pos_gei.y, self.elf_pos_gei.y, decimal=4)
        assert_array_almost_equal(elf_vel_gei.y, self.elf_vel_gei.y, decimal=4)
        assert_array_almost_equal(elf_att_gei.y, self.elf_att_gei.y, decimal=2)
        assert_allclose(elf_att_solution.times, self.elf_att_solution.y, rtol=1e-3)
        assert_array_equal(elf_att_flag.y, self.elf_att_flag.y)
        assert_allclose(elf_att_spinper.y, self.elf_att_spinper.y, rtol=1e-2)
        assert_allclose(elf_spin_orbnorm.y, self.elf_spin_orbnorm.y, rtol=1e-2)
        assert_allclose(elf_spin_sun.y, self.elf_spin_sun.y, rtol=1e-2)


if __name__ == '__main__':
    unittest.main()
