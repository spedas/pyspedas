import unittest
from pyspedas.mms.particles.mms_part_slice2d import mms_part_slice2d
from pyspedas.particles.spd_units_string import spd_units_string


class SliceTests(unittest.TestCase):
    def test_fpi_brst_rotations(self):
        time = '2015-10-16/13:06:30'
        rotations = ['xy', 'xz', 'bv', 'be', 'xvel', 'perp', 'perp_xy', 'perp_xz', 'perp_yz', 'b_exb', 'perp1-perp2']
        species = ['i', 'e']
        for spc in species:
            for rotation in rotations:
                mms_part_slice2d(time=time, probe='1', species=spc, data_rate='brst', rotation=rotation, save_png='test_fpi_brst_' + spc + '_' + rotation, display=False)

    def test_fpi_2d_interp(self):
        time = '2015-10-16/13:06:30'
        mms_part_slice2d(time=time, probe='1', species='i', data_rate='brst', rotation='xy',
                         interpolation='2d', save_png='test_fpi_brst_2d_interp', display=False)

    def test_fpi_limits(self):
        time = '2015-10-16/13:06:30'
        mms_part_slice2d(time=time, probe='1', species='i', data_rate='brst', rotation='xy', erange=[0, 10000],
                         save_png='test_fpi_brst_erange', display=False)

    def test_hpca(self):
        time = '2015-10-16/13:06:30'
        mms_part_slice2d(time=time, probe='1', species='hplus', instrument='hpca', data_rate='brst', rotation='xy',
                         save_png='test_hpca_brst', display=False)

    def test_units_string(self):
        self.assertTrue(spd_units_string('counts') == 'Counts')
        self.assertTrue(spd_units_string('rate') == 'Rate (#/sec)')
        self.assertTrue(spd_units_string('eflux') == 'Energy Flux (eV / sec / $cm^2$ / ster / eV)')
        self.assertTrue(spd_units_string('flux') == 'Flux (# / sec / $cm^2$ / ster / eV)')
        self.assertTrue(spd_units_string('df') == 'f ($s^3$ / $cm^3$ / $km^3$)')
        self.assertTrue(spd_units_string('df_cm') == 'f ($s^3$ / $cm^6$)')
        self.assertTrue(spd_units_string('df_km') == 'f ($s^3$ / $km^6$)')
        self.assertTrue(spd_units_string('e2flux') == '$Energy^2$ Flux ($eV^2$ / sec / $cm^2$ / ster /eV)')
        self.assertTrue(spd_units_string('e3flux') == '$Energy^3$ Flux ($eV^3$ / sec / $cm^2$ / ster /eV)')


if __name__ == '__main__':
    unittest.main()
