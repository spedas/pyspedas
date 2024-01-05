import numpy as np
import pyspedas
from pyspedas import mms_load_fpi
import unittest

from pytplot import data_exists, get_data
from pyspedas.mms.fpi.mms_fpi_split_tensor import mms_fpi_split_tensor
from pyspedas.mms.fpi.mms_fpi_ang_ang import mms_fpi_ang_ang
from pyspedas.mms.fpi.mms_get_fpi_dist import mms_get_fpi_dist
from pyspedas.mms.fpi.mms_pad_fpi import mms_pad_fpi


class FPITestCases(unittest.TestCase):
    def test_load_default_data(self):
        data = mms_load_fpi(trange=['2015-10-16/14:00', '2015-10-16/15:00'], available=True)
        data = mms_load_fpi(trange=['2015-10-16/14:00', '2015-10-16/15:00'])
        self.assertTrue(data_exists('mms1_dis_energyspectr_omni_fast'))

    def test_load_spdf_data(self):
        data = mms_load_fpi(trange=['2015-10-16/14:00', '2015-10-16/15:00'], spdf=True)
        self.assertTrue(data_exists('mms1_dis_energyspectr_omni_fast'))

    def test_load_small_brst_interval(self):
        data = mms_load_fpi(trange=['2015-10-16/13:06', '2015-10-16/13:07'], data_rate='brst', datatype=['dis-moms', 'dis-dist'], time_clip=True)
        self.assertTrue(data_exists('mms1_dis_energyspectr_omni_brst'))

    def test_load_rename_bars(self):
        data = mms_load_fpi(trange=['2015-10-16/13:06', '2015-10-16/13:07'], data_rate='brst', datatype='des-dist')
        data = mms_load_fpi(trange=['2015-10-16/13:06', '2015-10-16/13:07'], data_rate='brst', datatype='dis-dist')
        data = mms_load_fpi(trange=['2015-10-16/13:06', '2015-10-16/13:07'], data_rate='brst', datatype='des-moms')
        data = mms_load_fpi(trange=['2015-10-16/13:06', '2015-10-16/13:07'], data_rate='brst', datatype='dis-moms')
        self.assertTrue(data_exists('mms1_dis_compressionloss_brst_moms'))
        self.assertTrue(data_exists('mms1_dis_errorflags_brst_moms'))
        self.assertTrue(data_exists('mms1_des_errorflags_brst_moms'))
        self.assertTrue(data_exists('mms1_des_compressionloss_brst_moms'))
        self.assertTrue(data_exists('mms1_des_errorflags_brst_dist'))
        self.assertTrue(data_exists('mms1_des_compressionloss_brst_dist'))
        self.assertTrue(data_exists('mms1_dis_errorflags_brst_dist'))
        self.assertTrue(data_exists('mms1_dis_compressionloss_brst_dist'))

    def test_center_fast_ion_data(self):
        data = mms_load_fpi(trange=['2015-10-16/14:00', '2015-10-16/15:00'])
        centered = mms_load_fpi(trange=['2015-10-16/14:00', '2015-10-16/15:00'], center_measurement=True, suffix='_centered')

        t, d = get_data('mms1_dis_bulkv_gse_fast')
        c, d = get_data('mms1_dis_bulkv_gse_fast_centered')
        self.assertTrue(np.round(c[0]-t[0], decimals=3) == 2.25)

    def test_center_fast_electron_data(self):
        data = mms_load_fpi(trange=['2015-10-16/14:00', '2015-10-16/15:00'])
        centered = mms_load_fpi(trange=['2015-10-16/14:00', '2015-10-16/15:00'], center_measurement=True, suffix='_centered')

        t, d = get_data('mms1_des_bulkv_gse_fast')
        c, d = get_data('mms1_des_bulkv_gse_fast_centered')
        self.assertTrue(np.round(c[0]-t[0], decimals=3) == 2.25)

    def test_center_brst_ion_data(self):
        data = mms_load_fpi(trange=['2015-10-16/13:06', '2015-10-16/13:07'], data_rate='brst')
        centered = mms_load_fpi(trange=['2015-10-16/13:06', '2015-10-16/13:07'], data_rate='brst', center_measurement=True, suffix='_centered')

        t, d = get_data('mms1_dis_bulkv_gse_brst')
        c, d = get_data('mms1_dis_bulkv_gse_brst_centered')
        self.assertTrue(np.round(c[0]-t[0], decimals=3) == 0.075)

    def test_center_brst_electron_data(self):
        data = mms_load_fpi(trange=['2015-10-16/13:06', '2015-10-16/13:07'], data_rate='brst')
        centered = mms_load_fpi(trange=['2015-10-16/13:06', '2015-10-16/13:07'], data_rate='brst', center_measurement=True, suffix='_centered')

        t, d = get_data('mms1_des_bulkv_gse_brst')
        c, d = get_data('mms1_des_bulkv_gse_brst_centered')
        self.assertTrue(np.round(c[0]-t[0], decimals=3) == 0.015)

    def test_errorflag_compression_bars(self):
        data = mms_load_fpi(trange=['2015-10-16/13:06', '2015-10-16/13:07'], data_rate='brst', datatype=['des-dist', 'des-moms'])
        data = mms_load_fpi(trange=['2015-10-16/13:06', '2015-10-16/13:07'], data_rate='brst', datatype=['dis-dist', 'dis-moms'])
        # mms_fpi_make_errorflagbars('mms1_des_errorflags_brst_moms', level='l2')
        # mms_fpi_make_errorflagbars('mms1_dis_errorflags_brst_moms', level='l2')
        # mms_fpi_make_errorflagbars('mms1_des_errorflags_brst_dist', level='l2')
        # mms_fpi_make_errorflagbars('mms1_dis_errorflags_brst_dist', level='l2')
        # mms_fpi_make_compressionlossbars('mms1_des_compressionloss_brst_moms')
        # mms_fpi_make_compressionlossbars('mms1_dis_compressionloss_brst_moms')
        # mms_fpi_make_compressionlossbars('mms1_des_compressionloss_brst_dist')
        # mms_fpi_make_compressionlossbars('mms1_dis_compressionloss_brst_dist')
        self.assertTrue(data_exists('mms1_des_errorflags_brst_moms_flagbars_full'))
        self.assertTrue(data_exists('mms1_des_errorflags_brst_moms_flagbars_main'))
        self.assertTrue(data_exists('mms1_des_errorflags_brst_moms_flagbars_mini'))
        self.assertTrue(data_exists('mms1_dis_errorflags_brst_moms_flagbars_full'))
        self.assertTrue(data_exists('mms1_dis_errorflags_brst_moms_flagbars_main'))
        self.assertTrue(data_exists('mms1_dis_errorflags_brst_moms_flagbars_mini'))
        self.assertTrue(data_exists('mms1_des_errorflags_brst_dist_flagbars_dist'))
        self.assertTrue(data_exists('mms1_dis_errorflags_brst_dist_flagbars_dist'))
        self.assertTrue(data_exists('mms1_des_compressionloss_brst_moms_flagbars'))
        self.assertTrue(data_exists('mms1_dis_compressionloss_brst_moms_flagbars'))
        self.assertTrue(data_exists('mms1_des_compressionloss_brst_dist_flagbars'))
        self.assertTrue(data_exists('mms1_dis_compressionloss_brst_dist_flagbars'))

    def test_angle_angle(self):
        mms_fpi_ang_ang('2015-10-16/13:06:59.985', species='e',data_rate='brst', save_png='mms1_fpi_ang_ang_brst', display=False)
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
