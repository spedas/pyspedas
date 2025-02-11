"""Test gmag and themis load functions."""
import os
import unittest
from pytplot import data_exists, time_string, time_double, del_data, get_timespan
from pyspedas.projects.themis import autoload_support, get_spinmodel, fit
from pyspedas.projects.themis.state_tools.autoload_support import load_needed


class AutoLoadTestCases(unittest.TestCase):
    """Test themis support data autoload functions."""

    def test_load_needed_exact(self):
        # Test logic for determining whether support data needs to be loaded, based on exact comparisons
        # Timespan 1 completely encloses timespan 2
        ts1=['2007-03-23 00:00:00', '2007-03-24 00:00:00']
        ts2=['2007-03-23 00:00:01', '2007-03-23 23:59:59']

        tr1=time_double(ts1)
        tr2=time_double(ts2)
        trange_loaded=tr1
        trange_needed=tr2
        # trange loaded encloses trange needed on both sides, no load needed
        self.assertFalse(load_needed(trange_loaded,trange_needed,tolerance=0.0))
        trange_loaded=tr2
        trange_needed=tr1
        # trange loaded is a proper subset of trange needed, load needed
        self.assertTrue(load_needed(trange_loaded,trange_needed,tolerance=0.0))
        # tr3 starts before tr1
        tr3=[tr2[0] - 2.0, tr2[1]]
        trange_loaded=tr1
        trange_needed=tr3
        # trange needed starts before trange loaded, load needed
        self.assertTrue(load_needed(trange_loaded,trange_needed,tolerance=0.0))
        # tr4 ends after tr1
        tr4=[tr2[0], tr2[1]+2.0]
        trange_loaded=tr1
        trange_needed=tr4
        # trange needed ends after trange loaded, load needed
        self.assertTrue(load_needed(trange_loaded,trange_needed,tolerance=0.0))

    def test_load_needed_tolerance(self):
        # Test logic for determining whether support data needs to be loaded, while
        # allowing a certain amount of extrapolation
        tolerance = 10.0
        ts1=['2007-03-23 00:00:00', '2007-03-24 00:00:00']
        tr1 = time_double(ts1)
        trange_needed=tr1
        ts2=['2007-03-23 00:00:09', '2007-03-23 23:59:51']
        tr2=time_double(ts2)
        trange_loaded=tr2
        # Loaded data fails to overlap needed data by < tolerance on both sides, load not needed
        self.assertFalse(load_needed(trange_loaded,trange_needed,tolerance=tolerance))
        trange_loaded=tr1
        trange_needed=tr2
        # Loaded data overlaps needed data on both ends, load not needed
        self.assertFalse(load_needed(trange_loaded,trange_needed,tolerance=tolerance))
        trange_loaded=tr1
        trange_needed=[tr1[0] - 9.0, tr1[1]]
        # Loaded data fails to overlap needed data by < tolerance on left side, load not needed
        self.assertFalse(load_needed(trange_loaded,trange_needed,tolerance=tolerance))
        trange_needed=[tr1[0], tr1[1]+9.0]
        # Loaded data fails to overlap needed data by < tolerance on right side, load not needed
        self.assertFalse(load_needed(trange_loaded,trange_needed,tolerance=tolerance))
        trange_needed=[tr1[0] - 11.0, tr1[1]]
        # Loaded data fails to overlap needed data by > tolerance on left side, load needed
        self.assertTrue(load_needed(trange_loaded,trange_needed,tolerance=tolerance))
        trange_needed=[tr1[0], tr1[1]+11.0]
        # Loaded data fails to overlap needed data by > tolerance on right side, load needed
        self.assertTrue(load_needed(trange_loaded,trange_needed,tolerance=tolerance))


    def test_autoload_support_from_var(self):
        """Load FGM."""
        del_data('thc_*')
        del_data('slp_*')
        fit(trange=['2023-01-06','2023-01-07'])
        autoload_support(varname='thc_fgs_gse',slp=True,spinaxis=True,spinmodel=True)
        self.assertTrue(data_exists('thc_spinras'))
        self.assertTrue(data_exists('thc_spindec'))
        self.assertTrue(data_exists('slp_lun_att_x'))
        spinmodel=get_spinmodel(probe='c',correction_level=1)
        self.assertTrue(not (spinmodel is None))
        trange_needed=get_timespan('thc_fgs_gse')
        ts1=get_timespan('thc_spinras')
        ts2=get_timespan('thc_spindec')
        ts3=get_timespan('slp_lun_att_x')
        ts4=spinmodel.get_timerange()
        self.assertFalse(load_needed(ts1,trange_needed,tolerance=120.0))
        self.assertFalse(load_needed(ts2,trange_needed,tolerance=120.0))
        self.assertFalse(load_needed(ts3,trange_needed,tolerance=120.0))
        self.assertFalse(load_needed(ts4,trange_needed,tolerance=120.0))

    def test_autoload_support_without_var(self):
        """Load FGM."""
        del_data('thc_*')
        del_data('slp_*')
        trange=['2023-01-06','2023-01-07']
        autoload_support(trange=time_double(trange),probe='c',slp=True,spinaxis=True,spinmodel=True)
        self.assertTrue(data_exists('thc_spinras'))
        self.assertTrue(data_exists('thc_spindec'))
        self.assertTrue(data_exists('slp_lun_att_x'))
        spinmodel=get_spinmodel(probe='c',correction_level=1)
        self.assertTrue(not (spinmodel is None))
        trange_needed=time_double(trange)
        ts1=get_timespan('thc_spinras')
        ts2=get_timespan('thc_spindec')
        ts3=get_timespan('slp_lun_att_x')
        ts4=spinmodel.get_timerange()
        self.assertFalse(load_needed(ts1,trange_needed,tolerance=120.0))
        self.assertFalse(load_needed(ts2,trange_needed,tolerance=120.0))
        self.assertFalse(load_needed(ts3,trange_needed,tolerance=120.0))
        self.assertFalse(load_needed(ts4,trange_needed,tolerance=120.0))

    def test_autoload_support_reload_all(self):
        """Load FGM."""
        del_data('thc_*')
        del_data('slp_*')
        trange=['2008-01-01','2008-01-01']
        autoload_support(trange=time_double(trange),probe='c',slp=True,spinaxis=True,spinmodel=True)
        self.assertTrue(data_exists('thc_spinras'))
        self.assertTrue(data_exists('thc_spindec'))
        self.assertTrue(data_exists('slp_lun_att_x'))
        spinmodel=get_spinmodel(probe='c',correction_level=1)
        self.assertTrue(not (spinmodel is None))
        trange_needed=time_double(trange)
        ts1=get_timespan('thc_spinras')
        ts2=get_timespan('thc_spindec')
        ts3=get_timespan('slp_lun_att_x')
        ts4=spinmodel.get_timerange()
        self.assertFalse(load_needed(ts1,trange_needed,tolerance=120.0))
        self.assertFalse(load_needed(ts2,trange_needed,tolerance=120.0))
        self.assertFalse(load_needed(ts3,trange_needed,tolerance=120.0))
        self.assertFalse(load_needed(ts4,trange_needed,tolerance=120.0))
        # Now choose a different non-overlapping time range, and ensure everything got reloaded.
        trange=['2022-01-06','2022-01-07']
        autoload_support(trange=time_double(trange),probe='c',slp=True,spinaxis=True,spinmodel=True)
        trange_needed=time_double(trange)
        ts1=get_timespan('thc_spinras')
        ts2=get_timespan('thc_spindec')
        ts3=get_timespan('slp_lun_att_x')
        spinmodel=get_spinmodel(probe='c',correction_level=1)
        ts4=spinmodel.get_timerange()
        self.assertFalse(load_needed(ts1,trange_needed,tolerance=120.0))
        self.assertFalse(load_needed(ts2,trange_needed,tolerance=120.0))
        self.assertFalse(load_needed(ts3,trange_needed,tolerance=120.0))
        self.assertFalse(load_needed(ts4,trange_needed,tolerance=120.0))

    def test_autoload_support_var_doesntexist(self):
        # Should warn if a nonexistent tplot variable is passed
        autoload_support(varname='doesntexist',slp=True,spinaxis=True,spinmodel=True)

    def test_autoload_support_err_no_trange_no_var(self):
        # Should warn about trange being needed if no tplot variable passed
        autoload_support(probe='c',slp=True,spinaxis=True,spinmodel=True)

    def test_autoload_support_err_no_trange_no_probe(self):
        # Should warn about probe being needed if no tplot variable passed and spinaxis or spinmodel
        trange=['2007-03-23','2007-03-24']
        autoload_support(trange=trange,probe=None,slp=False,spinaxis=True,spinmodel=True)

    def test_autoload_support_no_probe_no_var_slp_only(self):
        # Passing a trange only should work if only SLP data is requested
        del_data('slp_*')
        trange=['2007-03-23','2007-03-24']
        autoload_support(trange=trange,slp=True)
        self.assertTrue(data_exists('slp_lun_att_x'))

if __name__ == '__main__':
    unittest.main()
