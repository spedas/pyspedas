"""
Unit Tests for minvar function.
"""
from pyspedas.cotrans.minvar import minvar
import numpy as np
import unittest


class TestMinvar(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tol = 1e-21

    def test_minvar_basic(self):
        data = np.zeros([2, 3])
        vrot, v, w = minvar(data)
        self.assertTrue(np.sum(vrot - data) < self.tol)
        self.assertTrue(np.sum(v - np.diag(np.ones(3))) < self.tol)
        self.assertTrue(np.sum(w - np.zeros(3)) < self.tol)


if __name__ == '__main__':
    unittest.main()