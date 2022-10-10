import pyspedas
import unittest

from pyspedas.utilities.data_exists import data_exists
from pyspedas.mms.fpi.mms_fpi_split_tensor import mms_fpi_split_tensor
from pyspedas.mms.fpi.mms_fpi_ang_ang import mms_fpi_ang_ang
from pyspedas.mms.fpi.mms_get_fpi_dist import mms_get_fpi_dist
from pyspedas.mms.fpi.mms_pad_fpi import mms_pad_fpi


class FPITestCases(unittest.TestCase):
    def test_angle_angle(self):
        mms_fpi_ang_ang('2015-10-16/13:06:30', data_rate='brst', save_png='mms1_fpi_ang_ang_brst', display=False)
        mms_fpi_ang_ang('2015-10-16/13:06:30', save_jpeg='mms1_fpi_ang_ang', display=False)
        mms_fpi_ang_ang('2015-10-16/13:06:30', probe='4', save_svg='mms4_fpi_ang_ang', display=False)
        mms_fpi_ang_ang('2015-10-16/13:06:30', probe='4', save_eps='mms4_fpi_ang_ang_viridis', cmap='viridis', display=False)

    def test_pad(self):
        trange = ['2015-10-16/13:06:29', '2015-10-16/13:06:32']
        pyspedas.mms.fpi(trange=trange, data_rate='brst', datatype=['dis-dist', 'des-dist', 'dis-moms'], time_clip=True)
        pyspedas.mms.fgm(trange=trange, data_rate='brst')
        dists = mms_get_fpi_dist('mms1_dis_dist_brst')
        dists_e = mms_get_fpi_dist('mms1_des_dist_brst')
        pa_dist = mms_pad_fpi(dists, trange=trange, mag_data='mms1_fgm_b_gse_brst_l2_bvec')
        pa_dist = mms_pad_fpi(dists_e, trange=trange, mag_data='mms1_fgm_b_gse_brst_l2_bvec')
        pa_dist = mms_pad_fpi(dists, time='2015-10-16/13:06:30', units='eflux', mag_data='mms1_fgm_b_gse_brst_l2_bvec')
        pa_dist = mms_pad_fpi(dists,
                      subtract_bulk=True,
                      time='2015-10-16/13:06:30',
                      units='eflux',
                      mag_data='mms1_fgm_b_gse_brst_l2_bvec',
                      vel_data='mms1_dis_bulkv_gse_brst')

    def test_split_tensors(self):
        data = pyspedas.mms.fpi(trange=['2015-10-16/13:06', '2015-10-16/13:07'],
                                data_rate='brst',
                                datatype=['dis-moms', 'des-moms'])

        split_vars = mms_fpi_split_tensor('mms1_dis_temptensor_gse_brst')

        components = ['xx', 'xy', 'xz', 'yx', 'yy', 'yz', 'zx', 'zy', 'zz']
        output = ['mms1_dis_temptensor_gse_brst_' + component for component in components]

        for v in output:
            self.assertTrue(data_exists(v))

        split_vars = mms_fpi_split_tensor('mms1_des_temptensor_gse_brst')

        components = ['xx', 'xy', 'xz', 'yx', 'yy', 'yz', 'zx', 'zy', 'zz']
        output = ['mms1_des_temptensor_gse_brst_' + component for component in components]

        for v in output:
            self.assertTrue(data_exists(v))


if __name__ == '__main__':
    unittest.main()
