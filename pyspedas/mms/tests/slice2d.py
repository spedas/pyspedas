import unittest
from pyspedas.mms.particles.mms_part_slice2d import mms_part_slice2d


class SliceTests(unittest.TestCase):
    def test_fpi_brst_ion_xy(self):
        tr = ['2015-10-16/13:06:30', '2015-10-16/13:06:35']
        mms_part_slice2d(trange=tr, probe='1', species='i', data_rate='brst', rotation='xy', save_png='test_fpi_brst_ion_xy', display=False)

    def test_fpi_brst_ion_xz(self):
        tr = ['2015-10-16/13:06:30', '2015-10-16/13:06:35']
        mms_part_slice2d(trange=tr, probe='1', species='i', data_rate='brst', rotation='xz', save_png='test_fpi_brst_ion_xz', display=False)


if __name__ == '__main__':
    unittest.main()
