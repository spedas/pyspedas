import numpy as np
import unittest
from pyspedas.mms.particles.mms_part_slice2d import mms_part_slice2d
from pyspedas.particles.spd_units_string import spd_units_string


class SliceTests(unittest.TestCase):
    def test_fpi_brst_rotations(self):
        time = '2015-10-16/13:06:30'
        # rotations = ['xy', 'xz', 'bv', 'be', 'xvel', 'perp', 'perp_xy', 'perp_xz', 'perp_yz', 'b_exb', 'perp1-perp2']
        rotations = ['bv']
        species = ['i']
        for spc in species:
            for rotation in rotations:
                mms_part_slice2d(time=time, probe='1', species=spc, data_rate='brst', rotation=rotation, save_png='test_fpi_brst_' + spc + '_' + rotation, display=False)

    def test_fpi_subtract_bulk(self):
        time = '2015-10-16/13:06:30'
        mms_part_slice2d(time=time, probe='1', species='i', data_rate='brst', rotation='xy',
                         interpolation='2d', save_png='test_fpi_brst_subtract_bulk',
                         subtract_bulk=True, display=False)

    def test_fpi_avg_angle(self):
        time = '2015-10-16/13:06:30'
        mms_part_slice2d(time=time, probe='1', species='i', data_rate='brst', rotation='xy',
                         interpolation='geometric', save_png='test_fpi_brst_avg_angle',
                         average_angle=[-45, 45], display=False)

    def test_fpi_sum_angle(self):
        time = '2015-10-16/13:06:30'
        mms_part_slice2d(time=time, probe='1', species='i', data_rate='brst', rotation='xy',
                         interpolation='geometric', save_png='test_fpi_brst_sum_angle',
                         sum_angle=[-45, 45], display=False)

    def test_fpi_energy(self):
        time = '2015-10-16/13:06:30'
        mms_part_slice2d(time=time, probe='1', species='i', data_rate='brst', rotation='xy',
                         interpolation='geometric', save_png='test_fpi_brst_energy',
                         energy=True, display=False)

    def test_fpi_samples(self):
        time = '2015-10-16/13:06:30'
        mms_part_slice2d(time=time, probe='1', species='i', data_rate='brst', rotation='xy',
                         interpolation='geometric', save_png='test_fpi_brst_samples',
                         samples=3, display=False)

    def test_fpi_window(self):
        time = '2015-10-16/13:06:30'
        mms_part_slice2d(time=time, probe='1', species='i', data_rate='brst', rotation='xy',
                         interpolation='geometric', save_png='test_fpi_brst_window',
                         window=3, display=False)

    def test_fpi_window_center(self):
        time = '2015-10-16/13:06:30'
        mms_part_slice2d(time=time, probe='1', species='i', data_rate='brst', rotation='xy',
                         interpolation='geometric', save_png='test_fpi_brst_window_center',
                         window=3, center_time=True, display=False)

    def test_fpi_custom_rotation(self):
        rot = np.zeros((3, 3))
        rot[:, 0] = [0.33796266 , -0.082956984 , 0.93749634]
        rot[:, 1] = [0.64217210 , -0.70788234 , -0.29413872]
        rot[:, 2] = [0.68803796 , 0.70144189 , -0.18596514]

        time = '2015-10-16/13:06:30'
        mms_part_slice2d(time=time, probe='1', species='i', data_rate='brst', rotation='xy',
                         interpolation='geometric', save_png='test_fpi_brst_custom_rotation',
                         custom_rotation=rot, display=False)

    def test_fpi_2d_interp(self):
        time = '2015-10-16/13:06:30'
        mms_part_slice2d(time=time, probe='1', species='i', data_rate='brst', rotation='xy',
                         interpolation='2d', save_png='test_fpi_brst_2d_interp', display=False)

    def test_fpi_2d_interp_zdirrange(self):
        time = '2015-10-16/13:06:30'
        mms_part_slice2d(time=time, probe='1', species='i', data_rate='brst', rotation='xy',
                         interpolation='2d', save_png='test_fpi_brst_zdirrange', display=False,
                         zdirrange=[0, 2500])

    def test_fpi_limits(self):
        time = '2015-10-16/13:06:30'
        mms_part_slice2d(time=time, probe='1', species='i', data_rate='brst', rotation='xy', erange=[0, 10000],
                         save_png='test_fpi_brst_erange', display=False)

    def test_fpi_electrons(self):
        time = '2015-10-16/13:06:30'
        mms_part_slice2d(time=time, probe='1', species='e', data_rate='brst', rotation='xy',
                         save_png='test_fpi_brst_electrons', display=False)

    def test_hpca(self):
        time = '2015-10-16/13:06:30'
        mms_part_slice2d(time=time, probe='1', species='hplus', instrument='hpca', data_rate='brst', rotation='xy',
                         save_png='test_hpca_brst', display=False)

    def test_hpca_trange(self):
        trange = ['2015-10-16/13:06:20', '2015-10-16/13:06:40']
        mms_part_slice2d(trange=trange, probe='1', species='hplus', instrument='hpca', data_rate='brst', rotation='xy',
                         save_png='test_hpca_brst_trange', display=False)

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
