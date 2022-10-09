import unittest
import pyspedas
from pyspedas.utilities.data_exists import data_exists
from pyspedas.cotrans.fac_matrix_make import fac_matrix_make
from pyspedas import tinterpol
from pytplot import get_data, store_data
from pyspedas import twavpol


class WavpolTestCases(unittest.TestCase):
    def test_brst(self):
        """
        See the MMS wave polarization notebook for details/notes on these calculations
        """
        trange = ['2015-10-16/13:05:40', '2015-10-16/13:07:25']  # Burch et al., Science event
        sc = '4'
        scm_data_rate = 'brst'
        scm_datatype = 'scb'
        pyspedas.mms.scm(probe=sc, datatype=scm_datatype, level='l2', trange=trange, data_rate=scm_data_rate)
        mms_scm_name = 'mms' + sc + '_scm_acb_gse_' + scm_datatype + '_' + scm_data_rate + '_l2'
        fgm_data_rate = 'srvy'
        pyspedas.mms.fgm(probe=sc, trange=trange, data_rate=fgm_data_rate)
        mms_fgm_name = 'mms' + sc + '_fgm_b_gse_' + fgm_data_rate + '_l2_bvec'
        fac_matrix_make(mms_fgm_name, other_dim='xgse', newname=mms_fgm_name + '_fac_mat')
        tinterpol('mms4_fgm_b_gse_srvy_l2_bvec_fac_mat', mms_scm_name)
        fac_mat = get_data('mms4_fgm_b_gse_srvy_l2_bvec_fac_mat-itrp')
        scm_data = get_data(mms_scm_name, dt=True)
        scm_fac = [fac_mat.y[idx, :, :] @ scm_data.y[idx, :] for idx in range(0, len(scm_data.y[:, 0]))]
        store_data(mms_scm_name + '_fac', data={'x': scm_data.times, 'y': scm_fac})
        # number of points for FFT
        nopfft_input = 8192  # 1024
        # number of points for shifting between 2 FFT
        steplength_input = nopfft_input / 2
        # number of bins for frequency averaging
        bin_freq_input = 3
        twavpol(mms_scm_name + '_fac', nopfft=nopfft_input, steplength=steplength_input, bin_freq=bin_freq_input)
        self.assertTrue(data_exists(mms_scm_name + '_fac'))
        self.assertTrue(data_exists('mms4_scm_acb_gse_scb_brst_l2_fac_powspec'))
        self.assertTrue(data_exists('mms4_scm_acb_gse_scb_brst_l2_fac_degpol'))
        self.assertTrue(data_exists('mms4_scm_acb_gse_scb_brst_l2_fac_waveangle'))
        self.assertTrue(data_exists('mms4_scm_acb_gse_scb_brst_l2_fac_elliptict'))
        self.assertTrue(data_exists('mms4_scm_acb_gse_scb_brst_l2_fac_helict'))


if __name__ == '__main__':
    unittest.main()
