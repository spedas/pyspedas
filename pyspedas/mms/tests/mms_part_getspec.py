import unittest
from pyspedas.mms.particles.mms_part_getspec import mms_part_getspec
from ...utilities.data_exists import data_exists


class PGSTests(unittest.TestCase):
    def test_fpi_brst_fac_type(self):
        mms_part_getspec(trange=['2015-10-16/13:06:00', '2015-10-16/13:06:10'],
                         data_rate='brst',
                         species='i',
                         fac_type='phigeo',
                         output='pa gyro moments')
        self.assertTrue(data_exists('mms1_dis_dist_brst_density'))
        mms_part_getspec(trange=['2015-10-16/13:06:00', '2015-10-16/13:06:10'],
                         data_rate='brst',
                         species='i',
                         fac_type='xgse',
                         output='pa gyro moments')
        self.assertTrue(data_exists('mms1_dis_dist_brst_density'))

    def test_fpi_brst_i(self):
        mms_part_getspec(trange=['2015-10-16/13:06:00', '2015-10-16/13:06:10'],
                         data_rate='brst',
                         species='i',
                         output='energy theta phi pa gyro moments')
        self.assertTrue(data_exists('mms1_dis_dist_brst_density'))
        self.assertTrue(data_exists('mms1_dis_dist_brst_velocity'))
        self.assertTrue(data_exists('mms1_dis_dist_brst_avgtemp'))
        self.assertTrue(data_exists('mms1_dis_dist_brst_energy'))
        self.assertTrue(data_exists('mms1_dis_dist_brst_theta'))
        self.assertTrue(data_exists('mms1_dis_dist_brst_phi'))
        self.assertTrue(data_exists('mms1_dis_dist_brst_pa'))
        self.assertTrue(data_exists('mms1_dis_dist_brst_gyro'))

    def test_fpi_disable_pe_corr(self):
        mms_part_getspec(trange=['2015-10-16/13:06:07', '2015-10-16/13:06:08'],
                         data_rate='brst',
                         species='e',
                         output='energy',
                         disable_photoelectron_corrections=True)
        self.assertTrue(data_exists('mms1_des_dist_brst_energy'))

    def test_fpi_brst_e(self):
        mms_part_getspec(trange=['2015-10-16/13:06:07', '2015-10-16/13:06:08'],
                         data_rate='brst',
                         species='e',
                         output='energy theta phi pa gyro moments')
        self.assertTrue(data_exists('mms1_des_dist_brst_density'))
        self.assertTrue(data_exists('mms1_des_dist_brst_velocity'))
        self.assertTrue(data_exists('mms1_des_dist_brst_avgtemp'))
        self.assertTrue(data_exists('mms1_des_dist_brst_energy'))
        self.assertTrue(data_exists('mms1_des_dist_brst_theta'))
        self.assertTrue(data_exists('mms1_des_dist_brst_phi'))
        self.assertTrue(data_exists('mms1_des_dist_brst_pa'))
        self.assertTrue(data_exists('mms1_des_dist_brst_gyro'))

    def test_fpi_brst_limits(self):
        mms_part_getspec(trange=['2015-10-16/13:06:07', '2015-10-16/13:06:08'],
                         data_rate='brst',
                         species='e',
                         theta=[0, 90],
                         phi=[0, 100],
                         gyro=[0, 180],
                         pitch=[45, 75],
                         energy=[1000, 20000],
                         output='energy theta phi pa gyro moments')
        self.assertTrue(data_exists('mms1_des_dist_brst_density'))
        self.assertTrue(data_exists('mms1_des_dist_brst_velocity'))
        self.assertTrue(data_exists('mms1_des_dist_brst_avgtemp'))
        self.assertTrue(data_exists('mms1_des_dist_brst_energy'))
        self.assertTrue(data_exists('mms1_des_dist_brst_theta'))
        self.assertTrue(data_exists('mms1_des_dist_brst_phi'))
        self.assertTrue(data_exists('mms1_des_dist_brst_pa'))
        self.assertTrue(data_exists('mms1_des_dist_brst_gyro'))

    def test_hpca_srvy_hplus(self):
        mms_part_getspec(trange=['2015-10-16/13:05', '2015-10-16/13:10'],
                         #data_rate='brst',
                         species='hplus',
                         instrument='hpca',
                         output='energy theta phi pa gyro moments')
        self.assertTrue(data_exists('mms1_hpca_hplus_phase_space_density_density'))
        self.assertTrue(data_exists('mms1_hpca_hplus_phase_space_density_velocity'))
        self.assertTrue(data_exists('mms1_hpca_hplus_phase_space_density_avgtemp'))
        self.assertTrue(data_exists('mms1_hpca_hplus_phase_space_density_energy'))
        self.assertTrue(data_exists('mms1_hpca_hplus_phase_space_density_theta'))
        self.assertTrue(data_exists('mms1_hpca_hplus_phase_space_density_phi'))
        self.assertTrue(data_exists('mms1_hpca_hplus_phase_space_density_pa'))
        self.assertTrue(data_exists('mms1_hpca_hplus_phase_space_density_gyro'))

    def test_hpca_srvy_oplus(self):
        mms_part_getspec(trange=['2015-10-16/13:05', '2015-10-16/13:10'],
                         species='oplus',
                         instrument='hpca',
                         output='energy')
        self.assertTrue(data_exists('mms1_hpca_oplus_phase_space_density_energy'))

    def test_hpca_srvy_heplus(self):
        mms_part_getspec(trange=['2015-10-16/13:05', '2015-10-16/13:10'],
                         species='heplus',
                         instrument='hpca',
                         output='energy')
        self.assertTrue(data_exists('mms1_hpca_heplus_phase_space_density_energy'))

    def test_hpca_srvy_heplusplus(self):
        mms_part_getspec(trange=['2015-10-16/13:05', '2015-10-16/13:10'],
                         species='heplusplus',
                         instrument='hpca',
                         output='energy')
        self.assertTrue(data_exists('mms1_hpca_heplusplus_phase_space_density_energy'))


if __name__ == '__main__':
    unittest.main()
