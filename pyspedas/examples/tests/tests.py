# -*- coding: utf-8 -*-
"""
File:
    tests.py

Description:
    Test the examples.

"""

import unittest


class LoadTestCases(unittest.TestCase):
    """ Run tests on examples. """

    '''
    def test_load_ex_analysis(self):
        from pyspedas.examples.basic.ex_analysis import ex_analysis
        ex = ex_analysis()
        self.assertEqual(ex, 1)
    '''

    def test_load_ex_basic(self):
        from pyspedas.examples.basic.ex_basic import ex_basic
        ex = ex_basic()
        self.assertEqual(ex, 1)

    def test_load_ex_cdagui(self):
        from pyspedas.examples.basic.ex_cdagui import ex_cdagui
        ex = ex_cdagui()
        self.assertEqual(ex, 1)

    def test_load_ex_dsl2gse(self):
        from pyspedas.examples.basic.ex_dsl2gse import ex_dsl2gse
        ex = ex_dsl2gse()
        self.assertEqual(ex, 1)

    def test_load_ex_cdasws(self):
        from pyspedas.examples.basic.ex_cdasws import ex_cdasws
        ex = ex_cdasws()
        self.assertEqual(ex, 1)
    '''
    def test_load_ex_omni(self):
        from pyspedas.examples.basic.ex_omni import ex_omni
        ex = ex_omni()
        self.assertEqual(ex, 1)
    '''


if __name__ == '__main__':
    unittest.main()
