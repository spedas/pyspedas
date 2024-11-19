
import unittest
import pyspedas
from pytplot import data_exists, tplot, get_data
import numpy as np

# Set this to False for Github CI testing, True to show the plots for interactive use
global_display=False

class MagNullTestCases(unittest.TestCase):


    def test_null_classification_x(self):
        # Test direct detection of 2-D type X nulls. (This will seldom or never occur in practice,
        # but see below for some degenerate cases that do appear in real data.
        l1 = complex(0.0,0.0)
        l2 = complex(-0.5, 0.0)
        l3 = complex(0.5,0.0)
        lambdas = [l1,l2,l3]
        tc = pyspedas.classify_null_type(lambdas)
        self.assertEqual(tc,1)

    def test_null_classification_o(self):
        # Test direct detection of 2-D type O nulls.  Again, this is not expected in practice, except
        # for degenerate cases checked below.
        l1 = complex(0.0,0.0)
        l2 = complex(0.0, 1.0)
        l3 = complex(0.0,-1.0)
        lambdas = [l1,l2,l3]
        tc = pyspedas.classify_null_type(lambdas)
        self.assertEqual(tc,2)

    def test_null_classification_a(self):
        # Test for 3-D type A (radial) null
        l1 = complex(-.25,0.0)
        l2 = complex(-.25, 0.0)
        l3 = complex(0.5,0.0)
        lambdas = [l1,l2,l3]
        tc = pyspedas.classify_null_type(lambdas)
        self.assertEqual(tc,3)

    def test_null_classification_b(self):
        # Test for 3-D type B (radial) null
        l1 = complex(.25,0.0)
        l2 = complex(.25, 0.0)
        l3 = complex(-0.5,0.0)
        lambdas = [l1,l2,l3]
        tc = pyspedas.classify_null_type(lambdas)
        self.assertEqual(tc,4)


    def test_null_classification_as(self):
        # Test for 3-D type A_s (spiral) null
        l1 = complex(0.5,0.0)
        l2 = complex(-0.25, 0.25)
        l3 = complex(-0.25,-0.25)
        lambdas = [l1,l2,l3]
        tc = pyspedas.classify_null_type(lambdas)
        self.assertEqual(tc,5)


    def test_null_classification_bs(self):
        # Test for 3-D type B_s (spiral) null
        l1 = complex(-0.5,0.0)
        l2 = complex(0.25, 0.25)
        l3 = complex(0.25,-0.25)
        lambdas = [l1,l2,l3]
        tc = pyspedas.classify_null_type(lambdas)
        self.assertEqual(tc,6)


    def test_null_classification_a_degen(self):
        # Test for type A null, degenerating to type X if the ratio of mim to max norm is < 0.25
        l1 = complex(-0.01,0.0)
        l2 = complex(-0.1, 0.0)
        l3 = complex(0.89,0.0)
        lambdas = [l1,l2,l3]
        tc = pyspedas.classify_null_type(lambdas)
        self.assertEqual(tc,7)


    def test_null_classification_b_degen(self):
        # Test for type B null, degenerating to type X if the ratio of min to max norm is < 0.25
        l1 = complex(0.01,0.0)
        l2 = complex(0.1, 0.0)
        l3 = complex(-0.89,0.0)
        lambdas = [l1,l2,l3]
        tc = pyspedas.classify_null_type(lambdas)
        self.assertEqual(tc,8)


    def test_null_classification_as_degen(self):
        # Test for type A_s null, degenerating to type O if the ratio of max(abs(real)) to min(abs(imag)) is < 0.25
        l1 = complex(0.1, 0.0)
        l2 = complex(-0.1, 0.5)
        l3 = complex(-0.1, -0.5)
        lambdas = [l1,l2,l3]
        tc = pyspedas.classify_null_type(lambdas)
        self.assertEqual(tc,9)


    def test_null_classification_bs_degen(self):
        # Test for type B_s null, degenerating to type O if the ratio of max(abs(real)) to min(abs(imag)) is < 0.25
        l1 = complex(-0.1,0.0)
        l2 = complex(-0.1, 0.5)
        l3 = complex(0.1,-0.5)
        lambdas = [l1,l2,l3]
        tc = pyspedas.classify_null_type(lambdas)
        self.assertEqual(tc,10)


    def test_find_magnetic_nulls_fote_mms(self):
        data = pyspedas.projects.mms.fgm(probe=[1, 2, 3, 4], trange=['2015-09-19/07:40', '2015-09-19/07:45'], data_rate='srvy', time_clip=True, varformat='*_gse_*', get_fgm_ephemeris=True)
        fields = ['mms'+prb+'_fgm_b_gse_srvy_l2' for prb in ['1', '2', '3', '4']]
        positions = ['mms'+prb+'_fgm_r_gse_srvy_l2' for prb in ['1', '2', '3', '4']]
        null_vars = pyspedas.find_magnetic_nulls_fote(fields=fields, positions=positions, smooth_fields=True,smooth_npts=10,smooth_median=True)
        tplot(null_vars,save_png='magnetic_null_vars',display=global_display)
        # We reconstruct the field vectors at the s/c positions using the Jacobian and the field value at the tetrahedron
        # barycenter.  The max difference between the observations and the reconstructed values for each time step
        # should be extremely close to zero, so that's what we'll use for our test.
        d=get_data('max_reconstruction_error')
        np.testing.assert_allclose(d.y,0.0,atol=1.0e-10)

    def test_find_magnetic_nulls_fote_cluster(self):
        data = pyspedas.projects.cluster.load_csa(probes=['C1','C2','C3','C4'],trange=['2003-08-17/16:40', '2003-08-17/16:45'],datatypes='CP_FGM_FULL', time_clip=True)
        #tplot_names()
        fields = ['B_vec_xyz_gse__C'+prb+'_CP_FGM_FULL' for prb in ['1', '2', '3', '4']]
        positions = ['sc_pos_xyz_gse__C'+prb+'_CP_FGM_FULL' for prb in ['1', '2', '3', '4']]
        null_vars = pyspedas.find_magnetic_nulls_fote(fields=fields, positions=positions, smooth_fields=True)
        tplot(null_vars,display=global_display,save_png='cluster_null_vars')
        d=get_data('max_reconstruction_error')
        np.testing.assert_allclose(d.y,0.0,atol=1.0e-10)




if __name__ == '__main__':
    unittest.main()