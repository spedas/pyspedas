"""Test functions in the utilites folder."""
import unittest
import pyspedas
from copy import deepcopy

from pytplot import del_data, tplot, tplot_options, tplot_names
from pytplot import store_data, get_data
from pytplot import wildcard_expand, tname_byindex, tplot_wildcard_expand, tindex_byname

global_display=False
tp_data={'x':[1,2,3], 'y':[4,5,6]}

class UtilTestCases(unittest.TestCase):
    """Test functions related to tplot variable indexing and wildcards."""

    def test_wildcard_expand(self):
        # Test wildcard expansion against defined list
        master_list = ['Foo', 'foo', 'tha_pos_gsm', 'thb_pos_gsm', 'mms1_mec_r_sm']
        # Literal match
        result = wildcard_expand(master_list,"Foo")
        self.assertEqual(result,['Foo'])
        # Results should be ordered following patterns, not master list
        result = wildcard_expand(master_list,['foo', 'Foo'])
        self.assertEqual(result, ['foo', 'Foo'])
        # Wildcard expansion
        result = wildcard_expand(master_list,"th?_*_*")
        self.assertEqual(result,['tha_pos_gsm', 'thb_pos_gsm'])
        # Case sensitive (by default), no matches found
        result = wildcard_expand(master_list,"*SM")
        self.assertEqual(result, [])
        # Case insensitive
        result = wildcard_expand(master_list,"*SM", case_sensitive=False)
        self.assertEqual(result, ['tha_pos_gsm', 'thb_pos_gsm', 'mms1_mec_r_sm'])
        # Null pattern
        result = wildcard_expand(master_list, None)
        self.assertEqual(result, [])
        # Master list and pattern both null
        result = wildcard_expand(None,None)
        self.assertEqual(result, [])
        # Master list not a list
        result = wildcard_expand('foo', 'foo')
        self.assertEqual(result, [])

    def test_tplot_wildcard_expand(self):
        # Test wildcard expansion against current tplot variables
        del_data('*')
        master_list = ['Foo', 'foo', 'tha_pos_gsm', 'thb_pos_gsm', 'mms1_mec_r_sm']
        for var in master_list:
            store_data(var,deepcopy(tp_data))
        # Add a composite variable
        store_data('composite',data=['foo', 'tha_pos_gsm', 'thb_pos_gsm'])
        tplot_names()
        tn = tplot_names(quiet=True)
        print(tn)
        # Literal match
        result = tplot_wildcard_expand("Foo")
        self.assertEqual(result,['Foo'])
        # Results should be ordered following patterns, not master list
        result = tplot_wildcard_expand(['foo', 'Foo'])
        self.assertEqual(result, ['foo', 'Foo'])
        # Wildcard expansion
        result = tplot_wildcard_expand("th?_*_*")
        self.assertEqual(result,['tha_pos_gsm', 'thb_pos_gsm'])
        # Composite variable
        result = tplot_wildcard_expand('composite')
        self.assertEqual(result, ['composite'])
        # Case sensitive (by default), no matches found
        result = tplot_wildcard_expand("*SM")
        self.assertEqual(result, [])
        # Case insensitive
        result = tplot_wildcard_expand("*SM", case_sensitive=False)
        self.assertEqual(result, ['tha_pos_gsm', 'thb_pos_gsm', 'mms1_mec_r_sm'])
        # Mixed strings and integers with repeated values
        result = tplot_wildcard_expand(['Foo',1,2,2,'tha*'], case_sensitive=False)
        self.assertEqual(result, ['Foo','foo','tha_pos_gsm'])
        # Null pattern
        result = tplot_wildcard_expand(None)
        self.assertEqual(result, [])

    def test_tindex_byname(self):
        # Test lookups of tplot variable indices by name
        del_data('*')
        store_data('foo',data=deepcopy(tp_data))
        store_data('bar',data=deepcopy(tp_data))
        result=tindex_byname('foo')
        self.assertEqual(result,0)
        result=tindex_byname('bar')
        self.assertEqual(result,1)
        result=tindex_byname('doesnt_exist')
        self.assertEqual(result,None)

    def test_tname_byindex(self):
        # Test lookups of tplot variable names by indices
        del_data('*')
        # Out of bounds (no tplot variables yet)
        result=tname_byindex(0)
        self.assertEqual(result,None)
        store_data('foo',data=deepcopy(tp_data))
        store_data('bar',data=deepcopy(tp_data))
        result=tname_byindex(0)
        self.assertEqual(result,'foo')
        result=tname_byindex(1)
        self.assertEqual(result,'bar')
        # Index too large
        result=tname_byindex(2)
        self.assertEqual(result,None)
        # Negative index
        result=tname_byindex(-1)
        self.assertEqual(result,None)


    def test_plotting_wildcards_indices(self):
        # Test tplot using wildcards
        del_data('*')
        pyspedas.projects.themis.state(probe=['a', 'b', 'c', 'd', 'e'])
        # Wildcard pattern
        tplot_options('title',"Positions of THEMIS A B C D E")
        tplot('th?_pos', save_png='tplot_wildcard.png', display=global_display)
        # List of integer indices
        indices = [tindex_byname('tha_pos'), tindex_byname('thb_pos'), tindex_byname('thc_pos')]
        tplot_options('title',"Positions of THEMIS A B C")
        tplot(indices,save_png='tplot_byindex.png', display=global_display)
        # List including a bad name
        tplot_options('title',"Positions of THEMIS A B C D E")
        tplot(['th?_pos', 'doesnt_exist'], save_png='tplot_list_onebad.png', display=global_display)


if __name__ == '__main__':
    unittest.main()
