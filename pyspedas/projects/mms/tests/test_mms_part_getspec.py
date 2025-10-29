import unittest
import numpy as np
from pyspedas.projects.mms.particles.mms_part_getspec import mms_part_getspec
from pyspedas.tplot_tools import data_exists, get_data, tplot_names, tplot, get_coords, get_units

global_display=True

class PGSTests(unittest.TestCase):
    def test_pgs_errors(self):
        # no trange specified
        mms_part_getspec()
        # unsupported instrument
        mms_part_getspec(trange=['2015-10-16/13:06:00', '2015-10-16/13:06:10'], instrument='feeps')

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
                         output='energy theta phi pa gyro moments',
                         prefix='pre_')
        self.assertTrue(data_exists('pre_mms1_dis_dist_brst_density'))
        self.assertTrue(data_exists('pre_mms1_dis_dist_brst_velocity'))
        self.assertTrue(data_exists('pre_mms1_dis_dist_brst_avgtemp'))
        self.assertTrue(data_exists('pre_mms1_dis_dist_brst_energy'))
        self.assertTrue(data_exists('pre_mms1_dis_dist_brst_theta'))
        self.assertTrue(data_exists('pre_mms1_dis_dist_brst_phi'))
        self.assertTrue(data_exists('pre_mms1_dis_dist_brst_pa'))
        self.assertTrue(data_exists('pre_mms1_dis_dist_brst_gyro'))

    def test_fpi_mom_metadata(self):
        # Check coordinate systems and units for moments data, with and without sdc_units flag
        mms_part_getspec(trange=['2015-10-16/13:06:00', '2015-10-16/13:06:10'],
                         data_rate='brst',
                         species='i',
                         output='moments',
                         prefix='pre_',
                         )
        mms_part_getspec(trange=['2015-10-16/13:06:00', '2015-10-16/13:06:10'],
                         data_rate='brst',
                         species='i',
                         output='moments',
                         prefix='pre_',
                         suffix='_sdc_units',
                         sdc_units=True)

        self.assertTrue(data_exists('pre_mms1_dis_dist_brst_qflux'))
        self.assertTrue(data_exists('pre_mms1_dis_dist_brst_ptens'))
        self.assertTrue(data_exists('pre_mms1_dis_dist_brst_qflux_sdc_units'))
        self.assertTrue(data_exists('pre_mms1_dis_dist_brst_ptens_sdc_units'))

        tplot(['pre_mms1_dis_dist_brst_qflux','pre_mms1_dis_dist_brst_ptens',
               'pre_mms1_dis_dist_brst_qflux_sdc_units','pre_mms1_dis_dist_brst_ptens_sdc_units'])

        self.assertEqual(get_coords('pre_mms1_dis_dist_brst_qflux').lower(), 'dbcs')
        self.assertEqual(get_units('pre_mms1_dis_dist_brst_qflux'), 'eV/(cm^2-s)')
        self.assertEqual(get_coords('pre_mms1_dis_dist_brst_ptens').lower(), 'dbcs')
        self.assertEqual(get_units('pre_mms1_dis_dist_brst_ptens'), 'eV/cm^3')

        self.assertEqual(get_units('pre_mms1_dis_dist_brst_qflux_sdc_units'), 'mW/m^2')
        self.assertEqual(get_units('pre_mms1_dis_dist_brst_ptens_sdc_units'), 'nPa')

        # Check order of magnitude of qflux and ptens outputs, with/without the sdc_units flag,
        # to make sure the values were actually converted and not just the metadata updated.

        qfdat_std = get_data('pre_mms1_dis_dist_brst_qflux')
        qfdat_sdc = get_data('pre_mms1_dis_dist_brst_qflux_sdc_units')
        ptdat_std = get_data('pre_mms1_dis_dist_brst_ptens')
        ptdat_sdc = get_data('pre_mms1_dis_dist_brst_ptens_sdc_units')

        qfdat_std_max = np.abs(np.max(qfdat_std.y))
        qfdat_sdc_max = np.abs(np.max(qfdat_sdc.y))
        ptdat_std_max = np.abs(np.max(ptdat_std.y))
        ptdat_sdc_max = np.abs(np.max(ptdat_sdc.y))

        self.assertTrue(qfdat_std_max > 5.0e10)
        self.assertTrue(ptdat_std_max > 4000)
        self.assertTrue(qfdat_sdc_max < 1.0)
        self.assertTrue(ptdat_sdc_max < 1.0)

    def test_fpi_disable_pe_corr(self):
        mms_part_getspec(trange=['2015-10-16/13:06:07', '2015-10-16/13:06:08'],
                         data_rate='brst',
                         species='e',
                         output='energy',
                         disable_photoelectron_corrections=True,
                         prefix=None,
                         suffix=None)
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
        self.assertTrue(data_exists('mms1_des_dist_brst_fac_density'))
        self.assertTrue(data_exists('mms1_des_dist_brst_fac_velocity'))
        self.assertTrue(data_exists('mms1_des_dist_brst_fac_avgtemp'))
        self.assertTrue(data_exists('mms1_des_dist_brst_fac_energy'))
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

    def test_pitch_angle_limits(self):
        # Regression test for application of pitch angle limits to energy spectra
        # Previously, energy spectra were always computed in standard coordinates,
        # so any pitch angle or gyro limits were ignored.  Now, if 'energy' or 'moments'
        # are requested, and non-default pitch or gyro limits are specified, the outputs are
        # changed to 'fac_energy' or 'fac_moments', and pitch and gyro limits are applied.
        # Note that this changes the energy and moment output variable names!  (They will
        # now have a '_fac_' infix.  JWL 2024-08-15

        trange = ['2023-10-20/08:15:00', '2023-10-20/08:15:15']
        pitch_ranges = [[0, 30], [60, 120], [150, 180]]

        pitch_range = pitch_ranges[0]
        mms_part_getspec(trange=trange, instrument='fpi', data_rate='fast', probe=1, species='e', pitch=pitch_range,
                         output='energy', suffix='_pa_0_30')
        self.assertTrue(data_exists('mms1_des_dist_fast_fac_energy_pa_0_30'))
        data0 = get_data('mms1_des_dist_fast_fac_energy_pa_0_30')

        pitch_range = pitch_ranges[1]
        mms_part_getspec(trange=trange, instrument='fpi', data_rate='fast', probe=1, species='e', pitch=pitch_range,
                         output='energy', suffix='_pa_60_120')
        self.assertTrue(data_exists('mms1_des_dist_fast_fac_energy_pa_60_120'))
        data1 = get_data('mms1_des_dist_fast_fac_energy_pa_60_120')
        tplot(['mms1_des_dist_fast_fac_energy_pa_0_30', 'mms1_des_dist_fast_fac_energy_pa_60_120'], display=global_display, save_png='energy_pitch_limits.png')

        # Check that the pitch angle limits were actually applied
        delta = np.max(np.abs(data1.y - data0.y))
        self.assertTrue(delta > 0.0)

if __name__ == '__main__':
    unittest.main()
