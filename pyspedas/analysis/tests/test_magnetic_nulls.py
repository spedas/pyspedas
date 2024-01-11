
import unittest
import pyspedas
from pytplot import data_exists, tplot

class MagNullTestCases(unittest.TestCase):


    def test_find_magnetic_nulls_fote_mms(self):
        from pytplot import tplot
        data = pyspedas.mms.fgm(probe=[1, 2, 3, 4], trange=['2015-09-19/07:40', '2015-09-19/07:45'], data_rate='srvy', time_clip=True, varformat='*_gse_*', get_fgm_ephemeris=True)
        fields = ['mms'+prb+'_fgm_b_gse_srvy_l2' for prb in ['1', '2', '3', '4']]
        positions = ['mms'+prb+'_fgm_r_gse_srvy_l2' for prb in ['1', '2', '3', '4']]
        tplot(fields)
        curl = pyspedas.find_magnetic_nulls_fote(fields=fields, positions=positions)
        tplot('magnull_null_bary_dist')


if __name__ == '__main__':
    unittest.main()