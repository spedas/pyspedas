import logging
import unittest
import pyspedas
import pytplot
from numpy.testing import assert_allclose

class TplotTimeValidation(unittest.TestCase):
    """ Tests creation of support variables in themis.state() """

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        pass
        """ We need to clean tplot variables before each run"""


    def test_timespan(self):
        """Test pytplot.timespan as used in ERG notebook"""
        from pytplot import tplot,timespan
        from pyspedas.erg import mgf
        vars = mgf(trange=['2017-03-27', '2017-03-28'])  # load MGF Lv.2 8-s data for 0-24 UT on Mar. 27, 2017.
        tplot('erg_mgf_l2_mag_8sec_sm')
        timespan('2017-03-27 09:00:00', 6, keyword='hours')
        tplot(['erg_mgf_l2_mag_8sec_sm', 'erg_mgf_l2_mag_8sec_gsm'])

    def test_subsec_timespan(self):
        """Test pytplot.timespan as used in ERG notebook"""
        from pytplot import tplot,timespan
        from pyspedas.themis import fgm
        vars = fgm(probe='a',level='l2',trange=['2007-03-23', '2007-03-24'])
        tplot('tha_fgl_dsl') # full plot
        timespan('2007-03-23/14:00',0.9,"seconds")
        tplot('tha_fgl_dsl')  # short time interval

    def test_subsec_tlimit(self):
        """Test pytplot.timespan as used in ERG notebook"""
        from pytplot import tplot,tlimit
        from pyspedas.themis import fgm
        vars = fgm(probe='a',level='l2',trange=['2007-03-23', '2007-03-24'])
        tplot('tha_fgl_dsl')  # full plot
        tlimit(['2007-03-23/14:00','2007-03-23/14:00:00.9'])
        tplot('tha_fgl_dsl')  # short time interval

    def test_tlimit_full_arg(self):
        """Test pytplot.timespan as used in ERG notebook"""
        from pytplot import tplot,tlimit
        from pyspedas.themis import fgm
        vars = fgm(probe='a',level='l2',trange=['2007-03-23', '2007-03-24'])
        tplot('tha_fgl_dsl')  # full plot
        tlimit(['2007-03-23/14:00','2007-03-23/14:00:00.9'])
        tplot('tha_fgl_dsl')  # short time interval
        tlimit('full')
        tplot('tha_fgl_dsl')  # back to full interval

    def test_tlimit_full_flag(self):
        """Test pytplot.timespan as used in ERG notebook"""
        from pytplot import tplot,tlimit
        from pyspedas.themis import fgm
        vars = fgm(probe='a',level='l2',trange=['2007-03-23', '2007-03-24'])
        tplot('tha_fgl_dsl')  # full plot
        tlimit(['2007-03-23/14:00','2007-03-23/14:00:00.9'])
        tplot('tha_fgl_dsl')  # short time interval
        tlimit(full=True)
        tplot('tha_fgl_dsl')  # back to full interval

    def test_tlimit_last_arg(self):
        """Test pytplot.timespan as used in ERG notebook"""
        from pytplot import tplot,tlimit
        from pyspedas.themis import fgm
        vars = fgm(probe='a',level='l2',trange=['2007-03-23', '2007-03-24'])
        tplot('tha_fgl_dsl')  # full plot
        tlimit(['2007-03-23/14:00','2007-03-23/15:00:00'])
        tplot('tha_fgl_dsl')  # time interval 1  14:00 to 15:00
        tlimit(['2007-03-23/12:00','2007-03-23/13:00:00'])
        tplot('tha_fgl_dsl')  # time interval 2 12:00 to 13:00
        tlimit('last')
        tplot('tha_fgl_dsl')  # back to time interval 1, 14:00 to 15:00

    def test_tlimit_last_flag(self):
        """Test pytplot.timespan as used in ERG notebook"""
        from pytplot import tplot,tlimit
        from pyspedas.themis import fgm
        vars = fgm(probe='a',level='l2',trange=['2007-03-23', '2007-03-24'])
        tplot('tha_fgl_dsl')  # full plot
        tlimit(['2007-03-23/14:00','2007-03-23/15:00:00'])
        tplot('tha_fgl_dsl')  # time interval 1  14:00 to 15:00
        tlimit(['2007-03-23/12:00','2007-03-23/13:00:00'])
        tplot('tha_fgl_dsl')  # time interval 2 12:00 to 13:00
        tlimit(last=True)
        tplot('tha_fgl_dsl')  # back to time interval 1, 14:00 to 15:00


if __name__ == '__main__':
    unittest.main()
