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
        tplot('tha_fgl_dsl')
        timespan('2007-03-23/14:00',0.9,"seconds")
        tplot('tha_fgl_dsl')

    def test_subsec_tlimit(self):
        """Test pytplot.timespan as used in ERG notebook"""
        from pytplot import tplot,tlimit
        from pyspedas.themis import fgm
        vars = fgm(probe='a',level='l2',trange=['2007-03-23', '2007-03-24'])
        tplot('tha_fgl_dsl')
        tlimit(['2007-03-23/14:00','2007-03-23/14:00:00.9'])
        tplot('tha_fgl_dsl')
        tlimit('full')
        tplot('tha_fgl_dsl')

if __name__ == '__main__':
    unittest.main()
