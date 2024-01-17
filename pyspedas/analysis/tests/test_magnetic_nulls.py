
import unittest
import pyspedas
from pytplot import data_exists, tplot

class MagNullTestCases(unittest.TestCase):


    def test_find_magnetic_nulls_fote_mms(self):
        from pytplot import tplot
        data = pyspedas.mms.fgm(probe=[1, 2, 3, 4], trange=['2015-09-19/07:40', '2015-09-19/07:45'], data_rate='srvy', time_clip=True, varformat='*_gse_*', get_fgm_ephemeris=True)
        fields = ['mms'+prb+'_fgm_b_gse_srvy_l2' for prb in ['1', '2', '3', '4']]
        positions = ['mms'+prb+'_fgm_r_gse_srvy_l2' for prb in ['1', '2', '3', '4']]
        #tplot(fields)
        null_vars = pyspedas.find_magnetic_nulls_fote(fields=fields, positions=positions, smooth_fields=True,smooth_npts=10,smooth_median=True)
        tplot(null_vars)

    def test_find_magnetic_nulls_fote_cluster(self):
        from pytplot import tplot, tplot_names
        #data = pyspedas.cluster.fgm(probe=[1, 2, 3, 4], trange=['2003-08-17/16:40', '2003-08-17/16:45'], time_clip=True)
        data = pyspedas.cluster.load_csa(probes=['C1','C2','C3','C4'],trange=['2003-08-17/16:40', '2003-08-17/16:45'],datatypes='CP_FGM_FULL', time_clip=True)
        #tplot_names()
        fields = ['B_vec_xyz_gse__C'+prb+'_CP_FGM_FULL' for prb in ['1', '2', '3', '4']]
        positions = ['sc_pos_xyz_gse__C'+prb+'_CP_FGM_FULL' for prb in ['1', '2', '3', '4']]
        #tplot(fields)
        #tplot(positions)
        null_vars = pyspedas.find_magnetic_nulls_fote(fields=fields, positions=positions, smooth_fields=True)
        tplot(null_vars)


if __name__ == '__main__':
    unittest.main()