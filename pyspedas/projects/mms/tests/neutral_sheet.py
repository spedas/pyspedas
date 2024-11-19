import numpy as np
import unittest
import pyspedas
from pyspedas import tkm2re
from pyspedas.analysis.neutral_sheet import neutral_sheet
from pytplot import get_data

pyspedas.projects.mms.mec()
tkm2re('mms1_mec_r_gsm')
pos_data = get_data('mms1_mec_r_gsm_re')


class NSTests(unittest.TestCase):
    def test_lopez(self):
        model = neutral_sheet(pos_data.times, pos_data.y, model='lopez', sc2NS=True)
        self.assertTrue(isinstance(model, np.ndarray))
        model = neutral_sheet(pos_data.times, pos_data.y, model='lopez')
        self.assertTrue(isinstance(model, np.ndarray))

    def test_sm(self):
        model = neutral_sheet(pos_data.times, pos_data.y, model='sm', sc2NS=True)
        self.assertTrue(isinstance(model, np.ndarray))
        model = neutral_sheet(pos_data.times, pos_data.y, model='sm')
        self.assertTrue(isinstance(model, np.ndarray))

    def test_themis(self):
        model = neutral_sheet(pos_data.times, pos_data.y, model='themis', sc2NS=True)
        self.assertTrue(isinstance(model, np.ndarray))
        model = neutral_sheet(pos_data.times, pos_data.y, model='themis')
        self.assertTrue(isinstance(model, np.ndarray))

    def test_aen(self):
        model = neutral_sheet(pos_data.times, pos_data.y, model='aen', sc2NS=True)
        self.assertTrue(isinstance(model, np.ndarray))
        model = neutral_sheet(pos_data.times, pos_data.y, model='aen')
        self.assertTrue(isinstance(model, np.ndarray))

    def test_den(self):
        model = neutral_sheet(pos_data.times, pos_data.y, model='den', sc2NS=True)
        self.assertTrue(isinstance(model, np.ndarray))
        model = neutral_sheet(pos_data.times, pos_data.y, model='den')
        self.assertTrue(isinstance(model, np.ndarray))

    def test_fairfield(self):
        model = neutral_sheet(pos_data.times, pos_data.y, model='fairfield', sc2NS=True)
        self.assertTrue(isinstance(model, np.ndarray))
        model = neutral_sheet(pos_data.times, pos_data.y, model='fairfield')
        self.assertTrue(isinstance(model, np.ndarray))

    def test_den_fairfield(self):
        model = neutral_sheet(pos_data.times, pos_data.y, model='den_fairfield', sc2NS=True)
        self.assertTrue(isinstance(model, np.ndarray))
        model = neutral_sheet(pos_data.times, pos_data.y, model='den_fairfield')
        self.assertTrue(isinstance(model, np.ndarray))

    def test_tag14(self):
        model = neutral_sheet(pos_data.times, pos_data.y, model='tag14', sc2NS=True)
        self.assertTrue(isinstance(model, np.ndarray))
        model = neutral_sheet(pos_data.times, pos_data.y, model='tag14')
        self.assertTrue(isinstance(model, np.ndarray))

    def test_invalid_model(self):
        with self.assertLogs(level='ERROR') as log:
            model = neutral_sheet(pos_data.times, pos_data.y, model='ff', sc2NS=True)
            self.assertTrue(not isinstance(model, np.ndarray))
            self.assertIn("An invalid neutral sheet model name was used.", log.output[0])


if __name__ == '__main__':
    unittest.main()
