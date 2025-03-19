"""Test functions in the utilites folder."""
import unittest

import pyspedas
from pyspedas.utilities.dailynames import dailynames
from pyspedas import tcopy
from pyspedas import themis
from pyspedas import cotrans
from pyspedas import mpause_2, mpause_t96
from pyspedas import find_datasets
from pytplot import data_exists, tkm2re, tplot, split_vec, del_data
from pytplot import get_data, store_data, options
import numpy as np
from numpy.testing import assert_allclose


class UtilTestCases(unittest.TestCase):
    """Test fuctions in the utilites folder."""

    def test_dailynames(self):
        """Test dailynames function."""
        self.assertTrue(dailynames(trange=['2015-12-1', '2015-12-1/2:00'],
                                   hour_res=True) == ['2015120100',
                                                      '2015120101'])
        self.assertTrue(dailynames(trange=['2015-12-1', '2015-12-3'])
                        == ['20151201', '20151202'])
        self.assertTrue(dailynames(trange=['2015-12-3', '2015-12-2'])
                        == ['20151203'])
        self.assertTrue(dailynames() is None)
        self.assertTrue(dailynames(trange=['2015-12-3', '2019-12-2'],
                                   file_format='%Y') ==
                        ['2015', '2016', '2017', '2018', '2019'])
        self.assertTrue(dailynames(trange=['2015-1-1', '2015-3-2'],
                                   file_format='%Y%m') == ['201501', '201502',
                                                           '201503'])
        self.assertTrue(dailynames(trange=['2015-1-1', '2015-3-2'],
                                   file_format='/%Y/%m/') ==
                        ['/2015/01/', '/2015/02/', '/2015/03/'])
        self.assertTrue(dailynames(trange=['2015-1-1', '2015-1-1/3:00'],
                                   file_format='%H', res=60.0) ==
                        ['00', '01', '02'])
        self.assertTrue(dailynames(trange=['2015-1-1/2:00', '2015-1-1/3:00'],
                                   file_format='%M', res=600.) ==
                        ['00', '10', '20', '30', '40', '50'])

    def test_tcopy(self):
        """Test tcopy function."""
        store_data('test', data={'x': [1, 2, 3], 'y': [5, 5, 5]})
        tcopy('test')
        tcopy('test', 'another-copy')
        t, d = get_data('test-copy')
        self.assertTrue(t.tolist() == [1, 2, 3])
        self.assertTrue(d.tolist() == [5, 5, 5])
        t, d = get_data('another-copy')
        self.assertTrue(t.tolist() == [1, 2, 3])
        self.assertTrue(d.tolist() == [5, 5, 5])
        # the following should gracefully error
        tcopy('doesnt exist', 'another-copy')
        tcopy(['another-copy', 'test'], 'another-copy')

    def test_tkm2re(self):
        store_data('test', data={'x': [1, 2, 3], 'y': [5, 5, 5]})
        options('test', 'ysubtitle', '[Re]')
        # convert to km
        tkm2re('test', km=True)
        # convert back
        tkm2re('test_km')
        self.assertTrue(data_exists('test_km_re'))
        nothing = tkm2re('doesnt_exist')
        self.assertTrue(nothing is None)
        tkm2re('test_km', newname='another_test_km')
        self.assertTrue(data_exists('another_test_km'))
        anerror = tkm2re('test_km', newname=['test1_km', 'test1_km'])
        self.assertTrue(anerror is None)

    def test_time_clip(self):
        import pytplot
        x=[1,2,3,4,5]
        y=[2,4,6,8,10]
        xfp = [1.0,2.0,3.0,4.0,5.0]
        # Data for a scalar variable
        y_scalar = [0.0, 1.0, 2.0, 3.0, 4.0]
        # Data for a vector variable
        y_vec = [[0.0, 1.0, 2.0],[3.0,4.0,5.0],[6.0,7.0,8.0],[9.0,10.0,11.0],[12.0,13.0,14.0]]
        y_vec = np.array(y_vec)
        # Constant metadata for a vector variable
        v1_1d = [1.0, 2.0, 3.0]
        # Time varying metadata for a vector variable
        v1_2d = y_vec
        # Data for a 3x3 matrix variable
        y_mat = [[[0.0, 1.0, 2.0],    [0.0, 1.0, 2.0],  [0.0, 1.0, 2.0]],
                 [[3.0, 4.0, 5.0],    [3.0,4.0,5.0],    [3.0,4.0,5.0]],
                 [[6.0, 7.0, 8.0],    [6.0,7.0,8.0],    [6.0,7.0,8.0]],
                 [[9.0, 10.0, 11.0],  [9.0,10.0,11.0],  [9.0,10.0,11.0]],
                 [[12.0, 13.0, 14.0], [12.0,13.0,14.0], [12.0,13.0,14.0]]]
        y_mat = np.array(y_mat)
        v2_1d = v1_1d
        v2_2d = y_vec

        # Scalar
        pytplot.store_data('fptest',data={'x':xfp,'y':y_scalar})
        # 1-D vec, no metadata
        pytplot.store_data('fptest_vec_no_v1',data={'x':xfp,'y':y_vec})
        # 1-D vec, with 1-D (constant) V1
        pytplot.store_data('fptest_vec_v1_1d',data={'x':xfp,'y':y_vec, 'v':v1_1d})
        # 1-D vec, with 2-D (time varying) V1
        pytplot.store_data('fptest_vec_v1_2d',data={'x':xfp,'y':y_vec, 'v':v1_2d})
        # 3x3 mat, with no V1, no V2
        pytplot.store_data('fptest_mat_v1_none_v2_none',data={'x':xfp,'y':y_mat})
        # 3x3 mat, with 1-D (constant) V1, 1-D (constant) V2
        pytplot.store_data('fptest_mat_v1_1d_v2_1d',data={'x':xfp,'y':y_mat, 'v1':v1_1d, 'v2':v2_1d})
        # 3x3 mat, with 2-D (time varying) V1, 2-D (time varying) V2
        pytplot.store_data('fptest_mat_v1_2d_v2_2d',data={'x':xfp,'y':y_mat, 'v1':v1_2d, 'v2':v2_2d})
        # 3x3 mat, with 2-D (time varying) V1, 1-D (constant) V2
        pytplot.store_data('fptest_mat_v1_2d_v2_1d',data={'x':xfp,'y':y_mat, 'v1':v1_2d, 'v2':v2_1d})
        # 3x3 mat, with 1-D (constant) V1, 2-D (time varying) V2
        pytplot.store_data('fptest_mat_v1_1d_v2_2d',data={'x':xfp,'y':y_mat, 'v1':v1_1d, 'v2':v2_2d})
        # 3x3 mat, with missing V1, 2-D (time varying) V2
        # This doesn't quite work.  The 'v2' value doesn't survive the store_data/get_data round trip
        # if v1 is missing.  Not sure if that really qualifies as a bug, considering how ill-advised such a
        # construct would be...
        # pytplot.store_data('fptest_mat_v1_none_v2_2d',data={'x':xfp,'y':y_mat, 'v1':None, 'v2':v2_2d})



        # Test warning for no data in time range
        pytplot.time_clip('fptest',1.5,1.7)

        # Single value in time range
        pytplot.time_clip('fptest',1.5,2.5)
        self.assertTrue(data_exists('fptest-tclip'))
        dat=get_data('fptest-tclip')
        self.assertTrue(len(dat.times) == 1)
        self.assertTrue(dat.times[0] == 2.0)

        # Multiple values in time range
        pytplot.time_clip('fptest',1.5,3.5)
        dat=get_data('fptest-tclip')
        self.assertTrue(len(dat.times) == 2)
        assert_allclose(dat.times, [2.0, 3.0])

        # Multiple values in time range -- clip interior
        pytplot.time_clip('fptest',1.5,3.5, suffix='-tclip-interior', interior_clip=True)
        dat=get_data('fptest-tclip-interior')
        self.assertTrue(len(dat.times) == 3)
        assert_allclose(dat.times, [1.0, 4.0, 5.0])

        # Entire time range
        pytplot.time_clip('fptest',-100.0,100.0, suffix='-full_range')
        self.assertTrue(data_exists('fptest-full_range'))
        dat=get_data('fptest-full_range')
        self.assertTrue(len(dat.times) == 5)
        assert_allclose(dat.times, xfp)

        # Vector data, single value in time range, no metadata
        pytplot.time_clip('fptest_vec_no_v1',1.5,2.5)
        self.assertTrue(data_exists('fptest_vec_no_v1-tclip'))
        dat=get_data('fptest_vec_no_v1-tclip')
        self.assertTrue(len(dat.times) == 1)
        self.assertTrue(dat.times[0] == 2.0)
        assert_allclose(dat.y[0,:], [3.0,4.0,5.0])

        # Vector data, single value in time range, constant metadata
        pytplot.time_clip('fptest_vec_v1_1d',1.5,2.5)
        self.assertTrue(data_exists('fptest_vec_v1_1d-tclip'))
        dat=get_data('fptest_vec_v1_1d-tclip')
        self.assertTrue(len(dat.times) == 1)
        self.assertTrue(dat.times[0] == 2.0)
        assert_allclose(dat.y[0,:], [3.0,4.0,5.0])
        assert_allclose(dat.v, v1_1d)

        # Vector data, multiple values in time range, constant metadata
        pytplot.time_clip('fptest_vec_v1_1d',1.5,3.5)
        self.assertTrue(data_exists('fptest_vec_v1_1d-tclip'))
        dat=get_data('fptest_vec_v1_1d-tclip')
        self.assertTrue(len(dat.times) == 2)
        assert_allclose(dat.times, [2.0, 3.0])
        assert_allclose(dat.y, [[3.0,4.0,5.0], [6.0, 7.0, 8.0]])
        assert_allclose(dat.v, v1_1d)

        # Vector data, single value in time range, time-varying metadata
        pytplot.time_clip('fptest_vec_v1_2d',1.5,2.5)
        self.assertTrue(data_exists('fptest_vec_v1_2d-tclip'))
        dat=get_data('fptest_vec_v1_2d-tclip')
        self.assertTrue(len(dat.times) == 1)
        self.assertTrue(dat.times[0] == 2.0)
        self.assertTrue(dat.v.shape == (1,3))
        assert_allclose(dat.y[0,:], [3.0,4.0,5.0])
        assert_allclose(dat.v, v1_2d[1:2])

        # Vector data, multiple values in time range, time-varying metadata
        pytplot.time_clip('fptest_vec_v1_2d',1.5,3.5)
        self.assertTrue(data_exists('fptest_vec_v1_2d-tclip'))
        dat=get_data('fptest_vec_v1_2d-tclip')
        self.assertTrue(len(dat.times) == 2)
        assert_allclose(dat.times, xfp[1:3])
        self.assertTrue(dat.y.shape == (2,3))
        assert_allclose(dat.y, y_vec[1:3,:])
        self.assertTrue(dat.v.shape == (2,3))
        assert_allclose(dat.v, v1_2d[1:3])

        # matrix data, single value in time range, no metadata
        pytplot.time_clip('fptest_mat_v1_none_v2_none',1.5,2.5)
        self.assertTrue(data_exists('fptest_mat_v1_none_v2_none-tclip'))
        dat=get_data('fptest_mat_v1_none_v2_none-tclip')
        self.assertTrue(len(dat.times) == 1)
        self.assertTrue(dat.times[0] == 2.0)
        assert_allclose(dat.y[0,:,:], y_mat[1,:,:])

        # matrix data, single value in time range, constant v1 and v2 metadata
        pytplot.time_clip('fptest_mat_v1_1d_v2_1d',1.5,2.5)
        self.assertTrue(data_exists('fptest_mat_v1_1d_v2_1d-tclip'))
        dat=get_data('fptest_mat_v1_1d_v2_1d-tclip')
        self.assertTrue(len(dat.times) == 1)
        self.assertTrue(dat.times[0] == 2.0)
        assert_allclose(dat.y[0,:,:], y_mat[1,:,:])
        assert_allclose(dat.v1, v1_1d)
        assert_allclose(dat.v2, v2_1d)

        # matrix data, multiple values in time range, constant v1 and v2 metadata
        pytplot.time_clip('fptest_mat_v1_1d_v2_1d',1.5,3.5)
        self.assertTrue(data_exists('fptest_mat_v1_1d_v2_1d-tclip'))
        dat=get_data('fptest_mat_v1_1d_v2_1d-tclip')
        self.assertTrue(len(dat.times) == 2)
        assert_allclose(dat.times, [2.0, 3.0])
        assert_allclose(dat.y, y_mat[1:3,:,:])
        assert_allclose(dat.v1, v1_1d)
        assert_allclose(dat.v2, v2_1d)

        # matrix data, single value in time range, constant v1, time-varying v2 metadata
        pytplot.time_clip('fptest_mat_v1_1d_v2_2d',1.5,2.5)
        self.assertTrue(data_exists('fptest_mat_v1_1d_v2_2d-tclip'))
        dat=get_data('fptest_mat_v1_1d_v2_2d-tclip')
        self.assertTrue(len(dat.times) == 1)
        self.assertTrue(dat.times[0] == 2.0)
        self.assertTrue(dat.v1.shape == (3,))
        assert_allclose(dat.y[:,:,:], y_mat[1:2,:,:])
        assert_allclose(dat.v1, v1_1d)
        assert_allclose(dat.v2, v1_2d[1:2])

        # matrix data, multiple values in time range, constant v1, time-varying v2 metadata
        pytplot.time_clip('fptest_mat_v1_1d_v2_2d',1.5,3.5)
        self.assertTrue(data_exists('fptest_mat_v1_1d_v2_2d-tclip'))
        dat=get_data('fptest_mat_v1_1d_v2_2d-tclip')
        self.assertTrue(len(dat.times) == 2)
        assert_allclose(dat.times, xfp[1:3])
        self.assertTrue(dat.v1.shape == (3,))
        assert_allclose(dat.y[:,:,:], y_mat[1:3,:,:])
        assert_allclose(dat.v1, v1_1d)
        assert_allclose(dat.v2, v1_2d[1:3])

        # matrix data, single values in time range, time-varying v1, constant v2 metadata
        pytplot.time_clip('fptest_mat_v1_2d_v2_1d',1.5,2.5)
        self.assertTrue(data_exists('fptest_mat_v1_2d_v2_1d-tclip'))
        dat=get_data('fptest_mat_v1_2d_v2_1d-tclip')
        self.assertTrue(len(dat.times) == 1)
        self.assertTrue(dat.times[0] == 2.0)
        self.assertTrue(dat.v1.shape == (1,3))
        self.assertTrue(dat.v2.shape == (3,))
        assert_allclose(dat.y[:,:,], y_mat[1:2,:,:])
        assert_allclose(dat.v1, v1_2d[1:2])
        assert_allclose(dat.v2, v2_1d)

        # matrix data, multiple values in time range, time-varying v1, constant v2 metadata
        pytplot.time_clip('fptest_mat_v1_2d_v2_1d',1.5,3.5)
        self.assertTrue(data_exists('fptest_mat_v1_2d_v2_1d-tclip'))
        dat=get_data('fptest_mat_v1_2d_v2_1d-tclip')
        self.assertTrue(len(dat.times) == 2)
        assert_allclose(dat.times, [2.0, 3.0])
        self.assertTrue(dat.v1.shape == (2,3))
        self.assertTrue(dat.v2.shape == (3,))
        assert_allclose(dat.y[:,:,], y_mat[1:3,:,:])
        assert_allclose(dat.v1, v1_2d[1:3])
        assert_allclose(dat.v2, v2_1d)

        # Multiple variables in one call
        pytplot.store_data('tst1',data={'x':x,'y':y})
        pytplot.store_data('tst2',data={'x':x,'y':y})
        # reversed time limits
        pytplot.time_clip(['tst1','tst2'],10,1)
        # data completely outside time limits
        pytplot.time_clip(['tst1','tst2'],10,20)
        # one point in limits
        pytplot.time_clip('tst1',1.5,2.5)
        self.assertTrue(data_exists('tst1-tclip'))
        # overwrite
        pytplot.del_data('tst1-tclip')
        pytplot.time_clip('tst1',1.5,2.0,overwrite=True)
        self.assertFalse(data_exists('tst1-tclip'))
        pytplot.time_clip('tst1',1.5,2.5,newname='tst1_new')
        self.assertTrue(data_exists('tst1_new'))
        pytplot.time_clip('tst1',1.5,2.5,newname='',suffix='-tc1')
        self.assertTrue(data_exists('tst1-tc1'))
        pytplot.time_clip('tst1',1.5,2.5,newname=[],suffix='-tc2')
        self.assertTrue(data_exists('tst1-tc2'))
        # newname has different count than input names, default to suffix
        pytplot.time_clip('tst1',1.5,2.5, newname=['foo','bar'],suffix='-tc3')
        self.assertTrue(data_exists('tst1-tc3'))
        pytplot.time_clip('tst1',1.5,2.5,newname=None, suffix='-tc4')
        self.assertTrue(data_exists('tst1-tc4'))
        # no such tplot name
        pytplot.time_clip('bogus',1.5,2.5)
        # empty input list
        pytplot.time_clip([],1.5,2.5)

        # Strings as start/end times
        trange = ['2007-03-23/9:30', '2007-03-23/12:00']
        # Note times are out of order if compared as strings!
        self.assertTrue(trange[0] > trange[1])
        pyspedas.projects.themis.state(probe='a',trange=trange)
        pyspedas.time_clip('tha_pos',trange[0], trange[1],newname='tha_pos-tclip')
        self.assertTrue(data_exists('tha_pos-tclip'))
        dat=get_data('tha_pos-tclip')
        self.assertTrue(dat.times[0] >= pyspedas.time_float(trange[0]))


    def test_mpause_t96(self):
        trange = ['2023-03-24', '2023-03-25']
        # THEMIS orbits come from the 'state' datatype
        # We will use GSE coordinates for the plots we'll make.
        themis.state(probe='a', trange=trange, varformat='*_pos_gse')
        cotrans('tha_pos_gse', name_out='tha_pos_gsm', coord_in='GSE', coord_out='GSM')
        posdat = get_data('tha_pos_gsm')
        re = 6378.0
        pos_gsm = posdat.y / re
        xmgnp, ymgnp, zmgnp, id, distan = mpause_t96(
            pd=14.0, xgsm=pos_gsm[:, 0], ygsm=pos_gsm[:, 1], zgsm=pos_gsm[:, 2])
        self.assertEqual(len(xmgnp), 90)
        self.assertEqual(id.min(), -1)
        self.assertEqual(id.max(), 1)
        self.assertTrue(distan.min() < 0.01)
        self.assertTrue(distan.max() > 10.0)
        self.assertEqual(len(id), len(posdat.times))

    def test_mpause_2(self):
        trange = ['2023-03-24', '2023-03-25']
        # THEMIS orbits come from the 'state' datatype
        # We will use GSE coordinates for the plots we'll make.
        themis.state(probe='a', trange=trange, varformat='*_pos_gse')
        cotrans('tha_pos_gse', name_out='tha_pos_gsm', coord_in='GSE', coord_out='GSM')
        posdat = get_data('tha_pos_gsm')
        re = 6378.0
        pos_gsm = posdat.y / re
        xmp, ymp  = mpause_2()
        self.assertEqual(len(xmp),2000)
        self.assertEqual(len(ymp), 2000)
        self.assertTrue(xmp.min() < -299.0)
        self.assertTrue(xmp.max() > 10.77)
        self.assertTrue(ymp.min() < -68.0)
        self.assertTrue(ymp.max() > 77.8)

    def test_find_datasets_quiet(self):
        ds = find_datasets(mission='MMS', instrument='FGM', quiet=True)
        self.assertTrue('MMS1_FGM_BRST_L2' in ds)
        self.assertTrue('MMS2_FGM_BRST_L2' in ds)

    def test_find_datasets_nolabel(self):
        ds = find_datasets(mission='MMS', instrument='FGM')
        self.assertTrue('MMS1_FGM_BRST_L2' in ds)
        self.assertTrue('MMS2_FGM_BRST_L2' in ds)

    def test_find_datasets_label(self):
        ds = find_datasets(mission='MMS', instrument='FGM',label=True)
        self.assertTrue('MMS1_FGM_BRST_L2' in ds)
        self.assertTrue('MMS2_FGM_BRST_L2' in ds)

    def test_split_vec_metadata(self):
        del_data('*')
        pyspedas.projects.themis.fit(probe='c')
        md = get_data('thc_fgs_dsl', metadata=True)
        split_vec('thc_fgs_dsl')
        self.assertTrue(data_exists('thc_fgs_dsl_x'))
        self.assertTrue(data_exists('thc_fgs_dsl_y'))
        self.assertTrue(data_exists('thc_fgs_dsl_z'))
        md_x = get_data('thc_fgs_dsl_x', metadata=True)
        self.assertTrue(md_x['plot_options']['xaxis_opt']['axis_label'] == md['plot_options']['xaxis_opt']['axis_label'])

    def test_imports(self):
        import pyspedas
        from pytplot import del_data, data_exists, tplot_names
        # fully qualified name without .projects.
        del_data('*')
        pyspedas.projects.themis.state(probe='a')
        self.assertTrue(data_exists('tha_pos'))
        # fully qualified name with .projects.
        del_data('*')
        pyspedas.projects.themis.state(probe='a')
        self.assertTrue(data_exists('tha_pos'))

        # import themis without .projects.
        from pyspedas import themis
        del_data('*')
        themis.state(probe='a')
        self.assertTrue(data_exists('tha_pos'))
        # import themis with .projects.
        from pyspedas.projects import themis
        del_data('*')
        themis.state(probe='a')
        self.assertTrue(data_exists('tha_pos'))

        # import themis.state without .projects.
        # PyCharm's static analysis doesn't like this (red underlines) but it works at runtime
        from pyspedas.themis import state
        del_data('*')
        state(probe='a')
        self.assertTrue(data_exists('tha_pos'))
        # import state with .projects.
        from pyspedas.projects.themis import state
        del_data('*')
        state(probe='a')
        self.assertTrue(data_exists('tha_pos'))

        from pyspedas import mms
        del_data('*')
        mms.fgm()
        self.assertTrue(data_exists('mms1_fgm_b_gsm_srvy_l2'))

        from pyspedas.projects.mms import fgm
        del_data('*')
        fgm()
        self.assertTrue(data_exists('mms1_fgm_b_gsm_srvy_l2'))

        # deep import themis.state without .projects.
        from pyspedas.themis.state_tools.state import state
        del_data('*')
        state(probe='a')
        self.assertTrue(data_exists('tha_pos'))
        # deep import themis.state with .projects.
        from pyspedas.projects.themis.state_tools.state import state
        del_data('*')
        state(probe='a')
        self.assertTrue(data_exists('tha_pos'))

if __name__ == '__main__':
    unittest.main()
