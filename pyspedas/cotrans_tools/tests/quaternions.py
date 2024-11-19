import unittest
import numpy as np
from pyspedas.cotrans_tools.quaternions import qslerp, qcompose, qconj, mtoq, qtom, qvalidate, qmult, qdecompose


class Qtests(unittest.TestCase):
    def test_qslerp(self):
        m1 = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
        m2 = np.array([[-1, 0, 0], [0, -1, 0], [0, 0, 1]])
        qin = np.transpose(np.array([mtoq(m1), mtoq(m2)])).reshape([4, 2]).transpose()
        x1 = np.array([0.0, 1.0])
        x2 = np.array([0.0, 1.0/6.0, 1.0/3.0, 1.0/2.0, 2.0/3.0, 5.0/6.0, 1.0])
        qout = qslerp(qin, x1, x2)
        qout_geo = qslerp(qin, x1, x2, geometric=True)
        mout = qtom(qout)
        qcomp = qcompose(np.array([[1, 2, 3]]), np.array([4]), free=False)
        self.assertTrue(np.abs(np.sum(qout-qout_geo))<1e-6)

    def test_errors(self):
        qs1 = np.ones((7, 5))
        qs2 = np.ones((8, 4))
        qs3 = np.ones(4)
        self.assertTrue(qvalidate(qs1, 'qs1', 'qslerp') == -1)
        self.assertTrue(qmult(qs1, qs2) == -1)
        self.assertTrue(qdecompose(np.array(1)) == -1)
        self.assertTrue(qdecompose(1) == -1)
        self.assertTrue(qconj(1) == -1)
        self.assertTrue(qslerp(qs1, qs1, qs1) == -1)


if __name__ == '__main__':
    unittest.main()