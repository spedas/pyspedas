"""Test functions in the utilites folder."""

import os
import unittest
from copy import deepcopy
from pyspedas.projects import themis
from pyspedas import (
    del_data,
    tplot,
    tplot_options,
    tplot_names,
    store_data,
    wildcard_expand,
    tname_byindex,
    tplot_wildcard_expand,
    tindex_byname,
    data_exists,
    tnames,
)
from pyspedas.utilities.config_testing import TESTING_CONFIG

# Whether to display plots during testing
global_display = TESTING_CONFIG["global_display"]
# Directory to save testing output files
output_dir = TESTING_CONFIG["local_testing_dir"]
# Ensure output directory exists
save_dir = os.path.join(output_dir, "utilities")
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

tp_data = {"x": [1, 2, 3], "y": [4, 5, 6]}


class UtilTestCases(unittest.TestCase):
    """Test functions related to tplot variable indexing and wildcards."""

    def test_wildcard_expand(self):
        # Test wildcard expansion against defined list
        master_list = ["Foo", "foo", "tha_pos_gsm", "thb_pos_gsm", "mms1_mec_r_sm"]
        # Literal match
        result = wildcard_expand(master_list, "Foo")
        self.assertEqual(result, ["Foo"])
        # Results should be ordered following patterns, not master list
        result = wildcard_expand(master_list, ["foo", "Foo"])
        self.assertEqual(result, ["foo", "Foo"])
        # Wildcard expansion
        result = wildcard_expand(master_list, "th?_*_*")
        self.assertEqual(result, ["tha_pos_gsm", "thb_pos_gsm"])
        # Case sensitive (by default), no matches found
        result = wildcard_expand(master_list, "*SM")
        self.assertEqual(result, [])
        # Case insensitive
        result = wildcard_expand(master_list, "*SM", case_sensitive=False)
        self.assertEqual(result, ["tha_pos_gsm", "thb_pos_gsm", "mms1_mec_r_sm"])
        # Null pattern
        result = wildcard_expand(master_list, None)
        self.assertEqual(result, [])
        # Master list and pattern both null
        result = wildcard_expand(None, None)
        self.assertEqual(result, [])
        # Master list not a list (Formerly an error, now accepted)
        result = wildcard_expand("foo", "foo")
        self.assertEqual(result, ["foo"])
        # Master list as space delimited string  (used to be an error, now accepted)
        master_list_str = "Foo foo tha_pos_gsm thb_pos_gsm mms1_mec_r_sm"
        result = wildcard_expand(master_list_str, "foo")
        self.assertEqual(result, ["foo"])
        # Master list and search list as space delimited strings
        result = wildcard_expand(master_list_str, "foo bar")
        self.assertEqual(result, ["foo"])
        # Search list is a list containing some space delimited strings
        result = wildcard_expand(master_list_str, ["Foo", "foo", "thb_pos_gsm mms1_mec_r_sm"])
        self.assertEqual(result, ["Foo", "foo", "thb_pos_gsm", "mms1_mec_r_sm"])
        # Master list is empty
        result = wildcard_expand([], "foo")
        self.assertEqual(result, [])
        result = wildcard_expand([""], "foo")
        self.assertEqual(result, [])
        # Patterns are empty
        result = wildcard_expand(master_list_str, [])
        self.assertEqual(result, [])
        result = wildcard_expand(master_list_str, "")
        self.assertEqual(result, [])
        # Do not split on spaces
        result = wildcard_expand(["foo bar", "baz quux"], "foo bar", split_whitespace=False)
        self.assertEqual(result, ["foo bar"])

    def test_wildcard_quiet(self):
        master = ["string1", "string2", "string3"]
        patt1 = "notfound"
        with self.assertLogs(level="WARNING") as log:
            # This should produce a warning
            result = wildcard_expand(master, patt1)
            self.assertTrue("No match found" in log.output[0])
            # With quiet==True, there should be no warning
            result = wildcard_expand(master, patt1, quiet=True)
            self.assertIsNotNone(result)
            self.assertTrue(len(log.output) == 1)

    def test_tplot_wildcard_quiet(self):
        del_data("*")
        store_data("foo", deepcopy(tp_data))
        patt1 = "notfound"
        with self.assertLogs(level="WARNING") as log:
            # This should produce a warning
            result = tplot_wildcard_expand(patt1)
            self.assertTrue("No match found" in log.output[0])
            self.assertFalse(result)
            # With quiet==True, there should be no warning
            result = tplot_wildcard_expand(patt1, quiet=True)
            self.assertTrue(len(log.output) == 1)
            del_data("*")
            # Should warn about empty list of tplot variable names
            result = tplot_wildcard_expand(patt1)
            self.assertTrue("is empty" in log.output[1])
            # len(log.output) is now 2
            # With quiet==True, there should be no warning
            result = tplot_wildcard_expand(patt1, quiet=True)
            self.assertTrue(len(log.output) == 2)

    def test_tplot_wildcard_expand(self):
        # Test wildcard expansion against current tplot variables
        del_data("*")
        master_list = ["Foo", "foo", "tha_pos_gsm", "thb_pos_gsm", "mms1_mec_r_sm"]
        for var in master_list:
            store_data(var, deepcopy(tp_data))
        # Add a composite variable
        store_data("composite", data=["foo", "tha_pos_gsm", "thb_pos_gsm"])
        tplot_names()
        tn = tplot_names(quiet=True)
        print(tn)
        # Literal match
        result = tplot_wildcard_expand("Foo")
        self.assertEqual(result, ["Foo"])
        # Results should be ordered following patterns, not master list
        result = tplot_wildcard_expand(["foo", "Foo"])
        self.assertEqual(result, ["foo", "Foo"])
        # Wildcard expansion
        result = tplot_wildcard_expand("th?_*_*")
        self.assertEqual(result, ["tha_pos_gsm", "thb_pos_gsm"])
        # Composite variable
        result = tplot_wildcard_expand("composite")
        self.assertEqual(result, ["composite"])
        # Case sensitive (by default), no matches found
        result = tplot_wildcard_expand("*SM")
        self.assertEqual(result, [])
        # Case insensitive
        result = tplot_wildcard_expand("*SM", case_sensitive=False)
        self.assertEqual(result, ["tha_pos_gsm", "thb_pos_gsm", "mms1_mec_r_sm"])
        # Mixed strings and integers with repeated values
        result = tplot_wildcard_expand(["Foo", 1, 2, 2, "tha*"], case_sensitive=False)
        self.assertEqual(result, ["Foo", "foo", "tha_pos_gsm"])
        # Null pattern
        result = tplot_wildcard_expand(None)
        self.assertEqual(result, [])

    def test_tindex_byname(self):
        # Test lookups of tplot variable indices by name
        del_data("*")
        store_data("foo", data=deepcopy(tp_data))
        store_data("bar", data=deepcopy(tp_data))
        result = tindex_byname("foo")
        self.assertEqual(result, 0)
        result = tindex_byname("bar")
        self.assertEqual(result, 1)
        result = tindex_byname("doesnt_exist")
        self.assertEqual(result, None)

    def test_tname_byindex(self):
        # Test lookups of tplot variable names by indices
        del_data("*")
        # Out of bounds (no tplot variables yet)
        result = tname_byindex(0)
        self.assertEqual(result, None)
        store_data("foo", data=deepcopy(tp_data))
        store_data("bar", data=deepcopy(tp_data))
        result = tname_byindex(0)
        self.assertEqual(result, "foo")
        result = tname_byindex(1)
        self.assertEqual(result, "bar")
        # Index too large
        result = tname_byindex(2)
        self.assertEqual(result, None)
        # Negative index
        result = tname_byindex(-1)
        self.assertEqual(result, None)

    def test_plotting_wildcards_indices(self):
        # Test tplot using wildcards
        del_data("*")
        themis.state(probe=["a", "b", "c", "d", "e"])
        # Wildcard pattern
        tplot_options("title", "Positions of THEMIS A B C D E")
        tplot("th?_pos", display=global_display, save_png=os.path.join(save_dir, "tplot_wildcard.png"))
        # List of integer indices
        indices = [tindex_byname("tha_pos"), tindex_byname("thb_pos"), tindex_byname("thc_pos")]
        tplot_options("title", "Positions of THEMIS A B C")
        tplot(indices, display=global_display, save_png=os.path.join(save_dir, "tplot_byindex.png"))
        # List including a bad name
        tplot_options("title", "Positions of THEMIS A B C D E")
        tplot(["th?_pos", "doesnt_exist"], display=global_display, save_png=os.path.join(save_dir, "tplot_list_onebad.png"))

    def test_tplot_names_embedded_spaces(self):
        # Tplot names can have embedded spaces, make sure they're treated correctly
        del_data("*")
        t = [1.0, 2.0, 3.0]
        d = [1, 2, 3]
        store_data("embedded spaces", data={"x": t, "y": d})
        names = tnames()
        self.assertEqual(names, ["embedded spaces"])
        names = tplot_names()
        self.assertEqual(names, ["embedded spaces"])
        del_data("embedded spaces")
        self.assertFalse(data_exists("embedded spaces"))
        store_data("embedded spaces", data={"x": t, "y": d})
        del_data("*")
        self.assertFalse(data_exists("embedded spaces"))
        store_data("embedded spaces", data={"x": t, "y": d})
        # This should warn about 'd', 'e', and 'f' not found, but not warn about 'embedded' or 'spaces'
        vals = tplot_wildcard_expand(["embedded spaces", "d e f"])
        self.assertEqual(vals, ["embedded spaces"])


if __name__ == "__main__":
    unittest.main()
