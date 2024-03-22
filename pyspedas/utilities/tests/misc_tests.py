"""Test functions in the utilites folder."""
import unittest

from pyspedas.utilities.dailynames import dailynames
from pyspedas import tcopy
from pyspedas import themis
from pytplot import data_exists, tkm2re, tplot
from pytplot import get_data, store_data, options


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
        x=[1,2,3]
        y=[2,4,6]
        xfp = [1.0,2.0,3.0]
        pytplot.store_data('fptest',data={'x':xfp,'y':y})
        # Test warning for no data in time range
        pytplot.time_clip('fptest',1.5,1.7)
        # Single value in time range
        pytplot.time_clip('fptest',1.5,2.5)
        self.assertTrue(data_exists('fptest-tclip'))
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
        pytplot.time_clip('tst1',1.5,2.5,new_names='tst1_new')
        self.assertTrue(data_exists('tst1_new'))
        pytplot.time_clip('tst1',1.5,2.5,new_names='',suffix='-tc1')
        self.assertTrue(data_exists('tst1-tc1'))
        pytplot.time_clip('tst1',1.5,2.5,new_names=[],suffix='-tc2')
        self.assertTrue(data_exists('tst1-tc2'))
        # new_names has different count than input names, default to suffix
        pytplot.time_clip('tst1',1.5,2.5, new_names=['foo','bar'],suffix='-tc3')
        self.assertTrue(data_exists('tst1-tc3'))
        pytplot.time_clip('tst1',1.5,2.5,new_names=None, suffix='-tc4')
        self.assertTrue(data_exists('tst1-tc4'))
        # no such tplot name
        pytplot.time_clip('bogus',1.5,2.5)
        # empty input list
        pytplot.time_clip([],1.5,2.5)

if __name__ == '__main__':
    unittest.main()
