import os
import unittest
from pytplot import data_exists
import pyspedas


class LoadTestCases(unittest.TestCase):
    def test_downloadonly(self):
        files = pyspedas.projects.polar.efi(downloadonly=True)
        self.assertTrue(os.path.exists(files[0]))

    def test_load_mfe_data(self):
        mfe_vars = pyspedas.projects.polar.mfe(trange=['2003-10-28', '2003-10-29'], get_support_data=True)
        self.assertTrue(data_exists('B_GSE'))
        self.assertTrue(data_exists('B_GSM'))
    
    def test_load_mfe_data_prefix_none(self):
        mfe_vars = pyspedas.projects.polar.mfe(trange=['2003-10-28', '2003-10-29'], get_support_data=True, prefix=None)
        self.assertTrue(data_exists('B_GSE'))
        self.assertTrue(data_exists('B_GSM'))

    def test_load_mfe_data_suffix_none(self):
        mfe_vars = pyspedas.projects.polar.mfe(trange=['2003-10-28', '2003-10-29'], get_support_data=True, suffix=None)
        self.assertTrue(data_exists('B_GSE'))
        self.assertTrue(data_exists('B_GSM'))
    
    def test_load_mfe_data_prefix_suffix(self):
        mfe_vars = pyspedas.projects.polar.mfe(trange=['2003-10-28', '2003-10-29'], get_support_data=True, prefix='pre_', suffix='_suf')
        self.assertTrue(data_exists('pre_B_GSE_suf'))
        self.assertTrue(data_exists('pre_B_GSM_suf'))

    def test_load_efi_data(self):
        efi_vars = pyspedas.projects.polar.efi(time_clip=True)
        self.assertTrue(data_exists('ESPIN'))

    def test_load_efi_data_prefix_none(self):
        efi_vars = pyspedas.projects.polar.efi(time_clip=True, prefix=None)
        self.assertTrue(data_exists('ESPIN'))

    def test_load_efi_data_suffix_none(self):
        efi_vars = pyspedas.projects.polar.efi(time_clip=True, suffix=None)
        self.assertTrue(data_exists('ESPIN'))

    def test_load_efi_data_prefix_suffix(self):
        efi_vars = pyspedas.projects.polar.efi(time_clip=True, prefix='pre_', suffix='_suf')
        self.assertTrue(data_exists('pre_ESPIN_suf'))

    def test_load_pwi_data(self):
        pwi_vars = pyspedas.projects.polar.pwi()
        self.assertTrue(data_exists('Fce'))

    def test_load_pwi_data_prefix_none(self):
        pwi_vars = pyspedas.projects.polar.pwi(prefix=None)
        self.assertTrue(data_exists('Fce'))

    def test_load_pwi_data_suffix_none(self):
        pwi_vars = pyspedas.projects.polar.pwi(suffix=None)
        self.assertTrue(data_exists('Fce'))

    def test_load_pwi_data_prefix_suffix(self):
        pwi_vars = pyspedas.projects.polar.pwi(prefix='pre_', suffix='_suf')
        self.assertTrue(data_exists('pre_Fce_suf'))

    def test_load_hydra_data(self):
        hydra_vars = pyspedas.projects.polar.hydra()
        self.assertTrue(data_exists('ELE_DENSITY'))
    
    def test_load_hydra_data_prefix_none(self):
        hydra_vars = pyspedas.projects.polar.hydra(prefix=None)
        self.assertTrue(data_exists('ELE_DENSITY'))

    def test_load_hydra_data_suffix_none(self):
        hydra_vars = pyspedas.projects.polar.hydra(suffix=None)
        self.assertTrue(data_exists('ELE_DENSITY'))

    def test_load_hydra_data_prefix_suffix(self):
        hydra_vars = pyspedas.projects.polar.hydra(prefix='pre_', suffix='_suf')
        self.assertTrue(data_exists('pre_ELE_DENSITY_suf'))

    def test_load_tide_data(self):
        tide_vars = pyspedas.projects.polar.tide()
        self.assertTrue(data_exists('total_den'))
        self.assertTrue(data_exists('total_v'))
        self.assertTrue(data_exists('total_t'))
    
    def test_load_tide_data_prefix_none(self):
        tide_vars = pyspedas.projects.polar.tide(prefix=None)
        self.assertTrue(data_exists('total_den'))
        self.assertTrue(data_exists('total_v'))
        self.assertTrue(data_exists('total_t'))

    def test_load_tide_data_suffix_none(self):
        tide_vars = pyspedas.projects.polar.tide(suffix=None)
        self.assertTrue(data_exists('total_den'))
        self.assertTrue(data_exists('total_v'))
        self.assertTrue(data_exists('total_t'))

    def test_load_tide_data_prefix_suffix(self):
        tide_vars = pyspedas.projects.polar.tide(prefix='pre_', suffix='_suf')
        self.assertTrue(data_exists('pre_total_den_suf'))
        self.assertTrue(data_exists('pre_total_v_suf'))
        self.assertTrue(data_exists('pre_total_t_suf'))

    def test_load_timas_data(self):
        timas_vars = pyspedas.projects.polar.timas()
        self.assertTrue(data_exists('Density_H'))
    
    def test_load_timas_data_prefix_none(self):
        timas_vars = pyspedas.projects.polar.timas(prefix=None)
        self.assertTrue(data_exists('Density_H'))

    def test_load_timas_data_suffix_none(self):
        timas_vars = pyspedas.projects.polar.timas(suffix=None)
        self.assertTrue(data_exists('Density_H'))

    def test_load_timas_data_prefix_suffix(self):
        timas_vars = pyspedas.projects.polar.timas(prefix='pre_', suffix='_suf')
        self.assertTrue(data_exists('pre_Density_H_suf'))

    def test_load_cammice_data(self):
        cammice_vars = pyspedas.projects.polar.cammice()
        self.assertTrue(data_exists('Protons'))
    
    def test_load_cammice_data_prefix_none(self):
        cammice_vars = pyspedas.projects.polar.cammice(prefix=None)
        self.assertTrue(data_exists('Protons'))

    def test_load_cammice_data_suffix_none(self):
        cammice_vars = pyspedas.projects.polar.cammice(suffix=None)
        self.assertTrue(data_exists('Protons'))

    def test_load_cammice_data_prefix_suffix(self):
        cammice_vars = pyspedas.projects.polar.cammice(prefix='pre_', suffix='_suf')
        self.assertTrue(data_exists('pre_Protons_suf'))

    def test_load_ceppad_data(self):
        ceppad_vars = pyspedas.projects.polar.ceppad()
        self.assertTrue(data_exists('IPS_10_ERR'))
    
    def test_load_ceppad_data_prefix_none(self):
        ceppad_vars = pyspedas.projects.polar.ceppad(prefix=None)
        self.assertTrue(data_exists('IPS_10_ERR'))

    def test_load_ceppad_data_suffix_none(self):
        ceppad_vars = pyspedas.projects.polar.ceppad(suffix=None)
        self.assertTrue(data_exists('IPS_10_ERR'))

    def test_load_ceppad_data_prefix_suffix(self):
        ceppad_vars = pyspedas.projects.polar.ceppad(prefix='pre_', suffix='_suf')
        self.assertTrue(data_exists('pre_IPS_10_ERR_suf'))

    def test_load_uvi_data(self):
        uvi_vars = pyspedas.projects.polar.uvi()
        self.assertTrue(data_exists('IMAGE_DATA'))

    def test_load_uvi_data_prefix_none(self):
        uvi_vars = pyspedas.projects.polar.uvi(prefix=None)
        self.assertTrue(data_exists('IMAGE_DATA'))

    def test_load_uvi_data_suffix_none(self):
        uvi_vars = pyspedas.projects.polar.uvi(suffix=None)
        self.assertTrue(data_exists('IMAGE_DATA'))

    def test_load_uvi_data_prefix_suffix(self):
        uvi_vars = pyspedas.projects.polar.uvi(prefix='pre_', suffix='_suf')
        self.assertTrue(data_exists('pre_IMAGE_DATA_suf'))

    def test_load_pixie_data(self):
        pixie_vars = pyspedas.projects.polar.pixie()
        self.assertTrue(data_exists('TXF_HIGH'))

    def test_load_pixie_data_prefix_none(self):
        pixie_vars = pyspedas.projects.polar.pixie(prefix=None)
        self.assertTrue(data_exists('TXF_HIGH'))

    def test_load_pixie_data_suffix_none(self):
        pixie_vars = pyspedas.projects.polar.pixie(suffix=None)
        self.assertTrue(data_exists('TXF_HIGH'))

    def test_load_pixie_data_prefix_suffix(self):
        pixie_vars = pyspedas.projects.polar.pixie(prefix='pre_', suffix='_suf')
        self.assertTrue(data_exists('pre_TXF_HIGH_suf'))

    def test_load_vis_data(self):
        vis_vars = pyspedas.projects.polar.vis(notplot=True)
        self.assertTrue('Image_Counts' in vis_vars)
    
    def test_load_vis_data_prefix_none(self):
        vis_vars = pyspedas.projects.polar.vis(prefix=None, notplot=True)
        self.assertTrue('Image_Counts' in vis_vars)

    def test_load_vis_data_suffix_none(self):
        vis_vars = pyspedas.projects.polar.vis(suffix=None, notplot=True)
        self.assertTrue('Image_Counts' in vis_vars)

    def test_load_vis_data_prefix_suffix(self):
        vis_vars = pyspedas.projects.polar.vis(prefix='pre_', suffix='_suf', notplot=True)
        self.assertTrue('pre_Image_Counts_suf' in vis_vars)

    def test_load_orbit_data(self):
        orbit_vars = pyspedas.projects.polar.orbit()
        self.assertTrue(data_exists('AVG_SPIN_RATE'))
        self.assertTrue(data_exists('SPIN_PHASE'))

    def test_load_orbit_data_prefix_none(self):
        orbit_vars = pyspedas.projects.polar.orbit(prefix=None)
        self.assertTrue(data_exists('AVG_SPIN_RATE'))
        self.assertTrue(data_exists('SPIN_PHASE'))

    def test_load_orbit_data_suffix_none(self):
        orbit_vars = pyspedas.projects.polar.orbit(suffix=None)
        self.assertTrue(data_exists('AVG_SPIN_RATE'))
        self.assertTrue(data_exists('SPIN_PHASE'))

    def test_load_orbit_data_prefix_suffix(self):
        orbit_vars = pyspedas.projects.polar.orbit(prefix='pre_', suffix='_suf')
        self.assertTrue(data_exists('pre_AVG_SPIN_RATE_suf'))
        self.assertTrue(data_exists('pre_SPIN_PHASE_suf'))


if __name__ == '__main__':
    unittest.main()
