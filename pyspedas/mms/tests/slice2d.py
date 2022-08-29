import unittest
from pyspedas.mms.particles.mms_part_slice2d import mms_part_slice2d


class SliceTests(unittest.TestCase):
    def test_fpi_brst_rotations(self):
        time = '2015-10-16/13:06:30'
        rotations = ['xy', 'xz', 'bv', 'be', 'xvel', 'perp', 'perp_xy', 'perp_xz', 'perp_yz', 'b_exb', 'perp1-perp2']
        species = ['i', 'e']
        for spc in species:
            for rotation in rotations:
                mms_part_slice2d(time=time, probe='1', species=spc, data_rate='brst', rotation=rotation, save_png='test_fpi_brst_' + spc + '_' + rotation, display=False)


if __name__ == '__main__':
    unittest.main()
