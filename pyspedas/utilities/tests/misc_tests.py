
import os
import unittest

from pyspedas import tcopy
from pytplot import get_data, store_data

class UtilTestCases(unittest.TestCase):
    def test_tcopy(self):
        store_data('test', data={'x': [1, 2, 3], 'y': [5, 5, 5]})
        tcopy('test')
        t, d = get_data('test-copy')
        self.assertTrue(t.tolist() == [1, 2, 3])
        self.assertTrue(d.tolist() == [5, 5, 5])