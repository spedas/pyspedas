
import os
import unittest
import pyspedas
from pytplot import del_data, data_exists, time_double, get_data


class LoadTestCases(unittest.TestCase):
    def test_downloadonly(self):
        mag_files = pyspedas.projects.barrel.sspc(probe='1A', downloadonly=True)
        self.assertTrue(os.path.exists(mag_files[0]))

    def test_sspc(self):
        del_data("*")
        sspc_vars = pyspedas.projects.barrel.sspc(probe='1A')
        self.assertTrue(len(sspc_vars) > 0)
        self.assertTrue('brl1A_SSPC' in sspc_vars)
        self.assertTrue(data_exists('brl1A_SSPC'))

    def test_sspc_time_clip(self):
        del_data("*")
        trange = ['2013-01-29 09:00', '2013-01-29 12:00']
        sspc_vars = pyspedas.projects.barrel.sspc(probe='1A',trange=trange,time_clip=True)
        self.assertTrue(len(sspc_vars) > 0)
        self.assertTrue('brl1A_SSPC' in sspc_vars)
        self.assertTrue(data_exists('brl1A_SSPC'))
        dat=get_data('brl1A_SSPC')
        trange_double=time_double(trange)
        self.assertTrue(dat.times[0] >= trange_double[0])
        self.assertTrue(dat.times[-1] <= trange_double[1])

    def test_mspc(self):
        del_data("*")
        mspc_vars = pyspedas.projects.barrel.mspc(probe='1A')
        self.assertTrue(len(mspc_vars) > 0)
        self.assertTrue('brl1A_MSPC' in mspc_vars)
        self.assertTrue(data_exists('brl1A_MSPC'))

    def test_fspc(self):
        del_data("*")
        fspc_vars = pyspedas.projects.barrel.fspc(probe='1A')
        self.assertTrue(len(fspc_vars) > 0)
        self.assertTrue('brl1A_FSPC1' in fspc_vars)
        self.assertTrue(data_exists('brl1A_FSPC1'))

    def test_rcnt(self):
        del_data("*")
        rcnt_vars = pyspedas.projects.barrel.rcnt(probe='1A')
        self.assertTrue(len(rcnt_vars) > 0)
        self.assertTrue('brl1A_PeakDet' in rcnt_vars)
        self.assertTrue(data_exists('brl1A_PeakDet'))

    def test_magn(self):
        del_data("*")
        magn_vars = pyspedas.projects.barrel.magn(probe='1A')
        self.assertTrue(len(magn_vars) > 0)
        self.assertTrue('brl1A_MAG_X_uncalibrated' in magn_vars)
        self.assertTrue(data_exists('brl1A_MAG_X_uncalibrated'))

    def test_magn_prefix_none(self):
        del_data("*")
        magn_vars = pyspedas.projects.barrel.magn(probe='1A', prefix=None)
        self.assertTrue(len(magn_vars) > 0)
        self.assertTrue('brl1A_MAG_X_uncalibrated' in magn_vars)
        self.assertTrue(data_exists('brl1A_MAG_X_uncalibrated'))

    def test_magn_suffix_none(self):
        del_data("*")
        magn_vars = pyspedas.projects.barrel.magn(probe='1A', suffix=None)
        self.assertTrue(len(magn_vars) > 0)
        self.assertTrue('brl1A_MAG_X_uncalibrated' in magn_vars)
        self.assertTrue(data_exists('brl1A_MAG_X_uncalibrated'))

    def test_magn_prefix_suffix(self):
        del_data("*")
        magn_vars = pyspedas.projects.barrel.magn(probe='1A', prefix='pre_', suffix='_suf')
        self.assertTrue(len(magn_vars) > 0)
        self.assertTrue('pre_brl1A_MAG_X_uncalibrated_suf' in magn_vars)
        self.assertTrue(data_exists('pre_brl1A_MAG_X_uncalibrated_suf'))

    def test_ephm(self):
        del_data("*")
        ephm_vars = pyspedas.projects.barrel.ephm(probe='1A')
        self.assertTrue('brl1A_GPS_Lat' in ephm_vars)
        self.assertTrue(data_exists('brl1A_GPS_Lat'))

    def test_hkpg(self):
        del_data("*")
        hkpg_vars = pyspedas.projects.barrel.hkpg(probe='1A')
        self.assertTrue(len(hkpg_vars) > 0)
        self.assertTrue('brl1A_V0_VoltAtLoad' in hkpg_vars)
        self.assertTrue(data_exists('brl1A_V0_VoltAtLoad'))


if __name__ == '__main__':
    unittest.main()
