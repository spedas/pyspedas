import unittest
import logging
import numpy as np
from numpy.testing import assert_allclose
import pyspedas
from pyspedas.geopack.prepare_pos_variable import prepare_pos_variable
from pyspedas import get_coords, get_units, tkm2re, tplot_copy
from pyspedas import set_coords, set_units
from pyspedas import cotrans, get_data

class LoadTestCases(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pyspedas.projects.themis.state(probe='a')
        tkm2re('tha_pos_gsm',newname='tha_pos_gsm_re')
        tkm2re('tha_pos_gse',newname='tha_pos_gse_re')
        tplot_copy('tha_pos_gsm_re', new_name='tha_pos_gsm_re_nocoord')
        set_coords('tha_pos_gsm_re_nocoord',None)
        tplot_copy('tha_pos_gsm_re', new_name='tha_pos_gsm_re_nounit')
        set_units('tha_pos_gsm_re_nounit', None)
        tplot_copy('tha_pos_gsm_re', new_name='tha_pos_gsm_re_badcoord')
        set_coords('tha_pos_gsm_re_badcoord','bogus')
        tplot_copy('tha_pos_gsm_re', new_name='tha_pos_gsm_re_badunit')
        set_units('tha_pos_gsm_re_badunit', 'bogus')


    def test_nonexistent_input(self):
        with self.assertRaises(ValueError):
            result = prepare_pos_variable('nonexistent')

    def test_input_gsm_units_re(self):
        result = prepare_pos_variable('tha_pos_gsm_re')
        self.assertEqual(result, 'tha_pos_gsm_re')


    def test_input_gsm_units_km(self):
        result = prepare_pos_variable('tha_pos_gsm')
        self.assertEqual(result, 'input_var_re')
        coords = get_coords('input_var_re')
        units = get_units('input_var_re')
        self.assertEqual(coords.lower(), 'gsm')
        self.assertEqual(units.lower(), 're')
        # Check that unit converted result is correct
        orig = get_data('tha_pos_gsm_re')
        prep = get_data(result)
        assert_allclose(orig.times, prep.times)
        assert_allclose(orig.y, prep.y, atol=1e-5)


    def test_input_gse_units_km(self):
        result = prepare_pos_variable('tha_pos_gse')
        coords = get_coords(result)
        units = get_units(result)
        self.assertNotEqual(result, 'tha_pos_gse')
        self.assertEqual(coords.lower(), 'gsm')
        self.assertEqual(units.lower(), 're')
        # Check that cotransed value is correct
        orig = get_data('tha_pos_gsm_re')
        prep = get_data(result)
        assert_allclose(orig.times, prep.times)
        assert_allclose(orig.y, prep.y, atol=1e-5)

    def test_input_gse_units_re(self):
        result = prepare_pos_variable('tha_pos_gse_re')
        coords = get_coords(result)
        units = get_units(result)
        self.assertNotEqual(result, 'tha_pos_gse_re')
        self.assertEqual(coords.lower(), 'gsm')
        self.assertEqual(units.lower(), 're')
        # Check that cotransed value is correct
        orig = get_data('tha_pos_gsm_re')
        prep = get_data(result)
        assert_allclose(orig.times, prep.times)
        assert_allclose(orig.y, prep.y, atol=1e-5)

    def test_input_override_nocoord(self):
        result=prepare_pos_variable('tha_pos_gsm_re_nocoord', coord_in='GSM')
        coords = get_coords(result)
        units = get_units(result)
        self.assertEqual(result, 'tha_pos_gsm_re_nocoord')
        self.assertEqual(coords, None)
        self.assertEqual(units.lower(), 're')

    def test_input_override_nounits(self):
        result=prepare_pos_variable('tha_pos_gsm_re_nounit', units_in='Re')
        coords = get_coords(result)
        units = get_units(result)
        self.assertEqual(result, 'tha_pos_gsm_re_nounit')
        self.assertEqual(coords.lower(), 'gsm')
        self.assertEqual(units, None)

    def test_input_override_coord_conflict(self):
        # This should warn about overriding existing metadata.
        with self.assertLogs(logging.getLogger(),'WARNING') as logs:
            result=prepare_pos_variable('tha_pos_gse_re', coord_in='GSM')
        # show what warnings were logged
        for msg in logs.output:
            logging.info(msg)
        coords = get_coords(result)
        units = get_units(result)
        self.assertEqual(result, 'tha_pos_gse_re')
        self.assertEqual(coords.lower() , 'gse')  # We lied!  So it didn't get changed.
        self.assertEqual(units.lower(), 're')

    def test_input_override_unit_conflict(self):
        # This should warn about overriding existing metadata.
        with self.assertLogs(logging.getLogger(),'WARNING') as logs:
            result=prepare_pos_variable('tha_pos_gsm', units_in='Re')
        # show what warnings were logged
        for msg in logs.output:
            logging.info(msg)
        coords = get_coords(result)
        units = get_units(result)
        self.assertEqual(result, 'tha_pos_gsm')
        self.assertEqual(coords.lower() , 'gsm')
        self.assertEqual(units.lower(), 'km') # We lied! So it didn't get changed.

    def test_input_nounit_nooverride(self):
        with self.assertRaises(ValueError):
            result=prepare_pos_variable('tha_pos_gsm_re_nounit')

    def test_input_nocoord_nooverride(self):
        with self.assertRaises(ValueError):
            result=prepare_pos_variable('tha_pos_gsm_re_nocoord')

    def test_input_badunit_nooverride(self):
        with self.assertRaises(ValueError):
            result=prepare_pos_variable('tha_pos_gsm_re_badunit')

    def test_input_badcoord_nooverride(self):
        with self.assertRaises(ValueError):
            result=prepare_pos_variable('tha_pos_gsm_re_badcoord')

    def test_input_nounit_badoverride(self):
        with self.assertRaises(ValueError):
            result=prepare_pos_variable('tha_pos_gsm_re_nounit', units_in='bogus')

    def test_input_nocoord_badoverride(self):
        with self.assertRaises(ValueError):
            result=prepare_pos_variable('tha_pos_gsm_re_nocoord', coord_in='bogus')

if __name__ == "__main__":
    unittest.main()
