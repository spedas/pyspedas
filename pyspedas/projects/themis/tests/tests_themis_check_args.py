import unittest
from pyspedas.projects.themis.common.check_args import check_args


class TestThemisCheckArg(unittest.TestCase):

    def test_basic(self):
        res_list = [['a'], ['l2']]
        self.assertEqual(check_args(probe='a', level='l2'), res_list)

    def test_multi_probes(self):
        res_list = [['a', 'b', 'c']]
        self.assertEqual(check_args(probe=' a B c   '), res_list)

    def test_multi_levels(self):
        res_list = [['l1', 'l2']]
        self.assertEqual(check_args(level='    l1 l0 l2  '), res_list)

    def test_lists(self):
        res_list = [['a', 'b', 'c'], ['l1', 'l2']]
        self.assertEqual(check_args(probe=[' a b ', 'c', 'g'], level=['l0 l1', 'l2']), res_list)

    def test_wrong_arguments(self):
        res_list = []
        self.assertEqual(check_args(probes='a b', levels='l0'), res_list)


if __name__ == '__main__':
    unittest.main()
